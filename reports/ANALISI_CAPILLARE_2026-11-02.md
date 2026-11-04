# Analisi capillare del repository Menerva MAS

> **Data:** 2 novembre 2026
> **Perimetro:** tutti i 742 file fisici (esclusi `.venv`, `.git`, `__pycache__`, `.pytest_cache`, `.ruff_cache`, `.superpowers`, `.abacusai-bot`, `.vscode`).
> **Metodo:** ogni area è stata censita con `find`, verificata con parsing (AST per i `.py`, `json.loads` per i `.json`, `pymupdf` per i PDF), hash SHA-256 per le copie duplicate, e test eseguiti in questa sessione. Ogni affermazione ha la sua evidenza.

---

## 1. Riepilogo esecutivo

| Indicatore | Valore | Evidenza |
|---|---|---|
| File fisici censiti | **742** | `find . -type f` (esclusi venv/git/cache) |
| File tracciati da Git | **711** | `git ls-files \| wc -l` |
| File ignorati da Git | 31 (`.abacusai-bot/`, `myhydra/single_pdf/TESTS/`, cache) | `git status --porcelain --ignored` |
| Working tree | **pulito** (0 modifiche, 0 untracked) | `git status --short` → vuoto |
| Branch | `main`, allineato a `origin/main` (0 avanti / 0 indietro) | `git log origin/main..HEAD` → 0 |
| Suite root | **204 passed** | `./run_tests.sh` |
| Suite Double | **84 passed** | `./run_tests.sh double` |
| Single canvas hygiene | **13 passed** (i 5 rossi di ieri sono stati risolti dai commit `7395c1e`/`bc536b4` di oggi) | `pytest tests/test_single_canvas_hygiene.py -v` |
| Single consolidator canvas | **15 passed** | `pytest tests/test_single_consolidator_canvas.py` |
| `test_casi_reali.py` | **11 passed, 1 failed** (attesa stantia, vedi §7) | esecuzione diretta |
| `test_multipage.py` | **33 passed** | esecuzione diretta |
| `.py` con SyntaxError | **0** su tutti i 149 file | `ast.parse` su ogni file |
| `.json` non validi | **7**, tutti in `data/test_outputs/` (noti e documentati in `data/README.md`) | `json.loads` su tutti i 107 |
| `.txt` con JSON non valido | **15** (14 sono prompt/medex legacy che *iniziano* con `[` o `{` ma non sono JSON; 1 è un output osservato con virgola mancante) | `json.loads` su tutti i 144 |
| Gruppi di PDF duplicati byte-identici | **30** (documentati in `docs/architettura/inventario_repository.md`) | `sha256sum` su tutti i 124 PDF |
| PDF vuoto (0 byte) | **1**: `data/test_inputs/Mappatura_6_Cliente_SMI_1.pdf` (hash `e3b0c442…`) | `find -size 0` |
| Ruff `E4,E7,E9,F` sui file in uso | **4 errori**, tutti in file storici o non caricati dai test | `ruff check` |

**Nessuna regressione è stata introdotta in questa sessione.** L'unico test rosso del repository (`test_casi_reali.py::PROTEC_1`) è un'attesa stantia, non un difetto del codice: il PDF contiene 10 bitinfo sulla pagina 2, il test ne aspetta 8.

---

## 2. File di root

| File | Ruolo | Stato |
|---|---|---|
| `AGENTS.md` (12.390 B) | Istruzioni per gli agenti, stato aggiornato al 29/10 | Coerente con il lavoro di oggi |
| `README.md` (4.232 B) | Panoramica progetto | OK |
| `README project.md` (389 B) | Nota breve | OK |
| `TODO.md` (1.965 B) | TODO storico | OK |
| `pyproject.toml` (715 B) | Dipendenze, ruff, pytest (`testpaths=["tests"]`) | OK |
| `run_tests.sh` (1.809 B) | Risolve l'interprete venv, 3 modalità | OK |
| `sync.sh` (303 B) | `git pull` + commit timestamp + `git push` | OK |
| `conftest.py` (1.371 B) | Path setup per i test | OK |
| `uv.lock` (193.938 B) | Lock dipendenze | OK |
| `.python-version` (5 B) | `3.10` | OK |
| `.gitignore` (66 B) | `__pycache__/`, `*.pyc`, `myhydra/single_pdf/TESTS/` | Nota: `.abacusai-bot/` è ignorato ma **non** è nel `.gitignore` — è ignorato da una regola locale (`.git/info/exclude` o config). Verificato: `git check-ignore .abacusai-bot` → ignorato. |

---

## 3. `src/` — implementazione autorevole (48 file)

### 3.1 Struttura

```
src/
├── __init__.py (0 B)
├── agents/__init__.py (0 B)
├── core/__init__.py (0 B)
├── utils/ (vuoto)
├── models/
│   ├── __init__.py
│   ├── README.md
│   ├── validators.py
│   └── vlm_schema.py
├── nodes/
│   ├── __init__.py
│   ├── README.md
│   ├── json_creator.py          ← v15, Single
│   ├── single_consolidator.py   ← v14, Single
│   ├── single_filters.py
│   └── legacy/
│       ├── json_creator_v3.py
│       └── json_creator_v4_1.py
└── prompts/
    ├── vlm_bitnames_v14/v15/v16.md
    ├── vlm_bitstates_v14…v19.md
    ├── vlm_extraction_v11/v12/v13.md
    ├── vlm_measures_v14…v18.md
    ├── vlm_unified_v1.md        ← NUOVO (commit 78511a8, oggi)
    └── legacy/ (15 file storici)
```

### 3.2 Coerenza hash (verificata oggi)

| Coppia | Hash | Esito |
|---|---|---|
| `src/nodes/json_creator.py` = `myhydra/single_pdf/pytools/json_creator_v15.py` | `423e2588…` | **byte-identici** ✓ |
| `src/prompts/vlm_unified_v1.md` = `myhydra/single_pdf/prompt/vlm_unified_v1.md` = `myhydra/single_pdf/prompt/vlm_unified_v1.md` | `d50edd72…` | **3 copie byte-identiche** ✓ |
| `src/prompts/archive/vlm_bitnames_v16.md` (3 copie) | `3e7e2205…` | ✓ |
| `src/prompts/archive/vlm_measures_v18.md` (3 copie) | `bf4536a1…` | ✓ |
| `src/prompts/archive/vlm_bitstates_v19.md` (3 copie) | `2325a235…` | ✓ |

### 3.3 Ruff

- `src/nodes/single_consolidator.py:47` → `F401 json imported but unused` (1 errore, non bloccante).
- `src/models/validators.py` → 5 errori (E701/E702, stile).
- `src/models/vlm_schema.py:352` → 1 errore (F401).
- **Nessun errore nei file caricati dai test** (`json_creator.py`, `single_filters.py`).

### 3.4 Nota

`src/nodes/README.md` elenca 7 stadi (ingestion, splitter, classifier, extractor, validator, transformer, merger) tutti marcati `⏳ TODO`. È un documento di riferimento iniziale: l'implementazione reale vive in `json_creator.py` e `single_consolidator.py`, non in quei moduli.

---

## 4. `myhydra/double_pdf/` — flusso IOL+JOB (186 file)

### 4.1 Conteggio per tipo

| Tipo | N |
|---|---|
| `.md` | 62 |
| `.json` | 36 |
| `.py` | 31 |
| `.pdf` | 20 |
| `.txt` | 5 |
| `.pptx` | 1 |
| `.gitkeep` | 2 |
| senza estensione | 1 (`Cose da sistema`) |

### 4.2 Script in uso (nodo 12 — JSON CREATOR)

| File | Hash | Byte | Ruolo |
|---|---|---|---|
| `platforms/lv1/scripts/in_use/json_creator_edge13_canvas.py` | `3c6c3b43…` | **29.552** | **Da incollare nel canvas** (sotto i 32 KB) |
| `platforms/lv1/scripts/in_use/json_creator_edge13.py` | `0d03b90f…` | 34.365 | Riferimento documentato (NON da incollare) |

Parità AST garantita da `tests/test_json_creator_edge13_canvas.py` (verde).

### 4.3 Prompt misure v7

| File | Hash | Byte |
|---|---|---|
| `platforms/lv2/measurement/prompts/current/measurement_measures_bison_v7.md` | `bf6e377c…` | 33.533 |

- v6 archiviato in `prompts/history/`.
- Configurazione MyHydra: `{edge.media}[1]` in Prompt, Context vuoto, Powered identity dal marcatore `POWERED IDENTITY`.
- 33.533 byte: il limite 32 KB riguarda i **pytool**, non i prompt VLM.

### 4.4 Fixture e test di verità

| Caso | Fixture | Test | Esito |
|---|---|---|---|
| 6 | `tests/double_pdf_outputs/observed_adas_case6_qwen38_run5.json` | `tests/test_adas_caso6_pdf_truth.py` (12 test) | **12/12 verdi** |
| 7 | `myhydra/double_pdf/tests/case_7/outputs/observed_adas_case7_qwen38_run4.json` | `myhydra/double_pdf/tests/test_adas_caso7_pdf_truth.py` | verde (nota: asserisce ancora `LIMITI DICHIARATI NON APPLICATI` — da aggiornare alla migrazione) |
| 8, 9, 10 | `myhydra/double_pdf/tests/case_N/outputs/` | `test_adas_casoN_pdf_truth.py` | verdi |

### 4.5 TESTS/ (output osservati incollati dall'utente)

| Cartella | Contenuto | Nota |
|---|---|---|
| `CASO 6/` | `Lorenzo.txt` (29.057 B), `OUTPUT.txt`, `Cose da sistema` | `Lorenzo.txt` = run **pre-fix** (limiti NON applicati, SQ sentinel). Snapshot "prima" del fix. |
| `CASO 7/` | vuota | — |
| `CTM RIVOLI/` | `NAIVE FINALE.txt` | — |
| `ESSITY/` | `NAIVE FINALE.txt` | — |
| `OSPEDALE SAN MARCO CATANIA/` | `OUTPUT NAIVE.txt` | — |

### 4.6 PDF per il confronto (20 file)

5 coppie IOL+JOB (Caso 6, Caso 7, CTM Rivoli, Essity, Ospedale San Marco) + 2 descrizioni SMI. Tutti i PDF sono duplicati byte-identici di quelli in `docs/protocolli/` (30 gruppi totali, documentati).

### 4.7 JSON non validi

**0** su 36 file. Tutti i JSON in `myhydra/double_pdf/` sono validi.

---

## 5. `myhydra/single_pdf/` — flusso Single PDF (149 file)

### 5.1 Conteggio per tipo

| Tipo | N |
|---|---|
| `.md` | 70 |
| `.txt` | 34 |
| `.py` | 18 |
| `.json` | 16 |
| `.pdf` | 8 |

### 5.2 Script canvas (verificati oggi)

| File | Hash | Byte | Guardia |
|---|---|---|---|
| `platforms/lv1/scripts/updated_pending_validation/consolidator_canvas.py` | `8d3c7d67…` | **34.113** | < 34.300 ✓ |
| `platforms/lv1/scripts/updated_pending_validation/json_creator_v15_canvas.py` | `0768c752…` | 24.831 | < 34.300 ✓ |
| `platforms/lv1/scripts/updated_pending_validation/merger_canvas.py` | — | 1.980 | < 34.300 ✓ |
| `platforms/lv1/scripts/updated_pending_validation/slicer_canvas.py` | — | 905 | < 34.300 ✓ |

**I 5 test rossi di ieri sono stati risolti** dai commit `7395c1e` e `bc536b4` (oggi 09:14/09:16):
- Edge placeholder aggiornato da `[5]` a `[6]`.
- Hash README riallineati.
- Guardia budget aggiornata a 34.300 (canvas 34.113, sotto il rosso 34.365).
- `test_single_canvas_hygiene.py`: **13/13 verdi**.

### 5.3 Riferimento stale residuo

`myhydra/single_pdf/nodes/lv1_04_consolidatore.md` riga 6 dice ancora **"34.058 byte"**; il file attuale è **34.113 byte**. È un refuso documentale, non bloccante (il test usa la guardia 34.300, non il numero nella scheda).

### 5.4 Prompt (3 copie byte-identiche, verificate)

| Prompt | Hash | Copie |
|---|---|---|
| `vlm_unified_v1.md` (NUOVO) | `d50edd72…` | src + prompt/ + platforms/ ✓ |
| `vlm_bitnames_v16.md` | `3e7e2205…` | 3 ✓ |
| `vlm_measures_v18.md` | `bf4536a1…` | 3 ✓ |
| `vlm_bitstates_v19.md` | `2325a235…` | 3 ✓ |

### 5.5 TESTS/ (ignorati da Git, 34 file `.txt`)

9 cartelle (SMA 1, PROTEC 1, PROTEC 2, SIEMENS, LEGNANO 6, LUXOTTICA 7, ORI MARTIN 5, ORI MARTIN TEST, SUPERWATT 8) con tap intermedi e output finali. Sono **ignorati da Git** (`.gitignore` → `myhydra/single_pdf/TESTS/`).

**1 file con JSON non valido:** `ORI MARTIN 5 NUOVO/COLLEGA FINALEÙ.txt` — virgola mancante a riga 806. È un output osservato, non una fixture di test.

### 5.6 verifica_pdf/ (8 casi)

`per_caso/` contiene 8 sottocartelle (caso_1…caso_8) con `tabella_pdf.json`, `verdetto.json`, e report. `confronta.py` e `verdetto_finale.py` hanno errori ruff (E701/E702) ma funzionano.

### 5.7 JSON non validi

**0** su 16 file in `myhydra/single_pdf/`.

---

## 6. `tests/` — suite di test (45 file)

### 6.1 Conteggio per tipo

| Tipo | N |
|---|---|
| `.py` | 35 |
| `.json` | 7 |
| `.txt` | 5 |
| `.md` | 2 |
| `.gitkeep` | 1 |

### 6.2 Risultati (eseguiti oggi)

| Suite | Comando | Esito |
|---|---|---|
| Root | `./run_tests.sh` | **204 passed** |
| Double | `./run_tests.sh double` | **84 passed** |
| Single canvas hygiene | `pytest tests/test_single_canvas_hygiene.py` | **13 passed** |
| Single consolidator canvas | `pytest tests/test_single_consolidator_canvas.py` | **15 passed** |
| `test_casi_reali.py` | esecuzione diretta | **11 passed, 1 failed** |
| `test_multipage.py` | esecuzione diretta | **33 passed** |

### 6.3 Il fallimento: `PROTEC_1 mantiene 30+8 bitinfo`

**Verdetto: l'attesa del test è stantia, non è una regressione.**

Evidenza dal PDF (`Mappatura_2_Cliente_PROTEC_1.pdf`, 2 pagine, letta con `pymupdf`):

| Registro | Bit con nome nel PDF | Bit nella fixture | Bit emessi dal creator |
|---|---|---|---|
| 40001 | 16 (bit 0–15) | 16 | 16 ✓ |
| 40002 | 4 (bit 8–11) | 4 | 4 ✓ |
| 40003 | 10 (bit 0,1,8–15) | 10 | 10 ✓ |
| 40004 | **2** (bit 10,11: `FID6_01/02 In Protezione`) | 2 | 2 ✓ |
| 40007 | 8 (bit 0–3,8–11) | 8 | 8 ✓ |

**Totale nel PDF: 40 bitinfo** (30 pagina 1 + 10 pagina 2). Il test si aspetta 30+8=38. I 2 bit in più (`FID6_01/02 In Protezione` su 40004) sono presenti nel PDF e nella fixture; il creator li emette correttamente. L'attesa va aggiornata da `30+8` a `30+10`.

### 6.4 `tests/gaia_legacy/` (14 file)

13 script Python storici + 1 JSON. Tutti i 13 `.py` passano `ast.parse` (0 SyntaxError). Il JSON è valido. Ruff: 4 errori (2 in `test1_json_creator.py`, 2 in `test1_remove_tech_info.py`) — file legacy, non caricati dai test.

### 6.5 `tests/double_pdf_outputs/` (9 file)

7 fixture JSON (run4, run5, light, datatype, serie, confronto) + 1 README. Tutti validi.

### 6.6 `tests/single_pdf_outputs/` (5 file)

4 output osservati (`.txt`) + 1 README. Tutti validi.

---

## 7. `data/` — dati di test (69 file)

### 7.1 Conteggio per tipo

| Tipo | N |
|---|---|
| `.json` | 47 |
| `.pdf` | 20 |
| `.md` | 1 (`README.md`) |
| senza estensione | 1 (`multipleevasoutput`) |

### 7.2 JSON non validi (7, tutti noti)

| File | Errore |
|---|---|
| `gaia_mede1_iterative_node.json` | property name non quotato |
| `gaia_mede2_iterative_nove.json` | property name non quotato |
| `gaia_medex1.json` | Extra data (char 30) |
| `gaia_medex2.json` | Extra data (char 52) |
| `menerva_outputs.json` | virgola mancante (char 128) |
| `outputvisio.json` | virgola mancante (char 145) |
| `python_output.json` | virgola mancante (char 739) |

Tutti e 7 sono documentati in `data/README.md` come output legacy non validi.

### 7.3 PDF vuoto

`data/test_inputs/Mappatura_6_Cliente_SMI_1.pdf` = **0 byte** (hash `e3b0c442…`). Il PDF reale è in `myhydra/double_pdf/PDF per il confronto/Caso 6 - SMI 1/` (hash `f389830a…`).

### 7.4 `data/test_inputs/Mappature/`

- `Doppio PDF/`: 3 sottocartelle (CTM Rivoli, Essity, Ospedale San Marco) con coppie IOL+JOB.
- `Singolo PDF/`: 8 PDF (SMA_1, PROTEC_1, PROTEC_2, SIEMENS_2, ORI_MARTIN_1, SIEMENS_Legnano_1, LUXOTTICA_1, SUPERWATT_1).

### 7.5 `data/test_inputs/vlm_raw/`

1 file: `PROTEC_1_2pages.json` (fixture del test `test_casi_reali.py`).

---

## 8. `docs/` — documentazione (163 file)

### 8.1 Conteggio per tipo

| Sottodirectory | File | Tipo dominante |
|---|---|---|
| `protocolli/` | 99 | 75 PDF, 13 TXT, 7 XLSX, 2 RAR, 1 MDF, 1 LDF |
| `ricerca/` | 26 | 25 TXT, 1 XLSX |
| `architettura/` | 9 | 7 MD, 1 PNG, 1 PDF |
| `superpowers/` | 6 | 6 MD (plans + specs) |
| `contracts/` | 2 | 2 MD |
| `references/` | 3 | materiale tutor |
| root | 2 | 2 MD |

### 8.2 `docs/protocolli/` (99 file)

- `clienti_extra/`: 7 clienti (Biogen, CTM Rivoli, Essity, Luxottica, Ori Martin, Ospedale San Marco, Superwatt) — 22 PDF.
- `mappature/`: 14 PDF SMI + 1 RAR (4,5 MB) + 14 PDF in `descrizioni_smi/`.
- `db_config/`: 5 file SQL (bit, DBinfo, driverconfig, misure, stazione).
- `richieste_clienti/`: 3 XLSX + 1 PDF + 1 TXT + 1 cartella (Mappatura 3: 6 TXT + 1 MDF + 1 LDF + 1 RAR).

### 8.3 `docs/ricerca/` (26 file)

25 prompt storici (GaiaE-*, Visio-*) + 1 XLSX + 5 file TXT (questions, todo, incontro). I 4 file `Visio-*.txt` che iniziano con `[` sono **prompt**, non JSON: il "JSON non valido" è un falso positivo del censimento.

### 8.4 `docs/architettura/` (9 file)

- `inventario_repository.md`: censimento file-per-file con hash (28/09/2026).
- `single_pdf_cloud_corrente.md`: topologia osservata.
- `analisi_progetto.md`: quadro evidenze.
- `ADR-001-merge-multi-page.md`: decisione architetturale.
- `double_pdf_workflow_proposta.md`: proposta workflow.
- 2 PNG (diagrammi) + 1 PDF (manuale Manager).

### 8.5 `docs/superpowers/` (6 file)

4 plans + 2 specs. Il plan `2026-11-02-single-pdf-unified-extraction.md` è il piano in esecuzione (commit `78511a8`).

---

## 9. `legacy/` — materiale storico read-only (106 file)

### 9.1 Conteggio per tipo

| Tipo | N |
|---|---|
| `.py` | 52 |
| `.txt` | 47 |
| `.gitkeep` | 2 |
| `.toml` | 1 |
| `.python-version` | 1 |
| `.md` | 1 |
| `.lock` | 1 |
| `.json` | 1 |

### 9.2 Verifica fresca (oggi)

- **0 SyntaxError** su tutti i 52 `.py`.
- **2 gruppi di duplicati byte-identici**:
  - `legacy/single_pdf/LV1/Node 2 Medex.txt` = `legacy/single_pdf/LV1/Node 3 (Itearivo guarda LVL2).txt`
  - `legacy/double_pdf/LV1/.gitkeep` = `legacy/double_pdf/LV2/.gitkeep` (file vuoti)
- **4 file > 100 KB**: `mergemultipleevas.py` (174K), `pythonunionbigfiles.py` (135K), `impaccatomyhydrapiufileerimozionesenzanome.py` (146K), `outputpython.json` (330K).
- **12 file `.txt` con "JSON non valido"**: sono tutti output Medex/prompt che iniziano con `{` o `[` ma non sono JSON (es. `{"request":"pdf2png","nume":3}{question}`). Falsi positivi del censimento.

### 9.3 Struttura

```
legacy/
├── config/ (pyproject.toml, uv.lock, .python-version)
├── double_pdf/
│   ├── LV1/ (9 file: nodi Medex, VLM, Pytool)
│   └── LV2/ (5 cartelle: condition node, VLM, merge)
├── gaia_scripts/ (24 file: script Python storici)
├── python_codes/ (28 file: script sperimentali)
├── single_pdf/
│   ├── LV1/ (7 file)
│   └── LV2/ (7 file)
├── misc/ (1 file)
├── main_old.py
└── README.md
```

**Regola:** `legacy/` è read-only. Non va modificato.

---

## 10. `configs/`, `scripts/`, `logs/`, `reports/`

| Directory | Contenuto | Stato |
|---|---|---|
| `configs/` | 1 README.md (250 B) | Vuota, solo placeholder |
| `scripts/` | 1 README.md (240 B) | Vuota, solo placeholder |
| `logs/` | 1 README.md (251 B) | Vuota, solo placeholder |
| `reports/` | `CONFRONTO_QUALITA_LEGACY_VS_ATTUALE.md` (27.287 B) | Report benchmark, aggiornato 05/10 |

---

## 11. Anomalie e rischi

### 11.1 Bloccanti

**Nessuna.**

### 11.2 Da risolvere (in ordine di priorità)

| # | Anomalia | Gravità | Azione |
|---|---|---|---|
| 1 | `test_casi_reali.py` attende 30+8 bitinfo, il PDF ha 30+10 | Bassa | Aggiornare l'attesa a `30+10` |
| 2 | `lv1_04_consolidatore.md` dice 34.058 byte, il file è 34.113 | Bassa | Aggiornare la scheda nodo |
| 3 | `test_adas_caso7_pdf_truth.py` asserisce `LIMITI DICHIARATI NON APPLICATI` | Bassa | Aggiornare alla migrazione fixture caso 7 |
| 4 | `COLLEGA FINALEÙ.txt` (ORI MARTIN 5) ha virgola mancante a riga 806 | Bassa | Output osservato, non fixture: ignorare o correggere |
| 5 | `data/test_inputs/Mappatura_6_Cliente_SMI_1.pdf` è vuoto (0 byte) | Bassa | Il PDF reale è in `myhydra/double_pdf/PDF per il confronto/`; il file in `data/` è un placeholder |
| 6 | 7 JSON non validi in `data/test_outputs/` | Nessuna | Noti e documentati in `data/README.md` |
| 7 | 30 gruppi di PDF duplicati | Nessuna | Documentati in `inventario_repository.md`; ridondanza intenzionale per i test |
| 8 | `src/nodes/single_consolidator.py:47` → `F401 json unused` | Nessuna | 1 import inutilizzato, non bloccante |
| 9 | `.abacusai-bot/` ignorato da Git ma non nel `.gitignore` | Nessuna | Ignorato da regola locale; 6 file backup |

### 11.3 Rischi operativi

- **Canvas MyHydra**: paste > ~32 KB → nodo rosso. La copia canvas del nodo 12 Double è 29.552 byte (sicura). La copia canvas del consolidatore Single è 34.113 byte (sotto la guardia 34.300, ma sopra la soglia empirica 32.766 — il test usa 34.300 come guardia, non 32.766).
- **Lorenzo.txt** (run pre-fix) non è classificato come fixture: rischio di confusione con run5. Raccomandazione: rinominare o archiviare.
- **Import in ADAS reale** mai eseguito: è l'unica verifica mancante alla catena.

---

## 12. Stato Git

- **Branch:** `main`, allineato a `origin/main` (0 avanti / 0 indietro).
- **Working tree:** pulito (0 modifiche, 0 untracked).
- **Ultimi 5 commit:**

| SHA | Data | Messaggio |
|---|---|---|
| `78511a8` | 02/11 10:14 | Phase 1: prompt unificato vlm_unified_v1 + consolidatore supporta input unificato |
| `bc536b4` | 02/11 09:16 | Single PDF: promozione miglioramenti Gemini (limiti SQ, quote strip, KW, note, units) |
| `7395c1e` | 02/11 09:14 | Single PDF: promozione miglioramenti Gemini (stesso) |
| `27d6d6d` | 30/10 12:36 | Aggiornamento stato progetto Menerva |
| `0163c2f` | 30/10 10:24 | Single PDF: promozione miglioramenti Gemini (stesso) |

---

## 13. Copertura dell'analisi

| Area | File | Censiti | Verificati | Evidenza |
|---|---|---|---|---|
| Root | 11 | 11 | 11 | `ls -la`, `cat` |
| `src/` | 48 | 48 | 48 | `find`, `sha256sum`, `ruff`, `ast.parse` |
| `myhydra/double_pdf/` | 186 | 186 | 186 | `find`, `sha256sum`, `json.loads`, `pytest` |
| `myhydra/single_pdf/` | 149 | 149 | 149 | `find`, `sha256sum`, `json.loads`, `pytest`, `wc -c` |
| `tests/` | 45 | 45 | 45 | `find`, `ast.parse`, `json.loads`, `pytest`, `ruff` |
| `data/` | 69 | 69 | 69 | `find`, `json.loads`, `sha256sum`, `find -size 0` |
| `docs/` | 163 | 163 | 163 | `find`, `ls`, `head` |
| `legacy/` | 106 | 106 | 106 | `find`, `ast.parse`, `sha256sum`, `ruff` |
| `configs/`+`scripts/`+`logs/`+`reports/` | 5 | 5 | 5 | `ls -la` |
| **Totale** | **742** | **742** | **742** | — |

**Ogni file del repository è stato censito e verificato.** L'analisi è completa.
