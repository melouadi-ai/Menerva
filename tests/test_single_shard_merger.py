"""Slicer + merger Single PDF per shard paralleli (pilot PROTEC 2, SIEMENS).

Lo slicer ritaglia fette di gruppi-pagina, il merger ricuce i chunk in
ordine. Stessa disciplina delle altre copie canvas: AST doc==canvas,
niente def/class/lambda, budget paste, ERROR mai blank, e passaggio nel
modello di exec del canvas (globals/locals separati).
"""

import ast
import builtins
import json
import os
import re
from pathlib import Path

REPO = Path(__file__).parent.parent
PYTOOLS = (REPO / "myhydra" / "single_pdf" / "platforms" / "lv1"
           / "scripts" / "updated_pending_validation")
STORE = REPO / "myhydra" / "single_pdf" / "pytools"

SLICER_DOC = STORE / "slicer.py"
SLICER_CANVAS = STORE / "slicer_canvas.py"
SLICER_PLAT = PYTOOLS / "slicer_canvas.py"
MERGER_DOC = STORE / "merger.py"
MERGER_CANVAS = STORE / "merger_canvas.py"
MERGER_PLAT = PYTOOLS / "merger_canvas.py"

CANVAS_MAX_BYTES = 28 * 1024

GROUPS_29 = [{"_medexkeys": {"key": "K%02d" % i}} for i in range(1, 30)]


def run_slicer(path, groups, start=None, end=None):
    source = Path(path).read_text(encoding="utf-8")
    patched = re.sub(r"raw\s*=\s*r?'''\{edge\}\[\d+\]'''",
                     "raw = __INJECTED_RAW__", source)
    assert patched != source
    if start is not None:
        patched = re.sub(r"^START\s*=\s*\d+", "START = %d" % start,
                         patched, flags=re.M)
    if end is not None:
        patched = re.sub(r"^END\s*=\s*\d+", "END = %d" % end,
                         patched, flags=re.M)
    ns = {"__INJECTED_RAW__": groups}
    exec(compile(patched, str(path), "exec"), ns)
    return json.loads(ns["result"])


def run_merger_canvas_model(path, chunk_a, chunk_b):
    source = Path(path).read_text(encoding="utf-8")
    patched = re.sub(r"raw_a\s*=\s*r?'''\{edge\}\[\d+\]'''",
                     "raw_a = __INJECTED_A__", source)
    patched = re.sub(r"raw_b\s*=\s*r?'''\{edge\}\[\d+\]'''",
                     "raw_b = __INJECTED_B__", patched)
    assert patched != source
    g = {"__builtins__": builtins}
    loc = {"__INJECTED_A__": chunk_a, "__INJECTED_B__": chunk_b}
    exec(compile(patched, str(path), "exec"), g, loc)
    return json.loads(loc["result"])


def run_merger_single(path, chunk_a, chunk_b):
    source = Path(path).read_text(encoding="utf-8")
    patched = re.sub(r"raw_a\s*=\s*r?'''\{edge\}\[\d+\]'''",
                     "raw_a = __INJECTED_A__", source)
    patched = re.sub(r"raw_b\s*=\s*r?'''\{edge\}\[\d+\]'''",
                     "raw_b = __INJECTED_B__", patched)
    ns = {"__INJECTED_A__": chunk_a, "__INJECTED_B__": chunk_b}
    exec(compile(patched, str(path), "exec"), ns)
    return json.loads(ns["result"])


def test_slicer_fette_siemens():
    assert run_slicer(SLICER_DOC, GROUPS_29, 1, 10) == GROUPS_29[0:10]
    assert run_slicer(SLICER_DOC, GROUPS_29, 11, 20) == GROUPS_29[10:20]
    assert run_slicer(SLICER_DOC, GROUPS_29, 21, 29) == GROUPS_29[20:29]
    assert run_slicer(SLICER_DOC, GROUPS_29[:2], 2, 2) == GROUPS_29[1:2]


def test_slicer_range_impossibile_errore_forte():
    for start, end in ((0, 5), (5, 4), (1, 30), (30, 30)):
        out = run_slicer(SLICER_DOC, GROUPS_29, start, end)
        assert out["status"] == "ERROR"
        assert "fetta" in out["error"]
        assert out["tb"] != ""
    out = run_slicer(SLICER_DOC, {"non": "lista"}, 1, 1)
    assert out["status"] == "ERROR"


def test_slicer_input_stringa_json():
    raw = json.dumps(GROUPS_29)
    assert run_slicer(SLICER_DOC, raw, 1, 10) == GROUPS_29[0:10]


def test_merger_concatena_in_ordine():
    a = [{"stations": [{"name": "P1"}]}, {"rows": [{"riga": 1}]}]
    b = [{"stations": [{"name": "P2"}]}]
    for path in (MERGER_DOC, MERGER_CANVAS):
        out = run_merger_single(path, a, b)
        assert out == a + b
        out = run_merger_canvas_model(path, a, b)
        assert out == a + b


def test_merger_stringhe_con_fence():
    a = "```json\n{\"stations\": []}\n```\n```json\n{\"rows\": []}\n```"
    b = [{"stations": []}]
    out = run_merger_canvas_model(MERGER_CANVAS, a, b)
    assert out == [{"stations": []}, {"rows": []}, {"stations": []}]


def test_merger_shard_vuoto_errore_forte():
    out = run_merger_canvas_model(MERGER_CANVAS, [{"stations": []}], [])
    assert out["status"] == "ERROR"
    assert "shard B" in out["error"]
    out = run_merger_canvas_model(MERGER_CANVAS, "spazzatura ]]]", [{"x": 1}])
    assert out["status"] == "ERROR"
    assert "shard A" in out["error"]


def test_copie_canvas_identico_ast_e_budget():
    for doc, canvas, plat in ((SLICER_DOC, SLICER_CANVAS, SLICER_PLAT),
                             (MERGER_DOC, MERGER_CANVAS, MERGER_PLAT)):
        assert canvas.read_bytes() == plat.read_bytes()
        assert (ast.dump(ast.parse(doc.read_text(encoding="utf-8")))
                == ast.dump(ast.parse(canvas.read_text(encoding="utf-8"))))
        assert os.path.getsize(canvas) <= CANVAS_MAX_BYTES
        src = canvas.read_text(encoding="utf-8")
        assert "def " not in src
        assert "lambda" not in src
        assert "class " not in src
        assert "result =" in src
