"""Igiene canvas Single PDF: copie incollabili sotto budget e standalone (Task 8).

Le copie canvas in myhydra/single_pdf/platforms/ sono cio' che si incolla
nei nodi MyHydra: devono restare sotto il budget di paste (28 KB, sotto la
soglia critica dei ~32 KB osservata sul canvas), senza def/class/lambda,
con ERROR JSON mai blank dove il contratto lo prevede e con le guardie
(copertura + linkage) attive nella copia incollata, non solo in src/.
"""

import ast
import io
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).parent.parent
PLATFORMS = REPO / "myhydra" / "single_pdf" / "platforms"
STORE_PYTOOLS = REPO / "myhydra" / "single_pdf" / "pytools"
STORE_PROMPTS = REPO / "src" / "prompts"
NODES = REPO / "myhydra" / "single_pdf" / "nodes"

CONSOLIDATOR_CANVAS = (PLATFORMS / "lv1" / "scripts"
                       / "updated_pending_validation"
                       / "consolidator_canvas.py")
CREATOR_CANVAS = (PLATFORMS / "lv1" / "scripts"
                  / "updated_pending_validation"
                  / "json_creator_v15_canvas.py")
CANVAS_COPIES = [CONSOLIDATOR_CANVAS, CREATOR_CANVAS]


def test_canvas_copies_sotto_budget_e_standalone():
    sizes = {}
    for path in CANVAS_COPIES:
        sizes[path.name] = path.stat().st_size
    max_size = max(sizes.values())
    assert max_size < 28 * 1024


def test_canvas_copies_byte_identical_to_store():
    assert (CONSOLIDATOR_CANVAS.read_bytes()
            == (STORE_PYTOOLS / "consolidator_canvas.py").read_bytes())
    assert (CREATOR_CANVAS.read_bytes()
            == (STORE_PYTOOLS / "json_creator_v15_canvas.py").read_bytes())


def test_canvas_senza_def_class_lambda():
    for path in CANVAS_COPIES:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        kinds = tuple(ast.walk(tree))
        assert not any(isinstance(n, ast.FunctionDef) for n in kinds), path
        assert not any(isinstance(n, ast.AsyncFunctionDef) for n in kinds), \
            path
        assert not any(isinstance(n, ast.ClassDef) for n in kinds), path
        assert not any(isinstance(n, ast.Lambda) for n in kinds), path


def test_canvas_edge_placeholders():
    consolidator = CONSOLIDATOR_CANVAS.read_text(encoding="utf-8")
    creator = CREATOR_CANVAS.read_text(encoding="utf-8")
    assert "{edge}[5]" in consolidator
    assert "{edge}[4]" in creator


def run_consolidator_canvas(raw_value):
    source = CONSOLIDATOR_CANVAS.read_text(encoding="utf-8")
    patched = re.sub(r"raw\s*=\s*r?'''\{edge\}\[\d+\]'''",
                     "raw = __INJECTED_RAW__", source)
    assert patched != source
    ns = {"__INJECTED_RAW__": raw_value}
    exec(compile(patched, str(CONSOLIDATOR_CANVAS), "exec"), ns)
    return json.loads(ns["result"])


def test_consolidator_error_json_mai_blank():
    for garbage in (42, {"pagina": "senza page_no ne stations"}):
        out = run_consolidator_canvas(garbage)
        assert out["status"] == "ERROR"
        assert out["error"] != ""
    ok = run_consolidator_canvas([{"page_no": 1, "stations": []}])
    assert ok["stations"] == []
    assert "status" not in ok


def test_contratto_io_print_vs_result():
    consolidator = CONSOLIDATOR_CANVAS.read_text(encoding="utf-8")
    creator = CREATOR_CANVAS.read_text(encoding="utf-8")
    assert "result =" in consolidator
    assert "print(" not in consolidator
    assert "print(output)" in creator
    assert "result =" not in creator


def run_creator_canvas(raw_value):
    source = CREATOR_CANVAS.read_text(encoding="utf-8")
    patched = re.sub(r"raw\s*=\s*r?'''\{edge\}\[\d+\]'''",
                     "raw = __INJECTED_RAW__", source)
    assert patched != source
    ns = {"__INJECTED_RAW__": raw_value}
    old_stdout = sys.stdout
    sys.stdout = buf = io.StringIO()
    try:
        exec(compile(patched, str(CREATOR_CANVAS), "exec"), ns)
    finally:
        sys.stdout = old_stdout
    printed = buf.getvalue().strip()
    if printed:
        return json.loads(printed)
    return json.loads(ns.get("output", "null"))


class _Unserializable:
    def __str__(self):
        raise RuntimeError("boom-canvas")

    __repr__ = __str__


def test_creator_error_json_mai_blank():
    out = run_creator_canvas(_Unserializable())
    assert out["status"] == "ERROR"
    assert out["error"] != ""
    ok = run_creator_canvas([{"stations": [_station(
        "A", "10.0.0.1", [_analogica("M", 40001)])]}])
    assert isinstance(ok, list)
    assert "status" not in ok[0]


def _analogica(desc, reg):
    return {"description": desc, "units": None, "modbus_register": reg,
            "bit": None, "data_type": None, "kind": "ANALOGICA",
            "read_write": "R", "state_on": None, "state_off": None,
            "scale_elec_start": None, "scale_elec_end": None,
            "scale_eng_start": None, "scale_eng_end": None,
            "limit_hour": None, "limit_day": None}


def _station(name, ip, variables):
    return {"name": name, "protocol": "ModBus TCP", "ip": ip, "port": 502,
            "modbus_id": 1, "variables": variables}


def _warnings_of(out):
    found = []
    for station in out:
        found.extend(station.get("_warnings", []))
    return found


def test_guardia_copertura_attiva_nella_copia_canvas():
    big = [_analogica("Misura " + str(i), 40001 + i) for i in range(60)]
    chunk = {"stations": [_station("A", "10.0.0.1", list(big)),
                          _station("B", "10.0.0.2", list(big))]}
    out = run_creator_canvas([chunk])
    assert any("COPERTURA SOSPETTA" in w for w in _warnings_of(out))
    small = [_analogica("Misura " + str(i), 40001 + i) for i in range(5)]
    out = run_creator_canvas([{"stations": [_station("A", "10.0.0.1",
                                                     list(small))]}])
    assert not any("COPERTURA SOSPETTA" in w for w in _warnings_of(out))


def test_guardia_linkage_presente_nella_copia_canvas():
    source = CREATOR_CANVAS.read_text(encoding="utf-8")
    assert "BITINFO NON COLLEGATI" in source


def test_prompts_current_byte_identical_to_src():
    current = PLATFORMS / "lv2" / "prompts" / "current"
    history = PLATFORMS / "lv2" / "prompts" / "history"
    for name in ("vlm_measures_v14.md", "vlm_bitnames_v14.md",
                 "vlm_bitstates_v15.md"):
        assert ((current / name).read_bytes()
                == (STORE_PROMPTS / name).read_bytes()), name
    assert ((history / "vlm_extraction_v13.md").read_bytes()
            == (STORE_PROMPTS / "vlm_extraction_v13.md").read_bytes())


def test_v15_hashes_nel_readme_pytools():
    readme = (STORE_PYTOOLS / "README.md").read_text(encoding="utf-8")
    assert "json_creator_v15.py" in readme
    assert "json_creator_v15_canvas.py" in readme
    assert "400a6e0484e8227ca9a19ee9841ca7ba31cee2fba9f04e606e0d5befeb168afa" \
        in readme
    assert "afd8ad23d171d33c631307be6f95b1c1ebb588406f912cd9ffb17a565a39479a" \
        in readme


def test_platforms_layout():
    assert (PLATFORMS / "README.md").is_file()
    assert (PLATFORMS / "lv1" / "README.md").is_file()
    assert (PLATFORMS / "lv2" / "README.md").is_file()
    assert (PLATFORMS / "lv1" / "scripts" / "in_use" / "README.md").is_file()
    assert (PLATFORMS / "lv1" / "scripts" / "updated_pending_validation"
            / "README.md").is_file()
    assert (PLATFORMS / "lv1" / "scripts" / "parked" / "README.md").is_file()
    assert (PLATFORMS / "lv2" / "prompts" / "current" / "README.md").is_file()
    assert (PLATFORMS / "lv2" / "prompts" / "history" / "README.md").is_file()


def test_checklist_edge_settings_nei_nodi_e_nel_readme():
    consolidator_card = (NODES / "lv1_04_consolidatore.md").read_text(
        encoding="utf-8")
    assert "{edge}[5]" in consolidator_card
    creator_card = (NODES / "lv1_05_json_creator.md").read_text(
        encoding="utf-8")
    assert "{edge}[4]" in creator_card
    flow_readme = (PLATFORMS / "README.md").read_text(encoding="utf-8")
    assert "pippo" in flow_readme
    assert "match" in flow_readme.lower()
