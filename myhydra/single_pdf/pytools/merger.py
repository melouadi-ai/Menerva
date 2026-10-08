# Merger Single PDF - concatena i chunk di 2 shard in ordine (A poi B).
# CONFIG CANVAS: ricontrollare N dei due {edge} dopo ogni rewiring e togliere
# match-condition spurie. Per 3 shard usare due merger in cascata (AB, poi ABC).
# Input: output grezzi dei motori (stringhe con fence ```json, array o dict).
# Output: array unico dei blocchi (A+B), pronto per il CONSOLIDATORE che li
# raggruppa in pagine in ordine di arrivo. page_no non serve qui.
# Shard vuoto -> ERROR JSON con tb (mai silenzio, mai blank).
import json
import traceback
raw_a = r'''{edge}[7]'''
raw_b = r'''{edge}[8]'''
try:
    raws = [raw_a, raw_b]
    names = ["A", "B"]
    all_blocks = []
    si = 0
    while si < 2:
        found = []
        queue = [raws[si]]
        while len(queue) > 0:
            item = queue.pop(0)
            if isinstance(item, str):
                ss = item.strip()
                dec = json.JSONDecoder()
                pos = 0
                n = len(ss)
                while pos < n:
                    while pos < n and ss[pos] in " \n\r\t,;":
                        pos = pos + 1
                    if pos >= n:
                        break
                    if ss[pos] != "{" and ss[pos] != "[":
                        n1 = ss.find("{", pos)
                        n2 = ss.find("[", pos)
                        cand = -1
                        if n1 >= 0 and n2 >= 0:
                            if n1 < n2:
                                cand = n1
                            else:
                                cand = n2
                        elif n1 >= 0:
                            cand = n1
                        elif n2 >= 0:
                            cand = n2
                        if cand < 0:
                            break
                        pos = cand
                        continue
                    try:
                        obj, end = dec.raw_decode(ss, pos)
                        queue.append(obj)
                        pos = end
                    except Exception:
                        n1 = ss.find("{", pos + 1)
                        n2 = ss.find("[", pos + 1)
                        cand = -1
                        if n1 >= 0 and n2 >= 0:
                            if n1 < n2:
                                cand = n1
                            else:
                                cand = n2
                        elif n1 >= 0:
                            cand = n1
                        elif n2 >= 0:
                            cand = n2
                        if cand < 0:
                            break
                        pos = cand
            elif isinstance(item, list):
                queue = list(item) + queue
            elif isinstance(item, dict):
                found.append(item)
            elif item is not None:
                found.append(item)
        if len(found) == 0:
            raise ValueError("merger: shard " + names[si] + " vuoto o illeggibile")
        all_blocks = all_blocks + found
        si = si + 1
    result = json.dumps(all_blocks, ensure_ascii=False)
except Exception as error:
    tb = traceback.format_exc(limit=3).replace("\n", " | ")[:900]
    result = json.dumps({"status": "ERROR", "error": str(error),
                         "tb": tb}, ensure_ascii=False)
