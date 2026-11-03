# LV1 scripts — updated_pending_validation

Revisione di produzione del redesign, pronta da incollare ma **mai eseguita
sul canvas**: la prima run MyHydra resta da fare.

## Quale incollare

- [`consolidator_canvas.py`](consolidator_canvas.py) — nel nodo
  `CONSOLIDATORE` (LV1-04). Placeholder `{edge}[5]`: ricontrollare N al
  rewiring (CONFIG). Emissione via `result`, ERROR JSON mai blank.
- [`oracle_apply_canvas.py`](oracle_apply_canvas.py) — nel nodo
  `ORACLE_APPLY` (LV1-04b, nuovo). Due placeholder da ricontrollare al
  rewiring: `raw_c = {edge}[6]` (consolidato) e `raw_v = {edge}[7]`
  (output grezzo del motore, con `verifica`). Applica solo aggiungi/annulla
  con `_audit_oracolo`; refusi e IP restano warning.
- [`json_creator_v15_canvas.py`](json_creator_v15_canvas.py) — nel nodo
  `JSON CREATOR` (LV1-05). Placeholder `{edge}[4]`: ricontrollare N, perché
  l'inserimento del consolidatore sposta gli indici a valle. Emissione via
  `print(output)` (meccanismo legacy, verificato sul canvas dal Double);
  `try/except` globale: mai blank, in errore stampa ERROR JSON.

Sono le copie canvas senza righe-commento (stesso AST delle documentate in
`../../../pytools/`). Non incollare le documentate: superano il budget.

## Verifica

```sh
sha256sum consolidator_canvas.py oracle_apply_canvas.py json_creator_v15_canvas.py slicer_canvas.py merger_canvas.py
```

Hash attesi:

- `consolidator_canvas.py`: `8d3c7d67a9fca15a52be226526ee225cbc8f63f4e1b876c2edca9fd40d61e1cc`
- `json_creator_v15_canvas.py`: `0768c752b5c18ac6852bed693619b21ff6ae91d052e3e67b815b3944e1bbe200`
- `oracle_apply_canvas.py`: `0eae5b65a3361d0992f9d2aaa2b33e3bc34f2c57ac0b5629dd5e46a9776489b2` (6.410 byte)
- `slicer_canvas.py`: `c008026276addcdc7cd06ca350647a44cfc29bc3930b82f1eb602bb5f19641a0`
- `merger_canvas.py`: `50614896814d0f7c8d034d868235b9a9857e4973216d72017d14fe0609a2f347`

Byte-identiche alle copie in `../../../pytools/` (pinnato da
`tests/test_single_canvas_hygiene.py`). Se divergono, vince `src/nodes/`
e vanno ricopiate da lì (documentata) e ri-derivate (canvas).
