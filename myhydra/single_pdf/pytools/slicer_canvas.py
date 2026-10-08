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
