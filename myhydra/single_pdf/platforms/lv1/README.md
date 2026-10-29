# LV1 — catena e script (redesign v14/v15)

## Catena ridisegnata

```text
LV1-01 pdf2png --> LV1-02 media2content --> LV1-03 engine (iterativo)
    --> LV1-04 CONSOLIDATORE (nuovo) --> LV1-05 JSON CREATOR --> JSON ADAS
```

Ogni giro del motore invoca il Livello 2 su una pagina (content2media +
3 rami VLM v14, vedi [`../lv2/`](../lv2/README.md)) e ne accumula il chunk.
Il consolidatore unisce rami e pagine; il creator trasforma in ADAS.

## Quale incollare dove

| Nodo | File da incollare | Placeholder | Stato |
|---|---|---|---|
| LV1-04 CONSOLIDATORE | [`scripts/updated_pending_validation/consolidator_canvas.py`](scripts/updated_pending_validation/consolidator_canvas.py) | `{edge}[5]` (CONFIG: ricontrollare N al rewiring) | Mai incollato: prima run da fare |
| LV1-05 JSON CREATOR | [`scripts/updated_pending_validation/json_creator_v15_canvas.py`](scripts/updated_pending_validation/json_creator_v15_canvas.py) | `{edge}[4]` (ricontrollare N: il consolidatore sposta gli indici a valle) | Mai incollato in questo flusso: prima run da fare |
| SLICE-A/B/C (shard paralleli) | [`scripts/updated_pending_validation/slicer_canvas.py`](scripts/updated_pending_validation/slicer_canvas.py) | `{edge}[6]` + costanti `START`/`END` (CONFIG: una copia per shard) | Nuovo: pilota PROTEC 2, poi SIEMENS |
| MERGER (ricucitura shard) | [`scripts/updated_pending_validation/merger_canvas.py`](scripts/updated_pending_validation/merger_canvas.py) | due `{edge}` (`raw_a`, `raw_b`; per 3 shard: due merger in cascata) | Nuovo: tra motori e CONSOLIDATORE |

Entrambe le copie stanno sotto la soglia di paste (33.245 e 23.595 byte;
guardia test 33.792, 34.365 = rosso certo), senza `def`/`class`/`lambda`, con
gli stessi AST delle versioni documentate (pinnato da
`tests/test_single_canvas_hygiene.py` e dai test di parità dei Task 4/5).
La copia canvas non si edita a mano: la genera
`pytools/render_canvas.py` dalla documentata.

Dopo la prima run validata sul canvas, le copie migrano in
[`scripts/in_use/`](scripts/in_use/README.md).

## Schede dei nodi

- [`../../nodes/lv1_01_pdf2png.md`](../../nodes/lv1_01_pdf2png.md)
- [`../../nodes/lv1_02_media2content.md`](../../nodes/lv1_02_media2content.md)
- [`../../nodes/lv1_03_single_pdf_engine.md`](../../nodes/lv1_03_single_pdf_engine.md)
- [`../../nodes/lv1_04_consolidatore.md`](../../nodes/lv1_04_consolidatore.md)
- [`../../nodes/lv1_05_json_creator.md`](../../nodes/lv1_05_json_creator.md)
