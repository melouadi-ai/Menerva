"""Un comando e basta: `pytest` (qualunque pytest) esegue la suite col Python giusto.

Perche' esiste: la suite ha bisogno di `pytest`, `pymupdf`, `pydantic`, che
vivono solo in `.venv` (Python 3.10). Se un harness lancia `pytest` col Python
di sistema (3.12) ottiene `No module named pytest`, che non e' un test rosso ma
un interprete sbagliato. Questo file porta l'esecuzione sull'interprete
corretto e propaga il codice di uscita reale di pytest.

Mai un "passed" finto: se nessun ambiente ha le dipendenze, esce con 2.
"""

import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
VENV_PYTHON = os.path.join(ROOT, ".venv", "bin", "python")


def _venv_has_pytest():
    """True se `.venv/bin/python` esiste ed e' un ambiente del progetto."""
    return os.path.exists(VENV_PYTHON) and os.path.realpath(
        sys.executable) != os.path.realpath(VENV_PYTHON)


def main(argv):
    if _venv_has_pytest():
        os.chdir(ROOT)
        os.execv(VENV_PYTHON, [VENV_PYTHON, "-m", "pytest"] + argv)
    sys.stderr.write(
        "conftest.py: nessun ambiente con le dipendenze del progetto.\n"
        "  interprete: %s\n"
        "  atteso:     %s\n"
        "  crea:       uv venv --python 3.10 .venv && "
        "uv pip install -e '.[dev]'\n" % (sys.executable, VENV_PYTHON))
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
