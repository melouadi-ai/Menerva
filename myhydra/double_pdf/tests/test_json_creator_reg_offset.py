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
