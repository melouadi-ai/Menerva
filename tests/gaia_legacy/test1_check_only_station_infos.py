import json

input_json = r''' [[
    {
        "nome_stazione": "SME",
        "stazione": "Sistema Analisi SO2",
        "protocollo": "ModBus TCP",
        "ip_plc": "10.100.50.95",
        "port": 511,
        "var": [],
        "STATION_INFORMATIONS": false
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
        "STATION_INFORMATIONS": false
    }
],
[],
[
    {
        "nome_stazione": "SME",
        "stazione": "Sistema Analisi SO2",
        "protocollo": "ModBus TCP",
        "ip_plc": "10.100.162.90",
        "port": null,
        "var": [],
        "STATION_INFORMATIONS": false
    }
],
[
    {
        "nome_stazione": "SME",
        "stazione": "Sistema Analisi SO2",
        "protocollo": "ModBus TCP",
        "ip_plc": "10.100.162.90",
        "port": null,
        "var": [],
        "STATION_INFORMATIONS": false
    }
],
[],
[],
[],
[]] '''

input_json = json.loads(input_json)

if isinstance(input_json, list):
    # Creiamo una lista escludendo i vettori vuoti []
    stazioni_popolate = [station for station in input_json if station]
    
    # Verifichiamo che TUTTE quelle rimaste abbiano STATION_INFORMATIONS a True
    if stazioni_popolate and all(s[0].get('STATION_INFORMATIONS') for s in stazioni_popolate):
        print('All of them are station informations!')
        output = 'ERRORE: tutte le stazioni contengono solo informazioni sulla stazione'
    elif stazioni_popolate and not all(s[0].get('STATION_INFORMATIONS') for s in stazioni_popolate):
        print('All of them are measure informations! ')
        output = 'ERRORE: tutte le stazioni contengono solo misure'
    elif stazioni_popolate:
        output = json.dumps(stazioni_popolate, indent=4, ensure_ascii=False)
    else:
        output = 'ERRORE: Nessun formato riconosciuto'    