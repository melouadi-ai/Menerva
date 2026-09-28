import json
import struct
import traceback

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
SIGNED_SHORT           = 150
FLOAT_SINGLE_BE        = 250
VM_SOURCE_CODE_DEFAULT = "if elapsed() then    storep(11);else store(8);fi;"
DRIVERCONFIG_MEASURE   = '<configuration SynopticAnalogicFormat=\\"%7.2f\\"/>'
BIG_POS =  3.40282e+38
BIG_NEG = -3.40282e+38

input_json = r''''''

# ---------------------------------------------------------------------------
# SAFE PARSE — handles empty string, "[]", whitespace-only, invalid JSON
# ---------------------------------------------------------------------------
def safe_parse(raw):
    import json
    if not isinstance(raw, str):
        return []
    raw = raw.strip()
    if not raw:
        return []
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return []
    if isinstance(parsed, dict):
        return [parsed]
    if isinstance(parsed, list):
        return parsed
    return []

# ---------------------------------------------------------------------------
# Main Execution Block
# ---------------------------------------------------------------------------
try:
    _parsed_json = safe_parse(input_json)

    if not _parsed_json:
        raise ValueError(
            "Il JSON in input è un array vuoto o non valido. "
            "Verificare che il nodo upstream abbia prodotto output."
        )

    # ── Flatten nested lists ──────────────────────────────────────────────
    data = []
    _stack = [_parsed_json]
    while _stack:
        _curr = _stack.pop()
        if isinstance(_curr, list):
            for _item in reversed(_curr):
                _stack.append(_item)
        elif isinstance(_curr, dict):
            data.append(_curr)

    # ── 1. Split station info from measures ──────────────────────────────
    station_info = None
    measures_raw = []

    for item in data:
        sub = item.get("_subkey", "")
        if sub == "stazione_insert":
            candidate = item["_params"][0]
            if station_info is None or (
                station_info.get("ip_plc") is None
                and candidate.get("ip_plc") is not None
            ):
                station_info = candidate
        elif sub == "misura_insert":
            measures_raw.extend(item["_params"])

    if station_info is None:
        raise ValueError("Nessun blocco 'stazione_insert' trovato nel JSON di input.")

    ip   = station_info.get("ip_plc", "127.0.0.1")
    port = station_info.get("port", 502)

    driverconfig = (
        f'<configuration><commProto>'
        f'<p0 class="Protocollo MODBUS (master) via TCP/IP" '
        f'name="Protocollo MODBUS (master) via TCP/IP" '
        f'ipaddress="{ip}" tcpport="{port}" '
        f'timeout="5000" retries="3" write4XXXX="6"/>'
        f'</commProto><recoveryProto/></configuration>'
    )

    station_id = 1

    # ── 2. Process measures ───────────────────────────────────────────────
    new_measures    = []
    new_bitinfo_raw = []
    packed_reg_to_idx = {}
    new_id_counter = 0

    for m in measures_raw:

        # Classify
        if m.get("analogico"):
            driverdata, type_code, is_analog, is_digital, is_packed = 0, 0, True, False, False
        elif m.get("digit_impaccato"):
            driverdata, type_code, is_analog, is_digital, is_packed = 2, 1, False, True, True
        elif m.get("digit_singolo"):
            driverdata, type_code, is_analog, is_digital, is_packed = 1, 1, False, True, False
        else:
            driverdata, type_code, is_analog, is_digital, is_packed = 0, 0, True, False, False

        raw_reg  = str(m.get("modbus_registro", "0")).strip()
        this_reg = int(raw_reg.split(".")[0]) if raw_reg and raw_reg != "None" else 0
        device   = int(m.get("modbus_id", 1))
        fmt      = FLOAT_SINGLE_BE if is_analog else SIGNED_SHORT
        units    = m.get("unità_misura")
        name     = m.get("nome") or m.get("tag") or "Unknown"
        bit_no   = m.get("bit_posizione")
        stato_on  = m.get("stato_on")
        stato_off = m.get("stato_off")

        # ── 2a. New measure entry or reuse packed ─────────────────────────
        if is_packed and this_reg in packed_reg_to_idx:
            measure_idx = packed_reg_to_idx[this_reg]
        else:
            new_id_counter += 1
            measure_idx = new_id_counter - 1

            display_name = "Ingresso_digitale" if is_packed else name

            _raw_blob = (
                struct.pack("<i", this_reg)
                + struct.pack("<i", 0)
                + struct.pack("<i", 0)
                + struct.pack("<i", 0)
                + struct.pack("<i", device)
                + struct.pack("<i", fmt)
            )
            blob = "0x" + _raw_blob.hex().upper()

            new_measures.append({
                "STATIONID":        station_id,
                "NAME":             display_name[:49],
                "DISABLED":         0,
                "DIGITAL":          None,
                "DOWNLOAD":         0,
                "SNAPSHOT":         1,
                "IGNOREERRORS":     0,
                "LOWCRITICAL":      None if is_digital else BIG_NEG,
                "HIGHCRITICAL":     None if is_digital else BIG_POS,
                "LOWRANGE":         None if is_digital else BIG_NEG,
                "HIGHRANGE":        None if is_digital else BIG_POS,
                "LOWOFFSET":        None if is_digital else BIG_NEG,
                "HIGHOFFSET":       None if is_digital else BIG_POS,
                "SQRAW":            None if is_digital else BIG_POS,
                "SQ1HOURMEAN":      None if is_digital else BIG_POS,
                "SQ3HOURMEAN":      None if is_digital else BIG_POS,
                "SQ8HOURMEAN":      None if is_digital else BIG_POS,
                "SQDAILYMEAN":      None if is_digital else BIG_POS,
                "UNITS":            units,
                "STANDARDRANGEID":  None,
                "DRIVERDATA":       driverdata,
                "TYPE":             type_code,
                "DRIVERPRIVATE":    blob,
                "ONLY_POSITIVES":   0 if is_analog else None,
                "VM_SOURCE_CODE":   VM_SOURCE_CODE_DEFAULT,
                "PERIOD":           5,
                "SNAPSIZE":         1000,
                "DRIVERCONFIG":     DRIVERCONFIG_MEASURE,
                "ID":               new_id_counter,
                "UNITS2":           units,
                "MODBUSREGISTRO":   this_reg,
                "_reg":             this_reg,
                "_device":          device,
                "_fmt":             fmt,
                "_is_digital":      is_digital,
            })

            if is_packed:
                packed_reg_to_idx[this_reg] = measure_idx

        # ── 2b. Bitinfo entry ─────────────────────────────────────────────
        if is_digital:
            effective_bit = int(bit_no) if bit_no is not None else 0

            nm = new_measures[measure_idx]
            _raw_blob2 = (
                struct.pack("<i", nm["_reg"])
                + struct.pack("<i", 0)
                + struct.pack("<i", 0)
                + struct.pack("<i", effective_bit)
                + struct.pack("<i", nm["_device"])
                + struct.pack("<i", nm["_fmt"])
            )
            nm["DRIVERPRIVATE"] = "0x" + _raw_blob2.hex().upper()

            # Guard: stato_on / stato_off may be None for packed measures
            texton  = stato_on.upper()  if isinstance(stato_on,  str) else (stato_on  or "Attivo")
            textoff = stato_off.upper() if isinstance(stato_off, str) else (stato_off or "OFF")

            new_bitinfo_raw.append({
                "BITNO":   effective_bit,
                "BITNAME": name.upper(),
                "TEXTON":  texton,
                "TEXTOFF": textoff,
                "_reg":    this_reg,
            })

    # ── 3. Finalise measure IDs ───────────────────────────────────────────
    packed_name_counter = 0
    reg_to_final_id = {}

    for idx, nm in enumerate(new_measures):
        if "ingresso_digitale" in nm["NAME"].lower():
            packed_name_counter += 1
            nm["NAME"] = f"Ingressi digitali {packed_name_counter}"

        nm["ID"] = idx + 1
        reg_to_final_id[nm["MODBUSREGISTRO"]] = nm["ID"]

        for k in ("_reg", "_device", "_fmt", "_is_digital"):
            nm.pop(k, None)

    # ── 4. Resolve MEASUREID in bitinfo ──────────────────────────────────
    new_bitinfo = []
    for b in new_bitinfo_raw:
        reg = b.pop("_reg")
        b["MEASUREID"] = reg_to_final_id.get(reg)
        new_bitinfo.append(b)

    # ── 5. Assemble final station object ──────────────────────────────────
    result = {
        "NAME":                  station_info.get("nome_stazione", "SME"),
        "DRIVERNAME":            "modbusplc",
        "XPOSITION":             430,
        "YPOSITION":             530,
        "DOWNLOADTYPE":          0,
        "DOWNLOADPROGRAM":       None,
        "IGNOREERRORS":          0,
        "SNAPSHOT":              None,
        "NORMALSNAPSHOT":        1,
        "CRITICSNAPSHOT":        32767,
        "ALARMSNAPSHOT":         32767,
        "SYNOBITMAP":            None,
        "LINENAME":              None,
        "AREACODE":              None,
        "ADDRESS":               None,
        "LINECONFIGURATION":     None,
        "TIMELASTCONFIGURATION": None,
        "TIMELASTDOWNLOAD":      None,
        "EVENTTIME":             None,
        "EVENTCODE":             0,
        "EVENTORIGIN":           None,
        "CODE":                  None,
        "DRIVERPRIVATE":         None,
        "OVERWRITEMEASURES":     1,
        "DRIVERCONFIG":          driverconfig,
        "ID":                    station_id,
        "measures":              new_measures,
        "bitinfo":               new_bitinfo,
    }

    # ── Output ────────────────────────────────────────────────────────────
    output_json = json.dumps(result, indent=2, ensure_ascii=False)
    print(output_json)

    print("\nRegister → Measure ID mapping:")
    for m in result["measures"]:
        print(f"  reg {m['MODBUSREGISTRO']:>6}  →  ID {m['ID']:>4}  ({m['NAME']})")

except Exception as e:
    print("ERROR:\n", traceback.format_exc())