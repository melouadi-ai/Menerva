"""Parita' fra riferimento, copia documentata e copia canvas del consolidatore."""

import ast
import io
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from nodes.single_consolidator import consolidate

REPO = Path(__file__).parent.parent
DOCUMENTED = REPO / "myhydra" / "single_pdf" / "pytools" / "consolidator.py"
CANVAS = REPO / "myhydra" / "single_pdf" / "pytools" / "consolidator_canvas.py"

CANVAS_MAX_BYTES = 28 * 1024


def fixture_pages():
    return [
        {"page_no": 1, "stations": [{
            "name": None, "protocol": "ModBus TCP", "ip": "192.168.2.11",
            "port": 502, "modbus_id": None, "variables": [
                {"description": "SO2", "units": None,
                 "modbus_register": 49, "bit": None, "data_type": "INT",
                 "kind": "ANALOGICA", "read_write": "R",
                 "state_on": None, "state_off": None,
                 "scale_elec_start": None, "scale_elec_end": None,
                 "scale_eng_start": None, "scale_eng_end": None,
                 "limit_hour": None, "limit_day": None,
                 "zona": "MISURE", "tag": "SO2", "pagina": None,
                 "riga": 1},
                {"description": "SO2 fondo scala", "units": None,
                 "modbus_register": 50, "bit": None, "data_type": None,
                 "kind": "ANALOGICA", "read_write": "R",
                 "state_on": None, "state_off": None,
                 "scale_elec_start": None, "scale_elec_end": None,
                 "scale_eng_start": 0, "scale_eng_end": 300,
                 "limit_hour": None, "limit_day": None,
                 "zona": "MISURE", "tag": "SO2", "pagina": None,
                 "riga": 2},
            ]}],
         "bitnames": {"rows": [
             {"description": "SO2", "modbus_register": 49, "bit": None,
              "riga": 1},
             {"description": "SO2 fondo scala", "modbus_register": 50,
              "bit": None, "riga": 2},
         ]}},
        {"page_no": 2, "stations": [{
            "name": None, "protocol": "ModBus TCP", "ip": "192.168.2.11",
            "port": 502, "modbus_id": None, "variables": [
                {"description": "Allarme sonda", "units": None,
                 "modbus_register": None, "bit": 8, "data_type": None,
                 "kind": "DIGITALE_IMPACCATO", "read_write": "R",
                 "state_on": None, "state_off": None,
                 "scale_elec_start": None, "scale_elec_end": None,
                 "scale_eng_start": None, "scale_eng_end": None,
                 "limit_hour": None, "limit_day": None,
                 "zona": "ALLARMI", "tag": None, "pagina": None,
                 "riga": 1},
            ]}]},
    ]


def run_script(path, pages):
    source = path.read_text(encoding="utf-8")
    patched = re.sub(r"raw\s*=\s*r?'''\{edge\}\[\d+\]'''",
                     "raw = __INJECTED_RAW__", source)
    assert patched != source
    ns = {"__INJECTED_RAW__": pages}
    exec(compile(patched, str(path), "exec"), ns)
    return json.loads(ns["result"])


def test_canvas_sotto_soglia_dimensionale():
    assert os.path.getsize(CANVAS) <= CANVAS_MAX_BYTES


def test_canvas_stesso_ast_del_documentato():
    assert (ast.dump(ast.parse(DOCUMENTED.read_text(encoding="utf-8")))
            == ast.dump(ast.parse(CANVAS.read_text(encoding="utf-8"))))


def test_canvas_stesso_output_del_documentato():
    pages = fixture_pages()
    a = run_script(DOCUMENTED, pages)
    b = run_script(CANVAS, pages)
    assert a == b
    assert a["warnings"] != []
    by_desc = {v["description"]: v for s in a["stations"]
               for v in s["variables"]}
    assert by_desc["SO2"]["scale_eng_end"] == 300
    assert by_desc["Allarme sonda"]["modbus_register"] == 50


def test_riferimento_src_allineato_al_documentato():
    pages = fixture_pages()
    ref = consolidate([json.loads(json.dumps(p)) for p in pages])
    doc = run_script(DOCUMENTED, pages)
    assert ref == doc


def test_canvas_senza_def_lambda_class():
    src = CANVAS.read_text(encoding="utf-8")
    assert "def " not in src
    assert "lambda" not in src
    assert "class " not in src
