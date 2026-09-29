import json

# QUESTION: finestra originale ricevuta dal ciclo LV1, contenente le chiavi Medex.
# EDGE #2: output del Visiomaru/VLM, con le classificazioni della finestra.
media_raw = r'''{question}'''.strip()
vlm_raw = r'''{edge}[2]'''.strip()

try:
    # Rimuove eventuali fence Markdown senza alterare i contenuti JSON.
    media_raw = media_raw.replace("```json", "").replace("```", "").strip()
    vlm_raw = vlm_raw.replace("```json", "").replace("```", "").strip()

    # Decodifica i due ingressi esterni.
    media_data = json.loads(media_raw)
    vlm_data = json.loads(vlm_raw)

    # Estrae le chiavi Medex anche se _medexkeys è JSON serializzato come stringa
    # o se la piattaforma aggiunge uno o più livelli di lista/serializzazione.
    media_queue = [media_data]
    media_queue_index = 0
    media_keys = []

    while media_queue_index < len(media_queue):
        media_item = media_queue[media_queue_index]
        media_queue_index += 1

        if isinstance(media_item, str):
            media_text = media_item.strip()
            if media_text:
                try:
                    media_queue.append(json.loads(media_text))
                except Exception:
                    pass

        elif isinstance(media_item, list):
            media_subindex = 0
            while media_subindex < len(media_item):
                media_queue.append(media_item[media_subindex])
                media_subindex += 1

        elif isinstance(media_item, dict):
            if "_medexkeys" in media_item:
                media_queue.append(media_item["_medexkeys"])
            elif "key" in media_item:
                media_key = media_item.get("key")
                if isinstance(media_key, str) and media_key.strip():
                    media_keys.append(media_key.strip())

    if not media_keys:
        raise ValueError("Nessuna chiave media trovata in {question} (input LV1).")

    # Estrae l'array pages dal VLM e tollera liste/stringhe JSON annidate.
    vlm_queue = [vlm_data]
    vlm_queue_index = 0
    vlm_pages = []

    while vlm_queue_index < len(vlm_queue):
        vlm_item = vlm_queue[vlm_queue_index]
        vlm_queue_index += 1

        if isinstance(vlm_item, str):
            vlm_text = vlm_item.strip()
            if vlm_text:
                try:
                    vlm_queue.append(json.loads(vlm_text))
                except Exception:
                    pass

        elif isinstance(vlm_item, list):
            vlm_subindex = 0
            while vlm_subindex < len(vlm_item):
                vlm_queue.append(vlm_item[vlm_subindex])
                vlm_subindex += 1

        elif isinstance(vlm_item, dict):
            if isinstance(vlm_item.get("pages"), list):
                pages_subindex = 0
                pages_value = vlm_item.get("pages")
                while pages_subindex < len(pages_value):
                    vlm_pages.append(pages_value[pages_subindex])
                    pages_subindex += 1
            elif "index" in vlm_item and "label" in vlm_item:
                vlm_pages.append(vlm_item)

    if not vlm_pages:
        raise ValueError("Nessuna classificazione 'pages' trovata nell'edge #2.")

    # Indicizza le classificazioni per indice locale alla finestra.
    labels_by_index = {}
    valid_labels = [
        "STATION_INFORMATION",
        "MEASUREMENT_TECHNICAL_DATA",
        "DENSITY_MAP"
    ]

    page_index = 0
    while page_index < len(vlm_pages):
        page_item = vlm_pages[page_index]

        if not isinstance(page_item, dict):
            raise ValueError("Una voce dell'array pages non è un oggetto JSON.")

        local_index = page_item.get("index")
        page_label = page_item.get("label")

        if not isinstance(local_index, int) or isinstance(local_index, bool):
            raise ValueError("L'indice locale di una pagina non è un intero valido.")
        if local_index in labels_by_index:
            raise ValueError("Il VLM ha restituito un indice pagina duplicato.")
        if page_label not in valid_labels:
            raise ValueError("Il VLM ha restituito un'etichetta non prevista.")

        labels_by_index[local_index] = page_label
        page_index += 1

    # Il VLM deve classificare una pagina per ogni chiave ricevuta nella finestra.
    if len(media_keys) != len(vlm_pages):
        raise ValueError(
            "Numero diverso di chiavi media e classificazioni: "
            + str(len(media_keys)) + " chiavi, "
            + str(len(vlm_pages)) + " classificazioni."
        )

    # Abbina ogni chiave alla sua etichetta tramite index locale 0..N-1.
    associated_pages = []
    local_index = 0
    while local_index < len(media_keys):
        if local_index not in labels_by_index:
            raise ValueError(
                "Il VLM non ha restituito la classificazione per index "
                + str(local_index) + "."
            )

        associated_pages.append({
            "key": media_keys[local_index],
            "index": local_index,
            "label": labels_by_index[local_index]
        })
        local_index += 1

    output_data = {
        "status": "OK",
        "pages": associated_pages
    }
    result = json.dumps(output_data, ensure_ascii=False, indent=2)

except Exception as error:
    # Non scartare finestre non valide: restituisci una diagnosi consumabile a valle.
    output_data = {
        "status": "ERROR",
        "error": str(error)
    }
    result = json.dumps(output_data, ensure_ascii=False, indent=2)
