import json
import traceback
raw_u = r'''{edge}[2]'''
raw_o = r'''{edge}[5]'''
try:
 categorie = ("mancanti", "unita_inventate", "junk_stati", "refusi_corretti", "ip_dichiarati_non_usati")
 assemble_warnings = []
 page = raw_u
 if isinstance(page, str):
  testo = page.strip()
  if testo.startswith("```"):
   taglio = testo.find("\n")
   if taglio >= 0:
    testo = testo[taglio + 1:]
   if testo.rstrip().endswith("```"):
    testo = testo.rstrip()[:-3]
   testo = testo.strip()
  page = json.loads(testo)
 if isinstance(page, list):
  scelto = None
  ui = 0
  while ui < len(page):
   candidato = page[ui]
   if (isinstance(candidato, dict) and isinstance(candidato.get("stations"), list)):
    scelto = candidato
    break
   ui = ui + 1
  page = scelto
 if not isinstance(page, dict) or not isinstance(page.get("stations"), list):
  raise ValueError("page_assembler: UNIFIED senza stations")
 page_no = page.get("page_no")
 ora = raw_o
 if isinstance(ora, str):
  try:
   testo = ora.strip()
   if testo.startswith("```"):
    taglio = testo.find("\n")
    if taglio >= 0:
     testo = testo[taglio + 1:]
    if testo.rstrip().endswith("```"):
     testo = testo.rstrip()[:-3]
    testo = testo.strip()
   ora = json.loads(testo)
  except Exception as errore_ora:
   assemble_warnings.append("oracolo_non_interpretabile: " + str(errore_ora)[:200])
   ora = None
 if isinstance(ora, list):
  scelto = None
  oi = 0
  while oi < len(ora):
   candidato = ora[oi]
   if isinstance(candidato, dict):
    ci = 0
    while ci < len(categorie):
     if isinstance(candidato.get(categorie[ci]), list):
      scelto = candidato
      break
     ci = ci + 1
    if scelto is not None:
     break
   oi = oi + 1
  ora = scelto
 verifica = None
 if isinstance(ora, dict):
  risposto = False
  ci = 0
  while ci < len(categorie):
   if isinstance(ora.get(categorie[ci]), list):
    risposto = True
   ci = ci + 1
  errore_input = ora.get("errore_input")
  if isinstance(errore_input, str) and errore_input.strip():
   assemble_warnings.append("oracolo_input_assente: " + errore_input.strip())
   risposto = True
  if risposto:
   verifica = {"page_no": ora.get("page_no")}
   ci = 0
   while ci < len(categorie):
    nome = categorie[ci]
    if isinstance(ora.get(nome), list):
     verifica[nome] = ora[nome]
    else:
     verifica[nome] = []
    ci = ci + 1
   if (not isinstance(page_no, int) and isinstance(verifica["page_no"], int)):
    page_no = verifica["page_no"]
   verifica["page_no"] = page_no
  else:
   assemble_warnings.append("oracolo_assente: nessuna categoria " "nell'output del secondo VLM")
 else:
  assemble_warnings.append("oracolo_assente: output non interpretabile")
 out = {"page_no": page_no, "stations": page["stations"], "verifica": verifica, "assemble_warnings": assemble_warnings}
 result = json.dumps(out, ensure_ascii=False)
except Exception as error:
 tb = traceback.format_exc(limit=3).replace("\n", " | ")[:900]
 result = json.dumps({"status": "ERROR", "error": str(error), "tb": tb, "page_no": None, "stations": [], "verifica": None, "assemble_warnings": []}, ensure_ascii=False)
