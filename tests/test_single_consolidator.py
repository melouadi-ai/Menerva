"""Consolidatore Single: join scale per tag, carry-over registro, fold packed."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from nodes.single_consolidator import consolidate


def _var(description, riga, tag=None, reg=None, bit=None, kind="ANALOGICA",
         pagina=None, zona="MISURE", units=None, eng=None, data_type=None,
         state_on=None, state_off=None, **extra):
    v = {"description": description, "units": units, "modbus_register": reg,
         "bit": bit, "data_type": data_type, "kind": kind, "read_write": "R",
         "state_on": state_on, "state_off": state_off,
         "scale_elec_start": None, "scale_elec_end": None,
         "scale_eng_start": eng[0] if eng else None,
         "scale_eng_end": eng[1] if eng else None,
         "limit_hour": None, "limit_day": None,
         "zona": zona, "tag": tag, "pagina": pagina, "riga": riga}
    v.update(extra)
    return v


def _station(ip, variables, name=None):
    return {"name": name, "protocol": "ModBus TCP", "ip": ip, "port": 502,
            "modbus_id": None, "variables": variables}


def page_con_tag_scala():
    return {"page_no": 1, "stations": [_station("192.168.2.11", [
        _var("SO2", 1, tag="SO2", reg=49, data_type="INT"),
        _var("SO2 fondo scala", 2, tag="SO2", reg=50, eng=(0, 300)),
    ])]}


def page_misura_senza_registro():
    return {"page_no": 2, "stations": [_station("192.168.2.11", [
        _var("Allarme sonda", 1, reg=None, bit=8,
             kind="DIGITALE_IMPACCATO"),
    ])]}


def test_join_scale_per_tag_e_carry_over():
    out = consolidate([page_con_tag_scala(), page_misura_senza_registro()])
    assert out["warnings"] != []


def test_scala_collegata_per_tag_e_registro_applicato_tracciato():
    out = consolidate([page_con_tag_scala(), page_misura_senza_registro()])
    by_desc = {v["description"]: v
               for s in out["stations"] for v in s["variables"]}
    assert by_desc["SO2"]["scale_eng_start"] == 0
    assert by_desc["SO2"]["scale_eng_end"] == 300
    assert by_desc["Allarme sonda"]["modbus_register"] == 50
    rules = [w["rule"] for w in out["warnings"]]
    assert "registro_applicato" in rules
    assert out["counters"]["registri_applicati"] == 1
    assert out["counters"]["scale_collegate"] >= 1


def test_mismatch_riga_sempre_avvisato():
    page = {"page_no": 1, "stations": [_station("10.0.0.1", [
        _var("A", 1, reg=40001), _var("B", 2, reg=40002),
    ])], "bitnames": {"rows": [
        {"description": "A", "modbus_register": 40001, "bit": None,
         "riga": 1},
        {"description": "B", "modbus_register": 40002, "bit": None,
         "riga": 2},
        {"description": "C", "modbus_register": 40003, "bit": None,
         "riga": 3},
    ]}}
    out = consolidate([page])
    rules = [w["rule"] for w in out["warnings"]]
    assert "riga_mismatch" in rules
    descs = [v["description"] for s in out["stations"]
             for v in s["variables"]]
    assert "C" not in descs


def test_precedenza_nomi_bit_per_bit_e_registro():
    page = {"page_no": 1, "stations": [_station("10.0.0.1", [
        _var("Allarme", 1, reg=40014, bit=3,
             kind="DIGITALE_IMPACCATO"),
    ])], "bitnames": {"rows": [
        {"description": "Allarme", "modbus_register": 40015, "bit": 5,
         "riga": 1},
    ]}}
    out = consolidate([page])
    var = out["stations"][0]["variables"][0]
    assert var["modbus_register"] == 40015
    assert var["bit"] == 5
    rules = [w["rule"] for w in out["warnings"]]
    assert "bit_register_mismatch" in rules


def test_scarti_v2_v20_v21_contati_con_motivo():
    page = {"page_no": 1, "stations": [_station("10.0.0.1", [
        _var("COG2: ALLARME FRIGO", 1, reg=40014, bit=11,
             kind="DIGITALE_IMPACCATO", zona="ALLARMI"),
        _var("Riserva", 2, reg=40015, zona="ALLARMI"),
        _var("Sonda", 3, reg=40016, zona="INPUT_HW"),
        _var("Pompa", 4, reg=40017, zona="CAMPO",
             note="NO PC SME"),
    ])]}
    out = consolidate([page])
    descs = [v["description"] for s in out["stations"]
             for v in s["variables"]]
    assert descs == ["COG2: ALLARME FRIGO"]
    assert out["counters"]["scarti_V2"] == 1
    assert out["counters"]["scarti_V21"] == 1
    assert out["counters"]["scarti_V20"] == 1
    scarti = [w for w in out["warnings"]
              if w["rule"].startswith("scarto_")]
    assert len(scarti) == 3


def test_lettura_canonica_description_come_classify_row():
    page = {"page_no": 1, "stations": [_station("10.0.0.1", [
        {"Description": "COG2: ALLARME FRIGO", "modbus_register": 40014,
         "bit": 11, "kind": "DIGITALE_IMPACCATO", "zona": "ALLARMI",
         "riga": 1},
        {"name": "COG2: ALLARME FRIGO", "modbus_register": 40015,
         "kind": "ANALOGICA", "zona": "ALLARMI", "riga": 2},
    ])]}
    out = consolidate([page])
    regs = [v["modbus_register"] for s in out["stations"]
            for v in s["variables"]]
    assert regs == [40014]
    assert out["stations"][0]["variables"][0]["description"] == \
        "COG2: ALLARME FRIGO"
    assert out["counters"]["scarti_V2"] == 1


def test_buchi_di_sequenza_avvisati():
    out = consolidate([page_con_tag_scala(),
                       {"page_no": 3, "stations": []}])
    rules = [w["rule"] for w in out["warnings"]]
    assert "sequenza_buchi" in rules
    detail = next(w["detail"] for w in out["warnings"]
                  if w["rule"] == "sequenza_buchi")
    assert "2" in detail


def test_fold_packed_singoli_con_registro_condiviso():
    page = {"page_no": 1, "stations": [_station("10.0.0.1", [
        _var("Marcia", 1, reg=40020, kind="DIGITALE_SINGOLO"),
        _var("Blocco", 2, reg=40020, kind="DIGITALE_SINGOLO"),
        _var("Solo", 3, reg=40021, kind="DIGITALE_SINGOLO"),
    ])]}
    out = consolidate([page])
    by_desc = {v["description"]: v
               for s in out["stations"] for v in s["variables"]}
    assert by_desc["Marcia"]["kind"] == "DIGITALE_IMPACCATO"
    assert by_desc["Blocco"]["kind"] == "DIGITALE_IMPACCATO"
    assert by_desc["Solo"]["kind"] == "DIGITALE_SINGOLO"
    rules = [w["rule"] for w in out["warnings"]]
    assert "fold_packed" in rules


def test_pagina_compilata_dal_contatore_motore_e_stati_dal_ramo_stati():
    page = {"page_no": 7, "stations": [_station("10.0.0.1", [
        _var("Allarme", 1, reg=40014, bit=5,
             kind="DIGITALE_IMPACCATO"),
    ])], "bitstates": {"rows": [
        {"state_on": "Attivo", "state_off": "OFF", "riga": 1},
    ]}}
    out = consolidate([page])
    var = out["stations"][0]["variables"][0]
    assert var["pagina"] == 7
    assert var["state_on"] == "Attivo"
    assert var["state_off"] == "OFF"
