import json
import struct
import traceback
import re

# Modificato la parte di apici nel DRIVERCONFIG per farlo funzionare correttamente
input_json = r'''{edge}[5]'''

output_json = []

input_json = input_json.replace("```json", "").replace("```", "").strip()

SIGNED_SHORT    = 150
FLOAT_SINGLE_BE = 250
VM_SOURCE_CODE_DEFAULT = "if elapsed() then    storep(11);else store(8);fi;"
DRIVERCONFIG_MEASURE = '<configuration SynopticAnalogicFormat=\\"%7.2f\\"/>'
BIG_POS =  3.40282e+38
BIG_NEG = -3.40282e+38

try:
    input_json = input_json.replace("```json", "").replace("```", "").strip()

    pattern = r'("\w+"\s*:\s*")(.*?)("\s*(?:,|}|\]))'

    clean_data = re.sub(
        pattern,
        lambda m: m.group(1) + m.group(2).replace('"', "'") + m.group(3),
        input_json,
        flags=re.DOTALL
    )

    input_data = json.loads(input_json)

    # Appiattisce il json
    stations_raw = []
    for item in input_data:
        if isinstance(item, list):
            stations_raw.extend(item)
        else:
            stations_raw.append(item)

    # ----------------------------------------------------------------
    # PRE-ELABORAZIONE NOMI: calcola i nomi finali di ogni stazione
    # gestendo i duplicati in modo incrementale.
    # Prima occorrenza → nome originale (es. "Forno")
    # Seconda          → "Forno 1"
    # Terza            → "Forno 2"  … e così via
    # ----------------------------------------------------------------
    name_list_stations = ['punto emissivo', 'camino', 'emissione', 'sae']

    # 1° passata: determina il nome "base" di ogni stazione
    base_names = []
    for raw_station in stations_raw:
        raw_name = raw_station.get("NAME", "SME")
        found = False
        for word in name_list_stations:
            if word in raw_name.lower():
                found = True
                break
        base_names.append(raw_name if found else "SME")

    # 2° passata: costruisce i nomi finali con suffisso incrementale
    name_occurrence = {}   # nome_base -> quante volte visto finora
    final_names = []
    for base in base_names:
        count = name_occurrence.get(base, 0)
        if count == 0:
            final_names.append(base)          # prima occorrenza: nessun suffisso
        else:
            final_names.append(f"{base} {count}")  # seconda → "Nome 1", terza → "Nome 2" …
        name_occurrence[base] = count + 1
    # ----------------------------------------------------------------

    result = []

    for idx, raw_station in enumerate(stations_raw, start=1):

        # ----------------------------------------------------------------
        # FIX BUG 1: station_id unico per ogni stazione, non bloccato a 1
        # ----------------------------------------------------------------
        station_id = idx

        # -- Estrai ip e porta dal DRIVERCONFIG intermedio -----------------
        raw_dc = raw_station.get("DRIVERCONFIG", "").split(":")

        ip   = raw_dc[0] if raw_dc[0] else "127.0.0.1"
        port = raw_dc[1] if len(raw_dc) > 1 and raw_dc[1] else "502"

        # Costruisci DRIVERCONFIG
        driverconfig = (
            f'<configuration><commProto>'
            f'<p0 class="Protocollo MODBUS (master) via TCP/IP" '
            f'name="Protocollo MODBUS (master) via TCP/IP" '
            f'ipaddress="{ip}" tcpport="{port}" '
            f'timeout="5000" retries="3" write4XXXX="6"/>'
            f'</commProto><recoveryProto/></configuration>'
        )

        # Conversione misure
        old_id_to_new_id    = {}
        new_measures        = []
        new_id_measure      = 1

        new_measureid_bitinfo = {}
        name_count  = {}
        last_reg    = None
        last_saved_mid = None

        # Il nome finale è già stato calcolato nella pre-elaborazione
        station_name = final_names[idx - 1]

        for m in raw_station.get("measures", []):
            reg_to_new_id = {}

            driverdata = m.get("DRIVERDATA", 0)
            type_code  = m.get("TYPE", 0)

            is_analog  = (driverdata == 0)
            is_packed  = (driverdata == 2)
            is_digital = (driverdata == 1 or driverdata == 5) or is_packed

            litt_end = FLOAT_SINGLE_BE if is_analog else SIGNED_SHORT

            raw_reg = m.get("MODBUSREGISTRO") or m.get("MODBUSREGISTER")

            if raw_reg is not None and int(str(raw_reg).strip().split(".")[0]) != 0:
                this_reg = int(str(raw_reg).strip().split(".")[0])
            else:
                this_reg = 0

            impaccato = (this_reg != 0) and (last_reg == this_reg)

            if not impaccato:

                mid    = m.get('MODBUSREGISTRO') or m.get('MODBUSREGISTER')
                device = m.get("MODBUSID") or m.get("MODBUS_ID") or 1

                new_id_measure += 1

                blob = (
                    struct.pack("<i", this_reg)
                    + struct.pack("<i", 0)
                    + struct.pack("<i", 0)
                    + struct.pack("<i", 0)
                    + struct.pack("<i", device)
                    + struct.pack("<i", litt_end)
                )
                dp_blob = "0x" + blob.hex().upper()

                units = m.get("UNITS")

                if m.get("NAME") and (not 'disponibile' in m.get("NAME").lower()):
                    raw_name = m.get("NAME") if not m.get("GROUP", False) else m.get("GROUP")

                    new_measures.append({
                        "STATIONID":        station_id,
                        "NAME":             raw_name[:49],
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
                        "DRIVERPRIVATE":    dp_blob,
                        "ONLY_POSITIVES":   0 if is_analog else None,
                        "VM_SOURCE_CODE":   VM_SOURCE_CODE_DEFAULT,
                        "PERIOD":           5,
                        "SNAPSIZE":         1000,
                        "DRIVERCONFIG":     DRIVERCONFIG_MEASURE,
                        "ID":               new_id_measure,
                        "UNITS2":           units,
                        "_reg":             this_reg,
                        "_device":          device,
                        "_fmt":             litt_end,
                        "_is_digital":      is_digital,
                        "MODBUSREGISTRO":   m.get("MODBUSREGISTRO") or m.get('MODBUSREGISTER')
                    })

                    old_id_to_new_id[m["ID"]] = mid
                    reg_to_new_id[this_reg]   = mid

                    if this_reg != 0:
                        last_reg = this_reg
                    last_saved_mid = mid
                    new_measureid_bitinfo[this_reg] = new_id_measure

                else:
                    new_id_measure -= 1

            else:
                old_id_to_new_id[m["ID"]] = last_saved_mid
                new_measureid_bitinfo[this_reg] = new_id_measure

        # Indice misure per lookup new_id -> misura
        measure_by_new_id = {nm["ID"]: nm for nm in new_measures}

        # -- Converti bitinfo e aggiorna DRIVERPRIVATE con il BITNO reale --
        new_bitinfo = []

        for b in raw_station.get("bitinfo", []):
            old_mid = b.get("MEASUREID")
            new_mid = old_id_to_new_id.get(old_mid)

            if new_mid is None:
                new_mid = reg_to_new_id.get(old_mid, False)

            bit_no  = int(b.get("BITNO", 0))
            txt_on  = b.get('TEXTON', '')
            txt_off = b.get("TEXTOFF", '')
            nm      = measure_by_new_id.get(new_mid)

            if nm and nm["_is_digital"]:
                blob_upd = (
                    struct.pack("<i", nm["_reg"])
                    + struct.pack("<i", 0)
                    + struct.pack("<i", 0)
                    + struct.pack("<i", bit_no)
                    + struct.pack("<i", nm["_device"])
                    + struct.pack("<i", nm["_fmt"])
                )
                nm["DRIVERPRIVATE"] = "0x" + blob_upd.hex().upper()

            bitname = b.get('BITNAME', '')
            if not 'disponibile' in str(bitname).lower():
                new_bitinfo.append({
                    "MEASUREID": new_measureid_bitinfo.get(b.get("MEASUREID")),
                    "BITNO":     bit_no,
                    "BITNAME":   str(bitname).upper(),
                    "TEXTON":    str(txt_on).upper(),
                    "TEXTOFF":   "RANGE ALTO" if txt_on.lower().strip() == 'range basso' else str(txt_off).upper(),
                    "_pippo":    b.get("MEASUREID")   # rimosso dopo la rinumerazione
                })

        # -- Rimuovi campi interni dalle misure ----------------------------
        for nm in new_measures:
            del nm["_reg"]
            del nm["_device"]
            del nm["_fmt"]
            del nm["_is_digital"]

        # ----------------------------------------------------------------
        # FIX BUG 2+3: rinumerazione ID misure e MEASUREID bitinfo
        # eseguita PER STAZIONE, non su tutto il risultato appiattito
        # ----------------------------------------------------------------
        new_measure_id_dict = {}
        n_digitale = 0

        for id_num, m in enumerate(new_measures, start=1):
            if "ingresso_digitale" in str(m.get("NAME")).lower():
                n_digitale += 1
                m["NAME"] = f"Ingressi digitali {n_digitale}"

            old_mid_val      = m.get('MODBUSREGISTRO')
            m['ID']          = id_num
            m['STATIONID']   = station_id   # assicura che ogni misura abbia l'ID della propria stazione
            new_measure_id_dict[old_mid_val] = id_num
            del m['MODBUSREGISTRO']

        for b in new_bitinfo:
            b['MEASUREID'] = new_measure_id_dict.get(b.get('_pippo'))
            del b['_pippo']

        # -- Assembla la stazione -----------------------------------------
        result.append({
            "NAME":                  station_name,   # nome con eventuale suffisso incrementale
            "DRIVERNAME":            raw_station.get("DRIVERNAME", "modbusplc"),
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
        })



    output_json = json.dumps(result, indent=2, ensure_ascii=False)
    print('--------------')
    print(f"[INFO] Stazioni prodotte: {len(result)}")
    for s in result:
        print(f"  Station {s['ID']} ({s['NAME']}) ({s['DRIVERCONFIG'][:60]}...): "
              f"{len(s['measures'])} misure, {len(s['bitinfo'])} bitinfo")

except Exception as e:
    error_msg = traceback.format_exc()
    error_report = [{
        "err":   str(e),
        "trace": error_msg
    }]
    output_json = json.dumps(error_report, indent=2, ensure_ascii=False)
    print(output_json)