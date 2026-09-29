# Menerva MAS

Menerva converte documenti tecnici di mappatura PLC/SCADA in configurazioni JSON per ADAS. Il progetto combina estrazione assistita da VLM e trasformazioni deterministiche in Python.

## Stato e perimetro

La pipeline **Single PDF corrente** è configurata sulla piattaforma cloud. Gli screenshot e il flusso osservabile sono documentati in [Single PDF cloud corrente](docs/architettura/single_pdf_cloud_corrente.md). La configurazione cloud non è contenuta integralmente in questo repository: i diagrammi documentano i nodi visibili, non i loro prompt o tutta la logica interna.

Questo repository contiene script Python, prompt, modelli, documentazione, materiali legacy e dati di esempio. Alcuni documenti descrivono versioni precedenti e non vanno assunti come stato corrente senza verifica.

## Aree principali

- `src/nodes/`: codice Python, incluso `json_creator.py`; non tutti gli stadi descritti nei documenti sono implementati qui.
- `src/prompts/`: prompt VLM correnti e storici.
- `src/models/`: modelli e validatori Pydantic.
- `legacy/single_pdf/`, `legacy/double_pdf/`: esportazioni testuali di flussi e prompt precedenti, utili come materiale di analisi.
- `docs/contracts/`: contratti JSON proposti per l’intermedio VLM e l’output ADAS.
- `docs/references/materiale_tutor/`: materiali storici ricevuti dal tutor, accompagnati da note di provenienza e cautele.
- `docs/protocolli/`: schemi DB, mappature, richieste e documenti cliente.
- `data/test_inputs/`, `data/test_outputs/`: esempi di input e risultati storici; verificare provenienza e ruolo di ogni file prima di usarlo come ground truth.
- `tests/`: test e strumenti di confronto.

## Doppio PDF

Il nuovo flusso Double PDF è in fase di progettazione. I documenti in `legacy/double_pdf/` descrivono un precedente flusso di classificazione ed estrazione; non definiscono ancora un contratto completo e verificato per abbinare i documenti IOL e JOB e riconciliare i dati tra loro. L’analisi dei materiali e i punti aperti sono raccolti in [Analisi del progetto](docs/architettura/analisi_progetto.md).

I primi casi indicati dal tutor sono le coppie 6 (IOL + descrizione JOB `0139.23`) e 7 (IOL + descrizione JOB `0105.22`): ogni coppia va trattata come un’unica unità di elaborazione. Le copie originali caricate non sono state aggiunte al repository.

La prima architettura a due livelli proposta è descritta in [Double PDF — workflow proposto](docs/architettura/double_pdf_workflow_proposta.md); è una bozza da verificare sulla piattaforma cloud e sui documenti campione.

## Riferimenti

- [Flusso Single PDF cloud corrente](docs/architettura/single_pdf_cloud_corrente.md)
- [Analisi e mappa del progetto](docs/architettura/analisi_progetto.md)
- [Inventario file e copertura della revisione](docs/architettura/inventario_repository.md)
- [Materiali ricevuti dal tutor](docs/references/materiale_tutor/README.md)
- [Decisione sul merge multi-pagina](docs/architettura/ADR-001-merge-multi-page.md)
- [Contratto intermedio VLM](docs/contracts/VLM_INTERMEDIATE.md)
- [Contratto finale ADAS](docs/contracts/ADAS_FINAL.md)

## Ambiente locale

Il repository definisce dipendenze e configurazione in `pyproject.toml`. Per l’ambiente locale usare le istruzioni compatibili con il Python installato e con il lockfile presente. La configurazione cloud del Single PDF non si avvia automaticamente con questi comandi.
