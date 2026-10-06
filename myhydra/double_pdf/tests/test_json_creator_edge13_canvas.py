"""Parita' tra la copia canvas e il file documentato del JSON CREATOR Double.

Il 6/10/2026 il file documentato `json_creator_edge13.py` (34.365 byte) ha
mandato in rosso il nodo 12 sul canvas, mentre la versione precedente
(32.766 byte) passava. La copia canvas senza commenti (26.731 byte, stesso
AST) passa. Evidenza: il paste oltre una certa dimensione fallisce, a parita'
di logica.

Questi test bloccano la disciplina: la copia canvas deve restare
comportamentalmente identica al file documentato. Se divergono, il test
fallisce e la copia va rigenerata, non rattoppata a mano.
"""
import ast
import io
import json
import os
import re
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
DOCUMENTED = os.path.join(
    REPO, "myhydra", "double_pdf", "platforms", "lv1", "scripts", "in_use",
    "json_creator_edge13.py",
)
CANVAS = os.path.join(
    REPO, "myhydra", "double_pdf", "platforms", "lv1", "scripts", "in_use",
    "json_creator_edge13_canvas.py",
)
CHUNK = os.path.join(
    REPO, "myhydra", "double_pdf", "tests", "case_6", "outputs",
    "observed_lv1_consolidator_qwen38_chunk.json",
)

# Soglia empirica del paste sul canvas (6/10/2026): 32.766 byte passano,
# 34.365 no. Margine di sicurezza incluso.
CANVAS_MAX_BYTES = 32000


def load(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def run_script(source, raw_value):
    src2 = re.sub(r"raw\s*=\s*r?'''\{edge\}\[\d+\]'''", "raw = __INJECTED_RAW__", source)
    ns = {"__INJECTED_RAW__": raw_value}
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        exec(compile(src2, "json_creator", "exec"), ns)
    finally:
        sys.stdout = old_stdout
    return json.loads(ns.get("output", "null"))


def test_canvas_sotto_soglia_dimensionale():
    size = os.path.getsize(CANVAS)
    assert size <= CANVAS_MAX_BYTES, size


def test_canvas_stesso_ast_del_documentato():
    assert ast.dump(ast.parse(load(DOCUMENTED))) == ast.dump(ast.parse(load(CANVAS)))


def test_canvas_stesso_output_sul_chunk_caso6():
    with open(CHUNK, encoding="utf-8") as f:
        chunk = json.load(f)
    a = run_script(load(DOCUMENTED), chunk)[0]
    b = run_script(load(CANVAS), chunk)[0]
    assert len(a["measures"]) == len(b["measures"]) == 22
    assert len(a["bitinfo"]) == len(b["bitinfo"]) == 60
    ka = [(m["NAME"], m["DRIVERPRIVATE"]) for m in a["measures"]]
    kb = [(m["NAME"], m["DRIVERPRIVATE"]) for m in b["measures"]]
    assert ka == kb
    ta = [(x["BITNAME"], x["BITNO"], x["TEXTON"], x["TEXTOFF"]) for x in a["bitinfo"]]
    tb = [(x["BITNAME"], x["BITNO"], x["TEXTON"], x["TEXTOFF"]) for x in b["bitinfo"]]
    assert ta == tb


def test_canvas_senza_def_lambda_class():
    src = load(CANVAS)
    assert "def " not in src and "lambda" not in src and "class " not in src
