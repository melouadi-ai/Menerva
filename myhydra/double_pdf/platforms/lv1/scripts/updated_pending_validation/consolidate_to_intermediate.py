import json


# Pytool LV1 Double PDF: consolida i rami Station e Measurement nell'intermedio VLM.
# Legge gli array aggregati dalle due iniezioni LV2 e le pagine Density in forwarding.
# Output: {"stations": [...]} pronto per json_creator, più density, scarti e review.
# CONFIG CANVAS (verificato 05-10-2026): i tre indici puntano agli edge reali
# 10 = iniezione Station, 11 = iniezione Measurement, 12 = Density.
# Dopo ogni ricablaggio aggiornare i numeri qui e nella scheda nodo.
station_raw = r'''{edge}[10]'''.strip()
measure_raw = r'''{edge}[11]'''.strip()
density_raw = r'''{edge}[12]'''.strip()

try:
    station_data = json.loads(station_raw)
    while isinstance(station_data, str):
        station_data = json.loads(station_data)
    measure_data = json.loads(measure_raw)
    while isinstance(measure_data, str):
        measure_data = json.loads(measure_data)
    density_data = json.loads(density_raw)
    while isinstance(density_data, str):
        density_data = json.loads(density_data)

    if isinstance(station_data, dict):
        station_data = [station_data]
    if isinstance(measure_data, dict):
        measure_data = [measure_data]
    if isinstance(density_data, dict):
        density_data = [density_data]
    if not isinstance(station_data, list):
        raise ValueError("Il ramo Station non contiene un array di pagine.")
    if not isinstance(measure_data, list):
        raise ValueError("Il ramo Measurement non contiene un array di pagine.")
    if not isinstance(density_data, list):
        raise ValueError("Il ramo Density non contiene un array di pagine.")

    review = []
    counters = {
        "station_pages": 0,
        "measurement_pages": 0,
        "density_pages": 0,
        "variables_total": 0,
        "scales_linked": 0,
        "scales_unmatched": 0,
        "duplicate_measures_kept": 0,
    }

    # Configurazioni stazione: primo valore non nullo per campo; IP distinti.
    station_name = None
    station_point = None
    station_protocol = None
    station_ips = []
    station_port = None
    scale_rows = []
    station_index = 0
    while station_index < len(station_data):
        station_page = station_data[station_index]
        if not isinstance(station_page, dict):
            station_index += 1
            continue
        counters["station_pages"] += 1
        info_list = station_page.get("station_info")
        if not isinstance(info_list, list):
            station_index += 1
            continue
        info_pos = 0
        while info_pos < len(info_list):
            info = info_list[info_pos]
            if not isinstance(info, dict):
                info_pos += 1
                continue
            if station_name is None and isinstance(info.get("nome_stazione"), str) and info.get("nome_stazione", "").strip():
                station_name = info["nome_stazione"].strip()
            if station_point is None and isinstance(info.get("stazione"), str) and info.get("stazione", "").strip():
                station_point = info["stazione"].strip()
            if station_protocol is None and isinstance(info.get("protocollo"), str) and info.get("protocollo", "").strip():
                station_protocol = info["protocollo"].strip()
            info_ip = info.get("ip_plc")
            if isinstance(info_ip, str) and info_ip.strip() and info_ip.strip() not in station_ips:
                station_ips.append(info_ip.strip())
            if station_port is None and isinstance(info.get("port"), int):
                station_port = info["port"]
            scale_list = info.get("campi_scala")
            if isinstance(scale_list, list):
                scale_pos = 0
                while scale_pos < len(scale_list):
                    scale_row = scale_list[scale_pos]
                    if isinstance(scale_row, dict):
                        scale_rows.append(scale_row)
                    scale_pos += 1
            info_pos += 1
        station_index += 1

    real_ips = []
    ip_index = 0
    while ip_index < len(station_ips):
        ip_value = station_ips[ip_index]
        if "xxx" not in ip_value and ip_value != ":" and ip_value.strip(".") != "":
            real_ips.append(ip_value)
        ip_index += 1

    chosen_ip = real_ips[0] if real_ips else None
    if len(real_ips) > 1:
        review.append({
            "rule": "multi_plc_unresolved",
            "detail": "IP distinti trovati: " + ", ".join(real_ips)
            + ". Misure attribuite al primo (" + str(chosen_ip)
            + "); caso multi-PLC non coperto dai dati di prova.",
        })
    if station_ips and not real_ips:
        review.append({
            "rule": "placeholder_only",
            "detail": "Solo IP placeholder o assenti: " + ", ".join(station_ips),
        })

    # Misure dalle pagine assemblate, in ordine di sequenza.
    ordered_pages = []
    page_index = 0
    while page_index < len(measure_data):
        measure_page = measure_data[page_index]
        if isinstance(measure_page, dict) and measure_page.get("diagnostic") == "LV2_MEASUREMENT_ASSEMBLY":
            if measure_page.get("status") != "OK":
                raise ValueError(
                    "Pagina assemblata in errore (seq "
                    + str((measure_page.get("page") or {}).get("sequence_index"))
                    + "): " + str(measure_page.get("error", "senza dettagli"))
                )
            inner = measure_page.get("page")
            page_review = measure_page.get("review")
            if isinstance(inner, dict):
                ordered_pages.append((inner.get("sequence_index"), inner, page_review))
        elif isinstance(measure_page, dict) and isinstance(measure_page.get("stations"), list):
            ordered_pages.append((measure_page.get("sequence_index"), measure_page, []))
        else:
            raise ValueError(
                "Record measurement non riconosciuto in posizione " + str(page_index) + "."
            )
        page_index += 1

    seq_pos = 0
    while seq_pos < len(ordered_pages):
        swap_pos = seq_pos
        while swap_pos < len(ordered_pages):
            first_seq = ordered_pages[seq_pos][0]
            other_seq = ordered_pages[swap_pos][0]
            if isinstance(other_seq, int) and (not isinstance(first_seq, int) or other_seq < first_seq):
                tmp_item = ordered_pages[seq_pos]
                ordered_pages[seq_pos] = ordered_pages[swap_pos]
                ordered_pages[swap_pos] = tmp_item
            swap_pos += 1
        seq_pos += 1

    variables = []
    seen_name_reg = []
    duplicate_pairs = []
    page_review_items = []
    page_pos = 0
    while page_pos < len(ordered_pages):
        seq_value, inner_page, page_review = ordered_pages[page_pos]
        counters["measurement_pages"] += 1
        if isinstance(page_review, list):
            review_pos = 0
            while review_pos < len(page_review):
                review_item = page_review[review_pos]
                if isinstance(review_item, dict):
                    review_item = dict(review_item)
                    review_item["page_sequence"] = seq_value
                page_review_items.append(review_item)
                review_pos += 1
        page_stations = inner_page.get("stations")
        if not isinstance(page_stations, list):
            page_pos += 1
            continue
        station_pos = 0
        while station_pos < len(page_stations):
            station_obj = page_stations[station_pos]
            station_measures = station_obj.get("measures") if isinstance(station_obj, dict) else None
            if not isinstance(station_measures, list):
                station_pos += 1
                continue
            measure_pos = 0
            while measure_pos < len(station_measures):
                measure_obj = station_measures[measure_pos]
                if not isinstance(measure_obj, dict):
                    measure_pos += 1
                    continue
                driver_data = measure_obj.get("DRIVERDATA")
                measure_type = measure_obj.get("TYPE")
                if driver_data == 0 and measure_type == 0:
                    kind_value = "ANALOGICA"
                elif driver_data == 2 and measure_type == 1:
                    kind_value = "DIGITALE_IMPACCATO"
                elif measure_type == 6:
                    kind_value = "DIGITALE_SINGOLO"
                elif driver_data == 1:
                    kind_value = "DIGITALE_SINGOLO"
                else:
                    kind_value = "ANALOGICA"
                if driver_data == 5:
                    read_write_value = "W"
                else:
                    read_write_value = "R"
                variable_obj = {
                    "description": measure_obj.get("NAME"),
                    "units": measure_obj.get("UNITS"),
                    "modbus_register": measure_obj.get("MODBUSREGISTRO"),
                    "bit": measure_obj.get("BIT"),
                    "data_type": None,
                    "kind": kind_value,
                    "read_write": read_write_value,
                    "state_on": measure_obj.get("TEXTON"),
                    "state_off": measure_obj.get("TEXTOFF"),
                    "scale_elec_start": None,
                    "scale_elec_end": None,
                    "scale_eng_start": None,
                    "scale_eng_end": None,
                    "limit_hour": None,
                    "limit_day": None,
                }
                name_reg_key = (measure_obj.get("NAME"), measure_obj.get("MODBUSREGISTRO"))
                if name_reg_key in seen_name_reg:
                    duplicate_pairs.append(str(measure_obj.get("NAME")) + " @ " + str(measure_obj.get("MODBUSREGISTRO")))
                else:
                    seen_name_reg.append(name_reg_key)
                variables.append(variable_obj)
                measure_pos += 1
            station_pos += 1
        page_pos += 1

    if duplicate_pairs:
        review.append({"rule": "duplicate_measures_kept", "detail": "; ".join(duplicate_pairs)})
    review.extend(page_review_items)
    counters["variables_total"] = len(variables)

    # Collega campi scala per tag: esatto oppure NAME == tag + " Raw".
    unmatched_scales = []
    scale_pos = 0
    while scale_pos < len(scale_rows):
        scale_row = scale_rows[scale_pos]
        scale_tag = scale_row.get("tag") if isinstance(scale_row, dict) else None
        linked = False
        if isinstance(scale_tag, str) and scale_tag.strip():
            scale_tag = scale_tag.strip()
            var_pos = 0
            while var_pos < len(variables):
                variable_obj = variables[var_pos]
                var_name = variable_obj.get("description")
                if isinstance(var_name, str) and (var_name == scale_tag or var_name == scale_tag + " Raw"):
                    variable_obj["scale_eng_start"] = scale_row.get("campo_da")
                    variable_obj["scale_eng_end"] = scale_row.get("campo_a")
                    counters["scales_linked"] += 1
                    linked = True
                var_pos += 1
        if not linked:
            unmatched_scales.append(scale_row)
            counters["scales_unmatched"] += 1
        scale_pos += 1
    if unmatched_scales:
        unmatched_tags = []
        unmatched_pos = 0
        while unmatched_pos < len(unmatched_scales):
            unmatched_row = unmatched_scales[unmatched_pos]
            if isinstance(unmatched_row, dict) and unmatched_row.get("tag") not in unmatched_tags:
                unmatched_tags.append(unmatched_row.get("tag"))
            unmatched_pos += 1
        review.append({"rule": "unmatched_scales", "detail": "Tag scala senza misura: " + ", ".join([str(t) for t in unmatched_tags])})

    density_pages = []
    density_pos = 0
    while density_pos < len(density_data):
        density_pages.append(density_data[density_pos])
        density_pos += 1
    counters["density_pages"] = len(density_pages)

    stations_out = [{
        "name": station_name,
        "protocol": station_protocol,
        "ip": chosen_ip,
        "port": station_port,
        "modbus_id": None,
        "variables": variables,
    }]

    result = json.dumps({
        "diagnostic": "LV1_CONSOLIDATOR",
        "status": "OK",
        "stations": stations_out,
        "density_pages": density_pages,
        "unmatched_scales": unmatched_scales,
        "review": review,
        "counters": counters,
    }, ensure_ascii=False)

except Exception as error:
    result = json.dumps(
        {
            "diagnostic": "LV1_CONSOLIDATOR",
            "status": "ERROR",
            "error": str(error),
        },
        ensure_ascii=False,
    )
