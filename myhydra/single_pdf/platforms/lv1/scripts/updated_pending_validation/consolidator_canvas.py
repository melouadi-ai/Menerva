import json
import traceback
xdigits = str.maketrans("", "", "0123456789")
raw = r'''{edge}[6]'''
try:
 blocks = []
 queue = [raw]
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
      cand = min(n1, n2)
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
      cand = min(n1, n2)
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
   blocks.append(item)
  elif item is not None:
   blocks.append(item)
 if len(blocks) == 0 and isinstance(raw, str) and raw.strip() != "":
  raise ValueError("input non JSON")
 warnings = []
 counters = {}
 counters["pagine"] = 0
 counters["variabili"] = 0
 counters["scarti_V2"] = 0
 counters["scarti_V20"] = 0
 counters["scarti_V21"] = 0
 counters["scale_collegate"] = 0
 counters["registri_applicati"] = 0
 counters["packed_fold"] = 0
 counters["riga_mismatch"] = 0
 counters["buchi_sequenza"] = 0
 counters["duplicati"] = 0
 pages = []
 current = None
 bi = 0
 while bi < len(blocks):
  block = blocks[bi]
  bi = bi + 1
  if not isinstance(block, dict):
   raise ValueError("blocco non valido: " + str(block)[:120])
  is_envelope = False
  if isinstance(block.get("stations"), list):
   if type(block.get("page_no")) is int:
    is_envelope = True
   elif block.get("bitnames") is not None:
    is_envelope = True
   elif block.get("bitstates") is not None:
    is_envelope = True
  if type(block.get("page_no")) is int and not isinstance(block.get("stations"), list) and block.get("rows") is None:
   is_envelope = True
  if is_envelope:
   pages.append(block)
   current = None
   continue
  if isinstance(block.get("stations"), list):
   current = {"stations": block["stations"], "bitnames": None, "bitstates": None}
   pages.append(current)
   continue
  rows = block.get("rows")
  fragment = False
  if rows is None:
   if ("description" in block or "modbus_register" in block or "bit" in block or "state_on" in block or "state_off" in block):
    rows = [block]
    fragment = True
  if not isinstance(rows, list):
   bkeys = sorted(block.keys())
   btypes = []
   for bk in bkeys:
    btn = type(block[bk]).__name__
    if btn not in btypes:
     btypes.append(btn)
   btypes = sorted(btypes)
   raise ValueError("blocco " + str(bi) + " senza stations ne rows: chiavi " + str(bkeys) + " tipi {" + ", ".join(btypes) + "}")
  dict_n = 0
  is_names = False
  is_states = False
  ri = 0
  while ri < len(rows):
   rk = rows[ri]
   ri = ri + 1
   if not isinstance(rk, dict):
    continue
   dict_n = dict_n + 1
   if "description" in rk or "modbus_register" in rk or "bit" in rk:
    is_names = True
   if "state_on" in rk or "state_off" in rk:
    is_states = True
  if dict_n == 0:
   counters["blocco_rows_vuoto"] = counters.get("blocco_rows_vuoto", 0) + 1
   continue
  if current is None:
   current = {"stations": [], "bitnames": None, "bitstates": None}
   pages.append(current)
   warnings.append({"rule": "righe_senza_misure", "page_no": None, "riga": None, "detail": str(dict_n) + " righe orfane"})
   counters["righe_senza_misure"] = counters.get("righe_senza_misure", 0) + 1
  if is_states:
   state_rows = []
   name_rows = []
   ri = 0
   while ri < len(rows):
    rk = rows[ri]
    ri = ri + 1
    if not isinstance(rk, dict):
     continue
    if "state_on" in rk or "state_off" in rk:
     state_rows.append(rk)
    else:
     name_rows.append(rk)
   if name_rows:
    warnings.append({"rule": "ramo_misto", "page_no": None, "riga": None, "detail": "split " + str(len(state_rows)) + "+" + str(len(name_rows))})
    counters["ramo_misto"] = counters.get("ramo_misto", 0) + 1
    if fragment:
     ex = current.get("bitnames")
     if isinstance(ex, dict) and isinstance(ex.get("rows"), list):
      ex["rows"] = ex["rows"] + name_rows
     else:
      current["bitnames"] = {"rows": name_rows}
    else:
     current["bitnames"] = {"rows": name_rows}
   if fragment:
    ex = current.get("bitstates")
    if isinstance(ex, dict) and isinstance(ex.get("rows"), list):
     ex["rows"] = ex["rows"] + state_rows
    else:
     current["bitstates"] = {"rows": state_rows}
   else:
    current["bitstates"] = {"rows": state_rows}
  elif is_names:
   bslot = "bitnames"
   if fragment:
    ex = current.get(bslot)
    if isinstance(ex, dict) and isinstance(ex.get("rows"), list):
     ex["rows"] = ex["rows"] + rows
    else:
     current[bslot] = {"rows": rows}
   else:
    current[bslot] = {"rows": rows}
  else:
   keys_seen = []
   for r in rows:
    if not isinstance(r, dict):
     continue
    for k in r:
     if k not in keys_seen:
      keys_seen.append(k)
   raise ValueError("blocco rows non riconoscibile " + str(bi) + ": chiavi " + str(sorted(keys_seen)))
 if counters.get("blocco_rows_vuoto"):
  warnings.append({"rule": "blocco_rows_vuoto", "page_no": None, "riga": None, "detail": str(counters["blocco_rows_vuoto"]) + " rows vuoti"})
 if not isinstance(pages, list):
  raise ValueError("attendo lista pagine.")
 v2_spare = ("disponibile", "disponibile/", "disponible", "riserva", "spare", "reserve", "non utilizzato", "non utilizzata", "non usato", "libero", "---")
 v2_headers = ("misure", "comandi", "impostazioni", "input", "output", "parametri", "registri", "segnali", "variabili", "allarmi", "stati")
 v20_phrases = ("no pc sme", "no sme", "not used", "non utilizzato")
 note_keys = ("note", "nota", "notes", "annotation", "annotazione", "comment", "commento", "trailing_note")
 norm = []
 pi = 0
 while pi < len(pages):
  pg = pages[pi]
  if isinstance(pg, str):
   pg = json.loads(pg)
   while isinstance(pg, str):
    pg = json.loads(pg)
  if not isinstance(pg, dict):
   raise ValueError("Pagina non valida in posizione " + str(pi) + ".")
  if (type(pg.get("page_no")) is not int and not isinstance(pg.get("stations"), list)):
   raise ValueError("Pagina in posizione " + str(pi) + " senza page_no ne stations.")
  norm.append([pi, pg])
  pi = pi + 1
 numbered = []
 unnumbered = []
 ni = 0
 while ni < len(norm):
  pos = norm[ni][0]
  pg = norm[ni][1]
  pn = pg.get("page_no")
  if type(pn) is int:
   numbered.append([pn, pos, pg])
  else:
   unnumbered.append([pos, pg])
  ni = ni + 1
 numbered = sorted(numbered)
 ordered = []
 oi = 0
 while oi < len(numbered):
  ordered.append([numbered[oi][0], numbered[oi][2]])
  oi = oi + 1
 ui = 0
 while ui < len(unnumbered):
  warnings.append({"rule": "pagina_senza_numero", "page_no": None, "riga": None, "detail": "pagina " + str(unnumbered[ui][0])})
  ordered.append([None, unnumbered[ui][1]])
  ui = ui + 1
 seen_pn = []
 bi = 0
 while bi < len(numbered):
  pn = numbered[bi][0]
  if pn not in seen_pn:
   seen_pn.append(pn)
  bi = bi + 1
 if seen_pn:
  mn = min(seen_pn)
  mx = max(seen_pn)
  missing = []
  cand = mn
  while cand <= mx:
   if cand not in seen_pn:
    missing.append(cand)
   cand = cand + 1
  if missing:
   parts = []
   qi = 0
   while qi < len(missing):
    parts.append(str(missing[qi]))
    qi = qi + 1
   warnings.append({"rule": "sequenza_buchi", "page_no": None, "riga": None, "detail": "page_no mancanti: " + ", ".join(parts)})
   counters["buchi_sequenza"] = counters["buchi_sequenza"] + 1
 acc = {}
 acc_order = []
 v14_fields = ("description", "units", "modbus_register", "bit", "data_type", "kind", "read_write", "note", "state_on", "state_off", "scale_elec_start", "scale_elec_end", "scale_eng_start", "scale_eng_end", "limit_hour", "limit_day", "zona", "tag", "pagina", "riga")
 fill_fields = ("units", "scale_elec_start", "scale_elec_end", "scale_eng_start", "scale_eng_end", "limit_hour", "limit_day")
 meta_keys = ("name", "protocol", "ip", "port", "modbus_id")
 oi = 0
 while oi < len(ordered):
  page_no = ordered[oi][0]
  page = ordered[oi][1]
  counters["pagine"] = counters["pagine"] + 1
  stations = page.get("stations")
  if not isinstance(stations, list):
   stations = []
  bitnames = page.get("bitnames")
  bitstates = page.get("bitstates")
  has_names = isinstance(bitnames, dict) or isinstance(bitnames, list)
  has_states = isinstance(bitstates, dict) or isinstance(bitstates, list)
  if isinstance(bitnames, dict):
   names_in = bitnames.get("rows")
  else:
   names_in = bitnames
  if not isinstance(names_in, list):
   names_in = []
  if isinstance(bitstates, dict):
   states_in = bitstates.get("rows")
  else:
   states_in = bitstates
  if not isinstance(states_in, list):
   states_in = []
  nbmr = {}
  ni = 0
  while ni < len(names_in):
   nr = names_in[ni]
   ni = ni + 1
   if not isinstance(nr, dict):
    continue
   riga = nr.get("riga")
   if type(riga) is int and riga not in nbmr and nr.get("description"):
    nbmr[riga] = nr
  names_by_desc = {}
  names_desc_dup = {}
  ni = 0
  while ni < len(names_in):
   nr = names_in[ni]
   ni = ni + 1
   if not isinstance(nr, dict):
    continue
   nd = nr.get("description", None)
   if nd is None:
    continue
   if nd in names_by_desc:
    names_desc_dup[nd] = True
   else:
    names_by_desc[nd] = nr
  states_by_riga = {}
  sdup = {}
  ti = 0
  while ti < len(states_in):
   sr = states_in[ti]
   ti = ti + 1
   if not isinstance(sr, dict):
    continue
   riga = sr.get("riga")
   if type(riga) is int:
    if riga not in states_by_riga:
     states_by_riga[riga] = sr
    if riga in sdup:
     sdup[riga].append(sr)
    else:
     sdup[riga] = [sr]
  raw_total = 0
  rti = 0
  while rti < len(stations):
   rslot = stations[rti]
   rti = rti + 1
   if not isinstance(rslot, dict):
    continue
   rvars = rslot.get("variables")
   if isinstance(rvars, list):
    raw_total = raw_total + len(rvars)
  ndi = 0
  rti = 0
  while rti < len(names_in):
   if isinstance(names_in[rti], dict):
    ndi = ndi + 1
   rti = rti + 1
  sdi = 0
  rti = 0
  while rti < len(states_in):
   if isinstance(states_in[rti], dict):
    sdi = sdi + 1
   rti = rti + 1
  if raw_total == 0 and ndi == 0 and sdi == 0:
   warnings.append({"rule": "pagina_vuota_sospetta", "page_no": page_no, "riga": None, "detail": "pagina vuota: immagine assente?"})
   counters["pagina_vuota_sospetta"] = counters.get("pagina_vuota_sospetta", 0) + 1
  sti = 0
  while sti < len(stations):
   station = stations[sti]
   sti = sti + 1
   if not isinstance(station, dict):
    continue
   raws = station.get("variables")
   if not isinstance(raws, list):
    raws = []
   mrge = []
   ri = 0
   while ri < len(raws):
    raw = raws[ri]
    ri = ri + 1
    if not isinstance(raw, dict):
     continue
    riga = raw.get("riga")
    if type(riga) is int and riga not in mrge:
     mrge.append(riga)
   digr = set()
   badregs = set()
   regbits = {}
   ri2 = 0
   while ri2 < len(raws):
    rraw = raws[ri2]
    ri2 = ri2 + 1
    if not isinstance(rraw, dict):
     continue
    rriga = rraw.get("riga")
    if type(rriga) is not int:
     continue
    rkind = rraw.get("kind")
    if isinstance(rkind, str) and rkind.startswith("DIGITALE"):
     digr.add(rriga)
    elif type(rraw.get("bit")) is int:
     digr.add(rriga)
    else:
     continue
    if not rraw.get("description"):
     continue
    rreg = rraw.get("modbus_register")
    rbit = rraw.get("bit")
    if type(rbit) is not int or rbit < 0 or rbit > 15:
     badregs.add(rreg)
    else:
     regbits.setdefault(rreg, []).append(rbit)
   for rreg in regbits:
    if len(regbits[rreg]) != len(set(regbits[rreg])):
     badregs.add(rreg)
   if has_names:
    if set(nbmr) != set(mrge):
     warnings.append({"rule": "riga_mismatch", "page_no": page_no, "riga": None, "detail": "nomi vs mis"})
     counters["riga_mismatch"] = counters["riga_mismatch"] + 1
   if has_states:
    if set(states_by_riga) != set(mrge):
     warnings.append({"rule": "riga_mismatch", "page_no": page_no, "riga": None, "detail": "stati vs mis"})
     counters["riga_mismatch"] = counters["riga_mismatch"] + 1
    orphans = sorted(set(states_by_riga) - set(mrge))
    if orphans:
     warnings.append({"rule": "stati_orfani", "page_no": page_no, "riga": None, "detail": str(len(orphans)) + " orfani"})
     counters["stati_orfani"] = counters.get("stati_orfani", 0) + 1
     for orf in orphans:
      for orow in sdup.get(orf, [states_by_riga[orf]]):
       oson = orow.get("state_on")
       osoff = orow.get("state_off")
       if oson is None and osoff is None:
        continue
       warnings.append({"rule": "stati_orfani_utili", "page_no": page_no, "riga": orf, "detail": "riga " + str(orf) + ": " + repr(orow.get("description")) + " on=" + str(oson) + " off=" + str(osoff) + " (no reg)"})
       counters["stati_orfani_utili"] = counters.get("stati_orfani_utili", 0) + 1
    if has_names:
     xnomi = list(nbmr.keys())
     xni = 0
     while xni < len(xnomi):
      xnr = nbmr[xnomi[xni]]
      xni = xni + 1
      if type(xnr.get("bit")) is int:
       digr.add(xnomi[xni - 1])
    if (digr and len(states_by_riga) * 2 < len(digr)):
     warnings.append({"rule": "sospetto_sottocampionamento", "page_no": page_no, "riga": None, "detail": "stati " + str(len(states_by_riga)) + "/" + str(len(digr)) + " digitali: TEXTON da keyword"})
     counters["sospetto_sottocampionamento"] = counters.get("sospetto_sottocampionamento", 0) + 1
   shift1regs = set()
   if has_names:
    cand = []
    shift_ok = True
    for raw in raws:
     if not isinstance(raw, dict):
      shift_ok = False
      break
     riga = raw.get("riga")
     nb = nbmr.get(riga) if type(riga) is int else None
     nbit = nb.get("bit") if nb is not None else None
     mbit = raw.get("bit")
     if type(nbit) is not int or type(mbit) is not int:
      shift_ok = False
      break
     if nb.get("modbus_register") != raw.get("modbus_register"):
      shift_ok = False
      break
     if nbit != mbit + 1:
      shift_ok = False
      break
     cand.append((raw.get("modbus_register"), nbit))
    top16 = False
    for reg, nbit in cand:
     if nbit > 15:
      top16 = True
    if shift_ok and top16 and len(cand) >= 3:
     for reg, nbit in cand:
      if reg is not None:
       shift1regs.add(reg)
   for reg in sorted(shift1regs):
    warnings.append({"rule": "bit_offset_pagina", "page_no": page_no, "riga": None, "detail": "reg " + str(reg) + ": nomi-bit 1-based, bit riportati a 0"})
    counters["bit_offset_pagina"] = counters.get("bit_offset_pagina", 0) + 1
   no_riga = False
   ri = 0
   while ri < len(raws):
    raw = raws[ri]
    ri = ri + 1
    if isinstance(raw, dict) and raw.get("riga") is None:
     no_riga = True
   if no_riga:
    warnings.append({"rule": "riga_mancante", "page_no": page_no, "riga": None, "detail": "misure senza riga"})
   kept = []
   ri = 0
   while ri < len(raws):
    raw = raws[ri]
    ri = ri + 1
    if not isinstance(raw, dict):
     counters["righe_non_valide"] = counters.get("righe_non_valide", 0) + 1
     continue
    desc = raw.get("description", None)
    if desc is None:
     try:
      rkeys = raw.keys()
     except Exception:
      rkeys = []
     ki = 0
     while ki < len(list(rkeys)):
      kk = list(rkeys)[ki]
      ki = ki + 1
      if isinstance(kk, str) and kk.lower() == "description":
       try:
        desc = raw.get(kk)
       except Exception:
        continue
       if desc is not None:
        break
    decision = "keep"
    reason = ""
    if desc is None:
     decision = "V2"
     reason = "description is null"
    elif not isinstance(desc, str):
     decision = "keep"
    elif not desc.strip() or desc.strip() == "/":
     decision = "V2"
     reason = "description is empty or '/'"
    else:
     normed_desc = " ".join(desc.strip().split()).lower()
     if normed_desc in v2_spare:
      decision = "V2"
      reason = "description is a spare/placeholder token: " + repr(desc.strip())
     elif normed_desc in v2_headers:
      decision = "V2"
      reason = "description is a section header: " + repr(desc.strip())
    zona = None
    for zk in ("zona", "area", "ZONA", "AREA"):
     try:
      zv = raw.get(zk)
     except Exception:
      zv = None
     if isinstance(zv, str) and zv.strip():
      zona = zv
      break
    if decision == "keep" and zona is not None:
     zkey = " ".join(zona.strip().split()).upper()
     if ("INPUT_HW" in zkey or "OUTPUT_HW" in zkey or zkey.endswith("_HW")):
      decision = "V21"
      reason = "zona is a hardware zone: " + repr(zona.strip())
    if decision == "keep":
     note = ""
     ki = 0
     while ki < len(note_keys):
      try:
       nv = raw.get(note_keys[ki])
      except Exception:
       nv = None
      ki = ki + 1
      if isinstance(nv, str) and nv.strip():
       note = nv
       break
     if note:
      lowered = " ".join(note.strip().split()).lower()
      pj = 0
      while pj < len(v20_phrases):
       if v20_phrases[pj] in lowered:
        decision = "V20"
        reason = "annotation contains " + repr(v20_phrases[pj].upper())
        break
       pj = pj + 1
    if decision != "keep":
     warnings.append({"rule": "scarto_" + decision, "page_no": page_no, "riga": raw.get("riga"), "detail": str(desc) + " - " + reason})
     counters["scarti_" + decision] = counters["scarti_" + decision] + 1
     continue
    var = {}
    fi = 0
    while fi < len(v14_fields):
     f = v14_fields[fi]
     fi = fi + 1
     if f == "description":
      var[f] = desc
     else:
      try:
       var[f] = raw.get(f)
      except Exception:
       var[f] = None
    if var.get("kind") is None:
     var["kind"] = "ANALOGICA"
    if var.get("pagina") is None and type(page_no) is int:
     var["pagina"] = page_no
    riga = raw.get("riga")
    xsd = None
    if (has_states and type(riga) is int):
     st = states_by_riga.get(riga)
     if st is not None:
      xsd = st.get("description", None)
    if (has_names and type(riga) is int and riga in nbmr):
     nb = nbmr[riga]
     nb_desc = nb.get("description", None)
     if (xsd is not None and nb_desc is not None and xsd == nb_desc and xsd != var.get("description") and nb.get("modbus_register") == var.get("modbus_register") and nb.get("bit") == var.get("bit")):
      warnings.append({"rule": "refuso_maggioranza", "page_no": page_no, "riga": riga, "detail": "riga " + str(riga) + " maggio"})
      counters["refuso_maggioranza"] = counters.get("refuso_maggioranza", 0) + 1
      var["description"] = nb_desc
     xvd = var.get("description")
     xna = None
     if isinstance(nb_desc, str):
      xna = " ".join(nb_desc.replace("()", "").replace("( )", "").split())
      if len(xna) >= 2 and xna[0] == xna[-1] and xna[0] in "'\"":
       xna = " ".join(xna[1:-1].split())
     xnb = None
     if isinstance(xvd, str):
      xnb = " ".join(xvd.replace("()", "").replace("( )", "").split())
      if len(xnb) >= 2 and xnb[0] == xnb[-1] and xnb[0] in "'\"":
       xnb = " ".join(xnb[1:-1].split())
     xsa = "".join(c for c in nb_desc.upper() if c.isalnum()) if isinstance(nb_desc, str) else ""
     xsb = "".join(c for c in xvd.upper() if c.isalnum()) if isinstance(xvd, str) else ""
     xt = (xsa != xsb and len(xsa) >= 4 and len(xsb) >= 4 and abs(len(xsa) - len(xsb)) <= 2 and xsa.translate(xdigits) != xsb.translate(xdigits) and (xsa[:3] == xsb[:3] and xsa[-3:] == xsb[-3:] or xsa in xsb or xsb in xsa or (len(xsa) == len(xsb) and sum(1 for xx, xy in zip(xsa, xsb) if xx != xy) <= 2)))
     desc_ok = (nb_desc is not None and (nb_desc == xvd or xna == xnb or xt))
     shift1 = var.get("modbus_register") in shift1regs
     if shift1:
      var["_bit_offset_pagina"] = True
     diffs = []
     if nb.get("modbus_register") != var.get("modbus_register"):
      diffs.append("reg " + str(var.get("modbus_register")) + "->" + str(nb.get("modbus_register")))
     if nb.get("bit") != var.get("bit"):
      diffs.append("bit " + str(var.get("bit")) + "->" + str(nb.get("bit")))
     if diffs and not shift1:
      same_reg = (nb.get("modbus_register") == var.get("modbus_register"))
      fill_null = var.get("modbus_register") is None
      suffix = " nomi-bit"
      if not desc_ok:
       suffix = " shift"
      elif not (same_reg or fill_null):
       suffix = " reg"
      warnings.append({"rule": "bit_register_mismatch", "page_no": page_no, "riga": riga, "detail": "riga " + str(riga) + ": " + "; ".join(diffs) + suffix})
      counters["bit_register_mismatch"] = counters.get("bit_register_mismatch", 0) + 1
      if desc_ok and (same_reg or fill_null):
       var["modbus_register"] = nb.get("modbus_register")
       var["bit"] = nb.get("bit")
      elif not desc_ok:
       warnings.append({"rule": "riga_disallineata", "page_no": page_no, "riga": riga, "detail": "riga " + str(riga) + " shift"})
       counters["riga_disallineata"] = counters.get("riga_disallineata", 0) + 1
     if nb_desc != var.get("description") and not shift1:
      warnings.append({"rule": "descrizione_mismatch", "page_no": page_no, "riga": riga, "detail": "riga " + str(riga) + " desc"})
      counters["descrizione_mismatch"] = counters.get("descrizione_mismatch", 0) + 1
      if (nb.get("modbus_register") == var.get("modbus_register") and nb.get("bit") == var.get("bit") and xt):
       warnings.append({"rule": "refuso_sospetto", "page_no": page_no, "riga": riga, "detail": "riga " + str(riga) + " refuso"})
       counters["refuso_sospetto"] = counters.get("refuso_sospetto", 0) + 1
    if (has_names and isinstance(var.get("kind"), str) and var.get("kind").upper().startswith("DIGITALE") and var.get("modbus_register") not in shift1regs):
     ncand = names_by_desc.get(var.get("description"), None)
     if (ncand is not None and var.get("modbus_register") is not None and var.get("modbus_register") in badregs and var.get("description") not in names_desc_dup and ncand.get("modbus_register") == var.get("modbus_register") and type(ncand.get("bit")) is int and ncand.get("bit") >= 0 and ncand.get("bit") <= 15 and ncand.get("bit") != var.get("bit")):
      warnings.append({"rule": "bit_register_mismatch", "page_no": page_no, "riga": riga, "detail": "riga " + str(ncand.get("riga")) + "->" + str(riga) + " bit->" + str(ncand.get("bit"))})
      counters["bit_register_mismatch"] = counters.get("bit_register_mismatch", 0) + 1
      var["bit"] = ncand.get("bit")
    if (has_states and type(riga) is int):
     xvd = var.get("description")
     xmn = ""
     if isinstance(xvd, str):
      xmn = " ".join(xvd.replace("()", "").replace("( )", "").split())
      if len(xmn) >= 2 and xmn[0] == xmn[-1] and xmn[0] in "'\"":
       xmn = " ".join(xmn[1:-1].split())
     xpair = (st is not None and (xsd is None or xsd == xvd))
     if st is not None and not xpair:
      xma = ""
      if isinstance(xsd, str):
       xma = " ".join(xsd.replace("()", "").replace("( )", "").split())
       if len(xma) >= 2 and xma[0] == xma[-1] and xma[0] in "'\"":
        xma = " ".join(xma[1:-1].split())
      xua = "".join(c for c in xsd.upper() if c.isalnum()) if isinstance(xsd, str) else ""
      xub = "".join(c for c in xvd.upper() if c.isalnum()) if isinstance(xvd, str) else ""
      xpair = (xma == xmn or (xua != xub and len(xua) >= 4 and len(xub) >= 4 and abs(len(xua) - len(xub)) <= 2 and xua.translate(xdigits) != xub.translate(xdigits) and (xua[:3] == xub[:3] and xua[-3:] == xub[-3:] or xua in xub or xub in xua or (len(xua) == len(xub) and sum(1 for xx, xy in zip(xua, xub) if xx != xy) <= 2))))
     if not xpair:
      xfound = None
      xfi = 0
      while xfi < len(states_in):
       xfr = states_in[xfi]
       xfi = xfi + 1
       xfd = xfr.get("description", None) if isinstance(xfr, dict) else None
       if xfd is None:
        continue
       xfkey = ""
       if isinstance(xfd, str):
        xfkey = " ".join(xfd.replace("()", "").replace("( )", "").split())
        if len(xfkey) >= 2 and xfkey[0] == xfkey[-1] and xfkey[0] in "'\"":
         xfkey = " ".join(xfkey[1:-1].split())
       if xfd == xvd or xfkey == xmn:
        if xfound is not None:
         xfound = None
         break
        xfound = xfr
      if xfound is not None:
       st = xfound
       xpair = True
       warnings.append({"rule": "stati_riallineati", "page_no": page_no, "riga": riga, "detail": "riga " + str(xfound.get("riga")) + "->" + str(riga)})
       counters["stati_riallineati"] = counters.get("stati_riallineati", 0) + 1
     if st is None or not xpair:
      if st is not None:
       warnings.append({"rule": "stati_disallineati", "page_no": page_no, "riga": riga, "detail": "riga " + str(riga) + ": " + repr(var.get("description")) + " vs " + repr(xsd) + " (tengo misure)"})
       counters["stati_disallineati"] = counters.get("stati_disallineati", 0) + 1
     else:
      for sf in ("state_on", "state_off"):
       sinc = st.get(sf)
       if sinc is None:
        continue
       if isinstance(sinc, str):
        xjin = sinc.strip().replace(" ", "")
        if xjin in ("0", "1") or xjin[:2] in ("0=", "1="):
         continue
       elif sinc in (0, 1):
        continue
       if (var.get(sf) is not None and sinc != var.get(sf)):
        warnings.append({"rule": "stati_mismatch", "page_no": page_no, "riga": riga, "detail": "riga " + str(riga) + " " + sf + ": " + str(var.get(sf)) + "->" + str(sinc)})
        counters["stati_mismatch"] = counters.get("stati_mismatch", 0) + 1
       var[sf] = sinc
    kept.append(var)
   ip = None
   try:
    ipv = station.get("ip")
   except Exception:
    ipv = None
   if isinstance(ipv, str) and ipv.strip():
    ip = ipv.strip()
   real = (ip is not None and "xxx" not in ip and ip != ":" and ip.strip(".") != "")
   if ip is not None and real:
    skey = ("ip", ip)
   elif ip is not None:
    skey = ("placeholder", page_no, stations.index(station))
   else:
    skey = ("anon",)
   if skey not in acc:
    acc[skey] = {"meta": {}, "variables": [], "last_reg": None}
    mi = 0
    while mi < len(meta_keys):
     try:
      acc[skey]["meta"][meta_keys[mi]] = station.get(meta_keys[mi])
     except Exception:
      acc[skey]["meta"][meta_keys[mi]] = None
     mi = mi + 1
    acc_order.append(skey)
   slot = acc[skey]
   mi = 0
   while mi < len(meta_keys):
    mk = meta_keys[mi]
    mi = mi + 1
    try:
     nv = station.get(mk)
    except Exception:
     nv = None
    if slot["meta"].get(mk) is None and nv is not None:
     slot["meta"][mk] = nv
   vi = 0
   while vi < len(kept):
    var = kept[vi]
    vi = vi + 1
    reg = var.get("modbus_register")
    if type(reg) is int:
     slot["last_reg"] = reg
    elif (reg is None and type(var.get("bit")) is int and var.get("kind") != "ANALOGICA" and slot["last_reg"] is not None):
     var["modbus_register"] = slot["last_reg"]
     warnings.append({"rule": "registro_applicato", "page_no": page_no, "riga": var.get("riga"), "detail": "REG " + str(slot["last_reg"]) + " carry"})
     counters["registri_applicati"] = counters["registri_applicati"] + 1
    slot["variables"].append(var)
  oi = oi + 1
 xi = 0
 while xi < len(acc_order):
  xkey = acc_order[xi]
  xi = xi + 1
  if not xkey or xkey[0] != "placeholder":
   continue
  xowned = []
  vi = 0
  while vi < len(acc[xkey]["variables"]):
   var = acc[xkey]["variables"][vi]
   vi = vi + 1
   xdesc = var.get("description")
   if isinstance(xdesc, str):
    xdkey = " ".join(xdesc.split()).lower()
   else:
    xdkey = ""
   xowned.append((xdkey, var.get("modbus_register"), var.get("bit")))
  xo = 0
  while xo < len(acc_order):
   xother = acc_order[xo]
   xo = xo + 1
   if xother is xkey or not xother or xother[0] == "placeholder":
    continue
   xkept = []
   vi = 0
   while vi < len(acc[xother]["variables"]):
    var = acc[xother]["variables"][vi]
    vi = vi + 1
    xdesc = var.get("description")
    if isinstance(xdesc, str):
     xdkey = " ".join(xdesc.split()).lower()
    else:
     xdkey = ""
    if (xdkey, var.get("modbus_register"), var.get("bit")) in xowned:
     warnings.append({"rule": "copia_reale_da_placeholder", "page_no": None, "riga": var.get("riga"), "detail": "->" + str(acc[xother]["meta"].get("ip"))})
     counters["copia_reale_da_placeholder"] = counters.get("copia_reale_da_placeholder", 0) + 1
    else:
     xkept.append(var)
   acc[xother]["variables"] = xkept
 qi = 0
 while qi < len(acc_order):
  qvars = acc[acc_order[qi]]["variables"]
  qi = qi + 1
  qk = 0
  while qk < len(qvars):
   qvar = qvars[qk]
   qk = qk + 1
   qbit = qvar.get("bit")
   if type(qbit) is not int or 0 <= qbit <= 15:
    continue
   if qvar.get("_bit_offset_pagina"):
    qvar["bit"] = qbit - 1
    qvar.pop("_bit_offset_pagina", None)
    warnings.append({"rule": "bit_offset_pagina", "page_no": qvar.get("pagina"), "riga": qvar.get("riga"), "detail": "reg " + str(qvar.get("modbus_register")) + ": bit " + str(qbit) + "->" + str(qbit - 1)})
    counters["bit_offset_pagina"] = counters.get("bit_offset_pagina", 0) + 1
    continue
   qs = []
   qi2 = 0
   while qi2 < len(qvars):
    qother = qvars[qi2]
    qi2 = qi2 + 1
    if qother is qvar:
     continue
    if (qother.get("modbus_register") == qvar.get("modbus_register") and type(qother.get("bit")) is int):
     qs.append(qother.get("bit"))
   if qbit == 16 and 15 not in qs:
    qvar["bit"] = 15
    warnings.append({"rule": "bit_fuori_range", "page_no": qvar.get("pagina"), "riga": qvar.get("riga"), "detail": "bit 16->15"})
    counters["bit_fuori_range"] = counters.get("bit_fuori_range", 0) + 1
   else:
    warnings.append({"rule": "bit_fuori_range", "page_no": qvar.get("pagina"), "riga": qvar.get("riga"), "detail": "bit " + str(qbit)})
    counters["bit_fuori_range"] = counters.get("bit_fuori_range", 0) + 1
  for qvar in qvars:
   qvar.pop("_bit_offset_pagina", None)
 ai = 0
 while ai < len(acc_order):
  variables = acc[acc_order[ai]]["variables"]
  ai = ai + 1
  vi = 0
  while vi < len(variables):
   var = variables[vi]
   vi = vi + 1
   tag = var.get("tag")
   if not (isinstance(tag, str) and tag.strip()):
    continue
   tag = tag.strip()
   di = 0
   while di < len(variables):
    donor = variables[di]
    di = di + 1
    if donor is var:
     continue
    dtag = donor.get("tag")
    same = isinstance(dtag, str) and dtag.strip() == tag
    ddesc = donor.get("description")
    fallback = (isinstance(ddesc, str) and (ddesc == tag or ddesc == tag + " Raw"))
    if not (same or fallback):
     continue
    fi = 0
    while fi < len(fill_fields):
     f = fill_fields[fi]
     fi = fi + 1
     if var.get(f) is None and donor.get(f) is not None:
      var[f] = donor.get(f)
      counters["scale_collegate"] = counters["scale_collegate"] + 1
  singles = {}
  vi = 0
  while vi < len(variables):
   var = variables[vi]
   vi = vi + 1
   if (var.get("kind") == "DIGITALE_SINGOLO" and type(var.get("modbus_register")) is int):
    reg = var.get("modbus_register")
    singles[reg] = singles.get(reg, 0) + 1
  shared = []
  for reg in singles:
   if singles[reg] > 1:
    shared.append(reg)
  shared = sorted(shared)
  hi = 0
  while hi < len(shared):
   reg = shared[hi]
   hi = hi + 1
   flipped = 0
   vi = 0
   while vi < len(variables):
    var = variables[vi]
    vi = vi + 1
    if (var.get("kind") == "DIGITALE_SINGOLO" and var.get("modbus_register") == reg):
     var["kind"] = "DIGITALE_IMPACCATO"
     flipped = flipped + 1
   counters["packed_fold"] = counters["packed_fold"] + flipped
   warnings.append({"rule": "fold_packed", "page_no": None, "riga": None, "detail": "REG " + str(reg)})
  seen_keys = []
  dup_pairs = []
  vi = 0
  while vi < len(variables):
   var = variables[vi]
   vi = vi + 1
   desc = var.get("description")
   if isinstance(desc, str):
    dkey = desc.lower()
   else:
    dkey = ""
   dkey = [dkey, var.get("modbus_register")]
   if dkey in seen_keys:
    dup_pairs.append(str(desc) + " @ " + str(var.get("modbus_register")))
   else:
    seen_keys.append(dkey)
  if dup_pairs:
   counters["duplicati"] = counters["duplicati"] + len(dup_pairs)
   warnings.append({"rule": "duplicati_mantenuti", "page_no": None, "riga": None, "detail": "; ".join(dup_pairs)})
 stations_out = []
 ai = 0
 while ai < len(acc_order):
  slot = acc[acc_order[ai]]
  ai = ai + 1
  stations_out.append({"name": slot["meta"].get("name"), "protocol": slot["meta"].get("protocol"), "ip": slot["meta"].get("ip"), "port": slot["meta"].get("port"), "modbus_id": slot["meta"].get("modbus_id"), "variables": slot["variables"]})
  counters["variabili"] = counters["variabili"] + len(slot["variables"])
 result = json.dumps({"stations": stations_out, "warnings": warnings, "counters": counters}, ensure_ascii=False)
except Exception as error:
 tb = traceback.format_exc(limit=3).replace("\n", " | ")[:900]
 result = json.dumps({"status": "ERROR", "error": str(error), "tb": tb, "stations": [], "warnings": [], "counters": {}}, ensure_ascii=False)
