"""JSON CREATOR Single slim v15: V19 wins over P5 + canvas parity.

Reference: src/nodes/json_creator.py. Documented snapshot:
myhydra/single_pdf/pytools/json_creator_v15.py. Canvas copy:
myhydra/single_pdf/pytools/json_creator_v15_canvas.py (23.595 byte, sotto la
guardia di paste di 33.792, comment lines stripped, same AST and same output).
"""
import ast
import io
import json
import os
import re
import struct
import sys
from pathlib import Path

REPO = Path(__file__).parent.parent
SRC = REPO / "src" / "nodes" / "json_creator.py"
DOCUMENTED = REPO / "myhydra" / "single_pdf" / "pytools" / "json_creator_v15.py"
CANVAS = REPO / "myhydra" / "single_pdf" / "pytools" / "json_creator_v15_canvas.py"

CANVAS_MAX_BYTES = 28 * 1024
NAME_MAX = 49
BIG = 3.40282e38


def run_script(path, raw_value):
    source = Path(path).read_text(encoding="utf-8")
    patched = re.sub(r"raw\s*=\s*r?'''\{edge\}\[\d+\]'''",
                     "raw = __INJECTED_RAW__", source)
    assert patched != source
    ns = {"__INJECTED_RAW__": raw_value}
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        exec(compile(patched, str(path), "exec"), ns)
    finally:
        sys.stdout = old_stdout
    return json.loads(ns.get("output", "null"))


def variable(desc, reg, kind="ANALOGICA", extra=None):
    v = {
        "description": desc, "units": None,
        "modbus_register": reg, "bit": None,
        "data_type": None, "kind": kind, "read_write": "R",
        "state_on": None, "state_off": None,
        "scale_elec_start": None, "scale_elec_end": None,
        "scale_eng_start": None, "scale_eng_end": None,
        "limit_hour": None, "limit_day": None,
    }
    v.update(extra or {})
    return v


def chunk(variables):
    return {"stations": [{
        "name": "S", "protocol": "ModBus TCP", "ip": "10.0.0.1",
        "port": 502, "modbus_id": 1, "variables": variables,
    }]}


def creator_name(desc, **kw):
    out = run_script(SRC, chunk([variable(desc, 40001, extra=kw)]))
    return out[0]["measures"][0]["NAME"]


def fmt_of(desc, data_type):
    out = run_script(
        SRC, chunk([variable(desc, 40001,
                             extra={"data_type": data_type})]))
    dp = out[0]["measures"][0]["DRIVERPRIVATE"]
    return struct.unpack("<I", bytes.fromhex(dp[2 + 40:2 + 48]))[0]


def test_parentesi_con_contenuto_conservate_e_formato_da_datatype():
    assert creator_name("(GR)") == "(GR)"
    assert creator_name("Polveri (GR)") == "Polveri (GR)"
    assert creator_name("Foo ()") == "Foo"
    assert creator_name("Foo ( ) Bar") == "Foo Bar"
    assert fmt_of("A", "INT16") == 150
    assert fmt_of("A", "INT") == 150
    assert fmt_of("A", "UINT16") == 150
    assert fmt_of("A", "Uint") == 150
    assert fmt_of("A", "UINT") == 150
    assert fmt_of("A", "REAL32") == 250
    assert fmt_of("A", None) == 250


def test_driverprivate_48_hex():
    out = run_script(SRC, chunk([
        variable("Analogica", 40001),
        variable("Singolo", 40010, kind="DIGITALE_SINGOLO",
                 extra={"bit": 0}),
        variable("Bit A", 40020, kind="DIGITALE_IMPACCATO",
                 extra={"bit": 0}),
        variable("Bit B", 40020, kind="DIGITALE_IMPACCATO",
                 extra={"bit": 1}),
    ]))
    assert len(out[0]["measures"]) == 3
    for m in out[0]["measures"]:
        assert re.fullmatch(r"0x[0-9A-F]{48}", m["DRIVERPRIVATE"]), \
            m["DRIVERPRIVATE"]


def test_name_troncato_a_49_caratteri():
    assert creator_name("Y" * 49) == "Y" * 49
    assert creator_name("X" * 60) == "X" * 49
    assert len(creator_name("X" * 60)) == 49


def test_sentinel_senza_scala_e_fondo_scala_dichiarato():
    out = run_script(SRC, chunk([variable("CO", 17)]))
    m = out[0]["measures"][0]
    assert (m["LOWRANGE"], m["HIGHRANGE"]) == (-BIG, BIG)
    out = run_script(SRC, chunk([variable(
        "CO", 17, extra={"scale_eng_start": 0, "scale_eng_end": 200})]))
    m = out[0]["measures"][0]
    assert (m["LOWRANGE"], m["HIGHRANGE"]) == (0, 200)


def test_stati_keyword_solo_se_null():
    out = run_script(SRC, chunk([variable(
        "Valvola V1", 40010, kind="DIGITALE_SINGOLO",
        extra={"bit": 0, "state_on": "APERTA",
               "state_off": "CHIUSA"})]))
    b = out[0]["bitinfo"][0]
    assert (b["TEXTON"], b["TEXTOFF"]) == ("APERTA", "CHIUSA")
    out = run_script(SRC, chunk([variable(
        "Allarme sonda", 40020, kind="DIGITALE_IMPACCATO",
        extra={"bit": 3})]))
    b = out[0]["bitinfo"][0]
    assert (b["TEXTON"], b["TEXTOFF"]) == ("ALLARME", "OFF")
    out = run_script(SRC, chunk([variable(
        "Temperatura", 40001, kind="DIGITALE_SINGOLO",
        extra={"bit": None})]))
    b = out[0]["bitinfo"][0]
    assert (b["TEXTON"], b["TEXTOFF"]) == ("ATTIVO", "OFF")


def test_packed_omonimi_bit_diversi_entrambi_in_bitinfo():
    out = run_script(SRC, chunk([
        variable("OVF Misura IW36", 40007, kind="DIGITALE_IMPACCATO",
                 extra={"bit": 2}),
        variable("OVF Misura IW38", 40007, kind="DIGITALE_IMPACCATO",
                 extra={"bit": 3}),
        variable("OVF Misura IW36", 40007, kind="DIGITALE_IMPACCATO",
                 extra={"bit": 10}),
        variable("OVF Misura IW38", 40007, kind="DIGITALE_IMPACCATO",
                 extra={"bit": 11}),
    ]))
    bits = sorted(b["BITNO"] for b in out[0]["bitinfo"])
    assert bits == [2, 3, 10, 11]


def test_packed_duplicato_esatto_resta_dedup():
    out = run_script(SRC, chunk([
        variable("OVF Misura IW36", 40007, kind="DIGITALE_IMPACCATO",
                 extra={"bit": 2}),
        variable("OVF Misura IW36", 40007, kind="DIGITALE_IMPACCATO",
                 extra={"bit": 2}),
    ]))
    assert len(out[0]["bitinfo"]) == 1


def test_linkage_bitinfo_misure_e_meta():
    out = run_script(SRC, chunk([
        variable("Analogica", 40001),
        variable("Bit A", 40020, kind="DIGITALE_IMPACCATO",
                 extra={"bit": 0}),
        variable("Bit B", 40020, kind="DIGITALE_IMPACCATO",
                 extra={"bit": 1}),
        variable("Singolo", 40010, kind="DIGITALE_SINGOLO",
                 extra={"bit": 0}),
    ]))
    st = out[0]
    assert "_meta" in st
    ids = {m["ID"] for m in st["measures"]}
    for b in st["bitinfo"]:
        assert b["MEASUREID"] in ids, b
    covered = {b["MEASUREID"] for b in st["bitinfo"]}
    for m in st["measures"]:
        if m["DRIVERDATA"] == 2:
            assert m["ID"] in covered, m["NAME"]
    for w in st.get("_warnings", []):
        assert "BITINFO NON COLLEGATI" not in w, w


def parity_fixture():
    return chunk([
        variable("Polveri (GR)", 40001, extra={"units": "mg/Nm3"}),
        variable("Vuota () coda", 40002),
        variable('"Quotata"', 40003),
        variable("X" * 60, 40004),
        variable("Bit A", 40020, kind="DIGITALE_IMPACCATO",
                 extra={"bit": 0}),
        variable("Bit B", 40020, kind="DIGITALE_IMPACCATO",
                 extra={"bit": 1}),
        variable("Comando", 40100, kind="DIGITALE_SINGOLO",
                 extra={"bit": 0, "read_write": "W"}),
    ])


def test_documented_identico_a_src():
    assert DOCUMENTED.read_bytes() == SRC.read_bytes()


def test_canvas_sotto_soglia_dimensionale():
    assert os.path.getsize(CANVAS) <= CANVAS_MAX_BYTES


def test_canvas_stesso_ast_del_documentato():
    assert (ast.dump(ast.parse(DOCUMENTED.read_text(encoding="utf-8")))
            == ast.dump(ast.parse(CANVAS.read_text(encoding="utf-8"))))


def test_canvas_stesso_output_del_documentato_e_src():
    pages = parity_fixture()
    a = run_script(DOCUMENTED, pages)
    b = run_script(CANVAS, pages)
    c = run_script(SRC, pages)
    assert a == b == c
    names = [m["NAME"] for m in a[0]["measures"]]
    assert "Polveri (GR)" in names
    assert ("X" * 49) in names


def test_canvas_senza_def_lambda_class():
    tree = ast.parse(CANVAS.read_text(encoding="utf-8"))
    kinds = tuple(ast.walk(tree))
    assert not any(isinstance(n, ast.FunctionDef) for n in kinds)
    assert not any(isinstance(n, ast.AsyncFunctionDef) for n in kinds)
    assert not any(isinstance(n, ast.ClassDef) for n in kinds)
    assert not any(isinstance(n, ast.Lambda) for n in kinds)


def test_keyword_ovf_da_errore():
    out = run_script(SRC, chunk([variable(
        "OVF COT_01", 40007, kind="DIGITALE_IMPACCATO",
        extra={"bit": 0})]))
    b = out[0]["bitinfo"][0]
    assert (b["TEXTON"], b["TEXTOFF"]) == ("ERRORE", "OFF")


def test_stato_junk_parentetico_va_in_fallback_keyword():
    out = run_script(SRC, chunk([variable(
        "Allarme Pompa M1 (1= RUNNING)", 40001, kind="DIGITALE_IMPACCATO",
        extra={"bit": 8, "state_on": "1= RUNNING"})]))
    b = out[0]["bitinfo"][0]
    assert (b["TEXTON"], b["TEXTOFF"]) == ("ALLARME", "OFF")


def test_stato_solo_uguale_isolato_va_in_fallback():
    out = run_script(SRC, chunk([variable(
        "Contatore impulsi", 40010, kind="DIGITALE_IMPACCATO",
        extra={"bit": 3, "state_on": "1 ="})]))
    b = out[0]["bitinfo"][0]
    assert (b["TEXTON"], b["TEXTOFF"]) == ("ATTIVO", "OFF")
