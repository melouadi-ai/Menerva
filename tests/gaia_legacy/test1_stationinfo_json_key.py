import json

input_json = r'''[[
    {
        "nome_stazione": "SME",
        "stazione": "SME",
        "protocollo": "ModBus TCP",
        "ip_plc": "10.100.50.95",
        "port": 511,
        "var": [],
        "STATION_INFORMATIONS": true
    }
],
[
    {
        "nome_stazione": "SME",
        "stazione": "Sistema Analisi SO2",
        "protocollo": "ModBus TCP",
        "ip_plc": null,
        "port": null,
        "var": [
            {
                "tag": "SO2",
                "unità_misura": "mg/Nm3",
                "inizio_scala_elettrico": null,
                "fine_scala_elettrico": null,
                "inizio_scala_ingegneristico": 0,
                "fine_scala_ingegneristico": 300,
                "limite_orario": 60,
                "limite_giornaliero": 60
            },
            {
                "tag": "TF",
                "unità_misura": "°C",
                "inizio_scala_elettrico": null,
                "fine_scala_elettrico": null,
                "inizio_scala_ingegneristico": 0,
                "fine_scala_ingegneristico": 100,
                "limite_orario": null,
                "limite_giornaliero": null
            }
        ],
        "STATION_INFORMATIONS": true
    }
],
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
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 1,
        "MODBUSREGISTRO": 1
      },
      {
        "STATIONID": 1,
        "NAME": "Allarme linea riscaldata",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 1,
        "MODBUSREGISTRO": 1
      },
      {
        "STATIONID": 1,
        "NAME": "Allarme frigorifero",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 1,
        "MODBUSREGISTRO": 1
      },
      {
        "STATIONID": 1,
        "NAME": "Allarme presenza condensa",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 1,
        "MODBUSREGISTRO": 1
      },
      {
        "STATIONID": 1,
        "NAME": "Allarme mancanza flusso",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 1,
        "MODBUSREGISTRO": 1
      },
      {
        "STATIONID": 1,
        "NAME": "Allarme SO2",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 1,
        "MODBUSREGISTRO": 1
      },
      {
        "STATIONID": 1,
        "NAME": "Sistema in",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 1,
        "MODBUSREGISTRO": 3
      },
      {
        "STATIONID": 1,
        "NAME": "Calibrazione automatica in corso",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 1,
        "MODBUSREGISTRO": 3
      },
      {
        "STATIONID": 1,
        "NAME": "SO2 in calibrazione di zero",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 1,
        "MODBUSREGISTRO": 3
      },
      {
        "STATIONID": 1,
        "NAME": "SO2 in calibrazione di span",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 1,
        "MODBUSREGISTRO": 3
      },
      {
        "STATIONID": 1,
        "NAME": "Secondo campo SO2",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 1,
        "MODBUSREGISTRO": 3
      },
      {
        "STATIONID": 1,
        "NAME": "QAL3 in corso",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 1,
        "MODBUSREGISTRO": 3
      },
      {
        "STATIONID": 1,
        "NAME": "QAL3: elettrovalvola ARIA",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 1,
        "MODBUSREGISTRO": 3
      },
      {
        "STATIONID": 1,
        "NAME": "QAL3: elettrovalvola span SO2",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 1,
        "MODBUSREGISTRO": 3
      },
      {
        "STATIONID": 1,
        "NAME": "QAL3: lavaggio con N2",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 1,
        "MODBUSREGISTRO": 3
      },
      {
        "STATIONID": 1,
        "NAME": "QAL3: ciclo concluso senza errori",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 1,
        "MODBUSREGISTRO": 3
      },
      {
        "STATIONID": 1,
        "NAME": "QAL3: ciclo concluso con errori",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 1,
        "MODBUSREGISTRO": 3
      },
      {
        "STATIONID": 1,
        "NAME": "Pompa analisi",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 1,
        "MODBUSREGISTRO": 3
      },
      {
        "STATIONID": 1,
        "NAME": "Stato elettrovalvola cal zero",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 1,
        "MODBUSREGISTRO": 4
      },
      {
        "STATIONID": 1,
        "NAME": "Stato elettrovalvola N2",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 1,
        "MODBUSREGISTRO": 4
      },
      {
        "STATIONID": 1,
        "NAME": "Stato elettrovalvola cal span",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 1,
        "MODBUSREGISTRO": 4
      },
      {
        "STATIONID": 1,
        "NAME": "Elettrovalvola cal da sonda",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 1,
        "MODBUSREGISTRO": 4
      },
      {
        "STATIONID": 1,
        "NAME": "PLC life signal",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 1,
        "MODBUSREGISTRO": 4
      },
      {
        "STATIONID": 1,
        "NAME": "Impianto in marcia",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 1,
        "MODBUSREGISTRO": 4
      },
      {
        "STATIONID": 1,
        "NAME": "Impianto in minimo tecnico/funzionamento anomalo",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 1,
        "MODBUSREGISTRO": 4
      },
      {
        "STATIONID": 1,
        "NAME": "Impianto in avviamento",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 1,
        "MODBUSREGISTRO": 4
      },
      {
        "STATIONID": 1,
        "NAME": "Impianto in spegnimento",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 1,
        "MODBUSREGISTRO": 4
      },
      {
        "STATIONID": 1,
        "NAME": "SME in manutenzione",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 1,
        "MODBUSREGISTRO": 4
      },
      {
        "STATIONID": 1,
        "NAME": "Impianto in manutenzione",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 1,
        "MODBUSREGISTRO": 4
      },
      {
        "STATIONID": 1,
        "NAME": "Impianto fuori servizio per guasto",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 1,
        "MODBUSREGISTRO": 4
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
        "TEXTON": "Guasto",
        "TEXTOFF": "OFF"
      }
    ]
  }
],
[
  {
    "NAME": "Sistema Analisi Emissioni",
    "DRIVERNAME": "modbusplc",
    "DRIVERCONFIG": ":",
    "ID": 1,
    "measures": [
      {
        "STATIONID": 1,
        "NAME": "Blocco da BSS2",
        "UNITS": null,
        "DRIVERDATA": 1,
        "TYPE": 6,
        "ID": 1,
        "MODBUSREGISTRO": 5,
        "MODBUSREGISTRONOME": "DBX 72.0",
        "GROUP": "Ingresso_digitale"
      },
      {
        "STATIONID": 1,
        "NAME": "Allarme bassa portata FT-2611",
        "UNITS": null,
        "DRIVERDATA": 1,
        "TYPE": 6,
        "ID": 2,
        "MODBUSREGISTRO": 5,
        "MODBUSREGISTRONOME": "DBX 72.1",
        "GROUP": "Ingresso_digitale"
      },
      {
        "STATIONID": 1,
        "NAME": "Allarme bassa portata FT-310",
        "UNITS": null,
        "DRIVERDATA": 1,
        "TYPE": 6,
        "ID": 3,
        "MODBUSREGISTRO": 5,
        "MODBUSREGISTRONOME": "DBX 72.2",
        "GROUP": "Ingresso_digitale"
      },
      {
        "STATIONID": 1,
        "NAME": "Allarme bassa portata FT-313",
        "UNITS": null,
        "DRIVERDATA": 1,
        "TYPE": 6,
        "ID": 4,
        "MODBUSREGISTRO": 5,
        "MODBUSREGISTRONOME": "DBX 72.3",
        "GROUP": "Ingresso_digitale"
      },
      {
        "STATIONID": 1,
        "NAME": "AI303A allarme basso pH",
        "UNITS": null,
        "DRIVERDATA": 1,
        "TYPE": 6,
        "ID": 5,
        "MODBUSREGISTRO": 5,
        "MODBUSREGISTRONOME": "DBX 72.4",
        "GROUP": "Ingresso_digitale"
      },
      {
        "STATIONID": 1,
        "NAME": "AI303B allarme basso pH",
        "UNITS": null,
        "DRIVERDATA": 1,
        "TYPE": 6,
        "ID": 6,
        "MODBUSREGISTRO": 5,
        "MODBUSREGISTRONOME": "DBX 72.5",
        "GROUP": "Ingresso_digitale"
      },
      {
        "STATIONID": 1,
        "NAME": "AI2602A allarme basso pH",
        "UNITS": null,
        "DRIVERDATA": 1,
        "TYPE": 6,
        "ID": 7,
        "MODBUSREGISTRO": 5,
        "MODBUSREGISTRONOME": "DBX 72.6",
        "GROUP": "Ingresso_digitale"
      },
      {
        "STATIONID": 1,
        "NAME": "AI2602B allarme basso pH",
        "UNITS": null,
        "DRIVERDATA": 1,
        "TYPE": 6,
        "ID": 8,
        "MODBUSREGISTRO": 5,
        "MODBUSREGISTRONOME": "DBX 72.7",
        "GROUP": "Ingresso_digitale"
      },
      {
        "STATIONID": 1,
        "NAME": "PM-302A in marcia",
        "UNITS": null,
        "DRIVERDATA": 1,
        "TYPE": 6,
        "ID": 9,
        "MODBUSREGISTRO": 6,
        "MODBUSREGISTRONOME": "DBX 73.1",
        "GROUP": "Ingresso_digitale"
      },
      {
        "STATIONID": 1,
        "NAME": "PM-302B in marcia",
        "UNITS": null,
        "DRIVERDATA": 1,
        "TYPE": 6,
        "ID": 10,
        "MODBUSREGISTRO": 6,
        "MODBUSREGISTRONOME": "DBX 73.2",
        "GROUP": "Ingresso_digitale"
      },
      {
        "STATIONID": 1,
        "NAME": "PM-310A in marcia",
        "UNITS": null,
        "DRIVERDATA": 1,
        "TYPE": 6,
        "ID": 11,
        "MODBUSREGISTRO": 6,
        "MODBUSREGISTRONOME": "DBX 73.4",
        "GROUP": "Ingresso_digitale"
      },
      {
        "STATIONID": 1,
        "NAME": "PM-310B in marcia",
        "UNITS": null,
        "DRIVERDATA": 1,
        "TYPE": 6,
        "ID": 12,
        "MODBUSREGISTRO": 6,
        "MODBUSREGISTRONOME": "DBX 73.5",
        "GROUP": "Ingresso_digitale"
      },
      {
        "STATIONID": 1,
        "NAME": "PM-2600A in marcia",
        "UNITS": null,
        "DRIVERDATA": 1,
        "TYPE": 6,
        "ID": 13,
        "MODBUSREGISTRO": 7,
        "MODBUSREGISTRONOME": "DBX 74.0",
        "GROUP": "Ingresso_digitale"
      },
      {
        "STATIONID": 1,
        "NAME": "PM-2600B in marcia",
        "UNITS": null,
        "DRIVERDATA": 1,
        "TYPE": 6,
        "ID": 14,
        "MODBUSREGISTRO": 7,
        "MODBUSREGISTRONOME": "DBX 74.1",
        "GROUP": "Ingresso_digitale"
      },
      {
        "STATIONID": 1,
        "NAME": "PM-2601A in marcia",
        "UNITS": null,
        "DRIVERDATA": 1,
        "TYPE": 6,
        "ID": 15,
        "MODBUSREGISTRO": 7,
        "MODBUSREGISTRONOME": "DBX 74.2",
        "GROUP": "Ingresso_digitale"
      },
      {
        "STATIONID": 1,
        "NAME": "PM-2601B in marcia",
        "UNITS": null,
        "DRIVERDATA": 1,
        "TYPE": 6,
        "ID": 16,
        "MODBUSREGISTRO": 7,
        "MODBUSREGISTRONOME": "DBX 74.3",
        "GROUP": "Ingresso_digitale"
      },
      {
        "STATIONID": 1,
        "NAME": "PM-2604A in marcia",
        "UNITS": null,
        "DRIVERDATA": 1,
        "TYPE": 6,
        "ID": 17,
        "MODBUSREGISTRO": 7,
        "MODBUSREGISTRONOME": "DBX 74.4",
        "GROUP": "Ingresso_digitale"
      },
      {
        "STATIONID": 1,
        "NAME": "PM-2604B in marcia",
        "UNITS": null,
        "DRIVERDATA": 1,
        "TYPE": 6,
        "ID": 18,
        "MODBUSREGISTRO": 7,
        "MODBUSREGISTRONOME": "DBX 74.5",
        "GROUP": "Ingresso_digitale"
      },
      {
        "STATIONID": 1,
        "NAME": "Ventilatore VN-400 in marcia",
        "UNITS": null,
        "DRIVERDATA": 1,
        "TYPE": 6,
        "ID": 19,
        "MODBUSREGISTRO": 8,
        "MODBUSREGISTRONOME": "DBX 75.0",
        "GROUP": "Ingresso_digitale"
      },
      {
        "STATIONID": 1,
        "NAME": "Ventilatore VN-2504 in marcia",
        "UNITS": null,
        "DRIVERDATA": 1,
        "TYPE": 6,
        "ID": 20,
        "MODBUSREGISTRO": 8,
        "MODBUSREGISTRONOME": "DBX 75.1",
        "GROUP": "Ingresso_digitale"
      },
      {
        "STATIONID": 1,
        "NAME": "Ventilatore 514K1 in marcia",
        "UNITS": null,
        "DRIVERDATA": 1,
        "TYPE": 6,
        "ID": 21,
        "MODBUSREGISTRO": 8,
        "MODBUSREGISTRONOME": "DBX 75.2",
        "GROUP": "Ingresso_digitale"
      },
      {
        "STATIONID": 1,
        "NAME": "Ventilatore 514K2 in marcia",
        "UNITS": null,
        "DRIVERDATA": 1,
        "TYPE": 6,
        "ID": 22,
        "MODBUSREGISTRO": 8,
        "MODBUSREGISTRONOME": "DBX 75.3",
        "GROUP": "Ingresso_digitale"
      },
      {
        "STATIONID": 1,
        "NAME": "QAL3: Tempo trascorso apertura elettrovalvola N2",
        "UNITS": null,
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 23,
        "MODBUSREGISTRO": 9
      },
      {
        "STATIONID": 1,
        "NAME": "QAL3: Tempo trascorso apertura elettrovalvola ARIA",
        "UNITS": null,
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 24,
        "MODBUSREGISTRO": 10
      },
      {
        "STATIONID": 1,
        "NAME": "QAL3: Tempo trascorso apertura elettrovalvola SO2",
        "UNITS": null,
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 25,
        "MODBUSREGISTRO": 11
      },
      {
        "STATIONID": 1,
        "NAME": "SO2",
        "UNITS": "mg/Nm3",
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 26,
        "MODBUSREGISTRO": 17
      },
      {
        "STATIONID": 1,
        "NAME": "Temperatura fumi",
        "UNITS": "°C",
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 27,
        "MODBUSREGISTRO": 33
      }
    ],
    "bitinfo": [
      {
        "MEASUREID": 5,
        "BITNO": 8,
        "BITNAME": "Blocco da BSS2",
        "TEXTON": "Blocco",
        "TEXTOFF": "OFF"
      },
      {
        "MEASUREID": 5,
        "BITNO": 9,
        "BITNAME": "Allarme bassa portata FT-2611",
        "TEXTON": "Allarme",
        "TEXTOFF": "OFF"
      },
      {
        "MEASUREID": 5,
        "BITNO": 10,
        "BITNAME": "Allarme bassa portata FT-310",
        "TEXTON": "Allarme",
        "TEXTOFF": "OFF"
      },
      {
        "MEASUREID": 5,
        "BITNO": 11,
        "BITNAME": "Allarme bassa portata FT-313",
        "TEXTON": "Allarme",
        "TEXTOFF": "OFF"
      },
      {
        "MEASUREID": 5,
        "BITNO": 12,
        "BITNAME": "AI303A allarme basso pH",
        "TEXTON": "Allarme",
        "TEXTOFF": "OFF"
      },
      {
        "MEASUREID": 5,
        "BITNO": 13,
        "BITNAME": "AI303B allarme basso pH",
        "TEXTON": "Allarme",
        "TEXTOFF": "OFF"
      },
      {
        "MEASUREID": 5,
        "BITNO": 14,
        "BITNAME": "AI2602A allarme basso pH",
        "TEXTON": "Allarme",
        "TEXTOFF": "OFF"
      },
      {
        "MEASUREID": 5,
        "BITNO": 15,
        "BITNAME": "AI2602B allarme basso pH",
        "TEXTON": "Allarme",
        "TEXTOFF": "OFF"
      },
      {
        "MEASUREID": 5,
        "BITNO": 1,
        "BITNAME": "PM-302A in marcia",
        "TEXTON": "Comando",
        "TEXTOFF": "OFF"
      },
      {
        "MEASUREID": 5,
        "BITNO": 2,
        "BITNAME": "PM-302B in marcia",
        "TEXTON": "Comando",
        "TEXTOFF": "OFF"
      },
      {
        "MEASUREID": 5,
        "BITNO": 4,
        "BITNAME": "PM-310A in marcia",
        "TEXTON": "Comando",
        "TEXTOFF": "OFF"
      },
      {
        "MEASUREID": 5,
        "BITNO": 5,
        "BITNAME": "PM-310B in marcia",
        "TEXTON": "Comando",
        "TEXTOFF": "OFF"
      },
      {
        "MEASUREID": 6,
        "BITNO": 8,
        "BITNAME": "PM-2600A in marcia",
        "TEXTON": "Comando",
        "TEXTOFF": "OFF"
      },
      {
        "MEASUREID": 6,
        "BITNO": 9,
        "BITNAME": "PM-2600B in marcia",
        "TEXTON": "Comando",
        "TEXTOFF": "OFF"
      },
      {
        "MEASUREID": 6,
        "BITNO": 10,
        "BITNAME": "PM-2601A in marcia",
        "TEXTON": "Comando",
        "TEXTOFF": "OFF"
      },
      {
        "MEASUREID": 6,
        "BITNO": 11,
        "BITNAME": "PM-2601B in marcia",
        "TEXTON": "Comando",
        "TEXTOFF": "OFF"
      },
      {
        "MEASUREID": 6,
        "BITNO": 12,
        "BITNAME": "PM-2604A in marcia",
        "TEXTON": "Comando",
        "TEXTOFF": "OFF"
      },
      {
        "MEASUREID": 6,
        "BITNO": 13,
        "BITNAME": "PM-2604B in marcia",
        "TEXTON": "Comando",
        "TEXTOFF": "OFF"
      },
      {
        "MEASUREID": 6,
        "BITNO": 0,
        "BITNAME": "Ventilatore VN-400 in marcia",
        "TEXTON": "Comando",
        "TEXTOFF": "OFF"
      },
      {
        "MEASUREID": 6,
        "BITNO": 1,
        "BITNAME": "Ventilatore VN-2504 in marcia",
        "TEXTON": "Comando",
        "TEXTOFF": "OFF"
      },
      {
        "MEASUREID": 6,
        "BITNO": 2,
        "BITNAME": "Ventilatore 514K1 in marcia",
        "TEXTON": "Comando",
        "TEXTOFF": "OFF"
      },
      {
        "MEASUREID": 6,
        "BITNO": 3,
        "BITNAME": "Ventilatore 514K2 in marcia",
        "TEXTON": "Comando",
        "TEXTOFF": "OFF"
      }
    ]
  }
],
[
  {
    "NAME": "Sistema Analisi Emissioni",
    "DRIVERNAME": "modbusplc",
    "DRIVERCONFIG": ":",
    "ID": 1,
    "measures": [
      {
        "STATIONID": 1,
        "NAME": "SO2",
        "UNITS": "mg/Nm3",
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 1,
        "MODBUSREGISTRO": 49
      },
      {
        "STATIONID": 1,
        "NAME": "SO2",
        "UNITS": "mg/Nm3",
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 2,
        "MODBUSREGISTRO": 51
      },
      {
        "STATIONID": 1,
        "NAME": "SO2",
        "UNITS": "mg/Nm3",
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 3,
        "MODBUSREGISTRO": 53
      },
      {
        "STATIONID": 1,
        "NAME": "SO2",
        "UNITS": "mg/Nm3",
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 4,
        "MODBUSREGISTRO": 55
      },
      {
        "STATIONID": 1,
        "NAME": "SO2",
        "UNITS": "mg/Nm3",
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 5,
        "MODBUSREGISTRO": 57
      },
      {
        "STATIONID": 1,
        "NAME": "SO2",
        "UNITS": "mg/Nm3",
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 6,
        "MODBUSREGISTRO": 59
      },
      {
        "STATIONID": 1,
        "NAME": "SO2",
        "UNITS": "mg/Nm3",
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 7,
        "MODBUSREGISTRO": 61
      },
      {
        "STATIONID": 1,
        "NAME": "SO2",
        "UNITS": "mg/Nm3",
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 8,
        "MODBUSREGISTRO": 63
      },
      {
        "STATIONID": 1,
        "NAME": "Temperatura fumi",
        "UNITS": "°C",
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 9,
        "MODBUSREGISTRO": 65
      },
      {
        "STATIONID": 1,
        "NAME": "Temperatura fumi",
        "UNITS": "°C",
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 10,
        "MODBUSREGISTRO": 67
      },
      {
        "STATIONID": 1,
        "NAME": "Temperatura fumi",
        "UNITS": "°C",
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 11,
        "MODBUSREGISTRO": 69
      },
      {
        "STATIONID": 1,
        "NAME": "Temperatura fumi",
        "UNITS": "°C",
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 12,
        "MODBUSREGISTRO": 71
      },
      {
        "STATIONID": 1,
        "NAME": "Temperatura fumi",
        "UNITS": "°C",
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 13,
        "MODBUSREGISTRO": 73
      },
      {
        "STATIONID": 1,
        "NAME": "Temperatura fumi",
        "UNITS": "°C",
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 14,
        "MODBUSREGISTRO": 75
      },
      {
        "STATIONID": 1,
        "NAME": "Temperatura fumi",
        "UNITS": "°C",
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 15,
        "MODBUSREGISTRO": 77
      },
      {
        "STATIONID": 1,
        "NAME": "Temperatura fumi",
        "UNITS": "°C",
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 16,
        "MODBUSREGISTRO": 79
      },
      {
        "STATIONID": 1,
        "NAME": "Impostazioni",
        "UNITS": null,
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 17,
        "MODBUSREGISTRO": 401
      },
      {
        "STATIONID": 1,
        "NAME": "Impostazioni",
        "UNITS": null,
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 18,
        "MODBUSREGISTRO": 402
      },
      {
        "STATIONID": 1,
        "NAME": "Impostazioni",
        "UNITS": null,
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 19,
        "MODBUSREGISTRO": 403
      },
      {
        "STATIONID": 1,
        "NAME": "Impostazioni",
        "UNITS": null,
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 20,
        "MODBUSREGISTRO": 404
      },
      {
        "STATIONID": 1,
        "NAME": "Impostazioni",
        "UNITS": null,
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 21,
        "MODBUSREGISTRO": 405
      },
      {
        "STATIONID": 1,
        "NAME": "Impostazioni",
        "UNITS": null,
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 22,
        "MODBUSREGISTRO": 406
      },
      {
        "STATIONID": 1,
        "NAME": "Impostazioni",
        "UNITS": null,
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 23,
        "MODBUSREGISTRO": 407
      },
      {
        "STATIONID": 1,
        "NAME": "Impostazioni",
        "UNITS": null,
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 24,
        "MODBUSREGISTRO": 408
      },
      {
        "STATIONID": 1,
        "NAME": "Impostazioni",
        "UNITS": null,
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 25,
        "MODBUSREGISTRO": 409
      },
      {
        "STATIONID": 1,
        "NAME": "Impostazioni",
        "UNITS": null,
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 26,
        "MODBUSREGISTRO": 410
      },
      {
        "STATIONID": 1,
        "NAME": "Impostazioni",
        "UNITS": null,
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 27,
        "MODBUSREGISTRO": 411
      },
      {
        "STATIONID": 1,
        "NAME": "Impostazioni",
        "UNITS": null,
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 28,
        "MODBUSREGISTRO": 412
      },
      {
        "STATIONID": 1,
        "NAME": "Impostazioni",
        "UNITS": null,
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 29,
        "MODBUSREGISTRO": 413
      },
      {
        "STATIONID": 1,
        "NAME": "Impostazioni",
        "UNITS": null,
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 30,
        "MODBUSREGISTRO": 414
      },
      {
        "STATIONID": 1,
        "NAME": "Impostazioni",
        "UNITS": null,
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 31,
        "MODBUSREGISTRO": 415
      },
      {
        "STATIONID": 1,
        "NAME": "Impostazioni",
        "UNITS": null,
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 32,
        "MODBUSREGISTRO": 416
      },
      {
        "STATIONID": 1,
        "NAME": "PC life signal",
        "UNITS": null,
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 33,
        "MODBUSREGISTRO": 417
      },
      {
        "STATIONID": 1,
        "NAME": "Start autocal",
        "UNITS": null,
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 34,
        "MODBUSREGISTRO": 418
      },
      {
        "STATIONID": 1,
        "NAME": "Stop autocal",
        "UNITS": null,
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 35,
        "MODBUSREGISTRO": 419
      },
      {
        "STATIONID": 1,
        "NAME": "Comandi",
        "UNITS": null,
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 36,
        "MODBUSREGISTRO": 420
      },
      {
        "STATIONID": 1,
        "NAME": "Comandi",
        "UNITS": null,
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 37,
        "MODBUSREGISTRO": 421
      },
      {
        "STATIONID": 1,
        "NAME": "Comandi",
        "UNITS": null,
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 38,
        "MODBUSREGISTRO": 422
      },
      {
        "STATIONID": 1,
        "NAME": "Comandi",
        "UNITS": null,
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 39,
        "MODBUSREGISTRO": 423
      },
      {
        "STATIONID": 1,
        "NAME": "Ack allarmi",
        "UNITS": null,
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 40,
        "MODBUSREGISTRO": 424
      },
      {
        "STATIONID": 1,
        "NAME": "Impianto in manutenzione",
        "UNITS": null,
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 41,
        "MODBUSREGISTRO": 425
      },
      {
        "STATIONID": 1,
        "NAME": "Impianto fuori servizio per guasto",
        "UNITS": null,
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 42,
        "MODBUSREGISTRO": 426
      },
      {
        "STATIONID": 1,
        "NAME": "Comandi",
        "UNITS": null,
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 43,
        "MODBUSREGISTRO": 427
      },
      {
        "STATIONID": 1,
        "NAME": "Comandi",
        "UNITS": null,
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 44,
        "MODBUSREGISTRO": 428
      },
      {
        "STATIONID": 1,
        "NAME": "Comandi",
        "UNITS": null,
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 45,
        "MODBUSREGISTRO": 429
      },
      {
        "STATIONID": 1,
        "NAME": "Allarme supero ultima media",
        "UNITS": null,
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 46,
        "MODBUSREGISTRO": 430
      },
      {
        "STATIONID": 1,
        "NAME": "Allarme supero media previsionale",
        "UNITS": null,
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 47,
        "MODBUSREGISTRO": 431
      },
      {
        "STATIONID": 1,
        "NAME": "stimata SO2",
        "UNITS": "mg/Nm3",
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 48,
        "MODBUSREGISTRO": 432
      },
      {
        "STATIONID": 1,
        "NAME": "stimata SO2",
        "UNITS": "mg/Nm3",
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 49,
        "MODBUSREGISTRO": 433
      },
      {
        "STATIONID": 1,
        "NAME": "stimata SO2",
        "UNITS": "mg/Nm3",
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 50,
        "MODBUSREGISTRO": 434
      },
      {
        "STATIONID": 1,
        "NAME": "stimata SO2",
        "UNITS": "mg/Nm3",
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 51,
        "MODBUSREGISTRO": 435
      },
      {
        "STATIONID": 1,
        "NAME": "stimata SO2",
        "UNITS": "mg/Nm3",
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 52,
        "MODBUSREGISTRO": 436
      }
    ],
    "bitinfo": []
  }
]]'''

input_json = json.loads(input_json)

# --- Passaggio 1: raccogli i dati di connessione dai group STATION_INFORMATIONS ---
ip_plc = ""
porta = None
nome_stazione = ""
stazione = ""

for group in input_json:
    for station in group:
        if station.get("STATION_INFORMATIONS"):
            # Prendi IP e porta solo se presenti (sono nel primo gruppo SI)
            if station.get("ip_plc") is not None:
                ip_plc = station.get("ip_plc", "")
                porta  = station.get("port")
            # nome_stazione e stazione: prendi il primo valorizzato
            if not nome_stazione and station.get("nome_stazione"):
                nome_stazione = station.get("nome_stazione", "")
            if not stazione and station.get("stazione"):
                stazione = station.get("stazione", "")

driver_config = f"{ip_plc}:{porta if porta is not None else ''}"

# --- Passaggio 2: fondi tutti i group non-STATION_INFORMATIONS ---
merged_measures = []
merged_bitinfo  = []
base_station    = None

measure_id_offset = 0
bitinfo_id_offset = 0

for group in input_json:
    for station in group:
        if station.get("STATION_INFORMATIONS"):
            continue

        # Usa il primo oggetto stazione come base strutturale
        if base_station is None:
            base_station = {
                "NAME":         nome_stazione,
                "DRIVERNAME":   station.get("DRIVERNAME", "modbusplc"),
                "DRIVERCONFIG": driver_config,
                "ID":           station.get("ID", 1),
            }

        group_measures = station.get("measures", [])
        group_bitinfo  = station.get("bitinfo", [])

        # Ricalcola gli ID misure in modo che non collidano tra group
        for m in group_measures:
            new_m = dict(m)
            new_m["ID"] = m["ID"] + measure_id_offset
            merged_measures.append(new_m)

        # Ricalcola i MEASUREID nei bitinfo in modo coerente con gli ID misura
        for b in group_bitinfo:
            new_b = dict(b)
            new_b["MEASUREID"] = b["MEASUREID"] + measure_id_offset
            merged_bitinfo.append(new_b)

        if group_measures:
            measure_id_offset += max(m["ID"] for m in group_measures)

# --- Passaggio 3: assembla l'output ---
base_station["measures"] = merged_measures
base_station["bitinfo"]  = merged_bitinfo

output = json.dumps([base_station], indent=4, ensure_ascii=False)
print(output)

with open('testlocaljson.json', 'w') as file:
    json.dump([base_station], file, ensure_ascii=False, indent=4)