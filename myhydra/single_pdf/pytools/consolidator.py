# Consolidatore Single PDF - copia documentata (nodo CONSOLIDADATORE).
# CONFIG CANVAS: edge 5 = array dei chunk per pagina dal motore iterativo.
# Ricontrollare N dopo ogni ricablaggio (Task 8) e togliere match-condition spurie.
# Accetta anche l'output grezzo del motore: i 3 blocchi VLM concatenati
# (misure {stations}, nomi {rows}, stati {rows}), con fence ```json e/o
# array esterno. I blocchi stations aprono una pagina, i blocchi rows si
# agganciano alla pagina aperta (nomi vs stati dalla forma delle righe).
# Unisce i 3 rami per pagina su riga, fonde le pagine in ordine di page_no.
# Precedenza scritta: nomi-bit vince bit/registro, misure il resto, stati gli stati.
# Ogni disaccordo e ogni scarto V2/V20/V21 e' un warning, mai silenzio.
# Fonte autorevole: src/nodes/single_consolidator.py (stessa logica, stessi warning).
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
        raise ValueError("consolidate: input non interpretabile come JSON")
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
        if dict_n == 0 and current is None:
            continue
        if dict_n == 0:
            rows = []
        if current is None:
            current = {"stations": [], "bitnames": None, "bitstates": None}
            pages.append(current)
            warnings.append({"rule": "righe_senza_misure", "page_no": None,
                             "riga": None,
                             "detail": str(dict_n) + " righe ramo senza pagina misure: in attesa di join"})
            counters["righe_senza_misure"] = counters.get(
                "righe_senza_misure", 0) + 1
        if is_names and not is_states:
            current["bitnames"] = {"rows": rows}
        elif is_states and not is_names:
            current["bitstates"] = {"rows": rows}
        elif is_names and is_states:
            current["bitnames"] = {"rows": rows}
            warnings.append({"rule": "ramo_misto", "page_no": None,
                             "riga": None,
                             "detail": "blocco rows con chiavi nomi e stati: assegnato a nomi"})
            counters["ramo_misto"] = counters.get("ramo_misto", 0) + 1
        elif dict_n > 0:
            raise ValueError("blocco rows non riconoscibile in posizione " + str(bi)
                + ": chiavi " + str(sorted(set(
                    k for r in rows if isinstance(r, dict) for k in r))))
        else:
            current["bitnames"] = {"rows": rows}
    if not isinstance(pages, list):
        raise ValueError("Il consolidatore attende una lista di pagine.")
    # V2: scarti per match esatto (case-insensitive dopo strip).
    v2_spare = ("disponibile", "disponibile/", "disponible", "riserva",
                "spare", "reserve", "non utilizzato", "non utilizzata",
                "non usato", "libero", "---")
    v2_headers = ("misure", "comandi", "impostazioni", "input", "output",
                  "parametri", "registri", "segnali", "variabili",
                  "allarmi", "stati")
    # V20: frasi cercate dentro l'annotazione (case-insensitive).
    v20_phrases = ("no pc sme", "no sme", "not used", "non utilizzato")
    # Chiave canonica dell'annotazione: "note"; alias tollerati sotto.
    note_keys = ("note", "nota", "notes", "annotation", "annotazione",
                 "comment", "commento", "trailing_note")
    # Normalizza pagine: stringhe JSON ammesse, non-dict rifiutato.
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
    # Ordine: prima le numerate (crescente), poi le senza numero.
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
    si = 0
    while si < len(numbered):
        sj = si + 1
        while sj < len(numbered):
            if numbered[sj][0] < numbered[si][0]:
                tmp = numbered[si]
                numbered[si] = numbered[sj]
                numbered[sj] = tmp
            sj = sj + 1
        si = si + 1
    ordered = []
    oi = 0
    while oi < len(numbered):
        ordered.append([numbered[oi][0], numbered[oi][2]])
        oi = oi + 1
    ui = 0
    while ui < len(unnumbered):
        warnings.append({"rule": "pagina_senza_numero", "page_no": None,
                         "riga": None,
                         "detail": "pagina in posizione "
                         + str(unnumbered[ui][0])
                         + " senza page_no: ordine di arrivo"})
        ordered.append([None, unnumbered[ui][1]])
        ui = ui + 1
    # Buchi di sequenza sui page_no numerati.
    seen_pn = []
    bi = 0
    while bi < len(numbered):
        pn = numbered[bi][0]
        if pn not in seen_pn:
            seen_pn.append(pn)
        bi = bi + 1
    if seen_pn:
        mn = seen_pn[0]
        mx = seen_pn[0]
        mi = 1
        while mi < len(seen_pn):
            if seen_pn[mi] < mn:
                mn = seen_pn[mi]
            if seen_pn[mi] > mx:
                mx = seen_pn[mi]
            mi = mi + 1
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
    # Accumulo stazioni: chiave (ip) / (placeholder, pagina, idx) / (anon,).
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
        names_by_riga = {}
        ni = 0
        while ni < len(names_in):
            nr = names_in[ni]
            ni = ni + 1
            if not isinstance(nr, dict):
                continue
            riga = nr.get("riga")
            if type(riga) is int and riga not in names_by_riga:
                names_by_riga[riga] = nr
        states_by_riga = {}
        ti = 0
        while ti < len(states_in):
            sr = states_in[ti]
            ti = ti + 1
            if not isinstance(sr, dict):
                continue
            riga = sr.get("riga")
            if type(riga) is int and riga not in states_by_riga:
                states_by_riga[riga] = sr
        # Riga di join: insiemi per ramo, mismatch sempre avvisato.
        sti = 0
        while sti < len(stations):
            station = stations[sti]
            sti = sti + 1
            if not isinstance(station, dict):
                continue
            raws = station.get("variables")
            if not isinstance(raws, list):
                raws = []
            measures_righe = []
            ri = 0
            while ri < len(raws):
                raw = raws[ri]
                ri = ri + 1
                if not isinstance(raw, dict):
                    continue
                riga = raw.get("riga")
                if type(riga) is int and riga not in measures_righe:
                    measures_righe.append(riga)
            if has_names:
                same = True
                if len(names_by_riga) != len(measures_righe):
                    same = False
                else:
                    ki = 0
                    keys = list(names_by_riga.keys())
                    while ki < len(keys):
                        if keys[ki] not in measures_righe:
                            same = False
                        ki = ki + 1
                if not same:
                    warnings.append({"rule": "riga_mismatch",
                                     "page_no": page_no, "riga": None,
                                     "detail": "bitnames rows "
                                     + str(sorted(names_by_riga.keys()))
                                     + " vs measures rows "
                                     + str(sorted(measures_righe))})
                    counters["riga_mismatch"] = counters["riga_mismatch"] + 1
            if has_states:
                same = True
                if len(states_by_riga) != len(measures_righe):
                    same = False
                else:
                    ki = 0
                    keys = list(states_by_riga.keys())
                    while ki < len(keys):
                        if keys[ki] not in measures_righe:
                            same = False
                        ki = ki + 1
                if not same:
                    warnings.append({"rule": "riga_mismatch",
                                     "page_no": page_no, "riga": None,
                                     "detail": "bitstates rows "
                                     + str(sorted(states_by_riga.keys()))
                                     + " vs measures rows "
                                     + str(sorted(measures_righe))})
                    counters["riga_mismatch"] = counters["riga_mismatch"] + 1
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
                                 "detail": "righe measures senza riga: "
                                 "join rami impossibile"})
            # Variabili tenute dopo scarti V2/V20/V21 e join rami.
            kept = []
            ri = 0
            while ri < len(raws):
                raw = raws[ri]
                ri = ri + 1
                if not isinstance(raw, dict):
                    counters["righe_non_valide"] = counters.get(
                        "righe_non_valide", 0) + 1
                    continue
                # Lettura canonica description: solo chiave description.
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
                # V2: vuota, "/" , spare o intestazioni (match esatto).
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
                # V21: zona hardware (mai usata come nome).
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
                # V20: annotazione di esclusione (chiave "note" o alias).
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
                # Ramo nomi-bit vince su bit e registro.
                if (has_names and type(riga) is int
                        and riga in names_by_riga):
                    nb = names_by_riga[riga]
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
                        warnings.append({"rule": "bit_register_mismatch",
                                         "page_no": page_no, "riga": riga,
                                         "detail": "riga " + str(riga) + ": "
                                         + "; ".join(diffs)
                                         + " (vince nomi-bit)"})
                        counters["bit_register_mismatch"] = counters.get(
                            "bit_register_mismatch", 0) + 1
                        var["modbus_register"] = nb.get("modbus_register")
                        var["bit"] = nb.get("bit")
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
                    if nb_desc != var.get("description"):
                        warnings.append({"rule": "descrizione_mismatch",
                                         "page_no": page_no, "riga": riga,
                                         "detail": "riga " + str(riga)
                                         + ": misure="
                                         + str(var.get("description"))
                                         + " nomi-bit=" + str(nb_desc)
                                         + " (vince misure)"})
                        counters["descrizione_mismatch"] = counters.get(
                            "descrizione_mismatch", 0) + 1
                # Ramo stati vince su state_on/state_off.
                if (has_states and type(riga) is int
                        and riga in states_by_riga):
                    st = states_by_riga[riga]
                    for sf in ("state_on", "state_off"):
                        if (var.get(sf) is not None
                                and st.get(sf) != var.get(sf)):
                            warnings.append({"rule": "stati_mismatch",
                                             "page_no": page_no,
                                             "riga": riga,
                                             "detail": "riga " + str(riga)
                                             + ": " + sf + " misure="
                                             + str(var.get(sf)) + " stati="
                                             + str(st.get(sf))
                                             + " (vince stati)"})
                            counters["stati_mismatch"] = counters.get(
                                "stati_mismatch", 0) + 1
                        var[sf] = st.get(sf)
                kept.append(var)
            # Chiave stazione: reale per IP, mai fusi i placeholder.
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
                                     + " applicato (carry-over, "
                                     "verificare sul PDF)"})
                    counters["registri_applicati"] = counters["registri_applicati"] + 1
                slot["variables"].append(var)
        oi = oi + 1
    # Join scale per tag: riempie solo i null, mai sovrascrive.
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
        # Fold packed: singoli con registro condiviso -> impaccato.
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
        # Duplicati mantenuti (trasformazione a valle, mai scarti qui).
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
