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
        if any(isinstance(raw, dict) and raw.get("riga") is None
               for raw in raws):
            _warn(warnings, counters, "riga_mancante",
                  "righe measures senza riga: join rami impossibile",
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
                diffs = []
                for field in ("modbus_register", "bit"):
                    if nb.get(field) != var.get(field):
                        diffs.append("%s misure=%s nomi-bit=%s" % (
                            field, var.get(field), nb.get(field)))
                if diffs:
                    _warn(warnings, counters, "bit_register_mismatch",
                          "riga %s: %s (vince nomi-bit)" % (
                              riga, "; ".join(diffs)),
                          page_no=page_no, riga=riga,
                          counter="bit_register_mismatch")
                    var["modbus_register"] = nb.get("modbus_register")
                    var["bit"] = nb.get("bit")
                nb_desc = _description_of(nb)
                if nb_desc != var.get("description"):
                    _warn(warnings, counters, "descrizione_mismatch",
                          "riga %s: misure=%r nomi-bit=%r "
                          "(vince misure)" % (
                              riga, var.get("description"), nb_desc),
                          page_no=page_no, riga=riga,
                          counter="descrizione_mismatch")
            if has_states and _is_int(riga) and riga in states_by_riga:
                st = states_by_riga[riga]
                for field in ("state_on", "state_off"):
                    if (var.get(field) is not None
                            and st.get(field) != var.get(field)):
                        _warn(warnings, counters, "stati_mismatch",
                              "riga %s: %s misure=%r stati=%r "
                              "(vince stati)" % (
                                  riga, field, var.get(field),
                                  st.get(field)),
                              page_no=page_no, riga=riga,
                              counter="stati_mismatch")
                    var[field] = st.get(field)
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


def _merge_meta(old, new):
    for key in ("name", "protocol", "ip", "port", "modbus_id"):
        if old.get(key) is None and new.get(key) is not None:
            old[key] = new[key]
    return old


def consolidate(pages):
    """Merge page chunks into one intermediate output (see module doc)."""
    if isinstance(pages, str):
        pages = json.loads(pages)
    if not isinstance(pages, list):
        raise ValueError("consolidate attende una lista di pagine")
    warnings = []
    counters = {"pagine": 0, "variabili": 0, "scarti_V2": 0,
                "scarti_V20": 0, "scarti_V21": 0, "scale_collegate": 0,
                "registri_applicati": 0, "packed_fold": 0,
                "riga_mismatch": 0, "buchi_sequenza": 0, "duplicati": 0}
    normed = []
    for pos, page in enumerate(pages):
        if isinstance(page, str):
            page = json.loads(page)
        if not isinstance(page, dict):
            raise ValueError("pagina %d non valida" % pos)
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
