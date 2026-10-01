# LV1 — script

## In uso

Questi sono i Pytool del flusso LV1 corrente, verificati nel caso 6/7 o nella run dei filtri. Incollare nel nodo col nome indicato nella scheda [`../../nodes/lv1_05_page_dispatcher.md`](../../nodes/lv1_05_page_dispatcher.md).

| Script | Ruolo |
|---|---|
| [`scripts/in_use/deduplicate_overlapping_pages.py`](scripts/in_use/deduplicate_overlapping_pages.py) | Deduplica per chiave pagina e conserva gli avvisi |
| [`scripts/in_use/prepare_pages_for_dispatch.py`](scripts/in_use/prepare_pages_for_dispatch.py) | Prepara l'array root |
| [`scripts/in_use/filter_station_information_pages.py`](scripts/in_use/filter_station_information_pages.py) | Filtra le pagine Station Information |
| [`scripts/in_use/filter_measurement_technical_data_pages.py`](scripts/in_use/filter_measurement_technical_data_pages.py) | Filtra le pagine Measurement Technical Data |
| [`scripts/in_use/filter_density_map_pages.py`](scripts/in_use/filter_density_map_pages.py) | Filtra Density Map |

## Non collegati al flusso corrente

- [`scripts/parked/dispatch_classified_pages.py`](scripts/parked/dispatch_classified_pages.py): vecchia prova con instradamento tramite stringa e condizioni.
- [`scripts/diagnostics/diagnose_dispatch_injection.py`](scripts/diagnostics/diagnose_dispatch_injection.py) e [`scripts/diagnostics/diagnose_pytool_inputs.py`](scripts/diagnostics/diagnose_pytool_inputs.py): sonde diagnostiche.

