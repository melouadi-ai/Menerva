import json
import re

json_input = r''' {edge}[9] '''

# Flatten iterativo (gestisce [], [[]], ecc.)
stack = list(json.loads(json_input))
data = []
while stack:
    item = stack.pop(0)
    if isinstance(item, dict):
        data.append(item)
    elif isinstance(item, list):
        stack = list(item) + stack

skip_words = [
    "disponibil",
    "riserva",
    "riservato",
    "non usato",
    "non utilizzato",
    "ingresso",
    "uscita",
    "parametro",
    "libero",
    "liberi",
    "int16",
    "vuoto",
    "spare",
    "reserve",
    "range"
]

for station in data:
    if "measures" in station:
        station["measures"] = [
            m for m in station["measures"]
            if (
                m.get("NAME") is not None
                and str(m.get("NAME")).strip() != ""
                and not any(word in str(m.get("NAME")).lower() for word in skip_words)
            )
        ]
    if "bitinfo" in station:
        station["bitinfo"] = [
            b for b in station["bitinfo"]
            if (
                b.get("BITNAME") is not None
                and str(b.get("BITNAME")).strip() != ""
                and not any(word in str(b.get("BITNAME")).lower() for word in skip_words)
            )
        ]

json_output = json.dumps(data, indent=2, ensure_ascii=False)