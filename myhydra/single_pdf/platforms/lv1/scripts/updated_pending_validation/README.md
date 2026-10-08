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

- `consolidator_canvas.py`: `34192dc8055ac865c9e4c1f4d1b2e59a4367d0fa2f5c78177f40560fa5f20b3b`
- `json_creator_v15_canvas.py`: `c990a12bf500ccfe9f93ba4a0dd7b52daca285a63dabdaf07a39dc0db84696b2`
- `slicer_canvas.py`: `af615ec3d73bcecfeaba7b07c8224c5fd1970be4a4cc1885d7c0887102168f60`
- `merger_canvas.py`: `50614896814d0f7c8d034d868235b9a9857e4973216d72017d14fe0609a2f347`

Byte-identiche alle copie in `../../../pytools/` (pinnato da
`tests/test_single_canvas_hygiene.py`). Se divergono, vince `src/nodes/`
e vanno ricopiate da lì (documentata) e ri-derivate (canvas).
