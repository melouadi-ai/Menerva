import json


# Pytool LV1: riceve l'array root prodotto da DISPATCHER PREP.
input_raw = r'''{edge}[7]'''.strip()
TARGET_LABEL = "MEASUREMENT_TECHNICAL_DATA"

try:
    source = json.loads(input_raw)
    while isinstance(source, str):
        source = json.loads(source)

    if isinstance(source, dict):
        if source.get("status") != "OK":
            raise ValueError(
                "L'input LV1 non è OK: "
                + str(source.get("error", source.get("status", "stato assente")))
            )
        pages = source.get("pages")
    elif isinstance(source, list):
        pages = source
    else:
        raise ValueError("L'input deve essere un array di record pagina.")

    if not isinstance(pages, list):
        raise ValueError("Non è stato trovato un array di pagine.")

    filtered_pages = []
    page_index = 0
    while page_index < len(pages):
        page = pages[page_index]
        if not isinstance(page, dict):
            raise ValueError("La pagina " + str(page_index + 1) + " non è un oggetto JSON.")
        if page.get("label") == TARGET_LABEL:
            filtered_pages.append(page)
        page_index += 1

    result = json.dumps(filtered_pages, ensure_ascii=False)

except Exception as error:
    result = json.dumps({"status": "ERROR", "error": str(error)}, ensure_ascii=False)
