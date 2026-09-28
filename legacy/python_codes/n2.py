import json
import struct
import traceback
import re
 
# Modificato la parte di apici nel DRIVERCONFIG per parlo funzionare correttamente, ora il tag HTML e' dentro apici singoli ('tag')
input_json  = r'''{edge}[5]'''
# Modificato la parte di apici nel DRIVERCONFIG per parlo funzionare correttamente, ora il tag HTML e' dentro apici singoli ('tag')

output_json = []

 
SIGNED_SHORT    = 150
FLOAT_SINGLE_BE = 250
VM_SOURCE_CODE_DEFAULT = "if elapsed() then    storep(11);else store(8);fi;"
DRIVERCONFIG_MEASURE = '<configuration SynopticAnalogicFormat="%7.2f"/>'
BIG_POS =  3.40282e+38
BIG_NEG = -3.40282e+38
 
try:
 
    clean_data = re.sub(
    r'("DRIVERCONFIG"\s*:\s*")(<.*?/>)(")',
    lambda m: m.group(1) + m.group(2).replace('"', '\\"') + m.group(3),
    input_json,
    flags=re.DOTALL
    )

    input_data = json.loads(clean_data)
    input_data = input_data[0]
    # Appiattisce il json
    stations_raw = []
    for item in input_data:
        if isinstance(item, list):
            stations_raw.extend(item) # prende elementi dentro se è list
        else:
            stations_raw.append(item)
 
    result = []
    measure_id_counter = 1
 
    for idx, raw_station in enumerate(stations_raw, start=1):
        station_id = idx
 
        # -- Estrai ip e porta dal DRIVERCONFIG intermedio -------------------
        raw_dc = raw_station.get("DRIVERCONFIG", "")
 
        m_ip   = re.search(r'ipaddress=[\'"]([^\'"]+)[\'"]', raw_dc)
        m_port = re.search(r'tcpport=[\'"]([^\'"]+)[\'"]', raw_dc)
        ip     = m_ip.group(1)   if m_ip   else "127.0.0.1"
        port   = m_port.group(1) if m_port else "502"
 
        #  Costruisci DRIVERCONFIG
        driverconfig = (
        '<configuration><commProto>'
        '<p0 class="Protocollo MODBUS (master) via TCP/IP"'   # fixed: quotes around class value
        ' name="Protocollo MODBUS (master) via TCP/IP"'
        ' ipaddress="' + ip + '" tcpport="' + port + '"'
        ' timeout="5000" retries="3" write4XXXX="6"/>'
        '</commProto><recoveryProto/></configuration>'
    )
        
        
        # Conversione misure
        old_bitinfo  = raw_station.get("bitinfo",  [])
 
        old_id_to_new_id = {} # x mappare
        new_measures     = []
        mid  = measure_id_counter
 
        for m in raw_station.get("measures", []):
 
            driverdata = m.get("DRIVERDATA", 0)
            type_code  = m.get("TYPE", 0)
 
            # Is_packed inteso e' impaccato?
            is_analog  = (driverdata == 0)
            is_packed  = (driverdata == 2)
            is_digital = (driverdata == 1) or is_packed
 
            litt_end = FLOAT_SINGLE_BE if is_analog else SIGNED_SHORT
 
            # Registro: stringa "40001" o "40001.8" -> int
            raw_reg = m.get("MODBUSREGISTRO")
            if raw_reg is not None:
                this_reg = int(str(raw_reg).strip().split(".")[0]) 
            else:
                this_reg = 0
 
            # Device (slave id): campo opzionale nel JSON intermedio
            device = m.get("MODBUSID") or m.get("MODBUS_ID") or 1
 
            # DRIVERPRIVATE con bit_no=0 (aggiornato dopo con i bitinfo)
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
 
            new_measures.append({
                "STATIONID":        station_id,
                "NAME":             m.get("NAME"),
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
                "ID":               mid,
                "UNITS2":           units,
                "_reg":             this_reg,
                "_device":          device,
                "_fmt":             litt_end,
                "_is_digital":      is_digital,
            })
 
            old_id_to_new_id[m["ID"]] = mid
            mid += 1
 
        measure_id_counter = mid
 
        # Indice misure per lookup new_id -> misura
        measure_by_new_id = {nm["ID"]: nm for nm in new_measures}
 
        # -- Converti bitinfo e aggiorna DRIVERPRIVATE con il BITNO reale ----
        new_bitinfo = []
 
        for b in old_bitinfo:
            old_mid = b.get("MEASUREID")
            new_mid = old_id_to_new_id.get(old_mid, old_mid)
            bit_no  = int(b.get("BITNO", 0))
 
            nm = measure_by_new_id.get(new_mid)
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
 
            new_bitinfo.append({
                "MEASUREID": new_mid,
                "BITNO":     bit_no,
                "BITNAME":   b.get("BITNAME"),
                "TEXTON":    b.get("TEXTON"),
                "TEXTOFF":   b.get("TEXTOFF"),
            })
 
        # -- Rimuovi campi interni dalle misure ------------------------------
        for nm in new_measures:
            del nm["_reg"]
            del nm["_device"]
            del nm["_fmt"]
            del nm["_is_digital"]
 
        # -- Assembla la stazione --------------------------------------------
        result.append({
            "NAME":                  raw_station.get("NAME", "SME"),
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
    print(result[0]['DRIVERCONFIG'])
 
except Exception as e:
    error_msg = traceback.format_exc()
    error_report = [{
        "err":             str(e),
        "trace":           error_msg,
        "input_originale": input_json
    }]
    output_json = json.dumps(error_report, indent=2, ensure_ascii=False)
    print(output_json)