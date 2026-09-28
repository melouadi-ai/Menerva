from collections import Counter, defaultdict
import json

input_json = r''' {edge}[12] '''
final_result_json = json.loads(input_json)

# STEP 1 — Normalizza MODBUSREGISTRO
for station in final_result_json:
    for m in station.get("measures", []):
        reg = m.get("MODBUSREGISTRO")
        if isinstance(reg, str) and "." in reg:
            base = reg.split(".")[0]
            try:
                m["MODBUSREGISTRO"] = int(base)
            except ValueError:
                m["MODBUSREGISTRO"] = base

# STEP 2 — Mappa registro → set di station_id (analisi cross-stazione)
reg_to_stations = defaultdict(set)
for station in final_result_json:
    station_id = station.get("ID") or station.get("id") or id(station)
    for m in station.get("measures", []):
        reg = m.get("MODBUSREGISTRO")
        if reg is not None:
            reg_to_stations[reg].add(station_id)

cross_station_regs = {
    reg for reg, stations in reg_to_stations.items() if len(stations) > 1
}

# STEP 3 — Assegna GROUP solo se:
#   - TYPE == 6 (ingresso digitale)
#   - registro condiviso NELLA stessa stazione
#   - registro NON condiviso cross-stazione
for station in final_result_json:
    measures = station.get("measures", [])

    # Conta solo tra le misure TYPE=6
    reg_counts = Counter(
        m["MODBUSREGISTRO"]
        for m in measures
        if m.get("MODBUSREGISTRO") is not None and m.get("TYPE") == 6
    )

    shared_regs = {
        reg for reg, count in reg_counts.items()
        if count > 1 and reg not in cross_station_regs
    }

    for m in measures:
        reg = m.get("MODBUSREGISTRO")
        if reg in shared_regs and m.get("TYPE") == 6:
            m["GROUP"] = "Ingresso_digitale"
        elif "GROUP" in m:
            del m["GROUP"]

final_result = json.dumps(final_result_json, indent=2, ensure_ascii=False)