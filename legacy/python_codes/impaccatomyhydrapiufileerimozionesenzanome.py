import json
import struct
import traceback
import re
 
# Modificato la parte di apici nel DRIVERCONFIG per parlo funzionare correttamente, ora il tag HTML e' dentro apici singoli ('tag')
input_json = r'''[
    {
        "NAME": "SME",
        "DRIVERNAME": "modbusplc",
        "DRIVERCONFIG": "192.168.1.50:502",
        "ID": 1,
        "measures": [
            {
                "NAME": "COMANDO ACK RESET",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 1,
                "MODBUSREGISTRO": 40001,
                "GROUP": "Ingresso_digitale"
            },
            {
                "NAME": "SELEZIONE CALIBRAZ/VERIFI",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 1,
                "MODBUSREGISTRO": 40003,
                "GROUP": "Ingresso_digitale"
            },
            {
                "NAME": "Watchdog Comunicaz.",
                "UNITS": null,
                "DRIVERDATA": 0,
                "TYPE": 0,
                "ID": 1,
                "MODBUSREGISTRO": 40008
            },
            {
                "NAME": "Watchdog_DA SME Server 01",
                "UNITS": null,
                "DRIVERDATA": 0,
                "TYPE": 0,
                "ID": 1,
                "MODBUSREGISTRO": 40009
            },
            {
                "NAME": "Watchdog_DA SME Server 02",
                "UNITS": null,
                "DRIVERDATA": 0,
                "TYPE": 0,
                "ID": 1,
                "MODBUSREGISTRO": 40010
            },
            {
                "NAME": "Fault Comm PC SME",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 1,
                "MODBUSREGISTRO": 40011,
                "GROUP": "Ingresso_digitale"
            },
            {
                "NAME": "COG2: Fault analogica MIS",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 1,
                "MODBUSREGISTRO": 40012,
                "GROUP": "Ingresso_digitale"
            },
            {
                "NAME": "All. Sitop Select 24Vdc",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 1,
                "MODBUSREGISTRO": 40013,
                "GROUP": "Ingresso_digitale"
            },
            {
                "NAME": "All. Temp. Sonda Prelievo",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 1,
                "MODBUSREGISTRO": 40014,
                "GROUP": "Ingresso_digitale"
            },
            {
                "NAME": "All. Temp. Sonda Prelievo",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 1,
                "MODBUSREGISTRO": 40016,
                "GROUP": "Ingresso_digitale"
            },
            {
                "NAME": "COG3: All. Comm. Anal. U2",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 1,
                "MODBUSREGISTRO": 40017,
                "GROUP": "Ingresso_digitale"
            },
            {
                "NAME": "ABILIT.MEMORIZZAZIONE DAT",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 1,
                "MODBUSREGISTRO": 40021,
                "GROUP": "Ingresso_digitale"
            },
            {
                "NAME": "COG2: MISURA Anal..U23 CO",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 1,
                "MODBUSREGISTRO": 40022,
                "GROUP": "Ingresso_digitale"
            },
            {
                "NAME": "Sel Inser. Pompa P1",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 1,
                "MODBUSREGISTRO": 40023,
                "GROUP": "Ingresso_digitale"
            },
            {
                "NAME": "COG3: MISURA Anal..U23 CO",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 1,
                "MODBUSREGISTRO": 40024,
                "GROUP": "Ingresso_digitale"
            },
            {
                "NAME": "Sel Inser. Pompa P1",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 1,
                "MODBUSREGISTRO": 40025,
                "GROUP": "Ingresso_digitale"
            },
            {
                "NAME": "COG2: Validita MISURA PRE",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 1,
                "MODBUSREGISTRO": 40028,
                "GROUP": "Ingresso_digitale"
            },
            {
                "NAME": "All. Sitop Select 24Vdc",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 1,
                "MODBUSREGISTRO": 40031,
                "GROUP": "Ingresso_digitale"
            },
            {
                "NAME": "All. Alta Temp. Quadro Analisi",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 1,
                "MODBUSREGISTRO": 40032,
                "GROUP": "Ingresso_digitale"
            },
            {
                "NAME": "BL1: COM SSR RISCALDAMENT",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 1,
                "MODBUSREGISTRO": 40041,
                "GROUP": "Ingresso_digitale"
            },
            {
                "NAME": "BL2: COM SSR RISCALDAMENT",
                "UNITS": null,
                "DRIVERDATA": 2,
                "TYPE": 1,
                "ID": 1,
                "MODBUSREGISTRO": 40042,
                "GROUP": "Ingresso_digitale"
            },
            {
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
                "NAME": "Contatore Funz. Cartuccia",
                "UNITS": "h",
                "DRIVERDATA": 0,
                "TYPE": 0,
                "ID": 1,
                "MODBUSREGISTRO": 40175,
                "STARTSCALE_ENG": 0,
                "ENDSCALE_ENG": 0
            }
        ],
        "bitinfo": [
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
        ]
    },
    {
        "NAME": "SME",
        "DRIVERNAME": "modbusplc",
        "DRIVERCONFIG": "xxx.xxx.xxx.xxx:",
        "ID": 2,
        "measures": [],
        "bitinfo": []
    }
]'''

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
    
    with open('outputlocaljson.json', 'w', encoding='utf-8') as f:
        json.dump(result,f, indent=4, ensure_ascii=False)

    print("Json creato correttamente")        


    for k,v in new_measure_id_dict.items():
      print(k,v)
    
except Exception as e:
    error_msg = traceback.format_exc()
    error_report = [{
        "err":             str(e),
        "trace":           error_msg
    }]
    output_json = json.dumps(error_report, indent=2, ensure_ascii=False)
    print(output_json)