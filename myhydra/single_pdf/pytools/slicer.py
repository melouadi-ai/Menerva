# Slicer Single PDF - fetta di gruppi-pagina per uno shard parallelo.
# CONFIG CANVAS: START/END sono 1-based e inclusi. Ogni shard ha la sua
# copia con solo questi due numeri diversi; ricontrollare N di {edge}
# dopo ogni rewiring e togliere match-condition spurie.
# Input: array dei gruppi da MEDIA2CONTENT (oggetti {_medexkeys}, in ordine).
# Output: la stessa forma (array) con le sole posizioni [START:END].
# Errori (range impossibile, input non lista) -> ERROR JSON con tb, mai blank.
import json
import traceback
raw = r'''{edge}[6]'''
START = 1
END = 10
try:
    groups = raw
    if isinstance(groups, str):
        groups = json.loads(groups.strip())
    if not isinstance(groups, list):
        raise ValueError("slicer: input non interpretabile come lista di gruppi")
    total = len(groups)
    if not (1 <= START <= END <= total):
        raise ValueError("slicer: fetta [%d:%d] fuori dai %d gruppi"
                         % (START, END, total))
    out = groups[START - 1:END]
    result = json.dumps(out, ensure_ascii=False)
except Exception as error:
    tb = traceback.format_exc(limit=3).replace("\n", " | ")[:900]
    result = json.dumps({"status": "ERROR", "error": str(error),
                         "tb": tb}, ensure_ascii=False)
