import json

input_str = r'''{edge}[3]'''  # la tua stringa JSON

data = json.loads(input_str)

terms = ["Punto emissivo", "camino", "Emissione", "SAE"]

for station in data:
    name = station["NAME"]
    found = False
    for term in terms:
        if term in name:
            found = True
            break
    if not found:
        station["NAME"] = "SME"

output_str = json.dumps(data, ensure_ascii=False, indent=4)