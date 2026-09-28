
import json
import struct
import traceback
import re

# Modificato la parte di apici nel DRIVERCONFIG per farlo funzionare correttamente
input_json = r'''[
  {
    "NAME": "Emissione",
    "DRIVERNAME": "modbusplc",
    "DRIVERCONFIG": "192.168.1.1:511",
    "ID": 1,
    "measures": [
      {
        "STATIONID": 1,
        "NAME": "Allarme sonda riscaldata",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 1,
        "MODBUSREGISTRO": 1,
        "GROUP": "Ingresso_digitale"
      },
      {
        "STATIONID": 1,
        "NAME": "Allarme linea riscaldata",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 2,
        "MODBUSREGISTRO": 1,
        "GROUP": "Ingresso_digitale"
      },
      {
        "STATIONID": 1,
        "NAME": "Allarme frigorifero",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 3,
        "MODBUSREGISTRO": 1,
        "GROUP": "Ingresso_digitale"
      },
      {
        "STATIONID": 1,
        "NAME": "Allarme presenza condensa",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 4,
        "MODBUSREGISTRO": 1,
        "GROUP": "Ingresso_digitale"
      },
      {
        "STATIONID": 1,
        "NAME": "Allarme mancanza flusso",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 5,
        "MODBUSREGISTRO": 1,
        "GROUP": "Ingresso_digitale"
      },
      {
        "STATIONID": 1,
        "NAME": "Allarme CO-O2",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 6,
        "MODBUSREGISTRO": 1,
        "GROUP": "Ingresso_digitale"
      },
      {
        "STATIONID": 1,
        "NAME": "Allarme comunicazione CO-O2",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 7,
        "MODBUSREGISTRO": 1,
        "GROUP": "Ingresso_digitale"
      },
      {
        "STATIONID": 1,
        "NAME": "Warm-up NO",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 8,
        "MODBUSREGISTRO": 1,
        "GROUP": "Ingresso_digitale"
      },
      {
        "STATIONID": 1,
        "NAME": "Allarme NO",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 9,
        "MODBUSREGISTRO": 1,
        "GROUP": "Ingresso_digitale"
      },
      {
        "STATIONID": 1,
        "NAME": "Sistema in",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 10,
        "MODBUSREGISTRO": 3,
        "GROUP": "Ingresso_digitale"
      },
      {
        "STATIONID": 1,
        "NAME": "Calibrazione automatica in corso",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 11,
        "MODBUSREGISTRO": 3,
        "GROUP": "Ingresso_digitale"
      },
      {
        "STATIONID": 1,
        "NAME": "CO-O2 in calibrazione di zero",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 12,
        "MODBUSREGISTRO": 3,
        "GROUP": "Ingresso_digitale"
      },
      {
        "STATIONID": 1,
        "NAME": "CO-O2 in calibrazione di span",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 13,
        "MODBUSREGISTRO": 3,
        "GROUP": "Ingresso_digitale"
      },
      {
        "STATIONID": 1,
        "NAME": "NOx in calibrazione di zero",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 14,
        "MODBUSREGISTRO": 3,
        "GROUP": "Ingresso_digitale"
      },
      {
        "STATIONID": 1,
        "NAME": "NOx in calibrazione di span",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 15,
        "MODBUSREGISTRO": 3,
        "GROUP": "Ingresso_digitale"
      },
      {
        "STATIONID": 1,
        "NAME": "Pompa analisi",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 16,
        "MODBUSREGISTRO": 3,
        "GROUP": "Ingresso_digitale"
      },
      {
        "STATIONID": 1,
        "NAME": "Stato elettrovalvola cal zero",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 17,
        "MODBUSREGISTRO": 4,
        "GROUP": "Ingresso_digitale"
      },
      {
        "STATIONID": 1,
        "NAME": "Stato elettrovalvola taratura",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 18,
        "MODBUSREGISTRO": 4,
        "GROUP": "Ingresso_digitale"
      },
      {
        "STATIONID": 1,
        "NAME": "Stato elettrovalvola cal span",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 19,
        "MODBUSREGISTRO": 4,
        "GROUP": "Ingresso_digitale"
      },
      {
        "STATIONID": 1,
        "NAME": "Elettrovalvola cal da sonda",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 20,
        "MODBUSREGISTRO": 4,
        "GROUP": "Ingresso_digitale"
      },
      {
        "STATIONID": 1,
        "NAME": "Convertitore in bypass",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 21,
        "MODBUSREGISTRO": 4,
        "GROUP": "Ingresso_digitale"
      },
      {
        "STATIONID": 1,
        "NAME": "PLC life signal",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 22,
        "MODBUSREGISTRO": 4,
        "GROUP": "Ingresso_digitale"
      },
      {
        "STATIONID": 1,
        "NAME": "Impianto in marcia",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 23,
        "MODBUSREGISTRO": 4,
        "GROUP": "Ingresso_digitale"
      },
      {
        "STATIONID": 1,
        "NAME": "Impianto in minimo tecnico/funzionamento anomalo",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 24,
        "MODBUSREGISTRO": 4,
        "GROUP": "Ingresso_digitale"
      },
      {
        "STATIONID": 1,
        "NAME": "Impianto in avviamento",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 25,
        "MODBUSREGISTRO": 4,
        "GROUP": "Ingresso_digitale"
      },
      {
        "STATIONID": 1,
        "NAME": "Impianto in spegnimento",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 26,
        "MODBUSREGISTRO": 4,
        "GROUP": "Ingresso_digitale"
      },
      {
        "STATIONID": 1,
        "NAME": "SME in manutenzione",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 27,
        "MODBUSREGISTRO": 4,
        "GROUP": "Ingresso_digitale"
      },
      {
        "STATIONID": 1,
        "NAME": "Impianto in manutenzione",
        "UNITS": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "ID": 28,
        "MODBUSREGISTRO": 4,
        "GROUP": "Ingresso_digitale"
      },
      {
        "STATIONID": 1,
        "NAME": "NOx (in ppm)",
        "UNITS": "mg/Nm3",
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 29,
        "MODBUSREGISTRO": 18
      },
      {
        "STATIONID": 1,
        "NAME": "Temperatura fumi",
        "UNITS": "°C",
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 30,
        "MODBUSREGISTRO": 25
      },
      {
        "STATIONID": 1,
        "NAME": "Portata gas",
        "UNITS": "Nm3/h",
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 31,
        "MODBUSREGISTRO": 31
      },
      {
        "STATIONID": 1,
        "NAME": "Potenza elettrica",
        "UNITS": null,
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 32,
        "MODBUSREGISTRO": 32
      },
      {
        "STATIONID": 1,
        "NAME": "CO",
        "UNITS": "mg/Nm3",
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 33,
        "MODBUSREGISTRO": 33
      },
      {
        "STATIONID": 1,
        "NAME": "O2 Secco",
        "UNITS": "%",
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 34,
        "MODBUSREGISTRO": 37
      },
      {
        "STATIONID": 1,
        "NAME": "CO riferito",
        "UNITS": "mg/Nm3",
        "DRIVERDATA": 5,
        "TYPE": 6,
        "ID": 35,
        "MODBUSREGISTRO": 193
      },
      {
        "STATIONID": 1,
        "NAME": "NO espressi come NO2 riferiti",
        "UNITS": "mg/Nm3",
        "DRIVERDATA": 5,
        "TYPE": 6,
        "ID": 36,
        "MODBUSREGISTRO": 194
      },
      {
        "STATIONID": 1,
        "NAME": "O2 secco",
        "UNITS": "%",
        "DRIVERDATA": 5,
        "TYPE": 6,
        "ID": 37,
        "MODBUSREGISTRO": 195
      },
      {
        "STATIONID": 1,
        "NAME": "O2 umido",
        "UNITS": "%",
        "DRIVERDATA": 5,
        "TYPE": 6,
        "ID": 38,
        "MODBUSREGISTRO": 196
      },
      {
        "STATIONID": 1,
        "NAME": "Portata fumi secca",
        "UNITS": "Nm3/h",
        "DRIVERDATA": 5,
        "TYPE": 6,
        "ID": 39,
        "MODBUSREGISTRO": 197
      },
      {
        "STATIONID": 1,
        "NAME": "Heartbit PLC",
        "UNITS": null,
        "DRIVERDATA": 5,
        "TYPE": 6,
        "ID": 40,
        "MODBUSREGISTRO": 209
      },
      {
        "STATIONID": 1,
        "NAME": "Stop calibrazione",
        "UNITS": null,
        "DRIVERDATA": 5,
        "TYPE": 6,
        "ID": 41,
        "MODBUSREGISTRO": 211
      },
      {
        "STATIONID": 1,
        "NAME": "Start autocal zero",
        "UNITS": null,
        "DRIVERDATA": 5,
        "TYPE": 6,
        "ID": 42,
        "MODBUSREGISTRO": 212
      },
      {
        "STATIONID": 1,
        "NAME": "Start QAL3",
        "UNITS": null,
        "DRIVERDATA": 5,
        "TYPE": 6,
        "ID": 43,
        "MODBUSREGISTRO": 213
      },
      {
        "STATIONID": 1,
        "NAME": "Stop QAL3",
        "UNITS": null,
        "DRIVERDATA": 5,
        "TYPE": 6,
        "ID": 44,
        "MODBUSREGISTRO": 214
      },
      {
        "STATIONID": 1,
        "NAME": "Bypass convertitore",
        "UNITS": null,
        "DRIVERDATA": 5,
        "TYPE": 6,
        "ID": 45,
        "MODBUSREGISTRO": 216
      },
      {
        "STATIONID": 1,
        "NAME": "Ack allarmi",
        "UNITS": null,
        "DRIVERDATA": 5,
        "TYPE": 6,
        "ID": 46,
        "MODBUSREGISTRO": 217
      },
      {
        "STATIONID": 1,
        "NAME": "Superamento media archiviata",
        "UNITS": null,
        "DRIVERDATA": 1,
        "TYPE": 6,
        "ID": 47,
        "MODBUSREGISTRO": 221
      },
      {
        "STATIONID": 1,
        "NAME": "Superamento media previsionale",
        "UNITS": null,
        "DRIVERDATA": 1,
        "TYPE": 6,
        "ID": 48,
        "MODBUSREGISTRO": 222
      },
      {
        "STATIONID": 1,
        "NAME": "stimata NOx (in ppm)",
        "UNITS": "mg/Nm3",
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 49,
        "MODBUSREGISTRO": 226
      },
      {
        "STATIONID": 1,
        "NAME": "stimata Temperatura fumi",
        "UNITS": "°C",
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 50,
        "MODBUSREGISTRO": 233
      },
      {
        "STATIONID": 1,
        "NAME": "stimata Portata gas",
        "UNITS": "Nm3/h",
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 51,
        "MODBUSREGISTRO": 239
      },
      {
        "STATIONID": 1,
        "NAME": "stimata Potenza elettrica",
        "UNITS": null,
        "DRIVERDATA": 0,
        "TYPE": 0,
        "ID": 52,
        "MODBUSREGISTRO": 240
      }
    ],
    "bitinfo": [
      {
        "MEASUREID": 1,
        "BITNO": 8,
        "BITNAME": "Allarme sonda riscaldata",
        "TEXTON": "Allarme",
        "TEXTOFF": "OFF",
        "STATIONID": 1
      },
      {
        "MEASUREID": 1,
        "BITNO": 9,
        "BITNAME": "Allarme linea riscaldata",
        "TEXTON": "Allarme",
        "TEXTOFF": "OFF",
        "STATIONID": 1
      },
      {
        "MEASUREID": 1,
        "BITNO": 10,
        "BITNAME": "Allarme frigorifero",
        "TEXTON": "Allarme",
        "TEXTOFF": "OFF",
        "STATIONID": 1
      },
      {
        "MEASUREID": 1,
        "BITNO": 11,
        "BITNAME": "Allarme presenza condensa",
        "TEXTON": "Allarme",
        "TEXTOFF": "OFF",
        "STATIONID": 1
      },
      {
        "MEASUREID": 1,
        "BITNO": 12,
        "BITNAME": "Allarme mancanza flusso",
        "TEXTON": "Allarme",
        "TEXTOFF": "OFF",
        "STATIONID": 1
      },
      {
        "MEASUREID": 1,
        "BITNO": 0,
        "BITNAME": "Allarme analizzatore CO-O2",
        "TEXTON": "Allarme",
        "TEXTOFF": "OFF",
        "STATIONID": 1
      },
      {
        "MEASUREID": 1,
        "BITNO": 1,
        "BITNAME": "Allarme comunicazione CO-O2",
        "TEXTON": "Allarme",
        "TEXTOFF": "OFF",
        "STATIONID": 1
      },
      {
        "MEASUREID": 1,
        "BITNO": 2,
        "BITNAME": "Warm-up analizzatore NO",
        "TEXTON": "Allarme",
        "TEXTOFF": "OFF",
        "STATIONID": 1
      },
      {
        "MEASUREID": 1,
        "BITNO": 3,
        "BITNAME": "Allarme analizzatore NO",
        "TEXTON": "Allarme",
        "TEXTOFF": "OFF",
        "STATIONID": 1
      },
      {
        "MEASUREID": 3,
        "BITNO": 8,
        "BITNAME": "Sistema in misura",
        "TEXTON": "Misura",
        "TEXTOFF": "OFF",
        "STATIONID": 1
      },
      {
        "MEASUREID": 3,
        "BITNO": 9,
        "BITNAME": "Calibrazione automatica in corso",
        "TEXTON": "Calibrazione",
        "TEXTOFF": "OFF",
        "STATIONID": 1
      },
      {
        "MEASUREID": 3,
        "BITNO": 10,
        "BITNAME": "Analizzatore CO-O2 in calibrazione di zero",
        "TEXTON": "Calibrazione",
        "TEXTOFF": "OFF",
        "STATIONID": 1
      },
      {
        "MEASUREID": 3,
        "BITNO": 11,
        "BITNAME": "Analizzatore CO-O2 in calibrazione di span",
        "TEXTON": "Calibrazione",
        "TEXTOFF": "OFF",
        "STATIONID": 1
      },
      {
        "MEASUREID": 3,
        "BITNO": 12,
        "BITNAME": "Analizzatore NOx in calibrazione di zero",
        "TEXTON": "Calibrazione",
        "TEXTOFF": "OFF",
        "STATIONID": 1
      },
      {
        "MEASUREID": 3,
        "BITNO": 13,
        "BITNAME": "Analizzatore NOx in calibrazione di span",
        "TEXTON": "Calibrazione",
        "TEXTOFF": "OFF",
        "STATIONID": 1
      },
      {
        "MEASUREID": 3,
        "BITNO": 7,
        "BITNAME": "Pompa analisi",
        "TEXTON": "Calibrazione",
        "TEXTOFF": "OFF",
        "STATIONID": 1
      },
      {
        "MEASUREID": 4,
        "BITNO": 8,
        "BITNAME": "Stato elettrovalvola cal zero",
        "TEXTON": "Stato",
        "TEXTOFF": "OFF",
        "STATIONID": 1
      },
      {
        "MEASUREID": 4,
        "BITNO": 9,
        "BITNAME": "Stato elettrovalvola taratura",
        "TEXTON": "Stato",
        "TEXTOFF": "OFF",
        "STATIONID": 1
      },
      {
        "MEASUREID": 4,
        "BITNO": 10,
        "BITNAME": "Stato elettrovalvola cal span",
        "TEXTON": "Stato",
        "TEXTOFF": "OFF",
        "STATIONID": 1
      },
      {
        "MEASUREID": 4,
        "BITNO": 11,
        "BITNAME": "Elettrovalvola cal da sonda",
        "TEXTON": "Stato",
        "TEXTOFF": "OFF",
        "STATIONID": 1
      },
      {
        "MEASUREID": 4,
        "BITNO": 12,
        "BITNAME": "Convertitore in bypass",
        "TEXTON": "Bypass",
        "TEXTOFF": "OFF",
        "STATIONID": 1
      },
      {
        "MEASUREID": 4,
        "BITNO": 13,
        "BITNAME": "PLC life signal",
        "TEXTON": "Stato",
        "TEXTOFF": "OFF",
        "STATIONID": 1
      },
      {
        "MEASUREID": 4,
        "BITNO": 0,
        "BITNAME": "Impianto in marcia",
        "TEXTON": "Marcia",
        "TEXTOFF": "OFF",
        "STATIONID": 1
      },
      {
        "MEASUREID": 4,
        "BITNO": 1,
        "BITNAME": "Impianto in minimo tecnico/funzionamento anomalo",
        "TEXTON": "Anomalia",
        "TEXTOFF": "OFF",
        "STATIONID": 1
      },
      {
        "MEASUREID": 4,
        "BITNO": 2,
        "BITNAME": "Impianto in avviamento",
        "TEXTON": "Avviamento",
        "TEXTOFF": "OFF",
        "STATIONID": 1
      },
      {
        "MEASUREID": 4,
        "BITNO": 3,
        "BITNAME": "Impianto in spegnimento",
        "TEXTON": "Spegnimento",
        "TEXTOFF": "OFF",
        "STATIONID": 1
      },
      {
        "MEASUREID": 4,
        "BITNO": 5,
        "BITNAME": "SME in manutenzione",
        "TEXTON": "Manutenzione",
        "TEXTOFF": "OFF",
        "STATIONID": 1
      },
      {
        "MEASUREID": 4,
        "BITNO": 6,
        "BITNAME": "Impianto in manutenzione",
        "TEXTON": "Manutenzione",
        "TEXTOFF": "OFF",
        "STATIONID": 1
      },
      {
        "MEASUREID": 209,
        "BITNO": 0,
        "BITNAME": "Heartbit PLC",
        "TEXTON": "Heartbit",
        "TEXTOFF": "OFF",
        "STATIONID": 1
      },
      {
        "MEASUREID": 211,
        "BITNO": 0,
        "BITNAME": "Stop calibrazione",
        "TEXTON": "Calibrazione",
        "TEXTOFF": "OFF",
        "STATIONID": 1
      },
      {
        "MEASUREID": 212,
        "BITNO": 0,
        "BITNAME": "Start autocal zero",
        "TEXTON": "Calibrazione",
        "TEXTOFF": "OFF",
        "STATIONID": 1
      },
      {
        "MEASUREID": 213,
        "BITNO": 0,
        "BITNAME": "Start QAL3",
        "TEXTON": "QAL3",
        "TEXTOFF": "OFF",
        "STATIONID": 1
      },
      {
        "MEASUREID": 214,
        "BITNO": 0,
        "BITNAME": "Stop QAL3",
        "TEXTON": "QAL3",
        "TEXTOFF": "OFF",
        "STATIONID": 1
      },
      {
        "MEASUREID": 216,
        "BITNO": 0,
        "BITNAME": "Bypass convertitore",
        "TEXTON": "Allarmi",
        "TEXTOFF": "OFF",
        "STATIONID": 1
      },
      {
        "MEASUREID": 217,
        "BITNO": 0,
        "BITNAME": "Ack allarmi",
        "TEXTON": "Allarmi",
        "TEXTOFF": "OFF",
        "STATIONID": 1
      },
      {
        "MEASUREID": 220,
        "BITNO": 0,
        "BITNAME": "Superamento media archiviata",
        "TEXTON": "Comando",
        "TEXTOFF": "OFF",
        "STATIONID": 1
      },
      {
        "MEASUREID": 221,
        "BITNO": 0,
        "BITNAME": "Superamento media archiviata",
        "TEXTON": "Comando",
        "TEXTOFF": "OFF",
        "STATIONID": 1
      },
      {
        "MEASUREID": 222,
        "BITNO": 0,
        "BITNAME": "Superamento media previsionale",
        "TEXTON": "Comando",
        "TEXTOFF": "OFF",
        "STATIONID": 1
      },
      {
        "MEASUREID": 223,
        "BITNO": 0,
        "BITNAME": "Superamento media archiviata",
        "TEXTON": "Comando",
        "TEXTOFF": "OFF",
        "STATIONID": 1
      },
      {
        "MEASUREID": 224,
        "BITNO": 0,
        "BITNAME": "Superamento media archiviata",
        "TEXTON": "Comando",
        "TEXTOFF": "OFF",
        "STATIONID": 1
      }
    ]
  }
]
'''

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
                    print(this_reg)
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

        # ----------------------------------------------------------------
        # FIX BUG 4: elimina i bitinfo duplicati/hallucinati che puntano a
        # registri Modbus inesistenti riusando BITNAME+TEXTON+TEXTOFF di un
        # bit reale già presente nella stessa stazione (tipico errore
        # dell'agente bitinfo su registri adiacenti a un bit vero).
        # Un bitinfo irrisolvibile viene scartato SOLO se esiste già,
        # nella stessa stazione, un altro bitinfo con firma identica che
        # si è risolto correttamente su una misura reale. Altrimenti è
        # trattato come orfano genuino e mantenuto con MEASUREID null,
        # segnalato via log per revisione manuale.
        # ----------------------------------------------------------------
        _valid_signatures = {}

        for b in new_bitinfo:
            _resolved = new_measure_id_dict.get(b.get('_pippo'))
            if _resolved is not None:
                _sig = (b['BITNAME'], b['TEXTON'], b['TEXTOFF'])
                _valid_signatures[_sig] = _resolved

        _final_bitinfo = []

        for b in new_bitinfo:
            _resolved = new_measure_id_dict.get(b.get('_pippo'))
            _sig = (b['BITNAME'], b['TEXTON'], b['TEXTOFF'])

            if _resolved is not None:
                b['MEASUREID'] = _resolved
                del b['_pippo']
                _final_bitinfo.append(b)
            elif _sig in _valid_signatures:
                print(f"[INFO] bitinfo duplicato scartato (registro fantasma "
                      f"{b.get('_pippo')}): {b['BITNAME']}")
                continue
            else:
                print(f"[WARN] bitinfo orfano, nessuna misura trovata "
                      f"(MEASUREID grezzo={b.get('_pippo')}): {b['BITNAME']}")
                b['MEASUREID'] = None
                del b['_pippo']
                _final_bitinfo.append(b)

        new_bitinfo = _final_bitinfo

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

    with open('testlocaljson.json', 'w') as file:
        json.dump(result, file, indent=4, ensure_ascii=True)
    
    #for key, value in new_measureid_bitinfo.items():
        #print(f'{key} : {value}')
    
except Exception as e:
    error_msg = traceback.format_exc()
    error_report = [{
        "err":   str(e),
        "trace": error_msg
    }]
    output_json = json.dumps(error_report, indent=2, ensure_ascii=False)
    print(output_json)