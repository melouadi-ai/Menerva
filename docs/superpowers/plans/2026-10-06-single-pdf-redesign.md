# Single PDF redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ricostruire il flusso Single PDF sull'ossatura verificata del Double PDF con copertura verificabile riga-per-riga.

**Architecture:** VLM a 3 rami per pagina, filtri LV1 con scarti conteggiati, consolidatore prima di un JSON CREATOR slim; ogni pytool con copia canvas e test di parità; verità dal PDF come oracolo.

**Tech Stack:** Python 3.10, MyHydra (nodi VLM + pytool inline), Pydantic (solo dev/test), pytest, pymupdf.

**Spec:** `docs/superpowers/specs/2026-10-06-single-pdf-redesign-design.md`

## Global Constraints

- Pytool standalone: solo inline, niente `def`/`class`/`lambda`, output in `result`, niente `import src.*`.
- Budget paste 28 KB per script; copia documentata + copia canvas, test di parità AST+output, mai hand-edit.
- `{edge}[N]` / `{edge.media}[N]` con N canvas-locale ricontrollato; nessuna match-condition spuria sugli edge.
- Diagnosi solo da output incollabili (`_warnings`, `_meta`, `review`); niente tap/debug sui nodi.
- `src/` autoritativo; copie `myhydra/` byte-identiche con sha256 nei README.
- Comunicazione italiano; prompt VLM e codice inglese; file completi incollabili, nodi per nome esatto.
- Test con `.venv/bin/python`; root suite `testpaths=["tests"]`, Double esplicito `myhydra/double_pdf/tests`.

## Review Focus

- Pagina densa tipo SIEMENS con 100+ righe troncata dal VLM senza warning: atteso warning di copertura con conteggio pagine/righe.
- Riga `Riserva INPUT` scartata in silenzio senza motivo: atteso motivo `V2` nel report scarti.
- Bit copiato dalla riga sbagliata (caso 40014 BITNO 3): atteso bit identico al PDF riga-per-riga nel test di verità.
- Unità `(mg/m3)` cancellata sia da `NAME` che da `UNITS`: atteso `UNITS` popolato oppure nome intatto con parentesi.
- Script canvas divergente dalla copia documentata: atteso test di parità rosso prima dell'incollaggio.

---

### Task 1: Schema intermedio v14 + validatori

**Files:**
- Modify: `src/models/vlm_schema.py` (campi `zona`, `tag`, `pagina`, `riga`, config decisioni)
- Modify: `src/models/validators.py` (`safe_validate_vlm` esteso)
- Modify: `docs/contracts/VLM_INTERMEDIATE.md` (da v11 a v14)
- Test: `tests/test_single_schema_v14.py`

**Interfaces:**
- Consumes: niente (primo task).
- Produces: `Variable` con campi `zona: str | None`, `tag: str | None`, `pagina: int | None`, `riga: int | None`; `safe_validate_vlm` che accetta i nuovi campi e segnala `description` nulla come errore.

- [ ] **Step 1: Write the failing test**

```python
def test_v14_accetta_zona_tag_pagina_riga():
    st = {"name": None, "ip": "192.168.2.11", "port": 5021, "modbus_id": None,
          "variables": [{"description": "COG2: ALLARME FRIGO", "units": None,
                         "modbus_register": 40014, "bit": 11, "kind": "DIGITALE_IMPACCATO",
                         "data_type": "INT16", "read_write": None, "state_on": None,
                         "state_off": None, "scale_eng_start": None, "scale_eng_end": None,
                         "limit_hour": None, "limit_day": None,
                         "zona": "ALLARMI", "tag": None, "pagina": 5, "riga": 12}]}
    res = safe_validate_vlm({"stations": [st]})
    assert res.success
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/bin/python -m pytest tests/test_single_schema_v14.py -q`
Expected: FAIL (campi sconosciuti o mancanti).

- [ ] **Step 3: Implement i nuovi campi in `src/models/vlm_schema.py` e `src/models/validators.py`**
- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/bin/python -m pytest tests/test_single_schema_v14.py -q`
Expected: PASS.

- [ ] **Step 5: Aggiorna `docs/contracts/VLM_INTERMEDIATE.md` a v14 e commit**

```bash
git add src/models/vlm_schema.py src/models/validators.py docs/contracts/VLM_INTERMEDIATE.md tests/test_single_schema_v14.py
git commit -m "Schema intermedio v14 con zona tag pagina riga"
```

### Task 2: Prompt VLM a 3 rami

**Files:**
- Create: `src/prompts/vlm_measures_v14.md`, `src/prompts/vlm_bitnames_v14.md`, `src/prompts/vlm_bitstates_v14.md`
- Modify: `myhydra/single_pdf/prompt/README.md` (hash delle 3 copie)
- Test: `tests/test_single_prompts_v14.py` (regole presenti per file, non LLM)

**Interfaces:**
- Consumes: schema v14 dal Task 1 (nomi campi).
- Produces: 3 file prompt; il ramo misure emette `tag` + self-check BIT; nomi-bit emette solo registro/bit/descrizione; stati emette solo `state_on/off` o null.

- [ ] **Step 1: Write the failing test**

```python
def test_tre_prompt_con_regole_chiave():
    import pathlib
    base = pathlib.Path("src/prompts")
    assert "tag" in (base / "vlm_measures_v14.md").read_text()
    assert "V23" in (base / "vlm_bitnames_v14.md").read_text()
    assert "state_on" in (base / "vlm_bitstates_v14.md").read_text()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/bin/python -m pytest tests/test_single_prompts_v14.py -q`
Expected: FAIL (file mancanti).

- [ ] **Step 3: Implement i 3 prompt partendo da `src/prompts/vlm_extraction_v13.md` (split, niente nuove regole di scarto oltre V2/V20/V21)**
- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/bin/python -m pytest tests/test_single_prompts_v14.py -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/prompts/vlm_measures_v14.md src/prompts/vlm_bitnames_v14.md src/prompts/vlm_bitstates_v14.md myhydra/single_pdf/prompt/README.md tests/test_single_prompts_v14.py
git commit -m "Prompt VLM Single a 3 rami v14"
```

### Task 3: Filtri LV1 con scarti conteggiati

**Files:**
- Create: `src/nodes/single_filters.py` (logica pura e testabile, poi copiata inline nei pytool)
- Test: `tests/test_single_filters.py`

**Interfaces:**
- Consumes: variabile v14.
- Produces: `classify_row(v) -> ("keep" | "V2" | "V20" | "V21")` con motivo; mai uso di `zona` come nome.

- [ ] **Step 1: Write the failing test**

```python
def test_riserva_input_contata_non_silente():
    assert classify_row({"description": "Riserva INPUT", "zona": "INPUT_HW"}) in ("V2", "V21")
    assert classify_row({"description": "COG2: ALLARME FRIGO", "zona": "ALLARMI"}) == "keep"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/bin/python -m pytest tests/test_single_filters.py -q`
Expected: FAIL.

- [ ] **Step 3: Implement `classify_row` in `src/nodes/single_filters.py`**
- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/bin/python -m pytest tests/test_single_filters.py -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/nodes/single_filters.py tests/test_single_filters.py
git commit -m "Filtri Single con scarti conteggiati"
```

### Task 4: Consolidatore + copia canvas

**Files:**
- Create: `src/nodes/single_consolidator.py` (riferimento testabile)
- Create: `myhydra/single_pdf/pytools/consolidator.py` + `consolidator_canvas.py`
- Test: `tests/test_single_consolidator.py` + `tests/test_single_consolidator_canvas.py` (parità AST+output)

**Interfaces:**
- Consumes: chunk per pagina `{stations[]}` v14; `classify_row` dal Task 3.
- Produces: intermedio unificato con join scale per `tag`, carry-over registro con voce `registro_applicato`, fold packed, `_warnings` con scarti+V2/V20/V21 e buchi di sequenza.

- [ ] **Step 1: Write the failing test**

```python
def test_join_scale_per_tag_e_carry_over():
    out = consolidate([page_con_tag_scala(), page_misura_senza_registro()])
    assert out["warnings"] != []
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/bin/python -m pytest tests/test_single_consolidator.py -q`
Expected: FAIL.

- [ ] **Step 3: Implement consolidatore sotto 28 KB, poi deriva `consolidator_canvas.py` senza commenti**
- [ ] **Step 4: Run tests to verify they pass**

Run: `.venv/bin/python -m pytest tests/test_single_consolidator.py tests/test_single_consolidator_canvas.py -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/nodes/single_consolidator.py myhydra/single_pdf/pytools/consolidator.py myhydra/single_pdf/pytools/consolidator_canvas.py tests/test_single_consolidator.py tests/test_single_consolidator_canvas.py
git commit -m "Consolidatore Single con join TAG e carry-over"
```

### Task 5: JSON CREATOR slim + copia canvas

**Files:**
- Modify: `src/nodes/json_creator.py` (solo trasformazione deterministica, V19 vince su P5)
- Create: `myhydra/single_pdf/pytools/json_creator_v15.py` + `json_creator_v15_canvas.py`
- Test: `tests/test_single_creator_v15.py` (150/250, DRIVERPRIVATE 48 hex, NAME 49 char, sentinel, linkage)

**Interfaces:**
- Consumes: intermedio unificato dal Task 4.
- Produces: lista stazioni ADAS con `measures`+`bitinfo`, `_meta`+`_warnings`; parentesi con contenuto mai rimosse; stati keyword solo se `state_on/off` null.

- [ ] **Step 1: Write the failing test**

```python
def test_parentesi_con_contenuto_conservate_e_formato_da_datatype():
    assert creator_name("(GR)") == "(GR)"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/bin/python -m pytest tests/test_single_creator_v15.py -q`
Expected: FAIL.

- [ ] **Step 3: Implement slim + `*_canvas.py` sotto 28 KB**
- [ ] **Step 4: Run tests to verify they pass**

Run: `.venv/bin/python -m pytest tests/test_single_creator_v15.py -q && .venv/bin/python -m pytest -q`
Expected: PASS, root suite verde.

- [ ] **Step 5: Commit**

```bash
git add src/nodes/json_creator.py myhydra/single_pdf/pytools/json_creator_v15.py myhydra/single_pdf/pytools/json_creator_v15_canvas.py tests/test_single_creator_v15.py
git commit -m "JSON CREATOR Single slim v15"
```

### Task 6: Regressioni note (bit 40014, unità, IP, refusi)

**Files:**
- Modify: gli stessi del Task 5 se serve, altrimenti solo test
- Test: `tests/test_single_regressions.py`

**Interfaces:**
- Consumes: pipeline Task 4+5.
- Produces: 40014 a 16 bit identici al PDF; `(mg/m3)`/`(%)` in `UNITS` o nel nome intatto; nessun `127.0.0.1` fabbricato senza warning; refusi con policy esplicita.

- [ ] **Step 1: Write the failing test**

```python
def test_40014_sedici_bit_come_pdf():
    assert bits_of(output_40014(), 40014) == [8, 9, 10, 11, 12, 13, 14, 15, 0, 1, 2, 3, 4, 5, 6, 7]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/bin/python -m pytest tests/test_single_regressions.py -q`
Expected: FAIL sull'output storico.

- [ ] **Step 3: Implement la correzione minima nel task che possiede il codice**
- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/bin/python -m pytest tests/test_single_regressions.py -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add tests/test_single_regressions.py src/nodes/json_creator.py
git commit -m "Regressioni Single: bit 40014, unita, IP, refusi"
```

### Task 7: Verità PDF e `confronta.py`

**Files:**
- Create: `tests/test_single_truth_siemens.py` (tabella verità estratta dal PDF, non dal GT)
- Modify: `myhydra/single_pdf/verifica_pdf/confronta.py` (match stazione+registro+bit, classi di scarto)
- Modify: `reports/CONFRONTO_QUALITA_LEGACY_VS_ATTUALE.md` (KPI riscritti)
- Test: il nuovo test di verità stesso

**Interfaces:**
- Consumes: output ADAS dei Task 4+5.
- Produces: `got == PDF` per misure/bit/nomi; GT usato solo per regressione errori noti.

- [ ] **Step 1: Write the failing test (verità da PDF, atteso FAIL sul corrente)**
- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/bin/python -m pytest tests/test_single_truth_siemens.py -q`
Expected: FAIL finché la pipeline non è completa.

- [ ] **Step 3: Implement fix `confronta.py` + tabelle verità SMA/PROTEC/SIEMENS**
- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/bin/python -m pytest tests/test_single_truth_siemens.py -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add tests/test_single_truth_siemens.py myhydra/single_pdf/verifica_pdf/confronta.py reports/CONFRONTO_QUALITA_LEGACY_VS_ATTUALE.md
git commit -m "Verita PDF Single e fix confronta per stazione"
```

### Task 8: Robustezza canvas e chiusura

**Files:**
- Modify: `myhydra/single_pdf/nodes/*.md` (engine, media2content, VLM, filtri, consolidatore, creator)
- Create: `myhydra/single_pdf/platforms/` (`prompts/current|history`, `scripts/in_use|updated_pending_validation|parked`) + README hash
- Test: `tests/test_single_canvas_hygiene.py` (budget 28 KB, niente `def/class/lambda` nelle copie canvas, ERROR JSON presente)

**Interfaces:**
- Consumes: tutti i task precedenti.
- Produces: canvas incollabile con checklist edge-settings, ERROR JSON mai blank, guardie copertura+linkage attive.

- [ ] **Step 1: Write the failing test**

```python
def test_canvas_copies_sotto_budget_e_standalone():
    assert max_size < 28 * 1024
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/bin/python -m pytest tests/test_single_canvas_hygiene.py -q`
Expected: FAIL finché le copie non sono pronte.

- [ ] **Step 3: Implement riorganizzazione + checklist edge + ERROR JSON**
- [ ] **Step 4: Run full suites to verify they pass**

Run: `.venv/bin/python -m pytest -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add myhydra/single_pdf/nodes myhydra/single_pdf/platforms tests/test_single_canvas_hygiene.py
git commit -m "Robustezza canvas Single e chiusura redesign"
```
