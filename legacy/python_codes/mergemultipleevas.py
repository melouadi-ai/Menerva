"""
plc_merger_strings.py
=====================
Merges the string outputs of the five Qwen models into the final
station/measures/bitinfo structure required by the PLC monitoring system.

No functions, no classes — pure sequential imperative code.

INPUTS: assign the raw string output from each model to the five variables
        below (M1_STRING … M5_STRING).  Each string is the JSON text the
        model returned — markdown fences are stripped automatically.

OUTPUT: the variable `result` holds the final list of station dicts,
        ready for json.dumps() or direct use.
"""

import json
import re
from copy import deepcopy

# ---------------------------------------------------------------------------
# CONFIGURATION — paste each model's raw string output here
# ---------------------------------------------------------------------------

M1_STRING = r'''[
  {
    "ID": 1,
    "NAME": "SME",
    "DRIVERNAME": "modbusplc",
    "DRIVERCONFIG": "192.168.1.50:502"
  },
  {
    "ID": 2,
    "NAME": "SME",
    "DRIVERNAME": "modbusplc",
    "DRIVERCONFIG": "xxx.xxx.xxx.xxx:"
  }
]'''



M2_STRING = r"""[
  {
    "STATIONID": 1,
    "NAME": "Temp. Linea Preli",
    "UNITS": "°C",
    "DRIVERDATA": 0,
    "TYPE": 0,
    "ID": 1,
    "MODBUSREGISTRO": 40051,
    "STARTSCALE_ENG": 0,
    "ENDSCALE_ENG": 0
  },
  {
    "STATIONID": 1,
    "NAME": "Press. Fumi",
    "UNITS": "mBar",
    "DRIVERDATA": 0,
    "TYPE": 0,
    "ID": 1,
    "MODBUSREGISTRO": 40053,
    "STARTSCALE_ENG": 0,
    "ENDSCALE_ENG": 0
  },
  {
    "STATIONID": 1,
    "NAME": "Temp. Fumi",
    "UNITS": "°C",
    "DRIVERDATA": 0,
    "TYPE": 0,
    "ID": 1,
    "MODBUSREGISTRO": 40055,
    "STARTSCALE_ENG": 0,
    "ENDSCALE_ENG": 0
  },
  {
    "STATIONID": 1,
    "NAME": "Potenza Cogener",
    "UNITS": "kW",
    "DRIVERDATA": 0,
    "TYPE": 0,
    "ID": 1,
    "MODBUSREGISTRO": 40057,
    "STARTSCALE_ENG": 0,
    "ENDSCALE_ENG": 0
  },
  {
    "STATIONID": 1,
    "NAME": "Portata Gas",
    "UNITS": "Nm3/h",
    "DRIVERDATA": 0,
    "TYPE": 0,
    "ID": 1,
    "MODBUSREGISTRO": 40059,
    "STARTSCALE_ENG": 0,
    "ENDSCALE_ENG": 0
  },
  {
    "STATIONID": 1,
    "NAME": "Temp. Linea Preli",
    "UNITS": "°C",
    "DRIVERDATA": 0,
    "TYPE": 0,
    "ID": 1,
    "MODBUSREGISTRO": 40063,
    "STARTSCALE_ENG": 0,
    "ENDSCALE_ENG": 0
  },
  {
    "STATIONID": 1,
    "NAME": "Press. Fumi",
    "UNITS": "mBar",
    "DRIVERDATA": 0,
    "TYPE": 0,
    "ID": 1,
    "MODBUSREGISTRO": 40065,
    "STARTSCALE_ENG": 0,
    "ENDSCALE_ENG": 0
  },
  {
    "STATIONID": 1,
    "NAME": "Temp. Fumi",
    "UNITS": "°C",
    "DRIVERDATA": 0,
    "TYPE": 0,
    "ID": 1,
    "MODBUSREGISTRO": 40067,
    "STARTSCALE_ENG": 0,
    "ENDSCALE_ENG": 0
  },
  {
    "STATIONID": 1,
    "NAME": "Potenza Cogener",
    "UNITS": "kW",
    "DRIVERDATA": 0,
    "TYPE": 0,
    "ID": 1,
    "MODBUSREGISTRO": 40069,
    "STARTSCALE_ENG": 0,
    "ENDSCALE_ENG": 0
  },
  {
    "STATIONID": 1,
    "NAME": "Portata Gas",
    "UNITS": "Nm3/h",
    "DRIVERDATA": 0,
    "TYPE": 0,
    "ID": 1,
    "MODBUSREGISTRO": 40071,
    "STARTSCALE_ENG": 0,
    "ENDSCALE_ENG": 0
  },
  {
    "STATIONID": 1,
    "NAME": "CO",
    "UNITS": "mg/m3",
    "DRIVERDATA": 0,
    "TYPE": 0,
    "ID": 1,
    "MODBUSREGISTRO": 40109,
    "STARTSCALE_ENG": 0,
    "ENDSCALE_ENG": 0
  },
  {
    "STATIONID": 1,
    "NAME": "NO",
    "UNITS": "mg/m3",
    "DRIVERDATA": 0,
    "TYPE": 0,
    "ID": 1,
    "MODBUSREGISTRO": 40111,
    "STARTSCALE_ENG": 0,
    "ENDSCALE_ENG": 0
  },
  {
    "STATIONID": 1,
    "NAME": "O2",
    "UNITS": "%",
    "DRIVERDATA": 0,
    "TYPE": 0,
    "ID": 1,
    "MODBUSREGISTRO": 40113,
    "STARTSCALE_ENG": 0,
    "ENDSCALE_ENG": 0
  },
  {
    "STATIONID": 1,
    "NAME": "CO",
    "UNITS": "mg/m3",
    "DRIVERDATA": 0,
    "TYPE": 0,
    "ID": 1,
    "MODBUSREGISTRO": 40115,
    "STARTSCALE_ENG": 0,
    "ENDSCALE_ENG": 0
  },
  {
    "STATIONID": 1,
    "NAME": "NO",
    "UNITS": "mg/m3",
    "DRIVERDATA": 0,
    "TYPE": 0,
    "ID": 1,
    "MODBUSREGISTRO": 40117,
    "STARTSCALE_ENG": 0,
    "ENDSCALE_ENG": 0
  },
  {
    "STATIONID": 1,
    "NAME": "O2",
    "UNITS": "%",
    "DRIVERDATA": 0,
    "TYPE": 0,
    "ID": 1,
    "MODBUSREGISTRO": 40119,
    "STARTSCALE_ENG": 0,
    "ENDSCALE_ENG": 0
  },
  {
    "STATIONID": 1,
    "NAME": "Contatore Funz. Pompa",
    "UNITS": "h",
    "DRIVERDATA": 0,
    "TYPE": 0,
    "ID": 1,
    "MODBUSREGISTRO": 40161,
    "STARTSCALE_ENG": 0,
    "ENDSCALE_ENG": 0
  },
  {
    "STATIONID": 1,
    "NAME": "Contatore Funz. Pompa",
    "UNITS": "h",
    "DRIVERDATA": 0,
    "TYPE": 0,
    "ID": 1,
    "MODBUSREGISTRO": 40165,
    "STARTSCALE_ENG": 0,
    "ENDSCALE_ENG": 0
  },
  {
    "STATIONID": 1,
    "NAME": "Contatore Funz. Cartuccia",
    "UNITS": "h",
    "DRIVERDATA": 0,
    "TYPE": 0,
    "ID": 1,
    "MODBUSREGISTRO": 40173,
    "STARTSCALE_ENG": 0,
    "ENDSCALE_ENG": 0
  },
  {
    "STATIONID": 1,
    "NAME": "Contatore Funz. Cartuccia",
    "UNITS": "h",
    "DRIVERDATA": 0,
    "TYPE": 0,
    "ID": 1,
    "MODBUSREGISTRO": 40175,
    "STARTSCALE_ENG": 0,
    "ENDSCALE_ENG": 0
  },
  {
    "STATIONID": 1,
    "NAME": "Watchdog Comunicaz.",
    "UNITS": null,
    "DRIVERDATA": 0,
    "TYPE": 0,
    "ID": 1,
    "MODBUSREGISTRO": 40008
  },
  {
    "STATIONID": 1,
    "NAME": "Watchdog_DA SME Server 01",
    "UNITS": null,
    "DRIVERDATA": 0,
    "TYPE": 0,
    "ID": 1,
    "MODBUSREGISTRO": 40009
  },
  {
    "STATIONID": 1,
    "NAME": "Watchdog_DA SME Server 02",
    "UNITS": null,
    "DRIVERDATA": 0,
    "TYPE": 0,
    "ID": 1,
    "MODBUSREGISTRO": 40010
  }
]"""



M3_STRING = r"""[
  {
    "STATIONID": 1,
    "NAME": "COMANDO ACK RESET",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40001,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COMANDO TACITAZIONE SIRENA",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40001,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: COMANDO RESET ORE CARTUCCIA",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40001,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: COMANDO RESET ORE CARTUCCIA",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40001,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: COMANDO Autocal ULTRAMAT 23 NO+CO+O2",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40001,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: COMANDO Autocal ULTRAMAT 23 NO+CO+O2",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40001,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: COMANDO START VERIFICA QAL 3 CO+NO+O2",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40001,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: COMANDO STOP VERIFICA QAL 3 CO+NO+O2",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40001,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: COMANDO SET BYPASS CONVERTITORE NO2-NO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40001,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: COMANDO RESET BYPASS CONVERTITORE NO2-NO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40001,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: COMANDO START VERIFICA QAL 3 CO+NO+O2",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40001,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: COMANDO STOP VERIFICA QAL 3 CO+NO+O2",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40001,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: COMANDO SET BYPASS CONVERTITORE NO2-NO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40001,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: COMANDO RESET BYPASS CONVERTITORE NO2-NO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40001,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "SELEZIONE CALIBRAZ/VERIFICA ZERO PER CO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40003,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "SELEZIONE CALIBRAZ/VERIFICA ZERO PER NO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40003,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "SELEZIONE CALIBRAZ/VERIFICA ZERO PER O2",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40003,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "SELEZIONE CALIBRAZ/VERIFICA SPAN PER CO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40003,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "SELEZIONE CALIBRAZ/VERIFICA SPAN PER NO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40003,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "SELEZIONE CALIBRAZ/VERIFICA SPAN PER O2",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40003,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "FAULT COMUNICAZIONE PC SME",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40011,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "FAULT COMUNICAZIONE Con DCS",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40011,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "ANALOG Output DCS Forzatl",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40011,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "SELETTORE MANUTENZIONE GENERALE",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40011,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: Fault analogica MISURA TEMPERATURA LINEA",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40012,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: Fault analogica MISURA PRESSIONE FUMI",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40012,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: Fault analogica MISURA TEMPERATURA FUMI",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40012,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: Fault analogica MISURA POTENZA_MOTORE",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40012,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: Fault analogica MISURA PORTATA GAS",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40012,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "Fault analogica MISURA Ris_006",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40012,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: Fault analogica MISURA TEMPERATURA LINEA",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40012,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: Fault analogica MISURA PRESSIONE FUMI",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40012,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: Fault analogica MISURA TEMPERATURA FUMI",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40012,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: Fault analogica MISURA POTENZA_MOTORE",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40012,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: Fault analogica MISURA PORTATA GAS",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40012,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: Fault analogica MISURA Ris_012",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40012,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "Gen: ALLARME SITOP SELECT 24Vdc",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40013,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "Gen: ALLARME ALTA TEMPERATURA QUADRO ANALISI",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40013,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "Gen: SCATTO INTERRUTTORI",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40013,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: ALLARME TEMPERATURA SONDA DI PRELIEVO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40014,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: ALLARME TEMPERATURA LINEA DI PRELIEVO BL1",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40014,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: BLOCCO ALTISSIME TEMPERATURE In REGOLAZIONE BL1",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40014,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: ALLARME FRIGO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40014,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: ALLARME PRESENZA CONDENSA",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40014,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: MEMORIA PRESENZA CONDENSA",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40014,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: PSL BASSA PRESSIONE GAS DI MISURA",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40014,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: SELETTORE MANUTENZIONE",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40014,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: SCATTO INTERRUTTORI",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40014,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: ALLARME CONVERTITORE NO2/NO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40014,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: ANOMALIA ANALIZZATORE U23 CO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40014,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: ALLARME BAD_QUALITY MISURA CO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40014,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: ANOMALIA ANALIZZATORE U23 NO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40014,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: ALLARME BAD_QUALITY MISURA NO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40014,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: ANOMALIA ANALIZZATORE U23 O2",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40014,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: ALLARME BAD_QUALITY MISURA O2",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40014,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: ALLARME TEMPERATURA SONDA DI PRELIEVO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40016,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: ALLARME TEMPERATURA LINEA DI PRELIEVO BL2",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40016,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: BLOCCO ALTISSIME TEMPERATURE In REGOLAZIONE BL2",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40016,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: ALLARME FRIGO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40016,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: ALLARME PRESENZA CONDENSA",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40016,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: MEMORIA PRESENZA CONDENSA",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40016,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: PSL BASSA PRESSIONE GAS DI MISURA",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40016,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: SELETTORE MANUTENZIONE",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40016,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: SCATTO INTERRUTTORI",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40016,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: ALLARME CONVERTITORE NO2/NO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40016,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: ANOMALIA ANALIZZATORE U23 CO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40016,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: ALLARME BAD_QUALITY MISURA CO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40016,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: ANOMALIA ANALIZZATORE U23 NO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40016,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: ALLARME BAD_QUALITY MISURA NO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40016,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: ANOMALIA ANALIZZATORE U23 O2",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40016,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: ALLARME BAD_QUALITY MISURA O2",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40016,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: ALLARME COMUNICAZIONE ANALIZZATORE U23 CO-NO+O2",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40017,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: ALLARME VERIFICA QAL3 CO+NO+O2 Terminata CON ERRORI",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40017,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "ABILIT.MEMORIZZAZIONE DATA In TO MMC",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40021,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "MEMORIZZAZIONE DATA MMC OK",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40021,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "MEMORIZZAZIONE DATA MMC ERRORE",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40021,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "MEMORIZZAZIONE IN CORSO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40021,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: OR ALLARMI",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40021,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: OR ALLARMI",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40021,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "Gen: OR ALLARMI",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40021,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "Gen: PULSANTE DI RESET",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40021,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: IN MISURA ANALIZZATORE.U23 CO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40022,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: IN CALIBRAZIONE ANALIZZATORE U23. CO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40022,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: SPAN GAS ANALIZZATORE U23. CO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40022,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: ZERO GAS ANALIZZATORE U23 CO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40022,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: IN MISURA ANALIZZATORE.U23 NO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40022,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: IN CALIBRAZIONE ANALIZZATORE U23. NO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40022,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: SPAN GAS ANALIZZATORE U23. NO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40022,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: ZERO GAS ANALIZZATORE U23 NO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40022,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: IN MISURA ANALIZZATORE.U23 O2",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40022,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: IN CALIBRAZIONE ANALIZZATORE U23. O2",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40022,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: SPAN GAS ANALIZZATORE U23. O2",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40022,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: ZERO GAS ANALIZZATORE U23 O2",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40022,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: AUTOCAL U 23 NO+CO+O2 IN CORSO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40022,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: SELETTORE INSERIMENTO POMPA P1",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40023,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: STATO COMANDO POMPA P1",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40023,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: COM. ELT YV1",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40023,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: COM. ELT YV3",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40023,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: COM. CONVERTITORE",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40023,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: MOTORE IN MARCIA",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40023,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: STATO VERIFICA QAL3 CO+NO+O2 IN CORSO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40023,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: STATO VERIFICA QAL3 CO+NO+O2 TERMINATA SENZA ERRORI",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40023,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: MOTORE IN MANUTENZIONE",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40023,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: PREALLARME EMISSIONE CO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40023,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: PREALLARME EMISSIONE NO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40023,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: ALLARME SUPERAMENTO EMISSIONI",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40023,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: IN MISURA ANALIZZATORE.U23 CO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40024,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: IN CALIBRAZIONE ANALIZZATORE U23. CO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40024,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: SPAN GAS ANALIZZATORE U23. CO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40024,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: ZERO GAS ANALIZZATORE U23 CO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40024,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: IN MISURA ANALIZZATORE.U23 NO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40024,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: IN CALIBRAZIONE ANALIZZATORE U23. NO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40024,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: SPAN GAS ANALIZZATORE U23. NO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40024,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: ZERO GAS ANALIZZATORE U23 NO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40024,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: IN MISURA ANALIZZATORE.U23 O2",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40024,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: IN CALIBRAZIONE ANALIZZATORE U23. O2",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40024,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: SPAN GAS ANALIZZATORE U23. O2",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40024,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: ZERO GAS ANALIZZATORE U23 O2",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40024,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: AUTOCAL U 23 NO IN CORSO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40024,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: SELETTORE INSERIMENTO POMPA P1",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40025,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: STATO COMANDO POMPA P1",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40025,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: COM. ELT YV2",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40025,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: COM. ELT YV4",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40025,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: COM. CONVERTITORE",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40025,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: MOTORE IN MARCIA",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40025,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: STATO VERIFICA QAL3 CO+NO+O2 IN CORSO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40025,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: STATO VERIFICA QAL3 CO+NO+O2 TERMINATA SENZA ERRORI",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40025,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: MOTORE IN MANUTENZIONE",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40025,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: PREALLARME EMISSIONE CO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40025,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: PREALLARME EMISSIONE NO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40025,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: ALLARME SUPERAMENTO EMISSIONI",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40025,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: Validita MISURA PRESSIONE FUMI",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40028,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: Validita MISURA TEMPERATURA FUMI",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40028,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: Validita MISURA POTENZA_COG",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40028,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: Validita MISURA PORTATA GAS I",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40028,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: Validita MISURA CO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40028,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: Validita MISURA NO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40028,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG2: Validita MISURA O2",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40028,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: Validita MISURA PRESSIONE FUMI",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40028,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: Validita MISURA TEMPERATURA FUMI",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40028,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: Validita MISURA POTENZA_COG",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40028,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: Validita MISURA PORTATA GAS I",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40028,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: Validita MISURA CO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40028,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: Validita MISURA NO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40028,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "COG3: Validita MISURA O2",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40028,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "Gen: ALLARME SITOP SELECT 24Vdc",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40031,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "M1: SCATTO INTERRUTTORI",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40031,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "M1: PULSANTE RESET",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40031,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "M1: SELETTORE MANUTENZIONE",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40031,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "M1: SELETTORE INSERIMENTO POMPA PRELIEVO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40031,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "M1: PULSANTE BYPASS NO2/NO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40031,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "M1: PSL BASSA PRESSIONE GAS DI MISURA",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40031,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "M1: ALLARME TEMPERATURA SONDA DI PRELIEVO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40031,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "M1-M2: ALLARME FRIGO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40031,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "M1: PRESENZA CONDENSA",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40031,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "M1: ALLARME CONVERTITORE NO2/NO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40031,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "M1: MOTORE In MARCIA",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40031,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "Gen: ALLARME ALTA TEMPERATURA QUADRO ANALISI",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40032,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "M2: SCATTO INTERRUTTORI",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40032,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "M2: PULSANTE RESET",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40032,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "M2: SELETTORE MANUTENZIONE",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40032,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "M2: SELETTORE INSERIMENTO POMPA PRELIEVO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40032,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "M2: PULSANTE BYPASS NO2/NO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40032,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "M2: PSL BASSA PRESSIONE GAS DI MISURA",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40032,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "M2: ALLARME TEMPERATURA SONDA DI PRELIEVO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40032,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "Gen: SCATTO INTERRUTTORI",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40032,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "M2: PRESENZA CONDENSA",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40032,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "M2: ALLARME CONVERTITORE NO2/NO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40032,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "M2: MOTORE IN MARCIA",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40032,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "BL1: COM SSR RISCALDAMENTO LINEA PRELIEVO M1",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40041,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "M1: COM. ELT YV1",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40041,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "M1: COM. ELT YV3",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40041,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "M1: COM. CONVERTITORE",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40041,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "M1: COM. Sync ULTRAMAT 23 NO+CO+O2",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40041,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "M1: COMANDO POMPA",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40041,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "M1: LAMPADA OR ALLARMI",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40041,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "M1: LAMPADA SELETTORE POMPA",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40041,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "M1: Ripetizione CUMULATIVO ALLARME",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40041,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "M1: Ripetizione IN MANUTENZIONE",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40041,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "M1: Ripetizione 01 PREALLARME EMISSIONE CO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40041,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "M1: Ripetizione 01 PREALLARME EMISSIONE NO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40041,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "M1: Ripetizione 01 ALLARME SUPERAMENTO EMISSIONI",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40041,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "M1: Ripetizione 02 PREALLARME EMISSIONE CO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40041,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "M1: Ripetizione 02 PREALLARME EMISSIONE NO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40041,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "M1: Ripetizione 02 ALLARME SUPERAMENTO EMISSIONI",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40041,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "BL2: COM SSR RISCALDAMENTO LINEA PRELIEVO M2",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40042,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "M2: COM. ELT YV2",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40042,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "M2: COM. ELT YV4",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40042,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "M2: COM. CONVERTITORE",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40042,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "M2: COM. Sync ULTRAMAT 23 NO+CO+O2",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40042,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "M2: COMANDO POMPA",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40042,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "M2: LAMPADA OR ALLARMI",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40042,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "M2: LAMPADA SELETTORE POMPA",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40042,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "M2: Ripetizione CUMULATIVO ALLARME",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40042,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "M2: Ripetizione IN MANUTENZIONE",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40042,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "M2: Ripetizione 01 PREALLARME EMISSIONE CO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40042,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "M2: Ripetizione 01 PREALLARME EMISSIONE NO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40042,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "M2: Ripetizione 01 ALLARME SUPERAMENTO EMISSIONI",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40042,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "M2: Ripetizione 02 PREALLARME EMISSIONE CO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40042,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "M2: Ripetizione 02 PREALLARME EMISSIONE NO",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40042,
    "GROUP": "Ingresso_digitale"
  },
  {
    "STATIONID": 1,
    "NAME": "M2: Ripetizione 02 ALLARME SUPERAMENTO EMISSIONI",
    "UNITS": null,
    "DRIVERDATA": 2,
    "TYPE": 1,
    "ID": 1,
    "MODBUSREGISTRO": 40042,
    "GROUP": "Ingresso_digitale"
  }
]"""



M4_STRING = r"""[
  {
    "MEASUREID": 40001,
    "BITNO": 9,
    "BITNAME": "COMANDO ACK RESET (impulsivo)",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40001,
    "BITNO": 10,
    "BITNAME": "COMANDO TACITAZIONE SIRENA (impulsivo)",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40001,
    "BITNO": 11,
    "BITNAME": "COG2: COMANDO RESET ORE CARTUCCIA (impulsivo)",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40001,
    "BITNO": 12,
    "BITNAME": "COG3: COMANDO RESET ORE CARTUCCIA (impulsivo)",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40001,
    "BITNO": 13,
    "BITNAME": "Bit 13",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40001,
    "BITNO": 14,
    "BITNAME": "COG2: COMANDO Autocal ULTRAMAT 23 \"NO+CO+O2\" (impulsivo)",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40001,
    "BITNO": 15,
    "BITNAME": "COG3: COMANDO Autocal ULTRAMAT 23 \"NO+CO+O2\" (impulsivo)",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40001,
    "BITNO": 16,
    "BITNAME": "Bit 16",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40001,
    "BITNO": 1,
    "BITNAME": "COG2: COMANDO START VERIFICA QAL 3 CO+NO+O2 (impulsivo)",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40001,
    "BITNO": 2,
    "BITNAME": "COG2: COMANDO STOP VERIFICA QAL 3 CO+NO+O2 (impulsivo)",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40001,
    "BITNO": 3,
    "BITNAME": "COG2: COMANDO SET BYPASS CONVERTITORE NO2-NO (impulsivo)",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40001,
    "BITNO": 4,
    "BITNAME": "COG2: COMANDO RESET BYPASS CONVERTITORE NO2-NO (impulsivo)",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40001,
    "BITNO": 5,
    "BITNAME": "COG3: COMANDO START VERIFICA QAL 3 CO+NO+O2 (impulsivo)",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40001,
    "BITNO": 6,
    "BITNAME": "COG3: COMANDO STOP VERIFICA QAL 3 CO+NO+O2 (impulsivo)",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40001,
    "BITNO": 7,
    "BITNAME": "COG3: COMANDO SET BYPASS CONVERTITORE NO2-NO (impulsivo)",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40001,
    "BITNO": 8,
    "BITNAME": "COG3: COMANDO RESET BYPASS CONVERTITORE NO2-NO (impulsivo)",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40002,
    "BITNO": 9,
    "BITNAME": "Bit 9",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40002,
    "BITNO": 10,
    "BITNAME": "Bit 10",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40002,
    "BITNO": 11,
    "BITNAME": "Bit 11",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40002,
    "BITNO": 12,
    "BITNAME": "Bit 12",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40002,
    "BITNO": 13,
    "BITNAME": "Bit 13",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40002,
    "BITNO": 14,
    "BITNAME": "Bit 14",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40002,
    "BITNO": 15,
    "BITNAME": "Bit 15",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40002,
    "BITNO": 16,
    "BITNAME": "Bit 16",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40002,
    "BITNO": 1,
    "BITNAME": "Bit 1",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40002,
    "BITNO": 2,
    "BITNAME": "Bit 2",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40002,
    "BITNO": 3,
    "BITNAME": "Bit 3",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40002,
    "BITNO": 4,
    "BITNAME": "Bit 4",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40002,
    "BITNO": 5,
    "BITNAME": "Bit 5",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40002,
    "BITNO": 6,
    "BITNAME": "Bit 6",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40002,
    "BITNO": 7,
    "BITNAME": "Bit 7",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40002,
    "BITNO": 8,
    "BITNAME": "Bit 8",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40003,
    "BITNO": 9,
    "BITNAME": "SELEZIONE CALIBRAZ/VERIFICA ZERO PER \"CO\"",
    "TEXTON": "Calibrazione",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40003,
    "BITNO": 10,
    "BITNAME": "SELEZIONE CALIBRAZ/VERIFICA ZERO PER \"NO\"",
    "TEXTON": "Calibrazione",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40003,
    "BITNO": 11,
    "BITNAME": "SELEZIONE CALIBRAZ/VERIFICA ZERO PER \"O2\"",
    "TEXTON": "Calibrazione",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40003,
    "BITNO": 12,
    "BITNAME": "Bit 12",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40003,
    "BITNO": 13,
    "BITNAME": "Bit 13",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40003,
    "BITNO": 14,
    "BITNAME": "Bit 14",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40003,
    "BITNO": 15,
    "BITNAME": "Bit 15",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40003,
    "BITNO": 16,
    "BITNAME": "Bit 16",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40003,
    "BITNO": 1,
    "BITNAME": "SELEZIONE CALIBRAZ/VERIFICA SPAN PER \"CO\"",
    "TEXTON": "Span",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40003,
    "BITNO": 2,
    "BITNAME": "SELEZIONE CALIBRAZ/VERIFICA SPAN PER \"NO\"",
    "TEXTON": "Span",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40003,
    "BITNO": 3,
    "BITNAME": "SELEZIONE CALIBRAZ/VERIFICA SPAN PER \"O2\"",
    "TEXTON": "Span",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40003,
    "BITNO": 4,
    "BITNAME": "Bit 4",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40003,
    "BITNO": 5,
    "BITNAME": "Bit 5",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40003,
    "BITNO": 6,
    "BITNAME": "Bit 6",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40003,
    "BITNO": 7,
    "BITNAME": "Bit 7",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40003,
    "BITNO": 8,
    "BITNAME": "Bit 8",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40004,
    "BITNO": 9,
    "BITNAME": "Bit 9",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40004,
    "BITNO": 10,
    "BITNAME": "Bit 10",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40004,
    "BITNO": 11,
    "BITNAME": "Bit 11",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40004,
    "BITNO": 12,
    "BITNAME": "Bit 12",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40004,
    "BITNO": 13,
    "BITNAME": "Bit 13",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40004,
    "BITNO": 14,
    "BITNAME": "Bit 14",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40004,
    "BITNO": 15,
    "BITNAME": "Bit 15",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40004,
    "BITNO": 16,
    "BITNAME": "Bit 16",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40004,
    "BITNO": 1,
    "BITNAME": "Bit 1",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40004,
    "BITNO": 2,
    "BITNAME": "Bit 2",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40004,
    "BITNO": 3,
    "BITNAME": "Bit 3",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40004,
    "BITNO": 4,
    "BITNAME": "Bit 4",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40004,
    "BITNO": 5,
    "BITNAME": "Bit 5",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40004,
    "BITNO": 6,
    "BITNAME": "Bit 6",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40004,
    "BITNO": 7,
    "BITNAME": "Bit 7",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40004,
    "BITNO": 8,
    "BITNAME": "Bit 8",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40005,
    "BITNO": 0,
    "BITNAME": "Libero",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40006,
    "BITNO": 9,
    "BITNAME": "Bit 9",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40006,
    "BITNO": 10,
    "BITNAME": "Bit 10",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40006,
    "BITNO": 11,
    "BITNAME": "Bit 11",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40006,
    "BITNO": 12,
    "BITNAME": "Bit 12",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40006,
    "BITNO": 13,
    "BITNAME": "Bit 13",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40006,
    "BITNO": 14,
    "BITNAME": "Bit 14",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40006,
    "BITNO": 15,
    "BITNAME": "Bit 15",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40006,
    "BITNO": 16,
    "BITNAME": "Bit 16",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40006,
    "BITNO": 1,
    "BITNAME": "Bit 1",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40006,
    "BITNO": 2,
    "BITNAME": "Bit 2",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40006,
    "BITNO": 3,
    "BITNAME": "Bit 3",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40006,
    "BITNO": 4,
    "BITNAME": "Bit 4",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40006,
    "BITNO": 5,
    "BITNAME": "Bit 5",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40006,
    "BITNO": 6,
    "BITNAME": "Bit 6",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40006,
    "BITNO": 7,
    "BITNAME": "Bit 7",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40006,
    "BITNO": 8,
    "BITNAME": "Bit 8",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40007,
    "BITNO": 0,
    "BITNAME": "Bit 0",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40008,
    "BITNO": 0,
    "BITNAME": "WATCH DOG COMUNICAZIONE PLC (se varia OK master+I/O ok)",
    "TEXTON": "OK",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40009,
    "BITNO": 0,
    "BITNAME": "WATCH_DOG_DA SME Server 01 (Valore che incrementa) (Write da PC-SME)",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40010,
    "BITNO": 0,
    "BITNAME": "WATCH_DOG_DA SME Server 02 (Valore che incrementa) (Write da PC-SME) nu",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40011,
    "BITNO": 9,
    "BITNAME": "Bit 9",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40011,
    "BITNO": 10,
    "BITNAME": "Bit 10",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40011,
    "BITNO": 11,
    "BITNAME": "Bit 11",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40011,
    "BITNO": 12,
    "BITNAME": "Bit 12",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40011,
    "BITNO": 13,
    "BITNAME": "Bit 13",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40011,
    "BITNO": 14,
    "BITNAME": "Bit 14",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40011,
    "BITNO": 15,
    "BITNAME": "Bit 15",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40011,
    "BITNO": 16,
    "BITNAME": "Bit 16",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40011,
    "BITNO": 1,
    "BITNAME": "FAULT COMUNICAZIONE PC SME",
    "TEXTON": "Guasto",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40011,
    "BITNO": 2,
    "BITNAME": "FAULT COMUNICAZIONE Con DCS",
    "TEXTON": "Guasto",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40011,
    "BITNO": 3,
    "BITNAME": "Bit 3",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40011,
    "BITNO": 4,
    "BITNAME": "Bit 4",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40011,
    "BITNO": 5,
    "BITNAME": "Bit 5",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40011,
    "BITNO": 6,
    "BITNAME": "Bit 6",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40011,
    "BITNO": 7,
    "BITNAME": "ANALOG Output DCS Forzatl",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40011,
    "BITNO": 8,
    "BITNAME": "SELETTORE MANUTENZIONE GENERALE (OR M1+M2)",
    "TEXTON": "Manutenzione",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40012,
    "BITNO": 9,
    "BITNAME": "COG2: Fault analogica MISURA \"TEMPERATURA LINEA\" (BL1)",
    "TEXTON": "Guasto",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40012,
    "BITNO": 10,
    "BITNAME": "COG2: Fault analogica MISURA \"PRESSIONE FUMI\"",
    "TEXTON": "Guasto",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40012,
    "BITNO": 11,
    "BITNAME": "COG2: Fault analogica MISURA \"TEMPERATURA FUMI\"",
    "TEXTON": "Guasto",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40012,
    "BITNO": 12,
    "BITNAME": "COG2: Fault analogica MISURA \"POTENZA_MOTORE\"",
    "TEXTON": "Guasto",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40012,
    "BITNO": 13,
    "BITNAME": "COG2: Fault analogica MISURA \"PORTATA GAS\"",
    "TEXTON": "Guasto",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40012,
    "BITNO": 14,
    "BITNAME": "Fault analogica MISURA Ris_006",
    "TEXTON": "Guasto",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40012,
    "BITNO": 15,
    "BITNAME": "COG3: Fault analogica MISURA \"TEMPERATURA LINEA\" (BL2)",
    "TEXTON": "Guasto",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40012,
    "BITNO": 16,
    "BITNAME": "COG3: Fault analogica MISURA \"PRESSIONE FUMI\"",
    "TEXTON": "Guasto",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40012,
    "BITNO": 1,
    "BITNAME": "COG3: Fault analogica MISURA \"TEMPERATURA FUMI\"",
    "TEXTON": "Guasto",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40012,
    "BITNO": 2,
    "BITNAME": "COG3: Fault analogica MISURA \"POTENZA_MOTORE\"",
    "TEXTON": "Guasto",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40012,
    "BITNO": 3,
    "BITNAME": "COG3: Fault analogica MISURA \"PORTATA GAS\"",
    "TEXTON": "Guasto",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40012,
    "BITNO": 4,
    "BITNAME": "Fault analogica MISURA Ris_012",
    "TEXTON": "Guasto",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40012,
    "BITNO": 5,
    "BITNAME": "Bit 5",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40012,
    "BITNO": 6,
    "BITNAME": "Bit 6",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40012,
    "BITNO": 7,
    "BITNAME": "Bit 7",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40012,
    "BITNO": 8,
    "BITNAME": "Bit 8",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40013,
    "BITNO": 9,
    "BITNAME": "Bit 9",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40013,
    "BITNO": 10,
    "BITNAME": "Bit 10",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40013,
    "BITNO": 11,
    "BITNAME": "Bit 11",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40013,
    "BITNO": 12,
    "BITNAME": "Bit 12",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40013,
    "BITNO": 13,
    "BITNAME": "Bit 13",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40013,
    "BITNO": 14,
    "BITNAME": "Bit 14",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40013,
    "BITNO": 15,
    "BITNAME": "Bit 15",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40013,
    "BITNO": 16,
    "BITNAME": "Bit 16",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40013,
    "BITNO": 1,
    "BITNAME": "Gen: ALLARME SITOP SELECT 24Vdc",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40013,
    "BITNO": 2,
    "BITNAME": "Gen: ALLARME ALTA TEMPERATURA QUADRO ANALISI",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40013,
    "BITNO": 3,
    "BITNAME": "Gen: SCATTO INTERRUTTORI",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40013,
    "BITNO": 4,
    "BITNAME": "Bit 4",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40013,
    "BITNO": 5,
    "BITNAME": "Bit 5",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40013,
    "BITNO": 6,
    "BITNAME": "Bit 6",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40013,
    "BITNO": 7,
    "BITNAME": "Bit 7",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40013,
    "BITNO": 8,
    "BITNAME": "Bit 8",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40014,
    "BITNO": 9,
    "BITNAME": "COG2: ALLARME TEMPERATURA SONDA DI PRELIEVO",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40014,
    "BITNO": 10,
    "BITNAME": "COG2: ALLARME TEMPERATURA LINEA DI PRELIEVO BL1",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40014,
    "BITNO": 11,
    "BITNAME": "COG2: BLOCCO ALTISSIME TEMPERATURE In REGOLAZIONE BL1",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40014,
    "BITNO": 12,
    "BITNAME": "COG2: ALLARME FRIGO",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40014,
    "BITNO": 13,
    "BITNAME": "COG2: ALLARME PRESENZA CONDENSA",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40014,
    "BITNO": 14,
    "BITNAME": "COG2: MEMORIA PRESENZA CONDENSA (Da Resettare)",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40014,
    "BITNO": 15,
    "BITNAME": "COG2: PSL BASSA PRESSIONE GAS DI MISURA",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40014,
    "BITNO": 16,
    "BITNAME": "COG2: SELETTORE MANUTENZIONE",
    "TEXTON": "Manutenzione",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40014,
    "BITNO": 1,
    "BITNAME": "COG2: SCATTO INTERRUTTORI",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40014,
    "BITNO": 2,
    "BITNAME": "COG2: ALLARME CONVERTITORE NO2/NO",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40014,
    "BITNO": 3,
    "BITNAME": "COG2: ANOMALIA ANALIZZATORE U23 \"CO\"",
    "TEXTON": "Anomalia",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40014,
    "BITNO": 4,
    "BITNAME": "COG2: ALLARME BAD_QUALITY MISURA \"CO\"",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40014,
    "BITNO": 5,
    "BITNAME": "COG2: ANOMALIA ANALIZZATORE U23 \"NO\"",
    "TEXTON": "Anomalia",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40014,
    "BITNO": 6,
    "BITNAME": "COG2: ALLARME BAD_QUALITY MISURA \"NO\"",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40014,
    "BITNO": 7,
    "BITNAME": "COG2: ANOMALIA ANALIZZATORE U23 \"O2\"",
    "TEXTON": "Anomalia",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40014,
    "BITNO": 8,
    "BITNAME": "COG2: ALLARME BAD_QUALITY MISURA \"O2\"",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40015,
    "BITNO": 9,
    "BITNAME": "COG2: ALLARME COMUNICAZIONE ANALIZZATORE U23 \"CO-NO+O2\"",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40015,
    "BITNO": 10,
    "BITNAME": "Bit 10",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40015,
    "BITNO": 11,
    "BITNAME": "Bit 11",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40015,
    "BITNO": 12,
    "BITNAME": "Bit 12",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40015,
    "BITNO": 13,
    "BITNAME": "Bit 13",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40015,
    "BITNO": 14,
    "BITNAME": "Bit 14",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40015,
    "BITNO": 15,
    "BITNAME": "Bit 15",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40015,
    "BITNO": 16,
    "BITNAME": "COG2: ALLARME VERIFICA QAL3 \"CO+NO+O2\" Terminata CON ERRORI",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40015,
    "BITNO": 1,
    "BITNAME": "Bit 1",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40015,
    "BITNO": 2,
    "BITNAME": "Bit 2",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40015,
    "BITNO": 3,
    "BITNAME": "Bit 3",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40015,
    "BITNO": 4,
    "BITNAME": "Bit 4",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40015,
    "BITNO": 5,
    "BITNAME": "Bit 5",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40015,
    "BITNO": 6,
    "BITNAME": "Bit 6",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40015,
    "BITNO": 7,
    "BITNAME": "Bit 7",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40015,
    "BITNO": 8,
    "BITNAME": "Bit 8",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40016,
    "BITNO": 9,
    "BITNAME": "COG3: ALLARME TEMPERATURA SONDA DI PRELIEVO",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40016,
    "BITNO": 10,
    "BITNAME": "COG3: ALLARME TEMPERATURA LINEA DI PRELIEVO BL2",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40016,
    "BITNO": 11,
    "BITNAME": "COG3: BLOCCO ALTISSIME TEMPERATURE In REGOLAZIONE BL2",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40016,
    "BITNO": 12,
    "BITNAME": "COG3: ALLARME FRIGO",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40016,
    "BITNO": 13,
    "BITNAME": "COG3: ALLARME PRESENZA CONDENSA",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40016,
    "BITNO": 14,
    "BITNAME": "COG3: MEMORIA PRESENZA CONDENSA (Da Resettare)",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40016,
    "BITNO": 15,
    "BITNAME": "COG3: PSL BASSA PRESSIONE GAS DI MISURA",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40016,
    "BITNO": 16,
    "BITNAME": "COG3: SELETTORE MANUTENZIONE",
    "TEXTON": "Manutenzione",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40016,
    "BITNO": 1,
    "BITNAME": "COG3: SCATTO INTERRUTTORI",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40016,
    "BITNO": 2,
    "BITNAME": "COG3: ALLARME CONVERTITORE NO2/NO",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40016,
    "BITNO": 3,
    "BITNAME": "COG3: ANOMALIA ANALIZZATORE U23 \"CO\"",
    "TEXTON": "Anomalia",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40016,
    "BITNO": 4,
    "BITNAME": "COG3: ALLARME BAD_QUALITY MISURA \"CO\"",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40016,
    "BITNO": 5,
    "BITNAME": "COG3: ANOMALIA ANALIZZATORE U23 \"NO\"",
    "TEXTON": "Anomalia",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40016,
    "BITNO": 6,
    "BITNAME": "COG3: ALLARME BAD_QUALITY MISURA \"NO\"",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40016,
    "BITNO": 7,
    "BITNAME": "COG3: ANOMALIA ANALIZZATORE U23 \"O2\"",
    "TEXTON": "Anomalia",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40016,
    "BITNO": 8,
    "BITNAME": "COG3: ALLARME BAD_QUALITY MISURA \"O2\"",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40017,
    "BITNO": 9,
    "BITNAME": "COG3: ALLARME COMUNICAZIONE ANALIZZATORE U23 \"CO-NO+O2\"",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40017,
    "BITNO": 10,
    "BITNAME": "Bit 10",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40017,
    "BITNO": 11,
    "BITNAME": "Bit 11",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40017,
    "BITNO": 12,
    "BITNAME": "Bit 12",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40017,
    "BITNO": 13,
    "BITNAME": "Bit 13",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40017,
    "BITNO": 14,
    "BITNAME": "Bit 14",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40017,
    "BITNO": 15,
    "BITNAME": "Bit 15",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40017,
    "BITNO": 16,
    "BITNAME": "COG3: ALLARME VERIFICA QAL3 \"CO+NO+O2\" Terminata CON ERRORI",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40017,
    "BITNO": 1,
    "BITNAME": "Bit 1",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40017,
    "BITNO": 2,
    "BITNAME": "Bit 2",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40017,
    "BITNO": 3,
    "BITNAME": "Bit 3",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40017,
    "BITNO": 4,
    "BITNAME": "Bit 4",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40017,
    "BITNO": 5,
    "BITNAME": "Bit 5",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40017,
    "BITNO": 6,
    "BITNAME": "Bit 6",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40017,
    "BITNO": 7,
    "BITNAME": "Bit 7",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40017,
    "BITNO": 8,
    "BITNAME": "Bit 8",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40018,
    "BITNO": 9,
    "BITNAME": "Bit 9",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40018,
    "BITNO": 10,
    "BITNAME": "Bit 10",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40018,
    "BITNO": 11,
    "BITNAME": "Bit 11",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40018,
    "BITNO": 12,
    "BITNAME": "Bit 12",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40018,
    "BITNO": 13,
    "BITNAME": "Bit 13",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40018,
    "BITNO": 14,
    "BITNAME": "Bit 14",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40018,
    "BITNO": 15,
    "BITNAME": "Bit 15",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40018,
    "BITNO": 16,
    "BITNAME": "Bit 16",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40018,
    "BITNO": 1,
    "BITNAME": "Bit 1",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40018,
    "BITNO": 2,
    "BITNAME": "Bit 2",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40018,
    "BITNO": 3,
    "BITNAME": "Bit 3",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40018,
    "BITNO": 4,
    "BITNAME": "Bit 4",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40018,
    "BITNO": 5,
    "BITNAME": "Bit 5",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40018,
    "BITNO": 6,
    "BITNAME": "Bit 6",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40018,
    "BITNO": 7,
    "BITNAME": "Bit 7",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40018,
    "BITNO": 8,
    "BITNAME": "Bit 8",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40019,
    "BITNO": 9,
    "BITNAME": "Bit 9",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40019,
    "BITNO": 10,
    "BITNAME": "Bit 10",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40019,
    "BITNO": 11,
    "BITNAME": "Bit 11",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40019,
    "BITNO": 12,
    "BITNAME": "Bit 12",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40019,
    "BITNO": 13,
    "BITNAME": "Bit 13",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40019,
    "BITNO": 14,
    "BITNAME": "Bit 14",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40019,
    "BITNO": 15,
    "BITNAME": "Bit 15",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40019,
    "BITNO": 16,
    "BITNAME": "Bit 16",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40019,
    "BITNO": 1,
    "BITNAME": "Bit 1",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40019,
    "BITNO": 2,
    "BITNAME": "Bit 2",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40019,
    "BITNO": 3,
    "BITNAME": "Bit 3",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40019,
    "BITNO": 4,
    "BITNAME": "Bit 4",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40019,
    "BITNO": 5,
    "BITNAME": "Bit 5",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40019,
    "BITNO": 6,
    "BITNAME": "Bit 6",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40019,
    "BITNO": 7,
    "BITNAME": "Bit 7",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40019,
    "BITNO": 8,
    "BITNAME": "Bit 8",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40020,
    "BITNO": 0,
    "BITNAME": "Bit 0",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40021,
    "BITNO": 9,
    "BITNAME": "ABILIT.MEMORIZZAZIONE DATA In TO MMC (EXT + TIME INTERLOCK) (Only HMI)",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40021,
    "BITNO": 10,
    "BITNAME": "MEMORIZZAZIONE DATA MMC OK (Only HMI)",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40021,
    "BITNO": 11,
    "BITNAME": "MEMORIZZAZIONE DATA MMC ERRORE (Only HMI)",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40021,
    "BITNO": 12,
    "BITNAME": "MEMORIZZAZIONE IN CORSO (Only HMI)",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40021,
    "BITNO": 13,
    "BITNAME": "Bit 13",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40021,
    "BITNO": 14,
    "BITNAME": "COG2: OR ALLARMI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40021,
    "BITNO": 15,
    "BITNAME": "COG3: OR ALLARMI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40021,
    "BITNO": 16,
    "BITNAME": "Bit 16",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40021,
    "BITNO": 1,
    "BITNAME": "Gen: OR ALLARMI (M1+M2)",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40021,
    "BITNO": 2,
    "BITNAME": "Gen: PULSANTE DI RESET (M1+M2)",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40021,
    "BITNO": 3,
    "BITNAME": "Bit 3",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40021,
    "BITNO": 4,
    "BITNAME": "Bit 4",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40021,
    "BITNO": 5,
    "BITNAME": "Bit 5",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40021,
    "BITNO": 6,
    "BITNAME": "Bit 6",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40021,
    "BITNO": 7,
    "BITNAME": "Bit 7",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40021,
    "BITNO": 8,
    "BITNAME": "Bit 8",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40022,
    "BITNO": 9,
    "BITNAME": "COG2: IN MISURA ANALIZZATORE.U23 \"CO\"",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40022,
    "BITNO": 10,
    "BITNAME": "COG2: IN CALIBRAZIONE ANALIZZATORE U23. \"CO\"",
    "TEXTON": "Calibrazione",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40022,
    "BITNO": 11,
    "BITNAME": "COG2: SPAN GAS ANALIZZATORE U23.\"CO\"",
    "TEXTON": "Span",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40022,
    "BITNO": 12,
    "BITNAME": "COG2: ZERO GAS ANALIZZATORE U23 \"CO\"",
    "TEXTON": "Zero",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40022,
    "BITNO": 13,
    "BITNAME": "COG2: IN MISURA ANALIZZATORE.U23 \"NO\"",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40022,
    "BITNO": 14,
    "BITNAME": "COG2: IN CALIBRAZIONE ANALIZZATORE U23. \"NO\"",
    "TEXTON": "Calibrazione",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40022,
    "BITNO": 15,
    "BITNAME": "COG2: SPAN GAS ANALIZZATORE U23.\"NO\"",
    "TEXTON": "Span",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40022,
    "BITNO": 16,
    "BITNAME": "COG2: ZERO GAS ANALIZZATORE U23 \"NO\"",
    "TEXTON": "Zero",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40022,
    "BITNO": 1,
    "BITNAME": "COG2: IN MISURA ANALIZZATORE.U23 \"O2\"",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40022,
    "BITNO": 2,
    "BITNAME": "COG2: IN CALIBRAZIONE ANALIZZATORE U23. \"O2\"",
    "TEXTON": "Calibrazione",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40022,
    "BITNO": 3,
    "BITNAME": "COG2: SPAN GAS ANALIZZATORE U23.\"O2\"",
    "TEXTON": "Span",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40022,
    "BITNO": 4,
    "BITNAME": "COG2: ZERO GAS ANALIZZATORE U23 \"O2\"",
    "TEXTON": "Zero",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40022,
    "BITNO": 5,
    "BITNAME": "COG2: AUTOCAL U 23 \"NO+CO+O2\" IN CORSO",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40022,
    "BITNO": 6,
    "BITNAME": "Bit 6",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40022,
    "BITNO": 7,
    "BITNAME": "Bit 7",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40022,
    "BITNO": 8,
    "BITNAME": "Bit 8",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40023,
    "BITNO": 9,
    "BITNAME": "COG2: SELETTORE INSERIMENTO POMPA P1",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40023,
    "BITNO": 10,
    "BITNAME": "COG2: STATO COMANDO POMPA P1",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40023,
    "BITNO": 11,
    "BITNAME": "COG2: COM. ELT YV1 (Mis_Cal)",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40023,
    "BITNO": 12,
    "BITNAME": "COG2: COM. ELT YV3 (Zero-SpanI)",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40023,
    "BITNO": 13,
    "BITNAME": "COG2: COM. CONVERTITORE (Bypass CONVERTITORE NO2/NO)",
    "TEXTON": "Bypass",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40023,
    "BITNO": 14,
    "BITNAME": "COG2: MOTORE IN MARCIA",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40023,
    "BITNO": 15,
    "BITNAME": "COG2: STATO VERIFICA QAL3 \"CO+NO+O2\" IN CORSO",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40023,
    "BITNO": 16,
    "BITNAME": "COG2: STATO VERIFICA QAL3 \"CO+NO+O2\" TERMINATA SENZA ERRORI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40023,
    "BITNO": 1,
    "BITNAME": "COG2: MOTORE IN MANUTENZIONE",
    "TEXTON": "Manutenzione",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40023,
    "BITNO": 2,
    "BITNAME": "COG2: PREALLARME EMISSIONE \"CO\"",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40023,
    "BITNO": 3,
    "BITNAME": "COG2: PREALLARME EMISSIONE \"NO\"",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40023,
    "BITNO": 4,
    "BITNAME": "COG2: ALLARME SUPERAMENTO EMISSIONI",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40023,
    "BITNO": 5,
    "BITNAME": "Bit 5",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40023,
    "BITNO": 6,
    "BITNAME": "Bit 6",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40023,
    "BITNO": 7,
    "BITNAME": "Bit 7",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40023,
    "BITNO": 8,
    "BITNAME": "Bit 8",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40024,
    "BITNO": 9,
    "BITNAME": "COG3: IN MISURA ANALIZZATORE.U23 \"CO\"",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40024,
    "BITNO": 10,
    "BITNAME": "COG3: IN CALIBRAZIONE ANALIZZATORE U23. \"CO\"",
    "TEXTON": "Calibrazione",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40024,
    "BITNO": 11,
    "BITNAME": "COG3: SPAN GAS ANALIZZATORE U23.\"CO\"",
    "TEXTON": "Span",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40024,
    "BITNO": 12,
    "BITNAME": "COG3: ZERO GAS ANALIZZATORE U23 \"CO\"",
    "TEXTON": "Zero",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40024,
    "BITNO": 13,
    "BITNAME": "COG3: IN MISURA ANALIZZATORE.U23 \"NO\"",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40024,
    "BITNO": 14,
    "BITNAME": "COG3: IN CALIBRAZIONE ANALIZZATORE U23. \"NO\"",
    "TEXTON": "Calibrazione",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40024,
    "BITNO": 15,
    "BITNAME": "COG3: SPAN GAS ANALIZZATORE U23.\"NO\"",
    "TEXTON": "Span",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40024,
    "BITNO": 16,
    "BITNAME": "COG3: ZERO GAS ANALIZZATORE U23 \"NO\"",
    "TEXTON": "Zero",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40024,
    "BITNO": 1,
    "BITNAME": "COG3: IN MISURA ANALIZZATORE.U23 \"O2\"",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40024,
    "BITNO": 2,
    "BITNAME": "COG3: IN CALIBRAZIONE ANALIZZATORE U23. \"O2\"",
    "TEXTON": "Calibrazione",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40024,
    "BITNO": 3,
    "BITNAME": "COG3: SPAN GAS ANALIZZATORE U23.\"O2\"",
    "TEXTON": "Span",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40024,
    "BITNO": 4,
    "BITNAME": "COG3: ZERO GAS ANALIZZATORE U23 \"O2\"",
    "TEXTON": "Zero",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40024,
    "BITNO": 5,
    "BITNAME": "COG3: AUTOCAL U 23 \"NO\" IN CORSO",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40024,
    "BITNO": 6,
    "BITNAME": "Bit 6",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40024,
    "BITNO": 7,
    "BITNAME": "Bit 7",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40024,
    "BITNO": 8,
    "BITNAME": "Bit 8",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40025,
    "BITNO": 9,
    "BITNAME": "COG3: SELETTORE INSERIMENTO POMPA P1",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40025,
    "BITNO": 10,
    "BITNAME": "COG3: STATO COMANDO POMPA P1",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40025,
    "BITNO": 11,
    "BITNAME": "COG3: COM. ELT YV2 (Mis_Cal)",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40025,
    "BITNO": 12,
    "BITNAME": "COG3: COM. ELT YV4 (Zero-SpanI)",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40025,
    "BITNO": 13,
    "BITNAME": "COG3: COM. CONVERTITORE(Bypass CONVERTITORE NO2/NO)",
    "TEXTON": "Bypass",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40025,
    "BITNO": 14,
    "BITNAME": "COG3:MOTORE IN MARCIA",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40025,
    "BITNO": 15,
    "BITNAME": "COG3: STATO VERIFICA QAL3 \"CO+NO+O2\" IN CORSO",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40025,
    "BITNO": 16,
    "BITNAME": "COG3: STATO VERIFICA QAL3 \"CO+NO+O2\" TERMINATA SENZA ERRORI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40025,
    "BITNO": 1,
    "BITNAME": "COG3: MOTORE IN MANUTENZIONE",
    "TEXTON": "Manutenzione",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40025,
    "BITNO": 2,
    "BITNAME": "COG3: PREALLARME EMISSIONE \"CO\"",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40025,
    "BITNO": 3,
    "BITNAME": "COG3: PREALLARME EMISSIONE \"NO\"",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40025,
    "BITNO": 4,
    "BITNAME": "COG3: ALLARME SUPERAMENTO EMISSIONI",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40025,
    "BITNO": 5,
    "BITNAME": "Bit 5",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40025,
    "BITNO": 6,
    "BITNAME": "Bit 6",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40025,
    "BITNO": 7,
    "BITNAME": "Bit 7",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40025,
    "BITNO": 8,
    "BITNAME": "Bit 8",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40026,
    "BITNO": 9,
    "BITNAME": "Bit 9",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40026,
    "BITNO": 10,
    "BITNAME": "Bit 10",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40026,
    "BITNO": 11,
    "BITNAME": "Bit 11",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40026,
    "BITNO": 12,
    "BITNAME": "Bit 12",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40026,
    "BITNO": 13,
    "BITNAME": "Bit 13",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40026,
    "BITNO": 14,
    "BITNAME": "Bit 14",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40026,
    "BITNO": 15,
    "BITNAME": "Bit 15",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40026,
    "BITNO": 16,
    "BITNAME": "Bit 16",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40026,
    "BITNO": 1,
    "BITNAME": "Bit 1",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40026,
    "BITNO": 2,
    "BITNAME": "Bit 2",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40026,
    "BITNO": 3,
    "BITNAME": "Bit 3",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40026,
    "BITNO": 4,
    "BITNAME": "Bit 4",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40026,
    "BITNO": 5,
    "BITNAME": "Bit 5",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40026,
    "BITNO": 6,
    "BITNAME": "Bit 6",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40026,
    "BITNO": 7,
    "BITNAME": "Bit 7",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40026,
    "BITNO": 8,
    "BITNAME": "Bit 8",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40027,
    "BITNO": 9,
    "BITNAME": "Bit 9",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40027,
    "BITNO": 10,
    "BITNAME": "Bit 10",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40027,
    "BITNO": 11,
    "BITNAME": "Bit 11",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40027,
    "BITNO": 12,
    "BITNAME": "Bit 12",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40027,
    "BITNO": 13,
    "BITNAME": "Bit 13",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40027,
    "BITNO": 14,
    "BITNAME": "Bit 14",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40027,
    "BITNO": 15,
    "BITNAME": "Bit 15",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40027,
    "BITNO": 16,
    "BITNAME": "Bit 16",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40027,
    "BITNO": 1,
    "BITNAME": "Bit 1",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40027,
    "BITNO": 2,
    "BITNAME": "Bit 2",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40027,
    "BITNO": 3,
    "BITNAME": "Bit 3",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40027,
    "BITNO": 4,
    "BITNAME": "Bit 4",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40027,
    "BITNO": 5,
    "BITNAME": "Bit 5",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40027,
    "BITNO": 6,
    "BITNAME": "Bit 6",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40027,
    "BITNO": 7,
    "BITNAME": "Bit 7",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40027,
    "BITNO": 8,
    "BITNAME": "Bit 8",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40028,
    "BITNO": 9,
    "BITNAME": "COG2: Validita MISURA \"PRESSIONE FUMI\"",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40028,
    "BITNO": 10,
    "BITNAME": "COG2: Validita MISURA \"TEMPERATURA FUMI\"",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40028,
    "BITNO": 11,
    "BITNAME": "COG2: Validita MISURA \"POTENZA_COG\"",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40028,
    "BITNO": 12,
    "BITNAME": "COG2: Validita MISURA \"PORTATA GAS I\"",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40028,
    "BITNO": 13,
    "BITNAME": "COG2: Validita MISURA \"CO\"",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40028,
    "BITNO": 14,
    "BITNAME": "COG2: Validita MISURA \"NO\"",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40028,
    "BITNO": 15,
    "BITNAME": "COG2: Validita MISURA \"O2\"",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40028,
    "BITNO": 16,
    "BITNAME": "Bit 16",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40028,
    "BITNO": 1,
    "BITNAME": "COG3: Validita MISURA \"PRESSIONE FUMI\"",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40028,
    "BITNO": 2,
    "BITNAME": "COG3: Validita MISURA \"TEMPERATURA FUMI\"",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40028,
    "BITNO": 3,
    "BITNAME": "COG3: Validita MISURA \"POTENZA_COG\"",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40028,
    "BITNO": 4,
    "BITNAME": "COG3: Validita MISURA \"PORTATA GAS I\"",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40028,
    "BITNO": 5,
    "BITNAME": "COG3: Validita MISURA \"CO\"",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40028,
    "BITNO": 6,
    "BITNAME": "COG3: Validita MISURA \"NO\"",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40028,
    "BITNO": 7,
    "BITNAME": "COG3: Validita MISURA \"O2\"",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40028,
    "BITNO": 8,
    "BITNAME": "Bit 8",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40029,
    "BITNO": 9,
    "BITNAME": "Bit 9",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40029,
    "BITNO": 10,
    "BITNAME": "Bit 10",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40029,
    "BITNO": 11,
    "BITNAME": "Bit 11",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40029,
    "BITNO": 12,
    "BITNAME": "Bit 12",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40029,
    "BITNO": 13,
    "BITNAME": "Bit 13",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40029,
    "BITNO": 14,
    "BITNAME": "Bit 14",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40029,
    "BITNO": 15,
    "BITNAME": "Bit 15",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40029,
    "BITNO": 16,
    "BITNAME": "Bit 16",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40029,
    "BITNO": 1,
    "BITNAME": "Bit 1",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40029,
    "BITNO": 2,
    "BITNAME": "Bit 2",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40029,
    "BITNO": 3,
    "BITNAME": "Bit 3",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40029,
    "BITNO": 4,
    "BITNAME": "Bit 4",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40029,
    "BITNO": 5,
    "BITNAME": "Bit 5",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40029,
    "BITNO": 6,
    "BITNAME": "Bit 6",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40029,
    "BITNO": 7,
    "BITNAME": "Bit 7",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40029,
    "BITNO": 8,
    "BITNAME": "Bit 8",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40030,
    "BITNO": 0,
    "BITNAME": "Riserva STATI LOGICI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40031,
    "BITNO": 9,
    "BITNAME": "%I0.0 - Gen: ALLARME SITOP SELECT 24Vdc (0=ALL)",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40031,
    "BITNO": 10,
    "BITNAME": "%I0.1 - M1: SCATTO INTERRUTTORI (0=ALL)",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40031,
    "BITNO": 11,
    "BITNAME": "%I0.2 - M1: PULSANTE RESET",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40031,
    "BITNO": 12,
    "BITNAME": "%I0.3 - M1: SELETTORE MANUTENZIONE",
    "TEXTON": "Manutenzione",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40031,
    "BITNO": 13,
    "BITNAME": "%I0.4 - M1: SELETTORE INSERIMENTO POMPA PRELIEVO",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40031,
    "BITNO": 14,
    "BITNAME": "%I0.5 - M1: PULSANTE BYPASS NO2/NO",
    "TEXTON": "Bypass",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40031,
    "BITNO": 15,
    "BITNAME": "%I0.6 - M1: PSL BASSA PRESSIONE GAS DI MISURA (0=ALL)",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40031,
    "BITNO": 16,
    "BITNAME": "%I0.7 - M1: ALLARME TEMPERATURA SONDA DI PRELIEVO (0=ALL)",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40031,
    "BITNO": 1,
    "BITNAME": "%I1.0 - M1-M2: ALLARME FRIGO (0=ALL)",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40031,
    "BITNO": 2,
    "BITNAME": "%I1.1 - M1: PRESENZA CONDENSA (0=ALL)",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40031,
    "BITNO": 3,
    "BITNAME": "%I1.2 - M1: ALLARME CONVERTITORE NO2/NO (0=ALL)",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40031,
    "BITNO": 4,
    "BITNAME": "%I1.3 - M1: MOTORE In MARCIA",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40031,
    "BITNO": 5,
    "BITNAME": "%I1.4 -",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40031,
    "BITNO": 6,
    "BITNAME": "%I1.5 -",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40031,
    "BITNO": 7,
    "BITNAME": "%I1.6 -",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40031,
    "BITNO": 8,
    "BITNAME": "%I1.7 -",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40032,
    "BITNO": 9,
    "BITNAME": "%I2.0 - Gen: ALLARME ALTA TEMPERATURA QUADRO ANALISI (0=ALL)",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40032,
    "BITNO": 10,
    "BITNAME": "%I2.1 - M2: SCATTO INTERRUTTORI (0=ALL)",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40032,
    "BITNO": 11,
    "BITNAME": "%I2.2 - M2: PULSANTE RESET",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40032,
    "BITNO": 12,
    "BITNAME": "%I2.3 - M2: SELETTORE MANUTENZIONE",
    "TEXTON": "Manutenzione",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40032,
    "BITNO": 13,
    "BITNAME": "%I2.4 - M2: SELETTORE INSERIMENTO POMPA PRELIEVO",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40032,
    "BITNO": 14,
    "BITNAME": "%I2.5 - M2: PULSANTE BYPASS NO2/NO",
    "TEXTON": "Bypass",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40032,
    "BITNO": 15,
    "BITNAME": "%I2.6 - M2: PSL BASSA PRESSIONE GAS DI MISURA (0=ALL)",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40032,
    "BITNO": 16,
    "BITNAME": "%I2.7 - M2: ALLARME TEMPERATURA SONDA DI PRELIEVO (0=ALL)",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40032,
    "BITNO": 1,
    "BITNAME": "%I3.0 - Gen: SCATTO INTERRUTTORI (0=ALL)",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40032,
    "BITNO": 2,
    "BITNAME": "%I3.1 - M2: PRESENZA CONDENSA (0=ALL)",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40032,
    "BITNO": 3,
    "BITNAME": "%I3.2 - M2: ALLARME CONVERTITORE NO2/NO (0=ALL)",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40032,
    "BITNO": 4,
    "BITNAME": "%I3.3 - M2: MOTORE IN MARCIA",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40032,
    "BITNO": 5,
    "BITNAME": "%I3.4 -",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40032,
    "BITNO": 6,
    "BITNAME": "%I3.5 -",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40032,
    "BITNO": 7,
    "BITNAME": "%I3.6 -",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40032,
    "BITNO": 8,
    "BITNAME": "%I3.7 -",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40033,
    "BITNO": 9,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40033,
    "BITNO": 10,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40033,
    "BITNO": 11,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40033,
    "BITNO": 12,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40033,
    "BITNO": 13,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40033,
    "BITNO": 14,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40033,
    "BITNO": 15,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40033,
    "BITNO": 16,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40033,
    "BITNO": 1,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40033,
    "BITNO": 2,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40033,
    "BITNO": 3,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40033,
    "BITNO": 4,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40033,
    "BITNO": 5,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40033,
    "BITNO": 6,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40033,
    "BITNO": 7,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40033,
    "BITNO": 8,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40034,
    "BITNO": 9,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40034,
    "BITNO": 10,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40034,
    "BITNO": 11,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40034,
    "BITNO": 12,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40034,
    "BITNO": 13,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40034,
    "BITNO": 14,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40034,
    "BITNO": 15,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40034,
    "BITNO": 16,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40034,
    "BITNO": 1,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40034,
    "BITNO": 2,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40034,
    "BITNO": 3,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40034,
    "BITNO": 4,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40034,
    "BITNO": 5,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40034,
    "BITNO": 6,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40034,
    "BITNO": 7,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40034,
    "BITNO": 8,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40035,
    "BITNO": 9,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40035,
    "BITNO": 10,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40035,
    "BITNO": 11,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40035,
    "BITNO": 12,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40035,
    "BITNO": 13,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40035,
    "BITNO": 14,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40035,
    "BITNO": 15,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40035,
    "BITNO": 16,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40035,
    "BITNO": 1,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40035,
    "BITNO": 2,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40035,
    "BITNO": 3,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40035,
    "BITNO": 4,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40035,
    "BITNO": 5,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40035,
    "BITNO": 6,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40035,
    "BITNO": 7,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40035,
    "BITNO": 8,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40036,
    "BITNO": 9,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40036,
    "BITNO": 10,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40036,
    "BITNO": 11,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40036,
    "BITNO": 12,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40036,
    "BITNO": 13,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40036,
    "BITNO": 14,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40036,
    "BITNO": 15,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40036,
    "BITNO": 16,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40036,
    "BITNO": 1,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40036,
    "BITNO": 2,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40036,
    "BITNO": 3,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40036,
    "BITNO": 4,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40036,
    "BITNO": 5,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40036,
    "BITNO": 6,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40036,
    "BITNO": 7,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40036,
    "BITNO": 8,
    "BITNAME": "Riserva INPUT",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40037,
    "BITNO": 0,
    "BITNAME": "Riserva",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40038,
    "BITNO": 0,
    "BITNAME": "Riserva",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40039,
    "BITNO": 0,
    "BITNAME": "Riserva",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40040,
    "BITNO": 0,
    "BITNAME": "Riserva",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40041,
    "BITNO": 9,
    "BITNAME": "%Q0.0 - BL1: COM SSR RISCALDAMENTO LINEA PRELIEVO M1",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40041,
    "BITNO": 10,
    "BITNAME": "%Q0.1 - M1: COM. ELT YV1 (Mis_Cal)",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40041,
    "BITNO": 11,
    "BITNAME": "%Q0.2 - M1: COM. ELT YV3 (Zero-Span)",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40041,
    "BITNO": 12,
    "BITNAME": "%Q0.3 - M1: COM. CONVERTITORE (Bypass CONVERTITORE NO2/NO)",
    "TEXTON": "Bypass",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40041,
    "BITNO": 13,
    "BITNAME": "%Q0.4 - M1: COM. Sync ULTRAMAT 23 \"NO+CO+O2\"",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40041,
    "BITNO": 14,
    "BITNAME": "%Q0.5 - M1: COMANDO POMPA",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40041,
    "BITNO": 15,
    "BITNAME": "%Q0.6 - M1: LAMPADA OR ALLARMI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40041,
    "BITNO": 16,
    "BITNAME": "%Q0.7 - M1: LAMPADA SELETTORE POMPA",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40041,
    "BITNO": 1,
    "BITNAME": "%Q1.0 - M1: Ripetizione CUMULATIVO ALLARME (0=All)",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40041,
    "BITNO": 2,
    "BITNAME": "%Q1.1 - M1: Ripetizione IN MANUTENZIONE (1=Maint)",
    "TEXTON": "Manutenzione",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40041,
    "BITNO": 3,
    "BITNAME": "%Q1.2 - M1: Ripetizione 01 PREALLARME EMISSIONE \"CO\" (1=All)",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40041,
    "BITNO": 4,
    "BITNAME": "%Q1.3 - M1: Ripetizione 01 PREALLARME EMISSIONE \"NO\" (1=All)",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40041,
    "BITNO": 5,
    "BITNAME": "%Q1.4 - M1: Ripetizione 01 ALLARME SUPERAMENTO EMISSIONI (1=All)",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40041,
    "BITNO": 6,
    "BITNAME": "%Q1.5 - M1: Ripetizione 02 PREALLARME EMISSIONE \"CO\" (1=All)",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40041,
    "BITNO": 7,
    "BITNAME": "%Q1.6 - M1: Ripetizione 02 PREALLARME EMISSIONE \"NO\" (1=All)",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40041,
    "BITNO": 8,
    "BITNAME": "%Q1.7 - M1: Ripetizione 02 ALLARME SUPERAMENTO EMISSIONI (1=All)",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40042,
    "BITNO": 9,
    "BITNAME": "%Q2.0 - BL2: COM SSR RISCALDAMENTO LINEA PRELIEVO M2",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40042,
    "BITNO": 10,
    "BITNAME": "%Q2.1 - M2: COM. ELT YV2 (Mis_Cal)",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40042,
    "BITNO": 11,
    "BITNAME": "%Q2.2 - M2: COM. ELT YV4 (Zero-Span)",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40042,
    "BITNO": 12,
    "BITNAME": "%Q2.3 - M2: COM. CONVERTITORE (Bypass CONVERTITORE NO2/NO)",
    "TEXTON": "Bypass",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40042,
    "BITNO": 13,
    "BITNAME": "%Q2.4 - M2: COM. Sync ULTRAMAT 23 \"NO+CO+O2\"",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40042,
    "BITNO": 14,
    "BITNAME": "%Q2.5 - M2: COMANDO POMPA",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40042,
    "BITNO": 15,
    "BITNAME": "%Q2.6 - M2: LAMPADA OR ALLARMI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40042,
    "BITNO": 16,
    "BITNAME": "%Q2.7 - M2: LAMPADA SELETTORE POMPA",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40042,
    "BITNO": 1,
    "BITNAME": "%Q3.0 - M2: Ripetizione CUMULATIVO ALLARME (0=All)",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40042,
    "BITNO": 2,
    "BITNAME": "%Q3.1 - M2: Ripetizione IN MANUTENZIONE (1=Maint)",
    "TEXTON": "Manutenzione",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40042,
    "BITNO": 3,
    "BITNAME": "%Q3.2 - M2: Ripetizione 01 PREALLARME EMISSIONE \"CO\" (1=All)",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40042,
    "BITNO": 4,
    "BITNAME": "%Q3.3 - M2: Ripetizione 01 PREALLARME EMISSIONE \"NO\" (1=All)",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40042,
    "BITNO": 5,
    "BITNAME": "%Q3.4 - M2: Ripetizione 01 ALLARME SUPERAMENTO EMISSIONI (1=All)",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40042,
    "BITNO": 6,
    "BITNAME": "%Q3.5 - M2: Ripetizione 02 PREALLARME EMISSIONE \"CO\" (1=All)",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40042,
    "BITNO": 7,
    "BITNAME": "%Q3.6 - M2: Ripetizione 02 PREALLARME EMISSIONE \"NO\" (1=All)",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40042,
    "BITNO": 8,
    "BITNAME": "%Q3.7 - M2: Ripetizione 02 ALLARME SUPERAMENTO EMISSIONI (1=All)",
    "TEXTON": "Allarme",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40043,
    "BITNO": 9,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40043,
    "BITNO": 10,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40043,
    "BITNO": 11,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40043,
    "BITNO": 12,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40043,
    "BITNO": 13,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40043,
    "BITNO": 14,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40043,
    "BITNO": 15,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40043,
    "BITNO": 16,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40043,
    "BITNO": 1,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40043,
    "BITNO": 2,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40043,
    "BITNO": 3,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40043,
    "BITNO": 4,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40043,
    "BITNO": 5,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40043,
    "BITNO": 6,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40043,
    "BITNO": 7,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40043,
    "BITNO": 8,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40044,
    "BITNO": 9,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40044,
    "BITNO": 10,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40044,
    "BITNO": 11,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40044,
    "BITNO": 12,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40044,
    "BITNO": 13,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40044,
    "BITNO": 14,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40044,
    "BITNO": 15,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40044,
    "BITNO": 16,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40044,
    "BITNO": 1,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40044,
    "BITNO": 2,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40044,
    "BITNO": 3,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40044,
    "BITNO": 4,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40044,
    "BITNO": 5,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40044,
    "BITNO": 6,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40044,
    "BITNO": 7,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40044,
    "BITNO": 8,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40045,
    "BITNO": 9,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40045,
    "BITNO": 10,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40045,
    "BITNO": 11,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40045,
    "BITNO": 12,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40045,
    "BITNO": 13,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40045,
    "BITNO": 14,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40045,
    "BITNO": 15,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40045,
    "BITNO": 16,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40045,
    "BITNO": 1,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40045,
    "BITNO": 2,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40045,
    "BITNO": 3,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40045,
    "BITNO": 4,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40045,
    "BITNO": 5,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40045,
    "BITNO": 6,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40045,
    "BITNO": 7,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40045,
    "BITNO": 8,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40046,
    "BITNO": 9,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40046,
    "BITNO": 10,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40046,
    "BITNO": 11,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40046,
    "BITNO": 12,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40046,
    "BITNO": 13,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40046,
    "BITNO": 14,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40046,
    "BITNO": 15,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40046,
    "BITNO": 16,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40046,
    "BITNO": 1,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40046,
    "BITNO": 2,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40046,
    "BITNO": 3,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40046,
    "BITNO": 4,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40046,
    "BITNO": 5,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40046,
    "BITNO": 6,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40046,
    "BITNO": 7,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40046,
    "BITNO": 8,
    "BITNAME": "Riserva OUTPUT DIRETTI",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40047,
    "BITNO": 0,
    "BITNAME": "Riserva",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40048,
    "BITNO": 0,
    "BITNAME": "Riserva",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40049,
    "BITNO": 0,
    "BITNAME": "Riserva",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  },
  {
    "MEASUREID": 40050,
    "BITNO": 0,
    "BITNAME": "Riserva",
    "TEXTON": "Attivo",
    "TEXTOFF": "OFF"
  }
]"""



M5_STRING = r"""[
  {
    "RAW": "COMANDO ACK RESET (impulsivo)",
    "NAME": "Cmd ACK Reset",
    "UNITS": null
  },
  {
    "RAW": "COMANDO TACITAZIONE SIRENA (impulsivo)",
    "NAME": "Cmd Tacitazione Sirena",
    "UNITS": null
  },
  {
    "RAW": "COG2: COMANDO RESET ORE CARTUCCIA (impulsivo)",
    "NAME": "Cmd Reset Ore Cartuccia",
    "UNITS": null
  },
  {
    "RAW": "COG3: COMANDO RESET ORE CARTUCCIA (impulsivo)",
    "NAME": "Cmd Reset Ore Cartuccia",
    "UNITS": null
  },
  {
    "RAW": "COG2: COMANDO Autocal ULTRAMAT 23 \"NO+CO+O2\" (impulsivo)",
    "NAME": "Cmd Autocal ULTRAMAT 23 NO+CO+O2",
    "UNITS": null
  },
  {
    "RAW": "COG3: COMANDO Autocal ULTRAMAT 23 \"NO+CO+O2\" (impulsivo)",
    "NAME": "Cmd Autocal ULTRAMAT 23 NO+CO+O2",
    "UNITS": null
  },
  {
    "RAW": "COG2: COMANDO START VERIFICA QAL 3 CO+NO+O2 (impulsivo)",
    "NAME": "Cmd Start Verifica QAL 3 CO+NO+O2",
    "UNITS": null
  },
  {
    "RAW": "COG2: COMANDO STOP VERIFICA QAL 3 CO+NO+O2 (impulsivo)",
    "NAME": "Cmd Stop Verifica QAL 3 CO+NO+O2",
    "UNITS": null
  },
  {
    "RAW": "COG2: COMANDO SET BYPASS CONVERTITORE NO2-NO (impulsivo)",
    "NAME": "Cmd Set Bypass Conv. NO2-NO",
    "UNITS": null
  },
  {
    "RAW": "COG2: COMANDO RESET BYPASS CONVERTITORE NO2-NO (impulsivo)",
    "NAME": "Cmd Reset Bypass Conv. NO2-NO",
    "UNITS": null
  },
  {
    "RAW": "COG3: COMANDO START VERIFICA QAL 3 CO+NO+O2 (impulsivo)",
    "NAME": "Cmd Start Verifica QAL 3 CO+NO+O2",
    "UNITS": null
  },
  {
    "RAW": "COG3: COMANDO STOP VERIFICA QAL 3 CO+NO+O2 (impulsivo)",
    "NAME": "Cmd Stop Verifica QAL 3 CO+NO+O2",
    "UNITS": null
  },
  {
    "RAW": "COG3: COMANDO SET BYPASS CONVERTITORE NO2-NO (impulsivo)",
    "NAME": "Cmd Set Bypass Conv. NO2-NO",
    "UNITS": null
  },
  {
    "RAW": "COG3: COMANDO RESET BYPASS CONVERTITORE NO2-NO (impulsivo)",
    "NAME": "Cmd Reset Bypass Conv. NO2-NO",
    "UNITS": null
  },
  {
    "RAW": "SELEZIONE CALIBRAZ/VERIFICA ZERO PER \"CO\"",
    "NAME": "Sel Calib/Verif Zero CO",
    "UNITS": null
  },
  {
    "RAW": "SELEZIONE CALIBRAZ/VERIFICA ZERO PER \"NO\"",
    "NAME": "Sel Calib/Verif Zero NO",
    "UNITS": null
  },
  {
    "RAW": "SELEZIONE CALIBRAZ/VERIFICA ZERO PER \"O2\"",
    "NAME": "Sel Calib/Verif Zero O2",
    "UNITS": null
  },
  {
    "RAW": "SELEZIONE CALIBRAZ/VERIFICA SPAN PER \"CO\"",
    "NAME": "Sel Calib/Verif Span CO",
    "UNITS": null
  },
  {
    "RAW": "SELEZIONE CALIBRAZ/VERIFICA SPAN PER \"NO\"",
    "NAME": "Sel Calib/Verif Span NO",
    "UNITS": null
  },
  {
    "RAW": "SELEZIONE CALIBRAZ/VERIFICA SPAN PER \"O2\"",
    "NAME": "Sel Calib/Verif Span O2",
    "UNITS": null
  },
  {
    "RAW": "WATCH DOG COMUNICAZIONE PLC (se varia OK master+I/O ok)",
    "NAME": "Watch Dog Comm PLC",
    "UNITS": null
  },
  {
    "RAW": "WATCH_DOG_DA SME Server 01 (Valore che incrementa) (Write da PC-SME)",
    "NAME": "Watch Dog SME Server 01",
    "UNITS": null
  },
  {
    "RAW": "WATCH_DOG_DA SME Server 02 (Valore che incrementa) (Write da PC-SME) nu",
    "NAME": "Watch Dog SME Server 02",
    "UNITS": null
  },
  {
    "RAW": "FAULT COMUNICAZIONE PC SME",
    "NAME": "Fault Comm PC SME",
    "UNITS": null
  },
  {
    "RAW": "FAULT COMUNICAZIONE Con DCS",
    "NAME": "Fault Comm DCS",
    "UNITS": null
  },
  {
    "RAW": "ANALOG Output DCS Forzatl",
    "NAME": "Analog Output DCS Forzatl",
    "UNITS": null
  },
  {
    "RAW": "SELETTORE MANUTENZIONE GENERALE (OR M1+M2)",
    "NAME": "Sel Manut. Gen. (OR M1+M2)",
    "UNITS": null
  },
  {
    "RAW": "COG2: Fault analogica MISURA \"TEMPERATURA LINEA\" (BL1)",
    "NAME": "Fault Anal. Temp. Linea BL1",
    "UNITS": null
  },
  {
    "RAW": "COG2: Fault analogica MISURA \"PRESSIONE FUMI\"",
    "NAME": "Fault Anal. Pressione Fumi",
    "UNITS": null
  },
  {
    "RAW": "COG2: Fault analogica MISURA \"TEMPERATURA FUMI\"",
    "NAME": "Fault Anal. Temp. Fumi",
    "UNITS": null
  },
  {
    "RAW": "COG2: Fault analogica MISURA \"POTENZA_MOTORE\"",
    "NAME": "Fault Anal. Potenza Motore",
    "UNITS": null
  },
  {
    "RAW": "COG2: Fault analogica MISURA \"PORTATA GAS\"",
    "NAME": "Fault Anal. Portata Gas",
    "UNITS": null
  },
  {
    "RAW": "Fault analogica MISURA Ris_006",
    "NAME": "Fault Anal. Ris_006",
    "UNITS": null
  },
  {
    "RAW": "COG3: Fault analogica MISURA \"TEMPERATURA LINEA\" (BL2)",
    "NAME": "Fault Anal. Temp. Linea BL2",
    "UNITS": null
  },
  {
    "RAW": "COG3: Fault analogica MISURA \"PRESSIONE FUMI\"",
    "NAME": "Fault Anal. Pressione Fumi",
    "UNITS": null
  },
  {
    "RAW": "COG3: Fault analogica MISURA \"TEMPERATURA FUMI\"",
    "NAME": "Fault Anal. Temp. Fumi",
    "UNITS": null
  },
  {
    "RAW": "COG3: Fault analogica MISURA \"POTENZA_MOTORE\"",
    "NAME": "Fault Anal. Potenza Motore",
    "UNITS": null
  },
  {
    "RAW": "COG3: Fault analogica MISURA \"PORTATA GAS\"",
    "NAME": "Fault Anal. Portata Gas",
    "UNITS": null
  },
  {
    "RAW": "Fault analogica MISURA Ris_012",
    "NAME": "Fault Anal. Ris_012",
    "UNITS": null
  },
  {
    "RAW": "Gen: ALLARME SITOP SELECT 24Vdc",
    "NAME": "All. Sitop Select 24Vdc",
    "UNITS": null
  },
  {
    "RAW": "Gen: ALLARME ALTA TEMPERATURA QUADRO ANALISI",
    "NAME": "All. Alta Temp. Quadro Analisi",
    "UNITS": null
  },
  {
    "RAW": "Gen: SCATTO INTERRUTTORI",
    "NAME": "Scatto Interruttori",
    "UNITS": null
  },
  {
    "RAW": "COG2: ALLARME TEMPERATURA SONDA DI PRELIEVO",
    "NAME": "All. Temp. Sonda Prelievo",
    "UNITS": null
  },
  {
    "RAW": "COG2: ALLARME TEMPERATURA LINEA DI PRELIEVO BL1",
    "NAME": "All. Temp. Linea Prelievo BL1",
    "UNITS": null
  },
  {
    "RAW": "COG2: BLOCCO ALTISSIME TEMPERATURE In REGOLAZIONE BL1",
    "NAME": "Blocco Altissime Temp. Regol. BL1",
    "UNITS": null
  },
  {
    "RAW": "COG2: ALLARME FRIGO",
    "NAME": "All. Frigo",
    "UNITS": null
  },
  {
    "RAW": "COG2: ALLARME PRESENZA CONDENSA",
    "NAME": "All. Presenza Condensa",
    "UNITS": null
  },
  {
    "RAW": "COG2: MEMORIA PRESENZA CONDENSA (Da Resettare)",
    "NAME": "Memoria Presenza Condensa",
    "UNITS": null
  },
  {
    "RAW": "COG2: PSL BASSA PRESSIONE GAS DI MISURA",
    "NAME": "PSL Bassa Pressione Gas",
    "UNITS": null
  },
  {
    "RAW": "COG2: SELETTORE MANUTENZIONE",
    "NAME": "Sel Manut.",
    "UNITS": null
  },
  {
    "RAW": "COG2: SCATTO INTERRUTTORI",
    "NAME": "Scatto Interruttori",
    "UNITS": null
  },
  {
    "RAW": "COG2: ALLARME CONVERTITORE NO2/NO",
    "NAME": "All. Conv. NO2/NO",
    "UNITS": null
  },
  {
    "RAW": "COG2: ANOMALIA ANALIZZATORE U23 \"CO\"",
    "NAME": "Anomalia Anal. U23 CO",
    "UNITS": null
  },
  {
    "RAW": "COG2: ALLARME BAD_QUALITY MISURA \"CO\"",
    "NAME": "All. Bad Quality CO",
    "UNITS": null
  },
  {
    "RAW": "COG2: ANOMALIA ANALIZZATORE U23 \"NO\"",
    "NAME": "Anomalia Anal. U23 NO",
    "UNITS": null
  },
  {
    "RAW": "COG2: ALLARME BAD_QUALITY MISURA \"NO\"",
    "NAME": "All. Bad Quality NO",
    "UNITS": null
  },
  {
    "RAW": "COG2: ANOMALIA ANALIZZATORE U23 \"O2\"",
    "NAME": "Anomalia Anal. U23 O2",
    "UNITS": null
  },
  {
    "RAW": "COG2: ALLARME BAD_QUALITY MISURA \"O2\"",
    "NAME": "All. Bad Quality O2",
    "UNITS": null
  },
  {
    "RAW": "COG2: ALLARME COMUNICAZIONE ANALIZZATORE U23 \"CO-NO+O2\"",
    "NAME": "All. Comm. Anal. U23 CO-NO+O2",
    "UNITS": null
  },
  {
    "RAW": "COG2: ALLARME VERIFICA QAL3 \"CO+NO+O2\" Terminata CON ERRORI",
    "NAME": "All. Verifica QAL3 CO+NO+O2 Errori",
    "UNITS": null
  },
  {
    "RAW": "COG3: ALLARME TEMPERATURA SONDA DI PRELIEVO",
    "NAME": "All. Temp. Sonda Prelievo",
    "UNITS": null
  },
  {
    "RAW": "COG3: ALLARME TEMPERATURA LINEA DI PRELIEVO BL2",
    "NAME": "All. Temp. Linea Prelievo BL2",
    "UNITS": null
  },
  {
    "RAW": "COG3: BLOCCO ALTISSIME TEMPERATURE In REGOLAZIONE BL2",
    "NAME": "Blocco Altissime Temp. Regol. BL2",
    "UNITS": null
  },
  {
    "RAW": "COG3: ALLARME FRIGO",
    "NAME": "All. Frigo",
    "UNITS": null
  },
  {
    "RAW": "COG3: ALLARME PRESENZA CONDENSA",
    "NAME": "All. Presenza Condensa",
    "UNITS": null
  },
  {
    "RAW": "COG3: MEMORIA PRESENZA CONDENSA (Da Resettare)",
    "NAME": "Memoria Presenza Condensa",
    "UNITS": null
  },
  {
    "RAW": "COG3: PSL BASSA PRESSIONE GAS DI MISURA",
    "NAME": "PSL Bassa Pressione Gas",
    "UNITS": null
  },
  {
    "RAW": "COG3: SELETTORE MANUTENZIONE",
    "NAME": "Sel Manut.",
    "UNITS": null
  },
  {
    "RAW": "COG3: SCATTO INTERRUTTORI",
    "NAME": "Scatto Interruttori",
    "UNITS": null
  },
  {
    "RAW": "COG3: ALLARME CONVERTITORE NO2/NO",
    "NAME": "All. Conv. NO2/NO",
    "UNITS": null
  },
  {
    "RAW": "COG3: ANOMALIA ANALIZZATORE U23 \"CO\"",
    "NAME": "Anomalia Anal. U23 CO",
    "UNITS": null
  },
  {
    "RAW": "COG3: ALLARME BAD_QUALITY MISURA \"CO\"",
    "NAME": "All. Bad Quality CO",
    "UNITS": null
  },
  {
    "RAW": "COG3: ANOMALIA ANALIZZATORE U23 \"NO\"",
    "NAME": "Anomalia Anal. U23 NO",
    "UNITS": null
  },
  {
    "RAW": "COG3: ALLARME BAD_QUALITY MISURA \"NO\"",
    "NAME": "All. Bad Quality NO",
    "UNITS": null
  },
  {
    "RAW": "COG3: ANOMALIA ANALIZZATORE U23 \"O2\"",
    "NAME": "Anomalia Anal. U23 O2",
    "UNITS": null
  },
  {
    "RAW": "COG3: ALLARME BAD_QUALITY MISURA \"O2\"",
    "NAME": "All. Bad Quality O2",
    "UNITS": null
  },
  {
    "RAW": "COG3: ALLARME COMUNICAZIONE ANALIZZATORE U23 \"CO-NO+O2\"",
    "NAME": "All. Comm. Anal. U23 CO-NO+O2",
    "UNITS": null
  },
  {
    "RAW": "COG3: ALLARME VERIFICA QAL3 \"CO+NO+O2\" Terminata CON ERRORI",
    "NAME": "All. Verifica QAL3 CO+NO+O2 Errori",
    "UNITS": null
  },
  {
    "RAW": "ABILIT.MEMORIZZAZIONE DATA In TO MMC (EXT + TIME INTERLOCK) (Only HMI)",
    "NAME": "Abil. Mem. Data TO MMC",
    "UNITS": null
  },
  {
    "RAW": "MEMORIZZAZIONE DATA MMC OK (Only HMI)",
    "NAME": "Mem. Data MMC OK",
    "UNITS": null
  },
  {
    "RAW": "MEMORIZZAZIONE DATA MMC ERRORE (Only HMI)",
    "NAME": "Mem. Data MMC Errore",
    "UNITS": null
  },
  {
    "RAW": "MEMORIZZAZIONE IN CORSO (Only HMI)",
    "NAME": "Mem. In Corso",
    "UNITS": null
  },
  {
    "RAW": "COG2: OR ALLARMI",
    "NAME": "OR All. COG2",
    "UNITS": null
  },
  {
    "RAW": "COG3: OR ALLARMI",
    "NAME": "OR All. COG3",
    "UNITS": null
  },
  {
    "RAW": "Gen: OR ALLARMI (M1+M2)",
    "NAME": "OR All. (M1+M2)",
    "UNITS": null
  },
  {
    "RAW": "Gen: PULSANTE DI RESET (M1+M2)",
    "NAME": "Pulsante Reset (M1+M2)",
    "UNITS": null
  },
  {
    "RAW": "COG2: IN MISURA ANALIZZATORE.U23 \"CO\"",
    "NAME": "In Misura Anal. U23 CO",
    "UNITS": null
  },
  {
    "RAW": "COG2: IN CALIBRAZIONE ANALIZZATORE U23. \"CO\"",
    "NAME": "In Calib. Anal. U23 CO",
    "UNITS": null
  },
  {
    "RAW": "COG2: SPAN GAS ANALIZZATORE U23.\"CO\"",
    "NAME": "Span Gas Anal. U23 CO",
    "UNITS": null
  },
  {
    "RAW": "COG2: ZERO GAS ANALIZZATORE U23 \"CO\"",
    "NAME": "Zero Gas Anal. U23 CO",
    "UNITS": null
  },
  {
    "RAW": "COG2: IN MISURA ANALIZZATORE.U23 \"NO\"",
    "NAME": "In Misura Anal. U23 NO",
    "UNITS": null
  },
  {
    "RAW": "COG2: IN CALIBRAZIONE ANALIZZATORE U23. \"NO\"",
    "NAME": "In Calib. Anal. U23 NO",
    "UNITS": null
  },
  {
    "RAW": "COG2: SPAN GAS ANALIZZATORE U23.\"NO\"",
    "NAME": "Span Gas Anal. U23 NO",
    "UNITS": null
  },
  {
    "RAW": "COG2: ZERO GAS ANALIZZATORE U23 \"NO\"",
    "NAME": "Zero Gas Anal. U23 NO",
    "UNITS": null
  },
  {
    "RAW": "COG2: IN MISURA ANALIZZATORE.U23 \"O2\"",
    "NAME": "In Misura Anal. U23 O2",
    "UNITS": null
  },
  {
    "RAW": "COG2: IN CALIBRAZIONE ANALIZZATORE U23. \"O2\"",
    "NAME": "In Calib. Anal. U23 O2",
    "UNITS": null
  },
  {
    "RAW": "COG2: SPAN GAS ANALIZZATORE U23.\"O2\"",
    "NAME": "Span Gas Anal. U23 O2",
    "UNITS": null
  },
  {
    "RAW": "COG2: ZERO GAS ANALIZZATORE U23 \"O2\"",
    "NAME": "Zero Gas Anal. U23 O2",
    "UNITS": null
  },
  {
    "RAW": "COG2: AUTOCAL U 23 \"NO+CO+O2\" IN CORSO",
    "NAME": "Autocal U23 NO+CO+O2 In Corso",
    "UNITS": null
  },
  {
    "RAW": "COG2: SELETTORE INSERIMENTO POMPA P1",
    "NAME": "Sel Inser. Pompa P1",
    "UNITS": null
  },
  {
    "RAW": "COG2: STATO COMANDO POMPA P1",
    "NAME": "Stato Comando Pompa P1",
    "UNITS": null
  },
  {
    "RAW": "COG2: COM. ELT YV1 (Mis_Cal)",
    "NAME": "Com. ELT YV1 (Mis_Cal)",
    "UNITS": null
  },
  {
    "RAW": "COG2: COM. ELT YV3 (Zero-SpanI)",
    "NAME": "Com. ELT YV3 (Zero-SpanI)",
    "UNITS": null
  },
  {
    "RAW": "COG2: COM. CONVERTITORE (Bypass CONVERTITORE NO2/NO)",
    "NAME": "Com. Conv. (Bypass NO2/NO)",
    "UNITS": null
  },
  {
    "RAW": "COG2: MOTORE IN MARCIA",
    "NAME": "Motore In Marcia",
    "UNITS": null
  },
  {
    "RAW": "COG2: STATO VERIFICA QAL3 \"CO+NO+O2\" IN CORSO",
    "NAME": "Stato Verifica QAL3 CO+NO+O2 In Corso",
    "UNITS": null
  },
  {
    "RAW": "COG2: STATO VERIFICA QAL3 \"CO+NO+O2\" TERMINATA SENZA ERRORI",
    "NAME": "Stato Verifica QAL3 CO+NO+O2 Term. Senza Errori",
    "UNITS": null
  },
  {
    "RAW": "COG2: MOTORE IN MANUTENZIONE",
    "NAME": "Motore In Manut.",
    "UNITS": null
  },
  {
    "RAW": "COG2: PREALLARME EMISSIONE \"CO\"",
    "NAME": "Preall. Emissione CO",
    "UNITS": null
  },
  {
    "RAW": "COG2: PREALLARME EMISSIONE \"NO\"",
    "NAME": "Preall. Emissione NO",
    "UNITS": null
  },
  {
    "RAW": "COG2: ALLARME SUPERAMENTO EMISSIONI",
    "NAME": "All. Superamento Emissioni",
    "UNITS": null
  },
  {
    "RAW": "COG3: IN MISURA ANALIZZATORE.U23 \"CO\"",
    "NAME": "In Misura Anal. U23 CO",
    "UNITS": null
  },
  {
    "RAW": "COG3: IN CALIBRAZIONE ANALIZZATORE U23. \"CO\"",
    "NAME": "In Calib. Anal. U23 CO",
    "UNITS": null
  },
  {
    "RAW": "COG3: SPAN GAS ANALIZZATORE U23.\"CO\"",
    "NAME": "Span Gas Anal. U23 CO",
    "UNITS": null
  },
  {
    "RAW": "COG3: ZERO GAS ANALIZZATORE U23 \"CO\"",
    "NAME": "Zero Gas Anal. U23 CO",
    "UNITS": null
  },
  {
    "RAW": "COG3: IN MISURA ANALIZZATORE.U23 \"NO\"",
    "NAME": "In Misura Anal. U23 NO",
    "UNITS": null
  },
  {
    "RAW": "COG3: IN CALIBRAZIONE ANALIZZATORE U23. \"NO\"",
    "NAME": "In Calib. Anal. U23 NO",
    "UNITS": null
  },
  {
    "RAW": "COG3: SPAN GAS ANALIZZATORE U23.\"NO\"",
    "NAME": "Span Gas Anal. U23 NO",
    "UNITS": null
  },
  {
    "RAW": "COG3: ZERO GAS ANALIZZATORE U23 \"NO\"",
    "NAME": "Zero Gas Anal. U23 NO",
    "UNITS": null
  },
  {
    "RAW": "COG3: IN MISURA ANALIZZATORE.U23 \"O2\"",
    "NAME": "In Misura Anal. U23 O2",
    "UNITS": null
  },
  {
    "RAW": "COG3: IN CALIBRAZIONE ANALIZZATORE U23. \"O2\"",
    "NAME": "In Calib. Anal. U23 O2",
    "UNITS": null
  },
  {
    "RAW": "COG3: SPAN GAS ANALIZZATORE U23.\"O2\"",
    "NAME": "Span Gas Anal. U23 O2",
    "UNITS": null
  },
  {
    "RAW": "COG3: ZERO GAS ANALIZZATORE U23 \"O2\"",
    "NAME": "Zero Gas Anal. U23 O2",
    "UNITS": null
  },
  {
    "RAW": "COG3: AUTOCAL U 23 \"NO\" IN CORSO",
    "NAME": "Autocal U23 NO In Corso",
    "UNITS": null
  },
  {
    "RAW": "COG3: SELETTORE INSERIMENTO POMPA P1",
    "NAME": "Sel Inser. Pompa P1",
    "UNITS": null
  },
  {
    "RAW": "COG3: STATO COMANDO POMPA P1",
    "NAME": "Stato Comando Pompa P1",
    "UNITS": null
  },
  {
    "RAW": "COG3: COM. ELT YV2 (Mis_Cal)",
    "NAME": "Com. ELT YV2 (Mis_Cal)",
    "UNITS": null
  },
  {
    "RAW": "COG3: COM. ELT YV4 (Zero-SpanI)",
    "NAME": "Com. ELT YV4 (Zero-SpanI)",
    "UNITS": null
  },
  {
    "RAW": "COG3: COM. CONVERTITORE(Bypass CONVERTITORE NO2/NO)",
    "NAME": "Com. Conv. (Bypass NO2/NO)",
    "UNITS": null
  },
  {
    "RAW": "COG3:MOTORE IN MARCIA",
    "NAME": "Motore In Marcia",
    "UNITS": null
  },
  {
    "RAW": "COG3: STATO VERIFICA QAL3 \"CO+NO+O2\" IN CORSO",
    "NAME": "Stato Verifica QAL3 CO+NO+O2 In Corso",
    "UNITS": null
  },
  {
    "RAW": "COG3: STATO VERIFICA QAL3 \"CO+NO+O2\" TERMINATA SENZA ERRORI",
    "NAME": "Stato Verifica QAL3 CO+NO+O2 Term. Senza Errori",
    "UNITS": null
  },
  {
    "RAW": "COG3: MOTORE IN MANUTENZIONE",
    "NAME": "Motore In Manut.",
    "UNITS": null
  },
  {
    "RAW": "COG3: PREALLARME EMISSIONE \"CO\"",
    "NAME": "Preall. Emissione CO",
    "UNITS": null
  },
  {
    "RAW": "COG3: PREALLARME EMISSIONE \"NO\"",
    "NAME": "Preall. Emissione NO",
    "UNITS": null
  },
  {
    "RAW": "COG3: ALLARME SUPERAMENTO EMISSIONI",
    "NAME": "All. Superamento Emissioni",
    "UNITS": null
  },
  {
    "RAW": "COG2: Validita MISURA \"PRESSIONE FUMI\"",
    "NAME": "Validita Pressione Fumi",
    "UNITS": null
  },
  {
    "RAW": "COG2: Validita MISURA \"TEMPERATURA FUMI\"",
    "NAME": "Validita Temp. Fumi",
    "UNITS": null
  },
  {
    "RAW": "COG2: Validita MISURA \"POTENZA_COG\"",
    "NAME": "Validita Potenza Cog",
    "UNITS": null
  },
  {
    "RAW": "COG2: Validita MISURA \"PORTATA GAS I\"",
    "NAME": "Validita Portata Gas I",
    "UNITS": null
  },
  {
    "RAW": "COG2: Validita MISURA \"CO\"",
    "NAME": "Validita CO",
    "UNITS": null
  },
  {
    "RAW": "COG2: Validita MISURA \"NO\"",
    "NAME": "Validita NO",
    "UNITS": null
  },
  {
    "RAW": "COG2: Validita MISURA \"O2\"",
    "NAME": "Validita O2",
    "UNITS": null
  },
  {
    "RAW": "COG3: Validita MISURA \"PRESSIONE FUMI\"",
    "NAME": "Validita Pressione Fumi",
    "UNITS": null
  },
  {
    "RAW": "COG3: Validita MISURA \"TEMPERATURA FUMI\"",
    "NAME": "Validita Temp. Fumi",
    "UNITS": null
  },
  {
    "RAW": "COG3: Validita MISURA \"POTENZA_COG\"",
    "NAME": "Validita Potenza Cog",
    "UNITS": null
  },
  {
    "RAW": "COG3: Validita MISURA \"PORTATA GAS I\"",
    "NAME": "Validita Portata Gas I",
    "UNITS": null
  },
  {
    "RAW": "COG3: Validita MISURA \"CO\"",
    "NAME": "Validita CO",
    "UNITS": null
  },
  {
    "RAW": "COG3: Validita MISURA \"NO\"",
    "NAME": "Validita NO",
    "UNITS": null
  },
  {
    "RAW": "COG3: Validita MISURA \"O2\"",
    "NAME": "Validita O2",
    "UNITS": null
  },
  {
    "RAW": "%I0.0 - Gen: ALLARME SITOP SELECT 24Vdc (0=ALL)",
    "NAME": "I0.0 All. Sitop Select 24Vdc",
    "UNITS": null
  },
  {
    "RAW": "%I0.1 - M1: SCATTO INTERRUTTORI (0=ALL)",
    "NAME": "I0.1 Scatto Interruttori M1",
    "UNITS": null
  },
  {
    "RAW": "%I0.2 - M1: PULSANTE RESET",
    "NAME": "I0.2 Pulsante Reset M1",
    "UNITS": null
  },
  {
    "RAW": "%I0.3 - M1: SELETTORE MANUTENZIONE",
    "NAME": "I0.3 Sel Manut. M1",
    "UNITS": null
  },
  {
    "RAW": "%I0.4 - M1: SELETTORE INSERIMENTO POMPA PRELIEVO",
    "NAME": "I0.4 Sel Inser. Pompa Prelievo M1",
    "UNITS": null
  },
  {
    "RAW": "%I0.5 - M1: PULSANTE BYPASS NO2/NO",
    "NAME": "I0.5 Pulsante Bypass NO2/NO M1",
    "UNITS": null
  },
  {
    "RAW": "%I0.6 - M1: PSL BASSA PRESSIONE GAS DI MISURA (0=ALL)",
    "NAME": "I0.6 PSL Bassa Pressione Gas M1",
    "UNITS": null
  },
  {
    "RAW": "%I0.7 - M1: ALLARME TEMPERATURA SONDA DI PRELIEVO (0=ALL)",
    "NAME": "I0.7 All. Temp. Sonda Prelievo M1",
    "UNITS": null
  },
  {
    "RAW": "%I1.0 - M1-M2: ALLARME FRIGO (0=ALL)",
    "NAME": "I1.0 All. Frigo M1-M2",
    "UNITS": null
  },
  {
    "RAW": "%I1.1 - M1: PRESENZA CONDENSA (0=ALL)",
    "NAME": "I1.1 Presenza Condensa M1",
    "UNITS": null
  },
  {
    "RAW": "%I1.2 - M1: ALLARME CONVERTITORE NO2/NO (0=ALL)",
    "NAME": "I1.2 All. Conv. NO2/NO M1",
    "UNITS": null
  },
  {
    "RAW": "%I1.3 - M1: MOTORE In MARCIA",
    "NAME": "I1.3 Motore In Marcia M1",
    "UNITS": null
  },
  {
    "RAW": "%I2.0 - Gen: ALLARME ALTA TEMPERATURA QUADRO ANALISI (0=ALL)",
    "NAME": "I2.0 All. Alta Temp. Quadro Analisi",
    "UNITS": null
  },
  {
    "RAW": "%I2.1 - M2: SCATTO INTERRUTTORI (0=ALL)",
    "NAME": "I2.1 Scatto Interruttori M2",
    "UNITS": null
  },
  {
    "RAW": "%I2.2 - M2: PULSANTE RESET",
    "NAME": "I2.2 Pulsante Reset M2",
    "UNITS": null
  },
  {
    "RAW": "%I2.3 - M2: SELETTORE MANUTENZIONE",
    "NAME": "I2.3 Sel Manut. M2",
    "UNITS": null
  },
  {
    "RAW": "%I2.4 - M2: SELETTORE INSERIMENTO POMPA PRELIEVO",
    "NAME": "I2.4 Sel Inser. Pompa Prelievo M2",
    "UNITS": null
  },
  {
    "RAW": "%I2.5 - M2: PULSANTE BYPASS NO2/NO",
    "NAME": "I2.5 Pulsante Bypass NO2/NO M2",
    "UNITS": null
  },
  {
    "RAW": "%I2.6 - M2: PSL BASSA PRESSIONE GAS DI MISURA (0=ALL)",
    "NAME": "I2.6 PSL Bassa Pressione Gas M2",
    "UNITS": null
  },
  {
    "RAW": "%I2.7 - M2: ALLARME TEMPERATURA SONDA DI PRELIEVO (0=ALL)",
    "NAME": "I2.7 All. Temp. Sonda Prelievo M2",
    "UNITS": null
  },
  {
    "RAW": "%I3.0 - Gen: SCATTO INTERRUTTORI (0=ALL)",
    "NAME": "I3.0 Scatto Interruttori",
    "UNITS": null
  },
  {
    "RAW": "%I3.1 - M2: PRESENZA CONDENSA (0=ALL)",
    "NAME": "I3.1 Presenza Condensa M2",
    "UNITS": null
  },
  {
    "RAW": "%I3.2 - M2: ALLARME CONVERTITORE NO2/NO (0=ALL)",
    "NAME": "I3.2 All. Conv. NO2/NO M2",
    "UNITS": null
  },
  {
    "RAW": "%I3.3 - M2: MOTORE IN MARCIA",
    "NAME": "I3.3 Motore In Marcia M2",
    "UNITS": null
  },
  {
    "RAW": "Riserva INPUT",
    "NAME": null,
    "UNITS": null
  },
  {
    "RAW": "%Q0.0 - BL1: COM SSR RISCALDAMENTO LINEA PRELIEVO M1",
    "NAME": "Q0.0 Com. SSR Riscald. Linea Prelievo M1",
    "UNITS": null
  },
  {
    "RAW": "%Q0.1 - M1: COM. ELT YV1 (Mis_Cal)",
    "NAME": "Q0.1 Com. ELT YV1 (Mis_Cal)",
    "UNITS": null
  },
  {
    "RAW": "%Q0.2 - M1: COM. ELT YV3 (Zero-Span)",
    "NAME": "Q0.2 Com. ELT YV3 (Zero-Span)",
    "UNITS": null
  },
  {
    "RAW": "%Q0.3 - M1: COM. CONVERTITORE (Bypass CONVERTITORE NO2/NO)",
    "NAME": "Q0.3 Com. Conv. (Bypass NO2/NO)",
    "UNITS": null
  },
  {
    "RAW": "%Q0.4 - M1: COM. Sync ULTRAMAT 23 \"NO+CO+O2\"",
    "NAME": "Q0.4 Com. Sync ULTRAMAT 23 NO+CO+O2",
    "UNITS": null
  },
  {
    "RAW": "%Q0.5 - M1: COMANDO POMPA",
    "NAME": "Q0.5 Comando Pompa",
    "UNITS": null
  },
  {
    "RAW": "%Q0.6 - M1: LAMPADA OR ALLARMI",
    "NAME": "Q0.6 Lampada OR All.",
    "UNITS": null
  },
  {
    "RAW": "%Q0.7 - M1: LAMPADA SELETTORE POMPA",
    "NAME": "Q0.7 Lampada Sel. Pompa",
    "UNITS": null
  },
  {
    "RAW": "%Q1.0 - M1: Ripetizione CUMULATIVO ALLARME (0=All)",
    "NAME": "Q1.0 Ripet. Cumulativo All.",
    "UNITS": null
  },
  {
    "RAW": "%Q1.1 - M1: Ripetizione IN MANUTENZIONE (1=Maint)",
    "NAME": "Q1.1 Ripet. In Manut. (1=Maint)",
    "UNITS": null
  },
  {
    "RAW": "%Q1.2 - M1: Ripetizione 01 PREALLARME EMISSIONE \"CO\" (1=All)",
    "NAME": "Q1.2 Ripet. 01 Preall. Emissione CO (1=All)",
    "UNITS": null
  },
  {
    "RAW": "%Q1.3 - M1: Ripetizione 01 PREALLARME EMISSIONE \"NO\" (1=All)",
    "NAME": "Q1.3 Ripet. 01 Preall. Emissione NO (1=All)",
    "UNITS": null
  },
  {
    "RAW": "%Q1.4 - M1: Ripetizione 01 ALLARME SUPERAMENTO EMISSIONI (1=All)",
    "NAME": "Q1.4 Ripet. 01 All. Superamento Emissioni (1=All)",
    "UNITS": null
  },
  {
    "RAW": "%Q1.5 - M1: Ripetizione 02 PREALLARME EMISSIONE \"CO\" (1=All)",
    "NAME": "Q1.5 Ripet. 02 Preall. Emissione CO (1=All)",
    "UNITS": null
  },
  {
    "RAW": "%Q1.6 - M1: Ripetizione 02 PREALLARME EMISSIONE \"NO\" (1=All)",
    "NAME": "Q1.6 Ripet. 02 Preall. Emissione NO (1=All)",
    "UNITS": null
  },
  {
    "RAW": "%Q1.7 - M1: Ripetizione 02 ALLARME SUPERAMENTO EMISSIONI (1=All)",
    "NAME": "Q1.7 Ripet. 02 All. Superamento Emissioni (1=All)",
    "UNITS": null
  },
  {
    "RAW": "%Q2.0 - BL2: COM SSR RISCALDAMENTO LINEA PRELIEVO M2",
    "NAME": "Q2.0 Com. SSR Riscald. Linea Prelievo M2",
    "UNITS": null
  },
  {
    "RAW": "%Q2.1 - M2: COM. ELT YV2 (Mis_Cal)",
    "NAME": "Q2.1 Com. ELT YV2 (Mis_Cal)",
    "UNITS": null
  },
  {
    "RAW": "%Q2.2 - M2: COM. ELT YV4 (Zero-Span)",
    "NAME": "Q2.2 Com. ELT YV4 (Zero-Span)",
    "UNITS": null
  },
  {
    "RAW": "%Q2.3 - M2: COM. CONVERTITORE (Bypass CONVERTITORE NO2/NO)",
    "NAME": "Q2.3 Com. Conv. (Bypass NO2/NO)",
    "UNITS": null
  },
  {
    "RAW": "%Q2.4 - M2: COM. Sync ULTRAMAT 23 \"NO+CO+O2\"",
    "NAME": "Q2.4 Com. Sync ULTRAMAT 23 NO+CO+O2",
    "UNITS": null
  },
  {
    "RAW": "%Q2.5 - M2: COMANDO POMPA",
    "NAME": "Q2.5 Comando Pompa",
    "UNITS": null
  },
  {
    "RAW": "%Q2.6 - M2: LAMPADA OR ALLARMI",
    "NAME": "Q2.6 Lampada OR All.",
    "UNITS": null
  },
  {
    "RAW": "%Q2.7 - M2: LAMPADA SELETTORE POMPA",
    "NAME": "Q2.7 Lampada Sel. Pompa",
    "UNITS": null
  },
  {
    "RAW": "%Q3.0 - M2: Ripetizione CUMULATIVO ALLARME (0=All)",
    "NAME": "Q3.0 Ripet. Cumulativo All.",
    "UNITS": null
  },
  {
    "RAW": "%Q3.1 - M2: Ripetizione IN MANUTENZIONE (1=Maint)",
    "NAME": "Q3.1 Ripet. In Manut. (1=Maint)",
    "UNITS": null
  },
  {
    "RAW": "%Q3.2 - M2: Ripetizione 01 PREALLARME EMISSIONE \"CO\" (1=All)",
    "NAME": "Q3.2 Ripet. 01 Preall. Emissione CO (1=All)",
    "UNITS": null
  },
  {
    "RAW": "%Q3.3 - M2: Ripetizione 01 PREALLARME EMISSIONE \"NO\" (1=All)",
    "NAME": "Q3.3 Ripet. 01 Preall. Emissione NO (1=All)",
    "UNITS": null
  },
  {
    "RAW": "%Q3.4 - M2: Ripetizione 01 ALLARME SUPERAMENTO EMISSIONI (1=All)",
    "NAME": "Q3.4 Ripet. 01 All. Superamento Emissioni (1=All)",
    "UNITS": null
  },
  {
    "RAW": "%Q3.5 - M2: Ripetizione 02 PREALLARME EMISSIONE \"CO\" (1=All)",
    "NAME": "Q3.5 Ripet. 02 Preall. Emissione CO (1=All)",
    "UNITS": null
  },
  {
    "RAW": "%Q3.6 - M2: Ripetizione 02 PREALLARME EMISSIONE \"NO\" (1=All)",
    "NAME": "Q3.6 Ripet. 02 Preall. Emissione NO (1=All)",
    "UNITS": null
  },
  {
    "RAW": "%Q3.7 - M2: Ripetizione 02 ALLARME SUPERAMENTO EMISSIONI (1=All)",
    "NAME": "Q3.7 Ripet. 02 All. Superamento Emissioni (1=All)",
    "UNITS": null
  },
  {
    "RAW": "Riserva OUTPUT DIRETTI",
    "NAME": null,
    "UNITS": null
  },
  {
    "RAW": "COG2: MISURA TEMPERATURA LINEA PRELIEVO (BL1)",
    "NAME": "Misura Temp. Linea Prelievo BL1",
    "UNITS": null
  },
  {
    "RAW": "COG2: MISURA PRESSIONE FUMI",
    "NAME": "Misura Pressione Fumi",
    "UNITS": null
  },
  {
    "RAW": "COG2: MISURA TEMPERATURA FUMI",
    "NAME": "Misura Temp. Fumi",
    "UNITS": null
  },
  {
    "RAW": "COG2: MISURA POTENZA COGENERATORE",
    "NAME": "Misura Potenza Cogeneratore",
    "UNITS": null
  },
  {
    "RAW": "COG2: MISURA PORTATA GAS",
    "NAME": "Misura Portata Gas",
    "UNITS": null
  },
  {
    "RAW": "COG3: MISURA TEMPERATURA LINEA PRELIEVO (BL2)",
    "NAME": "Misura Temp. Linea Prelievo BL2",
    "UNITS": null
  },
  {
    "RAW": "COG3: MISURA PRESSIONE FUMI",
    "NAME": "Misura Pressione Fumi",
    "UNITS": null
  },
  {
    "RAW": "COG3: MISURA TEMPERATURA FUMI",
    "NAME": "Misura Temp. Fumi",
    "UNITS": null
  },
  {
    "RAW": "COG3: MISURA POTENZA COGENERATORE",
    "NAME": "Misura Potenza Cogeneratore",
    "UNITS": null
  },
  {
    "RAW": "COG3: MISURA PORTATA GAS",
    "NAME": "Misura Portata Gas",
    "UNITS": null
  },
  {
    "RAW": "COG2: MISURA ANALIZZATORE \"CO\" (mg/m3)",
    "NAME": "Misura Anal. CO (mg/m3)",
    "UNITS": "mg/m3"
  },
  {
    "RAW": "COG2: MISURA ANALIZZATORE \"NO\" (mg/m3)",
    "NAME": "Misura Anal. NO (mg/m3)",
    "UNITS": "mg/m3"
  },
  {
    "RAW": "COG2: MISURA ANALIZZATORE \"O2\" (%)",
    "NAME": "Misura Anal. O2 (%)",
    "UNITS": "%"
  },
  {
    "RAW": "COG3: MISURA ANALIZZATORE \"CO\" (mg/m3)",
    "NAME": "Misura Anal. CO (mg/m3)",
    "UNITS": "mg/m3"
  },
  {
    "RAW": "COG3: MISURA ANALIZZATORE \"NO\" (mg/m3)",
    "NAME": "Misura Anal. NO (mg/m3)",
    "UNITS": "mg/m3"
  },
  {
    "RAW": "COG3: MISURA ANALIZZATORE \"O2\" (%)",
    "NAME": "Misura Anal. O2 (%)",
    "UNITS": "%"
  },
  {
    "RAW": "COG2: CONTAORE FUNZIONAMENTO POMPA",
    "NAME": "Contaore Funz. Pompa",
    "UNITS": null
  },
  {
    "RAW": "COG3: CONTAORE FUNZIONAMENTO POMPA",
    "NAME": "Contaore Funz. Pompa",
    "UNITS": null
  },
  {
    "RAW": "COG2: CONTAORE FUNZIONAMENTO CARTUCCIA NO2/NO",
    "NAME": "Contaore Funz. Cartuccia NO2/NO",
    "UNITS": null
  },
  {
    "RAW": "COG3: CONTAORE FUNZIONAMENTO CARTUCCIA NO2/NO",
    "NAME": "Contaore Funz. Cartuccia NO2/NO",
    "UNITS": null
  },
  {
    "RAW": "COG2: PROGRESSIVO DATI CALIBRAZIONE COMPLETAM. OK CALx C1 (Variaz = read Data a PC)",
    "NAME": "Prog. Dati Calib. OK CALx C1",
    "UNITS": null
  },
  {
    "RAW": "COG2: MISURA ULTIMA CALx \"CO\" ZERO (Calibrazione Strumentale) N.U.",
    "NAME": "Misura Ultima Calx CO Zero",
    "UNITS": null
  },
  {
    "RAW": "COG2: MISURA ULTIMA CALx \"CO\" SPAN (Calibrazione Strumentale) N.U.",
    "NAME": "Misura Ultima Calx CO Span",
    "UNITS": null
  },
  {
    "RAW": "COG2: MISURA ULTIMA CALx \"NO\" ZERO (Calibrazione Strumentale) N.U.",
    "NAME": "Misura Ultima Calx NO Zero",
    "UNITS": null
  },
  {
    "RAW": "COG2: MISURA ULTIMA CALx \"NO\" SPAN (Calibrazione Strumentale) N.U.",
    "NAME": "Misura Ultima Calx NO Span",
    "UNITS": null
  },
  {
    "RAW": "COG2: MISURA ULTIMA CALx \"O2\" ZERO (Calibrazione Strumentale) N.U.",
    "NAME": "Misura Ultima Calx O2 Zero",
    "UNITS": null
  },
  {
    "RAW": "COG2: MISURA ULTIMA CALx \"O2\" SPAN (Calibrazione Strumentale) N.U.",
    "NAME": "Misura Ultima Calx O2 Span",
    "UNITS": null
  },
  {
    "RAW": "COG3: PROGRESSIVO DATI CALIBRAZIONE COMPLETAM. OK CALx C2 (Variaz = read Data a PC)",
    "NAME": "Prog. Dati Calib. OK CALx C2",
    "UNITS": null
  },
  {
    "RAW": "COG3: MISURA ULTIMA CALx \"CO\" ZERO (Calibrazione Strumentale) N.U.",
    "NAME": "Misura Ultima Calx CO Zero",
    "UNITS": null
  },
  {
    "RAW": "COG3: MISURA ULTIMA CALx \"CO\" SPAN (Calibrazione Strumentale) N.U.",
    "NAME": "Misura Ultima Calx CO Span",
    "UNITS": null
  },
  {
    "RAW": "COG3: MISURA ULTIMA CALx \"NO\" ZERO (Calibrazione Strumentale) N.U.",
    "NAME": "Misura Ultima Calx NO Zero",
    "UNITS": null
  },
  {
    "RAW": "COG3: MISURA ULTIMA CALx \"NO\" SPAN (Calibrazione Strumentale) N.U.",
    "NAME": "Misura Ultima Calx NO Span",
    "UNITS": null
  },
  {
    "RAW": "COG3: MISURA ULTIMA CALx \"O2\" ZERO (Calibrazione Strumentale) N.U.",
    "NAME": "Misura Ultima Calx O2 Zero",
    "UNITS": null
  },
  {
    "RAW": "COG3: MISURA ULTIMA CALx \"O2\" SPAN (Calibrazione Strumentale) N.U.",
    "NAME": "Misura Ultima Calx O2 Span",
    "UNITS": null
  },
  {
    "RAW": "COG2: PROGRESSIVO DATI VERIFICA COMPLETAM. OK QAL3 C1 (Variaz = read Data a PC)",
    "NAME": "Prog. Dati Verifica QAL3 C1",
    "UNITS": null
  },
  {
    "RAW": "COG2: MISURA ULTIMA QAL3 \"CO\" ZERO (Validazione Strumentale)",
    "NAME": "Misura Ultima QAL3 CO Zero",
    "UNITS": null
  },
  {
    "RAW": "COG2: MISURA ULTIMA QAL3 \"CO\" SPAN (Validazione Strumentale)",
    "NAME": "Misura Ultima QAL3 CO Span",
    "UNITS": null
  },
  {
    "RAW": "COG2: MISURA ULTIMA QAL3 \"NO\" ZERO (Validazione Strumentale)",
    "NAME": "Misura Ultima QAL3 NO Zero",
    "UNITS": null
  },
  {
    "RAW": "COG2: MISURA ULTIMA QAL3 \"NO\" SPAN (Validazione Strumentale)",
    "NAME": "Misura Ultima QAL3 NO Span",
    "UNITS": null
  },
  {
    "RAW": "COG2: MISURA ULTIMA QAL3 \"O2\" ZERO (Validazione Strumentale)",
    "NAME": "Misura Ultima QAL3 O2 Zero",
    "UNITS": null
  },
  {
    "RAW": "COG2: MISURA ULTIMA QAL3 \"O2\" SPAN (Validazione Strumentale)",
    "NAME": "Misura Ultima QAL3 O2 Span",
    "UNITS": null
  },
  {
    "RAW": "COG3: PROGRESSIVO DATI VERIFICA COMPLETAM. OK QAL3 C2 (Variaz = read Data a PC)",
    "NAME": "Prog. Dati Verifica QAL3 C2",
    "UNITS": null
  },
  {
    "RAW": "COG3: MISURA ULTIMA QAL3 \"CO\" ZERO (Validazione Strumentale)",
    "NAME": "Misura Ultima QAL3 CO Zero",
    "UNITS": null
  },
  {
    "RAW": "COG3: MISURA ULTIMA QAL3 \"CO\" SPAN (Validazione Strumentale)",
    "NAME": "Misura Ultima QAL3 CO Span",
    "UNITS": null
  },
  {
    "RAW": "COG3: MISURA ULTIMA QAL3 \"NO\" ZERO (Validazione Strumentale)",
    "NAME": "Misura Ultima QAL3 NO Zero",
    "UNITS": null
  },
  {
    "RAW": "COG3: MISURA ULTIMA QAL3 \"NO\" SPAN (Validazione Strumentale)",
    "NAME": "Misura Ultima QAL3 NO Span",
    "UNITS": null
  },
  {
    "RAW": "COG3: MISURA ULTIMA QAL3 \"O2\" ZERO (Validazione Strumentale)",
    "NAME": "Misura Ultima QAL3 O2 Zero",
    "UNITS": null
  },
  {
    "RAW": "COG3: MISURA ULTIMA QAL3 \"O2\" SPAN (Validazione Strumentale)",
    "NAME": "Misura Ultima QAL3 O2 Span",
    "UNITS": null
  },
  {
    "RAW": "COG2: CAMPO SCALA LOW 1 MISURA \"TEMPERATURA LINEA PRELIEVO\"",
    "NAME": "Campo Scala Low Temp. Linea Prelievo",
    "UNITS": null
  },
  {
    "RAW": "COG2: CAMPO SCALA HIGH 1 MISURA \"TEMPERATURA LINEA PRELIEVO\"",
    "NAME": "Campo Scala High Temp. Linea Prelievo",
    "UNITS": null
  },
  {
    "RAW": "COG2: CAMPO SCALA LOW 1 MISURA \"PRESSIONE FUMI\"",
    "NAME": "Campo Scala Low Pressione Fumi",
    "UNITS": null
  },
  {
    "RAW": "COG2: CAMPO SCALA HIGH 1 MISURA \"PRESSIONE FUMI\"",
    "NAME": "Campo Scala High Pressione Fumi",
    "UNITS": null
  },
  {
    "RAW": "COG2: CAMPO SCALA LOW 1 MISURA \"TEMPERATURA FUMI\"",
    "NAME": "Campo Scala Low Temp. Fumi",
    "UNITS": null
  },
  {
    "RAW": "COG2: CAMPO SCALA HIGH 1 MISURA \"TEMPERATURA FUMI\"",
    "NAME": "Campo Scala High Temp. Fumi",
    "UNITS": null
  },
  {
    "RAW": "COG2: CAMPO SCALA LOW 1 MISURA \"POTENZA COGENERATORE\"",
    "NAME": "Campo Scala Low Potenza Cogeneratore",
    "UNITS": null
  },
  {
    "RAW": "COG2: CAMPO SCALA HIGH 1 MISURA \"POTENZA COGENERATORE\"",
    "NAME": "Campo Scala High Potenza Cogeneratore",
    "UNITS": null
  },
  {
    "RAW": "COG2: CAMPO SCALA LOW 1 MISURA \"PORTATA GAS\"",
    "NAME": "Campo Scala Low Portata Gas",
    "UNITS": null
  },
  {
    "RAW": "COG2: CAMPO SCALA HIGH 1 MISURA \"PORTATA GAS\"",
    "NAME": "Campo Scala High Portata Gas",
    "UNITS": null
  },
  {
    "RAW": "COG3: CAMPO SCALA LOW 1 MISURA \"TEMPERATURA LINEA PRELIEVO\"",
    "NAME": "Campo Scala Low Temp. Linea Prelievo",
    "UNITS": null
  },
  {
    "RAW": "COG3: CAMPO SCALA HIGH 1 MISURA \"TEMPERATURA LINEA PRELIEVO\"",
    "NAME": "Campo Scala High Temp. Linea Prelievo",
    "UNITS": null
  },
  {
    "RAW": "COG3: CAMPO SCALA LOW 1 MISURA \"PRESSIONE FUMI\"",
    "NAME": "Campo Scala Low Pressione Fumi",
    "UNITS": null
  },
  {
    "RAW": "COG3: CAMPO SCALA HIGH 1 MISURA \"PRESSIONE FUMI\"",
    "NAME": "Campo Scala High Pressione Fumi",
    "UNITS": null
  },
  {
    "RAW": "COG3: CAMPO SCALA LOW 1 MISURA \"TEMPERATURA FUMI\"",
    "NAME": "Campo Scala Low Temp. Fumi",
    "UNITS": null
  },
  {
    "RAW": "COG3: CAMPO SCALA HIGH 1 MISURA \"TEMPERATURA FUMI\"",
    "NAME": "Campo Scala High Temp. Fumi",
    "UNITS": null
  },
  {
    "RAW": "COG3: CAMPO SCALA LOW 1 MISURA \"POTENZA COGENERATORE\"",
    "NAME": "Campo Scala Low Potenza Cogeneratore",
    "UNITS": null
  },
  {
    "RAW": "COG3: CAMPO SCALA HIGH 1 MISURA \"POTENZA COGENERATORE\"",
    "NAME": "Campo Scala High Potenza Cogeneratore",
    "UNITS": null
  },
  {
    "RAW": "COG3: CAMPO SCALA LOW 1 MISURA \"PORTATA GAS\"",
    "NAME": "Campo Scala Low Portata Gas",
    "UNITS": null
  },
  {
    "RAW": "COG3: CAMPO SCALA HIGH 1 MISURA \"PORTATA GAS\"",
    "NAME": "Campo Scala High Portata Gas",
    "UNITS": null
  },
  {
    "RAW": "COG2-SUPERATO LIMITE CO MEDIA 1H PROGRESSIVA (Write PC Sme)",
    "NAME": "Superato Limite CO Media 1H Progr.",
    "UNITS": null
  },
  {
    "RAW": "COG2-SUPERATO LIMITE CO MEDIA 1H PREVISIONALE (Write PC Sme)",
    "NAME": "Superato Limite CO Media 1H Prev.",
    "UNITS": null
  },
  {
    "RAW": "COG2-SUPERATO LIMITE CO MEDIA 1H PRECEDENTE (Write PC Sme)",
    "NAME": "Superato Limite CO Media 1H Prec.",
    "UNITS": null
  },
  {
    "RAW": "COG2-SUPERATO LIMITE NOX MEDIA 1H PROGRESSIVA (Write PC Sme)",
    "NAME": "Superato Limite NOx Media 1H Progr.",
    "UNITS": null
  },
  {
    "RAW": "COG2-SUPERATO LIMITE NOX MEDIA 1H PREVISIONALE (Write PC Sme)",
    "NAME": "Superato Limite NOx Media 1H Prev.",
    "UNITS": null
  },
  {
    "RAW": "COG2-SUPERATO LIMITE NOX MEDIA 1H PRECEDENTE (Write PC Sme)",
    "NAME": "Superato Limite NOx Media 1H Prec.",
    "UNITS": null
  },
  {
    "RAW": "COG3-SUPERATO LIMITE CO MEDIA 1H PROGRESSIVA (Write PC Sme)",
    "NAME": "Superato Limite CO Media 1H Progr.",
    "UNITS": null
  },
  {
    "RAW": "COG3-SUPERATO LIMITE CO MEDIA 1H PREVISIONALE (Write PC Sme)",
    "NAME": "Superato Limite CO Media 1H Prev.",
    "UNITS": null
  },
  {
    "RAW": "COG3-SUPERATO LIMITE CO MEDIA 1H PRECEDENTE (Write PC Sme)",
    "NAME": "Superato Limite CO Media 1H Prec.",
    "UNITS": null
  },
  {
    "RAW": "COG3-SUPERATO LIMITE NOX MEDIA 1H PROGRESSIVA (Write PC Sme)",
    "NAME": "Superato Limite NOx Media 1H Progr.",
    "UNITS": null
  },
  {
    "RAW": "COG3-SUPERATO LIMITE NOX MEDIA 1H PREVISIONALE (Write PC Sme)",
    "NAME": "Superato Limite NOx Media 1H Prev.",
    "UNITS": null
  },
  {
    "RAW": "COG3-SUPERATO LIMITE NOX MEDIA 1H PRECEDENTE (Write PC Sme)",
    "NAME": "Superato Limite NOx Media 1H Prec.",
    "UNITS": null
  },
  {
    "RAW": "COG2- PREALLARME EMISSIONE \"CO\" (Write PC Sme)",
    "NAME": "Preall. Emissione CO (Write PC Sme)",
    "UNITS": null
  },
  {
    "RAW": "COG2- PREALLARME EMISSIONE \"NO\" (Write PC Sme)",
    "NAME": "Preall. Emissione NO (Write PC Sme)",
    "UNITS": null
  },
  {
    "RAW": "COG2- ALLARME SUPERAMENTO EMISSIONI (Write PC Sme)",
    "NAME": "All. Superamento Emissioni (Write PC Sme)",
    "UNITS": null
  },
  {
    "RAW": "COG3- PREALLARME EMISSIONE \"CO\" (Write PC Sme)",
    "NAME": "Preall. Emissione CO (Write PC Sme)",
    "UNITS": null
  },
  {
    "RAW": "COG3- PREALLARME EMISSIONE \"NO\" (Write PC Sme)",
    "NAME": "Preall. Emissione NO (Write PC Sme)",
    "UNITS": null
  },
  {
    "RAW": "COG3- ALLARME SUPERAMENTO EMISSIONI (Write PC Sme)",
    "NAME": "All. Superamento Emissioni (Write PC Sme)",
    "UNITS": null
  }
]"""

# ---------------------------------------------------------------------------
# STEP 0 — Parse all five model strings into Python lists
# Markdown fences (```json ... ```) are stripped automatically.
# ---------------------------------------------------------------------------

_raw_text_m1 = M1_STRING.strip()
_raw_text_m1 = re.sub(r"^```(?:json)?\s*", "", _raw_text_m1)
_raw_text_m1 = re.sub(r"\s*```$", "", _raw_text_m1)
m1 = json.loads(_raw_text_m1)

_raw_text_m2 = M2_STRING.strip()
_raw_text_m2 = re.sub(r"^```(?:json)?\s*", "", _raw_text_m2)
_raw_text_m2 = re.sub(r"\s*```$", "", _raw_text_m2)
m2 = json.loads(_raw_text_m2)

_raw_text_m3 = M3_STRING.strip()
_raw_text_m3 = re.sub(r"^```(?:json)?\s*", "", _raw_text_m3)
_raw_text_m3 = re.sub(r"\s*```$", "", _raw_text_m3)
m3 = json.loads(_raw_text_m3)

_raw_text_m4 = M4_STRING.strip()
_raw_text_m4 = re.sub(r"^```(?:json)?\s*", "", _raw_text_m4)
_raw_text_m4 = re.sub(r"\s*```$", "", _raw_text_m4)
m4 = json.loads(_raw_text_m4)

_raw_text_m5 = M5_STRING.strip()
_raw_text_m5 = re.sub(r"^```(?:json)?\s*", "", _raw_text_m5)
_raw_text_m5 = re.sub(r"\s*```$", "", _raw_text_m5)
m5 = json.loads(_raw_text_m5)

print(f"[INFO] Loaded — M1:{len(m1)} stations  M2:{len(m2)} analogs  "
      f"M3:{len(m3)} packed  M4:{len(m4)} bits  M5:{len(m5)} names")

# ---------------------------------------------------------------------------
# STEP 1 — Build station map from Model 1
# One dict per distinct IP.  Keys: ID, NAME, DRIVERNAME, DRIVERCONFIG,
# measures (list), bitinfo (list), _ip (internal).
# ---------------------------------------------------------------------------

stations = {}

for _raw_station in m1:
    _sid = int(_raw_station["ID"])
    _cfg = _raw_station.get("DRIVERCONFIG", ":")
    _ip_part = _cfg.split(":")[0] if ":" in _cfg else _cfg
    _ip_norm = _ip_part.replace(",", ".").strip()

    stations[_sid] = {
        "NAME":         _raw_station.get("NAME", "SME"),
        "DRIVERNAME":   _raw_station.get("DRIVERNAME", "modbusplc"),
        "DRIVERCONFIG": _cfg,
        "ID":           _sid,
        "_ip":          _ip_norm,
        "measures":     [],
        "bitinfo":      [],
    }

print(f"[INFO] Stations found: {len(stations)}")

# ---------------------------------------------------------------------------
# STEP 2 — Build NAME / UNITS lookup table from Model 5
# {lowercase_raw_description: {"NAME": ..., "UNITS": ...}}
# ---------------------------------------------------------------------------

name_lookup = {}

for _entry in m5:
    _raw_key = _entry.get("RAW", "").strip().lower()
    name_lookup[_raw_key] = {
        "NAME":  _entry.get("NAME"),   # may be None for skip-words
        "UNITS": _entry.get("UNITS"),
    }

print(f"[INFO] Name lookup entries: {len(name_lookup)}")

# ---------------------------------------------------------------------------
# STEP 3 — Process analog measures from Model 2
# Skip rows with reserved descriptions.
# Apply NAME resolution + field enforcement inline.
# ---------------------------------------------------------------------------

SKIP_DESCRIPTIONS = {
    "available", "disponibile", "not used", "reserve",
    "spare", "input", "output", "parameter",
}

all_measures = []

print(f"[INFO] Analog measures (M2): {len(m2)}")

for _raw_m in m2:

    # --- Skip check ---
    _desc = _raw_m.get("NAME")
    if _desc is None:
        continue
    _desc_lower = _desc.strip().lower()
    if _desc_lower in SKIP_DESCRIPTIONS:
        continue
    if "disponibile" in _desc_lower:
        continue

    # --- Deep copy so we don't mutate the original ---
    _m = deepcopy(_raw_m)

    # --- NAME resolution ---
    _raw_name = _m.get("NAME", "")
    _lookup_key = _raw_name.strip().lower()

    if _lookup_key in name_lookup and name_lookup[_lookup_key]["NAME"] is not None:
        _m["NAME"] = name_lookup[_lookup_key]["NAME"]
    else:
        # Fallback: run NAME algorithm inline
        _n = _raw_name
        _n = re.sub(r"\([^)]*\)", "", _n)
        _n = re.sub(r"\[[^\]]*\]", "", _n)
        _n = _n.strip()
        _n = re.sub(r"\b(di|del|della|in|da|per|con)\b", "", _n, flags=re.IGNORECASE).strip()
        _n = re.sub(r"\s{2,}", " ", _n)
        if len(_n) > 25:
            _n = re.sub(r"\bAnalizzatore\b", "Anal.",   _n, flags=re.IGNORECASE)
        if len(_n) > 25:
            _n = re.sub(r"\bConvertitore\b", "Conv.",   _n, flags=re.IGNORECASE)
        if len(_n) > 25:
            _n = re.sub(r"\bManutenzione\b", "Manut.",  _n, flags=re.IGNORECASE)
        if len(_n) > 25:
            _n = re.sub(r"\bCalibrazione\b", "Calib.",  _n, flags=re.IGNORECASE)
        if len(_n) > 25:
            _n = re.sub(r"\bTemperatura\b",  "Temp.",   _n, flags=re.IGNORECASE)
        if len(_n) > 25:
            _n = re.sub(r"\bCollegamento\b", "Colleg.", _n, flags=re.IGNORECASE)
        if len(_n) > 25:
            _n = re.sub(r"\bComunicazione\b","Comm.",   _n, flags=re.IGNORECASE)
        if len(_n) > 25:
            _n = re.sub(r"\bOssigeno\b",     "O2",      _n, flags=re.IGNORECASE)
        if len(_n) > 25:
            _n = re.sub(r"\bAllarme\b",      "All.",    _n, flags=re.IGNORECASE)
        if len(_n) > 25:
            _n = re.sub(r"\brichiesta\b",    "rich.",   _n, flags=re.IGNORECASE)
        if len(_n) > 25:
            _n = re.sub(r"\bpresenza\b",     "pres.",   _n, flags=re.IGNORECASE)
        if len(_n) > 25:
            _n = re.sub(r"\bComando\b",      "Cmd",     _n, flags=re.IGNORECASE)
        _n = _n[:25].strip()
        _m["NAME"] = _n

    # --- UNITS resolution ---
    _declared_units = _m.get("UNITS")
    if _declared_units is None:
        _uk = _raw_name.strip().lower()
        if _uk in name_lookup:
            _m["UNITS"] = name_lookup[_uk]["UNITS"]
        # else stays None

    # --- Force analog fields ---
    _m["DRIVERDATA"] = 0
    _m["TYPE"]       = 0

    # --- MODBUSREGISTRO: ensure key exists; coerce plain integer strings ---
    if "MODBUSREGISTRO" not in _m:
        _m["MODBUSREGISTRO"] = None
    _reg = _m["MODBUSREGISTRO"]
    if isinstance(_reg, str) and re.match(r"^[1-9]\d*$", _reg):
        _m["MODBUSREGISTRO"] = int(_reg)

    # --- STATIONID: validate and default ---
    try:
        _sid = int(_raw_m.get("STATIONID", 1))
    except (TypeError, ValueError):
        _sid = 1
    if _sid not in stations:
        _sid = min(stations.keys())
    _m["STATIONID"] = _sid

    # --- Clean internal keys ---
    _m.pop("_raw_desc", None)

    all_measures.append(_m)

# ---------------------------------------------------------------------------
# STEP 4 — Process packed digital measures from Model 3
# ---------------------------------------------------------------------------

print(f"[INFO] Packed measures (M3): {len(m3)}")

for _raw_m in m3:

    _m = deepcopy(_raw_m)

    # --- NAME resolution (same inline algorithm) ---
    _raw_name = _m.get("NAME", "")
    _lookup_key = _raw_name.strip().lower()

    if _lookup_key in name_lookup and name_lookup[_lookup_key]["NAME"] is not None:
        _m["NAME"] = name_lookup[_lookup_key]["NAME"]
    else:
        _n = _raw_name
        _n = re.sub(r"\([^)]*\)", "", _n)
        _n = re.sub(r"\[[^\]]*\]", "", _n)
        _n = _n.strip()
        _n = re.sub(r"\b(di|del|della|in|da|per|con)\b", "", _n, flags=re.IGNORECASE).strip()
        _n = re.sub(r"\s{2,}", " ", _n)
        if len(_n) > 25:
            _n = re.sub(r"\bAnalizzatore\b", "Anal.",   _n, flags=re.IGNORECASE)
        if len(_n) > 25:
            _n = re.sub(r"\bConvertitore\b", "Conv.",   _n, flags=re.IGNORECASE)
        if len(_n) > 25:
            _n = re.sub(r"\bManutenzione\b", "Manut.",  _n, flags=re.IGNORECASE)
        if len(_n) > 25:
            _n = re.sub(r"\bCalibrazione\b", "Calib.",  _n, flags=re.IGNORECASE)
        if len(_n) > 25:
            _n = re.sub(r"\bTemperatura\b",  "Temp.",   _n, flags=re.IGNORECASE)
        if len(_n) > 25:
            _n = re.sub(r"\bCollegamento\b", "Colleg.", _n, flags=re.IGNORECASE)
        if len(_n) > 25:
            _n = re.sub(r"\bComunicazione\b","Comm.",   _n, flags=re.IGNORECASE)
        if len(_n) > 25:
            _n = re.sub(r"\bOssigeno\b",     "O2",      _n, flags=re.IGNORECASE)
        if len(_n) > 25:
            _n = re.sub(r"\bAllarme\b",      "All.",    _n, flags=re.IGNORECASE)
        if len(_n) > 25:
            _n = re.sub(r"\brichiesta\b",    "rich.",   _n, flags=re.IGNORECASE)
        if len(_n) > 25:
            _n = re.sub(r"\bpresenza\b",     "pres.",   _n, flags=re.IGNORECASE)
        if len(_n) > 25:
            _n = re.sub(r"\bComando\b",      "Cmd",     _n, flags=re.IGNORECASE)
        _n = _n[:25].strip()
        _m["NAME"] = _n

    # --- UNITS always null for packed digitals ---
    _m["UNITS"] = None

    # --- Force packed digital fields ---
    _m["DRIVERDATA"] = 2
    _m["TYPE"]       = 1

    # --- GROUP: preserve if present and non-empty; remove otherwise ---
    if "GROUP" in _m and not _m["GROUP"]:
        del _m["GROUP"]

    # --- MODBUSREGISTRO: coerce plain integer strings ---
    _reg = _m.get("MODBUSREGISTRO")
    if isinstance(_reg, str) and re.match(r"^[1-9]\d*$", _reg):
        _m["MODBUSREGISTRO"] = int(_reg)

    # --- STATIONID: validate and default ---
    try:
        _sid = int(_raw_m.get("STATIONID", 1))
    except (TypeError, ValueError):
        _sid = 1
    if _sid not in stations:
        _sid = min(stations.keys())
    _m["STATIONID"] = _sid

    _m.pop("_raw_desc", None)

    all_measures.append(_m)

# ---------------------------------------------------------------------------
# STEP 5 — Deduplicate: if M2 and M3 both produced the same (station, register)
# as a packed digital, keep M3's version. Analogs may share registers freely.
# ---------------------------------------------------------------------------

_packed_keys = set()
for _m in all_measures:
    if _m.get("DRIVERDATA") == 2:
        _packed_keys.add((_m.get("STATIONID"), _m.get("MODBUSREGISTRO")))

_seen_packed = set()
_deduped_measures = []

for _m in all_measures:
    if _m.get("DRIVERDATA") == 2:
        _key = (_m.get("STATIONID"), _m.get("MODBUSREGISTRO"))
        if _key in _seen_packed:
            continue   # drop duplicate packed measure
        _seen_packed.add(_key)
        _deduped_measures.append(_m)
    elif _m.get("DRIVERDATA") == 0:
        _key = (_m.get("STATIONID"), _m.get("MODBUSREGISTRO"))
        if _key in _packed_keys and _m["MODBUSREGISTRO"] is not None:
            continue   # M3 owns this register; drop M2's analog version
        _deduped_measures.append(_m)
    else:
        _deduped_measures.append(_m)

all_measures = _deduped_measures

# ---------------------------------------------------------------------------
# STEP 6 — Assign measures to their stations
# ---------------------------------------------------------------------------

for _m in all_measures:
    _sid = _m["STATIONID"]
    stations[_sid]["measures"].append(_m)

# ---------------------------------------------------------------------------
# STEP 7 — Process bitinfo entries from Model 4
# ---------------------------------------------------------------------------

print(f"[INFO] Bitinfo entries  (M4): {len(m4)}")

for _raw_b in m4:

    _b = deepcopy(_raw_b)

    # --- MEASUREID: coerce to int if plain integer string ---
    _mid = _b.get("MEASUREID")
    if isinstance(_mid, str) and re.match(r"^[1-9]\d*$", _mid):
        _b["MEASUREID"] = int(_mid)

    # --- BITNO: always int ---
    _b["BITNO"] = int(_b.get("BITNO", 0))

    # --- BITNAME: never empty ---
    if not _b.get("BITNAME", "").strip():
        _b["BITNAME"] = f"Bit {_b['BITNO']}"

    # --- TEXTON / TEXTOFF must differ ---
    if _b.get("TEXTON") == _b.get("TEXTOFF"):
        _b["TEXTOFF"] = "OFF" if _b["TEXTON"] != "OFF" else "Attivo"

    # --- STATIONID: validate and default ---
    try:
        _sid = int(_raw_b.get("STATIONID", 1))
    except (TypeError, ValueError):
        _sid = 1
    if _sid not in stations:
        _sid = min(stations.keys())
    _b["STATIONID"] = _sid

    stations[_sid]["bitinfo"].append(_b)

# ---------------------------------------------------------------------------
# STEP 8 — Assign sequential _measure_seq IDs per station (internal use)
# ---------------------------------------------------------------------------

for _sid, _station in stations.items():
    for _idx, _measure in enumerate(_station["measures"], start=1):
        _measure["_measure_seq"] = _idx

# ---------------------------------------------------------------------------
# STEP 9 — Serialise to final output structure
# ---------------------------------------------------------------------------

INTERNAL_KEYS = {"_ip", "_measure_seq", "_raw_desc", "STATIONID"}

result = []

for _sid in sorted(stations.keys()):
    _station = stations[_sid]

    _out_station = {
        "NAME":         _station["NAME"],
        "DRIVERNAME":   _station["DRIVERNAME"],
        "DRIVERCONFIG": _station["DRIVERCONFIG"],
        "ID":           _station["ID"],
        "measures":     [],
        "bitinfo":      [],
    }

    for _m in _station["measures"]:
        _entry = {_k: _v for _k, _v in _m.items() if _k not in INTERNAL_KEYS}
        if "UNITS" not in _entry:
            _entry["UNITS"] = None
        _out_station["measures"].append(_entry)

    for _b in _station["bitinfo"]:
        _entry = {_k: _v for _k, _v in _b.items() if _k not in INTERNAL_KEYS}
        _out_station["bitinfo"].append(_entry)

    result.append(_out_station)

# ---------------------------------------------------------------------------
# STEP 10 — Validation summary + warnings
# ---------------------------------------------------------------------------

_total_measures = sum(len(_s["measures"]) for _s in result)
_total_bits     = sum(len(_s["bitinfo"])  for _s in result)
print(f"[INFO] Final: {len(result)} stations, "
      f"{_total_measures} measures, {_total_bits} bitinfo entries")

for _s in result:
    for _m in _s["measures"]:
        if not _m.get("NAME"):
            print(f"[WARN] Measure with empty NAME in station {_s['ID']}: {_m}")

# ---------------------------------------------------------------------------
# result  ←  final list of station dicts, ready for use
# ---------------------------------------------------------------------------
output_json_final = json.dumps(result, ensure_ascii=False, indent=2)

with open('./multipleevasoutput.json', 'w', encoding="utf-8") as file:
    json.dump(result, file, indent=4, ensure_ascii=False)
