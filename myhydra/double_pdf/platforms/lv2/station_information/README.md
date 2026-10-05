# LV2 Station Information

## Configurazione corrente

- **Prompt:** `{edge.media}[2]`
- **Context:** vuoto
- **Powered identity:** [`prompts/current/station_information_extraction_v5.md`](prompts/current/station_information_extraction_v5.md) (v5: righe scala con `unita` e limiti; v4 in `prompts/history/`)
- **Stato:** associatore e catena di estrazione verificati in una run precedente; la Powered identity v4 va ancora verificata con i campi VLM separati.

## Script

- [`scripts/in_use/associate_station_extraction_to_page.py`](scripts/in_use/associate_station_extraction_to_page.py): associa l'estrazione al record pagina della `{question}` corrente; la revisione è stata verificata su MyHydra.
- [`../shared/scripts/in_use/extract_page_key.py`](../shared/scripts/in_use/extract_page_key.py): utility condivisa, usata dal nodo Pytool iniziale prima di Medex `content2media`.

Le Powered identity precedenti sono in [`prompts/history/`](prompts/history/). La v2 è quella usata nelle run documentate; v3 e v4 separano il token immagine dalle istruzioni.
