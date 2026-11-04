# Nodo LV2-03 — PAGE ASSEMBLER (nuovo, redesign v2)

- **Tipo/nome:** Pytool — unisce i due output VLM in una pagina.
- **Input (due edge, ricontrollare N a ogni rewiring):**
  - `raw_u = r'''{edge}[2]'''` — output del visiomaru `UNIFIED`
    (`{"righe_viste", "checklist", "stations"}`);
  - `raw_o = r'''{edge}[5]'''` — output del visiomaru `ORACOLO`
    (5 categorie + `errore_input`, schema in `vlm_oracle_v1.md`).
- **CONFIG:** ispezionare le impostazioni di **entrambi** gli edge a ogni
  rewiring (match-condition spurie = wire bloccato in silenzio).
- **Script:** [`../pytools/page_assembler_canvas.py`](../pytools/page_assembler_canvas.py)
  (copia canvas 3.108 byte; documentata in
  [`../pytools/page_assembler.py`](../pytools/page_assembler.py)).
- **Output:** `{"page_no", "stations", "verifica"|null,
  "assemble_warnings": []}` via `result`. Mai blank: in caso di errore
  `result` è un ERROR JSON `{"status": "ERROR", ...}`.

## Perché esiste

Senza questo nodo la catena si rompe in due punti:

1. **L'oracolo non ha un input.** Il secondo visiomaru deve ricevere il
   JSON di UNIFIED nel campo **Context** (`{edge}[M]`); senza, il prompt
   R0 risponde con le liste vuote e `errore_input`.
2. **Il consolidatore rifiuta le 5 categorie.** Un blocco che non ha né
   `stations` né `rows` fa fallire `_group_branches`
   (`blocco senza stations ne rows`): la pagina intera andrebbe persa.

Questo nodo chiude entrambi i buchi: unisce i due output in una pagina
con `verifica` sempre presente (liste anche vuote) e porta gli avvisi
nell'output grezzo del motore, dove `ORACLE_APPLY` li legge.

## Regole

- `stations` **non viene mai riscritto**: l'oracolo non estrae.
- `verifica` contiene sempre le cinque liste; `page_no` viene da UNIFIED,
  o dall'oracolo se UNIFIED non ce l'ha.
- Oracolo muto o illeggibile → `verifica: null` + `assemble_warnings`
  (`oracolo_assente`, `oracolo_non_interpretabile`): la pagina passa
  comunque, con il difetto dichiarato.
- `errore_input` dell'oracolo → warning `oracolo_input_assente`
  (il Context era vuoto: l'oracolo non ha verificato nulla).
- UNIFIED illeggibile → ERROR JSON con traceback, mai blank.

## Posizione nella catena

Dopo i due visiomaru del LV2, prima dell'uscita del sottomotore verso il
LV1. A valle: `MERGE_ABC` → `CONSOLIDATORE` (LV1-04) → `ORACLE_APPLY`
(LV1-04b) → `JSON CREATOR` (LV1-05).

- **Riferimenti:** [`lv2_02_vlm_parsing_json_principale.md`](lv2_02_vlm_parsing_json_principale.md),
  [`lv1_04b_oracle_apply.md`](lv1_04b_oracle_apply.md),
  [`../platforms/lv2/README.md`](../platforms/lv2/README.md),
  [`../verifica_pdf/BENCHMARK_GATE.md`](../verifica_pdf/BENCHMARK_GATE.md)
  (§13-bis).
