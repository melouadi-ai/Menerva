"""PAGE_ASSEMBLER (LV2-03): unisce UNIFIED + ORACOLO in una pagina."""

import ast
import json
import os
import re
from pathlib import Path

REPO = Path(__file__).parent.parent
DOCUMENTED = REPO / "myhydra" / "single_pdf" / "pytools" / "page_assembler.py"
CANVAS = REPO / "myhydra" / "single_pdf" / "pytools" / "page_assembler_canvas.py"

CANVAS_MAX_BYTES = 34300
EDGE_RE = re.compile(r"(raw_u|raw_o)\s*=\s*r?'''\{edge\}\[\d+\]'''")


def run_script(path, unified, oracle):
    source = path.read_text(encoding="utf-8")
    patched = EDGE_RE.sub(lambda m: "%s = __%s__" % (m.group(1),
                                                    m.group(1).upper()),
                          source)
    assert patched != source
    ns = {"__RAW_U__": unified, "__RAW_O__": oracle}
    exec(compile(patched, str(path), "exec"), ns)
    return json.loads(ns["result"])


def _unified():
    return {"page_no": 3, "stations": [{
        "name": "SME", "protocol": "ModBus TCP", "ip": "10.0.0.1",
        "port": 502, "modbus_id": None,
        "variables": [{"description": "SO2", "units": "mg/Nm3",
                       "modbus_register": 49, "bit": None}]}]}


def _oracle():
    return {"page_no": 3,
            "mancanti": [{"description": "NOX", "registro": 51, "bit": None,
                          "evidenza": "riga 3: NOX 40051"}],
            "unita_inventate": [],
            "junk_stati": [],
            "refusi_corretti": [],
            "ip_dichiarati_non_usati": []}


def test_canvas_sotto_soglia_dimensionale():
    assert os.path.getsize(CANVAS) <= CANVAS_MAX_BYTES


def test_canvas_stesso_ast_del_documentato():
    assert (ast.dump(ast.parse(DOCUMENTED.read_text(encoding="utf-8")))
            == ast.dump(ast.parse(CANVAS.read_text(encoding="utf-8"))))


def test_canvas_standalone_senza_def_class_lambda():
    for path in (DOCUMENTED, CANVAS):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            assert not isinstance(node, (ast.FunctionDef, ast.ClassDef,
                                         ast.Lambda)), path.name


def test_assembla_pagina_con_verifica_completa():
    out = run_script(CANVAS, _unified(), _oracle())
    assert out["page_no"] == 3
    assert out["stations"] == _unified()["stations"]
    ver = out["verifica"]
    assert set(ver) == {"page_no", "mancanti", "unita_inventate",
                        "junk_stati", "refusi_corretti",
                        "ip_dichiarati_non_usati"}
    assert ver["page_no"] == 3
    assert ver["mancanti"][0]["description"] == "NOX"
    assert out["assemble_warnings"] == []


def test_oracolo_senza_categorie_segnalato():
    out = run_script(CANVAS, _unified(), {"page_no": 3})
    assert out["verifica"] is None
    assert out["assemble_warnings"][0].startswith("oracolo_assente")


def test_oracolo_vuoto_segnalato():
    out = run_script(CANVAS, _unified(), "")
    assert out["verifica"] is None
    assert any("oracolo_assente" in w for w in out["assemble_warnings"])


def test_errore_input_oracolo_segnalato():
    ora = {"page_no": 3, "errore_input": "json UNIFIED assente"}
    out = run_script(CANVAS, _unified(), ora)
    assert out["verifica"] is not None
    assert out["verifica"]["mancanti"] == []
    assert any(w.startswith("oracolo_input_assente")
               for w in out["assemble_warnings"])


def test_page_no_dall_oracolo_se_unified_non_lo_ha():
    page = _unified()
    page["page_no"] = None
    out = run_script(CANVAS, page, _oracle())
    assert out["page_no"] == 3
    assert out["verifica"]["page_no"] == 3


def test_input_con_fence_json():
    unified = "```json\n" + json.dumps(_unified()) + "\n```"
    oracle = "```json\n" + json.dumps(_oracle()) + "\n```"
    out = run_script(CANVAS, unified, oracle)
    assert out["page_no"] == 3
    assert out["verifica"]["mancanti"]


def test_unified_non_interpretabile_errore_esplicito():
    out = run_script(CANVAS, "non json", _oracle())
    assert out["status"] == "ERROR"
    assert out["tb"]
    out2 = run_script(CANVAS, {"stations": "x"}, _oracle())
    assert out2["status"] == "ERROR"
    assert "page_assembler" in out2["error"]


def test_oracolo_non_interpretabile_non_blocca_la_pagina():
    out = run_script(CANVAS, _unified(), "testo non json")
    assert out["stations"] == _unified()["stations"]
    assert out["verifica"] is None
    assert any(w.startswith("oracolo_non_interpretabile")
               for w in out["assemble_warnings"])


def test_documentato_e_canvas_stesso_output():
    a = run_script(DOCUMENTED, _unified(), _oracle())
    b = run_script(CANVAS, _unified(), _oracle())
    assert a == b
