"""Offset 40000 sui registri Double (decisione sistema 12/10/2026).

Gli IOL Double scrivono il REG corto (1, 17, 417); il registro Modbus reale
e' 40000 + REG (1 -> 40001, come i PDF Single che scrivono gia' 40001).
Il test esegue la **copia canvas** (l'artefatto che va sul nodo 12), non il
documentato: la parita' AST tra i due e' coperta da
test_json_creator_edge13_canvas.py.
"""
import io
import json
import os
import re
import struct
import sys

SCRIPT_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "platforms",
        "lv1",
        "scripts",
        "in_use",
        "json_creator_edge13_canvas.py",
    )
)


def run_script(raw_value):
    with open(SCRIPT_PATH, encoding="utf-8") as f:
        source = f.read()
    src2 = re.sub(r"raw\s*=\s*r?'''\{edge\}\[\d+\]'''", "raw = __INJECTED_RAW__", source)
    ns = {"__INJECTED_RAW__": raw_value}
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        exec(compile(src2, SCRIPT_PATH, "exec"), ns)
    finally:
        sys.stdout = old_stdout
    return json.loads(ns.get("output", "null"))


def variable(name, reg, extra=None):
    v = {
        "description": name,
        "units": None,
        "modbus_register": reg,
        "bit": None,
        "data_type": None,
        "kind": "ANALOGICA",
        "read_write": "R",
        "state_on": None,
        "state_off": None,
        "scale_elec_start": None,
        "scale_elec_end": None,
        "scale_eng_start": None,
        "scale_eng_end": None,
        "limit_hour": None,
        "limit_day": None,
    }
    v.update(extra or {})
    return v


def chunk(variables):
    return {
        "stations": [
            {
                "name": "S",
                "protocol": "ModBus TCP",
                "ip": "10.0.0.1",
                "port": 502,
                "modbus_id": None,
                "variables": variables,
            }
        ]
    }


def reg_of(measure):
    return struct.unpack("<I", bytes.fromhex(measure["DRIVERPRIVATE"][2:10]))[0]


def test_registro_corto_diventa_40000_piu_reg():
    out = run_script(chunk([variable("CO", 17), variable("Ingressi digitali 1", 1, {"kind": "DIGITALE_IMPACCATO", "bit": 8})]))
    regs = sorted(reg_of(m) for m in out[0]["measures"])
    assert regs == [40001, 40017]


def test_senza_registro_resta_scartato_prima_della_somma():
    """La somma non deve resuscitare le righe senza indirizzo: lo scarto
    (None/blank) avviene prima, sul valore grezzo."""
    out = run_script(chunk([variable("Derivata", None), variable("CO", 17)]))
    assert [reg_of(m) for m in out[0]["measures"]] == [40017]
    warn = " ".join(out[0].get("_warnings", []))
    assert "VARIABILI SENZA INDIRIZZO" in warn


def test_limiti_orario_e_giornaliero_applicati_a_sq_means():
    """limit_hour va in SQ1HOURMEAN e limit_day va in SQDAILYMEAN come float."""
    out = run_script(chunk([
        variable("CO", 17, {"limit_hour": 50, "limit_day": 40}),
        variable("NO", 18, {"limit_hour": "37,5", "limit_day": "30.0"}),
        variable("TF", 25, {"limit_hour": None, "limit_day": None}),
    ]))
    by_name = {m["NAME"]: m for m in out[0]["measures"]}
    assert by_name["CO"]["SQ1HOURMEAN"] == 50.0
    assert by_name["CO"]["SQDAILYMEAN"] == 40.0
    assert by_name["NO"]["SQ1HOURMEAN"] == 37.5
    assert by_name["NO"]["SQDAILYMEAN"] == 30.0
    assert by_name["TF"]["SQ1HOURMEAN"] == 3.40282e+38
    assert by_name["TF"]["SQDAILYMEAN"] == 3.40282e+38
    warn = " ".join(out[0].get("_warnings", []))
    assert "LIMITI DICHIARATI APPLICATI IN ADAS" in warn


def test_limite_non_numerico_non_dichiara_applicato():
    """Difetto latente trovato il 29/10: con un limite non numerico
    ("<= 60", "60 mg/Nm3") la conversione fallisce e SQ resta sentinel, ma
    il warning diceva comunque "APPLICATI". Ora la misura finisce in
    LIMITI NON NUMERICI NON APPLICATI."""
    out = run_script(chunk([
        variable("CO", 17, {"limit_hour": "<= 60", "limit_day": "60 mg/Nm3"}),
    ]))
    m = out[0]["measures"][0]
    assert m["SQ1HOURMEAN"] == 3.40282e+38
    assert m["SQDAILYMEAN"] == 3.40282e+38
    warn = " ".join(out[0].get("_warnings", []))
    assert "LIMITI DICHIARATI APPLICATI" not in warn
    assert "LIMITI NON NUMERICI NON APPLICATI" in warn
    assert "CO (giornaliero=60 mg/Nm3, orario=<= 60)" in warn


def test_limite_parziale_applica_solo_il_numerico():
    """Un limite numerico e uno no: il numerico va in SQ, l'altro resta
    sentinel, e il warning "applicati" (almeno uno) compare."""
    out = run_script(chunk([
        variable("NO", 18, {"limit_hour": 125, "limit_day": "n.d."}),
    ]))
    m = out[0]["measures"][0]
    assert m["SQ1HOURMEAN"] == 125.0
    assert m["SQDAILYMEAN"] == 3.40282e+38
    warn = " ".join(out[0].get("_warnings", []))
    assert "LIMITI DICHIARATI APPLICATI IN ADAS" in warn

