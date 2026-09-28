import json
import re

# JSON in input come stringa
json_input = Edge[6]

# Eventuale correzione di virgolette interne malformate
json_input = re.sub(
    r'(?<=\w)"(?=\w)',
    r'\"',
    json_input
)

data = json.loads(json_input)

skip_words = [
    "disponibil",      # Disponibile, Disponibili
    "riserva",
    "riservato",
    "non usato",
    "non utilizzato",
    "ingresso",
    "uscita",
    "parametro",
    "libero",
    "vuoto",
    "spare",
    "reserve"
]

for station in data:

    if "measures" in station:

        station["measures"] = [
            measure
            for measure in station["measures"]
            if (
                measure.get("NAME") is not None
                and str(measure.get("NAME")).strip() != ""
                and not any(
                    word in str(measure.get("NAME")).lower()
                    for word in skip_words
                )
            )
        ]

    if "bitinfo" in station:

        station["bitinfo"] = [
            bit
            for bit in station["bitinfo"]
            if (
                bit.get("BITNAME") is not None
                and str(bit.get("BITNAME")).strip() != ""
                and not any(
                    word in str(bit.get("BITNAME")).lower()
                    for word in skip_words
                )
            )
        ]

json_output = json.dumps(
    data,
    indent=2,
    ensure_ascii=False
)

print(json_output)