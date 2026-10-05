# AGENTS.md — Menerva MAS

Python 3.10. This repo converts PLC/SCADA mapping PDFs into ADAS JSON (Single PDF flow live on a cloud platform; Double PDF IOL+JOB flow in development). The cloud canvas config is NOT fully in this repo — docs describe visible nodes, not their internals.

## Environment: always use the venv

System `python3` lacks dependencies (`pymupdf` missing). Never use it.

```sh
.venv/bin/python -m pytest -q                            # root suite, 13 tests
.venv/bin/python -m pytest myhydra/double_pdf/tests -q  # 33 tests, NOT collected by default
```

`pyproject.toml` sets `testpaths = ["tests"]`, so the Double PDF suite only runs with the explicit path. Ruff (`line-length = 100`, `py310`) is in the venv but nothing enforces it — no CI, no pre-commit.

## Source of truth hierarchy

- `src/` is authoritative. Copies under `myhydra/` (prompts, pytools) must stay **byte-identical**; each has a README with the expected sha256. If hashes diverge, `src/` wins — recopy the file and update the hash.
- `legacy/` is read-only reference material. Never modify it; new work goes in `myhydra/`.
- Docs can be stale — the root README says so explicitly. `data/test_inputs/`, `data/test_outputs/`, and `tests/*/outputs/` contain mixed-provenance files: check a file's role before using it as ground truth. Fixture names starting with `observed_` are pasted runtime outputs (sanitized), `expected_` are derived.

## MyHydra script constraints (non-negotiable on canvas)

Pytool scripts pasted into MyHydra nodes must be standalone: inline code only, **no `def`/`class`/`lambda`**, output assigned to the `result` variable. They cannot import `src.*` — pydantic validation is skipped by design on the platform (`_pydantic_available = False`, pipeline continues identically). Paste clean: a stray non-Python line (e.g. an annotation like `riga 5` copied from chat) is a compile-time SyntaxError — `result` is never assigned, the node exposes nothing and downstream starves **silently** (blank output, not even an ERROR JSON, because `try/except` never runs).

- `{question}` = current iteration input; `{edge}[N]` = another node's text output (`N` is canvas-local, re-check after rewiring). **Edges can carry match conditions**: a leftover placeholder condition (seen: `pippo` on a filter→injection edge) silently blocks the wire — the downstream injection starves with no error. After any rewiring, inspect edge settings and remove stray conditions.
- VLM nodes: two verified working layouts — legacy single Prompt field with instructions **and** `{edge.media}[N]` inline (legacy screenshots show `[19]`–`[23]`), and the split layout (`{edge.media}[N]` alone in Prompt, instructions in Powered identity, Context empty; verified 2 Oct 2026 with `image_readable: true`). The empty shells were a Medex input problem, never a field-layout problem.

## Before starting work

Read the current work-state file for the area: `myhydra/single_pdf/PENDENZE.md`, `myhydra/double_pdf/WORKFLOW_DESIGN.md`. Node cards live in `myhydra/*/nodes/` (`lv1_`/`lv2_` prefixes); Double PDF copy-paste material is organized per subplatform in `myhydra/double_pdf/platforms/` (`prompts/current/` vs `prompts/history/`, `scripts/in_use/` vs `updated_pending_validation/` vs `parked/`).

When passing a script or prompt change to the user, always paste the **complete file** with changes applied — never a single line or fragment. They copy-paste into the MyHydra canvas, so fragments slow them down. Mark temporary/debug lines with a `DEBUG` comment so they can be reverted.

Always refer to canvas nodes by their **exact node names** (e.g. `FILTER_MEASUREMENT_TECHNICAL_DATA`, not "the measurement filter"). When providing a prompt, always give the **raw markdown** ready to paste.

Always communicate with the user in **Italian**. VLM prompts and code stay in English (technical artifacts); everything else — chat, docs, commit messages — in Italian.

Sync habit in this repo is `sync.sh`: `git pull origin main`, `git add .`, timestamp commit, `git push origin main`.

## Stato attuale (5 ott 2026)

- Single PDF: prompt v13 + `src/nodes/json_creator.py` v4.3. Registro verificato in `myhydra/single_pdf/PENDENZE.md` (A1 guardia copertura mai attivabile, A2 copia `myhydra/` ferma a v4.2 — entrambi aperti).
- Double PDF caso 6: LV1 verificata (14 pagine uniche, filtri 6 Station / 7 Measurement / 1 Density); LV2 Station verificata (6 pagine associate); LV2 Measurement a 3 rami verificata (65 misure leggero, 69 misure serie Qwen 3.8, BIT ramo misure corretto 6/6 da coordinate PDF).
- Lavoro non committato in corso: assemblatore per pagina `assemble_page_measurements.py` + `test_assemble_page_measurements.py` (5 test); consolidatore LV1 `consolidate_to_intermediate.py` + scheda `nodes/lv1_06_consolidator.md` + `test_consolidate_to_intermediate.py` (5 test); 7 nuovi fixture `observed_lv2_*` + 1 station; riallineamento edge tagger (`{edge}[8]`/`[4]`/`[5]`); doc (`WORKFLOW_DESIGN.md`, `lv2_06`, `platforms/README.md`, report qualità Double PDF).

## Prossimo passo

Cablare su canvas i due pytool non iterativi ancora solo locali: (1) assemblatore per pagina dentro la sottopiattaforma Measurement dopo i tagger (riportare nello script gli indici reali misure/bitinfo/stati e nel doc); (2) `CONSOLIDA INTERMEDIO VLM` dopo le iniezioni LV2 (impostare `STATION_EDGE`/`MEASURE_EDGE`/`DENSITY_EDGE` reali — con `None` lo script fallisce esplicitamente). Poi re-run fresca con script verificati identici al repo e confronto con i fixture serie prima di progettare l'output ADAS finale via `json_creator`.
