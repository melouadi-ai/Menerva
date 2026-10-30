# LV2 Measurement Technical Data

La sottopiattaforma esegue tre estrazioni parallele della stessa pagina iterativa.

| Ramo | Prompt | Context | Powered identity |
|---|---|---|---|
| Misure e BISON | `{edge.media}[1]` | vuoto | [`prompts/current/measurement_measures_bison_v7.md`](prompts/current/measurement_measures_bison_v7.md) (v7: tabella senza colonna REG → nessuna misura, REG mai da `DBX`/`DBW`/`DBD`; v6 in `prompts/history/`) |
| Bitinfo e nomi | `{edge.media}[2]` | vuoto | [`prompts/current/measurement_bitinfo_names_v3.md`](prompts/current/measurement_bitinfo_names_v3.md) |
| Stati TEXTON/TEXTOFF | `{edge.media}[3]` | vuoto | [`prompts/current/measurement_bitinfo_states_v3.md`](prompts/current/measurement_bitinfo_states_v3.md) |

## Stato

La sottopiattaforma è in uso nei casi 6, 7, 8, 9 e 10. La run5 del caso 6 (29/10/2026, prompt
misure v6) ha chiuso il verdetto: 22 misure, 60 bitinfo, registri `40000 + REG`, limiti in `SQ*`.
Il caso 7 ha chiuso carry-over e unità (40 misure, 47 bitinfo).

Il prompt misure è alla **v7**: una tabella priva di colonna REG (mappa DB50 lato PLC, viste su
Essity) non produce misure; `MODBUSREGISTRO` non si ricava mai da `DBX`/`DBW`/`DBD`. La verifica
attesa è la sparizione delle 3 misure inventate (registri 160/168/192) nella prossima run Essity,
con le 20 misure DB100 intatte. Il prompt va nel **Powered identity**; **Prompt** resta
`{edge.media}[1]` e **Context** vuoto.

La sonda diagnostica di leggibilità in [`prompts/diagnostics/`](prompts/diagnostics/) resta
materiale di debug: non va usata per l'output applicativo.

## Script Pytool

I tre script etichettatori preparano payload distinguibili e conservano il contesto pagina. Il ramo misure ha confermato che il parsing/tagging funziona; gli script dei rami BITINFO/STATES restano da verificare. I file sono in [`scripts/updated_pending_validation/`](scripts/updated_pending_validation/). La chiave pagina è estratta con l'utility condivisa [`../shared/scripts/in_use/extract_page_key.py`](../shared/scripts/in_use/extract_page_key.py).

L'output Qwen 3.8 anonimizzato è in [`../../../tests/case_6/outputs/observed_lv2_measurement_qwen38_measures_rerun_sanitized.json`](../../../tests/case_6/outputs/observed_lv2_measurement_qwen38_measures_rerun_sanitized.json). I prompt v1/v2 sono in [`prompts/history/`](prompts/history/). La struttura dei collegamenti e il prossimo test diagnostico sono descritti in [`../../../nodes/lv2_06_measurement_extraction_design.md`](../../../nodes/lv2_06_measurement_extraction_design.md).
