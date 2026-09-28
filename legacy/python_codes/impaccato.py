import json
import struct
import traceback
import re
 
# Modificato la parte di apici nel DRIVERCONFIG per parlo funzionare correttamente, ora il tag HTML e' dentro apici singoli ('tag')
input_json  = r'''[[
    {
        "NAME": "IKW",
        "DRIVERNAME": "modbusplc",
        "DRIVERCONFIG": "<p0 class="Protocollo MODBUS (master) via TCP/IP" name="Protocollo MODBUS (master) via TCP/IP" ipaddress="192.168.0.1" tcpport="502" timeout="5000" retries="3" write4XXXX="6"/>",
        "ID": 1,
        "measures": [
            {
                "STATIONID": 1,
                "NAME": "Allarme Generatore H2",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 1,
                "MODBUSREGISTRO": 40001
            },
            {
                "STATIONID": 1,
                "NAME": "Allarme FID6_01",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 2,
                "MODBUSREGISTRO": 40001
            },
            {
                "STATIONID": 1,
                "NAME": "Richiesta Manutenzione FID6_01",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 3,
                "MODBUSREGISTRO": 40001
            },
            {
                "STATIONID": 1,
                "NAME": "Calibrazione FID6_01",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 4,
                "MODBUSREGISTRO": 40001
            },
            {
                "STATIONID": 1,
                "NAME": "Range Di Misura Alto FID6_01",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 5,
                "MODBUSREGISTRO": 40001
            },
            {
                "STATIONID": 1,
                "NAME": "Allarme FID6_02",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 6,
                "MODBUSREGISTRO": 40001
            },
            {
                "STATIONID": 1,
                "NAME": "Richiesta Manutenzione FID6_02",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 7,
                "MODBUSREGISTRO": 40001
            },
            {
                "STATIONID": 1,
                "NAME": "Calibrazione FID6_02",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 8,
                "MODBUSREGISTRO": 40001
            },
            {
                "STATIONID": 1,
                "NAME": "Allarme Sensore H2",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 9,
                "MODBUSREGISTRO": 40001
            },
            {
                "STATIONID": 1,
                "NAME": "Soglia 1 Sensore H2",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 10,
                "MODBUSREGISTRO": 40001
            },
            {
                "STATIONID": 1,
                "NAME": "Soglia 2 Sensore H2",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 11,
                "MODBUSREGISTRO": 40001
            },
            {
                "STATIONID": 1,
                "NAME": "Allarme Sonda Di Prelievo_E01",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 12,
                "MODBUSREGISTRO": 40001
            },
            {
                "STATIONID": 1,
                "NAME": "Allarme Linea Riscaldata EH_01",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 13,
                "MODBUSREGISTRO": 40001
            },
            {
                "STATIONID": 1,
                "NAME": "Allarme Sonda Di Prelievo_E02",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 14,
                "MODBUSREGISTRO": 40001
            },
            {
                "STATIONID": 1,
                "NAME": "Allarme Linea Riscaldata EH_02",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 15,
                "MODBUSREGISTRO": 40001
            },
            {
                "STATIONID": 1,
                "NAME": "Allarme Purificatore Aria",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 16,
                "MODBUSREGISTRO": 40001
            },
            {
                "STATIONID": 1,
                "NAME": "Range Di Misura Alto FID6_02",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 17,
                "MODBUSREGISTRO": 40002
            },
            {
                "STATIONID": 1,
                "NAME": "Manutenzione Sistema 01",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 18,
                "MODBUSREGISTRO": 40002
            },
            {
                "STATIONID": 1,
                "NAME": "Manutenzione Sistema 02",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 19,
                "MODBUSREGISTRO": 40002
            },
            {
                "STATIONID": 1,
                "NAME": "Allarme Alta Temperatura Quadro",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 20,
                "MODBUSREGISTRO": 40002
            },
            {
                "STATIONID": 1,
                "NAME": "Relè OUT OR Allarmi_01",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 21,
                "MODBUSREGISTRO": 40003
            },
            {
                "STATIONID": 1,
                "NAME": "Relè OUT OR Allarmi_02",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 22,
                "MODBUSREGISTRO": 40003
            },
            {
                "STATIONID": 1,
                "NAME": "CMD Zero FID6_01",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 23,
                "MODBUSREGISTRO": 40003
            },
            {
                "STATIONID": 1,
                "NAME": "CMD Misura FID6_01",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 24,
                "MODBUSREGISTRO": 40003
            },
            {
                "STATIONID": 1,
                "NAME": "CMD Zero FID6_02",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 25,
                "MODBUSREGISTRO": 40003
            },
            {
                "STATIONID": 1,
                "NAME": "CMD Misura FID6_02",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 26,
                "MODBUSREGISTRO": 40003
            },
            {
                "STATIONID": 1,
                "NAME": "Lampada Manutenzione_01",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 27,
                "MODBUSREGISTRO": 40003
            },
            {
                "STATIONID": 1,
                "NAME": "Lampada OR Allarmi_01",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 28,
                "MODBUSREGISTRO": 40003
            },
            {
                "STATIONID": 1,
                "NAME": "Lampada Manutenzione_02",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 29,
                "MODBUSREGISTRO": 40003
            },
            {
                "STATIONID": 1,
                "NAME": "Lampada OR Allarmi_02",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 30,
                "MODBUSREGISTRO": 40003
            },
            {
                "STATIONID": 1,
                "NAME": "FID6_01 In Protezione",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 31,
                "MODBUSREGISTRO": 40004
            },
            {
                "STATIONID": 1,
                "NAME": "FID6_02 In Protezione",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 32,
                "MODBUSREGISTRO": 40004
            },
            {
                "STATIONID": 1,
                "NAME": "OVF COT_01",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 33,
                "MODBUSREGISTRO": 40007
            },
            {
                "STATIONID": 1,
                "NAME": "OVF COT_02",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 34,
                "MODBUSREGISTRO": 40007
            },
            {
                "STATIONID": 1,
                "NAME": "OVF Misura Disponibile IW36",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 35,
                "MODBUSREGISTRO": 40007
            },
            {
                "STATIONID": 1,
                "NAME": "OVF Misura Disponibile IW38",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 36,
                "MODBUSREGISTRO": 40007
            },
            {
                "STATIONID": 1,
                "NAME": "RC COT_01",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 37,
                "MODBUSREGISTRO": 40007
            },
            {
                "STATIONID": 1,
                "NAME": "RC COT_02",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 38,
                "MODBUSREGISTRO": 40007
            },
            {
                "STATIONID": 1,
                "NAME": "Misura COT_01",
                "UNITS": "mg/Nm3",
                "DRIVERDATA": 0,
                "TYPE": 0,
                "ID": 39,
                "MODBUSREGISTRO": 40008
            },
            {
                "STATIONID": 1,
                "NAME": "Misura COT_02",
                "UNITS": "mg/Nm3",
                "DRIVERDATA": 0,
                "TYPE": 0,
                "ID": 40,
                "MODBUSREGISTRO": 40012
            },
            {
                "STATIONID": 1,
                "NAME": "Misura Disponibile IW36",
                "UNITS": null,
                "DRIVERDATA": 0,
                "TYPE": 0,
                "ID": 41,
                "MODBUSREGISTRO": 40016
            },
            {
                "STATIONID": 1,
                "NAME": "Misura Disponibile IW38",
                "UNITS": null,
                "DRIVERDATA": 0,
                "TYPE": 0,
                "ID": 42,
                "MODBUSREGISTRO": 40020
            },
            {
                "STATIONID": 1,
                "NAME": "Live PLC",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 43,
                "MODBUSREGISTRO": 40032
            }
        ],
        "bitinfo": [
            {
                "MEASUREID": 1,
                "BITNO": 0,
                "BITNAME": "Allarme Generatore H2",
                "TEXTON": "Da Definire",
                "TEXTOFF": "OK"
            },
            {
                "MEASUREID": 2,
                "BITNO": 1,
                "BITNAME": "Allarme FID6_01",
                "TEXTON": "OK",
                "TEXTOFF": "OK"
            },
            {
                "MEASUREID": 3,
                "BITNO": 2,
                "BITNAME": "Richiesta Manutenzione FID6_01",
                "TEXTON": "Manutenzione",
                "TEXTOFF": "OK"
            },
            {
                "MEASUREID": 4,
                "BITNO": 3,
                "BITNAME": "Calibrazione FID6_01",
                "TEXTON": "Calibrazione",
                "TEXTOFF": "OK"
            },
            {
                "MEASUREID": 5,
                "BITNO": 4,
                "BITNAME": "Range Di Misura Alto FID6_01",
                "TEXTON": "Range Basso",
                "TEXTOFF": "OK"
            },
            {
                "MEASUREID": 6,
                "BITNO": 5,
                "BITNAME": "Allarme FID6_02",
                "TEXTON": "OK",
                "TEXTOFF": "OK"
            },
            {
                "MEASUREID": 7,
                "BITNO": 6,
                "BITNAME": "Richiesta Manutenzione FID6_02",
                "TEXTON": "Manutenzione",
                "TEXTOFF": "OK"
            },
            {
                "MEASUREID": 8,
                "BITNO": 7,
                "BITNAME": "Calibrazione FID6_02",
                "TEXTON": "Calibrazione",
                "TEXTOFF": "OK"
            },
            {
                "MEASUREID": 9,
                "BITNO": 8,
                "BITNAME": "Allarme Sensore H2",
                "TEXTON": "Da Definire",
                "TEXTOFF": "OK"
            },
            {
                "MEASUREID": 10,
                "BITNO": 9,
                "BITNAME": "Soglia 1 Sensore H2",
                "TEXTON": "Da Definire",
                "TEXTOFF": "OK"
            },
            {
                "MEASUREID": 11,
                "BITNO": 10,
                "BITNAME": "Soglia 2 Sensore H2",
                "TEXTON": "Da Definire",
                "TEXTOFF": "OK"
            },
            {
                "MEASUREID": 12,
                "BITNO": 11,
                "BITNAME": "Allarme Sonda Di Prelievo_E01",
                "TEXTON": "OK",
                "TEXTOFF": "OK"
            },
            {
                "MEASUREID": 13,
                "BITNO": 12,
                "BITNAME": "Allarme Linea Riscaldata EH_01",
                "TEXTON": "OK",
                "TEXTOFF": "OK"
            },
            {
                "MEASUREID": 14,
                "BITNO": 13,
                "BITNAME": "Allarme Sonda Di Prelievo_E02",
                "TEXTON": "OK",
                "TEXTOFF": "OK"
            },
            {
                "MEASUREID": 15,
                "BITNO": 14,
                "BITNAME": "Allarme Linea Riscaldata EH_02",
                "TEXTON": "OK",
                "TEXTOFF": "OK"
            },
            {
                "MEASUREID": 16,
                "BITNO": 15,
                "BITNAME": "Allarme Purificatore Aria",
                "TEXTON": "Da Definire",
                "TEXTOFF": "OK"
            },
            {
                "MEASUREID": 17,
                "BITNO": 0,
                "BITNAME": "Range Di Misura Alto FID6_02",
                "TEXTON": "Range Basso",
                "TEXTOFF": "OK"
            },
            {
                "MEASUREID": 18,
                "BITNO": 1,
                "BITNAME": "Manutenzione Sistema 01",
                "TEXTON": "Manutenzione",
                "TEXTOFF": "OK"
            },
            {
                "MEASUREID": 19,
                "BITNO": 2,
                "BITNAME": "Manutenzione Sistema 02",
                "TEXTON": "Manutenzione",
                "TEXTOFF": "OK"
            },
            {
                "MEASUREID": 20,
                "BITNO": 3,
                "BITNAME": "Allarme Alta Temperatura Quadro",
                "TEXTON": "OK",
                "TEXTOFF": "OK"
            },
            {
                "MEASUREID": 21,
                "BITNO": 0,
                "BITNAME": "Relè OUT OR Allarmi_01",
                "TEXTON": "OK",
                "TEXTOFF": "OK"
            },
            {
                "MEASUREID": 22,
                "BITNO": 1,
                "BITNAME": "Relè OUT OR Allarmi_02",
                "TEXTON": "OK",
                "TEXTOFF": "OK"
            },
            {
                "MEASUREID": 23,
                "BITNO": 8,
                "BITNAME": "CMD Zero FID6_01",
                "TEXTON": "OK",
                "TEXTOFF": "OK"
            },
            {
                "MEASUREID": 24,
                "BITNO": 9,
                "BITNAME": "CMD Misura FID6_01",
                "TEXTON": "OK",
                "TEXTOFF": "OK"
            },
            {
                "MEASUREID": 25,
                "BITNO": 10,
                "BITNAME": "CMD Zero FID6_02",
                "TEXTON": "OK",
                "TEXTOFF": "OK"
            },
            {
                "MEASUREID": 26,
                "BITNO": 11,
                "BITNAME": "CMD Misura FID6_02",
                "TEXTON": "OK",
                "TEXTOFF": "OK"
            },
            {
                "MEASUREID": 27,
                "BITNO": 12,
                "BITNAME": "Lampada Manutenzione_01",
                "TEXTON": "Manutenzione",
                "TEXTOFF": "OK"
            },
            {
                "MEASUREID": 28,
                "BITNO": 13,
                "BITNAME": "Lampada OR Allarmi_01",
                "TEXTON": "Allarme",
                "TEXTOFF": "OK"
            },
            {
                "MEASUREID": 29,
                "BITNO": 14,
                "BITNAME": "Lampada Manutenzione_02",
                "TEXTON": "Manutenzione",
                "TEXTOFF": "OK"
            },
            {
                "MEASUREID": 30,
                "BITNO": 15,
                "BITNAME": "Lampada OR Allarmi_02",
                "TEXTON": "Allarme",
                "TEXTOFF": "OK"
            },
            {
                "MEASUREID": 31,
                "BITNO": 10,
                "BITNAME": "FID6_01 In Protezione",
                "TEXTON": "Protezione Attiva",
                "TEXTOFF": "OK"
            },
            {
                "MEASUREID": 32,
                "BITNO": 11,
                "BITNAME": "FID6_02 In Protezione",
                "TEXTON": "Protezione Attiva",
                "TEXTOFF": "OK"
            },
            {
                "MEASUREID": 33,
                "BITNO": 0,
                "BITNAME": "OVF COT_01",
                "TEXTON": "Errore",
                "TEXTOFF": "OK"
            },
            {
                "MEASUREID": 34,
                "BITNO": 1,
                "BITNAME": "OVF COT_02",
                "TEXTON": "Errore",
                "TEXTOFF": "OK"
            },
            {
                "MEASUREID": 35,
                "BITNO": 2,
                "BITNAME": "OVF Misura Disponibile IW36",
                "TEXTON": "Errore",
                "TEXTOFF": "OK"
            },
            {
                "MEASUREID": 36,
                "BITNO": 3,
                "BITNAME": "OVF Misura Disponibile IW38",
                "TEXTON": "Errore",
                "TEXTOFF": "OK"
            },
            {
                "MEASUREID": 37,
                "BITNO": 8,
                "BITNAME": "RC COT_01",
                "TEXTON": "Errore",
                "TEXTOFF": "OK"
            },
            {
                "MEASUREID": 38,
                "BITNO": 9,
                "BITNAME": "RC COT_02",
                "TEXTON": "Errore",
                "TEXTOFF": "OK"
            },
            {
                "MEASUREID": 43,
                "BITNO": 0,
                "BITNAME": "Live PLC",
                "TEXTON": "Contatore da 0-999",
                "TEXTOFF": "OK"
            }
        ]
    }
]]'''
 
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
 
        old_id_to_new_id = {}
        new_measures     = []
        mid  = measure_id_counter
        
        last_reg = None 
        last_saved_mid = None
 
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
                
            impaccato = (last_reg == this_reg)
 
            if not impaccato:
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

                last_reg = this_reg
                last_saved_mid = mid
                mid += 1
            
            else:
                # IMPORTANTISSIMO: Se la misura è impaccata (quindi la ignoriamo e 
                # non facciamo l'append), dobbiamo comunque mappare il suo vecchio ID
                # in modo che i bitinfo vadano a finire sulla misura "master" creata prima!
                old_id_to_new_id[m["ID"]] = last_saved_mid
                
 
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
    print(output_json)
 
except Exception as e:
    error_msg = traceback.format_exc()
    error_report = [{
        "err":             str(e),
        "trace":           error_msg,
        "input_originale": input_json
    }]
    output_json = json.dumps(error_report, indent=2, ensure_ascii=False)
    print(output_json)