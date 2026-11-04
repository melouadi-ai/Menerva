# Archivio — versione precedente del Single PDF

Qui dentro c'è la **versione precedente** del flusso Single PDF (VLM a 3 rami,
v13–v19, e le run di ottobre 2026). Non si incolla nel canvas, non si esegue,
non si aggiorna: serve solo come **riferimento di qualità da superare**.

Regola: tutto ciò che sta fuori da `archive/` è materiale corrente.

| Cartella | Contenuto | Stato |
|---|---|---|
| `prompts_v13_v19/` | prompt dei 3 rami (misure, nomi bit, stati) + `vlm_extraction_v13` | superati dal prompt unico `UNIFIED` |
| `pytools_v4/` | `json_creator_v4_2/v4_4/v4_5.py` | superati da `json_creator_v15` |
| `nodes_v14/` | backlog mai costruiti + `flusso_cloud_osservato.md` | riferimento storico |
| `fixtures_v14/` | `caso_2_protec_1/` (input VLM dei 3 rami e output legacy) | riferimento per i confronti |
| `outputs_2026_10/` | output ADAS delle run di ottobre (SMA_1, PROTEC_1/2, SIEMENS_2) | riferimento di qualità |

La copia autorevole dei prompt storici è in
[`../../../src/prompts/archive/`](../../../src/prompts/archive/): questo
archivio contiene solo le copie che erano nel ramo MyHydra.

## Perché è archiviato e non cancellato

Il confronto con il legacy ha valore solo se resta verificabile: i test
`tests/test_adas_caso6_pdf_truth.py` e i report in
[`../verifica_pdf/`](../verifica_pdf/) citano queste run per dimostrare
quali errori la versione nuova non deve reintrodurre. Cancellarle
renderebbe impossibile quel confronto.
