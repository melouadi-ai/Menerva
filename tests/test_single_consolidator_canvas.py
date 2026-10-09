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

# Limite empirico MyHydra (6/10/2026): 34.365 byte = rosso,
# 32.766 = verde. Margine sotto il verde osservato.
CANVAS_MAX_BYTES = 32 * 1024


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
        {"page_no": 3, "stations": [{
            "name": None, "protocol": "ModBus TCP", "ip": "192.168.2.11",
            "port": 502, "modbus_id": None, "variables": [
                {"description": "CO", "units": None,
                 "modbus_register": 51, "bit": None, "data_type": None,
                 "kind": "ANALOGICA", "read_write": "R",
                 "state_on": None, "state_off": None,
                 "scale_elec_start": None, "scale_elec_end": None,
                 "scale_eng_start": None, "scale_eng_end": None,
                 "limit_hour": None, "limit_day": None,
                 "zona": "MISURE", "tag": None, "pagina": None,
                 "riga": 1},
                {"description": "Riserva", "units": None,
                 "modbus_register": 52, "bit": None, "data_type": None,
                 "kind": "ANALOGICA", "read_write": "R",
                 "state_on": None, "state_off": None,
                 "scale_elec_start": None, "scale_elec_end": None,
                 "scale_eng_start": None, "scale_eng_end": None,
                 "limit_hour": None, "limit_day": None,
                 "zona": "MISURE", "tag": None, "pagina": None,
                 "riga": 2},
                {"description": "Sonda", "units": None,
                 "modbus_register": 53, "bit": None, "data_type": None,
                 "kind": "ANALOGICA", "read_write": "R",
                 "state_on": None, "state_off": None,
                 "scale_elec_start": None, "scale_elec_end": None,
                 "scale_eng_start": None, "scale_eng_end": None,
                 "limit_hour": None, "limit_day": None,
                 "zona": "INPUT_HW", "tag": None, "pagina": None,
                 "riga": 3},
                {"description": "Pompa", "units": None,
                 "modbus_register": 54, "bit": None, "data_type": None,
                 "kind": "ANALOGICA", "read_write": "R",
                 "state_on": None, "state_off": None,
                 "scale_elec_start": None, "scale_elec_end": None,
                 "scale_eng_start": None, "scale_eng_end": None,
                 "limit_hour": None, "limit_day": None,
                 "zona": "CAMPO", "tag": None, "pagina": None,
                 "riga": 4, "note": "NO PC SME"},
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


def test_scarti_v2_v20_v21_con_reason_letterali():
    pages = fixture_pages()
    ref = consolidate([json.loads(json.dumps(p)) for p in pages])
    scarti = {w["rule"]: w["detail"] for w in ref["warnings"]
              if w["rule"].startswith("scarto_")}
    assert scarti["scarto_V2"] == \
        "Riserva - description is a spare/placeholder token: 'Riserva'"
    assert scarti["scarto_V21"] == \
        "Sonda - zona is a hardware zone: 'INPUT_HW'"
    assert scarti["scarto_V20"] == \
        "Pompa - annotation contains 'NO PC SME'"
    assert ref["counters"]["scarti_V2"] == 1
    assert ref["counters"]["scarti_V21"] == 1
    assert ref["counters"]["scarti_V20"] == 1


def test_canvas_senza_def_lambda_class():
    src = CANVAS.read_text(encoding="utf-8")
    assert "def " not in src
    assert "lambda" not in src
    assert "class " not in src


def run_script_canvas_model(path, raw_value):
    """Esegue la copia come fa MyHydra: globals e locals separati.

    Con namespace separati le comprehension non vedono i locali dello
    script (il corpo del genexpr non chiude sui locali di exec): questo
    runner riproduce il modello e inchioda la regressione
    "name 'block' is not defined" vista sul canvas (run SMA_1, ott 2026).
    """
    source = path.read_text(encoding="utf-8")
    patched = re.sub(r"raw\s*=\s*r?'''\{edge\}\[\d+\]'''",
                     "raw = __INJECTED_RAW__", source)
    assert patched != source
    g = {"__builtins__": __builtins__}
    loc = {"__INJECTED_RAW__": raw_value}
    exec(compile(patched, str(path), "exec"), g, loc)
    return json.loads(loc["result"])


def test_canvas_model_messaggio_chiavi_tipi_senza_nameerror():
    raw_value = {"pagina": "x", "count": 3}
    single = run_script(DOCUMENTED, raw_value)
    canvas = run_script_canvas_model(CANVAS, raw_value)
    assert canvas.pop("tb") and single.pop("tb")
    assert canvas == single
    assert canvas["status"] == "ERROR"
    assert "senza stations ne rows" in canvas["error"]
    assert "chiavi ['count', 'pagina']" in canvas["error"]
    assert "tipi {int, str}" in canvas["error"]
    assert "NameError" not in canvas["error"]


def test_canvas_model_righe_non_riconoscibili():
    pages = [{"stations": []}, {"rows": [{"zzz": 1}]}]
    single = run_script(DOCUMENTED, pages)
    canvas = run_script_canvas_model(CANVAS, pages)
    assert canvas.pop("tb") and single.pop("tb")
    assert canvas == single
    assert canvas["status"] == "ERROR"
    assert "non riconoscibile" in canvas["error"]


def test_canvas_model_output_pari_su_fixture():
    pages = fixture_pages()
    assert (run_script_canvas_model(CANVAS, pages)
            == run_script(DOCUMENTED, pages))


def _sma1_bare_states_blocks():
    station = {"name": "E1", "protocol": "ModBus TCP", "ip": "192.168.6.20",
               "port": None, "modbus_id": None, "variables": [
                   {"description": "CO", "units": "mg/Nm3",
                    "modbus_register": 40001, "bit": None,
                    "data_type": "ANALOGICO", "kind": "ANALOGICA",
                    "read_write": "R", "state_on": None, "state_off": None,
                    "scale_elec_start": None, "scale_elec_end": None,
                    "scale_eng_start": 0, "scale_eng_end": 200,
                    "limit_hour": None, "limit_day": None, "zona": None,
                    "tag": None, "pagina": None, "riga": 1},
                   {"description": "Allarme", "units": None,
                    "modbus_register": 33, "bit": None, "data_type": "WORD",
                    "kind": "DIGITALE_SINGOLO", "read_write": "R",
                    "state_on": None, "state_off": None,
                    "scale_elec_start": None, "scale_elec_end": None,
                    "scale_eng_start": None, "scale_eng_end": None,
                    "limit_hour": None, "limit_day": None, "zona": None,
                    "tag": None, "pagina": None, "riga": 2},
               ]}
    return [
        {"stations": [station]},
        {"state_on": None, "state_off": None, "riga": 1},
        {"state_on": "On", "state_off": "Off", "riga": 2},
        {"rows": [
            {"description": "CO", "modbus_register": 40001, "bit": None,
             "riga": 1},
            {"description": "Allarme", "modbus_register": 33, "bit": 0,
             "riga": 2},
        ]},
    ]


def test_canvas_model_righe_stati_sciolte_si_agganciano():
    blocks = _sma1_bare_states_blocks()
    single = run_script(DOCUMENTED, blocks)
    canvas = run_script_canvas_model(CANVAS, blocks)
    assert canvas.pop("tb", None) is None
    assert single.pop("tb", None) is None
    assert canvas == single
    assert "status" not in canvas
    by_desc = {v["description"]: v
               for s in canvas["stations"] for v in s["variables"]}
    assert by_desc["Allarme"]["bit"] == 0
    assert by_desc["Allarme"]["state_on"] == "On"
    assert by_desc["Allarme"]["state_off"] == "Off"
    assert by_desc["CO"]["state_on"] is None


def _shift_blocks():
    station = {"name": None, "protocol": "ModBus TCP", "ip": "10.0.0.1",
               "port": 502, "modbus_id": None, "variables": [
                   {"description": "FAULT PC SME", "units": None,
                    "modbus_register": 40011, "bit": 0,
                    "data_type": None, "kind": "DIGITALE_IMPACCATO",
                    "read_write": "R", "state_on": None, "state_off": None,
                    "scale_elec_start": None, "scale_elec_end": None,
                    "scale_eng_start": None, "scale_eng_end": None,
                    "limit_hour": None, "limit_day": None, "zona": None,
                    "tag": None, "pagina": None, "riga": 1},
               ]}
    return [{"stations": [station]},
            {"rows": [{"description": "WATCH_DOG Server 02",
                       "modbus_register": 40010, "bit": None, "riga": 1}]}]


def test_canvas_shift_tiene_misure_e_avvisa_forte():
    blocks = _shift_blocks()
    single = run_script(DOCUMENTED, blocks)
    canvas = run_script_canvas_model(CANVAS, blocks)
    assert canvas.pop("tb", None) is None
    assert single.pop("tb", None) is None
    assert canvas == single
    var = canvas["stations"][0]["variables"][0]
    assert var["description"] == "FAULT PC SME"
    assert var["modbus_register"] == 40011
    assert var["bit"] == 0
    rules = [w["rule"] for w in canvas["warnings"]]
    assert "bit_register_mismatch" in rules
    assert "descrizione_mismatch" in rules
    assert "riga_disallineata" in rules


def test_canvas_busta_vuota_non_azzera_bitnames():
    station = {"name": None, "protocol": "ModBus TCP", "ip": "10.0.0.1",
               "port": 502, "modbus_id": None, "variables": [
                   {"description": "A", "units": None,
                    "modbus_register": 40001, "bit": None,
                    "data_type": None, "kind": "ANALOGICA",
                    "read_write": "R", "state_on": None, "state_off": None,
                    "scale_elec_start": None, "scale_elec_end": None,
                    "scale_eng_start": None, "scale_eng_end": None,
                    "limit_hour": None, "limit_day": None, "zona": None,
                    "tag": None, "pagina": None, "riga": 1},
               ]}
    blocks = [{"stations": [station]},
              {"rows": [{"description": "A", "modbus_register": 40001,
                         "bit": None, "riga": 1}]},
              {"rows": []}]
    single = run_script(DOCUMENTED, blocks)
    canvas = run_script_canvas_model(CANVAS, blocks)
    assert canvas.pop("tb", None) is None
    assert single.pop("tb", None) is None
    assert canvas == single
    var = canvas["stations"][0]["variables"][0]
    assert var["modbus_register"] == 40001
    rules = [w["rule"] for w in canvas["warnings"]]
    assert "riga_mismatch" not in rules
