import json

input_json = r''' [ [{ "_medexkeys": "{ \"key\": \"DJRB7ETEWK\\\/b88806bf-38c3-4f0c-9b76-6950b0c8d287\" }" },

{
  "pages": [
    {
      "index": 0,
      "label": "STATION_INFORMATION"
    }
  ]
}] ]  '''

TARGET_LABEL = "STATION_INFORMATION"

# Provo prima un parsing diretto; se fallisce (es. arrivano due oggetti
# "nudi" separati da virgola, senza parentesi quadre esterne), li
# incapsulo io stesso in una lista e riprovo
try:
    data = json.loads(input_json)
except json.JSONDecodeError:
    data = json.loads("[" + input_json + "]")

# Normalizzo la struttura esterna: a volte arriva come [dict_medexkeys, dict_pages],
# altre volte incapsulata in un livello di lista in piu': [[dict_medexkeys, dict_pages]]
if len(data) == 1 and isinstance(data[0], list):
    data = data[0]

keys_raw = data[0]["_medexkeys"]

# Se _medexkeys e' arrivata come stringa JSON (doppiamente serializzata), la decodifico
if isinstance(keys_raw, str):
    keys_raw = json.loads(keys_raw)

# Normalizzo: se non e' una lista, la trasformo in lista con un solo elemento
if isinstance(keys_raw, list):
    keys_list = keys_raw
else:
    keys_list = [keys_raw]

pages = data[1]["pages"]

# Per ogni pagina con label target, prendo la chiave corrispondente
# usando "index" come posizione dentro keys_list
filtered_keys = []
i = 0
while i < len(pages):
    if pages[i]["label"] == TARGET_LABEL:
        page_index = pages[i]["index"]
        if page_index < len(keys_list):
            filtered_keys.append({"key": keys_list[page_index]["key"]})
    i = i + 1

result = json.dumps(filtered_keys[0], indent=2)

print(result)