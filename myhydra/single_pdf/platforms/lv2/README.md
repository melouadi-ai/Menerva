# LV2 — i 3 rami VLM (misure v18 · nomi-bit v16 · stati v19)

Ogni giro del motore elabora **una pagina** con tre estrazioni parallele
della stessa immagine (da LV2-01 content2media). Il join fra rami avviene a
valle nel consolidatore, sulla chiave `riga` (indice fisico di riga, buche
comprese: è il contratto comune ai tre rami).

| Ramo | Prompt (Powered identity) | Prompt (campo) | Context | Self-check |
|---|---|---|---|---|
| Misure + dati tecnici | [`prompts/current/vlm_measures_v18.md`](prompts/current/vlm_measures_v18.md) | `{edge.media}[N]` | vuoto | `checklist` + `righe_viste` prima delle variabili; nessuna variabile senza cella descrizione |
| Nomi-bit | [`prompts/current/vlm_bitnames_v16.md`](prompts/current/vlm_bitnames_v16.md) | `{edge.media}[N]` | vuoto | solo registro/bit/descrizione + `riga`; bit solo da suffisso/N.Bit |
| Stati TEXTON/TEXTOFF | [`prompts/current/vlm_bitstates_v19.md`](prompts/current/vlm_bitstates_v19.md) | `{edge.media}[N]` | vuoto | `checklist` + `digitali_visti` prima degli stati; copie esatte + `riga` |

`N` negli `{edge.media}[N]` è locale al canvas: ricontrollarlo al rewiring
come gli `{edge}[N]` dei Pytool (checklist in [`../README.md`](../README.md)).

Layout ammessi (entrambi verificati): token media dentro il testo del campo
Prompt insieme alle istruzioni (legacy-inline), oppure token solo in Prompt
e istruzioni in Powered identity con Context vuoto. Il colpevole dei gusci
vuoti era l'input del Medex, mai il layout.

Precedenza su disaccordo fra rami (fissata nel consolidatore, mai silenzio —
ogni disaccordo è un warning): nomi-bit vince bit/registro **solo a
descrizioni concordi** (altrimenti tengono le misure, `riga_disallineata`);
due rami contro uno ripristinano la versione fedele (`refuso_maggioranza`);
misure tutto il resto; stati vincono `state_on`/`state_off` **solo a
descrizione concorde** (`stati_disallineati` altrimenti).

## Versioni correnti

La tabella completa delle versioni (e la storia di ogni regola) sta in
[`../../prompt/README.md`](../../prompt/README.md). In breve:

- **misure**: v13 (ramo unico) → v14 split → v15 riga/check-key → v16
  checklist → v17 BIT SOURCE → **v18** vietate le variabili senza descrizione;
- **nomi-bit**: v14 → v15 → **v16** (V30);
- **stati**: v14 → v15 → v16 → v17 → v18 → **v19**.

## Schede dei nodi

- [`../../nodes/lv2_01_content2media.md`](../../nodes/lv2_01_content2media.md)
- [`../../nodes/lv2_02_vlm_parsing_json_principale.md`](../../nodes/lv2_02_vlm_parsing_json_principale.md)
