import json

# QUESTION è la finestra originale LV1 con le chiavi Medex.
# EDGE #2 è la classificazione VLM della stessa finestra.
media_raw = r'''{question}'''.strip()
vlm_raw = r'''{edge}[2]'''.strip()

try:
    # Decodifica il JSON esterno e la stringa JSON annidata _medexkeys.
    media_data = json.loads(media_raw)
    if isinstance(media_data, str):
        media_data = json.loads(media_data)

    if isinstance(media_data, dict):
        keys_data = media_data.get("_medexkeys")
    else:
        keys_data = media_data

    if isinstance(keys_data, str):
        keys_data = json.loads(keys_data)
    if isinstance(keys_data, dict):
        keys_data = [keys_data]

    vlm_data = json.loads(vlm_raw)
    if isinstance(vlm_data, str):
        vlm_data = json.loads(vlm_data)

    if not isinstance(keys_data, list):
        raise ValueError("_medexkeys non è una lista di chiavi.")
    if not isinstance(vlm_data, dict) or not isinstance(vlm_data.get("pages"), list):
        raise ValueError("L'edge #2 non contiene l'array pages del VLM.")

    pages_data = vlm_data.get("pages")
    if len(keys_data) != len(pages_data):
        raise ValueError(
            "Conteggio diverso: " + str(len(keys_data)) + " chiavi e "
            + str(len(pages_data)) + " classificazioni."
        )

    allowed_labels = [
        "STATION_INFORMATION",
        "MEASUREMENT_TECHNICAL_DATA",
        "DENSITY_MAP"
    ]
    allowed_document_roles = ["IOL", "JOB", "UNKNOWN"]
    output_pages = []
    seen_indexes = []
    index = 0

    while index < len(pages_data):
        page_data = pages_data[index]
        if not isinstance(page_data, dict):
            raise ValueError("Una classificazione VLM non è un oggetto JSON.")

        local_index = page_data.get("index")
        label = page_data.get("label")
        document_role = page_data.get("document_role", "UNKNOWN")
        if not isinstance(local_index, int) or isinstance(local_index, bool):
            raise ValueError("Index VLM non intero.")
        if local_index < 0 or local_index >= len(keys_data):
            raise ValueError("Index VLM fuori dall'intervallo delle chiavi.")
        if local_index in seen_indexes:
            raise ValueError("Index VLM duplicato.")
        if label not in allowed_labels:
            raise ValueError("Etichetta VLM non ammessa.")
        if document_role not in allowed_document_roles:
            raise ValueError("Ruolo documento VLM non ammesso.")

        key_data = keys_data[local_index]
        if not isinstance(key_data, dict) or not key_data.get("key"):
            raise ValueError("Chiave Medex assente o non valida.")

        seen_indexes.append(local_index)
        output_pages.append({
            "key": key_data.get("key"),
            "index": local_index,
            "document_role": document_role,
            "label": label
        })
        index += 1

    if len(seen_indexes) != len(keys_data):
        raise ValueError("Manca la classificazione di una o più chiavi.")

    result = json.dumps({
        "status": "OK",
        "pages": output_pages
    }, ensure_ascii=False)

except Exception as error:
    result = json.dumps({
        "status": "ERROR",
        "error": str(error)
    }, ensure_ascii=False)
