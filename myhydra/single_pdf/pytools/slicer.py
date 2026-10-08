# Slicer Single PDF - fetta di gruppi-pagina per uno shard parallelo.
# TOPOLOGIA UNIVERSALE (una sola volta, vale per ogni documento):
#   SLICE-A: START=1,   END=10    | SLICE-B: START=11, END=20
#   SLICE-C: START=21,  END=10000 (fino a fine documento, qualunque lunghezza)
# Documenti corti: gli shard fuori portata restituiscono [] e il merger li
# salta (seriale automatico). Documenti lunghi: parallelo automatico.
# CONFIG CANVAS: solo START/END qui sopra; ricontrollare N di {edge} dopo
# ogni rewiring e togliere match-condition spurie.
# Input: array dei gruppi da MEDIA2CONTENT (oggetti {_medexkeys}, in ordine).
# Output: la stessa forma (array) con le sole posizioni [START:min(END,tot)].
# Solo errori di CONFIG (START<1, END<START) -> ERROR JSON con tb, mai blank.
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
    if START < 1 or END < START:
        raise ValueError("slicer: configurazione invalida [%d:%d]"
                         % (START, END))
    total = len(groups)
    out = []
    if START <= total:
        last = END
        if last > total:
            last = total
        out = groups[START - 1:last]
    result = json.dumps(out, ensure_ascii=False)
except Exception as error:
    tb = traceback.format_exc(limit=3).replace("\n", " | ")[:900]
    result = json.dumps({"status": "ERROR", "error": str(error),
                         "tb": tb}, ensure_ascii=False)
