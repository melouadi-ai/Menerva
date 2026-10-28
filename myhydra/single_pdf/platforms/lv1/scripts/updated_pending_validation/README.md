# LV1 scripts — updated_pending_validation

Revisione di produzione del redesign, pronta da incollare ma **mai eseguita
sul canvas**: la prima run MyHydra resta da fare.

## Quale incollare

- [`consolidator_canvas.py`](consolidator_canvas.py) — nel nodo
  `CONSOLIDATORE` (LV1-04). Placeholder `{edge}[5]`: ricontrollare N al
  rewiring (CONFIG). Emissione via `result`, ERROR JSON mai blank.
- [`json_creator_v15_canvas.py`](json_creator_v15_canvas.py) — nel nodo
  `JSON CREATOR` (LV1-05). Placeholder `{edge}[4]`: ricontrollare N, perché
  l'inserimento del consolidatore sposta gli indici a valle. Emissione via
  `print(output)` (meccanismo legacy, verificato sul canvas dal Double);
  `try/except` globale: mai blank, in errore stampa ERROR JSON.

Sono le copie canvas senza righe-commento (stesso AST delle documentate in
`../../../pytools/`). Non incollare le documentate: superano il budget.

## Verifica

```sh
sha256sum consolidator_canvas.py json_creator_v15_canvas.py slicer_canvas.py merger_canvas.py
```

Hash attesi:

- `consolidator_canvas.py`: `29148f2c13c7ad2182408b7f8222dea954a6b95abaa6bd3677cb70bacc501b87`
- `json_creator_v15_canvas.py`: `f269a48c499fc2d67233f772a5e8306d9d5cf32b7638577610fc2235715a99f4`
- `slicer_canvas.py`: `c008026276addcdc7cd06ca350647a44cfc29bc3930b82f1eb602bb5f19641a0`
- `merger_canvas.py`: `50614896814d0f7c8d034d868235b9a9857e4973216d72017d14fe0609a2f347`

Byte-identiche alle copie in `../../../pytools/` (pinnato da
`tests/test_single_canvas_hygiene.py`). Se divergono, vince `src/nodes/`
e vanno ricopiate da lì (documentata) e ri-derivate (canvas).
