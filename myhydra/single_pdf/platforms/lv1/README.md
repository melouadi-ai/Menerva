# LV1 — catena e script (redesign v2)

## Catena

```text
LV1-01 PDF2PNG --> LV1-02 MEDIA2CONTENT (1 pagina = 1 gruppo)
    --> SLICE-A / SLICE-B / SLICE-C (shard paralleli)
    --> ENGINE A (iterativo, 3 istanze)
    --> MERGE_AB --> MERGE_ABC
    --> CONSOLIDATORE --> ORACLE_APPLY --> JSON CREATOR --> JSON ADAS
```

Ogni giro di `ENGINE A` invoca il Livello 2 su una pagina (`CONTENT2MEDIA` →
`UNIFIED` + `ORACOLO` → `PAGE ASSEMBLER`, vedi
[`../lv2/README.md`](../lv2/README.md)) e ne accumula il chunk. `MERGE_AB` /
`MERGE_ABC` ricuciono gli shard, `CONSOLIDATORE` fonde pagine e stazioni,
`ORACLE_APPLY` applica le correzioni dell'oracolo, `JSON CREATOR` trasforma in
ADAS.

Nel canvas c'è **un solo `ENGINE A` duplicato 3 volte**: le istanze B e C sono
state rimosse, quindi una modifica su A si propaga a tutti e tre i rami.

## Quale incollare dove

| Nodo | File da incollare | Edge | Byte |
|---|---|---|---|
| `SLICE-A/B/C` | [`../../pytools/slicer_canvas.py`](../../pytools/slicer_canvas.py) | `{edge}[N]` + costanti `START`/`END` | 905 |
| `MERGE_AB`, `MERGE_ABC` | [`../../pytools/merger_canvas.py`](../../pytools/merger_canvas.py) | due `{edge}` (`raw_a`, `raw_b`) | 1.980 |
| `CONSOLIDATORE` | [`../../pytools/consolidator_canvas.py`](../../pytools/consolidator_canvas.py) | `{edge}[N]` | 34.113 |
| `ORACLE_APPLY` | [`../../pytools/oracle_apply_canvas.py`](../../pytools/oracle_apply_canvas.py) | due `{edge}` (`raw_c`, `raw_v`) | 6.949 |
| `JSON CREATOR` | [`../../pytools/json_creator_v15_canvas.py`](../../pytools/json_creator_v15_canvas.py) | `{edge}[N]` | 25.299 |

Tutte le copie stanno sotto la guardia di progetto (< 34.300 byte; 34.365 =
rosso certo), senza `def`/`class`/`lambda`, con lo stesso AST delle versioni
documentate (pinnato da `tests/test_single_canvas_hygiene.py` e dai test di
parità). La copia canvas **non si edita a mano**: la genera
[`../../pytools/render_canvas.py`](../../pytools/render_canvas.py).

Gli indici `{edge}[N]` sono **locali al canvas**: vanno riletti a ogni rewiring.
Un indice sbagliato non dà errore, dà un nodo blank. Checklist in
[`../README.md`](../README.md).

## Schede dei nodi

- [`../../nodes/lv1_01_pdf2png.md`](../../nodes/lv1_01_pdf2png.md)
- [`../../nodes/lv1_02_media2content.md`](../../nodes/lv1_02_media2content.md)
- [`../../nodes/lv1_02b_slicer.md`](../../nodes/lv1_02b_slicer.md)
- [`../../nodes/lv1_03_single_pdf_engine.md`](../../nodes/lv1_03_single_pdf_engine.md)
- [`../../nodes/lv1_03b_merger.md`](../../nodes/lv1_03b_merger.md)
- [`../../nodes/lv1_04_consolidatore.md`](../../nodes/lv1_04_consolidatore.md)
- [`../../nodes/lv1_04b_oracle_apply.md`](../../nodes/lv1_04b_oracle_apply.md)
- [`../../nodes/lv1_05_json_creator.md`](../../nodes/lv1_05_json_creator.md)
