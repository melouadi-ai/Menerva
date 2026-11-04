# Schede dei nodi — Single PDF (redesign v2)

Una scheda per nodo del flusso **corrente**: `UNIFIED` + `ORACOLO` al LV2,
`PAGE ASSEMBLER` come assemblatore di pagina, `ORACLE_APPLY` come applicatore
delle correzioni, `JSON CREATOR` v15 come trasformatore finale.

Le schede dei nodi dei 3 rami v14 e i backlog mai costruiti sono in
[`../archive/nodes_v14/`](../archive/nodes_v14/): non si incollano.

## Livello 1 — canvas principale

| Scheda | Nodo | Ruolo |
|---|---|---|
| [`lv1_01_pdf2png.md`](lv1_01_pdf2png.md) | `PDF2PNG` (Medex) | PDF → immagini, una per pagina |
| [`lv1_02_media2content.md`](lv1_02_media2content.md) | `MEDIA2CONTENT` (Medex) | una immagine per gruppo = una pagina per giro |
| [`lv1_02b_slicer.md`](lv1_02b_slicer.md) | `SLICE-A/B/C` (Pytool) | shard 1-10 / 11-20 / 21-fine |
| [`lv1_03_single_pdf_engine.md`](lv1_03_single_pdf_engine.md) | `ENGINE A` (Iterative) | un giro per pagina, invoca il LV2 |
| [`lv1_03b_merger.md`](lv1_03b_merger.md) | `MERGE_AB`, `MERGE_ABC` (Pytool) | ricucitura dei chunk degli shard |
| [`lv1_04_consolidatore.md`](lv1_04_consolidatore.md) | `CONSOLIDATORE` (Pytool) | fonde pagine e stazioni |
| [`lv1_04b_oracle_apply.md`](lv1_04b_oracle_apply.md) | `ORACLE_APPLY` (Pytool) | applica le correzioni dell'oracolo |
| [`lv1_05_json_creator.md`](lv1_05_json_creator.md) | `JSON CREATOR` (Pytool) | consolidato → ADAS |

## Livello 2 — sottomotore

| Scheda | Nodo | Ruolo |
|---|---|---|
| [`lv2_01_content2media.md`](lv2_01_content2media.md) | `CONTENT2MEDIA` (Medex) | chiave media → immagine per il VLM |
| [`lv2_02_vlm_parsing_json_principale.md`](lv2_02_vlm_parsing_json_principale.md) | `UNIFIED` + `ORACOLO` (Visiomaru) | estrazione unica + verifica con evidenza |
| [`lv2_03_page_assembler.md`](lv2_03_page_assembler.md) | `PAGE ASSEMBLER` (Pytool) | unisce i due output in una pagina |

## Regola

Ogni scheda dichiara gli indici `{edge}[N]` come **valori del canvas**:
vanno riletti a ogni rewiring. Un indice sbagliato non produce errori, produce
un nodo blank.
