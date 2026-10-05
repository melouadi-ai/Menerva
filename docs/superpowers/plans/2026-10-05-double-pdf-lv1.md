# Double PDF LV1 canvas fix Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Sbloccare e stabilizzare la LV1 Double PDF del canvas in screenshot senza toccare il Single PDF.

**Architecture:** Solo operazioni canvas + verifica locale: prima si rimuove la condizione spuria che affama un ramo, poi si verificano gli edge dei filtri contro gli script `in_use`, poi si cabla il consolidatore ancora assente.

**Tech Stack:** MyHydra canvas (Medex, Pytool standalone senza `def`/`class`/`lambda` con `result`, Naive, iniezioni iterative), Python 3.10 `.venv`, pytest.

**Spec:** `myhydra/double_pdf/WORKFLOW_DESIGN.md`, `myhydra/double_pdf/nodes/lv1_05_page_dispatcher.md`, `myhydra/double_pdf/nodes/lv1_06_consolidator.md`, screenshot LV1 del 05-10-2026.

## Global Constraints

- Single PDF e Double PDF sono progetti separati: non riusare prompt/script dell'uno nell'altro.
- Pytool canvas: solo codice inline, nessun `def`/`class`/`lambda`, output in `result`, nessun `import src.*`.
- `{question}` = input iterazione corrente; `{edge}[N]` = output testuale altro nodo, `N` canvas-locale da rileggere dopo ogni ricablaggio.
- Dopo ogni ricablaggio ispezionare le impostazioni edge e rimuovere condizioni spurie.
- Incollare sempre il file completo pronto per il canvas, mai frammenti.

## Review Focus

- Edge con condizione residua che blocca in silenzio un ramo mentre gli altri girano.
- Indice `{edge}[N]` incollato da documentazione ma diverso dal canvas reale dopo riordini.
- Filtro Density con edge ambiguo in screenshot (`#6` atteso dallo script contro `#8` letto male).
- Consolidatore cablato agli array sbagliati (singole pagine invece degli aggregati delle iniezioni).
- `STATION_EDGE`/`MEASURE_EDGE`/`DENSITY_EDGE` lasciati a `None` sul canvas.

---

### Task 1: Sbloccare il ramo Station (edge con condizione `pippo`)

**Files:**
- Modify (canvas, no repo): edge `FILTER STATION INFORMATION` (nodo 6) -> `ESTRAZIONE STATI... / DOUBLE PDF STATION INFORMATION` (nodo 11), oggi `#11 pippo`
- Test: run canvas ramo Station + `myhydra/double_pdf/tests/case_6/outputs/observed_lv1_filtered_branches_sanitized.json` come riferimento

**Interfaces:**
- Consumes: array `STATION_INFORMATION` dal nodo 6 (6 record attesi caso 6: sequenze 6, 7, 9, 10, 11, 12)
- Produces: iniezione nodo 11 riceve pagine (non più `{question}` vuota a valle)

- [ ] **Step 1: Sul canvas, aprire le impostazioni dell'edge #11 tra nodo 6 e nodo 11 e cancellare la condizione `pippo`**
- [ ] **Step 2: Verificare che l'edge resti `#11` e senza condizioni, salvare il canvas**
- [ ] **Step 3: Re-run del solo ramo Station e confermare che il nodo 11 itera (non più iniezione affamata)**
- [ ] **Step 4: Confrontare il conteggio con il riferimento (6 Station caso 6)**
- [ ] **Step 5: Riportare il numero edge confermato in `nodes/lv1_05_page_dispatcher.md` se diverso**

### Task 2: Verificare gli edge dei tre filtri contro gli script `in_use`

**Files:**
- Modify: nessuno (solo verifica canvas + eventuale aggiornamento doc)
- Test: `.venv/bin/python -m pytest myhydra/double_pdf/tests -q`

**Interfaces:**
- Consumes: `PREPARA PAGINE PER I FILTRI` (nodo 5) via `{edge}[5]` / `[7]` / `[6]`
- Produces: tabella edge confermata per i tre filtri

- [ ] **Step 1: Confermare sul canvas gli ingressi: nodo 6 `FILTER STATION INFORMATION` = `#5`, nodo 7 `FILTER MEASUREMENT TECHNICAL DATA` = `#7`, nodo 8 `FILTER DENSITY MAP` = `#6`**
- [ ] **Step 2: Se l'ingresso del nodo 8 risulta `#8` in screenshot, sciogliere l'ambiguità (l'edge `#8` visibile sotto il nodo 8 è l'uscita 8 -> 9 `INOLTRA DENSITY MAP`)**
- [ ] **Step 3: Eseguire la suite double in locale**
Run: `.venv/bin/python -m pytest myhydra/double_pdf/tests -q`
Expected: PASS (33 passed)
- [ ] **Step 4: Aggiornare `nodes/lv1_05_page_dispatcher.md` solo se un numero reale differisce**

### Task 3: Cablare `CONSOLIDA INTERMEDIO VLM` (assente in screenshot)

**Files:**
- Create (canvas): Pytool `CONSOLIDA INTERMEDIO VLM` dopo nodo 11, nodo 10 e nodo 9, non iterativo
- Modify (canvas paste): `myhydra/double_pdf/platforms/lv1/scripts/updated_pending_validation/consolidate_to_intermediate.py` (impostare `STATION_EDGE`, `MEASURE_EDGE`, `DENSITY_EDGE` reali)
- Test: `myhydra/double_pdf/tests/test_consolidate_to_intermediate.py`

**Interfaces:**
- Consumes: array aggregato Station (da nodo 11/12), pagine assemblate Measurement (da nodo 10/13), pagine Density (da nodo 9)
- Produces: `{"diagnostic": "LV1_CONSOLIDATOR", "status": "OK", "stations": [...chunk per json_creator...], ...}`

- [ ] **Step 1: Scrivere il test di cablaggio (solo edge reali, mai `None`)**
- [ ] **Step 2: Creare il nodo canvas e incollare il file completo con i tre indici reali**
- [ ] **Step 3: Re-run e confermare `status: OK` con `stations` non vuoto sul caso 6**
- [ ] **Step 4: Riportare i tre numeri edge in `nodes/lv1_06_consolidator.md`**
