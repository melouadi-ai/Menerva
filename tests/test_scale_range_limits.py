"""v4.5 di json_creator: fondo scala -> LOWRANGE/HIGHRANGE, limiti e divisori
solo in review (decisione 6/10/2026, mapping BISON col cliente)."""
import io
import json
import os
import re
import sys

SCRIPT_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "src", "nodes", "json_creator.py")
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


def warnings_of(out):
    return out[0].get("_warnings", [])


def test_fondo_scala_in_lowrange_highrange():
    out = run_script(chunk([variable("CO", 17, {"scale_eng_start": 0, "scale_eng_end": 200})]))
    m = out[0]["measures"][0]
    assert (m["LOWRANGE"], m["HIGHRANGE"]) == (0, 200)
    assert warnings_of(out) == []


def test_senza_scala_sentinel_e_silenzio():
    out = run_script(chunk([variable("CO", 17)]))
    m = out[0]["measures"][0]
    assert (m["LOWRANGE"], m["HIGHRANGE"]) == (-3.40282e38, 3.40282e38)
    assert warnings_of(out) == []


def test_limiti_in_review_senza_cambiare_valori():
    out = run_script(
        chunk([variable("CO", 17, {"limit_day": 40, "limit_hour": 50})])
    )
    m = out[0]["measures"][0]
    assert (m["LOWCRITICAL"], m["HIGHCRITICAL"]) == (-3.40282e38, 3.40282e38)
    w = warnings_of(out)
    assert len(w) == 1 and "LIMITI DICHIARATI NON APPLICATI IN ADAS" in w[0]
    assert "CO" in w[0] and "40" in w[0] and "50" in w[0]


def test_divisione_in_review():
    out = run_script(
        chunk(
            [
                variable(
                    "Temperatura urea",
                    33,
                    {"Division": True, "Division_value": 10},
                )
            ]
        )
    )
    w = warnings_of(out)
    assert len(w) == 1 and "DIVISIONE NON APPLICATA IN ADAS" in w[0]
    assert "Temperatura urea" in w[0] and "x10" in w[0]
