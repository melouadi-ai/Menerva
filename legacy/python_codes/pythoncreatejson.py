import json
import struct
import traceback
import re
 
# Modificato la parte di apici nel DRIVERCONFIG per parlo funzionare correttamente, ora il tag HTML e' dentro apici singoli ('tag')
input_json = r'''edge'''


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
            stations_raw.extend(item) # prende elementi dentro se è list
        else:
            stations_raw.append(item)
 
    result = []
    flag_station = False
    
    for idx, raw_station in enumerate(stations_raw, start=1):
 
        # Check per la singola stazione
        # Prendo solamente la prima stazione
        if not flag_station:
          station_id = idx
          flag_station = True 
 
        # -- Estrai ip e porta dal DRIVERCONFIG intermedio -------------------
        raw_dc = raw_station.get("DRIVERCONFIG", "").split(":")
 
        # # Cerca all'interno dei tag <Address> e <Port>
        # m_ip   = re.search(r'<IP>[\'"]?(.*?)[\'"]?</IP>', raw_dc)
        # m_port = re.search(r'<Port>(\d+)</Port>', raw_dc)
        
        ip     = raw_dc[0]   if raw_dc[0]    else "127.0.0.1"
        port   = raw_dc[1] if raw_dc[1]  else "502"
 
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
 
        old_id_to_new_id = {}
        new_measures     = []
        new_id_measure = 1
                
        new_measureid_bitinfo = {}
        name_count = {}
        last_reg = None 
        last_saved_mid = None
        
        raw_station["NAME"] = "SME"
 
        for m in raw_station.get("measures", []):
            reg_to_new_id = {}
 
            driverdata = m.get("DRIVERDATA", 0)
            type_code  = m.get("TYPE", 0)
 
            # Is_packed inteso e' impaccato?
            is_analog  = (driverdata == 0)
            is_packed  = (driverdata == 2)
            is_digital = (driverdata == 1) or is_packed
 
            litt_end = FLOAT_SINGLE_BE if is_analog else SIGNED_SHORT
 
            # Registro: stringa "40001" o "40001.8" -> int
            raw_reg = m.get("MODBUSREGISTRO") or m.get("MODBUSREGISTER")

            if raw_reg is not None and int(str(raw_reg).strip().split(".")[0]) != 0:
                this_reg = int(str(raw_reg).strip().split(".")[0])
            else:
                this_reg = 0  # fallback sull'ID quando MODBUSREGISTRO=0
                          
            impaccato = (this_reg != 0) and (last_reg == this_reg)
            
            if not impaccato:
                  
                mid = m.get('MODBUSREGISTRO') or m.get('MODBUSREGISTER')
                # Device (slave id): campo opzZonale nel JSON intermedio
                device = m.get("MODBUSID") or m.get("MODBUS_ID") or 1
    
                new_id_measure += 1

                # DRIVERPRIVATE con bit_no=0 (aggiornato dopo con i bitinfo)
                blob = (
                    struct.pack("<i", this_reg ) # Gestione del dato analogico senza valore Impaccato
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
                  
                  # # Vecchia gestione per il nome dell'impaccato
                  # if raw_name not in name_count:
                  #     name_count[raw_name] = 0
                  #     final_name = raw_name
                  # else:
                  #     name_count[raw_name] += 1
                  #     final_name = f"{raw_name}_{name_count[raw_name]}"
                      
                  new_measures.append({
                      "STATIONID":        station_id,
                      "NAME":             raw_name[:29],
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
                  reg_to_new_id[this_reg] = mid         # mapping via numero registro (per i bitinfo)

                  if this_reg != 0:
                    last_reg = this_reg
                  last_saved_mid = mid
                  new_measureid_bitinfo[this_reg] = new_id_measure

                else:
                  new_id_measure -= 1

            else:
                # IMPORTANTISSIMO: Se la misura è impaccata (quindi la ignoriamo e 
                # non facciamo l'append), dobbiamo comunque mappare il suo vecchio ID
                # in modo che i bitinfo vadano a finire sulla misura "master" creata prima!
                old_id_to_new_id[m["ID"]] = last_saved_mid
                new_measureid_bitinfo[this_reg] = new_id_measure
                
         # Indice misure per lookup new_id -> misura
        measure_by_new_id = {nm["ID"]: nm for nm in new_measures}
 
        # -- Converti bitinfo e aggiorna DRIVERPRIVATE con il BITNO reale ----
        new_bitinfo = []

 
        for measureid, b in enumerate(raw_station.get("bitinfo",  [])):
            old_mid = b.get("MEASUREID")
            new_mid = old_id_to_new_id.get(old_mid)
            
            if new_mid is None:
                new_mid = reg_to_new_id.get(old_mid, False)          
                
            bit_no  = int(b.get("BITNO", 0))
            txt_on = b['TEXTON']
            
            txt_off = b["TEXTOFF"]
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

            if not 'disponibile' in b.get('BITNAME').lower():
              new_bitinfo.append({
                  "MEASUREID": new_measureid_bitinfo.get(b.get("MEASUREID")),
                  "BITNO":     bit_no,
                  "BITNAME":   str(b.get("BITNAME")).upper(),
                  "TEXTON":    b.get('TEXTON').upper(),
                  "TEXTOFF": "RANGE ALTO" if b.get('TEXTON', '').lower().strip() == 'range basso' else b.get('TEXTOFF', '').upper(),
                  "pippo": b.get("MEASUREID")
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
 
    measures_doc = []
    bitinfo_doc = []
    
    for doc in result:
        measures_doc.extend(doc.get('measures',[]))
        bitinfo_doc.extend(doc.get('bitinfo'))
        doc.pop('measures', None)
        doc.pop('bitinfo', None)
     
    result = result[0]
    
    result['measures'] = measures_doc
    result['bitinfo'] = bitinfo_doc
 
    # Implementazione per la gestione multipla dei nomi degli impaccati
    new_measure_id_dict = {}
    n = 0
    for id_num, m in enumerate(result.get("measures")):
      
      if "ingresso_digitale" in str(m.get("NAME")).lower():
        n += 1
        new_name = f"Ingressi digitali {n}"
        m["NAME"] = new_name
        
      m['ID'] = id_num + 1
      new_measure_id_dict[m.get('MODBUSREGISTRO')] = m.get('ID')
    
      del m['MODBUSREGISTRO']
 
    for b in result.get('bitinfo'):
      b['MEASUREID'] = new_measure_id_dict.get(b.get('pippo'))
      del b['pippo']
     
              
    output_json = json.dumps(result, indent=2, ensure_ascii=False)
    print('--------------')
    # print(output_json)  

    for k,v in new_measure_id_dict.items():
      print(k,v)
      
    
    with open('localoutput28page2.json', 'w') as file:
        json.dump(result, file, ensure_ascii=False, indent=4)
    
except Exception as e:
    error_msg = traceback.format_exc()
    error_report = [{
        "err":             str(e),
        "trace":           error_msg
    }]
    output_json = json.dumps(error_report, indent=2, ensure_ascii=False)
    print(output_json)