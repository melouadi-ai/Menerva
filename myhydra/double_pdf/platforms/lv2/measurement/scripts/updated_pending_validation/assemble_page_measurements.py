import json
import re


# Pytool LV2 Measurement: assembla per pagina i tre rami.
# Legge il record pagina dall'iterazione {question} e i tre envelope dai tagger.
# CONFIG CANVAS: aggiornare i tre indici dopo ogni ricablaggio (devono puntare
# agli edge tagger -> questo nodo: misure, bitinfo, stati).
page_raw = r'''{question}'''.strip()
meas_raw = r'''{edge}[7]'''.strip()
bitn_raw = r'''{edge}[8]'''.strip()
bits_raw = r'''{edge}[9]'''.strip()

try:
    page = json.loads(page_raw)
    while isinstance(page, str):
        page = json.loads(page)
    if isinstance(page, list):
        if len(page) != 1:
            raise ValueError("Attesa una sola pagina nell'iterazione corrente.")
        page = page[0]
        while isinstance(page, str):
            page = json.loads(page)
    if not isinstance(page, dict):
        raise ValueError("La question non contiene un record pagina JSON.")
    page_key = page.get("key")
    if not isinstance(page_key, str) or not page_key.strip():
        raise ValueError("Il record pagina non contiene una key valida.")

    branch_errors = {}
    branches = {}
    branch_index = 0
    branch_names = ["MEASURES_BISON", "BITINFO_NAMES", "BITINFO_STATES"]
    branch_raws = [meas_raw, bitn_raw, bits_raw]
    while branch_index < 3:
        branch_name = branch_names[branch_index]
        raw = branch_raws[branch_index]
        try:
            parsed = json.loads(raw)
            while isinstance(parsed, str):
                parsed = json.loads(parsed)
            if isinstance(parsed, dict) and "vlm_output" in parsed:
                if isinstance(parsed.get("status"), str) and parsed.get("status") != "OK":
                    raise ValueError(str(parsed.get("error", "branch in errore")))
                branches[branch_name] = parsed.get("vlm_output")
            elif isinstance(parsed, (list, dict)) or parsed is None:
                branches[branch_name] = parsed
            else:
                raise ValueError("Formato branch non riconosciuto.")
        except Exception as branch_error:
            branch_errors[branch_name] = str(branch_error)
        branch_index += 1

    if branch_errors:
        raise ValueError(
            "Rami non leggibili: "
            + "; ".join([k + " (" + v + ")" for k, v in branch_errors.items()])
        )

    review = []
    counters = {
        "dropped_empty_bitinfo": 0,
        "dropped_numeric_bitinfo": 0,
        "dropped_reserved_states": 0,
        "merged_stations": 0,
    }

    measures_data = branches["MEASURES_BISON"]
    if measures_data is None:
        measures_data = []
    if isinstance(measures_data, dict):
        measures_data = [measures_data]
    if not isinstance(measures_data, list):
        raise ValueError("Il ramo misure non contiene un array di stazioni.")

    # Mappa NAME -> BIT dal ramo misure (verificata corretta 6/6 contro PDF).
    pair_bits = {}
    pair_dupes = []
    station_index = 0
    while station_index < len(measures_data):
        station_obj = measures_data[station_index]
        if isinstance(station_obj, dict):
            bit_rows = station_obj.get("bitinfo")
            if isinstance(bit_rows, list):
                bit_index = 0
                while bit_index < len(bit_rows):
                    bit_row = bit_rows[bit_index]
                    if isinstance(bit_row, dict):
                        pair_name = bit_row.get("NAME")
                        pair_bit = bit_row.get("BIT")
                        if isinstance(pair_name, str) and pair_name.strip() and isinstance(pair_bit, int):
                            if pair_name in pair_bits and pair_bits[pair_name] != pair_bit:
                                pair_dupes.append(pair_name + ": " + str(pair_bits[pair_name]) + " vs " + str(pair_bit))
                            if pair_name not in pair_bits:
                                pair_bits[pair_name] = pair_bit
                    bit_index += 1
        station_index += 1
    if pair_dupes:
        review.append({"rule": "duplicate_measure_bits", "detail": "; ".join(pair_dupes)})

    # Unisce oggetti stazione con stesso DRIVERCONFIG (frammenti di una pagina).
    merged = []
    station_index = 0
    while station_index < len(measures_data):
        station_obj = measures_data[station_index]
        if not isinstance(station_obj, dict):
            station_index += 1
            continue
        placed = False
        merged_index = 0
        while merged_index < len(merged):
            if merged[merged_index].get("DRIVERCONFIG") == station_obj.get("DRIVERCONFIG"):
                target_measures = merged[merged_index].get("measures")
                extra_measures = station_obj.get("measures")
                if isinstance(target_measures, list) and isinstance(extra_measures, list):
                    target_measures.extend(extra_measures)
                    counters["merged_stations"] += 1
                    placed = True
                break
            merged_index += 1
        if not placed:
            merged.append({
                "NAME": station_obj.get("NAME"),
                "DRIVERNAME": station_obj.get("DRIVERNAME"),
                "DRIVERCONFIG": station_obj.get("DRIVERCONFIG"),
                "ID": station_obj.get("ID"),
                "measures": list(station_obj.get("measures") or []) if isinstance(station_obj.get("measures"), list) else [],
            })
        station_index += 1

    sme_names = []
    station_index = 0
    while station_index < len(merged):
        station_name = merged[station_index].get("NAME")
        if isinstance(station_name, str):
            normalized = station_name[4:] if station_name.startswith("SME ") else station_name
            if normalized not in sme_names:
                sme_names.append(normalized)
        station_index += 1
    if len(sme_names) > 1:
        review.append({"rule": "station_name_mismatch", "detail": "Nomi stazione diversi nella pagina: " + " | ".join(sme_names)})

    # Indicizza bitinfo per NAME; scarta vuoti e numerici (regole legacy confermate).
    bitinfo_data = branches["BITINFO_NAMES"]
    if bitinfo_data is None:
        bitinfo_data = []
    if isinstance(bitinfo_data, dict):
        bitinfo_data = [bitinfo_data]
    bit_rows_all = []
    station_index = 0
    while station_index < len(bitinfo_data):
        station_obj = bitinfo_data[station_index]
        if isinstance(station_obj, dict):
            bit_list = station_obj.get("bitinfo")
            if isinstance(bit_list, list):
                bit_index = 0
                while bit_index < len(bit_list):
                    bit_rows_all.append(bit_list[bit_index])
                    bit_index += 1
        station_index += 1
    bitinfo_by_name = {}
    bitinfo_dupes = []
    bit_index = 0
    while bit_index < len(bit_rows_all):
        bit_row = bit_rows_all[bit_index]
        if isinstance(bit_row, dict):
            bit_name = bit_row.get("BITNAME")
            if bit_name is None or (isinstance(bit_name, str) and not bit_name.strip()):
                counters["dropped_empty_bitinfo"] += 1
            elif isinstance(bit_name, str) and re.fullmatch(r"[0-9]+", bit_name.strip()):
                counters["dropped_numeric_bitinfo"] += 1
            elif isinstance(bit_name, str):
                if bit_name in bitinfo_by_name:
                    bitinfo_dupes.append(bit_name)
                else:
                    bitinfo_by_name[bit_name] = bit_row
        bit_index += 1
    if bitinfo_dupes:
        seen_dupes = []
        dupe_index = 0
        while dupe_index < len(bitinfo_dupes):
            if bitinfo_dupes[dupe_index] not in seen_dupes:
                seen_dupes.append(bitinfo_dupes[dupe_index])
            dupe_index += 1
        review.append({"rule": "duplicate_bitinfo_names", "detail": "Usata prima occorrenza per: " + "; ".join(seen_dupes)})

    # Indicizza stati per (MEASUREID, BITNO); primo vince a parità di valori.
    states_data = branches["BITINFO_STATES"]
    if states_data is None:
        states_data = []
    if isinstance(states_data, dict):
        states_data = [states_data]
    states_rows_all = []
    station_index = 0
    while station_index < len(states_data):
        station_obj = states_data[station_index]
        if isinstance(station_obj, dict):
            state_list = station_obj.get("bitinfo")
            if isinstance(state_list, list):
                state_index = 0
                while state_index < len(state_list):
                    states_rows_all.append(state_list[state_index])
                    state_index += 1
        station_index += 1
    states_by_key = {}
    states_dupes = []
    state_index = 0
    while state_index < len(states_rows_all):
        state_row = states_rows_all[state_index]
        if isinstance(state_row, dict):
            state_key = (state_row.get("MEASUREID"), state_row.get("BITNO"))
            if state_key in states_by_key:
                prev = states_by_key[state_key]
                if prev.get("TEXTON") != state_row.get("TEXTON") or prev.get("TEXTOFF") != state_row.get("TEXTOFF"):
                    states_dupes.append(str(state_key[0]) + "/" + str(state_key[1]))
            else:
                states_by_key[state_key] = state_row
        state_index += 1
    if states_dupes:
        review.append({"rule": "duplicate_states", "detail": "Valori diversi stessa chiave, usato primo: " + "; ".join(states_dupes)})

    bit_conflicts = []
    unverified_bits = []
    out_stations = []
    all_orphans = []
    station_index = 0
    while station_index < len(merged):
        station_obj = merged[station_index]
        station_measures = station_obj.get("measures")
        if not isinstance(station_measures, list):
            station_measures = []
        out_measures = []
        unmatched_names = []
        measure_names = []
        measure_index = 0
        while measure_index < len(station_measures):
            measure_obj = station_measures[measure_index]
            if isinstance(measure_obj, dict):
                measure_name = measure_obj.get("NAME")
                if isinstance(measure_name, str) and measure_name not in measure_names:
                    measure_names.append(measure_name)
            measure_index += 1
        measure_dupes = []
        measure_index = 0
        while measure_index < len(station_measures):
            measure_obj = station_measures[measure_index]
            if isinstance(measure_obj, dict):
                measure_name = measure_obj.get("NAME")
                if isinstance(measure_name, str):
                    occurrences = 0
                    scan_index = 0
                    while scan_index < len(station_measures):
                        other = station_measures[scan_index]
                        if isinstance(other, dict) and other.get("NAME") == measure_name:
                            occurrences += 1
                        scan_index += 1
                    if occurrences > 1 and measure_name not in measure_dupes:
                        measure_dupes.append(measure_name)
            measure_index += 1
        if measure_dupes:
            review.append({"rule": "duplicate_measure_names", "detail": "; ".join(measure_dupes)})

        bitinfo_names = list(bitinfo_by_name.keys())
        orphan_index = 0
        while orphan_index < len(bitinfo_names):
            orphan_name = bitinfo_names[orphan_index]
            if orphan_name not in measure_names:
                unmatched_names.append(orphan_name)
            orphan_index += 1

        measure_index = 0
        while measure_index < len(station_measures):
            measure_obj = station_measures[measure_index]
            if not isinstance(measure_obj, dict):
                measure_index += 1
                continue
            measure_name = measure_obj.get("NAME")
            driver_data = measure_obj.get("DRIVERDATA")
            bit_value = None
            texton_value = None
            textoff_value = None
            if isinstance(measure_name, str) and measure_name in pair_bits:
                bit_value = pair_bits[measure_name]
            bit_row = bitinfo_by_name.get(measure_name) if isinstance(measure_name, str) else None
            if isinstance(bit_row, dict):
                row_bitno = bit_row.get("BITNO")
                if bit_value is None and isinstance(row_bitno, int):
                    bit_value = row_bitno
                    if driver_data == 2:
                        unverified_bits.append(
                            str(measure_name) + ": BIT " + str(row_bitno) + " solo da bitinfo (non verificato)"
                        )
                elif (isinstance(bit_value, int) and isinstance(row_bitno, int)
                        and bit_value != row_bitno):
                    bit_conflicts.append(
                        str(measure_name) + ": misure=" + str(bit_value)
                        + " bitinfo=" + str(row_bitno) + " (usato " + str(bit_value) + ")"
                    )
                state_key = (bit_row.get("MEASUREID"), row_bitno)
                state_row = states_by_key.get(state_key)
                if isinstance(state_row, dict):
                    texton_value = state_row.get("TEXTON")
                    textoff_value = state_row.get("TEXTOFF")
            elif driver_data != 0:
                review.append({"rule": "missing_bitinfo", "detail": str(measure_name) + " senza riga bitinfo"})
            out_measure = dict(measure_obj)
            out_measure["BIT"] = bit_value
            out_measure["TEXTON"] = texton_value
            out_measure["TEXTOFF"] = textoff_value
            out_measures.append(out_measure)
            measure_index += 1

        orphan_index = 0
        while orphan_index < len(unmatched_names):
            orphan_name = unmatched_names[orphan_index]
            if orphan_name not in all_orphans:
                all_orphans.append(orphan_name)
            orphan_index += 1

        unmatched_rows = []
        orphan_index = 0
        while orphan_index < len(unmatched_names):
            orphan_name = unmatched_names[orphan_index]
            orphan_row = bitinfo_by_name.get(orphan_name)
            orphan_out = dict(orphan_row) if isinstance(orphan_row, dict) else {"BITNAME": orphan_name}
            state_key = (orphan_out.get("MEASUREID"), orphan_out.get("BITNO"))
            state_row = states_by_key.get(state_key)
            if isinstance(state_row, dict):
                orphan_out["TEXTON"] = state_row.get("TEXTON")
                orphan_out["TEXTOFF"] = state_row.get("TEXTOFF")
            unmatched_rows.append(orphan_out)
            orphan_index += 1

        out_stations.append({
            "NAME": station_obj.get("NAME"),
            "DRIVERNAME": station_obj.get("DRIVERNAME"),
            "DRIVERCONFIG": station_obj.get("DRIVERCONFIG"),
            "ID": station_obj.get("ID"),
            "measures": out_measures,
            "bitinfo_unmatched": unmatched_rows,
        })
        station_index += 1

    if bit_conflicts:
        review.append({"rule": "bit_conflicts", "detail": "; ".join(bit_conflicts)})
    if unverified_bits:
        review.append({"rule": "unverified_bits", "detail": "; ".join(unverified_bits)})
    if all_orphans:
        review.append({"rule": "orphan_bitinfo", "detail": "; ".join(all_orphans)})

    matched_state_keys = []
    state_key_list = list(states_by_key.keys())
    state_index = 0
    while state_index < len(state_key_list):
        matched_state_keys.append(state_key_list[state_index])
        state_index += 1
    used_state_keys = []
    station_index = 0
    while station_index < len(out_stations):
        measure_index = 0
        while measure_index < len(out_stations[station_index]["measures"]):
            measure_obj = out_stations[station_index]["measures"][measure_index]
            bit_row = bitinfo_by_name.get(measure_obj.get("NAME")) if isinstance(measure_obj.get("NAME"), str) else None
            if isinstance(bit_row, dict):
                state_key = (bit_row.get("MEASUREID"), bit_row.get("BITNO"))
                if state_key in states_by_key and state_key not in used_state_keys:
                    used_state_keys.append(state_key)
            measure_index += 1
        orphan_index = 0
        while orphan_index < len(out_stations[station_index]["bitinfo_unmatched"]):
            orphan_row = out_stations[station_index]["bitinfo_unmatched"][orphan_index]
            state_key = (orphan_row.get("MEASUREID"), orphan_row.get("BITNO"))
            if state_key in states_by_key and state_key not in used_state_keys:
                used_state_keys.append(state_key)
            orphan_index += 1
        station_index += 1
    reserved_dropped = 0
    state_index = 0
    while state_index < len(matched_state_keys):
        if matched_state_keys[state_index] not in used_state_keys:
            reserved_dropped += 1
        state_index += 1
    counters["dropped_reserved_states"] = reserved_dropped

    page_review_required = page.get("review_required")
    if not isinstance(page_review_required, bool):
        page_review_required = bool(page_review_required)
    if review:
        page_review_required = True

    result = json.dumps({
        "diagnostic": "LV2_MEASUREMENT_ASSEMBLY",
        "status": "OK",
        "page": {
            "key": page_key,
            "sequence_index": page.get("sequence_index"),
            "document_role": page.get("document_role"),
            "label": page.get("label"),
            "stations": out_stations,
            "review_required": page_review_required,
        },
        "review": review,
        "counters": counters,
    }, ensure_ascii=False)

except Exception as error:
    result = json.dumps(
        {
            "diagnostic": "LV2_MEASUREMENT_ASSEMBLY",
            "status": "ERROR",
            "error": str(error),
        },
        ensure_ascii=False,
    )
