"""Pagina con N.Bit contato 1-based nel ramo nomi-bit (SIEMENS_2 p4).

Il ramo nomi legge la colonna N.Bit come 1..16 mentre il ramo misure emette
0..15: ogni bit della pagina e' uno troppo alto e il bit in cima a un
registro (0, o 8) non viene mai emesso. Riga per riga i due rami sembrano
d'accordo, quindi la guardia per-riga non lo vede: serve un controllo di
pagina.

Atteso: bit del ramo misure (giusti) e nome della propria riga.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from nodes.single_consolidator import consolidate


def _var(desc, riga, reg, bit, kind="DIGITALE_IMPACCATO"):
    return {"description": desc, "units": None, "modbus_register": reg,
            "bit": bit, "data_type": "INT16", "kind": kind,
            "read_write": "R", "state_on": None, "state_off": None,
            "scale_elec_start": None, "scale_elec_end": None,
            "scale_eng_start": None, "scale_eng_end": None,
            "limit_hour": None, "limit_day": None,
            "zona": "ALLARMI", "tag": None, "pagina": 4, "riga": riga}


def _name(desc, riga, reg, bit):
    return {"description": desc, "modbus_register": reg, "bit": bit,
            "riga": riga}


def _page(vars_, names):
    return {"page_no": 4,
            "stations": [{"name": None, "protocol": "ModBus TCP",
                          "ip": "192.168.2.11", "port": 502,
                          "modbus_id": None, "variables": vars_}],
            "bitnames": {"rows": names}}


def _bits(out):
    return {v["riga"]: v["bit"] for v in out["stations"][0]["variables"]}


def _rules(out):
    return [w["rule"] for w in out["warnings"]]


def test_pagina_1based_riporta_i_bit_a_zero():
    """40011 nel PDF: bit 1,2,7,8; 40012: bit 9,10 (il ramo nomi scrive
    2,3,8,9 e 10,11, e il 16 della riga 15 e' il bit 15 del PDF)."""
    out = consolidate([_page(
        [_var("FAULT PC SME", 13, 40011, 1),
         _var("FAULT DCS", 14, 40011, 2),
         _var("ANALOG Output DCS ForzatI", 19, 40011, 7),
         _var("SELETTORE MANUTENZIONE GENERALE", 20, 40011, 8),
         _var("COG2 TEMPERATURA LINEA", 27, 40012, 9),
         _var("COG3 TEMPERATURA FUMI", 29, 40012, 15)],
        [_name("FAULT PC SME", 13, 40011, 2),
         _name("FAULT DCS", 14, 40011, 3),
         _name("ANALOG Output DCS Forzati", 19, 40011, 8),
         _name("SELETTORE MANUTENZIONE GENERALE", 20, 40011, 9),
         _name("COG2 TEMPERATURA LINEA", 27, 40012, 10),
         _name("COG3 TEMPERATURA FUMI", 29, 40012, 16)])])
    assert _bits(out) == {13: 1, 14: 2, 19: 7, 20: 8, 27: 9, 29: 15}
    assert "bit_offset_pagina" in _rules(out)
    # Il flag interno non deve uscire dal nodo.
    assert not any("_bit_offset_pagina" in v
                   for v in out["stations"][0]["variables"])


def test_nome_resta_quello_della_propria_riga():
    """Con la pagina 1-based il nome non deve migrare alla riga adiacente:
    riga 19 e' ForzatI (PDF), non Forzati (riga sopra)."""
    out = consolidate([_page(
        [_var("ANALOG Output DCS ForzatI", 19, 40011, 7),
         _var("SELETTORE MANUTENZIONE GENERALE", 20, 40011, 8)],
        [_name("ANALOG Output DCS Forzati", 19, 40011, 8),
         _name("SELETTORE MANUTENZIONE GENERALE", 20, 40011, 9)])])
    desc = {v["riga"]: v["description"] for v in out["stations"][0]["variables"]}
    assert desc[19] == "ANALOG Output DCS ForzatI"


def test_pagina_zero_based_non_viene_toccata():
    """Rami d'accordo (bit identici): nessun offset, nessun warning nuovo."""
    out = consolidate([_page(
        [_var("A", 1, 40011, 1), _var("B", 2, 40011, 2),
         _var("C", 3, 40011, 7)],
        [_name("A", 1, 40011, 1), _name("B", 2, 40011, 2),
         _name("C", 3, 40011, 7)])])
    assert _bits(out) == {1: 1, 2: 2, 3: 7}
    assert "bit_offset_pagina" not in _rules(out)


def test_bit_davvero_diversi_non_sono_uno_shift():
    """Rami discordi su bit sparsi (non tutti +1): nessun offset di pagina.
    Con descrizioni concordi resta la regola per-riga (il nome decide il
    bit), come prima della guardia: qui il bit e' quello del nome."""
    out = consolidate([_page(
        [_var("A", 1, 40011, 7), _var("B", 2, 40011, 8)],
        [_name("A", 1, 40011, 3), _name("B", 2, 40011, 12)])])
    assert _bits(out) == {1: 3, 2: 12}
    assert "bit_offset_pagina" not in _rules(out)


def test_pagina_mista_non_scatta():
    """Una sola riga fuori posto non e' una pagina 1-based."""
    out = consolidate([_page(
        [_var("A", 1, 40011, 7), _var("B", 2, 40011, 8),
         _var("C", 3, 40011, 9)],
        [_name("A", 1, 40011, 8), _name("B", 2, 40011, 8),
         _name("C", 3, 40011, 9)])])
    assert "bit_offset_pagina" not in _rules(out)


# --- La regola vale anche nella copia canvas (non solo in src) --------------
import json  # noqa: E402
import sys as _sys  # noqa: E402

_sys.path.insert(0, str(Path(__file__).parent))
from test_single_consolidator_canvas import (  # noqa: E402
    CANVAS, run_script_canvas_model)


def _pagina_siemens():
    return [_page(
        [_var("FAULT PC SME", 13, 40011, 1),
         _var("FAULT DCS", 14, 40011, 2),
         _var("ANALOG Output DCS ForzatI", 19, 40011, 7),
         _var("SELETTORE MANUTENZIONE GENERALE", 20, 40011, 8),
         _var("COG2 TEMPERATURA LINEA", 27, 40012, 9),
         _var("COG3 TEMPERATURA FUMI", 29, 40012, 15)],
        [_name("FAULT PC SME", 13, 40011, 2),
         _name("FAULT DCS", 14, 40011, 3),
         _name("ANALOG Output DCS Forzati", 19, 40011, 8),
         _name("SELETTORE MANUTENZIONE GENERALE", 20, 40011, 9),
         _name("COG2 TEMPERATURA LINEA", 27, 40012, 10),
         _name("COG3 TEMPERATURA FUMI", 29, 40012, 16)])]


def test_canvas_riproduce_la_pagina_1based():
    """MyHydra esegue la copia canvas, non `src`: stesso output, bit a 0."""
    pages = json.loads(json.dumps(_pagina_siemens()))
    ref = consolidate(json.loads(json.dumps(pages)))
    canvas = run_script_canvas_model(CANVAS, pages)
    assert canvas.pop("tb", None) is None
    assert canvas == ref
    assert _bits(canvas) == {13: 1, 14: 2, 19: 7, 20: 8, 27: 9, 29: 15}
    assert "bit_offset_pagina" in _rules(canvas)
    assert not any("_bit_offset_pagina" in v
                   for v in canvas["stations"][0]["variables"])


def test_ancoraggio_non_usa_i_nomi_in_pagina_1based():
    """Se il registro ha un bit fuori scala (16), il gate di ancoraggio
    scatterebbe e riprenderebbe i bit dei nomi (+1): sulla pagina 1-based
    deve tacere, altrimenti rimette lo shift appena tolto."""
    pages = [_page(
        [_var("A", 1, 40011, 0), _var("B", 2, 40011, 1),
         _var("C", 3, 40011, 16)],
        [_name("A", 1, 40011, 1), _name("B", 2, 40011, 2),
         _name("C", 3, 40011, 17)])]
    out = consolidate(json.loads(json.dumps(pages)))
    assert _bits(out) == {1: 0, 2: 1, 3: 15}
    can = run_script_canvas_model(CANVAS, json.loads(json.dumps(pages)))
    can.pop("tb", None)
    assert can == out
