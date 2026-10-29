#!/usr/bin/env bash
# Test della suite Menerva MAS, sempre con il Python del progetto.
#
# Perche' esiste: `/usr/bin/python3` (3.12, di sistema) non ha le dipendenze
# del progetto (`pymupdf`, `pytest`, `pydantic`). Lanciare `pytest` da li'
# fallisce con "No module named pytest" e non e' un test rosso: e' un
# interprete sbagliato. Questo script sceglie l'interprete giusto da solo.
#
# Uso:
#   ./run_tests.sh                       # suite root (tests/)
#   ./run_tests.sh double                # suite Double PDF
#   ./run_tests.sh all                   # entrambe
#   ./run_tests.sh tests/test_multipage.py -k warning   # argomenti extra a pytest
set -euo pipefail

cd "$(dirname "$0")"

# 1) venv del repository (quello usato da AGENTS.md e dai README)
PY=".venv/bin/python"

# 2) fallback: uv, che ricrea l'ambiente dichiarato in pyproject/.python-version
if [ ! -x "$PY" ] || ! "$PY" -c "import pytest" >/dev/null 2>&1; then
    if command -v uv >/dev/null 2>&1; then
        echo "[run_tests] .venv assente o incompleto: preparo l'ambiente con uv" >&2
        uv venv --python 3.10 .venv >/dev/null 2>&1 || uv venv .venv
        uv pip install --python "$PY" -e ".[dev]" >/dev/null
    fi
fi

if [ ! -x "$PY" ] || ! "$PY" -c "import pytest" >/dev/null 2>&1; then
    echo "[run_tests] ERRORE: nessun interprete con pytest." >&2
    echo "[run_tests] Crea l'ambiente con: uv venv .venv && uv pip install -e '.[dev]'" >&2
    exit 2
fi

target="${1:-}"
case "$target" in
    double)
        shift
        exec "$PY" -m pytest myhydra/double_pdf/tests -q "$@"
        ;;
    all)
        shift
        "$PY" -m pytest -q "$@"
        "$PY" -m pytest myhydra/double_pdf/tests -q "$@"
        ;;
    "")
        exec "$PY" -m pytest -q
        ;;
    *)
        exec "$PY" -m pytest "$@"
        ;;
esac
