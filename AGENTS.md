# AGENTS.md — Menerva MAS

Python 3.10. This repo converts PLC/SCADA mapping PDFs into ADAS JSON (Single PDF flow live on a cloud platform; Double PDF IOL+JOB flow in development). The cloud canvas config is NOT fully in this repo — docs describe visible nodes, not their internals.

## Environment: always use the venv

System `python3` lacks dependencies (`pymupdf` missing). Never use it.

```sh
.venv/bin/python -m pytest -q                            # root suite, 13 tests
.venv/bin/python -m pytest myhydra/double_pdf/tests -q  # 23 tests, NOT collected by default
```

`pyproject.toml` sets `testpaths = ["tests"]`, so the Double PDF suite only runs with the explicit path. Ruff (`line-length = 100`, `py310`) is in the venv but nothing enforces it — no CI, no pre-commit.

## Source of truth hierarchy

- `src/` is authoritative. Copies under `myhydra/` (prompts, pytools) must stay **byte-identical**; each has a README with the expected sha256. If hashes diverge, `src/` wins — recopy the file and update the hash.
- `legacy/` is read-only reference material. Never modify it; new work goes in `myhydra/`.
- Docs can be stale — the root README says so explicitly. `data/test_inputs/`, `data/test_outputs/`, and `tests/*/outputs/` contain mixed-provenance files: check a file's role before using it as ground truth. Fixture names starting with `observed_` are pasted runtime outputs (sanitized), `expected_` are derived.

## MyHydra script constraints (non-negotiable on canvas)

Pytool scripts pasted into MyHydra nodes must be standalone: inline code only, **no `def`/`class`/`lambda`**, output assigned to the `result` variable. They cannot import `src.*` — pydantic validation is skipped by design on the platform (`_pydantic_available = False`, pipeline continues identically).

- `{question}` = current iteration input; `{edge}[N]` = another node's text output (`N` is canvas-local, re-check after rewiring).
- VLM nodes take the image **only** in the Prompt field as `{edge.media}[N]`; Context stays empty; instructions go in Powered identity. Never embed the media token inside instruction text.

## Before starting work

Read the current work-state file for the area: `myhydra/single_pdf/PENDENZE.md`, `myhydra/double_pdf/WORKFLOW_DESIGN.md`. Node cards live in `myhydra/*/nodes/` (`lv1_`/`lv2_` prefixes); Double PDF copy-paste material is organized per subplatform in `myhydra/double_pdf/platforms/` (`prompts/current/` vs `prompts/history/`, `scripts/in_use/` vs `updated_pending_validation/` vs `parked/`).

When passing a script or prompt change to the user, always paste the **complete file** with changes applied — never a single line or fragment. They copy-paste into the MyHydra canvas, so fragments slow them down. Mark temporary/debug lines with a `DEBUG` comment so they can be reverted.

Sync habit in this repo is `sync.sh`: `git pull origin main`, `git add .`, timestamp commit, `git push origin main`.
