import json

input_json = r'''[ [
    {
        "nome_stazione": "SME",
        "stazione": "centrale Edison di teleriscaldamento a Rivoli (TO)",
        "protocollo": "ModBus TCP",
        "ip_plc": "192.168.1.1",
        "port": 511,
        "var": [],
        "STATION_INFORMATIONS": true
    },
    {
        "NAME": "SME",
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
                "NAME": "Allarme CO-O2",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 1,
                "MODBUSREGISTRO": 1
            },
            {
                "STATIONID": 1,
                "NAME": "Allarme comunicazione CO-O2",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 1,
                "MODBUSREGISTRO": 1
            },
            {
                "STATIONID": 1,
                "NAME": "Warm-up NO",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 1,
                "MODBUSREGISTRO": 1
            },
            {
                "STATIONID": 1,
                "NAME": "Allarme NO",
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
                "NAME": "CO-O2 in calibrazione di zero",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 1,
                "MODBUSREGISTRO": 3
            },
            {
                "STATIONID": 1,
                "NAME": "CO-O2 in calibrazione di span",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 1,
                "MODBUSREGISTRO": 3
            },
            {
                "STATIONID": 1,
                "NAME": "NOx in calibrazione di zero",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 1,
                "MODBUSREGISTRO": 3
            },
            {
                "STATIONID": 1,
                "NAME": "NOx in calibrazione di span",
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
                "NAME": "Stato elettrovalvola taratura",
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
                "NAME": "Convertitore in bypass",
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
                "BITNO": 0,
                "BITNAME": "Allarme analizzatore CO-O2",
                "TEXTON": "Allarme",
                "TEXTOFF": "OFF"
            },
            {
                "MEASUREID": 1,
                "BITNO": 1,
                "BITNAME": "Allarme comunicazione CO-O2",
                "TEXTON": "Allarme",
                "TEXTOFF": "OFF"
            },
            {
                "MEASUREID": 1,
                "BITNO": 2,
                "BITNAME": "Warm-up analizzatore NO",
                "TEXTON": "Allarme",
                "TEXTOFF": "OFF"
            },
            {
                "MEASUREID": 1,
                "BITNO": 3,
                "BITNAME": "Allarme analizzatore NO",
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
                "TEXTON": "Attivo",
                "TEXTOFF": "OFF"
            },
            {
                "MEASUREID": 3,
                "BITNO": 10,
                "BITNAME": "Analizzatore CO-O2 in calibrazione di zero",
                "TEXTON": "Attivo",
                "TEXTOFF": "OFF"
            },
            {
                "MEASUREID": 3,
                "BITNO": 11,
                "BITNAME": "Analizzatore CO-O2 in calibrazione di span",
                "TEXTON": "Attivo",
                "TEXTOFF": "OFF"
            },
            {
                "MEASUREID": 3,
                "BITNO": 12,
                "BITNAME": "Analizzatore NOx in calibrazione di zero",
                "TEXTON": "Attivo",
                "TEXTOFF": "OFF"
            },
            {
                "MEASUREID": 3,
                "BITNO": 13,
                "BITNAME": "Analizzatore NOx in calibrazione di span",
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
                "BITNAME": "Stato elettrovalvola taratura",
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
                "BITNO": 12,
                "BITNAME": "Convertitore in bypass",
                "TEXTON": "Bypass",
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
                "TEXTON": "Marcia",
                "TEXTOFF": "OFF"
            },
            {
                "MEASUREID": 4,
                "BITNO": 1,
                "BITNAME": "Impianto in minimo tecnico/funzionamento anomalo",
                "TEXTON": "Anomalia",
                "TEXTOFF": "OFF"
            },
            {
                "MEASUREID": 4,
                "BITNO": 2,
                "BITNAME": "Impianto in avviamento",
                "TEXTON": "Avviamento",
                "TEXTOFF": "OFF"
            },
            {
                "MEASUREID": 4,
                "BITNO": 3,
                "BITNAME": "Impianto in spegnimento",
                "TEXTON": "Spegnimento",
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
            }
        ]
    }
] ,
 [
    {
        "NAME": "Sistema analisi emissioni",
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
                "NAME": "Allarme CO-O2",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 1,
                "MODBUSREGISTRO": 1
            },
            {
                "STATIONID": 1,
                "NAME": "Allarme comunicazione CO-O2",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 1,
                "MODBUSREGISTRO": 1
            },
            {
                "STATIONID": 1,
                "NAME": "Warm-up NO",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 1,
                "MODBUSREGISTRO": 1
            },
            {
                "STATIONID": 1,
                "NAME": "Allarme NO",
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
                "NAME": "CO-O2 in calibrazione di zero",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 1,
                "MODBUSREGISTRO": 3
            },
            {
                "STATIONID": 1,
                "NAME": "CO-O2 in calibrazione di span",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 1,
                "MODBUSREGISTRO": 3
            },
            {
                "STATIONID": 1,
                "NAME": "NOx in calibrazione di zero",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 1,
                "MODBUSREGISTRO": 3
            },
            {
                "STATIONID": 1,
                "NAME": "NOx in calibrazione di span",
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
                "NAME": "Stato elettrovalvola taratura",
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
                "NAME": "Convertitore in bypass",
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
                "BITNO": 0,
                "BITNAME": "Allarme analizzatore CO-O2",
                "TEXTON": "Allarme",
                "TEXTOFF": "OFF"
            },
            {
                "MEASUREID": 1,
                "BITNO": 1,
                "BITNAME": "Allarme comunicazione CO-O2",
                "TEXTON": "Allarme",
                "TEXTOFF": "OFF"
            },
            {
                "MEASUREID": 1,
                "BITNO": 2,
                "BITNAME": "Warm-up analizzatore NO",
                "TEXTON": "Allarme",
                "TEXTOFF": "OFF"
            },
            {
                "MEASUREID": 1,
                "BITNO": 3,
                "BITNAME": "Allarme analizzatore NO",
                "TEXTON": "Allarme",
                "TEXTOFF": "OFF"
            },
            {
                "MEASUREID": 3,
                "BITNO": 8,
                "BITNAME": "Sistema in misura",
                "TEXTON": "Marcia",
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
                "BITNAME": "Analizzatore CO-O2 in calibrazione di zero",
                "TEXTON": "Calibrazione",
                "TEXTOFF": "OFF"
            },
            {
                "MEASUREID": 3,
                "BITNO": 11,
                "BITNAME": "Analizzatore CO-O2 in calibrazione di span",
                "TEXTON": "Calibrazione",
                "TEXTOFF": "OFF"
            },
            {
                "MEASUREID": 3,
                "BITNO": 12,
                "BITNAME": "Analizzatore NOx in calibrazione di zero",
                "TEXTON": "Calibrazione",
                "TEXTOFF": "OFF"
            },
            {
                "MEASUREID": 3,
                "BITNO": 13,
                "BITNAME": "Analizzatore NOx in calibrazione di span",
                "TEXTON": "Calibrazione",
                "TEXTOFF": "OFF"
            },
            {
                "MEASUREID": 3,
                "BITNO": 7,
                "BITNAME": "Pompa analisi",
                "TEXTON": "Calibrazione",
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
                "BITNAME": "Stato elettrovalvola taratura",
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
                "BITNO": 12,
                "BITNAME": "Convertitore in bypass",
                "TEXTON": "Bypass",
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
                "TEXTON": "Marcia",
                "TEXTOFF": "OFF"
            },
            {
                "MEASUREID": 4,
                "BITNO": 1,
                "BITNAME": "Impianto in minimo tecnico/funzionamento anomalo",
                "TEXTON": "Anomalia",
                "TEXTOFF": "OFF"
            },
            {
                "MEASUREID": 4,
                "BITNO": 2,
                "BITNAME": "Impianto in avviamento",
                "TEXTON": "Avviamento",
                "TEXTOFF": "OFF"
            },
            {
                "MEASUREID": 4,
                "BITNO": 3,
                "BITNAME": "Impianto in spegnimento",
                "TEXTON": "Spegnimento",
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
            }
        ]
    }
] ] 
'''

input_json = json.loads(input_json)

if isinstance(input_json, list):
    # Creiamo una lista escludendo i vettori vuoti []
    stazioni_popolate = [station for station in input_json if station]
    
    # Verifichiamo che TUTTE quelle rimaste abbiano STATION_INFORMATIONS a True
    if stazioni_popolate and all(s[0].get('STATION_INFORMATIONS') for s in stazioni_popolate):
        print('All of them are station informations!')
        output = 'ERRORE: tutte le stazioni contengono solo informazioni sulla stazione'
    elif stazioni_popolate and all(not s[0].get('STATION_INFORMATIONS') for s in stazioni_popolate):
        print('All of them are measure informations! ')
        output = 'ERRORE: tutte le stazioni contengono solo misure'
    elif stazioni_popolate:
        output = json.dumps(stazioni_popolate, indent=4, ensure_ascii=False)
    else:
        output = 'ERRORE: Nessun formato riconosciuto'    
        
    print(output)