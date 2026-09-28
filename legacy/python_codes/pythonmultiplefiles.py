import json
import struct
import traceback
import re

# ---------------------------------------------------------------------------
# Constants 
# ---------------------------------------------------------------------------
SIGNED_SHORT     = 150
FLOAT_SINGLE_BE  = 250
VM_SOURCE_CODE_DEFAULT = "if elapsed() then    storep(11);else store(8);fi;"
DRIVERCONFIG_MEASURE   = '<configuration SynopticAnalogicFormat=\\"%7.2f\\"/>'
BIG_POS =  3.40282e+38
BIG_NEG = -3.40282e+38

input_json = r'''[

[
  {
    "_subkey": "misura_insert",
    "_params": [
      {
        "nome": "Allarme sonda riscaldata",
        "tag": "AL_SONDA",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40001",
        "analogico": 0,
        "digit_singolo": 0,
        "digit_impaccato": 1,
        "bit_posizione": 8,
        "stato_off": "OFF",
        "stato_on": "Allarme",
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "Allarme linea riscaldata",
        "tag": "AL_LINEA",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40001",
        "analogico": 0,
        "digit_singolo": 0,
        "digit_impaccato": 1,
        "bit_posizione": 9,
        "stato_off": "OFF",
        "stato_on": "Allarme",
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "Allarme frigorifero",
        "tag": "AL_FRIGO",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40001",
        "analogico": 0,
        "digit_singolo": 0,
        "digit_impaccato": 1,
        "bit_posizione": 10,
        "stato_off": "OFF",
        "stato_on": "Allarme",
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "Allarme presenza condensa",
        "tag": "AL_COND",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40001",
        "analogico": 0,
        "digit_singolo": 0,
        "digit_impaccato": 1,
        "bit_posizione": 11,
        "stato_off": "OFF",
        "stato_on": "Allarme",
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "Allarme mancanza flusso",
        "tag": "AL_FL",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40001",
        "analogico": 0,
        "digit_singolo": 0,
        "digit_impaccato": 1,
        "bit_posizione": 12,
        "stato_off": "OFF",
        "stato_on": "Allarme",
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "Allarme analizzatore SO2",
        "tag": "AL_A1",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40001",
        "analogico": 0,
        "digit_singolo": 0,
        "digit_impaccato": 1,
        "bit_posizione": 13,
        "stato_off": "OFF",
        "stato_on": "Allarme",
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "Sistema in misura",
        "tag": "MEASURE",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40003",
        "analogico": 0,
        "digit_singolo": 0,
        "digit_impaccato": 1,
        "bit_posizione": 8,
        "stato_off": "OFF",
        "stato_on": "Misura",
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "Calibrazione automatica in corso",
        "tag": "CAL_AUTO",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40003",
        "analogico": 0,
        "digit_singolo": 0,
        "digit_impaccato": 1,
        "bit_posizione": 9,
        "stato_off": "OFF",
        "stato_on": "Calibrazione",
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "Analizzatore SO2 in calibrazione di zero",
        "tag": "CAL_ZERO_1",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40003",
        "analogico": 0,
        "digit_singolo": 0,
        "digit_impaccato": 1,
        "bit_posizione": 10,
        "stato_off": "OFF",
        "stato_on": "Calibrazione",
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "Analizzatore SO2 in calibrazione di span",
        "tag": "CAL_SPAN_1",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40003",
        "analogico": 0,
        "digit_singolo": 0,
        "digit_impaccato": 1,
        "bit_posizione": 11,
        "stato_off": "OFF",
        "stato_on": "Calibrazione",
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "Secondo campo SO2",
        "tag": "SO2_RG2",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40003",
        "analogico": 0,
        "digit_singolo": 0,
        "digit_impaccato": 1,
        "bit_posizione": 15,
        "stato_off": "OFF",
        "stato_on": "Campo",
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "QAL3 in corso",
        "tag": "Q3",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40003",
        "analogico": 0,
        "digit_singolo": 0,
        "digit_impaccato": 1,
        "bit_posizione": 0,
        "stato_off": "OFF",
        "stato_on": "QAL3",
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "QAL3: elettrovalvola ARIA",
        "tag": "Q3_Z",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40003",
        "analogico": 0,
        "digit_singolo": 0,
        "digit_impaccato": 1,
        "bit_posizione": 1,
        "stato_off": "OFF",
        "stato_on": "QAL3",
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "QAL3: elettrovalvola span SO2",
        "tag": "Q3_S1",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40003",
        "analogico": 0,
        "digit_singolo": 0,
        "digit_impaccato": 1,
        "bit_posizione": 2,
        "stato_off": "OFF",
        "stato_on": "QAL3",
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "QAL3: lavaggio con N2",
        "tag": "Q3_N2",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40003",
        "analogico": 0,
        "digit_singolo": 0,
        "digit_impaccato": 1,
        "bit_posizione": 3,
        "stato_off": "OFF",
        "stato_on": "QAL3",
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "QAL3: ciclo concluso senza errori",
        "tag": "Q3_OK",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40003",
        "analogico": 0,
        "digit_singolo": 0,
        "digit_impaccato": 1,
        "bit_posizione": 5,
        "stato_off": "OFF",
        "stato_on": "QAL3",
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "QAL3: ciclo concluso con errori",
        "tag": "Q3_KO",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40003",
        "analogico": 0,
        "digit_singolo": 0,
        "digit_impaccato": 1,
        "bit_posizione": 6,
        "stato_off": "OFF",
        "stato_on": "QAL3",
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "Pompa analisi",
        "tag": "PA1",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40003",
        "analogico": 0,
        "digit_singolo": 0,
        "digit_impaccato": 1,
        "bit_posizione": 7,
        "stato_off": "OFF",
        "stato_on": "Pompa",
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "Stato elettrovalvola cal zero",
        "tag": "EVZ",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40004",
        "analogico": 0,
        "digit_singolo": 0,
        "digit_impaccato": 1,
        "bit_posizione": 8,
        "stato_off": "OFF",
        "stato_on": "Stato",
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "Stato elettrovalvola N2",
        "tag": "EVZ2",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40004",
        "analogico": 0,
        "digit_singolo": 0,
        "digit_impaccato": 1,
        "bit_posizione": 9,
        "stato_off": "OFF",
        "stato_on": "Stato",
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "Stato elettrovalvola cal span",
        "tag": "EVS",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40004",
        "analogico": 0,
        "digit_singolo": 0,
        "digit_impaccato": 1,
        "bit_posizione": 10,
        "stato_off": "OFF",
        "stato_on": "Stato",
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "Elettrovalvola cal da sonda",
        "tag": "EVC",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40004",
        "analogico": 0,
        "digit_singolo": 0,
        "digit_impaccato": 1,
        "bit_posizione": 11,
        "stato_off": "OFF",
        "stato_on": "Stato",
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "PLC life signal",
        "tag": "HB",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40004",
        "analogico": 0,
        "digit_singolo": 0,
        "digit_impaccato": 1,
        "bit_posizione": 13,
        "stato_off": "OFF",
        "stato_on": "PLC",
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "Impianto in marcia",
        "tag": "PL_ON",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40004",
        "analogico": 0,
        "digit_singolo": 0,
        "digit_impaccato": 1,
        "bit_posizione": 0,
        "stato_off": "OFF",
        "stato_on": "Marcia",
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "Impianto in minimo tecnico/funzionamento anomalo",
        "tag": "PL_MT",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40004",
        "analogico": 0,
        "digit_singolo": 0,
        "digit_impaccato": 1,
        "bit_posizione": 1,
        "stato_off": "OFF",
        "stato_on": "Anomalia",
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "Impianto in avviamento",
        "tag": "PL_AVV",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40004",
        "analogico": 0,
        "digit_singolo": 0,
        "digit_impaccato": 1,
        "bit_posizione": 2,
        "stato_off": "OFF",
        "stato_on": "Avviamento",
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "Impianto in spegnimento",
        "tag": "PL_SHUT",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40004",
        "analogico": 0,
        "digit_singolo": 0,
        "digit_impaccato": 1,
        "bit_posizione": 3,
        "stato_off": "OFF",
        "stato_on": "Spegnimento",
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "SME in manutenzione",
        "tag": "SME_MAINT",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40004",
        "analogico": 0,
        "digit_singolo": 0,
        "digit_impaccato": 1,
        "bit_posizione": 5,
        "stato_off": "OFF",
        "stato_on": "Manutenzione",
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "Impianto in manutenzione",
        "tag": "PL_MAINT",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40004",
        "analogico": 0,
        "digit_singolo": 0,
        "digit_impaccato": 1,
        "bit_posizione": 6,
        "stato_off": "OFF",
        "stato_on": "Manutenzione",
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "Impianto fuori servizio per guasto",
        "tag": "PL_OUT",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40004",
        "analogico": 0,
        "digit_singolo": 0,
        "digit_impaccato": 1,
        "bit_posizione": 7,
        "stato_off": "OFF",
        "stato_on": "Guasto",
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "Blocco da BSS2",
        "tag": "AL_BSS2",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40005",
        "analogico": 0,
        "digit_singolo": 0,
        "digit_impaccato": 1,
        "bit_posizione": 8,
        "stato_off": "OFF",
        "stato_on": "Blocco",
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "Allarme bassa portata FT-2611",
        "tag": "ALL_FT_2611",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40005",
        "analogico": 0,
        "digit_singolo": 0,
        "digit_impaccato": 1,
        "bit_posizione": 9,
        "stato_off": "OFF",
        "stato_on": "Allarme",
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "Allarme bassa portata FT-310",
        "tag": "ALL_FT_310",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40005",
        "analogico": 0,
        "digit_singolo": 0,
        "digit_impaccato": 1,
        "bit_posizione": 10,
        "stato_off": "OFF",
        "stato_on": "Allarme",
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "Allarme bassa portata FT-313",
        "tag": "ALL_FT_313",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40005",
        "analogico": 0,
        "digit_singolo": 0,
        "digit_impaccato": 1,
        "bit_posizione": 11,
        "stato_off": "OFF",
        "stato_on": "Allarme",
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "Allarme basso pH",
        "tag": "ALL_AI_303A",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40005",
        "analogico": 0,
        "digit_singolo": 0,
        "digit_impaccato": 1,
        "bit_posizione": 12,
        "stato_off": "OFF",
        "stato_on": "Allarme",
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "Allarme basso pH",
        "tag": "ALL_AI_303B",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40005",
        "analogico": 0,
        "digit_singolo": 0,
        "digit_impaccato": 1,
        "bit_posizione": 13,
        "stato_off": "OFF",
        "stato_on": "Allarme",
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "Allarme basso pH",
        "tag": "ALL_AI2602A",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40005",
        "analogico": 0,
        "digit_singolo": 0,
        "digit_impaccato": 1,
        "bit_posizione": 14,
        "stato_off": "OFF",
        "stato_on": "Allarme",
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "Allarme basso pH",
        "tag": "ALL_2602B",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40005",
        "analogico": 0,
        "digit_singolo": 0,
        "digit_impaccato": 1,
        "bit_posizione": 15,
        "stato_off": "OFF",
        "stato_on": "Allarme",
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "PM-302A in marcia",
        "tag": "PM_302A",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40005",
        "analogico": 0,
        "digit_singolo": 0,
        "digit_impaccato": 1,
        "bit_posizione": 1,
        "stato_off": "OFF",
        "stato_on": "Marcia",
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "PM-302B in marcia",
        "tag": "PM_302B",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40005",
        "analogico": 0,
        "digit_singolo": 0,
        "digit_impaccato": 1,
        "bit_posizione": 2,
        "stato_off": "OFF",
        "stato_on": "Marcia",
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "PM-310A in marcia",
        "tag": "PM_310A",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40005",
        "analogico": 0,
        "digit_singolo": 0,
        "digit_impaccato": 1,
        "bit_posizione": 4,
        "stato_off": "OFF",
        "stato_on": "Marcia",
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "PM-310B in marcia",
        "tag": "PM_310B",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40005",
        "analogico": 0,
        "digit_singolo": 0,
        "digit_impaccato": 1,
        "bit_posizione": 5,
        "stato_off": "OFF",
        "stato_on": "Marcia",
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "PM-2600A in marcia",
        "tag": "PM_2600A",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40006",
        "analogico": 0,
        "digit_singolo": 0,
        "digit_impaccato": 1,
        "bit_posizione": 8,
        "stato_off": "OFF",
        "stato_on": "Marcia",
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "PM-2600B in marcia",
        "tag": "PM_2600B",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40006",
        "analogico": 0,
        "digit_singolo": 0,
        "digit_impaccato": 1,
        "bit_posizione": 9,
        "stato_off": "OFF",
        "stato_on": "Marcia",
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "PM-2601A in marcia",
        "tag": "PM_2601A",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40006",
        "analogico": 0,
        "digit_singolo": 0,
        "digit_impaccato": 1,
        "bit_posizione": 10,
        "stato_off": "OFF",
        "stato_on": "Marcia",
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "PM-2601B in marcia",
        "tag": "PM_2601B",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40006",
        "analogico": 0,
        "digit_singolo": 0,
        "digit_impaccato": 1,
        "bit_posizione": 11,
        "stato_off": "OFF",
        "stato_on": "Marcia",
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "PM-2604A in marcia",
        "tag": "PM_2604A",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40006",
        "analogico": 0,
        "digit_singolo": 0,
        "digit_impaccato": 1,
        "bit_posizione": 12,
        "stato_off": "OFF",
        "stato_on": "Marcia",
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "PM-2604B in marcia",
        "tag": "PM_2604B",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40006",
        "analogico": 0,
        "digit_singolo": 0,
        "digit_impaccato": 1,
        "bit_posizione": 13,
        "stato_off": "OFF",
        "stato_on": "Marcia",
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "Ventilatore VN-400 in marcia",
        "tag": "VN_400",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40006",
        "analogico": 0,
        "digit_singolo": 0,
        "digit_impaccato": 1,
        "bit_posizione": 0,
        "stato_off": "OFF",
        "stato_on": "Marcia",
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "Ventilatore VN-2504 in marcia",
        "tag": "VN_2504",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40006",
        "analogico": 0,
        "digit_singolo": 0,
        "digit_impaccato": 1,
        "bit_posizione": 1,
        "stato_off": "OFF",
        "stato_on": "Marcia",
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "Ventilatore 514K1 in marcia",
        "tag": "514K1",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40006",
        "analogico": 0,
        "digit_singolo": 0,
        "digit_impaccato": 1,
        "bit_posizione": 2,
        "stato_off": "OFF",
        "stato_on": "Marcia",
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "Ventilatore 514K2 in marcia",
        "tag": "514K2",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40006",
        "analogico": 0,
        "digit_singolo": 0,
        "digit_impaccato": 1,
        "bit_posizione": 3,
        "stato_off": "OFF",
        "stato_on": "Marcia",
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "QAL3: Tempo elettrov N2",
        "tag": "TT_Q3_N2",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40009",
        "analogico": 1,
        "digit_singolo": 0,
        "digit_impaccato": 0,
        "bit_posizione": null,
        "stato_off": null,
        "stato_on": null,
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "QAL3: Tempo elettrov ARIA",
        "tag": "TT_Q3_AIR",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40010",
        "analogico": 1,
        "digit_singolo": 0,
        "digit_impaccato": 0,
        "bit_posizione": null,
        "stato_off": null,
        "stato_on": null,
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "QAL3: Tempo elettrov SO2",
        "tag": "TT_Q3_SO2",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "40011",
        "analogico": 1,
        "digit_singolo": 0,
        "digit_impaccato": 0,
        "bit_posizione": null,
        "stato_off": null,
        "stato_on": null,
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "SO2",
        "tag": "SO2",
        "unità_misura": "mg/Nm3",
        "modbus_id": 1,
        "modbus_registro": "40017",
        "analogico": 1,
        "digit_singolo": 0,
        "digit_impaccato": 0,
        "bit_posizione": null,
        "stato_off": null,
        "stato_on": null,
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "Temperatura fumi",
        "tag": "TF",
        "unità_misura": "°C",
        "modbus_id": 1,
        "modbus_registro": "40033",
        "analogico": 1,
        "digit_singolo": 0,
        "digit_impaccato": 0,
        "bit_posizione": null,
        "stato_off": null,
        "stato_on": null,
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "SO2",
        "tag": "SO2",
        "unità_misura": "mg/Nm3",
        "modbus_id": 1,
        "modbus_registro": "40049",
        "analogico": 1,
        "digit_singolo": 0,
        "digit_impaccato": 0,
        "bit_posizione": null,
        "stato_off": null,
        "stato_on": null,
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "Temperatura fumi",
        "tag": "TF",
        "unità_misura": "°C",
        "modbus_id": 1,
        "modbus_registro": "40065",
        "analogico": 1,
        "digit_singolo": 0,
        "digit_impaccato": 0,
        "bit_posizione": null,
        "stato_off": null,
        "stato_on": null,
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "PC life signal",
        "tag": "HB",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "0",
        "analogico": 1,
        "digit_singolo": 0,
        "digit_impaccato": 0,
        "bit_posizione": null,
        "stato_off": null,
        "stato_on": null,
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "Start autocal",
        "tag": "AUTOCAL_START",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "0",
        "analogico": 1,
        "digit_singolo": 0,
        "digit_impaccato": 0,
        "bit_posizione": null,
        "stato_off": null,
        "stato_on": null,
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "Stop autocal",
        "tag": "AUTOCAL_STOP",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "0",
        "analogico": 1,
        "digit_singolo": 0,
        "digit_impaccato": 0,
        "bit_posizione": null,
        "stato_off": null,
        "stato_on": null,
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "Ack allarmi",
        "tag": "ACK",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "0",
        "analogico": 1,
        "digit_singolo": 0,
        "digit_impaccato": 0,
        "bit_posizione": null,
        "stato_off": null,
        "stato_on": null,
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "Impianto in manutenzione",
        "tag": "PL_MAINT",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "0",
        "analogico": 1,
        "digit_singolo": 0,
        "digit_impaccato": 0,
        "bit_posizione": null,
        "stato_off": null,
        "stato_on": null,
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "Impianto fuori servizio per guasto",
        "tag": "PL_OFF",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "0",
        "analogico": 1,
        "digit_singolo": 0,
        "digit_impaccato": 0,
        "bit_posizione": null,
        "stato_off": null,
        "stato_on": null,
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "Allarme supero ultima media",
        "tag": "AVG",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "0",
        "analogico": 1,
        "digit_singolo": 0,
        "digit_impaccato": 0,
        "bit_posizione": null,
        "stato_off": null,
        "stato_on": null,
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "Allarme supero media previsionale",
        "tag": "AVG_P",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "0",
        "analogico": 1,
        "digit_singolo": 0,
        "digit_impaccato": 0,
        "bit_posizione": null,
        "stato_off": null,
        "stato_on": null,
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "Misura stimata SO2",
        "tag": "SO2_XTM",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "0",
        "analogico": 1,
        "digit_singolo": 0,
        "digit_impaccato": 0,
        "bit_posizione": null,
        "stato_off": null,
        "stato_on": null,
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      },
      {
        "nome": "Misura stimata Temperatura fumi",
        "tag": "TF_XTM",
        "unità_misura": null,
        "modbus_id": 1,
        "modbus_registro": "0",
        "analogico": 1,
        "digit_singolo": 0,
        "digit_impaccato": 0,
        "bit_posizione": null,
        "stato_off": null,
        "stato_on": null,
        "inizio_scala_elettrico": null,
        "fine_scala_elettrico": null,
        "inizio_scala_ingegneristico": null,
        "fine_scala_ingegneristico": null,
        "limite_orario": null,
        "limite_giornaliero": null
      }
    ]
  }
],


[
  {
    "_subkey": "stazione_insert",
    "_params": [
      {
        "nome_stazione": "Impianto lavorazione SO2",
        "stazione": "Impianto lavorazione SO2",
        "protocollo": "ModBus TCP",
        "ip_plc": "10.100.50.95",
        "port": 502,
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
        ]
      }
    ]
  }
],


[
  {
    "_subkey": "stazione_insert",
    "_params": [
      {
        "nome_stazione": "Sistema Analisi SO2",
        "stazione": "Sistema Analisi SO2",
        "protocollo": "ModBus TCP",
        "ip_plc": "10.100.162.90",
        "port": null,
        "var": []
      }
    ]
  }
],


[
  {
    "_subkey": "stazione_insert",
    "_params": [
      {
        "nome_stazione": "Sistema Analisi SO2",
        "stazione": "Sistema Analisi SO2",
        "protocollo": "ModBus TCP",
        "ip_plc": null,
        "port": null,
        "var": []
      }
    ]
  }
]]'''



# ---------------------------------------------------------------------------
# Main Execution Block (No user-defined functions)
# ---------------------------------------------------------------------------
try:
    # Parse input
    _parsed_json = json.loads(input_json)

    # ── Flatten nested lists (Iterative replacement for recursion) ────────
    data = []
    _stack = [_parsed_json]
    while _stack:
        _curr = _stack.pop()
        if isinstance(_curr, list):
            # Reverse to maintain original order when popping from stack
            for _item in reversed(_curr):
                _stack.append(_item)
        elif isinstance(_curr, dict):
            data.append(_curr)

    # ── 1. Split station info from measures ──────────────────────────────
    station_info  = None
    measures_raw  = []

    for item in data:
        sub = item.get("_subkey", "")
        if sub == "stazione_insert":
            station_info = item["_params"][0]
        elif sub == "misura_insert":
            measures_raw.extend(item["_params"])

    if station_info is None:
        raise ValueError("No 'stazione_insert' block found in input JSON.")

    ip   = station_info.get("ip",   "127.0.0.1")
    port = station_info.get("port", 502)

    driverconfig = (
        f'<configuration><commProto>'
        f'<p0 class="Protocollo MODBUS (master) via TCP/IP" '
        f'name="Protocollo MODBUS (master) via TCP/IP" '
        f'ipaddress="{ip}" tcpport="{port}" '
        f'timeout="5000" retries="3" write4XXXX="6"/>'
        f'</commProto><recoveryProto/></configuration>'
    )

    station_id = 1

    # ── 2. Process measures ───────────────────────────────────────────────
    new_measures      = []        
    new_bitinfo_raw   = []        

    packed_reg_to_idx = {}
    new_id_counter = 0

    for m in measures_raw:

        # ── Inline classify_measure ───────────────────────────────────────
        if m.get("analogico"):
            driverdata, type_code, is_analog, is_digital, is_packed = 0, 0, True, False, False
        elif m.get("digit_impaccato"):
            driverdata, type_code, is_analog, is_digital, is_packed = 2, 1, False, True, True
        elif m.get("digit_singolo"):
            driverdata, type_code, is_analog, is_digital, is_packed = 1, 1, False, True, False
        else:
            driverdata, type_code, is_analog, is_digital, is_packed = 0, 0, True, False, False

        # Modbus register number
        raw_reg = str(m.get("modbus_registro", "0")).strip()
        this_reg = int(raw_reg.split(".")[0]) if raw_reg and str(raw_reg).strip() != 'None' else 0
        device  = int(m.get("modbus_id", 1))
        fmt     = FLOAT_SINGLE_BE if is_analog else SIGNED_SHORT
        units   = m.get("unità_misura")
        name    = m.get("nome") or m.get("tag") or "Unknown"
        bit_no  = m.get("bit_posizione")
        stato_on  = m.get("stato_on")
        stato_off = m.get("stato_off")

        # ── 2a. Decide whether we need a new measure entry ────────────────
        if is_packed and this_reg in packed_reg_to_idx:
            measure_idx = packed_reg_to_idx[this_reg]
        else:
            new_id_counter += 1
            measure_idx = new_id_counter - 1

            display_name = "Ingresso_digitale" if is_packed else name

            # Inline blob creation (bit_no=0 initially)
            _raw_blob = (
                struct.pack("<i", this_reg)
                + struct.pack("<i", 0)
                + struct.pack("<i", 0)
                + struct.pack("<i", 0)
                + struct.pack("<i", device)
                + struct.pack("<i", fmt)
            )
            blob = "0x" + _raw_blob.hex().upper()

            new_measures.append({
                "STATIONID":        station_id,
                "NAME":             display_name[:29],
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
                "DRIVERPRIVATE":    blob,
                "ONLY_POSITIVES":   0 if is_analog else None,
                "VM_SOURCE_CODE":   VM_SOURCE_CODE_DEFAULT,
                "PERIOD":           5,
                "SNAPSIZE":         1000,
                "DRIVERCONFIG":     DRIVERCONFIG_MEASURE,
                "ID":               new_id_counter,
                "UNITS2":           units,
                "MODBUSREGISTRO":   this_reg,
                "_reg":             this_reg,
                "_device":          device,
                "_fmt":             fmt,
                "_is_digital":      is_digital,
            })

            if is_packed:
                packed_reg_to_idx[this_reg] = measure_idx

        # ── 2b. Bitinfo entry for every digital measure ───────────────────
        if is_digital:
            effective_bit = int(bit_no) if bit_no is not None else 0

            nm = new_measures[measure_idx]
            
            # Inline blob creation for specific bit
            _raw_blob2 = (
                struct.pack("<i", nm["_reg"])
                + struct.pack("<i", 0)
                + struct.pack("<i", 0)
                + struct.pack("<i", effective_bit)
                + struct.pack("<i", nm["_device"])
                + struct.pack("<i", nm["_fmt"])
            )
            nm["DRIVERPRIVATE"] = "0x" + _raw_blob2.hex().upper()

            new_bitinfo_raw.append({
                "BITNO":   effective_bit,
                "BITNAME": name.upper(),
                "TEXTON":  stato_on.upper(),
                "TEXTOFF": stato_off.upper(),
                "_reg":    this_reg,
            })

    # ── 3. Finalise measure IDs and build reg → final-ID lookup ──────────
    packed_name_counter = 0
    reg_to_final_id = {}

    for idx, nm in enumerate(new_measures):
        if "ingresso_digitale" in nm["NAME"].lower():
            packed_name_counter += 1
            nm["NAME"] = f"Ingressi digitali {packed_name_counter}"

        nm["ID"] = idx + 1
        reg_to_final_id[nm["MODBUSREGISTRO"]] = nm["ID"]

        for k in ("_reg", "_device", "_fmt", "_is_digital"):
            nm.pop(k, None)

    # ── 4. Resolve MEASUREID in bitinfo ───────────────────────────────────
    new_bitinfo = []
    for b in new_bitinfo_raw:
        reg = b.pop("_reg")
        b["MEASUREID"] = reg_to_final_id.get(reg)
        new_bitinfo.append(b)

    # ── 5. Assemble final station object ──────────────────────────────────
    result = {
        "NAME":                  station_info.get("nome", "SME"),
        "DRIVERNAME":            "modbusplc",
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
    }

    # ---------------------------------------------------------------------------
    # Output and Save Data
    # ---------------------------------------------------------------------------
    output_json = json.dumps(result, indent=2, ensure_ascii=False)

    output_path = "output_multiple_files.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    print(f"✔  JSON created successfully → {output_path}")
    print(f"   Measures : {len(result['measures'])}")
    print(f"   Bitinfo  : {len(result['bitinfo'])}")

    print("\nRegister → Measure ID mapping:")
    for m in result["measures"]:
        print(f"  reg {m['MODBUSREGISTRO']:>6}  →  ID {m['ID']:>4}  ({m['NAME']})")

except Exception as e:
    error = traceback.format_exc()
    print("ERROR:\n", error)