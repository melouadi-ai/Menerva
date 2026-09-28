import json

input_json = r'''{edge}[14]'''

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
            new_m["ID"] = m["ID"]
            merged_measures.append(new_m)

        # Ricalcola i MEASUREID nei bitinfo in modo coerente con gli ID misura
        for b in group_bitinfo:
            new_b = dict(b)
            new_b["MEASUREID"] = b["MEASUREID"]
            merged_bitinfo.append(new_b)

        if group_measures:
            measure_id_offset += max(m["ID"] for m in group_measures)

# --- Passaggio 3: assembla l'output ---
base_station["measures"] = merged_measures
base_station["bitinfo"]  = merged_bitinfo

output = json.dumps([base_station], indent=4, ensure_ascii=False)
print(output)
# with open('testmeasures.json', 'w') as file:
#     json.dump([base_station], file, indent=4, ensure_ascii=False)