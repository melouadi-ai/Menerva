# LV2 — estrazione unificata + oracolo (redesign v2)

Ogni giro del motore elabora **una pagina** con **due** VLM in parallelo,
alimentati dalla stessa immagine di LV2-01:

| Istanze | Prompt (Powered identity) | Campo Prompt | Context | Output |
|---|---|---|---|---|
| UNIFIED | [`../../prompt/vlm_unified_v1.md`](../../prompt/vlm_unified_v1.md) | `{edge.media}[N]` | vuoto | `{"righe_viste", "checklist", "stations"}` |
| ORACOLO | [`../../prompt/vlm_oracle_v1.md`](../../prompt/vlm_oracle_v1.md) | `{edge.media}[N]` | `{edge}[M]` = testo di UNIFIED | `{"page_no", "errore_input", 5 categorie}` |

`N` e `M` sono **locali al canvas**: ricontrollarli a ogni rewiring, come
gli `{edge}[N]` dei Pytool (checklist in [`../README.md`](../README.md)).

Due dettagli che hanno già fatto perdere una run:

- **L'ORACOLO deve ricevere il JSON di UNIFIED nel Context.** Senza
  `{edge}[M]` il modello non ha niente da verificare: il prompt v1 ha la
  regola R0 che in quel caso risponde con le liste vuote e
  `errore_input`, e `PAGE_ASSEMBLER` lo porta nel tap come
  `oracolo_input_assente`. Non è un silenzio, ma non è nemmeno una verifica.
- **Il campo Prompt contiene SOLO il token media.** Istruzioni e schema stanno
  in Powered identity, altrimenti il modello le confonde con il contenuto
  dell'immagine.

## Assemblaggio della pagina (LV2-03)

I due output non si possono dare in pasto al consolidatore così come sono:
un blocco con le sole 5 categorie non è né `stations` né `rows`, e
`_group_branches` lo rifiuta (`blocco senza stations ne rows`). Serve un
nodo che li unisca:

- [`../../pytools/page_assembler_canvas.py`](../../pytools/page_assembler_canvas.py)
  (2.960 byte) — due edge: `raw_u = {edge}[2]`, `raw_o = {edge}[5]`.
  Emette `{"page_no", "stations", "verifica", "assemble_warnings"}`.

Regole:

- `stations` non viene mai riscritto (l'oracolo non estrae);
- `verifica` contiene **sempre** le cinque liste, anche quando vuote;
- oracolo muto/illeggibile → `verifica: null` + `assemble_warnings`
  (`oracolo_assente`, `oracolo_non_interpretabile`): la pagina passa
  comunque, con il difetto dichiarato;
- `errore_input` dell'oracolo → warning `oracolo_input_assente`;
- UNIFIED illeggibile → ERROR JSON con traceback, mai blank.

`ORACLE_APPLY` (LV1-04b) legge `verifica` e `assemble_warnings` dall'output
grezzo del motore.

## Perché una sola estrazione

Il redesign v14 divideva la stessa immagine in **tre** estrazioni
(misure, nomi-bit, stati) unite sulla chiave `riga`. Il join posizionale
era fragile: ogni discordanza produceva `riga_mismatch`,
`descrizione_mismatch`, `stati_riallineati` — 62 warning su una run
SIEMENS. Con una sola estrazione la riga è scritta una volta sola e non
esistono rami che possano divergere.

L'ORACOLO **non estrae**: riceve l'immagine e l'output di UNIFIED e
restituisce solo discrepanze con `evidenza` obbligatoria. Non riscrive,
non corregge, non inventa (prompt, regole R1-R5, D1-D6).

## Contratto di uscita verso il LV1

Per ogni pagina, `PAGE_ASSEMBLER` produce:

```json
{"page_no": 1,
 "stations": [{"name", "protocol", "ip", "port", "modbus_id",
               "variables": [...]}],
 "verifica": {"page_no": 1, "mancanti": [], "unita_inventate": [],
              "junk_stati": [], "refusi_corretti": [],
              "ip_dichiarati_non_usati": []},
 "assemble_warnings": []}
```

`stations` è il contratto storico (v14); `verifica` è la novità v2. Il
consolidatore (LV1-04) ignora `verifica`, `ORACLE_APPLY` (LV1-04b) la
applica al consolidato.

## Prompt: correnti e archiviati

Correnti (da incollare nei due visiomaru): `vlm_unified_v1.md`,
`vlm_oracle_v1.md`. Archiviati in [`src/prompts/archive/`](../../../../src/prompts/archive/):
`vlm_measures_v18.md`, `vlm_bitnames_v16.md`, `vlm_bitstates_v19.md`
(i tre rami v14) e i predecessori. Inventario completo e hash in
[`../../prompt/README.md`](../../prompt/README.md).

## Schede dei nodi

- [`../../nodes/lv2_01_content2media.md`](../../nodes/lv2_01_content2media.md)
- [`../../nodes/lv2_02_vlm_parsing_json_principale.md`](../../nodes/lv2_02_vlm_parsing_json_principale.md)
- [`../../nodes/lv2_03_page_assembler.md`](../../nodes/lv2_03_page_assembler.md)
