# LV2 Measurement Technical Data

La sottopiattaforma esegue tre estrazioni parallele della stessa pagina iterativa.

| Ramo | Prompt | Context | Powered identity |
|---|---|---|---|
| Misure e BISON | `{edge.media}[2]` | vuoto | [`prompts/current/measurement_measures_bison_v3.md`](prompts/current/measurement_measures_bison_v3.md) |
| Bitinfo e nomi | `{edge.media}[3]` | vuoto | [`prompts/current/measurement_bitinfo_names_v3.md`](prompts/current/measurement_bitinfo_names_v3.md) |
| Stati TEXTON/TEXTOFF | `{edge.media}[4]` | vuoto | [`prompts/current/measurement_bitinfo_states_v3.md`](prompts/current/measurement_bitinfo_states_v3.md) |

## Stato

I tre VLM, i Pytool etichettatori e i Naive di debug sono presenti nel canvas. Nel ramo `MEASURES_BISON`, il tagger ha associato correttamente tutte e 7 le risposte alle pagine; nessuna risposta contiene righe estratte. I rami BITINFO/STATES non sono inclusi nell'output ricevuto.

Prossimo test: eseguire una sola run con la [sonda di leggibilità tabella](prompts/diagnostics/measure_table_readability_probe_v1.md), mantenendo `{edge.media}[2]` nel campo Prompt e mettendo temporaneamente il testo della sonda in Powered identity. Non usare il risultato diagnostico per l'output applicativo; dopo la prova ripristinare il prompt di produzione.

## Script Pytool

I tre script etichettatori preparano payload distinguibili e conservano il contesto pagina. Il ramo misure ha confermato che il parsing/tagging funziona; gli script dei rami BITINFO/STATES restano da verificare. I file sono in [`scripts/updated_pending_validation/`](scripts/updated_pending_validation/). La chiave pagina è estratta con l'utility condivisa [`../shared/scripts/in_use/extract_page_key.py`](../shared/scripts/in_use/extract_page_key.py).

L'output Qwen 3.8 anonimizzato è in [`../../../tests/case_6/outputs/observed_lv2_measurement_qwen38_measures_rerun_sanitized.json`](../../../tests/case_6/outputs/observed_lv2_measurement_qwen38_measures_rerun_sanitized.json). I prompt v1/v2 sono in [`prompts/history/`](prompts/history/). La struttura dei collegamenti e il prossimo test diagnostico sono descritti in [`../../../nodes/lv2_06_measurement_extraction_design.md`](../../../nodes/lv2_06_measurement_extraction_design.md).
