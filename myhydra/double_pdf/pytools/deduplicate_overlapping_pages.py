import json

# EDGE #3 contiene i risultati aggregati del ciclo Double PDF Engine.
input_raw = r'''{edge}[3]'''.strip()

try:
    input_data = json.loads(input_raw)
    if isinstance(input_data, str):
        input_data = json.loads(input_data)

    if isinstance(input_data, dict):
        input_data = [input_data]
    if not isinstance(input_data, list):
        raise ValueError("L'edge #3 non contiene una lista di risultati iterativi.")

    allowed_labels = [
        "STATION_INFORMATION",
        "MEASUREMENT_TECHNICAL_DATA",
        "DENSITY_MAP"
    ]
    allowed_document_roles = ["IOL", "JOB", "UNKNOWN"]
    label_priority = [
        "DENSITY_MAP",
        "STATION_INFORMATION",
        "MEASUREMENT_TECHNICAL_DATA"
    ]
    output_pages = []
    key_positions = {}
    labels_by_key = {}
    roles_by_key = {}
    iteration_index = 0

    while iteration_index < len(input_data):
        iteration_data = input_data[iteration_index]
        if isinstance(iteration_data, str):
            iteration_data = json.loads(iteration_data)
        if not isinstance(iteration_data, dict):
            raise ValueError("Il risultato iterativo " + str(iteration_index + 1) + " non è un oggetto JSON.")
        if iteration_data.get("status") != "OK":
            raise ValueError(
                "Il risultato iterativo " + str(iteration_index + 1)
                + " non è OK: " + str(iteration_data.get("error", "errore senza dettagli"))
            )

        pages_data = iteration_data.get("pages")
        if not isinstance(pages_data, list):
            raise ValueError("Manca l'array pages nel risultato iterativo " + str(iteration_index + 1) + ".")

        page_index = 0
        while page_index < len(pages_data):
            page_data = pages_data[page_index]
            if not isinstance(page_data, dict):
                raise ValueError("Una pagina del risultato iterativo non è un oggetto JSON.")

            key = page_data.get("key")
            label = page_data.get("label")
            document_role = page_data.get("document_role", "UNKNOWN")
            if not isinstance(key, str) or not key.strip():
                raise ValueError("Una pagina non contiene una chiave media valida.")
            if label not in allowed_labels:
                raise ValueError("Etichetta non ammessa per la chiave " + key + ".")
            if document_role not in allowed_document_roles:
                raise ValueError("Ruolo documento non ammesso per la chiave " + key + ".")

            if key in key_positions:
                if label not in labels_by_key[key]:
                    labels_by_key[key].append(label)
                if document_role not in roles_by_key[key]:
                    roles_by_key[key].append(document_role)
            else:
                key_positions[key] = len(output_pages)
                labels_by_key[key] = [label]
                roles_by_key[key] = [document_role]
                output_pages.append({
                    "key": key,
                    "sequence_index": len(output_pages) + 1,
                    "document_role": document_role,
                    "label": label
                })
            page_index += 1
        iteration_index += 1

    if len(output_pages) == 0:
        raise ValueError("Il ciclo iterativo non ha restituito pagine.")

    # Risolve le categorie discordanti con la priorità esplicita del prompt legacy.
    # Mantiene un avviso con tutti i valori osservati per la revisione.
    warnings = []
    unique_index = 0
    while unique_index < len(output_pages):
        unique_page = output_pages[unique_index]
        unique_key = unique_page["key"]
        observed_labels = labels_by_key[unique_key]
        observed_roles = roles_by_key[unique_key]

        if len(observed_labels) > 1:
            priority_index = 0
            resolved_label = observed_labels[0]
            while priority_index < len(label_priority):
                if label_priority[priority_index] in observed_labels:
                    resolved_label = label_priority[priority_index]
                    break
                priority_index += 1
            unique_page["label"] = resolved_label
            warnings.append({
                "key": unique_key,
                "field": "label",
                "observed": observed_labels,
                "resolved": resolved_label,
                "rule": "legacy_category_priority"
            })

        if len(observed_roles) > 1:
            unique_page["document_role"] = "UNKNOWN"
            warnings.append({
                "key": unique_key,
                "field": "document_role",
                "observed": observed_roles,
                "resolved": "UNKNOWN",
                "rule": "conflicting_role_evidence"
            })
        unique_index += 1

    result = json.dumps({
        "status": "OK",
        "page_count": len(output_pages),
        "review_required": len(warnings) > 0,
        "warnings": warnings,
        "pages": output_pages
    }, ensure_ascii=False)

except Exception as error:
    result = json.dumps({
        "status": "ERROR",
        "error": str(error)
    }, ensure_ascii=False)
