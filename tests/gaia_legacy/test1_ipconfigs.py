import json

input_json = r'''[
  [
    {
      "NAME": "Sistema Analisi Emissioni",
      "DRIVERNAME": "modbusplc",
      "DRIVERCONFIG": ":",
      "ID": 1,
      "measures": [
        {
          "STATIONID": 1,
          "NAME": "Allarme sonda riscaldata",
          "UNITS": null,
          "DRIVERDATA": 1,
          "TYPE": 6,
          "ID": 1,
          "MODBUSREGISTRO": 1,
          "BIT": 8,
          "GROUP": "Ingresso_digitale"
        },
        {
          "STATIONID": 1,
          "NAME": "Allarme linea riscaldata",
          "UNITS": null,
          "DRIVERDATA": 1,
          "TYPE": 6,
          "ID": 2,
          "MODBUSREGISTRO": 1,
          "BIT": 9,
          "GROUP": "Ingresso_digitale"
        },
        {
          "STATIONID": 1,
          "NAME": "Allarme frigorifero",
          "UNITS": null,
          "DRIVERDATA": 1,
          "TYPE": 6,
          "ID": 3,
          "MODBUSREGISTRO": 1,
          "BIT": 10,
          "GROUP": "Ingresso_digitale"
        },
        {
          "STATIONID": 1,
          "NAME": "Allarme presenza condensa",
          "UNITS": null,
          "DRIVERDATA": 1,
          "TYPE": 6,
          "ID": 4,
          "MODBUSREGISTRO": 1,
          "BIT": 11,
          "GROUP": "Ingresso_digitale"
        },
        {
          "STATIONID": 1,
          "NAME": "Allarme mancanza flusso",
          "UNITS": null,
          "DRIVERDATA": 1,
          "TYPE": 6,
          "ID": 5,
          "MODBUSREGISTRO": 1,
          "BIT": 12,
          "GROUP": "Ingresso_digitale"
        },
        {
          "STATIONID": 1,
          "NAME": "Allarme SO2",
          "UNITS": null,
          "DRIVERDATA": 1,
          "TYPE": 6,
          "ID": 6,
          "MODBUSREGISTRO": 1,
          "BIT": 13,
          "GROUP": "Ingresso_digitale"
        },
        {
          "STATIONID": 1,
          "NAME": "Sistema in",
          "UNITS": null,
          "DRIVERDATA": 1,
          "TYPE": 6,
          "ID": 7,
          "MODBUSREGISTRO": 3,
          "BIT": 8,
          "GROUP": "Ingresso_digitale"
        },
        {
          "STATIONID": 1,
          "NAME": "Calibrazione automatica in corso",
          "UNITS": null,
          "DRIVERDATA": 1,
          "TYPE": 6,
          "ID": 8,
          "MODBUSREGISTRO": 3,
          "BIT": 9,
          "GROUP": "Ingresso_digitale"
        },
        {
          "STATIONID": 1,
          "NAME": "SO2 in calibrazione di zero",
          "UNITS": null,
          "DRIVERDATA": 1,
          "TYPE": 6,
          "ID": 9,
          "MODBUSREGISTRO": 3,
          "BIT": 10,
          "GROUP": "Ingresso_digitale"
        },
        {
          "STATIONID": 1,
          "NAME": "SO2 in calibrazione di span",
          "UNITS": null,
          "DRIVERDATA": 1,
          "TYPE": 6,
          "ID": 10,
          "MODBUSREGISTRO": 3,
          "BIT": 11,
          "GROUP": "Ingresso_digitale"
        },
        {
          "STATIONID": 1,
          "NAME": "Secondo campo SO2",
          "UNITS": null,
          "DRIVERDATA": 1,
          "TYPE": 6,
          "ID": 11,
          "MODBUSREGISTRO": 3,
          "BIT": 15,
          "GROUP": "Ingresso_digitale"
        },
        {
          "STATIONID": 1,
          "NAME": "QAL3 in corso",
          "UNITS": null,
          "DRIVERDATA": 1,
          "TYPE": 6,
          "ID": 12,
          "MODBUSREGISTRO": 3,
          "BIT": 0,
          "GROUP": "Ingresso_digitale"
        },
        {
          "STATIONID": 1,
          "NAME": "QAL3: elettrovalvola ARIA",
          "UNITS": null,
          "DRIVERDATA": 1,
          "TYPE": 6,
          "ID": 13,
          "MODBUSREGISTRO": 3,
          "BIT": 1,
          "GROUP": "Ingresso_digitale"
        },
        {
          "STATIONID": 1,
          "NAME": "QAL3: elettrovalvola span SO2",
          "UNITS": null,
          "DRIVERDATA": 1,
          "TYPE": 6,
          "ID": 14,
          "MODBUSREGISTRO": 3,
          "BIT": 2,
          "GROUP": "Ingresso_digitale"
        },
        {
          "STATIONID": 1,
          "NAME": "QAL3: lavaggio con N2",
          "UNITS": null,
          "DRIVERDATA": 1,
          "TYPE": 6,
          "ID": 15,
          "MODBUSREGISTRO": 3,
          "BIT": 3,
          "GROUP": "Ingresso_digitale"
        },
        {
          "STATIONID": 1,
          "NAME": "QAL3: ciclo concluso senza errori",
          "UNITS": null,
          "DRIVERDATA": 1,
          "TYPE": 6,
          "ID": 16,
          "MODBUSREGISTRO": 3,
          "BIT": 5,
          "GROUP": "Ingresso_digitale"
        },
        {
          "STATIONID": 1,
          "NAME": "QAL3: ciclo concluso con errori",
          "UNITS": null,
          "DRIVERDATA": 1,
          "TYPE": 6,
          "ID": 17,
          "MODBUSREGISTRO": 3,
          "BIT": 6,
          "GROUP": "Ingresso_digitale"
        },
        {
          "STATIONID": 1,
          "NAME": "Pompa analisi",
          "UNITS": null,
          "DRIVERDATA": 1,
          "TYPE": 6,
          "ID": 18,
          "MODBUSREGISTRO": 3,
          "BIT": 7,
          "GROUP": "Ingresso_digitale"
        },
        {
          "STATIONID": 1,
          "NAME": "Stato elettrovalvola cal zero",
          "UNITS": null,
          "DRIVERDATA": 1,
          "TYPE": 6,
          "ID": 19,
          "MODBUSREGISTRO": 4,
          "BIT": 8,
          "GROUP": "Ingresso_digitale"
        },
        {
          "STATIONID": 1,
          "NAME": "Stato elettrovalvola N2",
          "UNITS": null,
          "DRIVERDATA": 1,
          "TYPE": 6,
          "ID": 20,
          "MODBUSREGISTRO": 4,
          "BIT": 9,
          "GROUP": "Ingresso_digitale"
        },
        {
          "STATIONID": 1,
          "NAME": "Stato elettrovalvola cal span",
          "UNITS": null,
          "DRIVERDATA": 1,
          "TYPE": 6,
          "ID": 21,
          "MODBUSREGISTRO": 4,
          "BIT": 10,
          "GROUP": "Ingresso_digitale"
        },
        {
          "STATIONID": 1,
          "NAME": "Elettrovalvola cal da sonda",
          "UNITS": null,
          "DRIVERDATA": 1,
          "TYPE": 6,
          "ID": 22,
          "MODBUSREGISTRO": 4,
          "BIT": 11,
          "GROUP": "Ingresso_digitale"
        },
        {
          "STATIONID": 1,
          "NAME": "PLC life signal",
          "UNITS": null,
          "DRIVERDATA": 1,
          "TYPE": 6,
          "ID": 23,
          "MODBUSREGISTRO": 4,
          "BIT": 13,
          "GROUP": "Ingresso_digitale"
        },
        {
          "STATIONID": 1,
          "NAME": "Impianto in marcia",
          "UNITS": null,
          "DRIVERDATA": 1,
          "TYPE": 6,
          "ID": 24,
          "MODBUSREGISTRO": 4,
          "BIT": 0,
          "GROUP": "Ingresso_digitale"
        },
        {
          "STATIONID": 1,
          "NAME": "Impianto in minimo tecnico/funzionamento anomalo",
          "UNITS": null,
          "DRIVERDATA": 1,
          "TYPE": 6,
          "ID": 25,
          "MODBUSREGISTRO": 4,
          "BIT": 1,
          "GROUP": "Ingresso_digitale"
        },
        {
          "STATIONID": 1,
          "NAME": "Impianto in avviamento",
          "UNITS": null,
          "DRIVERDATA": 1,
          "TYPE": 6,
          "ID": 26,
          "MODBUSREGISTRO": 4,
          "BIT": 2,
          "GROUP": "Ingresso_digitale"
        },
        {
          "STATIONID": 1,
          "NAME": "Impianto in spegnimento",
          "UNITS": null,
          "DRIVERDATA": 1,
          "TYPE": 6,
          "ID": 27,
          "MODBUSREGISTRO": 4,
          "BIT": 3,
          "GROUP": "Ingresso_digitale"
        },
        {
          "STATIONID": 1,
          "NAME": "SME in manutenzione",
          "UNITS": null,
          "DRIVERDATA": 1,
          "TYPE": 6,
          "ID": 28,
          "MODBUSREGISTRO": 4,
          "BIT": 5,
          "GROUP": "Ingresso_digitale"
        },
        {
          "STATIONID": 1,
          "NAME": "Impianto in manutenzione",
          "UNITS": null,
          "DRIVERDATA": 1,
          "TYPE": 6,
          "ID": 29,
          "MODBUSREGISTRO": 4,
          "BIT": 6,
          "GROUP": "Ingresso_digitale"
        },
        {
          "STATIONID": 1,
          "NAME": "Impianto fuori servizio per guasto",
          "UNITS": null,
          "DRIVERDATA": 1,
          "TYPE": 6,
          "ID": 30,
          "MODBUSREGISTRO": 4,
          "BIT": 7,
          "GROUP": "Ingresso_digitale"
        }
      ],
      "bitinfo": [
        {
          "MEASUREID": 1,
          "BITNO": 8,
          "BITNAME": "Allarme sonda riscaldata",
          "TEXTON": "Allarme",
          "TEXTOFF": "OFF"
        },
        {
          "MEASUREID": 1,
          "BITNO": 9,
          "BITNAME": "Allarme linea riscaldata",
          "TEXTON": "Allarme",
          "TEXTOFF": "OFF"
        },
        {
          "MEASUREID": 1,
          "BITNO": 10,
          "BITNAME": "Allarme frigorifero",
          "TEXTON": "Allarme",
          "TEXTOFF": "OFF"
        },
        {
          "MEASUREID": 1,
          "BITNO": 11,
          "BITNAME": "Allarme presenza condensa",
          "TEXTON": "Allarme",
          "TEXTOFF": "OFF"
        },
        {
          "MEASUREID": 1,
          "BITNO": 12,
          "BITNAME": "Allarme mancanza flusso",
          "TEXTON": "Allarme",
          "TEXTOFF": "OFF"
        },
        {
          "MEASUREID": 1,
          "BITNO": 13,
          "BITNAME": "Allarme analizzatore SO2",
          "TEXTON": "Allarme",
          "TEXTOFF": "OFF"
        },
        {
          "MEASUREID": 3,
          "BITNO": 8,
          "BITNAME": "Sistema in misura",
          "TEXTON": "Attivo",
          "TEXTOFF": "OFF"
        },
        {
          "MEASUREID": 3,
          "BITNO": 9,
          "BITNAME": "Calibrazione automatica in corso",
          "TEXTON": "Calibrazione",
          "TEXTOFF": "OFF"
        },
        {
          "MEASUREID": 3,
          "BITNO": 10,
          "BITNAME": "Analizzatore SO2 in calibrazione di zero",
          "TEXTON": "Calibrazione",
          "TEXTOFF": "OFF"
        },
        {
          "MEASUREID": 3,
          "BITNO": 11,
          "BITNAME": "Analizzatore SO2 in calibrazione di span",
          "TEXTON": "Calibrazione",
          "TEXTOFF": "OFF"
        },
        {
          "MEASUREID": 3,
          "BITNO": 15,
          "BITNAME": "Secondo campo SO2",
          "TEXTON": "Attivo",
          "TEXTOFF": "OFF"
        },
        {
          "MEASUREID": 3,
          "BITNO": 0,
          "BITNAME": "QAL3 in corso",
          "TEXTON": "Attivo",
          "TEXTOFF": "OFF"
        },
        {
          "MEASUREID": 3,
          "BITNO": 1,
          "BITNAME": "QAL3: elettrovalvola ARIA",
          "TEXTON": "Attivo",
          "TEXTOFF": "OFF"
        },
        {
          "MEASUREID": 3,
          "BITNO": 2,
          "BITNAME": "QAL3: elettrovalvola span SO2",
          "TEXTON": "Attivo",
          "TEXTOFF": "OFF"
        },
        {
          "MEASUREID": 3,
          "BITNO": 3,
          "BITNAME": "QAL3: lavaggio con N2",
          "TEXTON": "Attivo",
          "TEXTOFF": "OFF"
        },
        {
          "MEASUREID": 3,
          "BITNO": 5,
          "BITNAME": "QAL3: ciclo concluso senza errori",
          "TEXTON": "Attivo",
          "TEXTOFF": "OFF"
        },
        {
          "MEASUREID": 3,
          "BITNO": 6,
          "BITNAME": "QAL3: ciclo concluso con errori",
          "TEXTON": "Attivo",
          "TEXTOFF": "OFF"
        },
        {
          "MEASUREID": 3,
          "BITNO": 7,
          "BITNAME": "Pompa analisi",
          "TEXTON": "Attivo",
          "TEXTOFF": "OFF"
        },
        {
          "MEASUREID": 4,
          "BITNO": 8,
          "BITNAME": "Stato elettrovalvola cal zero",
          "TEXTON": "Attivo",
          "TEXTOFF": "OFF"
        },
        {
          "MEASUREID": 4,
          "BITNO": 9,
          "BITNAME": "Stato elettrovalvola N2",
          "TEXTON": "Attivo",
          "TEXTOFF": "OFF"
        },
        {
          "MEASUREID": 4,
          "BITNO": 10,
          "BITNAME": "Stato elettrovalvola cal span",
          "TEXTON": "Attivo",
          "TEXTOFF": "OFF"
        },
        {
          "MEASUREID": 4,
          "BITNO": 11,
          "BITNAME": "Elettrovalvola cal da sonda",
          "TEXTON": "Attivo",
          "TEXTOFF": "OFF"
        },
        {
          "MEASUREID": 4,
          "BITNO": 13,
          "BITNAME": "PLC life signal",
          "TEXTON": "Attivo",
          "TEXTOFF": "OFF"
        },
        {
          "MEASUREID": 4,
          "BITNO": 0,
          "BITNAME": "Impianto in marcia",
          "TEXTON": "Attivo",
          "TEXTOFF": "OFF"
        },
        {
          "MEASUREID": 4,
          "BITNO": 1,
          "BITNAME": "Impianto in minimo tecnico/funzionamento anomalo",
          "TEXTON": "Attivo",
          "TEXTOFF": "OFF"
        },
        {
          "MEASUREID": 4,
          "BITNO": 2,
          "BITNAME": "Impianto in avviamento",
          "TEXTON": "Attivo",
          "TEXTOFF": "OFF"
        },
        {
          "MEASUREID": 4,
          "BITNO": 3,
          "BITNAME": "Impianto in spegnimento",
          "TEXTON": "Attivo",
          "TEXTOFF": "OFF"
        },
        {
          "MEASUREID": 4,
          "BITNO": 5,
          "BITNAME": "SME in manutenzione",
          "TEXTON": "Manutenzione",
          "TEXTOFF": "OFF"
        },
        {
          "MEASUREID": 4,
          "BITNO": 6,
          "BITNAME": "Impianto in manutenzione",
          "TEXTON": "Manutenzione",
          "TEXTOFF": "OFF"
        },
        {
          "MEASUREID": 4,
          "BITNO": 7,
          "BITNAME": "Impianto fuori servizio per guasto",
          "TEXTON": "Allarme",
          "TEXTOFF": "OFF"
        }
      ]
    }
  ],
  [
    {
      "nome_stazione": "SME",
      "stazione": "Esseco di Trecate (NO)",
      "protocollo": "ModBus TCP",
      "ip_plc": "10.100.50.95",
      "port": 511,
      "var": [],
      "STATION_INFORMATIONS": true
    }
  ]
]
'''

input_json = json.loads(input_json)

nome_stazione = ""
stazione = ""
ip_plc = ""
porta = None

# Scorri la lista esterna, poi quella interna
for group in input_json:
    for station in group:
        if station.get("STATION_INFORMATIONS"):
            nome_stazione = station.get("nome_stazione", "")
            stazione      = station.get("stazione", "")
            ip_plc        = station.get("ip_plc", "")
            porta         = station.get("port")        # int o None

# Secondo passaggio: aggiorna le stazioni senza STATION_INFORMATIONS
for group in input_json:
    for station in group:
        if not station.get("STATION_INFORMATIONS"):
            station["NAME"]         = nome_stazione
            station["DRIVERCONFIG"] = f"{ip_plc}:{porta if porta is not None else ''}"

output = json.dumps(input_json, indent=4, ensure_ascii=False)
print(output)