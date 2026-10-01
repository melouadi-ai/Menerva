# LV2 Measurement Technical Data

La sottopiattaforma esegue tre estrazioni parallele della stessa pagina iterativa.

| Ramo | Prompt | Context | Powered identity |
|---|---|---|---|
| Misure e BISON | `{edge.media}[2]` | vuoto | [`prompts/current/measurement_measures_bison_v3.md`](prompts/current/measurement_measures_bison_v3.md) |
| Bitinfo e nomi | `{edge.media}[3]` | vuoto | [`prompts/current/measurement_bitinfo_names_v3.md`](prompts/current/measurement_bitinfo_names_v3.md) |
| Stati TEXTON/TEXTOFF | `{edge.media}[4]` | vuoto | [`prompts/current/measurement_bitinfo_states_v3.md`](prompts/current/measurement_bitinfo_states_v3.md) |

## Stato

I tre VLM, i Pytool etichettatori e i Naive di debug sono presenti nel canvas. Le Powered identity v3 separano il token immagine dalle istruzioni; non sono ancora state verificate in una run con questa configurazione.

## Script Pytool

I tre script etichettatori preparano payload distinguibili e conservano il contesto pagina. Sono in [`scripts/updated_pending_validation/`](scripts/updated_pending_validation/), perché la run non ha ancora verificato i payload di uscita. La chiave pagina è estratta con l'utility condivisa [`../shared/scripts/in_use/extract_page_key.py`](../shared/scripts/in_use/extract_page_key.py).

I prompt v1/v2 sono in [`prompts/history/`](prompts/history/). La struttura dei collegamenti e gli edge sono descritti in [`../../../nodes/lv2_06_measurement_extraction_design.md`](../../../nodes/lv2_06_measurement_extraction_design.md).
