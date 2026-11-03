# LV2 scripts — updated_pending_validation

Una sola copia canvas, pronta da incollare ma **mai eseguita sul canvas**:
la prima run MyHydra resta da fare.

## Quale incollare

- [`page_assembler_canvas.py`](page_assembler_canvas.py) — nel nodo
  `PAGE ASSEMBLER` (LV2-03, nuovo). Due placeholder da ricontrollare al
  rewiring: `raw_u = {edge}[2]` (output del visiomaru `UNIFIED`) e
  `raw_o = {edge}[5]` (output del visiomaru `ORACOLO`). Emette
  `{"page_no", "stations", "verifica", "assemble_warnings"}` via `result`.
  Non riscrive mai `stations`; un oracolo muto diventa un warning
  (`oracolo_assente`), non un silenzio.

E' la copia canvas senza righe-commento (stesso AST della documentata in
[`../../../pytools/page_assembler.py`](../../../pytools/page_assembler.py)).
Non incollare la documentata: il canvas rifiuta i paste oltre ~34 KB.

## Verifica

```sh
sha256sum page_assembler_canvas.py
```

Hash atteso:

- `page_assembler_canvas.py`: `7edd34825b1e8ef473077feeeafdddb037a87915bfb444761d54396e393e283b` (3.108 byte)

Byte-identica alla copia in `../../../pytools/` (pinnata da
`tests/test_single_canvas_hygiene.py`). Se divergono, vince
`pytools/page_assembler.py`: si rigenera con
`python myhydra/single_pdf/pytools/render_canvas.py --write`.
