# Single PDF — Redesign v2: piano di implementazione

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Spec:** `docs/superpowers/specs/2026-11-02-single-pdf-redesign-v2-design.md`

**Goal:** Implementare il redesign v2: prompt oracolo, oracle apply nel consolidatore, gate v6, schede nodo aggiornate, test, hash.

**Architecture:** Il LV2 riceve un 2° visiomaru ORACOLO in parallelo a UNIFIED. Il consolidatore separa `estrazione` da `verifica`, consolida l'estrazione, applica le correzioni (aggiungi/annulla solo) con audit trail. Il gate v6 estende il v5 con le regole oracolo.

**Tech Stack:** Python 3.10, pytest, ruff (line-length 100). VLM: Qwen 3.8.

## Global Constraints

- Copie `myhydra/` byte-identiche a `src/` (hash in README).
- Script canvas: standalone, no `def`/`class`/`lambda`, output in `result`, paste <34KB.
- `{edge}[N]` canvas-local: consolidatore `[6]`, creator `[2]`.
- Comunicazione in italiano; prompt e codice in inglese.
- Test: `./run_tests.sh` (root) + `./run_tests.sh double` verdi ad ogni commit.

---

### Task 1: Prompt oracolo `vlm_oracle_v1.md`

**Files:**
- Create: `src/prompts/vlm_oracle_v1.md`
- Create: `myhydra/single_pdf/platforms/lv2/prompts/current/vlm_oracle_v1.md`
- Create: `myhydra/single_pdf/prompt/vlm_oracle_v1.md`
- Test: `tests/test_single_oracle.py`

**Interfaces:**
- Consumes: immagine pagina + output UNIFIED (JSON variabili)
- Produces: JSON difetti (`mancanti`, `unita_inventate`, `junk_stati`, `refusi_corretti`, `ip_dichiarati_non_usati`)

- [ ] **Step 1: Scrivere il prompt oracolo** con:
  - ROLE: verificatore tecnico, non estrattore
  - INPUT: immagine + JSON UNIFIED
  - OUTPUT: schema difetti (5 categorie)
  - Regole: mai sovrascrivere, fedeltà refusi, unità solo se nel PDF, junk = "1"/"0"/"1=…"/"0=…", mancanti = righe PDF non nel JSON, IP dichiarati non usati
  - Evidenza obbligatoria per ogni difetto
  - Prohibitions: D1-D6 (stesse di UNIFIED)

- [ ] **Step 2: Copiare in `myhydra/`** (byte-identiche)

- [ ] **Step 3: Test contract** in `test_single_oracle.py`:
  - `assert "mai sovrascrivere" in flat`
  - `assert "evidenza" in flat`
  - byte-identical tra src e platform copy

- [ ] **Step 4: Run test** → PASS

- [ ] **Step 5: Commit** `feat(single): oracle prompt v1`

---

### Task 2: Oracle apply nel consolidatore

**Files:**
- Modify: `src/nodes/single_consolidator.py` (separa `estrazione`/`verifica`, applica correzioni)
- Modify: `myhydra/single_pdf/pytools/consolidator.py` (stesso)
- Modify: `myhydra/single_pdf/pytools/consolidator_canvas.py` (rigenerare)
- Test: `tests/test_single_oracle_apply.py`

**Interfaces:**
- Consumes: pagine con `estrazione` (variabili) + `verifica` (JSON difetti)
- Produces: stesso output `{"stations", "warnings", "counters"}` + `_audit_oracolo` sulle variabili toccate

- [ ] **Step 1: Scrivere test fallente** — `test_oracle_apply_aggiunge_mancante`: pagina con 1 variabile UNIFIED + verifica con 1 `mancante`. Output = 2 variabili, la seconda con `_audit_oracolo: {"azione": "aggiunta"}`.

- [ ] **Step 2: Run test** → FAIL

- [ ] **Step 3: Implementare** in `assemble_page`:
  - Se la pagina ha `verifica`, separarla da `estrazione`.
  - Dopo il consolidamento, per ogni difetto:
    - `mancanti`: aggiungi variabile (verbatim, con `_audit_oracolo`)
    - `unita_inventate`: annulla unità (`units = null`, con `_audit_oracolo`)
    - `junk_stati`: annulla stato (`state_on/off = null`, con `_audit_oracolo`)
    - `refusi_corretti`: warning solo, non tocca
    - `ip_dichiarati_non_usati`: warning solo, non tocca
  - L'audit trail è nel FINALE.

- [ ] **Step 4: Run test** → PASS

- [ ] **Step 5: Rigenerare canvas** + copiare in platforms

- [ ] **Step 6: Run suite completa** → PASS

- [ ] **Step 7: Commit** `feat(single): oracle apply in consolidator`

---

### Task 3: Gate v6

**Files:**
- Modify: `myhydra/single_pdf/verifica_pdf/BENCHMARK_GATE.md`

- [ ] **Step 1: Aggiungere §16-18** al gate:
  - §16. Oracolo: ogni correzione verificabile contro il PDF
  - §17. Audit trail: `_audit_oracolo` con `evidenza` non vuota
  - §18. Refusi: warning, non errori

- [ ] **Step 2: Aggiornare changelog** (v6, 2026-11-02)

- [ ] **Step 3: Commit** `docs(single): gate v6 with oracle rules`

---

### Task 4: Schede nodo aggiornate

**Files:**
- Modify: `myhydra/single_pdf/nodes/lv2_02_vlm_parsing_json_principale.md`
- Modify: `myhydra/single_pdf/nodes/lv1_04_consolidatore.md`

- [ ] **Step 1: LV2-02**: 2 visiomaru (UNIFIED + ORACOLO), assemblatore `{estrazione, verifica}`

- [ ] **Step 2: LV1-04**: apply oracolo (aggiungi/annulla solo, audit trail)

- [ ] **Step 3: Commit** `docs(single): node cards for oracle`

---

### Task 5: Archiviazione prompt vecchi

**Files:**
- Move: `vlm_measures_v18.md`, `vlm_bitnames_v16.md`, `vlm_bitstates_v19.md` → `prompts/history/`

- [ ] **Step 1: Spostare in `history/`**

- [ ] **Step 2: Commit** `chore(single): archive old prompts`

---

### Task 6: Hash README + suite completa

**Files:**
- Modify: `myhydra/single_pdf/pytools/README.md`
- Modify: `myhydra/single_pdf/platforms/lv1/scripts/updated_pending_validation/README.md`

- [ ] **Step 1: Aggiornare hash** (consolidator, canvas, creator)

- [ ] **Step 2: Run suite completa** → PASS

- [ ] **Step 3: Commit** `chore(single): refresh hashes`

---

## Self-Review

1. **Spec coverage**: ogni decisione (12) è coperta da un task.
2. **Step scan**: ogni step è un'azione con risultato verificabile.
3. **Type consistency**: `assemble_page` cambia (riceve `verifica`), output invariato.
4. **Proportion**: 6 task, ~1 settimana. Non è un transcript.

## Execution Handoff

Plan complete. Proceeding with Task 1 (oracle prompt).
