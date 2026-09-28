import json

agent_a = json.loads(r'''{edge}[8]''')   # measures
agent_b = json.loads(r'''{edge}[13]''')  # bitinfo

b_index = {
    (s["DRIVERCONFIG"], s["NAME"]): s
    for s in agent_b
}

merged = []

for a_station in agent_a:

    key = (a_station["DRIVERCONFIG"], a_station["NAME"])
    b_station = b_index.get(key, {})

    measures = []

    for m in a_station.get("measures", []):
        measures.append({
            k: v
            for k, v in m.items()
            if k != "_packed_rows"
        })

    merged.append({
        "NAME": a_station.get("NAME"),
        "DRIVERNAME": a_station.get("DRIVERNAME"),
        "DRIVERCONFIG": a_station.get("DRIVERCONFIG"),
        "ID": a_station.get("ID"),
        "measures": measures,
        "bitinfo": b_station.get("bitinfo", [])
    })

result = json.dumps(
    merged,
    ensure_ascii=False,
    indent=2
)

