import json

base = json.loads(r''' {edge}[11] ''') # General
states = json.loads(r''' {edge}[12] ''') # TEXTON/OFF

state_index = {}

for station in states:
    for bit in station.get("bitinfo", []):
        key = (
            bit["MEASUREID"],
            bit["BITNO"]
        )

        state_index[key] = (
            bit.get("TEXTON"),
            bit.get("TEXTOFF")
        )

for station in base:
    for bit in station.get("bitinfo", []):

        key = (
            bit["MEASUREID"],
            bit["BITNO"]
        )

        if key in state_index:
            bit["TEXTON"] = state_index[key][0]
            bit["TEXTOFF"] = state_index[key][1]

result = json.dumps(
        base,
        ensure_ascii=False,
        indent=2
    )