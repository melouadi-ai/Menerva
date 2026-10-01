# Pytools — Double PDF

Gli script sono sorgenti da incollare nei nodi Pytool MyHydra. I placeholder e gli edge sono parte del contratto: ricontrollarli sul canvas se si cambia un collegamento. L'output del nodo deve essere assegnato alla variabile `result`.

## Workflow attivo

| File | Nodo | Input / edge | Output e stato |
|---|---|---|---|
| [`deduplicate_overlapping_pages.py`](deduplicate_overlapping_pages.py) | LV1-04 `DEDUPLICAZIONE` | Output aggregato classificatore, edge #3 | Oggetto LV1 con pagine uniche e avvisi. Eseguito nel runtime sui casi 6 e 7. |
| [`prepare_pages_for_dispatch.py`](prepare_pages_for_dispatch.py) | LV1-05 `DISPATCHER PREP` | Oggetto deduplicato, edge #4 | Array root di record pagina con metadati/avvisi. Verificato in locale e su MyHydra. |
| [`filter_station_information_pages.py`](filter_station_information_pages.py) | LV1-06 filtro Station | Array preparato, edge #5 | Solo pagine `STATION_INFORMATION`, record completi; destinazione LV2 Station. |
| [`filter_measurement_technical_data_pages.py`](filter_measurement_technical_data_pages.py) | LV1-07 filtro Measurement | Array preparato, edge #7 | Solo pagine `MEASUREMENT_TECHNICAL_DATA`, record completi; destinazione LV2 Measurement. |
| [`filter_density_map_pages.py`](filter_density_map_pages.py) | LV1-08 filtro Density | Array preparato, edge #6 | Solo pagine `DENSITY_MAP`, record completi; destinazione Naive forwarding. |
| [`extract_page_key.py`](extract_page_key.py) | LV2 Station nodo 1 `ESTRAI CHIAVE PAGINA` | `{question}`: record pagina corrente | Stringa della chiave da risolvere con Medex. Presente nel percorso testato; ricontrollare se il Medex non risolve la chiave. |
| [`associate_station_extraction_to_page.py`](associate_station_extraction_to_page.py) | LV2 Station nodo 5 `ASSOCIA ESTRAZIONE ALLA PAGINA` | `{question}`: record pagina; edge #3: output VLM | Revisione verificata su MyHydra: accetta array, oggetto singolo o `null`; scarta oggetti senza campi estratti. Mantiene i tipi originali dei metadati. |

I filtri non sono iterativi: restituiscono ciascuno un array di pagine. Le iniezioni LV2 Station e Measurement sono iterative e ricevono i rispettivi array filtrati. La prova runtime dei filtri sul caso 6 ha ripartito gli indici 1–14 in gruppi disgiunti di 6 Station, 7 Measurement e 1 Density.

## Script diagnostici o parcheggiati

| File | Uso |
|---|---|
| [`associate_page_labels_to_media_keys.py`](associate_page_labels_to_media_keys.py) | Associatore classificatore storico per le finestre LV1; usato prima dell'attuale classificatore iniettato. |
| [`dispatch_classified_pages.py`](dispatch_classified_pages.py) | Prova precedente che emette una stringa categoria per pagina per un routing a condizioni esatte; non è nel percorso corrente. |
| [`diagnose_dispatch_injection.py`](diagnose_dispatch_injection.py) | Diagnostica della forma ricevuta dall'iniezione `PAGE DISPATCHER`; non è nel percorso corrente. |
| [`diagnose_pytool_inputs.py`](diagnose_pytool_inputs.py) | Diagnostica grezza dei placeholder e degli edge in ingresso. |

## Compatibilità runtime

Gli script seguono lo stile Pytool usato nel progetto (parsing JSON esplicito, `try/except`, cicli `while`; niente funzioni o classi). Alcuni nodi restituiscono JSON serializzato, mentre il Pytool di estrazione chiave deve restituire la chiave come stringa semplice perché il Medex successivo la usa come `content`. Non aggiungere un wrapper JSON alla chiave senza verificare il comportamento del Medex.
