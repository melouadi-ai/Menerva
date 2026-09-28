# Legacy — Vecchi MAS su MyHydra (punto di riferimento)

Questa cartella contiene i sorgenti dei vecchi flussi GAIA/MAS eseguiti su MyHydra,
usati come **riferimento (ground truth comportamentale)** per il nuovo Menerva MAS.

## Organizzazione: Single PDF vs Double PDF

Il progetto è suddiviso in due casi d'uso, e la repo riflette questa divisione:

| Caso d'uso | Descrizione | Riferimento legacy | Output attuali |
|---|---|---|---|
| **SINGLE PDF** | Un solo PDF di mappatura (tabelle MODBUS). Pipeline attuale già funzionante (prompt v13 + `json_creator` v4.2). | [`single_pdf/`](single_pdf/) — LV1 + LV2 già presenti | [`tests/single_pdf_outputs/`](../tests/single_pdf_outputs/) |
| **DOUBLE PDF** | Coppia di file: **IOL.xxxx.xx.pdf** (mappatura I/O) + **JOB.xxxx.xx.pdf** (lavori/descrizioni), es. CTM Rivoli, Ospedale San Marco Catania, Biogen, Essity (vedi `docs/protocolli/clienti_extra/`). Richiede i nodi mancanti: `pdf_splitter`, `page_classifier`, `merge_pages`. | [`double_pdf/`](double_pdf/) — **da popolare** | ⏳ non ancora avviato |

## Dove incollare i nuovi contenuti legacy

- **LV1 del vecchio Double PDF** → `legacy/double_pdf/LV1/`
  (un file `.txt` per nodo, stesso formato di `legacy/single_pdf/LV1/`: nome nodo + contenuto MyHydra)
- **LV2 del vecchio Double PDF** → `legacy/double_pdf/LV2/`
  (nodi interni all'iterativo: VLM, pytool di merge, ecc.)

Convenzione nomi file (ereditata dal single PDF): `Node <N> <NomeNodo>.txt` per LV1,
`Nodo <N> <NomeNodo>.txt` per LV2.

## Contenuto delle cartelle esistenti

```
legacy/
├── single_pdf/          # Vecchio MAS Single PDF su MyHydra (RIFERIMENTO COMPLETO)
│   ├── LV1/             # 7 nodi orchestratore (MEDEX, iterativo, stations/ports,
│   │                    #   pages merger, JSON creator, remove quotes/brackets/units)
│   └── LV2/             # 10 nodi interni iterativo (VLM paralleli, merge bitinfo, ecc.)
├── double_pdf/          # ⏳ SLOT VUOTO — attende LV1/LV2 del vecchio MAS Double PDF
│   ├── LV1/.gitkeep
│   └── LV2/.gitkeep
├── gaia_scripts/        # Script Python estratti dai vari MAS storici (GAIA/EVA/Visio)
├── python_codes/        # Codice Python sperimentale / versioni intermedie
├── config/              # pyproject.toml legacy
├── main_old.py          # Vecchio entry point
└── misc/                # Appunti/salvataggi estemporanei
```

## Nota sui dataset Double PDF già in repo

I PDF di prova Double PDF sono già presenti in:
- `data/test_inputs/Mappature/Doppio PDF/CTM Rivoli/` (IOL + JOB)
- `data/test_inputs/Mappature/Doppio PDF/Ospedale San Marco Catania/` (IOL + JOB)
- `docs/protocolli/clienti_extra/` (Biogen, Essity, altre varianti CTM)

Output legacy GAIA Double PDF di confronto in `data/test_outputs/`:
`gaia_ctm_rivoli.json`, `gaia_doublefile_result_6/7.json`, `output_multiple_files.json`,
`outputvisiopiufiles.json`, `legacy_multifilesvisio.json`.
