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
  `print(output)` (meccanismo legacy, verificato sul canvas dal Double).

Sono le copie canvas senza righe-commento (stesso AST delle documentate in
`../../../pytools/`). Non incollare le documentate: superano il budget.

## Verifica

```sh
sha256sum consolidator_canvas.py json_creator_v15_canvas.py
```

Hash attesi:

- `consolidator_canvas.py`: `6b5f9270adc1d7d4f02c073fef10079ecb118ac5ac781d625a09bc5447acc01e`
- `json_creator_v15_canvas.py`: `0523dab5010fcc6eaa72a5d4ed116d4212e1145d14dd70d5c6b0ddc316187593`

Byte-identiche alle copie in `../../../pytools/` (pinnato da
`tests/test_single_canvas_hygiene.py`). Se divergono, vince `src/nodes/`
e vanno ricopiate da lì (documentata) e ri-derivate (canvas).
