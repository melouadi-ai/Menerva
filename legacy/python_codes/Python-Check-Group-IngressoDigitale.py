from collections import Counter
import json

input_json = r'''{edge}[6]'''

final_result_json = json.loads(input_json)

for station in final_result_json:
    measures = station.get("measures", [])

    # STEP 1 — Normalizza MODBUSREGISTRO: "40001.3" → 40001, "00033" rimane "00033"
    for m in measures:
        reg = m.get("MODBUSREGISTRO")
        if isinstance(reg, str) and "." in reg:
            base = reg.split(".")[0]
            try:
                m["MODBUSREGISTRO"] = int(base)
            except ValueError:
                m["MODBUSREGISTRO"] = base

    # STEP 2 — Trova registri che appaiono più di una volta
    reg_counts = Counter(
        m["MODBUSREGISTRO"]
        for m in measures
        if m.get("MODBUSREGISTRO") is not None
    )
    shared_regs = {reg for reg, count in reg_counts.items() if count > 1}

    # STEP 3 — Assegna GROUP a tutte le misure con registro condiviso
    for m in measures:
        if m.get("MODBUSREGISTRO") in shared_regs:
            m["GROUP"] = "Ingresso_digitale"

    # STEP 4 — Rimuovi GROUP dalle misure con registro NON condiviso (unico)
    for m in measures:
        if "GROUP" in m and m.get("MODBUSREGISTRO") not in shared_regs:
            del m["GROUP"]

final_result = json.dumps(final_result_json, indent=2, ensure_ascii=False)