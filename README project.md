<<<<<<< HEAD
# Menerva MAS — Multi-Agent System

Pipeline per la conversione automatica di documenti di mappatura PLC/SCADA (PDF/Excel) in configurazione ADAS per sistemi di monitoraggio emissioni industriali (SME/SAE).

## 🎯 Obiettivo

Trasformare documenti tecnici (tabelle MODBUS, liste I/O, specifiche ADAS) in file di configurazione pronti per la piattaforma ADAS, eliminando l'inserimento manuale e gli errori di trascrizione.

## 🏗️ Architettura

### Pipeline a 7 stadi

```
PDF/Excel
    │
    ▼
┌─────────────────────────┐
│ Stadio 1: INGESTIONE    │  Python — apre il file, verifica leggibilità
├─────────────────────────┤
│ Stadio 2: SPEZZETTAMENTO│  Python — pagine → immagini (PDF) o righe (Excel)
├─────────────────────────┤
│ Stadio 3: CLASSIFICAZ.  │  VLM — identifica tipo di contenuto per pagina
├─────────────────────────┤
│ Stadio 4: ESTRAZIONE    │  VLM — produce JSON intermedio (stazioni + misure)
├─────────────────────────┤
│ Stadio 5: VALIDAZIONE   │  Pydantic — verifica schema JSON intermedio
├─────────────────────────┤
│ Stadio 6: TRASFORMAZ.   │  Python — JSON intermedio → ADAS finale
├─────────────────────────┤
│ Stadio 7: MERGE         │  Python — unisce stazioni, calcola hex, rinumera ID
└─────────────────────────┘
    │
    ▼
ADAS JSON (formato finale con DRIVERPRIVATE, XML DRIVERCONFIG, VM_SOURCE_CODE)
```

### Separazione delle responsabilità

| Componente | Ruolo |
|---|---|
| **VLM (Qwen-VL)** | Legge e trascrive tabelle dai documenti. Produce JSON intermedio. |
| **Python** | Calcoli deterministici: hex DRIVERPRIVATE, XML DRIVERCONFIG, BISON, merge stazioni, rinumerazione ID. |
| **MyHydra** | Orchestrazione della pipeline completa su PDF reali. |

## 📁 Struttura del progetto

```
Menerva_MAS/
├── src/
│   ├── agents/          # Agenti specializzati (futuro)
│   ├── core/            # Logica core condivisa
│   ├── nodes/           # Singoli stadi della pipeline
│   ├── prompts/         # Prompt VLM
│   │   ├── vlm_extraction_v12.md      ← prompt corrente (v12, con V20-V24)
│   │   ├── vlm_extraction_v11.md      ← prompt precedente (v11)
│   │   └── legacy/      # Prompt precedenti (v10bis, Visio, GAIA, EVA)
│   └── models/          # Modelli Pydantic per validazione
│       ├── vlm_schema.py  # Schemi VLM intermedio + ADAS finale
│       └── validators.py  # Funzioni di validazione sicura
│   └── utils/           # Funzioni di utilità
├── configs/             # Configurazioni esterne
├── data/
│   ├── test_inputs/     # PDF di test
│   └── test_outputs/    # Output attesi (ground truth)
├── docs/
│   ├── architettura/    # Documentazione architetturale
│   ├── contracts/       # Schemi JSON dei contratti tra stadi
│   ├── protocolli/      # Documenti cliente e specifiche DB
│   └── ricerca/         # Note di ricerca, meeting, TODO
├── reports/             # Report di qualità e benchmark (Legacy vs Attuale)
├── tests/               # Test automatici
│   └── gaia_legacy/     # Test del vecchio sistema
├── logs/                # Log di esecuzione
├── scripts/             # Script di utilità
└── pyproject.toml       # Dipendenze e configurazione
```

## 🔧 Setup ambiente

### Prerequisiti

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (gestore pacchetti consigliato)

### Installazione

```bash
# Installa uv (se non presente)
pip install uv

# Sincronizza le dipendenze
uv sync

# Oppure con pip
pip install -e .
```

### Dipendenze principali

| Pacchetto | Uso |
|---|---|
| `PyMuPDF` | Apertura PDF e conversione pagine → immagini |
| `Pillow` | Manipolazione immagini |
| `pydantic` | Validazione schema JSON |
| `openpyxl` | Lettura file Excel |
| `requests` | Chiamate API (se VLM via API) |

## 🧪 Test

```bash
# Esegui tutti i test
pytest

# Test specifici
pytest tests/test_pdf_to_images.py
pytest tests/test_vlm_extraction.py
pytest tests/test_adas_transform.py
```

## 📋 Contratti JSON

La pipeline usa due formati JSON distinti:

1. **VLM Intermedio** (`docs/contracts/VLM_INTERMEDIATE.md`)
   - Prodotto dal VLM dopo estrazione
   - Contiene: stazioni, misure, bitinfo in forma grezza
   - Validato da Pydantic prima di passare al nodo successivo

2. **ADAS Finale** (`docs/contracts/ADAS_FINAL.md`)
   - Prodotto dal nodo Python di trasformazione
   - Contiene: DRIVERPRIVATE hex, XML DRIVERCONFIG, VM_SOURCE_CODE, ID rinumerati
   - Formato pronto per l'import nella piattaforma ADAS

## 🚧 Stato attuale

### ✅ Completato
- ✅ **Prompt VLM v12** con regole V20-V24 (filtri note/HW, registri doppi, rimap bit 1-16, porte gate)
- ✅ **json_creator v4.1** con supporto multi-pagina e logiche P1-P6 (dedup measures, group digitali, registri robusti, filtri riservato, pulizia parentesi Nodo 8, sanitize stati)
- ✅ **Modelli Pydantic** per validazione contratto intermedio e finale
- ✅ **Architettura 2 livelli** documentata (ADR-001)
- ✅ **Struttura progetto** inizializzata
- ✅ **Documentazione contratti** completata

### ⏳ Da fare
- ⏳ Configurazione MyHydra Livello 1 (orchestratore)
- ⏳ Semplificazione Livello 2 (rimozione pytool interno)
- ⏳ Test su altri PDF (PROTEC_2, SIEMENS, Curtiriso)
- ⏳ Generatore BISON (in attesa specifiche cliente)

### ⏸️ Rimandato
- ⏸️ Sistema doppio-PDF (caso SMI_1 e documenti con indice)
- ⏸️ BISON e linearizzazioni (bloccato su specifiche cliente)

## 📝 Convenzioni

- **Lingua codice**: inglese
- **Lingua commenti/doc**: italiano
- **Branching**: `main` (stabile) + feature branch
- **Commit**: messaggi descrittivi in italiano o inglese
=======
# Menerva
>>>>>>> 9421eb0a31db47d99a76e21f95d7572c14a5a5a6
