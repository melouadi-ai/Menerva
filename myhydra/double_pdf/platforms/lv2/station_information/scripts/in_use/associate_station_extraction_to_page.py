import json


# Pytool LV2 Station Information: associa l'estrazione VLM alla pagina corrente.
# {question} è il record pagina della singola iterazione; edge #3 è l'output VLM.
page_raw = r'''{question}'''.strip()
vlm_raw = r'''{edge}[3]'''.strip()

try:
    page = json.loads(page_raw)
    while isinstance(page, str):
        page = json.loads(page)

    if isinstance(page, list):
        if len(page) != 1:
            raise ValueError("Attesa una sola pagina nel contesto iterativo.")
        page = page[0]
        while isinstance(page, str):
            page = json.loads(page)

    if not isinstance(page, dict):
        raise ValueError("Il contesto iterativo non è un record pagina.")

    key = page.get("key")
    if not isinstance(key, str) or not key.strip():
        raise ValueError("Il record pagina non contiene una key valida.")

    vlm_data = json.loads(vlm_raw)
    while isinstance(vlm_data, str):
        vlm_data = json.loads(vlm_data)

    if vlm_data is None:
        vlm_data = []
    elif isinstance(vlm_data, dict):
        if vlm_data.get("status") == "ERROR":
            raise ValueError(str(vlm_data.get("error", "Errore restituito dal VLM.")))
        if isinstance(vlm_data.get("station_info"), list):
            vlm_data = vlm_data.get("station_info")
        else:
            schema_fields = [
                "nome_stazione",
                "stazione",
                "protocollo",
                "ip_plc",
                "port",
                "campi_scala",
            ]
            schema_field_index = 0
            matches_station_schema = False
            while schema_field_index < len(schema_fields):
                if schema_fields[schema_field_index] in vlm_data:
                    matches_station_schema = True
                schema_field_index += 1
            if not matches_station_schema:
                raise ValueError("L'oggetto VLM non contiene campi dello schema Station Information.")
            # Recupera il caso in cui il VLM restituisce un singolo oggetto
            # rispettando lo schema dei campi, invece di un array con un elemento.
            vlm_data = [vlm_data]

    if not isinstance(vlm_data, list):
        raise ValueError(
            "L'output VLM deve essere un array JSON, un singolo oggetto stazione o null."
        )

    normalized_station_info = []
    station_index = 0
    while station_index < len(vlm_data):
        station = vlm_data[station_index]
        if not isinstance(station, dict):
            raise ValueError("Un elemento dell'output VLM non è un oggetto JSON.")

        scale_fields = station.get("campi_scala", [])
        if scale_fields is None:
            scale_fields = []
        if not isinstance(scale_fields, list):
            raise ValueError("Il campo campi_scala deve essere un array JSON.")
        scale_index = 0
        while scale_index < len(scale_fields):
            if not isinstance(scale_fields[scale_index], dict):
                raise ValueError("Un elemento di campi_scala non è un oggetto JSON.")
            scale_index += 1

        has_extracted_value = False
        scalar_fields = ["nome_stazione", "stazione", "protocollo", "ip_plc", "port"]
        scalar_index = 0
        while scalar_index < len(scalar_fields):
            field_value = station.get(scalar_fields[scalar_index])
            if field_value is not None:
                if not isinstance(field_value, str) or field_value.strip():
                    has_extracted_value = True
            scalar_index += 1

        if len(scale_fields) > 0:
            has_extracted_value = True

        if has_extracted_value:
            station["campi_scala"] = scale_fields
            normalized_station_info.append(station)

        station_index += 1

    associated_page = dict(page)
    associated_page["station_info"] = normalized_station_info
    result = json.dumps(associated_page, ensure_ascii=False)

except Exception as error:
    error_page = {}
    try:
        parsed_page = json.loads(page_raw)
        while isinstance(parsed_page, str):
            parsed_page = json.loads(parsed_page)
        if isinstance(parsed_page, dict):
            error_page = {
                "key": parsed_page.get("key"),
                "sequence_index": parsed_page.get("sequence_index"),
                "document_role": parsed_page.get("document_role"),
                "label": parsed_page.get("label")
            }
    except Exception:
        error_page = {}

    error_page["status"] = "ERROR"
    error_page["error"] = str(error)
    result = json.dumps(error_page, ensure_ascii=False)
