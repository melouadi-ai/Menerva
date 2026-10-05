"""Regression end-to-end caso 6 Double PDF: chunk del CONSOLIDA PRE-JSON
CREATOR (run Qwen 3.8) -> src/nodes/json_creator.py -> ADAS.

Pinna il comportamento verificato contro il PDF IOL.0139.23:
1 stazione, 22 misure, 60 bitinfo, linkage misure-bitinfo intatto
(nessun warning BITINFO NON COLLEGATI), registri Modbus da DRIVERPRIVATE.
"""
import io
import json
import os
import re
import struct
import sys

SCRIPT_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "src", "nodes", "json_creator.py")
)
CHUNK_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "myhydra",
        "double_pdf",
        "tests",
        "case_6",
        "outputs",
        "observed_lv1_consolidator_qwen38_chunk.json",
    )
)


def run_script(raw_value):
    with open(SCRIPT_PATH, encoding="utf-8") as f:
        source = f.read()
    src2 = re.sub(
        r"raw\s*=\s*r?'''\{edge\}\[\d+\]'''", "raw = __INJECTED_RAW__", source
    )
    ns = {"__INJECTED_RAW__": raw_value}
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        exec(compile(src2, SCRIPT_PATH, "exec"), ns)
    finally:
        sys.stdout = old_stdout
    return json.loads(ns.get("output", "null"))


def load_adas():
    with open(CHUNK_PATH, encoding="utf-8") as f:
        chunk = json.load(f)
    out = run_script(chunk)
    assert isinstance(out, list) and len(out) == 1
    return out[0]


def reg_of(measure):
    return struct.unpack("<I", bytes.fromhex(measure["DRIVERPRIVATE"][2:10]))[0]


def test_caso6_una_stazione_con_ip_e_porta():
    st = load_adas()
    assert st["NAME"] == "Sistema Analisi SO2"
    assert 'ipaddress="10.100.50.95"' in st["DRIVERCONFIG"]
    assert 'tcpport="511"' in st["DRIVERCONFIG"]


def test_caso6_conteggi_misure_bitinfo():
    st = load_adas()
    assert len(st["measures"]) == 22
    assert len(st["bitinfo"]) == 60


def test_caso6_nessun_warning_di_linkage():
    st = load_adas()
    for w in st.get("_warnings", []):
        assert "BITINFO NON COLLEGATI" not in w, w


def test_caso6_linkage_bitinfo_misure_intatto():
    st = load_adas()
    ids = {m["ID"] for m in st["measures"]}
    for b in st["bitinfo"]:
        assert b["MEASUREID"] in ids, b
    covered = {b["MEASUREID"] for b in st["bitinfo"]}
    for m in st["measures"]:
        if m["DRIVERDATA"] == 2:
            assert m["ID"] in covered, m["NAME"]


def test_caso6_registri_packed_e_singoli():
    st = load_adas()
    packed_regs = sorted(reg_of(m) for m in st["measures"] if m["DRIVERDATA"] == 2)
    assert packed_regs == [1, 3, 4, 5, 6]
    single_regs = sorted(reg_of(m) for m in st["measures"] if m["DRIVERDATA"] == 5)
    assert single_regs == [417, 418, 419, 425, 426, 427, 431, 432]


def test_caso6_pm302a_bit1_e_texton_presenti():
    st = load_adas()
    by_name = {b["BITNAME"]: b for b in st["bitinfo"]}
    assert by_name["PM-302A IN MARCIA"]["BITNO"] == 1
    assert by_name["PM-310A IN MARCIA"]["BITNO"] == 4
    for b in st["bitinfo"]:
        assert b["TEXTON"], b
        assert b["TEXTOFF"], b
