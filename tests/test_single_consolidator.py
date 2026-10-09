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


def test_shift_riga_tiene_misure_e_avvisa_forte():
    page = {"page_no": 1, "stations": [{
        "name": None, "protocol": "ModBus TCP", "ip": "10.0.0.1",
        "port": 502, "modbus_id": None, "variables": [
            _var("FAULT PC SME", 1, reg=40011, bit=0,
                 kind="DIGITALE_IMPACCATO"),
        ]}], "bitnames": {"rows": [
            {"description": "WATCH_DOG Server 02",
             "modbus_register": 40010, "bit": None, "riga": 1},
        ]}}
    out = consolidate([page])
    var = out["stations"][0]["variables"][0]
    assert var["description"] == "FAULT PC SME"
    assert var["modbus_register"] == 40011
    assert var["bit"] == 0
    rules = [w["rule"] for w in out["warnings"]]
    assert "bit_register_mismatch" in rules
    assert "descrizione_mismatch" in rules
    assert "riga_disallineata" in rules


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


def _triple_misure():
    return {"stations": [_station("192.168.6.20", [
        _var("CO", 1, reg=40001, data_type="ANALOGICO",
             units="mg/Nm3", eng=(0, 200)),
        _var("Allarme sonda", 2, reg=33, bit=None,
             kind="DIGITALE_SINGOLO", data_type="INPUT DIGITALE"),
    ], name="E1")]}


def _triple_nomi():
    return {"rows": [
        {"description": "CO", "modbus_register": 40001, "bit": None,
         "riga": 1},
        {"description": "Allarme sonda", "modbus_register": 33, "bit": 0,
         "riga": 2},
    ]}


def _triple_stati(n=2):
    return {"rows": [
        {"state_on": None, "state_off": None, "riga": i} for i in
        range(1, n + 1)
    ]}


def test_tripla_grezza_motore_in_fence_raggruppata_in_una_pagina():
    import json
    raw = ("[```json\n" + json.dumps(_triple_misure())
           + "\n```\n```json\n" + json.dumps(_triple_nomi())
           + "\n```\n```json\n" + json.dumps(_triple_stati())
           + "\n```]")
    out = consolidate(raw)
    assert out["counters"]["pagine"] == 1
    by_desc = {v["description"]: v
               for s in out["stations"] for v in s["variables"]}
    assert by_desc["Allarme sonda"]["bit"] == 0
    assert by_desc["CO"]["units"] == "mg/Nm3"


def test_mismatch_conteggi_rami_sempre_avvisato_su_tripla():
    import json
    raw = ("```json\n" + json.dumps(_triple_misure()) + "\n```"
           + "```json\n" + json.dumps(_triple_stati(n=5)) + "```")
    out = consolidate(raw)
    rules = [w["rule"] for w in out["warnings"]]
    assert "riga_mismatch" in rules


def test_righe_orfane_senza_misure_avvisate_mai_silenziose():
    out = consolidate([_triple_nomi()])
    rules = [w["rule"] for w in out["warnings"]]
    assert "righe_senza_misure" in rules
    assert out["stations"] == []


def test_buste_con_page_no_e_triple_grezze_convivono():
    import json
    envelope = {"page_no": 1, "stations": [_station("10.0.0.1", [
        _var("X", 1, reg=40001),
    ])]}
    raw = (json.dumps(envelope) + "```json\n"
           + json.dumps(_triple_misure()) + "```")
    out = consolidate(raw)
    assert out["counters"]["pagine"] == 2
    descs = [v["description"] for s in out["stations"]
             for v in s["variables"]]
    assert "X" in descs and "CO" in descs


def test_input_spazzatura_resta_errore_mai_output_vuoto():
    import pytest
    with pytest.raises(ValueError):
        consolidate("ciao mondo ]]]")


def test_blocco_rows_misto_avvisato_e_assegnato_a_nomi():
    out = consolidate([{"stations": []}, {"rows": [
        {"description": "X", "state_on": "On", "riga": 1},
    ]}])
    rules = [w["rule"] for w in out["warnings"]]
    assert "ramo_misto" in rules


def test_blocco_rows_irriconoscibile_resta_errore_forte():
    import pytest
    with pytest.raises(ValueError):
        consolidate([{"stations": []}, {"rows": [{"foo": 1}]}])


def test_blocco_rows_vuoto_nessun_rumore():
    out = consolidate([{"rows": []}])
    assert out["stations"] == []
    assert out["warnings"] == []


def test_righe_stati_grezze_senza_busta_si_agganciano():
    blocks = [_triple_misure(),
              {"state_on": None, "state_off": None, "riga": 1},
              {"state_on": "On", "state_off": "Off", "riga": 2},
              _triple_nomi()]
    out = consolidate(blocks)
    assert out["counters"]["pagine"] == 1
    by_desc = {v["description"]: v
               for s in out["stations"] for v in s["variables"]}
    assert by_desc["Allarme sonda"]["bit"] == 0
    assert by_desc["Allarme sonda"]["state_on"] == "On"
    assert by_desc["Allarme sonda"]["state_off"] == "Off"
    assert by_desc["CO"]["state_on"] is None


def test_riga_stato_orfana_apre_pagina_avvisata_mai_silenziosa():
    out = consolidate([{"state_on": "X", "state_off": "Y", "riga": 9}])
    assert out["stations"] == []
    rules = [w["rule"] for w in out["warnings"]]
    assert "righe_senza_misure" in rules


def test_dizionario_non_riga_resta_errore_forte():
    import pytest
    with pytest.raises(ValueError):
        consolidate([{"pagina": "x"}])


def test_busta_vuota_dopo_nomi_non_azzera_bitnames():
    page = {"page_no": 1, "stations": [{
        "name": None, "protocol": "ModBus TCP", "ip": "10.0.0.1",
        "port": 502, "modbus_id": None, "variables": [
            _var("A", 1, reg=40001), _var("B", 2, reg=40002),
        ]}]}
    names = {"rows": [
        {"description": "A", "modbus_register": 40001, "bit": None,
         "riga": 1},
        {"description": "B", "modbus_register": 40002, "bit": None,
         "riga": 2},
    ]}
    empty_states = {"rows": []}
    out = consolidate([page, names, empty_states])
    by_desc = {v["description"]: v
               for s in out["stations"] for v in s["variables"]}
    assert by_desc["A"]["modbus_register"] == 40001
    assert by_desc["B"]["modbus_register"] == 40002
    rules = [w["rule"] for w in out["warnings"]]
    assert "riga_mismatch" not in rules
