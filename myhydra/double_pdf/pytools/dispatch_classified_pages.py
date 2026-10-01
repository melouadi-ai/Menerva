import json


# Questo codice va nel Pytool interno alla sottopiattaforma LV2 Dispatcher.
# L'iniezione iterativa deve consegnare una pagina per esecuzione.
input_raw = r'''{question}'''.strip()

ALLOWED_LABELS = (
    "STATION_INFORMATION",
    "MEASUREMENT_TECHNICAL_DATA",
    "DENSITY_MAP",
)

try:
    input_data = json.loads(input_raw)
    while isinstance(input_data, str):
        input_data = json.loads(input_data)

    # Accetta un record singolo, un record incapsulato in una lista, oppure
    # l'oggetto LV1 con una sola pagina esposto dal ciclo iterativo.
    if isinstance(input_data, list):
        if len(input_data) != 1:
            raise ValueError(
                "Il dispatcher deve ricevere una pagina per iterazione; ricevuti "
                + str(len(input_data)) + " elementi."
            )
        input_data = input_data[0]
        while isinstance(input_data, str):
            input_data = json.loads(input_data)

    if not isinstance(input_data, dict):
        raise ValueError("L'input del dispatcher deve essere un record pagina JSON.")

    if input_data.get("status") == "ERROR":
        raise ValueError(
            "L'input LV1 è in errore: "
            + str(input_data.get("error", "errore senza dettagli"))
        )

    if isinstance(input_data.get("pages"), list):
        if len(input_data["pages"]) != 1:
            raise ValueError(
                "Il dispatcher deve ricevere una pagina per iterazione; ricevute "
                + str(len(input_data["pages"])) + " pagine."
            )
        page = input_data["pages"][0]
    else:
        page = input_data

    if not isinstance(page, dict):
        raise ValueError("Il record della pagina non è un oggetto JSON.")
    if not isinstance(page.get("key"), str) or not page["key"].strip():
        raise ValueError("Il record della pagina non contiene una chiave media valida.")

    label = page.get("label")
    if label not in ALLOWED_LABELS:
        raise ValueError(
            "Categoria non ammessa per la chiave " + page["key"] + ": " + str(label)
        )

    # L'output deve corrispondere letteralmente al valore configurato
    # nell'edge condizionale, senza JSON, virgolette o testo aggiuntivo.
    result = label

except Exception as error:
    # Un errore non deve corrispondere a nessuna condizione di categoria.
    result = "ERROR: " + str(error)
