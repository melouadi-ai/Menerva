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

## Confronto con il legacy: il GT non è un riferimento di qualità

`tests/compare_with_gt.py` confronta output vs `data/test_outputs/gaia_doublefile_result_6.json`, ma il legacy **ha errori propri**: letto riga per riga, `Mappatura_6_Cliente_SMI_1.pdf` dà 22 misure e **60** bitinfo, il GT ne ha 78. In dettaglio: 18 bitinfo fantasma (12 su righe senza TITOLO, più `PM-2601A/B` e i 4 ventilatori duplicati), due registri comandi sbagliati (430/431 invece di 431/432, shift di una riga su una riga bianca trattata come misura), `TEXTON` disallineati di una posizione, `QAL3` da `INT` scritti 250 invece di 150, e i nomi `STIMATA SO2`/`… ARI` troncati.

Conseguenza: **le differenze di un confronto col GT non vanno colmate senza verifica sul PDF.** Il metodo è in `tests/test_adas_caso6_pdf_truth.py`, che fissa la tabella verità e registra anche dove il legacy sbaglia (`test_legacy_ha_errori_noti_il_nostro_no`), così nessuna correzione futura li riporta indietro per allineamento.

Attenzione anche alle unità: nel PDF IOL del caso 6 **non esiste la colonna unità**. `mg/Nm3` e `°C` nel GT sono inferenze del legacy; noi emettiamo `mg/Nm3` solo dove la scala SO2 è dichiarata e `null` altrove. Non trattare `°C` come un dato mancante da recuperare: è una decisione di dominio (vedi `reports/CONFRONTO_QUALITA_LEGACY_VS_ATTUALE.md`).

## Stato attuale (5 ott 2026)

- Single PDF: prompt v13 + `src/nodes/json_creator.py` v4.4 (A1 soglia 100, A2 copia `myhydra/` allineata). Registro in `myhydra/single_pdf/PENDENZE.md`.
- Double PDF: catena LV1→LV2→consolidatore→ADAS verificata end-to-end sui casi 6 e 7 con Qwen 3.8. Caso 6 ha il **verdetto completo**: 22 misure + 60 bitinfo confrontati riga per riga col PDF, 22/22 registri, tutti i bit, formati `INT`→150 e `REAL`→250, `UNITS mg/Nm3` su SO2/SO2 Raw, linkage intatto. Fixture `tests/double_pdf_outputs/observed_adas_case6_qwen38_datatype.json`, tabella verità `tests/test_adas_caso6_pdf_truth.py`.
- Caso 7: uscita ADAS prodotta (39 misure + 42 bitinfo, `172.16.1.31:511`, 5 variabili scartate con warning) ma **non ancora confrontata riga per riga col PDF**.

## Prossimo passo

1. Caso 7: stesso metodo del caso 6 — leggere il PDF IOL riga per riga, produrre la tabella verità, fissarla in un test. È l'unico pezzo di verifica che manca.
2. Attendere dal cliente: fonte delle unità di misura, nome stazione in ADAS, BISON, zeri iniziali, regola V2.
3. Terza coppia IOL+JOB mai vista, per allargare il campione oltre 6 e 7.
