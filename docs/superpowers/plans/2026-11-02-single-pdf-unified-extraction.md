# Single PDF — Phase 1: estrazione unificata (1 chiamata VLM per pagina)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Eliminare il join a 3 rami (misure/nomi/stati) per `riga`: un'unica chiamata VLM per pagina produce un JSON unificato con tutti i campi. Il consolidatore diventa un trasformatore puro (validazione + classifica + carry-over + fold packed), non un riparatore.

**Architecture:** Un prompt unificato (`vlm_unified_v1.md`) sostituisce i 3 prompt separati. Il motore iterativo (LV1-03) invia 1 chunk per pagina (già così). Il consolidatore (LV1-04) riceve 1 ramo per pagina invece di 3. Il creator (LV1-05) resta invariato. La parità src ↔ documentata ↔ canvas resta pinnata da `render_canvas.py`.

**Tech Stack:** Python 3.10, pytest, ruff (line-length 100). VLM: Qwen 3.8 (come oggi). PyMuPDF per l'oracolo di copertura (futuro).

**Spec:** `AGENTS.md` (regole canvas: no def/class/lambda, output in `result`, paste <34KB), `myhydra/single_pdf/PENDENZE.md`, `myhydra/single_pdf/verifica_pdf/BENCHMARK_GATE.md` v5.

## Global Constraints

- Copie `myhydra/` devono restare byte-identiche a `src/` (hash in README). Se divergono, `src/` vince.
- Script canvas: standalone, no `def`/`class`/`lambda`, output in `result`, paste <34KB (rosso certo 34.365).
- `{edge}[N]` canvas-local: consolidatore `[6]`, creator `[2]`.
- Comunicazione in italiano; prompt e codice in inglese.
- Test: `./run_tests.sh` (root) + `./run_tests.sh double` devono restare verdi ad ogni commit.

## Review Focus

1. **Descrizioni non verbatim** — il VLM parafrasa nonostante il prompt. Senza il join by `riga`, una descrizione sbagliata non viene più corretta dal consolidatore. Serve controllo post-hoc vs testo PDF.
2. **Bit shift** — senza il ramo bitnames separato, il VLM deve leggere il bit dalla riga giusta. Il `bit_offset_pagina` (page-level) resta come safety net.
3. **Stati mancanti** — il VLM sotto-campiona TEXTON/TEXTOFF. Con 1 chiamata, deve leggerli tutti. Fallback keyword rimosso.
4. **Unità inventate** — il VLM emette `mg/m3` dove il PDF non ha unità. Post-hoc: null se non nel testo PDF.
5. **Righe vuote** — 47 `blocco_rows_vuoto` nel run attuale. Con schema unificato, il VLM deve emettere `null` per righe vuote, non saltarle.

---

### Task 1: Prompt unificato `vlm_unified_v1.md` ✅ DONE

Creato `src/prompts/vlm_unified_v1.md` (e copie in `myhydra/`). Schema unificato con tutti i campi (measures + bit + stati + tecnici). Regole V1-V30, V23, V26, V27, V28, V7, V8, D1-D7. "copy verbatim, never correct refusos", "emit null for units unless explicitly printed".

### Task 2: Refactor consolidatore per input unificato

**Files:**
- Modify: `src/nodes/single_consolidator.py` (assemble_page: aggiungere path unificato)
- Modify: `myhydra/single_pdf/pytools/consolidator.py` (stesso)
- Modify: `myhydra/single_pdf/pytools/consolidator_canvas.py` (rigenerare)
- Test: `tests/test_single_consolidator.py`, `tests/test_single_consolidator_canvas.py`

**Interfaces:**
- Consumes: `pages` = lista di pagine, ognuna con `stations` (variabili unificate, tutti i campi) e nessun `bitnames`/`bitstates`
- Produces: stesso output `{"stations", "warnings", "counters"}`

- [ ] **Step 1: Scrivere test fallente** — `test_input_unificato_nessun_join_per_riga`: pagina con 1 stazione e 3 variabili unificate (con bit, state_on, state_off), nessun bitnames/bitstates. Output = 3 variabili con bit e stati corretti, nessun `descrizione_mismatch`/`stati_riallineati`.

- [ ] **Step 2: Run test** → FAIL

- [ ] **Step 3: Refactor `assemble_page`**: aggiungere path unificato all'inizio: se `page.get("bitnames")` o `page.get("bitstates")` è presente, fare il join 3-rami (vecchio, per backward compat con tap esistenti). Altrimenti, trattare `stations` come variabili unificate: per ogni stazione, per ogni variabile, `_base_variable` + `classify_row_with_reason` + keep/discard. Nessun join, nessun `refuso_maggioranza`, nessun `stati_riallineati`.

- [ ] **Step 4: Run test** → PASS

- [ ] **Step 5: Run suite completa** → PASS (test esistenti 3-rami restano verdi per backward compat)

- [ ] **Step 6: Commit** `refactor(single): consolidator handles unified VLM output`

### Task 3: Aggiornare canvas e node card

- [ ] **Step 1: Aggiornare scheda nodo** LV1-04: input è `{"stations": [{"variables": [...]}]}` (1 ramo), no join by riga.
- [ ] **Step 2: Rigenerare canvas** + copiare in platforms.
- [ ] **Step 3: Run test** → PASS
- [ ] **Step 4: Commit** `docs(single): node card for unified extraction`

### Task 4: Aggiornare prompt LV2 e scheda nodo

- [ ] **Step 1: Aggiornare scheda nodo** LV2-02: 1 prompt unificato, 1 chiamata VLM per pagina.
- [ ] **Step 2: Archiviare i prompt vecchi** in `prompts/history/`.
- [ ] **Step 3: Copiare il prompt unificato** in `platforms/lv2/prompts/current/`.
- [ ] **Step 4: Commit** `docs(single): LV2 node for unified extraction`

### Task 5: Verifica su SIEMENS_2

- [ ] **Step 1: Eseguire la run** su SIEMENS_2 con il nuovo prompt + consolidatore.
- [ ] **Step 2: Verdetto**: target ≥235/431, 0 buchi reali, 0 invenzioni, 0 ADAS-invalidi.
- [ ] **Step 3: Se peggiore, analizzare** warning e rafforzare prompt.
- [ ] **Step 4: Commit** `feat(single): verified unified extraction on SIEMENS_2`

### Task 6: Controllo post-hoc refusi/unità vs testo PDF (Fase 3)

- [ ] **Step 1: Implementare** `_check_fidelity_vs_pdf_text` in consolidatore.
- [ ] **Step 2: Test** su caso 6 e 7.
- [ ] **Step 3: Commit** `feat(single): fidelity check vs PDF text`

## Self-Review

1. **Spec coverage**: ogni difetto aperto coperto da almeno un task.
2. **Step scan**: ogni step è un'azione con risultato verificabile.
3. **Type consistency**: `assemble_page` accetta entrambi i formati (3-rami e unificato). Output invariato.
4. **Review Focus**: i 5 punti coperti dai test.
5. **Proportion**: 6 task, ~2 settimane. Non un transcript.

## Execution Handoff

Plan complete. Proceeding with Task 1 (already done: prompt created) and Task 2 (consolidator refactor). Shall I start Task 2?