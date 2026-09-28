import json
import struct
import traceback
import re
 
input_json  = r'''[
    [
        {
            "NAME": "Forno 1",
            "DRIVERNAME": "modbusplc",
            "DRIVERCONFIG": "<p0 class="Protocollo MODBUS (master) via TCP/IP" name="Protocollo MODBUS (master) via TCP/IP" ipaddress="192.168.6.20" tcpport="502" timeout="5000" retries="3" write4XXXX="6"/>",
            "ID": 1,
            "measures": [
                {
                    "STATIONID": 1,
                    "NAME": "CO",
                    "UNITS": "mg/Nm3",
                    "DRIVERDATA": 0,
                    "TYPE": 0,
                    "ID": 1,
                    "MODBUSREGISTRO": 40001
                },
                {
                    "STATIONID": 1,
                    "NAME": "NO",
                    "UNITS": "mg/Nm3",
                    "DRIVERDATA": 0,
                    "TYPE": 0,
                    "ID": 2,
                    "MODBUSREGISTRO": 40002
                },
                {
                    "STATIONID": 1,
                    "NAME": "NOX",
                    "UNITS": "mg/Nm3",
                    "DRIVERDATA": 0,
                    "TYPE": 0,
                    "ID": 3,
                    "MODBUSREGISTRO": 40003
                },
                {
                    "STATIONID": 1,
                    "NAME": "O2 secco",
                    "UNITS": "%",
                    "DRIVERDATA": 0,
                    "TYPE": 0,
                    "ID": 4,
                    "MODBUSREGISTRO": 40004
                },
                {
                    "STATIONID": 1,
                    "NAME": "O2 umido",
                    "UNITS": "%",
                    "DRIVERDATA": 0,
                    "TYPE": 0,
                    "ID": 5,
                    "MODBUSREGISTRO": 40005
                },
                {
                    "STATIONID": 1,
                    "NAME": "H2O",
                    "UNITS": "%",
                    "DRIVERDATA": 0,
                    "TYPE": 0,
                    "ID": 6,
                    "MODBUSREGISTRO": 40006
                },
                {
                    "STATIONID": 1,
                    "NAME": "Pressione",
                    "UNITS": "mBar",
                    "DRIVERDATA": 0,
                    "TYPE": 0,
                    "ID": 7,
                    "MODBUSREGISTRO": 40007
                },
                {
                    "STATIONID": 1,
                    "NAME": "TEMPERATURA FUMI",
                    "UNITS": "°C",
                    "DRIVERDATA": 0,
                    "TYPE": 0,
                    "ID": 8,
                    "MODBUSREGISTRO": 40008
                },
                {
                    "STATIONID": 1,
                    "NAME": "Pressione Diff.",
                    "UNITS": "mBar",
                    "DRIVERDATA": 0,
                    "TYPE": 0,
                    "ID": 9,
                    "MODBUSREGISTRO": 40009
                },
                {
                    "STATIONID": 1,
                    "NAME": "PORTATA FUMI umida",
                    "UNITS": "Nm3/h",
                    "DRIVERDATA": 0,
                    "TYPE": 0,
                    "ID": 10,
                    "MODBUSREGISTRO": 40010
                },
                {
                    "STATIONID": 1,
                    "NAME": "Polveri (GR)",
                    "UNITS": "Unità",
                    "DRIVERDATA": 0,
                    "TYPE": 0,
                    "ID": 11,
                    "MODBUSREGISTRO": 40011
                },
                {
                    "STATIONID": 1,
                    "NAME": "Polveri ()",
                    "UNITS": "mg/Nm3",
                    "DRIVERDATA": 0,
                    "TYPE": 0,
                    "ID": 12,
                    "MODBUSREGISTRO": 40012
                },
                {
                    "STATIONID": 1,
                    "NAME": "Polveri TQ",
                    "UNITS": "mg/m3",
                    "DRIVERDATA": 0,
                    "TYPE": 0,
                    "ID": 13,
                    "MODBUSREGISTRO": 40013
                },
                {
                    "STATIONID": 1,
                    "NAME": "Anomalia Collegamento ADAM",
                    "UNITS": null,
                    "DRIVERDATA": 2,
                    "TYPE": 1,
                    "ID": 14,
                    "MODBUSREGISTRO": 40001
                },
                {
                    "STATIONID": 1,
                    "NAME": "Temperatura Fumi",
                    "UNITS": null,
                    "DRIVERDATA": 0,
                    "TYPE": 0,
                    "ID": 15,
                    "MODBUSREGISTRO": 40001
                },
                {
                    "STATIONID": 1,
                    "NAME": "CO",
                    "UNITS": null,
                    "DRIVERDATA": 0,
                    "TYPE": 0,
                    "ID": 16,
                    "MODBUSREGISTRO": 40005
                },
                {
                    "STATIONID": 1,
                    "NAME": "NOX",
                    "UNITS": null,
                    "DRIVERDATA": 0,
                    "TYPE": 0,
                    "ID": 17,
                    "MODBUSREGISTRO": 40009
                },
                {
                    "STATIONID": 1,
                    "NAME": "Polveri",
                    "UNITS": null,
                    "DRIVERDATA": 0,
                    "TYPE": 0,
                    "ID": 18,
                    "MODBUSREGISTRO": 40013
                },
                {
                    "STATIONID": 1,
                    "NAME": "O2",
                    "UNITS": null,
                    "DRIVERDATA": 0,
                    "TYPE": 0,
                    "ID": 19,
                    "MODBUSREGISTRO": 40017
                },
                {
                    "STATIONID": 1,
                    "NAME": "PORTATA FUMI umida",
                    "UNITS": null,
                    "DRIVERDATA": 0,
                    "TYPE": 0,
                    "ID": 20,
                    "MODBUSREGISTRO": 40021
                },
                {
                    "STATIONID": 1,
                    "NAME": "Stato impianto",
                    "UNITS": null,
                    "DRIVERDATA": 2,
                    "TYPE": 1,
                    "ID": 21,
                    "MODBUSREGISTRO": 40242
                },
                {
                    "STATIONID": 1,
                    "NAME": "Allarme Sonda riscaldata",
                    "UNITS": null,
                    "DRIVERDATA": 1,
                    "TYPE": 6,
                    "ID": 22,
                    "MODBUSREGISTRO": 40033
                },
                {
                    "STATIONID": 1,
                    "NAME": "Allarme Linea riscaldata",
                    "UNITS": null,
                    "DRIVERDATA": 1,
                    "TYPE": 6,
                    "ID": 23,
                    "MODBUSREGISTRO": 40034
                },
                {
                    "STATIONID": 1,
                    "NAME": "Allarme gruppo frigo",
                    "UNITS": null,
                    "DRIVERDATA": 1,
                    "TYPE": 6,
                    "ID": 24,
                    "MODBUSREGISTRO": 40035
                },
                {
                    "STATIONID": 1,
                    "NAME": "Allarme presenza condensa",
                    "UNITS": null,
                    "DRIVERDATA": 1,
                    "TYPE": 6,
                    "ID": 25,
                    "MODBUSREGISTRO": 40036
                },
                {
                    "STATIONID": 1,
                    "NAME": "Anomalia flusso/pressione",
                    "UNITS": null,
                    "DRIVERDATA": 1,
                    "TYPE": 6,
                    "ID": 26,
                    "MODBUSREGISTRO": 40037
                },
                {
                    "STATIONID": 1,
                    "NAME": "Allarme temp. convertitore NO2-NO",
                    "UNITS": null,
                    "DRIVERDATA": 1,
                    "TYPE": 6,
                    "ID": 27,
                    "MODBUSREGISTRO": 40038
                },
                {
                    "STATIONID": 1,
                    "NAME": "Fault/Anomalia Analizzatore CO/NO/O2",
                    "UNITS": null,
                    "DRIVERDATA": 1,
                    "TYPE": 6,
                    "ID": 28,
                    "MODBUSREGISTRO": 40039
                },
                {
                    "STATIONID": 1,
                    "NAME": "Manutenzione richiesta Analizzatore CO/NO/O2",
                    "UNITS": null,
                    "DRIVERDATA": 1,
                    "TYPE": 6,
                    "ID": 29,
                    "MODBUSREGISTRO": 40040
                },
                {
                    "STATIONID": 1,
                    "NAME": "Manutenzione/Cal. Analizzatore CO/NO/O2",
                    "UNITS": null,
                    "DRIVERDATA": 1,
                    "TYPE": 6,
                    "ID": 30,
                    "MODBUSREGISTRO": 40041
                },
                {
                    "STATIONID": 1,
                    "NAME": "Fault Sonda Polveri",
                    "UNITS": null,
                    "DRIVERDATA": 1,
                    "TYPE": 6,
                    "ID": 31,
                    "MODBUSREGISTRO": 40042
                },
                {
                    "STATIONID": 1,
                    "NAME": "Manutenzione Sonda Polveri",
                    "UNITS": null,
                    "DRIVERDATA": 1,
                    "TYPE": 6,
                    "ID": 32,
                    "MODBUSREGISTRO": 40043
                },
                {
                    "STATIONID": 1,
                    "NAME": "Fault Ossigeno umido",
                    "UNITS": null,
                    "DRIVERDATA": 1,
                    "TYPE": 6,
                    "ID": 33,
                    "MODBUSREGISTRO": 40044
                },
                {
                    "STATIONID": 1,
                    "NAME": "Allarme 1 Ossigeno umido",
                    "UNITS": null,
                    "DRIVERDATA": 1,
                    "TYPE": 6,
                    "ID": 34,
                    "MODBUSREGISTRO": 40045
                },
                {
                    "STATIONID": 1,
                    "NAME": "Allarme 2 Ossigeno umido",
                    "UNITS": null,
                    "DRIVERDATA": 1,
                    "TYPE": 6,
                    "ID": 35,
                    "MODBUSREGISTRO": 40046
                },
                {
                    "STATIONID": 1,
                    "NAME": "Portata",
                    "UNITS": null,
                    "DRIVERDATA": 1,
                    "TYPE": 6,
                    "ID": 36,
                    "MODBUSREGISTRO": 40047
                },
                {
                    "STATIONID": 1,
                    "NAME": "Allarme temp. armadio",
                    "UNITS": null,
                    "DRIVERDATA": 1,
                    "TYPE": 6,
                    "ID": 37,
                    "MODBUSREGISTRO": 40048
                },
                {
                    "STATIONID": 1,
                    "NAME": "Manutenzione in corso",
                    "UNITS": null,
                    "DRIVERDATA": 1,
                    "TYPE": 6,
                    "ID": 38,
                    "MODBUSREGISTRO": 40049
                },
                {
                    "STATIONID": 1,
                    "NAME": "Allarme PSU",
                    "UNITS": null,
                    "DRIVERDATA": 1,
                    "TYPE": 6,
                    "ID": 39,
                    "MODBUSREGISTRO": 40050
                },
                {
                    "STATIONID": 1,
                    "NAME": "Allarme apertura quadro",
                    "UNITS": null,
                    "DRIVERDATA": 1,
                    "TYPE": 6,
                    "ID": 40,
                    "MODBUSREGISTRO": 40051
                },
                {
                    "STATIONID": 1,
                    "NAME": "Calibrazione di zero Manuale da selettore",
                    "UNITS": null,
                    "DRIVERDATA": 1,
                    "TYPE": 6,
                    "ID": 41,
                    "MODBUSREGISTRO": 40052
                },
                {
                    "STATIONID": 1,
                    "NAME": "Calibrazione di span Manuale da selettore",
                    "UNITS": null,
                    "DRIVERDATA": 1,
                    "TYPE": 6,
                    "ID": 42,
                    "MODBUSREGISTRO": 40053
                },
                {
                    "STATIONID": 1,
                    "NAME": "Stato di zero Analizzatore CO/NO/O2",
                    "UNITS": null,
                    "DRIVERDATA": 1,
                    "TYPE": 6,
                    "ID": 43,
                    "MODBUSREGISTRO": 40054
                },
                {
                    "STATIONID": 1,
                    "NAME": "Stato di span Analizzatore CO/NO/O2",
                    "UNITS": null,
                    "DRIVERDATA": 1,
                    "TYPE": 6,
                    "ID": 44,
                    "MODBUSREGISTRO": 40055
                },
                {
                    "STATIONID": 1,
                    "NAME": "By-pass convertitore NO2-NO",
                    "UNITS": null,
                    "DRIVERDATA": 1,
                    "TYPE": 6,
                    "ID": 45,
                    "MODBUSREGISTRO": 40056
                },
                {
                    "STATIONID": 1,
                    "NAME": "Fault switch",
                    "UNITS": null,
                    "DRIVERDATA": 1,
                    "TYPE": 6,
                    "ID": 46,
                    "MODBUSREGISTRO": 40057
                },
                {
                    "STATIONID": 1,
                    "NAME": "Valvola EVC",
                    "UNITS": null,
                    "DRIVERDATA": 1,
                    "TYPE": 6,
                    "ID": 47,
                    "MODBUSREGISTRO": 40065
                },
                {
                    "STATIONID": 1,
                    "NAME": "Valvola EVZ",
                    "UNITS": null,
                    "DRIVERDATA": 1,
                    "TYPE": 6,
                    "ID": 48,
                    "MODBUSREGISTRO": 40066
                },
                {
                    "STATIONID": 1,
                    "NAME": "Valvola EVS",
                    "UNITS": null,
                    "DRIVERDATA": 1,
                    "TYPE": 6,
                    "ID": 49,
                    "MODBUSREGISTRO": 40067
                },
                {
                    "STATIONID": 1,
                    "NAME": "By-pass convertitore NO2-NO remoto",
                    "UNITS": null,
                    "DRIVERDATA": 1,
                    "TYPE": 6,
                    "ID": 50,
                    "MODBUSREGISTRO": 40068
                },
                {
                    "STATIONID": 1,
                    "NAME": "Manutenzione Sistema",
                    "UNITS": null,
                    "DRIVERDATA": 1,
                    "TYPE": 6,
                    "ID": 51,
                    "MODBUSREGISTRO": 40069
                }
            ],
            "bitinfo": [
                {
                    "MEASUREID": 14,
                    "BITNO": 0,
                    "BITNAME": "Anomalia Collegamento ADAM",
                    "TEXTON": "ANOMALIA",
                    "TEXTOFF": "OK"
                },
                {
                    "MEASUREID": 21,
                    "BITNO": 0,
                    "BITNAME": "Stato impianto",
                    "TEXTON": "OK",
                    "TEXTOFF": "OK"
                },
                {
                    "MEASUREID": 22,
                    "BITNO": 0,
                    "BITNAME": "Allarme Sonda riscaldata",
                    "TEXTON": "ALLARME",
                    "TEXTOFF": "OK"
                },
                {
                    "MEASUREID": 23,
                    "BITNO": 0,
                    "BITNAME": "Allarme Linea riscaldata",
                    "TEXTON": "ALLARME",
                    "TEXTOFF": "OK"
                },
                {
                    "MEASUREID": 24,
                    "BITNO": 0,
                    "BITNAME": "Allarme gruppo frigo",
                    "TEXTON": "ALLARME",
                    "TEXTOFF": "OK"
                },
                {
                    "MEASUREID": 25,
                    "BITNO": 0,
                    "BITNAME": "Allarme presenza condensa",
                    "TEXTON": "ALLARME",
                    "TEXTOFF": "OK"
                },
                {
                    "MEASUREID": 26,
                    "BITNO": 0,
                    "BITNAME": "Anomalia flusso/pressione",
                    "TEXTON": "ANOMALIA",
                    "TEXTOFF": "OK"
                },
                {
                    "MEASUREID": 27,
                    "BITNO": 0,
                    "BITNAME": "Allarme temp. convertitore NO2-NO",
                    "TEXTON": "ALLARME",
                    "TEXTOFF": "OK"
                },
                {
                    "MEASUREID": 28,
                    "BITNO": 0,
                    "BITNAME": "Fault/Anomalia Analizzatore CO/NO/O2",
                    "TEXTON": "FAULT",
                    "TEXTOFF": "OK"
                },
                {
                    "MEASUREID": 29,
                    "BITNO": 0,
                    "BITNAME": "Manutenzione richiesta Analizzatore CO/NO/O2",
                    "TEXTON": "MANUTENZIONE",
                    "TEXTOFF": "OK"
                },
                {
                    "MEASUREID": 30,
                    "BITNO": 0,
                    "BITNAME": "Manutenzione/Cal. Analizzatore CO/NO/O2",
                    "TEXTON": "MANUTENZIONE",
                    "TEXTOFF": "OK"
                },
                {
                    "MEASUREID": 31,
                    "BITNO": 0,
                    "BITNAME": "Fault Sonda Polveri",
                    "TEXTON": "FAULT",
                    "TEXTOFF": "OK"
                },
                {
                    "MEASUREID": 32,
                    "BITNO": 0,
                    "BITNAME": "Manutenzione Sonda Polveri",
                    "TEXTON": "MANUTENZIONE",
                    "TEXTOFF": "OK"
                },
                {
                    "MEASUREID": 33,
                    "BITNO": 0,
                    "BITNAME": "Fault Ossigeno umido",
                    "TEXTON": "FAULT",
                    "TEXTOFF": "OK"
                },
                {
                    "MEASUREID": 34,
                    "BITNO": 0,
                    "BITNAME": "Allarme 1 Ossigeno umido",
                    "TEXTON": "ALLARME",
                    "TEXTOFF": "OK"
                },
                {
                    "MEASUREID": 35,
                    "BITNO": 0,
                    "BITNAME": "Allarme 2 Ossigeno umido",
                    "TEXTON": "ALLARME",
                    "TEXTOFF": "OK"
                },
                {
                    "MEASUREID": 36,
                    "BITNO": 0,
                    "BITNAME": "Portata",
                    "TEXTON": "OK",
                    "TEXTOFF": "OK"
                },
                {
                    "MEASUREID": 37,
                    "BITNO": 0,
                    "BITNAME": "Allarme temp. armadio",
                    "TEXTON": "ALLARME",
                    "TEXTOFF": "OK"
                },
                {
                    "MEASUREID": 38,
                    "BITNO": 0,
                    "BITNAME": "Manutenzione in corso",
                    "TEXTON": "MANUTENZIONE",
                    "TEXTOFF": "OK"
                },
                {
                    "MEASUREID": 39,
                    "BITNO": 0,
                    "BITNAME": "Allarme PSU",
                    "TEXTON": "ALLARME",
                    "TEXTOFF": "OK"
                },
                {
                    "MEASUREID": 40,
                    "BITNO": 0,
                    "BITNAME": "Allarme apertura quadro",
                    "TEXTON": "ALLARME",
                    "TEXTOFF": "OK"
                },
                {
                    "MEASUREID": 41,
                    "BITNO": 0,
                    "BITNAME": "Calibrazione di zero Manuale da selettore",
                    "TEXTON": "CALIBRAZIONE",
                    "TEXTOFF": "OK"
                },
                {
                    "MEASUREID": 42,
                    "BITNO": 0,
                    "BITNAME": "Calibrazione di span Manuale da selettore",
                    "TEXTON": "CALIBRAZIONE",
                    "TEXTOFF": "OK"
                },
                {
                    "MEASUREID": 43,
                    "BITNO": 0,
                    "BITNAME": "Stato di zero Analizzatore CO/NO/O2",
                    "TEXTON": "ZERO",
                    "TEXTOFF": "OK"
                },
                {
                    "MEASUREID": 44,
                    "BITNO": 0,
                    "BITNAME": "Stato di span Analizzatore CO/NO/O2",
                    "TEXTON": "SPAN",
                    "TEXTOFF": "OK"
                },
                {
                    "MEASUREID": 45,
                    "BITNO": 0,
                    "BITNAME": "By-pass convertitore NO2-NO",
                    "TEXTON": "OK",
                    "TEXTOFF": "OK"
                },
                {
                    "MEASUREID": 46,
                    "BITNO": 0,
                    "BITNAME": "Fault switch",
                    "TEXTON": "FAULT",
                    "TEXTOFF": "OK"
                },
                {
                    "MEASUREID": 47,
                    "BITNO": 0,
                    "BITNAME": "Valvola EVC",
                    "TEXTON": "OK",
                    "TEXTOFF": "OK"
                },
                {
                    "MEASUREID": 48,
                    "BITNO": 0,
                    "BITNAME": "Valvola EVZ",
                    "TEXTON": "OK",
                    "TEXTOFF": "OK"
                },
                {
                    "MEASUREID": 49,
                    "BITNO": 0,
                    "BITNAME": "Valvola EVS",
                    "TEXTON": "OK",
                    "TEXTOFF": "OK"
                },
                {
                    "MEASUREID": 50,
                    "BITNO": 0,
                    "BITNAME": "By-pass convertitore NO2-NO remoto",
                    "TEXTON": "OK",
                    "TEXTOFF": "OK"
                },
                {
                    "MEASUREID": 51,
                    "BITNO": 0,
                    "BITNAME": "Manutenzione Sistema",
                    "TEXTON": "MANUTENZIONE",
                    "TEXTOFF": "OK"
                }
            ]
        }
    ]
]'''

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