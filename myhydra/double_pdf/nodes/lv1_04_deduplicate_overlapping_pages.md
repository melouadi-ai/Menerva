# Nodo LV1-04 — Deduplicazione pagine sovrapposte

- **Tipo/nome canvas:** Pytool `DEDUPLICAZIONE` / `ELIMINAZIONE DUPLICATI` (nodo 4 nella configurazione documentata più recente).
- **Posizione:** dopo l'iniezione iterativa `DOUBLE PDF PAGE CLASSIFIER`, fuori dal ciclo.
- **Input:** edge #3 dal classificatore LV2: output aggregato delle classificazioni per finestra.
- **Script:** [`../platforms/lv1/scripts/in_use/deduplicate_overlapping_pages.py`](../platforms/lv1/scripts/in_use/deduplicate_overlapping_pages.py).
- **Output:** JSON `status`, `page_count`, `review_required`, `warnings` e array `pages` con chiave, sequenza, ruolo e categoria.
- **Collegamento documentato:** edge #4 verso `DISPATCHER PREP`.

## Comportamento

Collassa solo le occorrenze della stessa chiave media prodotte dalle finestre sovrapposte, preservando l'ordine. In caso di categorie discordanti usa la priorità legacy (`DENSITY_MAP` > `STATION_INFORMATION` > `MEASUREMENT_TECHNICAL_DATA`) e registra i valori osservati negli avvisi. In caso di ruoli discordanti usa `UNKNOWN` e registra un avviso. Gli errori nelle iterazioni restano errori bloccanti.

Non identifica il PDF di origine, il numero di pagina stampato e non fonde pagine diverse con contenuto simile.

## Evidenze

- Casi 6 e 7: output MyHydra con 14 e 11 pagine uniche.
- Caso 6 aggiornato: due conflitti di categoria risolti con avviso e `review_required: true`.
- Fixture anonimizzate: [`../tests/case_6/outputs/observed_role_v2_dedup_sanitized.json`](../tests/case_6/outputs/observed_role_v2_dedup_sanitized.json) e [`../tests/case_7/outputs/observed_role_v2_dedup_sanitized.json`](../tests/case_7/outputs/observed_role_v2_dedup_sanitized.json).
- Test locali: [`../tests/test_deduplicate_overlapping_pages.py`](../tests/test_deduplicate_overlapping_pages.py).

Gli indici di edge dipendono dal canvas. Se si riordinano o si aggiungono nodi, aggiornare questa scheda e verificare di nuovo i placeholder prima di incollare il codice.
