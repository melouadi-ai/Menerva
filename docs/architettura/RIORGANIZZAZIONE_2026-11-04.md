# Riorganizzazione della directory — 4 novembre 2026

Obiettivo: la struttura del repository deve raccontare **il progetto attuale**
(redesign v2: `UNIFIED` + `ORACOLO` + `PAGE_ASSEMBLER` + `ORACLE_APPLY`), e
tutto ciò che appartiene alla versione precedente (3 rami v13–v19, creator
v4.x, run di ottobre) deve stare in un **archivio esplicito**, consultabile
solo come riferimento di qualità da superare.

Regola che vale dopo questa riorganizzazione:

> Fuori da `archive/` c'è solo materiale che si incolla o si esegue **oggi**.
> Dentro `archive/` c'è materiale che **non si incolla e non si esegue**, e
> che serve solo a capire da dove veniamo.

## Mappa dei movimenti

### `myhydra/single_pdf/`

| Prima | Dopo | Perché |
|---|---|---|
| `prompt/vlm_measures_v14..v17`, `bitnames_v14/v15`, `bitstates_v15..v18`, `extraction_v13` | `archive/prompts_v13_v19/` | prompt dei 3 rami, superati dal prompt unico |
| `prompt/history/*` (5 file) | `archive/prompts_v13_v19/` | idem |
| `platforms/lv2/prompts/current/*` (13 file) | **eliminati** | copie byte-identiche di prompt già archiviati: un solo posto per versione |
| `platforms/lv2/prompts/history/*` (7 file) | **eliminati** | idem |
| `platforms/lv1/scripts/updated_pending_validation/*.py` (5) | **eliminati** | duplicati byte-identici di `pytools/*_canvas.py` |
| `platforms/lv2/scripts/updated_pending_validation/*.py` (1) | **eliminato** | idem |
| `platforms/lv1/scripts/{in_use,parked}/README.md` | **eliminati** | cartelle vuote: il paste source è `pytools/` |
| `pytools/json_creator_v4_2/v4_4/v4_5.py` | `archive/pytools_v4/` | versioni del periodo pre-v15 |
| `nodes/backlog_*.md` (3) | `archive/nodes_v14/` | nodi mai costruita |
| `flusso_cloud_osservato.md` | `archive/nodes_v14/` | topologia osservata del flusso v14 |
| `test/caso_2_protec_1/*` + `test/README.md` | `archive/fixtures_v14/` | fixture del vecchio pytool |
| `Outputs MYHYDRA/*` (4) | `archive/outputs_2026_10/` | output delle run di ottobre |
| `PDFs per il confronto/` (8 PDF) | `pdf_input/` | nome parlante: sono gli input |
| `prompt/` | resta, con **solo** `vlm_unified_v1.md` + `vlm_oracle_v1.md` | è il paste source dei due prompt correnti |
| `pytools/` | resta, con **solo** i 6 script v2 (+ copie canvas) e `render_canvas.py` | è il paste source degli script correnti |
| `nodes/` | resta, con **solo** le schede dei nodi v2 + `README.md` indice | |

### `src/`

| Prima | Dopo | Perché |
|---|---|---|
| `src/prompts/vlm_{measures,bitnames,bitstates}_v1x.md`, `vlm_extraction_v11..v13.md` | `src/prompts/archive/` | `src/` è autorevole: la versione corrente resta in radice, lo storico va in archivio |
| `src/prompts/vlm_unified_v1.md`, `vlm_oracle_v1.md` | restano in radice | contratto corrente |
| `src/prompts/legacy/` | resta | già archivio dichiarato |

### Radice del repository

| Prima | Dopo | Perché |
|---|---|---|
| `README project.md` | `docs/architettura/storico/README_project.md` | copia storica del README, non deve competere con `README.md` |
| `README.md` | aggiornato con la **mappa del repository** | punto di ingresso unico |

## Regole mantenute

- `src/` vince sempre sulle copie in `myhydra/` (byte-identiche, hash nei README).
- `legacy/` resta read-only e non viene toccato.
- I test pinnano la struttura: ogni spostamento aggiorna i test nello stesso commit.
- `myhydra/single_pdf/TESTS/` resta la cartella degli artefatti di run (ignorata da git).

## Effetti sui test

- `tests/test_single_canvas_hygiene.py`: le copie canvas sono una sola, in
  `pytools/`; i prompt correnti hanno una sola copia in `myhydra/` (oltre a
  `src/`), mentre lo storico si verifica in `src/prompts/archive/`.
- `tests/test_single_prompt_contracts.py` e `tests/test_single_prompts_v14.py`:
  base dei prompt storici = `src/prompts/archive/`; le asserzioni sui mirror
  storici non hanno più senso (il mirror non esiste) e vengono rimosse.
- `tests/test_casi_reali.py`, `tests/test_single_truth_siemens.py`: percorsi
  aggiornati (`pdf_input/`, `archive/outputs_2026_10/`).
