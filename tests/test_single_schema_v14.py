"""Schema intermedio v14: zona, tag, pagina, riga + description nulla = errore."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from models import safe_validate_vlm


def test_v14_accetta_zona_tag_pagina_riga():
    st = {"name": None, "ip": "192.168.2.11", "port": 5021, "modbus_id": None,
          "variables": [{"description": "COG2: ALLARME FRIGO", "units": None,
                         "modbus_register": 40014, "bit": 11, "kind": "DIGITALE_IMPACCATO",
                         "data_type": "INT16", "read_write": None, "state_on": None,
                         "state_off": None, "scale_eng_start": None, "scale_eng_end": None,
                         "limit_hour": None, "limit_day": None,
                         "zona": "ALLARMI", "tag": None, "pagina": 5, "riga": 12}]}
    res = safe_validate_vlm({"stations": [st]})
    assert res.success


def test_v14_description_null_e_errore():
    st = {"name": None, "ip": "192.168.2.11", "port": 5021, "modbus_id": None,
          "variables": [{"description": None, "units": None,
                         "modbus_register": 40014, "bit": 11, "kind": "DIGITALE_IMPACCATO",
                         "data_type": "INT16", "read_write": None, "state_on": None,
                         "state_off": None, "scale_eng_start": None, "scale_eng_end": None,
                         "limit_hour": None, "limit_day": None,
                         "zona": "ALLARMI", "tag": None, "pagina": 5, "riga": 12}]}
    res = safe_validate_vlm({"stations": [st]})
    assert not res.success
    assert any("description" in e.lower() for e in res.errors)
