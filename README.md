# Menerva MAS

Menerva converte documenti tecnici di mappatura PLC/SCADA in configurazioni JSON
per ADAS. Combina estrazione assistita da VLM e trasformazioni deterministiche in
Python.

## Mappa del repository

| Percorso | Cosa contiene | Stato |
|---|---|---|
| `myhydra/single_pdf/` | flusso **Single PDF redesign v2** (UNIFIED + ORACOLO + PAGE ASSEMBLER + ORACLE_APPLY) | **corrente** |
| `myhydra/double_pdf/` | flusso **Double PDF** (coppia IOL + JOB) | corrente, in sviluppo |
| `src/` | codice e prompt **autorevoli** (`src/nodes/`, `src/prompts/`, `src/models/`) | **fonte di verità** |
| `tests/` | suite root + strumenti di confronto | corrente |
| `docs/` | contratti, architettura, protocolli, materiali del tutor | misto (leggere lo stato dichiarato) |
| `data/` | esempi di input/output storici | misto, verificare provenienza |
| `legacy/` | esportazioni dei flussi precedenti | **read-only** |
| `reports/` | confronti qualità legacy vs attuale | corrente |
| `configs/`, `scripts/`, `logs/` | segnaposto documentati dai rispettivi README | — |

**Regola della struttura:** fuori da una cartella `archive/` c'è solo materiale
che si incolla o si esegue **oggi**; dentro `archive/` c'è materiale che serve
solo come riferimento di qualità da superare. La mappa completa dei movimenti è
in [Riorganizzazione della directory](docs/architettura/RIORGANIZZAZIONE_2026-11-04.md).

## Stato e perimetro

La pipeline **Single PDF** è configurata sulla piattaforma cloud MyHydra. La
configurazione cloud **non** è contenuta integralmente in questo repository: i
diagrammi documentano i nodi visibili, non i loro prompt o tutta la logica
interna. Il flusso osservabile è in
[Single PDF cloud corrente](docs/architettura/single_pdf_cloud_corrente.md).

Al 4 novembre 2026:

- **Single PDF, redesign v2:** progettazione chiusa, canvas cablato (LV1 16 nodi,
  LV2 5 nodi), prima run di collaudo su PROTEC_2. Vedi
  [`myhydra/single_pdf/README.md`](myhydra/single_pdf/README.md).
- **Double PDF:** catena verificata end-to-end sui casi 6 e 7 con Qwen 3.8.
  Vedi [`myhydra/double_pdf/README.md`](myhydra/double_pdf/README.md).
- **Non fatto:** nessun output importato in ADAS reale; decisioni cliente aperte
  su BISON, zeri iniziali, regola V2, nome stazione.

Alcuni documenti descrivono versioni precedenti e non vanno assunti come stato
corrente senza verifica: quelli del Single PDF pre-v2 sono in
[`myhydra/single_pdf/archive/`](myhydra/single_pdf/archive/README.md) e in
[`legacy/`](legacy/).

## Doppio PDF

Il flusso Double PDF abbina un PDF **IOL** e uno **JOB** della stessa unità. Le
copie originali caricate dal cliente non sono nel repository. Le coppie note sono
la 6 (IOL + JOB `0139.23`) e la 7 (IOL + JOB `0105.22`); ogni coppia è un'unica
unità di elaborazione. Architettura e stato in
[Double PDF — workflow](docs/architettura/double_pdf_workflow_proposta.md) e in
[`myhydra/double_pdf/WORKFLOW_DESIGN.md`](myhydra/double_pdf/WORKFLOW_DESIGN.md).

## Riferimenti

- [Flusso Single PDF cloud corrente](docs/architettura/single_pdf_cloud_corrente.md)
- [Riorganizzazione della directory — 4/11/2026](docs/architettura/RIORGANIZZAZIONE_2026-11-04.md)
- [Analisi e mappa del progetto](docs/architettura/analisi_progetto.md)
- [Inventario file e copertura della revisione](docs/architettura/inventario_repository.md)
- [Materiali ricevuti dal tutor](docs/references/materiale_tutor/README.md)
- [Decisione sul merge multi-pagina (ADR-001)](docs/architettura/ADR-001-merge-multi-page.md)
- [Contratto intermedio VLM](docs/contracts/VLM_INTERMEDIATE.md)
- [Contratto finale ADAS](docs/contracts/ADAS_FINAL.md)
- [README storico del progetto](docs/architettura/storico/README_project.md)

## Ambiente locale

Il repository definisce dipendenze e configurazione in `pyproject.toml`. Usa
l'ambiente locale compatibile con il Python installato e con il lockfile.

### Test

Il Python di sistema (`/usr/bin/python3`) **non** ha le dipendenze del progetto:
`pytest` e `pymupdf` esistono solo nel `.venv` (Python 3.10). Lanciare `pytest`
con l'interprete di sistema fallisce con `No module named pytest`: non è un test
rosso, è un interprete sbagliato.

```sh
./run_tests.sh           # suite root (tests/)
./run_tests.sh double    # suite Double PDF (myhydra/double_pdf/tests)
./run_tests.sh all       # entrambe
./run_tests.sh tests/test_multipage.py -k warning   # argomenti extra a pytest
```

`run_tests.sh` usa `.venv/bin/python` e, se il `.venv` manca o non ha `pytest`,
lo ricrea con `uv` da `pyproject.toml` (extra `dev`). In alternativa, a mano:

```sh
.venv/bin/python -m pytest -q
.venv/bin/python -m pytest myhydra/double_pdf/tests -q
```

`pyproject.toml` imposta `testpaths = ["tests"]`, quindi la suite Double va
lanciata con il percorso esplicito.
