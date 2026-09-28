import json

parsed = json.loads(r'''edge''')



# Flatten iterativo senza funzioni
stack = list(parsed)
input_json = []
while stack:
    item = stack.pop(0)
    if isinstance(item, dict):
        input_json.append(item)
    elif isinstance(item, list):
        stack = list(item) + stack

DEFAULT_IP   = "192.168.1.1"
DEFAULT_PORT = "502"

# Trova il primo DRIVERCONFIG reale
real_cfg = None
for s in input_json:
    cfg   = s.get("DRIVERCONFIG", ":")
    parts = cfg.split(":", 1)
    ip    = parts[0].strip() if len(parts) > 0 else ""
    port  = parts[1].strip() if len(parts) > 1 else ""
    
    # Verifica che 'ip' non sia vuoto, non contenga "x" e non sia quello di default
    if ip and "x" not in ip.lower() and (ip != DEFAULT_IP or port != DEFAULT_PORT):
        real_cfg = cfg
        break

# Propaga a tutte le stazioni
if real_cfg:
    for s in input_json:
        if s.get("DRIVERCONFIG") != real_cfg:
            s["DRIVERCONFIG"] = real_cfg

# Normalizza MEASUREID nei bitinfo: "40007.0" → 40007, "40004.10" → 40004
# Valori senza punto (interi o stringhe pure) rimangono invariati
for s in input_json:
    for b in s.get("bitinfo", []):
        mid = b.get("MEASUREID")
        if mid is not None:
            mid_str = str(mid)
            if "." in mid_str:
                base = mid_str.split(".")[0]
                try:
                    b["MEASUREID"] = int(base)
                except ValueError:
                    b["MEASUREID"] = base

output_json = json.dumps(input_json, ensure_ascii=False, indent=4)

with open('localoutput28page.json', 'w') as file:
    json.dump(input_json, file, ensure_ascii=False, indent=4)