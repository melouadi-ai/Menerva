"""Parita' e igiene del pytool ORACLE_APPLY (redesign v2)."""

import ast
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

REPO = Path(__file__).parent.parent
DOCUMENTED = REPO / "myhydra" / "single_pdf" / "pytools" / "oracle_apply.py"
CANVAS = REPO / "myhydra" / "single_pdf" / "pytools" / "oracle_apply_canvas.py"

CANVAS_MAX_BYTES = 34300

EDGE_RE = re.compile(r"(raw_c|raw_v)\s*=\s*r?'''\{edge\}\[\d+\]'''")


def run_script(path, consolidated, engine):
    """Esegue lo script con i due edge iniettati (raw_c, raw_v)."""
    source = path.read_text(encoding="utf-8")
    patched = EDGE_RE.sub(lambda m: "%s = __%s__" % (m.group(1),
                                                     m.group(1).upper()),
                          source)
    assert patched != source
    ns = {"__RAW_C__": consolidated, "__RAW_V__": engine}
    exec(compile(patched, str(path), "exec"), ns)
    return json.loads(ns["result"])


def _consolidated():
    return {
        "stations": [{
            "name": "SME", "protocol": "ModBus TCP", "ip": "10.0.0.1",
            "port": 502, "modbus_id": None,
            "variables": [
                {"description": "SO2", "units": "mg/Nm3",
                 "modbus_register": 49, "bit": None, "kind": "ANALOGICA",
                 "state_on": None, "state_off": None, "riga": 1},
                {"description": "Allarme sonda", "units": None,
                 "modbus_register": 50, "bit": 3,
                 "kind": "DIGITALE_IMPACCATO", "state_on": "1",
                 "state_off": None, "riga": 2},
            ]}],
        "warnings": [{"rule": "pagina_vuota_sospetta", "page_no": 1,
                      "riga": None, "detail": "x"}],
        "counters": {"pagine": 1},
    }


def _engine():
    return [{"page_no": 1, "verifica": {
        "page_no": 1,
        "mancanti": [{"description": "NOX", "registro": 51, "bit": None,
                      "evidenza": "riga 3: NOX 40051"}],
        "unita_inventate": [{"description": "SO2", "unita": "mg/Nm3",
                             "evidenza": "cella vuota"}],
        "junk_stati": [{"description": "Allarme sonda",
                        "campo": "state_on", "valore": "1",
                        "evidenza": "cella vuota"}],
        "refusi_corretti": [{"description_finale": "Ossigeno",
                             "description_pdf": "Ossiegno",
                             "evidenza": "cella: Ossiegno"}],
        "ip_dichiarati_non_usati": [{"ip": "10.0.0.2",
                                     "evidenza": "IP PLC: 10.0.0.2"}],
    }}]


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


def test_aggiunge_annulla_e_audit():
    out = run_script(CANVAS, _consolidated(), _engine())
    by_desc = {v["description"]: v for v in out["stations"][0]["variables"]}
    assert set(by_desc) == {"SO2", "Allarme sonda", "NOX"}
    # Aggiunta con audit.
    assert by_desc["NOX"]["modbus_register"] == 51
    assert by_desc["NOX"]["_audit_oracolo"]["azione"] == "aggiunta"
    assert by_desc["NOX"]["_audit_oracolo"]["evidenza"].startswith("riga 3")
    # Unita' inventata annullata.
    assert by_desc["SO2"]["units"] is None
    assert by_desc["SO2"]["_audit_oracolo"]["campo"] == "units"
    # Stato junk annullato.
    assert by_desc["Allarme sonda"]["state_on"] is None
    assert by_desc["Allarme sonda"]["_audit_oracolo"]["campo"] == "state_on"
    rules = [w["rule"] for w in out["warnings"]]
    assert "oracolo_aggiunta" in rules
    assert "oracolo_annullata" in rules
    assert "oracolo_refuso" in rules
    assert "oracolo_ip" in rules
    # Refuso e IP: solo warning, nessuna stazione inventata.
    assert len(out["stations"]) == 1
    assert by_desc["SO2"]["description"] == "SO2"


def test_evidenza_vuota_non_applica():
    cons = _consolidated()
    engine = [{"page_no": 1, "verifica": {
        "mancanti": [], "junk_stati": [], "refusi_corretti": [],
        "ip_dichiarati_non_usati": [],
        "unita_inventate": [{"description": "SO2", "unita": "mg/Nm3",
                             "evidenza": ""}]}}]
    out = run_script(CANVAS, cons, engine)
    by_desc = {v["description"]: v for v in out["stations"][0]["variables"]}
    assert by_desc["SO2"]["units"] == "mg/Nm3"
    assert "_audit_oracolo" not in by_desc["SO2"]
    assert "oracolo_evidenza_vuota" in [w["rule"] for w in out["warnings"]]


def test_duplicato_non_aggiunto():
    cons = _consolidated()
    engine = [{"page_no": 1, "verifica": {
        "mancanti": [{"description": "SO2", "registro": 49, "bit": None,
                      "evidenza": "riga 1"}],
        "unita_inventate": [], "junk_stati": [], "refusi_corretti": [],
        "ip_dichiarati_non_usati": []}}]
    out = run_script(CANVAS, cons, engine)
    assert len(out["stations"][0]["variables"]) == 2
    assert "oracolo_duplicato" in [w["rule"] for w in out["warnings"]]


def test_senza_verifica_invariato():
    out = run_script(CANVAS, _consolidated(), [{"page_no": 1,
                                                "stations": []}])
    assert out["stations"] == _consolidated()["stations"]
    assert not any(w["rule"].startswith("oracolo_")
                   for w in out["warnings"])


def test_documentato_e_canvas_stesso_output():
    a = run_script(DOCUMENTED, _consolidated(), _engine())
    b = run_script(CANVAS, _consolidated(), _engine())
    assert a == b


def test_input_non_interpretabile_errore_esplicito():
    out = run_script(CANVAS, "non json", "non json")
    assert out["status"] == "ERROR"
    assert out["tb"]
    out2 = run_script(CANVAS, {"stations": "x"}, [])
    assert out2["status"] == "ERROR"
    assert "oracle_apply" in out2["error"]
