import json
import re

json_input = r'''{edge}[7]'''

# Flatten iterativo
stack = list(json.loads(json_input))
data = []
while stack:
    item = stack.pop(0)
    if isinstance(item, dict):
        data.append(item)
    elif isinstance(item, list):
        stack = list(item) + stack

# Lista 1: confronto ESATTO — scarta se il nome coincide perfettamente
exact_skip = [
    "range"
]

# Lista 2: confronto per CONTENIMENTO — scarta se il nome CONTIENE una di queste parole
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
    "reserve"   
]

# Lista 3: parole da RIMUOVERE dal testo interno del nome
remove_words = ['misure', 'misura', 'miura', 'analizzatore', 'analizzatori', 'parametro', 'parametri']

# Pattern costruito con while, senza funzioni dentro join
pattern = ""
i = 0
while i < len(remove_words):
    if i > 0:
        pattern += "|"
    pattern += remove_words[i]
    i += 1

pattern = r"\b(" + pattern + r")\b\s*"

for station in data:

    if "measures" in station:
        station["measures"] = [
            m for m in station["measures"]
            if (
                m.get("NAME") is not None
                and str(m.get("NAME")).strip() != ""
                # Lista 1: esatto
                and str(m.get("NAME")).lower().strip() not in exact_skip
                # Lista 2: contenimento
                and not any(word in str(m.get("NAME")).lower() for word in skip_words)
            )
        ]
        for m in station["measures"]:
            m["NAME"] = re.sub(pattern, "", str(m["NAME"]), flags=re.IGNORECASE).strip()
            m["NAME"] = re.sub(r"\s+", " ", m["NAME"])

    if "bitinfo" in station:
        station["bitinfo"] = [
            b for b in station["bitinfo"]
            if (
                b.get("BITNAME") is not None
                and str(b.get("BITNAME")).strip() != ""
                # Lista 1: esatto
                and str(b.get("BITNAME")).lower().strip() not in exact_skip
                # Lista 2: contenimento
                and not any(word in str(b.get("BITNAME")).lower() for word in skip_words)
            )
        ]

json_output = json.dumps(data, indent=2, ensure_ascii=False)
print(json_output)