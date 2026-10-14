# edge 5 = array chunk per pagina dal motore iterativo (ricontrollare N dopo rewiring).
import json
import traceback
raw = r'''{edge}[5]'''
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
      if ("description" in block or "modbus_register" in block
        or "bit" in block or "state_on" in block
        or "state_off" in block):
       rows = [block]
       fragment = True
  if not isinstance(rows, list):
   bkeys = list(block.keys())
   bsi = 0
   while bsi < len(bkeys):
    bsj = bsi + 1
    while bsj < len(bkeys):
     if bkeys[bsj] < bkeys[bsi]:
      btw = bkeys[bsi]
      bkeys[bsi] = bkeys[bsj]
      bkeys[bsj] = btw
     bsj = bsj + 1
    bsi = bsi + 1
   btypes = []
   bti = 0
   while bti < len(bkeys):
    btn = type(block[bkeys[bti]]).__name__
    if btn not in btypes:
     btypes.append(btn)
    bti = bti + 1
   bsi = 0
   while bsi < len(btypes):
    bsj = bsi + 1
    while bsj < len(btypes):
     if btypes[bsj] < btypes[bsi]:
      btw = btypes[bsi]
      btypes[bsi] = btypes[bsj]
      btypes[bsj] = btw
     bsj = bsj + 1
    bsi = bsi + 1
   raise ValueError("blocco " + str(bi) + " senza stations ne rows: chiavi "
    + str(bkeys) + " tipi {"
    + ", ".join(btypes)
    + "}")
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
   counters["blocco_rows_vuoto"] = counters.get(
    "blocco_rows_vuoto", 0) + 1
   continue
  if current is None:
   current = {"stations": [], "bitnames": None, "bitstates": None}
   pages.append(current)
   warnings.append({"rule": "righe_senza_misure", "page_no": None,
       "riga": None,
       "detail": str(dict_n) + " righe orfane"})
   counters["righe_senza_misure"] = counters.get(
    "righe_senza_misure", 0) + 1
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
   if len(name_rows) > 0:
    warnings.append({"rule": "ramo_misto", "page_no": None,
        "riga": None,
        "detail": "misto "
        + str(len(state_rows)) + " stati + "
        + str(len(name_rows)) + " nomi: "
        "split per riga"})
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
   raise ValueError("blocco rows non riconoscibile " + str(bi)
    + ": chiavi " + str(sorted(set(
     k for r in rows if isinstance(r, dict) for k in r))))
 if counters.get("blocco_rows_vuoto"):
  warnings.append({"rule": "blocco_rows_vuoto", "page_no": None,
   "riga": None,
   "detail": str(counters["blocco_rows_vuoto"])
   + " rows vuoti (silente)"})
 if not isinstance(pages, list):
  raise ValueError("attendo lista pagine.")
 v2_spare = ("disponibile", "disponibile/", "disponible", "riserva",
    "spare", "reserve", "non utilizzato", "non utilizzata",
    "non usato", "libero", "---")
 v2_headers = ("misure", "comandi", "impostazioni", "input", "output",
    "parametri", "registri", "segnali", "variabili",
    "allarmi", "stati")
 v20_phrases = ("no pc sme", "no sme", "not used", "non utilizzato")
 note_keys = ("note", "nota", "notes", "annotation", "annotazione",
    "comment", "commento", "trailing_note")
 norm = []
 pi = 0
 while pi < len(pages):
  pg = pages[pi]
  if isinstance(pg, str):
   pg = json.loads(pg)
   while isinstance(pg, str):
    pg = json.loads(pg)
  if not isinstance(pg, dict):
   raise ValueError("Pagina non valida in posizione " + str(pi)
       + ".")
  if (type(pg.get("page_no")) is not int
    and not isinstance(pg.get("stations"), list)):
   raise ValueError("Pagina in posizione " + str(pi)
       + " senza page_no ne stations.")
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
  warnings.append({"rule": "pagina_senza_numero", "page_no": None,
      "riga": None,
      "detail": "pagina " + str(unnumbered[ui][0])
      + " senza page_no"})
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
   warnings.append({"rule": "sequenza_buchi", "page_no": None,
       "riga": None,
       "detail": "page_no mancanti: "
       + ", ".join(parts)})
   counters["buchi_sequenza"] = counters["buchi_sequenza"] + 1
 acc = {}
 acc_order = []
 v14_fields = ("description", "units", "modbus_register", "bit",
    "data_type", "kind", "read_write", "state_on",
    "state_off", "scale_elec_start", "scale_elec_end",
    "scale_eng_start", "scale_eng_end", "limit_hour",
    "limit_day", "zona", "tag", "pagina", "riga")
 fill_fields = ("units", "scale_elec_start", "scale_elec_end",
    "scale_eng_start", "scale_eng_end", "limit_hour",
    "limit_day")
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
   if type(riga) is int and riga not in nbmr:
    nbmr[riga] = nr
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
   warnings.append({"rule": "pagina_vuota_sospetta",
       "page_no": page_no, "riga": None,
       "detail": "pagina vuota: immagine assente?"})
   counters["pagina_vuota_sospetta"] = counters.get(
    "pagina_vuota_sospetta", 0) + 1
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
   if has_names:
    if set(nbmr) != set(mrge):
     warnings.append({"rule": "riga_mismatch",
         "page_no": page_no, "riga": None,
         "detail": "nomi "
         + str(sorted(nbmr.keys()))
         + " vs mis "
         + str(sorted(mrge))})
     counters["riga_mismatch"] = counters["riga_mismatch"] + 1
   if has_states:
    if set(states_by_riga) != set(mrge):
     warnings.append({"rule": "riga_mismatch",
         "page_no": page_no, "riga": None,
         "detail": "stati "
         + str(sorted(states_by_riga.keys()))
         + " vs mis "
         + str(sorted(mrge))})
     counters["riga_mismatch"] = counters["riga_mismatch"] + 1
    orphans = sorted(set(states_by_riga) - set(mrge))
    if len(orphans) > 0:
     warnings.append({"rule": "stati_orfani",
         "page_no": page_no, "riga": None,
         "detail": "stati orfani "
         + str(sorted(orphans))
         + " (ignorati)"})
     counters["stati_orfani"] = counters.get(
      "stati_orfani", 0) + 1
     for orf in orphans:
      for orow in sdup.get(orf, [states_by_riga[orf]]):
       oson = orow.get("state_on")
       osoff = orow.get("state_off")
       if oson is None and osoff is None:
        continue
       warnings.append({"rule": "stati_orfani_utili",
           "page_no": page_no, "riga": orf,
           "detail": "riga " + str(orf)
           + ": " + repr(orow.get("description"))
           + " on=" + str(oson)
           + " off=" + str(osoff)
           + " (no reg)"})
       counters["stati_orfani_utili"] = counters.get(
        "stati_orfani_utili", 0) + 1
    digr = set()
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
    if has_names:
     xnomi = list(nbmr.keys())
     xni = 0
     while xni < len(xnomi):
      xnr = nbmr[xnomi[xni]]
      xni = xni + 1
      if type(xnr.get("bit")) is int:
       digr.add(xnomi[xni - 1])
    if (len(digr) > 0
     and len(states_by_riga) * 2 < len(digr)):
     warnings.append({"rule": "sospetto_sottocampionamento",
         "page_no": page_no, "riga": None,
         "detail": "stati "
         + str(len(states_by_riga))
         + "/" + str(len(digr))
         + " digitali: TEXTON da keyword"})
     counters["sospetto_sottocampionamento"] = counters.get(
      "sospetto_sottocampionamento", 0) + 1
   no_riga = False
   ri = 0
   while ri < len(raws):
    raw = raws[ri]
    ri = ri + 1
    if isinstance(raw, dict) and raw.get("riga") is None:
     no_riga = True
   if no_riga:
    warnings.append({"rule": "riga_mancante",
        "page_no": page_no, "riga": None,
        "detail": "misure senza riga"})
   kept = []
   ri = 0
   while ri < len(raws):
    raw = raws[ri]
    ri = ri + 1
    if not isinstance(raw, dict):
     counters["righe_non_valide"] = counters.get(
      "righe_non_valide", 0) + 1
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
     if ("INPUT_HW" in zkey or "OUTPUT_HW" in zkey
       or zkey.endswith("_HW")):
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
     warnings.append({"rule": "scarto_" + decision,
         "page_no": page_no,
         "riga": raw.get("riga"),
         "detail": str(desc) + " - " + reason})
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
     if xsd is None and st is not None:
      try:
       xskeys = st.keys()
      except Exception:
       xskeys = []
      xsi = 0
      while xsi < len(list(xskeys)):
       xsk = list(xskeys)[xsi]
       xsi = xsi + 1
       if (isinstance(xsk, str)
         and xsk.lower() == "description"):
        try:
         xsd = st.get(xsk)
        except Exception:
         continue
        if xsd is not None:
         break
    if (has_names and type(riga) is int
      and riga in nbmr):
     nb = nbmr[riga]
     nb_desc = nb.get("description", None)
     if nb_desc is None:
      try:
       nkeys = nb.keys()
      except Exception:
       nkeys = []
      ki = 0
      while ki < len(list(nkeys)):
       kk = list(nkeys)[ki]
       ki = ki + 1
       if (isinstance(kk, str)
         and kk.lower() == "description"):
        try:
         nb_desc = nb.get(kk)
        except Exception:
         continue
        if nb_desc is not None:
         break
     if (xsd is not None and nb_desc is not None
       and xsd == nb_desc
       and xsd != var.get("description")
       and nb.get("modbus_register")
       == var.get("modbus_register")
       and nb.get("bit") == var.get("bit")):
      warnings.append({"rule": "refuso_maggioranza",
          "page_no": page_no, "riga": riga,
          "detail": "riga " + str(riga)
          + ": misure="
          + repr(var.get("description"))
          + " contro nomi-bit=stati="
          + repr(nb_desc)
          + ", tengo maggioranza (2 rami)"})
      counters["refuso_maggioranza"] = counters.get(
       "refuso_maggioranza", 0) + 1
      var["description"] = nb_desc
     desc_ok = (nb_desc is not None
      and nb_desc == var.get("description"))
     diffs = []
     if nb.get("modbus_register") != var.get("modbus_register"):
      diffs.append("modbus_register misure="
         + str(var.get("modbus_register"))
         + " nomi-bit="
         + str(nb.get("modbus_register")))
     if nb.get("bit") != var.get("bit"):
      diffs.append("bit misure=" + str(var.get("bit"))
         + " nomi-bit=" + str(nb.get("bit")))
     if diffs:
      same_reg = (nb.get("modbus_register")
       == var.get("modbus_register"))
      fill_null = var.get("modbus_register") is None
      suffix = " (vince nomi-bit)"
      if not desc_ok:
       suffix = " (tengo misure: shift riga?)"
      elif not (same_reg or fill_null):
       suffix = " (tengo misure: reg diversi)"
      warnings.append({"rule": "bit_register_mismatch",
          "page_no": page_no, "riga": riga,
          "detail": "riga " + str(riga) + ": "
          + "; ".join(diffs)
          + suffix})
      counters["bit_register_mismatch"] = counters.get(
       "bit_register_mismatch", 0) + 1
      if desc_ok and (same_reg or fill_null):
       var["modbus_register"] = nb.get("modbus_register")
       var["bit"] = nb.get("bit")
      elif not desc_ok:
       warnings.append({"rule": "riga_disallineata",
           "page_no": page_no, "riga": riga,
           "detail": "riga " + str(riga)
           + ": misure=" + repr(var.get("description"))
           + " contro nomi-bit=" + repr(nb_desc)
           + ", tengo misure"})
       counters["riga_disallineata"] = counters.get(
        "riga_disallineata", 0) + 1
     if nb_desc != var.get("description"):
      warnings.append({"rule": "descrizione_mismatch",
          "page_no": page_no, "riga": riga,
          "detail": "riga " + str(riga)
          + ": misure="
          + repr(var.get("description"))
          + " nomi-bit=" + repr(nb_desc)
          + " (vince misure)"})
      counters["descrizione_mismatch"] = counters.get(
       "descrizione_mismatch", 0) + 1
      if (nb.get("modbus_register")
       == var.get("modbus_register")
       and nb.get("bit") == var.get("bit")
       and isinstance(nb_desc, str)
       and isinstance(var.get("description"),
        str)):
       xa = []
       xup = nb_desc.upper()
       xui = 0
       while xui < len(xup):
        if xup[xui].isalnum():
         xa.append(xup[xui])
        xui = xui + 1
       xb = []
       xup = var.get("description").upper()
       xui = 0
       while xui < len(xup):
        if xup[xui].isalnum():
         xb.append(xup[xui])
        xui = xui + 1
       xsa = "".join(xa)
       xsb = "".join(xb)
       xtypo = False
       if (xsa != xsb and len(xsa) >= 4
        and len(xsb) >= 4
        and abs(len(xsa) - len(xsb)) <= 2):
        if xsa[:3] == xsb[:3] and xsa[-3:] == xsb[-3:]:
         xtypo = True
        elif xsa in xsb or xsb in xsa:
         xtypo = True
       if xtypo:
        warnings.append({"rule": "refuso_sospetto",
         "page_no": page_no,
         "riga": riga,
         "detail": "riga " + str(riga)
         + ": misure="
         + repr(var.get("description"))
         + " contro nomi-bit="
         + repr(nb_desc)
         + ", refuso? (tengo misure)"})
        counters["refuso_sospetto"] = counters.get(
         "refuso_sospetto", 0) + 1
    if (has_states and type(riga) is int):
     xpair = (st is not None and (xsd is None
       or xsd == var.get("description")))
     if (st is not None and not xpair
       and isinstance(xsd, str)
       and isinstance(var.get("description"), str)):
      xa = xsd
      if len(xa) >= 2 and xa[0] == xa[-1] and xa[0] in "'\"":
       xa = xa[1:-1]
      xa = " ".join(xa.replace("()", "").replace("( )", "").split())
      xb = var.get("description")
      if len(xb) >= 2 and xb[0] == xb[-1] and xb[0] in "'\"":
       xb = xb[1:-1]
      xb = " ".join(xb.replace("()", "").replace("( )", "").split())
      if xa == xb:
       xpair = True
      yna = []
      yup = xsd.upper()
      yui = 0
      while yui < len(yup):
       if yup[yui].isalnum():
        yna.append(yup[yui])
       yui = yui + 1
      ynb = []
      yup = var.get("description").upper()
      yui = 0
      while yui < len(yup):
       if yup[yui].isalnum():
        ynb.append(yup[yui])
       yui = yui + 1
      ysa = "".join(yna)
      ysb = "".join(ynb)
      if (ysa != ysb and len(ysa) >= 4
        and len(ysb) >= 4
        and abs(len(ysa) - len(ysb)) <= 2):
       if ysa[:3] == ysb[:3] and ysa[-3:] == ysb[-3:]:
        xpair = True
       elif ysa in ysb or ysb in ysa:
        xpair = True
     if not xpair:
      xfound = None
      xfi = 0
      while xfi < len(states_in):
       xfr = states_in[xfi]
       xfi = xfi + 1
       xfd = xfr.get("description", None) if isinstance(xfr, dict) else None
       if xfd is None:
        continue
       if xfd == var.get("description"):
        if xfound is not None: xfound = None; break
        xfound = xfr
      if xfound is not None:
       st = xfound
       xpair = True
       warnings.append({"rule": "stati_riallineati",
           "page_no": page_no, "riga": riga,
           "detail": "riga " + str(xfound.get("riga"))
           + "->" + str(riga)})
       counters["stati_riallineati"] = counters.get(
        "stati_riallineati", 0) + 1
     if st is None or not xpair:
      if st is not None:
       warnings.append({"rule": "stati_disallineati",
           "page_no": page_no, "riga": riga,
           "detail": "riga " + str(riga)
           + ": "
           + repr(var.get("description"))
           + " vs "
           + repr(xsd)
           + " (tengo misure)"})
       counters["stati_disallineati"] = counters.get(
        "stati_disallineati", 0) + 1
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
       if (var.get(sf) is not None
         and sinc != var.get(sf)):
        warnings.append({"rule": "stati_mismatch",
            "page_no": page_no,
            "riga": riga,
            "detail": "riga " + str(riga)
            + " " + sf + ": "
            + str(var.get(sf))
            + "->" + str(sinc)})
        counters["stati_mismatch"] = counters.get(
         "stati_mismatch", 0) + 1
       var[sf] = sinc
    kept.append(var)
   ip = None
   try:
    ipv = station.get("ip")
   except Exception:
    ipv = None
   if isinstance(ipv, str) and ipv.strip():
    ip = ipv.strip()
   real = (ip is not None and "xxx" not in ip and ip != ":"
     and ip.strip(".") != "")
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
    elif (reg is None and type(var.get("bit")) is int
      and var.get("kind") != "ANALOGICA"
      and slot["last_reg"] is not None):
     var["modbus_register"] = slot["last_reg"]
     warnings.append({"rule": "registro_applicato",
         "page_no": page_no,
         "riga": var.get("riga"),
         "detail": str(var.get("description"))
         + ": REG " + str(slot["last_reg"])
         + " applicato (carry-over?)"})
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
   xowned.append((xdkey, var.get("modbus_register"),
    var.get("bit")))
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
    if (xdkey, var.get("modbus_register"),
     var.get("bit")) in xowned:
     warnings.append({"rule": "copia_reale_da_placeholder",
      "page_no": None,
      "riga": var.get("riga"),
      "detail": str(var.get("description"))
      + " @ "
      + str(var.get("modbus_register"))
      + "->" + str(acc[xother]["meta"].get("ip"))
      + " (tenuto)"})
     counters["copia_reale_da_placeholder"] = counters.get(
      "copia_reale_da_placeholder", 0) + 1
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
   qs = []
   qi2 = 0
   while qi2 < len(qvars):
    qother = qvars[qi2]
    qi2 = qi2 + 1
    if qother is qvar:
     continue
    if (qother.get("modbus_register")
      == qvar.get("modbus_register")
      and type(qother.get("bit")) is int):
     qs.append(qother.get("bit"))
   if qbit == 16 and 15 not in qs:
    qvar["bit"] = 15
    warnings.append({"rule": "bit_fuori_range",
        "page_no": qvar.get("pagina"),
        "riga": qvar.get("riga"),
        "detail": repr(qvar.get("description"))
        + " @ "
        + str(qvar.get("modbus_register"))
        + ": bit 16->15 (N.Bit?)"
        })
    counters["bit_fuori_range"] = counters.get(
     "bit_fuori_range", 0) + 1
   else:
    warnings.append({"rule": "bit_fuori_range",
        "page_no": qvar.get("pagina"),
        "riga": qvar.get("riga"),
        "detail": repr(qvar.get("description"))
        + " @ "
        + str(qvar.get("modbus_register"))
        + " bit " + str(qbit)
        + " fuori 0-15: tenuto, verificare su ADAS"})
    counters["bit_fuori_range"] = counters.get(
     "bit_fuori_range", 0) + 1
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
    fallback = (isinstance(ddesc, str)
       and (ddesc == tag or ddesc == tag + " Raw"))
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
   if (var.get("kind") == "DIGITALE_SINGOLO"
     and type(var.get("modbus_register")) is int):
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
    if (var.get("kind") == "DIGITALE_SINGOLO"
      and var.get("modbus_register") == reg):
     var["kind"] = "DIGITALE_IMPACCATO"
     flipped = flipped + 1
   counters["packed_fold"] = counters["packed_fold"] + flipped
   warnings.append({"rule": "fold_packed", "page_no": None,
       "riga": None,
       "detail": "REG " + str(reg) + ": " + str(flipped)
       + " singoli -> IMPACCATO"})
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
    dup_pairs.append(str(desc) + " @ "
        + str(var.get("modbus_register")))
   else:
    seen_keys.append(dkey)
  if dup_pairs:
   counters["duplicati"] = counters["duplicati"] + len(dup_pairs)
   warnings.append({"rule": "duplicati_mantenuti",
       "page_no": None, "riga": None,
       "detail": "; ".join(dup_pairs)})
 stations_out = []
 ai = 0
 while ai < len(acc_order):
  slot = acc[acc_order[ai]]
  ai = ai + 1
  stations_out.append({"name": slot["meta"].get("name"),
       "protocol": slot["meta"].get("protocol"),
       "ip": slot["meta"].get("ip"),
       "port": slot["meta"].get("port"),
       "modbus_id": slot["meta"].get("modbus_id"),
       "variables": slot["variables"]})
  counters["variabili"] = counters["variabili"] + len(slot["variables"])
 result = json.dumps({"stations": stations_out, "warnings": warnings,
      "counters": counters}, ensure_ascii=False)
except Exception as error:
 tb = traceback.format_exc(limit=3).replace("\n", " | ")[:900]
 result = json.dumps({"status": "ERROR", "error": str(error),
      "tb": tb,
      "stations": [], "warnings": [],
      "counters": {}}, ensure_ascii=False)
