"""Single PDF consolidator: page assembly (3 branches) + multi-page merge.

Reference testable implementation. Canvas copies live under
``myhydra/single_pdf/pytools/`` (inline style, no defs); if they diverge,
this file wins.

Input: list of page chunks, one per PDF page, in any order. Each page::

    {"page_no": int | None,
     "stations": [{"name", "protocol", "ip", "port", "modbus_id",
                   "variables": [v14 variable dicts]}],
     "bitnames": {"rows": [{"description", "modbus_register", "bit",
                            "riga"}]},   # optional branch 2
     "bitstates": {"rows": [{"state_on", "state_off",
                             "riga"}]}}  # optional branch 3

Raw engine output is also accepted: the 3 VLM branch blocks concatenated
(measures ``{"stations": [...]}``, names ``{"rows": [...]}``, states
``{"rows": [...]}``), optionally wrapped in ```json fences or a JSON
array. Branch blocks are grouped into pages in arrival order: every
``stations`` block opens a new page, ``rows`` blocks attach to the open
page (classified names vs states by row keys). Pages keep arrival order
(``page_no`` None) unless envelopes carry one.

The ``bitnames``/``bitstates`` branches carry the same ``riga`` numbering
as the measures rows so the page assembler can join on ``riga``.

Output::

    {"stations": [merged stations with v14 variables],
     "warnings": [{"rule", "page_no", "riga", "detail"}],
     "counters": {...}}

Precedence on branch disagreement (explicit, never silent):
- bit-names branch wins for ``bit`` and ``modbus_register``;
- measures branch wins for ``description`` and every technical field;
- states branch wins for ``state_on``/``state_off``.
Every disagreement is a warning. In particular a ``riga_mismatch``
warning is ALWAYS emitted when the present branches disagree on the
row set (the ``riga`` join is fragile if branches diverge on discards).

Discards use ``classify_row`` (V2/V20/V21): counted per rule with a
reason, never silent. ``description`` is read with the canonical rule
(case-insensitive, key ``description`` only), like single_filters.
"""

import json

from nodes.single_filters import classify_row_with_reason

V14_FIELDS = (
    "description", "units", "modbus_register", "bit", "data_type", "kind",
    "read_write", "state_on", "state_off", "scale_elec_start",
    "scale_elec_end", "scale_eng_start", "scale_eng_end", "limit_hour",
    "limit_day", "zona", "tag", "pagina", "riga",
)

FILLABLE_FROM_TAG = (
    "units", "scale_elec_start", "scale_elec_end", "scale_eng_start",
    "scale_eng_end", "limit_hour", "limit_day",
)


def _description_of(row):
    """Canonical description: key ``description`` only, any case."""
    get = getattr(row, "get", None)
    if get is None:
        return None
    value = get("description", None)
    if value is not None:
        return value
    try:
        keys = row.keys()
    except Exception:
        return None
    for key in keys:
        if isinstance(key, str) and key.lower() == "description":
            try:
                return get(key)
            except Exception:
                continue
    return None


def _norm_str(value):
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def _is_int(value):
    return type(value) is int


def _alnum_upper(value):
    return "".join(c for c in value.upper() if c.isalnum())


def _norm_key(value):
    """V19-normalized join key (compare-only, values never rewritten)."""
    if not isinstance(value, str):
        return ""
    out = value.replace("()", "").replace("( )", "")
    out = " ".join(out.split())
    if len(out) >= 2 and out[0] == out[-1] and out[0] in ("'", '"'):
        out = out[1:-1]
    return " ".join(out.split())


def _typo_pair(a, b):
    """True if two descriptions look like the same text with a typo."""
    if not isinstance(a, str) or not isinstance(b, str):
        return False
    na, nb = _alnum_upper(a), _alnum_upper(b)
    if na == nb or len(na) < 4 or len(nb) < 4:
        return False
    if abs(len(na) - len(nb)) > 2:
        return False
    if na[:3] == nb[:3] and na[-3:] == nb[-3:]:
        return True
    return na in nb or nb in na


def _branch_rows(branch):
    """Accept {"rows": [...]} or a bare list; else []."""
    if isinstance(branch, dict):
        branch = branch.get("rows")
    if isinstance(branch, list):
        return [r for r in branch if isinstance(r, dict)]
    return []


def _riga_map(rows):
    """Map riga -> row for rows with an int riga (first wins)."""
    out = {}
    for row in rows:
        riga = row.get("riga")
        if _is_int(riga) and riga not in out:
            out[riga] = row
    return out


def _warn(warnings, counters, rule, detail, page_no=None, riga=None,
          counter=None):
    warnings.append({"rule": rule, "page_no": page_no, "riga": riga,
                     "detail": detail})
    if counter is not None:
        counters[counter] = counters.get(counter, 0) + 1


def _base_variable(raw, page_no):
    """Project a raw measures row onto the full v14 shape."""
    var = {}
    for field in V14_FIELDS:
        if field == "description":
            var[field] = _description_of(raw)
        else:
            try:
                var[field] = raw.get(field)
            except Exception:
                var[field] = None
    if var.get("kind") is None:
        var["kind"] = "ANALOGICA"
    if var.get("pagina") is None and _is_int(page_no):
        var["pagina"] = page_no
    return var


def assemble_page(page, page_no):
    """Join the 3 branches of one page on ``riga`` + apply discards.

    Returns (station_items, warnings, counters) where station_items is a
    list of (meta, variables) in page order.
    """
    warnings = []
    counters = {}
    items = []
    stations = page.get("stations")
    if not isinstance(stations, list):
        return items, warnings, counters
    names_rows = _branch_rows(page.get("bitnames"))
    states_rows = _branch_rows(page.get("bitstates"))
    has_names = isinstance(page.get("bitnames"), (dict, list))
    has_states = isinstance(page.get("bitstates"), (dict, list))
    names_by_riga = _riga_map(names_rows)
    states_by_riga = _riga_map(states_rows)
    states_dup = {}
    for row in states_rows:
        riga = row.get("riga")
        if _is_int(riga):
            states_dup.setdefault(riga, []).append(row)
    raw_total = 0
    for station in stations:
        if (isinstance(station, dict)
                and isinstance(station.get("variables"), list)):
            raw_total += len(station["variables"])
    if raw_total == 0 and not names_rows and not states_rows:
        _warn(warnings, counters, "pagina_vuota_sospetta",
              "pagina vuota: immagine assente?",
              page_no=page_no, counter="pagina_vuota_sospetta")
    for station in stations:
        if not isinstance(station, dict):
            continue
        meta = {k: station.get(k) for k in
                ("name", "protocol", "ip", "port", "modbus_id")}
        raws = station.get("variables")
        if not isinstance(raws, list):
            items.append((meta, []))
            continue
        measures_righe = set()
        for raw in raws:
            if isinstance(raw, dict) and _is_int(raw.get("riga")):
                measures_righe.add(raw.get("riga"))
        names_righe = set(names_by_riga)
        states_righe = set(states_by_riga)
        if has_names and names_righe != measures_righe:
            _warn(warnings, counters, "riga_mismatch",
                  "bitnames rows %s vs measures rows %s" % (
                      sorted(names_righe), sorted(measures_righe)),
                  page_no=page_no, counter="riga_mismatch")
        if has_states and states_righe != measures_righe:
            _warn(warnings, counters, "riga_mismatch",
                  "bitstates rows %s vs measures rows %s" % (
                      sorted(states_righe), sorted(measures_righe)),
                  page_no=page_no, counter="riga_mismatch")
        orphans = sorted(states_righe - measures_righe) if has_states else []
        if orphans:
            _warn(warnings, counters, "stati_orfani",
                  "bitstates senza measures: righe %s (stati ignorati)" % (
                      orphans,),
                  page_no=page_no, counter="stati_orfani")
        digital_righe = set()
        for raw in raws:
            if not isinstance(raw, dict):
                continue
            if not _is_int(raw.get("riga")):
                continue
            kind = raw.get("kind")
            if (isinstance(kind, str) and kind.startswith("DIGITALE")) \
                    or _is_int(raw.get("bit")):
                digital_righe.add(raw.get("riga"))
        if has_names:
            for riga, row in names_by_riga.items():
                if _is_int(row.get("bit")):
                    digital_righe.add(riga)
        if (has_states and len(digital_righe) > 0
                and len(states_righe) * 2 < len(digital_righe)):
            _warn(warnings, counters, "sospetto_sottocampionamento",
                  "stati %d/%d digitali: TEXTON da keyword" % (
                      len(states_righe), len(digital_righe)),
                  page_no=page_no, counter="sospetto_sottocampionamento")
        if any(isinstance(raw, dict) and raw.get("riga") is None
               for raw in raws):
            _warn(warnings, counters, "riga_mancante",
                  "misure senza riga",
                  page_no=page_no)
        variables = []
        for raw in raws:
            if not isinstance(raw, dict):
                counters["righe_non_valide"] = \
                    counters.get("righe_non_valide", 0) + 1
                continue
            decision, reason = classify_row_with_reason(raw)
            if decision != "keep":
                _warn(warnings, counters, "scarto_" + decision,
                      "%s - %s" % (str(_description_of(raw)), reason),
                      page_no=page_no, riga=raw.get("riga"),
                      counter="scarti_" + decision)
                continue
            var = _base_variable(raw, page_no)
            riga = raw.get("riga")
            if has_names and _is_int(riga) and riga in names_by_riga:
                nb = names_by_riga[riga]
                nb_desc = _description_of(nb)
                st_desc = None
                if has_states and _is_int(riga) and riga in states_by_riga:
                    st_desc = _description_of(states_by_riga[riga])
                if (st_desc is not None and nb_desc is not None
                        and st_desc == nb_desc
                        and st_desc != var.get("description")
                        and nb.get("modbus_register")
                        == var.get("modbus_register")
                        and nb.get("bit") == var.get("bit")):
                    _warn(warnings, counters, "refuso_maggioranza",
                          "riga %s: misure=%r contro nomi-bit=stati=%r, "
                          "tengo maggioranza (2 rami)" % (
                              riga, var.get("description"), nb_desc),
                          page_no=page_no, riga=riga,
                          counter="refuso_maggioranza")
                    var["description"] = nb_desc
                desc_ok = (nb_desc is None
                           or nb_desc == var.get("description"))
                diffs = []
                for field in ("modbus_register", "bit"):
                    if nb.get(field) != var.get(field):
                        diffs.append("%s misure=%s nomi-bit=%s" % (
                            field, var.get(field), nb.get(field)))
                if diffs:
                    same_reg = (nb.get("modbus_register")
                                == var.get("modbus_register"))
                    fill_null = var.get("modbus_register") is None
                    if desc_ok and (same_reg or fill_null):
                        suffix = "(vince nomi-bit)"
                    elif desc_ok:
                        suffix = ("(tengo misure: reg diversi)")
                    else:
                        suffix = ("(tengo misure: shift riga?)")
                    _warn(warnings, counters, "bit_register_mismatch",
                          "riga %s: %s %s" % (
                              riga, "; ".join(diffs), suffix),
                          page_no=page_no, riga=riga,
                          counter="bit_register_mismatch")
                    if desc_ok and (same_reg or fill_null):
                        var["modbus_register"] = nb.get("modbus_register")
                        var["bit"] = nb.get("bit")
                    elif not desc_ok:
                        _warn(warnings, counters, "riga_disallineata",
                              "riga %s: misure=%r contro nomi-bit=%r, "
                              "tengo misure" % (
                                  riga, var.get("description"), nb_desc),
                              page_no=page_no, riga=riga,
                              counter="riga_disallineata")
                if nb_desc != var.get("description"):
                    _warn(warnings, counters, "descrizione_mismatch",
                          "riga %s: misure=%r nomi-bit=%r "
                          "(vince misure)" % (
                              riga, var.get("description"), nb_desc),
                          page_no=page_no, riga=riga,
                          counter="descrizione_mismatch")
                    if (nb.get("modbus_register")
                            == var.get("modbus_register")
                            and nb.get("bit") == var.get("bit")
                            and _typo_pair(nb_desc,
                                           var.get("description"))):
                        _warn(warnings, counters, "refuso_sospetto",
                              "riga %s: misure=%r contro nomi-bit=%r, "
                              "stesso registro: una delle due versioni "
                              "corregge un refuso (tenuta misure)" % (
                                  riga, var.get("description"), nb_desc),
                              page_no=page_no, riga=riga,
                              counter="refuso_sospetto")
            if has_states and _is_int(riga) and riga in states_by_riga:
                st = states_by_riga[riga]
                for cand in states_dup.get(riga, [st]):
                    cd = _description_of(cand)
                    if (cd == var.get("description")
                            or _norm_key(cd) == _norm_key(
                                var.get("description"))
                            or _typo_pair(cd, var.get("description"))):
                        st = cand
                        break
                st_desc = _description_of(st)
                st_pair = (st_desc is None
                           or st_desc == var.get("description")
                           or _norm_key(st_desc) == _norm_key(
                               var.get("description"))
                           or _typo_pair(st_desc, var.get("description")))
                if not st_pair:
                    _warn(warnings, counters, "stati_disallineati",
                          "riga %s: misure=%r contro stati=%r, "
                          "stati ignorati (tengo misure)" % (
                              riga, var.get("description"), st_desc),
                          page_no=page_no, riga=riga,
                          counter="stati_disallineati")
                else:
                    for field in ("state_on", "state_off"):
                        incoming = st.get(field)
                        if incoming is None:
                            continue
                        if isinstance(incoming, str):
                            _jin = incoming.strip().replace(" ", "")
                            if _jin in ("0", "1") \
                                    or _jin[:2] in ("0=", "1="):
                                continue
                        elif incoming in (0, 1):
                            continue
                        if (var.get(field) is not None
                                and incoming != var.get(field)):
                            _warn(warnings, counters, "stati_mismatch",
                                  "riga %s: %s misure=%r stati=%r "
                                  "(vince stati)" % (
                                      riga, field, var.get(field),
                                      incoming),
                                  page_no=page_no, riga=riga,
                                  counter="stati_mismatch")
                        var[field] = incoming
            variables.append(var)
        items.append((meta, variables))
    return items, warnings, counters


def _is_real_ip(value):
    return (isinstance(value, str) and value.strip()
            and "xxx" not in value and value.strip() != ":"
            and value.strip().strip(".") != "")


def _station_key(meta, page_no, index):
    ip = _norm_str(meta.get("ip"))
    if ip is not None and _is_real_ip(ip):
        return ("ip", ip)
    if ip is not None:
        return ("placeholder", page_no, index)
    return ("anon",)


def _identity_key(var):
    """Identity of a physical row: description + register + bit."""
    desc = var.get("description")
    if isinstance(desc, str):
        desc_key = " ".join(desc.split()).lower()
    else:
        desc_key = ""
    return (desc_key, var.get("modbus_register"), var.get("bit"))


def _merge_meta(old, new):
    for key in ("name", "protocol", "ip", "port", "modbus_id"):
        if old.get(key) is None and new.get(key) is not None:
            old[key] = new[key]
    return old


def _split_blocks(raw):
    """Split raw engine output into a flat list of blocks.

    Accepts fence-wrapped Markdown, concatenated JSON objects, a JSON
    array, or an already-parsed structure. Strings are decoded, lists
    flattened one level, anything else kept for the grouper to reject
    loudly (never silent).
    """
    import re as _re
    import json as _json

    def _decode_text(text):
        cleaned = _re.sub(r"^```[a-zA-Z]*\s*", "", text.strip())
        cleaned = _re.sub(r"```", "", cleaned).strip()
        if not cleaned:
            return []
        decoder = _json.JSONDecoder()
        found = []
        pos = 0
        end = len(cleaned)
        while pos < end:
            while pos < end and cleaned[pos] in " \n\r\t,;":
                pos += 1
            if pos >= end:
                break
            if cleaned[pos] not in "{[":
                nxt_open = cleaned.find("{", pos)
                nxt_arr = cleaned.find("[", pos)
                cands = [n for n in (nxt_open, nxt_arr) if n >= 0]
                if not cands:
                    break
                pos = min(cands)
                continue
            try:
                obj, stop = decoder.raw_decode(cleaned, pos)
                found.append(obj)
                pos = stop
            except Exception:
                nxt_open = cleaned.find("{", pos + 1)
                nxt_arr = cleaned.find("[", pos + 1)
                cands = [n for n in (nxt_open, nxt_arr) if n >= 0]
                if not cands:
                    break
                pos = min(cands)
        return found

    blocks = []
    queue = [raw]
    while queue:
        item = queue.pop(0)
        if isinstance(item, str):
            for obj in _decode_text(item):
                queue.append(obj)
        elif isinstance(item, list):
            queue = list(item) + queue
        elif isinstance(item, dict):
            blocks.append(item)
        elif item is not None:
            blocks.append(item)
    return blocks


def _is_names_rows(rows):
    """True when rows look like the bit-names branch output."""
    for row in rows:
        if not isinstance(row, dict):
            continue
        keys = set(row)
        if keys & {"description", "modbus_register", "bit"}:
            return True
        if keys & {"state_on", "state_off"}:
            return False
    return False


_BRANCH_ROW_KEYS = frozenset(
    ("description", "modbus_register", "bit", "state_on", "state_off"))


def _is_branch_row(block):
    """True when a bare dict looks like one branch row (no envelope).

    The engine sometimes forwards the states branch as a raw array, so
    single rows reach the grouper without a ``stations``/``rows`` wrapper.
    Anything else stays a loud structural error, never silent.
    """
    return bool(set(block) & _BRANCH_ROW_KEYS)


def _attach_branch(current, slot, rows, fragment):
    """Attach branch rows, accumulating bare-row fragments in arrival order.

    Full ``rows`` envelopes overwrite (tested semantics); bare fragments
    extend an existing envelope instead of clobbering it.
    """
    if fragment:
        existing = current.get(slot)
        if (isinstance(existing, dict)
                and isinstance(existing.get("rows"), list)):
            existing["rows"] = existing["rows"] + rows
            return
    current[slot] = {"rows": rows}


def _group_branches(blocks, warnings, counters):
    """Group raw branch blocks into page envelopes in arrival order.

    A block with a ``stations`` list opens a new page (full envelopes
    with ``page_no``/``bitnames``/``bitstates`` pass through untouched).
    A ``rows`` block attaches to the open page as names or states by
    row shape. Orphan rows (no open page) open an empty-stations page
    with a warning so nothing is lost silently.
    """
    pages = []
    current = None

    def _open():
        page = {"stations": [], "bitnames": None, "bitstates": None,
                "_raw_group": True}
        pages.append(page)
        return page

    for block in blocks:
        if not isinstance(block, dict):
            raise ValueError("blocco non valido: %r" % (block,))
        if isinstance(block.get("stations"), list) and (
                _is_int(block.get("page_no"))
                or block.get("bitnames") is not None
                or block.get("bitstates") is not None):
            pages.append(block)
            current = None
            continue
        if _is_int(block.get("page_no")):
            pages.append(block)
            current = None
            continue
        if isinstance(block.get("stations"), list):
            current = _open()
            current["stations"] = block["stations"]
            for key in ("page_no",):
                if _is_int(block.get(key)):
                    current[key] = block[key]
            continue
        rows = block.get("rows")
        fragment = rows is None and _is_branch_row(block)
        if fragment:
            rows = [block]
        if not isinstance(rows, list):
            raise ValueError(
                "blocco senza stations ne rows: chiavi %s tipi {%s}" % (
                    sorted([k for k in block]),
                    ", ".join(sorted(set(
                        type(block[k]).__name__ for k in block)))))
        dict_rows = [r for r in rows if isinstance(r, dict)]
        if not dict_rows:
            counters["blocco_rows_vuoto"] = counters.get(
                "blocco_rows_vuoto", 0) + 1
            continue
        if current is None:
            current = _open()
            _warn(warnings, counters, "righe_senza_misure",
                  "%d righe ramo senza pagina misure: in attesa di join"
                  % len(dict_rows),
                  counter="righe_senza_misure")
        state_rows = [r for r in dict_rows
                      if "state_on" in r or "state_off" in r]
        if not state_rows:
            has_names_keys = any(
                "description" in r or "modbus_register" in r or "bit" in r
                for r in dict_rows)
            if not has_names_keys:
                raise ValueError(
                    "blocco rows non riconoscibile: chiavi %s" % sorted(
                        set(k for r in dict_rows for k in r)))
            _attach_branch(current, "bitnames", rows, fragment)
        else:
            name_rows = [r for r in dict_rows if r not in state_rows]
            if name_rows:
                _warn(warnings, counters, "ramo_misto",
                      "blocco rows con %d righe stati e %d righe nomi: "
                      "instradate per riga" % (len(state_rows),
                                               len(name_rows)),
                      counter="ramo_misto")
                _attach_branch(current, "bitnames", name_rows, fragment)
            _attach_branch(current, "bitstates", state_rows, fragment)
    if counters.get("blocco_rows_vuoto"):
        _warn(warnings, counters, "blocco_rows_vuoto",
              "%d blocchi rows vuoti scartati (ramo silente)" % (
                  counters["blocco_rows_vuoto"],))
    cleaned = []
    for page in pages:
        if page.get("_raw_group"):
            page = {k: v for k, v in page.items() if k != "_raw_group"}
            if page.get("bitnames") is None:
                page.pop("bitnames", None)
            if page.get("bitstates") is None:
                page.pop("bitstates", None)
        cleaned.append(page)
    return cleaned


def consolidate(pages):
    """Merge page chunks into one intermediate output (see module doc)."""
    if isinstance(pages, dict):
        pages = [pages]
    if isinstance(pages, (str, list)):
        pass
    else:
        raise ValueError("attendo lista pagine")
    warnings = []
    counters = {"pagine": 0, "variabili": 0, "scarti_V2": 0,
                "scarti_V20": 0, "scarti_V21": 0, "scale_collegate": 0,
                "registri_applicati": 0, "packed_fold": 0,
                "riga_mismatch": 0, "buchi_sequenza": 0, "duplicati": 0}
    blocks = _split_blocks(pages)
    if not blocks and isinstance(pages, str) and pages.strip():
        raise ValueError("input non JSON")
    pages = _group_branches(blocks, warnings, counters)
    normed = []
    for pos, page in enumerate(pages):
        if (not _is_int(page.get("page_no"))
                and not isinstance(page.get("stations"), list)):
            raise ValueError("pagina %d senza page_no ne stations" % pos)
        normed.append((pos, page))
    numbered = [(pg.get("page_no"), pos, pg) for pos, pg in normed
                if _is_int(pg.get("page_no"))]
    unnumbered = [(pos, pg) for pos, pg in normed
                  if not _is_int(pg.get("page_no"))]
    numbered.sort(key=lambda t: t[0])
    ordered = [(pn, pg) for pn, _, pg in numbered]
    for pos, pg in unnumbered:
        _warn(warnings, counters, "pagina_senza_numero",
              "pagina in posizione %d senza page_no: ordine di arrivo" % pos)
        ordered.append((None, pg))
    if numbered:
        seen = sorted({pn for pn, _, _ in numbered})
        missing = [n for n in range(seen[0], seen[-1] + 1) if n not in seen]
        if missing:
            _warn(warnings, counters, "sequenza_buchi",
                  "page_no mancanti: %s" % ", ".join(str(n) for n in missing),
                  counter="buchi_sequenza")
    acc = {}
    order = []
    for page_no, page in ordered:
        counters["pagine"] += 1
        items, w, c = assemble_page(page, page_no)
        warnings.extend(w)
        for key in c:
            counters[key] = counters.get(key, 0) + c.get(key, 0)
        for index, (meta, variables) in enumerate(items):
            key = _station_key(meta, page_no, index)
            if key not in acc:
                acc[key] = {"meta": {k: meta.get(k) for k in
                                     ("name", "protocol", "ip", "port",
                                      "modbus_id")},
                            "variables": [], "last_reg": None}
                order.append(key)
            slot = acc[key]
            _merge_meta(slot["meta"], meta)
            for var in variables:
                reg = var.get("modbus_register")
                if _is_int(reg):
                    slot["last_reg"] = reg
                elif (reg is None and _is_int(var.get("bit"))
                        and var.get("kind") != "ANALOGICA"
                        and slot["last_reg"] is not None):
                    var["modbus_register"] = slot["last_reg"]
                    _warn(warnings, counters, "registro_applicato",
                          "%s: REG %s applicato "
                          "(carry-over, verificare sul PDF)" % (
                              var.get("description"), slot["last_reg"]),
                          page_no=page_no, riga=var.get("riga"),
                          counter="registri_applicati")
                slot["variables"].append(var)
    for key in order:
        if not key or key[0] != "placeholder":
            continue
        owned = set()
        for var in acc[key]["variables"]:
            owned.add(_identity_key(var))
        for other in order:
            if other is key or not other or other[0] == "placeholder":
                continue
            kept = []
            for var in acc[other]["variables"]:
                if _identity_key(var) in owned:
                    _warn(warnings, counters, "copia_reale_da_placeholder",
                          "%s @ %s: copia placeholder su %s, tenuto placeholder" % (
                              var.get("description"),
                              var.get("modbus_register"),
                              acc[other]["meta"].get("ip")),
                          page_no=None, riga=var.get("riga"),
                          counter="copia_reale_da_placeholder")
                else:
                    kept.append(var)
            acc[other]["variables"] = kept
    for key in order:
        variables = acc[key]["variables"]
        ik = 0
        while ik < len(variables):
            var = variables[ik]
            ik = ik + 1
            bit = var.get("bit")
            if not _is_int(bit) or 0 <= bit <= 15:
                continue
            siblings = set()
            for other in variables:
                if other is var:
                    continue
                if (other.get("modbus_register")
                        == var.get("modbus_register")
                        and _is_int(other.get("bit"))):
                    siblings.add(other.get("bit"))
            if bit == 16 and 15 not in siblings:
                var["bit"] = 15
                _warn(warnings, counters, "bit_fuori_range",
                      "%r @ %s: bit 16->15 (N.Bit?)" % (
                          var.get("description"),
                          var.get("modbus_register")),
                      page_no=var.get("pagina"), riga=var.get("riga"),
                      counter="bit_fuori_range")
            else:
                _warn(warnings, counters, "bit_fuori_range",
                      "%r @ %s bit %s fuori 0-15: tenuto, verificare "
                      "su ADAS" % (var.get("description"),
                                   var.get("modbus_register"), bit),
                      page_no=var.get("pagina"), riga=var.get("riga"),
                      counter="bit_fuori_range")
    stations = []
    for key in order:
        slot = acc[key]
        variables = slot["variables"]
        for var in variables:
            tag = _norm_str(var.get("tag"))
            if tag is None:
                continue
            for donor in variables:
                if donor is var:
                    continue
                donor_tag = _norm_str(donor.get("tag"))
                donor_desc = donor.get("description")
                same = donor_tag == tag
                fallback = (isinstance(donor_desc, str)
                            and (donor_desc == tag
                                 or donor_desc == tag + " Raw"))
                if not (same or fallback):
                    continue
                for field in FILLABLE_FROM_TAG:
                    if (var.get(field) is None
                            and donor.get(field) is not None):
                        var[field] = donor.get(field)
                        counters["scale_collegate"] += 1
        singles = {}
        for var in variables:
            if (var.get("kind") == "DIGITALE_SINGOLO"
                    and _is_int(var.get("modbus_register"))):
                reg = var.get("modbus_register")
                singles[reg] = singles.get(reg, 0) + 1
        shared = {reg for reg, count in singles.items() if count > 1}
        for reg in sorted(shared):
            flipped = 0
            for var in variables:
                if (var.get("kind") == "DIGITALE_SINGOLO"
                        and var.get("modbus_register") == reg):
                    var["kind"] = "DIGITALE_IMPACCATO"
                    flipped += 1
            counters["packed_fold"] += flipped
            _warn(warnings, counters, "fold_packed",
                  "REG %s: %d singoli -> IMPACCATO" % (reg, flipped))
        seen_keys = set()
        dup_pairs = []
        for var in variables:
            desc = var.get("description")
            desc_key = desc.lower() if isinstance(desc, str) else ""
            dkey = (desc_key, var.get("modbus_register"))
            if dkey in seen_keys:
                dup_pairs.append("%s @ %s" % (desc,
                                              var.get("modbus_register")))
            else:
                seen_keys.add(dkey)
        if dup_pairs:
            counters["duplicati"] += len(dup_pairs)
            _warn(warnings, counters, "duplicati_mantenuti",
                  "; ".join(dup_pairs))
        counters["variabili"] += len(variables)
        stations.append({**slot["meta"], "variables": variables})
    return {"stations": stations, "warnings": warnings, "counters": counters}
