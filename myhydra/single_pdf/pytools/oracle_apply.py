# ORACLE_APPLY - applica le correzioni dell'oracolo al consolidato (redesign v2).
# CONFIG CANVAS: due edge da ricontrollare a ogni rewiring:
#   raw_c = consolidato (nodo CONSOLIDATORE)                    -> {edge}[6]
#   raw_v = output grezzo del motore (con verifica per pagina)  -> {edge}[7]
# Regole (vlm_oracle_v1.md):
#   mancanti                -> si AGGIUNGE la variabile (verbatim + evidenza)
#   unita_inventate         -> si ANNULLA units (null)
#   junk_stati              -> si ANNULLA lo stato (null)
#   refusi_corretti         -> SOLO warning (fedelta': il PDF decide)
#   ip_dichiarati_non_usati -> SOLO warning (mai stazioni inventate)
# Ogni variabile toccata porta _audit_oracolo {azione, campo?, evidenza}.
# Evidenza vuota -> il difetto NON si applica (oracolo_evidenza_vuota).
# Gli avvisi di PAGE_ASSEMBLER (`assemble_warnings`) entrano nel tap come
# `oracolo_assente` / `oracolo_input_assente`: un oracolo non collegato non
# puo' restare in silenzio.
# Fonte autorevole della logica: src/nodes/single_consolidator.py (_oracle_apply).
import json
import traceback
raw_c = r'''{edge}[6]'''
raw_v = r'''{edge}[7]'''
try:
    v14_fields = ("description", "units", "modbus_register", "bit",
                  "data_type", "kind", "read_write", "note", "state_on",
                  "state_off", "scale_elec_start", "scale_elec_end",
                  "scale_eng_start", "scale_eng_end", "limit_hour",
                  "limit_day", "zona", "tag", "pagina", "riga")
    cons = raw_c
    if isinstance(cons, str):
        cons = json.loads(cons.strip())
    if not isinstance(cons, dict) or not isinstance(cons.get("stations"), list):
        raise ValueError("oracle_apply: input consolidato non interpretabile")
    eng = raw_v
    if isinstance(eng, str):
        eng = json.loads(eng.strip())
    # Le verifiche vivono nelle pagine dell'output grezzo del motore.
    verif = []
    # PAGE_ASSEMBLER annota qui i propri avvisi (oracolo assente o input
    # non interpretabile): vanno portati nel tap, non persi.
    assemble = []
    queue = [eng]
    while len(queue) > 0:
        node = queue.pop(0)
        if isinstance(node, dict):
            if isinstance(node.get("verifica"), dict):
                verif.append(node["verifica"])
            if isinstance(node.get("assemble_warnings"), list):
                assemble = assemble + list(node["assemble_warnings"])
            for key in ("pages", "stations", "results", "result", "data"):
                if isinstance(node.get(key), list):
                    queue = list(node[key]) + queue
        elif isinstance(node, list):
            queue = list(node) + queue
    warnings = cons.get("warnings")
    if not isinstance(warnings, list):
        warnings = []
    counters = cons.get("counters")
    if not isinstance(counters, dict):
        counters = {}
    ai = 0
    while ai < len(assemble):
        voce = assemble[ai]
        ai = ai + 1
        if not isinstance(voce, str):
            continue
        regola = "assemble"
        dettaglio = voce
        taglio = voce.find(":")
        if taglio > 0:
            regola = voce[:taglio].strip()
            dettaglio = voce[taglio + 1:].strip()
        warnings.append({"rule": regola, "page_no": None, "riga": None,
                         "detail": dettaglio})
        counters[regola] = counters.get(regola, 0) + 1
    stations = cons["stations"]
    vi = 0
    while vi < len(verif):
        ver = verif[vi]
        vi = vi + 1
        # Indice descrizione -> variabile, per le ricerche del giro.
        vk = {}
        sti = 0
        while sti < len(stations):
            vars_ = stations[sti].get("variables")
            if not isinstance(vars_, list):
                vars_ = []
                stations[sti]["variables"] = vars_
            si = 0
            while si < len(vars_):
                kk = vars_[si].get("description")
                if isinstance(kk, str):
                    vk[" ".join(kk.split()).lower()] = vars_[si]
                si = si + 1
            sti = sti + 1
        # 1. mancanti: si aggiunge solo se non esiste e con evidenza.
        added = []
        mi = 0
        mis = ver.get("mancanti")
        while isinstance(mis, list) and mi < len(mis):
            ent = mis[mi]
            mi = mi + 1
            if not isinstance(ent, dict):
                continue
            ev = ent.get("evidenza")
            dk = ent.get("description")
            kk = " ".join(dk.split()).lower() if isinstance(dk, str) else None
            if not isinstance(ev, str) or not ev.strip():
                warnings.append({"rule": "oracolo_evidenza_vuota",
                                 "page_no": None, "riga": None,
                                 "detail": "mancante senza evidenza"})
                counters["oracolo_evidenza_vuota"] = counters.get(
                    "oracolo_evidenza_vuota", 0) + 1
                continue
            if kk is None or kk in vk or kk in added:
                warnings.append({"rule": "oracolo_duplicato",
                                 "page_no": None, "riga": None,
                                 "detail": str(dk) + " gia' presente"})
                counters["oracolo_duplicato"] = counters.get(
                    "oracolo_duplicato", 0) + 1
                continue
            var = dict.fromkeys(v14_fields)
            var["description"] = dk
            var["modbus_register"] = ent.get("registro")
            var["bit"] = ent.get("bit")
            var["kind"] = "ANALOGICA"
            var["_audit_oracolo"] = {"azione": "aggiunta", "evidenza": ev}
            if len(stations) == 0:
                stations.append({"name": None, "protocol": None, "ip": None,
                                 "port": None, "modbus_id": None,
                                 "variables": []})
            target = stations[0]
            if not isinstance(target.get("variables"), list):
                target["variables"] = []
            target["variables"].append(var)
            vk[kk] = var
            added.append(kk)
            warnings.append({"rule": "oracolo_aggiunta", "page_no": None,
                             "riga": None, "detail": str(dk)})
            counters["oracolo_aggiunta"] = counters.get(
                "oracolo_aggiunta", 0) + 1
        # 2. unita_inventate: si annulla units.
        ui = 0
        uni = ver.get("unita_inventate")
        while isinstance(uni, list) and ui < len(uni):
            ent = uni[ui]
            ui = ui + 1
            if not isinstance(ent, dict):
                continue
            ev = ent.get("evidenza")
            if not isinstance(ev, str) or not ev.strip():
                warnings.append({"rule": "oracolo_evidenza_vuota",
                                 "page_no": None, "riga": None,
                                 "detail": "unita senza evidenza"})
                counters["oracolo_evidenza_vuota"] = counters.get(
                    "oracolo_evidenza_vuota", 0) + 1
                continue
            dk = ent.get("description")
            kk = " ".join(dk.split()).lower() if isinstance(dk, str) else None
            var = vk.get(kk) if kk is not None else None
            if var is None or var.get("units") is None:
                continue
            var["units"] = None
            var["_audit_oracolo"] = {"azione": "annullata",
                                     "campo": "units", "evidenza": ev}
            warnings.append({"rule": "oracolo_annullata", "page_no": None,
                             "riga": None,
                             "detail": str(dk) + " units "
                             + str(ent.get("unita"))})
            counters["oracolo_annullata"] = counters.get(
                "oracolo_annullata", 0) + 1
        # 3. junk_stati: si annulla lo stato.
        ji = 0
        junk = ver.get("junk_stati")
        while isinstance(junk, list) and ji < len(junk):
            ent = junk[ji]
            ji = ji + 1
            if not isinstance(ent, dict):
                continue
            ev = ent.get("evidenza")
            if not isinstance(ev, str) or not ev.strip():
                warnings.append({"rule": "oracolo_evidenza_vuota",
                                 "page_no": None, "riga": None,
                                 "detail": "stato senza evidenza"})
                counters["oracolo_evidenza_vuota"] = counters.get(
                    "oracolo_evidenza_vuota", 0) + 1
                continue
            campo = ent.get("campo")
            if campo not in ("state_on", "state_off"):
                continue
            dk = ent.get("description")
            kk = " ".join(dk.split()).lower() if isinstance(dk, str) else None
            var = vk.get(kk) if kk is not None else None
            if var is None or var.get(campo) is None:
                continue
            var[campo] = None
            var["_audit_oracolo"] = {"azione": "annullata", "campo": campo,
                                     "evidenza": ev}
            warnings.append({"rule": "oracolo_annullata", "page_no": None,
                             "riga": None,
                             "detail": str(dk) + " " + campo + "="
                             + str(ent.get("valore"))})
            counters["oracolo_annullata"] = counters.get(
                "oracolo_annullata", 0) + 1
        # 4. refusi_corretti: solo warning (fedelta', mai sovrascrivere).
        ri = 0
        ref = ver.get("refusi_corretti")
        while isinstance(ref, list) and ri < len(ref):
            ent = ref[ri]
            ri = ri + 1
            if not isinstance(ent, dict):
                continue
            warnings.append({"rule": "oracolo_refuso", "page_no": None,
                             "riga": None,
                             "detail": str(ent.get("description_finale"))
                             + " -> " + str(ent.get("description_pdf"))})
            counters["oracolo_refuso"] = counters.get(
                "oracolo_refuso", 0) + 1
        # 5. ip_dichiarati_non_usati: solo warning (mai stazioni inventate).
        ii = 0
        ips = ver.get("ip_dichiarati_non_usati")
        while isinstance(ips, list) and ii < len(ips):
            ent = ips[ii]
            ii = ii + 1
            if not isinstance(ent, dict):
                continue
            warnings.append({"rule": "oracolo_ip", "page_no": None,
                             "riga": None, "detail": str(ent.get("ip"))})
            counters["oracolo_ip"] = counters.get("oracolo_ip", 0) + 1
    result = json.dumps({"stations": stations, "warnings": warnings,
                         "counters": counters}, ensure_ascii=False)
except Exception as error:
    tb = traceback.format_exc(limit=3).replace("\n", " | ")[:900]
    result = json.dumps({"status": "ERROR", "error": str(error),
                         "tb": tb, "stations": [], "warnings": [],
                         "counters": {}}, ensure_ascii=False)
