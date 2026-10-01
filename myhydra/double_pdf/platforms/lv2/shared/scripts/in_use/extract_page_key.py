import json


# Pytool LV2 Station Information: inoltra al Medex la chiave della pagina corrente.
page_raw = r'''{question}'''.strip()

try:
    page = json.loads(page_raw)
    while isinstance(page, str):
        page = json.loads(page)

    if isinstance(page, list):
        if len(page) != 1:
            raise ValueError("Atteso un solo record pagina nell'iterazione corrente.")
        page = page[0]
        while isinstance(page, str):
            page = json.loads(page)

    if not isinstance(page, dict):
        raise ValueError("L'input non è un record pagina JSON.")

    key = page.get("key")
    if not isinstance(key, str) or not key.strip():
        raise ValueError("Il record pagina non contiene una key valida.")

    # Il Medex content2media riceve la chiave semplice come contenuto.
    result = key.strip()

except Exception as error:
    result = json.dumps({"status": "ERROR", "error": str(error)}, ensure_ascii=False)
