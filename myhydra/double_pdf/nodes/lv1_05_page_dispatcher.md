# Nodo LV1-05 — Preparazione e filtri per categoria

Questa scheda documenta il tratto operativo che nel canvas segue la deduplicazione. Il nome storico `page_dispatcher` del file resta per continuità; la sottopiattaforma `PAGE DISPATCHER` con stringhe e condizioni **non** è il routing corrente.

## Preparazione

- **Tipo/nome canvas:** Pytool `DISPATCHER PREP` (nodo 5 nella configurazione documentata più recente).
- **Posizione:** dopo LV1-04 `DEDUPLICAZIONE`.
- **Compito:** trasforma l'oggetto LV1 in un array root di record pagina, propagando avvisi e metadati per l'iniezione e i filtri.
- **Script:** [`../platforms/lv1/scripts/in_use/prepare_pages_for_dispatch.py`](../platforms/lv1/scripts/in_use/prepare_pages_for_dispatch.py).
- **Edge entrante documentato:** #4 dal nodo 4; verificare se cambia il canvas.

## Routing attivo

I tre filtri sono Pytool semplici e non iterativi. Ricevono i record preparati e restituiscono tutte le pagine corrispondenti mantenendo il record originale.

| Nodo canvas | Etichetta esatta | Script | Edge input | Destinazione |
|---|---|---|---:|---|
| 6 | `STATION_INFORMATION` | [`../platforms/lv1/scripts/in_use/filter_station_information_pages.py`](../platforms/lv1/scripts/in_use/filter_station_information_pages.py) | #5 | Iniezione LV2 Station Information, iterativa |
| 7 | `MEASUREMENT_TECHNICAL_DATA` | [`../platforms/lv1/scripts/in_use/filter_measurement_technical_data_pages.py`](../platforms/lv1/scripts/in_use/filter_measurement_technical_data_pages.py) | #7 | Iniezione LV2 Measurement Data, iterativa |
| 8 | `DENSITY_MAP` | [`../platforms/lv1/scripts/in_use/filter_density_map_pages.py`](../platforms/lv1/scripts/in_use/filter_density_map_pages.py) | #6 | Naive forwarding |

Gli indici edge riportati sono quelli usati negli script e verificati nella configurazione documentata. Gli edge sono locali al canvas: prima di modificare i collegamenti o copiare uno script in un canvas diverso, ricontrollare il numero dell'edge sorgente.

## Verifica MyHydra

Nel caso 6, una run dei tre rami ha restituito:

- `DENSITY_MAP`: sequenza 1 (1 record);
- `MEASUREMENT_TECHNICAL_DATA`: sequenze 2, 3, 4, 5, 8, 13, 14 (7 record);
- `STATION_INFORMATION`: sequenze 6, 7, 9, 10, 11, 12 (6 record).

I tre insiemi coprivano ogni indice da 1 a 14 una sola volta. I due record Station alle sequenze 11 e 12 conservavano `review_required: true` e i relativi avvisi di classificazione. Il risultato verifica il filtro e il passaggio delle pagine alle destinazioni, non l'estrazione semantica nelle LV2.

## Dispatcher condizionale parcheggiato

La precedente ipotesi usava un'iniezione `PAGE DISPATCHER` che emetteva una stringa per pagina e attivava tre archi a confronto esatto. Il test runtime ha mostrato difficoltà nel confronto condizionale esatto; la soluzione corrente filtra direttamente i record per `label` in LV1. Gli script storici [`../platforms/lv1/scripts/parked/dispatch_classified_pages.py`](../platforms/lv1/scripts/parked/dispatch_classified_pages.py) e [`../platforms/lv1/scripts/diagnostics/diagnose_dispatch_injection.py`](../platforms/lv1/scripts/diagnostics/diagnose_dispatch_injection.py) restano come materiale diagnostico, ma non vanno inseriti nel flusso operativo attuale. La piattaforma MyHydra corrispondente rimane parcheggiata.
