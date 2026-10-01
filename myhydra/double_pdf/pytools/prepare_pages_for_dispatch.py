import json


# Pytool non iterativo tra il deduplicatore LV1 e l'iniezione LV2.
# Verificare l'indice dell'edge entrante sul canvas.
input_raw = r'''{edge}[4]'''.strip()

try:
    source = json.loads(input_raw)
    while isinstance(source, str):
        source = json.loads(source)

    if not isinstance(source, dict):
        raise ValueError("L'input deve essere l'oggetto completo del deduplicatore LV1.")
    if source.get("status") != "OK":
        raise ValueError(
            "Il deduplicatore LV1 è in errore: "
            + str(source.get("error", "errore senza dettagli"))
        )

    pages = source.get("pages")
    if not isinstance(pages, list) or not pages:
        raise ValueError("L'output LV1 non contiene l'array pages.")

    warnings = source.get("warnings", [])
    if not isinstance(warnings, list):
        raise ValueError("Il campo warnings LV1 deve essere un array.")

    warnings_by_key = {}
    warning_index = 0
    while warning_index < len(warnings):
        warning = warnings[warning_index]
        if isinstance(warning, dict) and isinstance(warning.get("key"), str):
            warning_key = warning["key"]
            if warning_key not in warnings_by_key:
                warnings_by_key[warning_key] = []
            warnings_by_key[warning_key].append(warning)
        warning_index += 1

    dispatch_pages = []
    page_index = 0
    while page_index < len(pages):
        page = pages[page_index]
        if not isinstance(page, dict):
            raise ValueError("La pagina " + str(page_index + 1) + " non è un oggetto JSON.")

        key = page.get("key")
        if not isinstance(key, str) or not key.strip():
            raise ValueError("La pagina " + str(page_index + 1) + " non contiene una chiave valida.")

        page_warnings = warnings_by_key.get(key, [])
        dispatch_page = dict(page)
        dispatch_page["review_required"] = (
            len(page_warnings) > 0 or page.get("document_role", "UNKNOWN") == "UNKNOWN"
        )
        dispatch_page["review_warnings"] = page_warnings
        dispatch_pages.append(dispatch_page)
        page_index += 1

    # L'output è intenzionalmente un array root: la sottopiattaforma LV2
    # iterativa deve ricevere ogni record pagina separatamente.
    result = json.dumps(dispatch_pages, ensure_ascii=False)

except Exception as error:
    result = json.dumps({
        "status": "ERROR",
        "error": str(error),
    }, ensure_ascii=False)
