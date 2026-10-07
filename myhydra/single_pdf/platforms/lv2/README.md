# LV2 — i 3 rami VLM v14

Ogni giro del motore elabora **una pagina** con tre estrazioni parallele
della stessa immagine (da LV2-01 content2media). Il join fra rami avviene a
valle nel consolidatore, sulla chiave `riga`.

| Ramo | Prompt (Powered identity) | Prompt (campo) | Context | Self-check |
|---|---|---|---|---|
| Misure + dati tecnici | [`prompts/current/vlm_measures_v14.md`](prompts/current/vlm_measures_v14.md) | `{edge.media}[N]` | vuoto | BIT "point-to-cell": ogni bit punta alla propria cella |
| Nomi-bit | [`prompts/current/vlm_bitnames_v14.md`](prompts/current/vlm_bitnames_v14.md) | `{edge.media}[N]` | vuoto | solo registro/bit/descrizione + `riga` |
| Stati TEXTON/TEXTOFF | [`prompts/current/vlm_bitstates_v14.md`](prompts/current/vlm_bitstates_v14.md) | `{edge.media}[N]` | vuoto | `state_on`/`state_off` copie esatte + `riga` |

`N` negli `{edge.media}[N]` è locale al canvas: ricontrollarlo al rewiring
come gli `{edge}[N]` dei Pytool (checklist in [`../README.md`](../README.md)).

Layout ammessi (entrambi verificati): token media dentro il testo del campo
Prompt insieme alle istruzioni (legacy-inline), oppure token solo in Prompt
e istruzioni in Powered identity con Context vuoto. Il colpevole dei gusci
vuoti era l'input del Medex, mai il layout.

Precedenza su disaccordo fra rami (fissata nel consolidatore): nomi-bit
vince bit/registro, misure tutto il resto, stati vince state_on/off. Ogni
disaccordo è un warning, mai silenzio.

## Schede dei nodi

- [`../../nodes/lv2_01_content2media.md`](../../nodes/lv2_01_content2media.md)
- [`../../nodes/lv2_02_vlm_parsing_json_principale.md`](../../nodes/lv2_02_vlm_parsing_json_principale.md)
