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


def test_precedenza_nomi_con_registro_diverso_tiene_misure():
    # F11 + Luxottica 40028/40029: a descrizioni concordi ma registri
    # diversi, applicare i nomi corrompe (righe fantasma adiacenti).
    page = {"page_no": 1, "stations": [_station("10.0.0.1", [
        _var("Allarme", 1, reg=40014, bit=3,
             kind="DIGITALE_IMPACCATO"),
    ])], "bitnames": {"rows": [
        {"description": "Allarme", "modbus_register": 40015, "bit": 5,
         "riga": 1},
    ]}}
    out = consolidate([page])
    var = out["stations"][0]["variables"][0]
    assert var["modbus_register"] == 40014
    assert var["bit"] == 3
    rules = [w["rule"] for w in out["warnings"]]
    assert "bit_register_mismatch" in rules


def test_precedenza_nomi_riempie_registro_nullo():
    page = {"page_no": 1, "stations": [_station("10.0.0.1", [
        _var("Allarme", 1, reg=None, bit=None,
             kind="DIGITALE_IMPACCATO"),
    ])], "bitnames": {"rows": [
        {"description": "Allarme", "modbus_register": 40015, "bit": 5,
         "riga": 1},
    ]}}
    out = consolidate([page])
    var = out["stations"][0]["variables"][0]
    assert var["modbus_register"] == 40015
    assert var["bit"] == 5


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


def test_blocco_rows_misto_con_chiavi_stato_va_a_stati():
    # Contratto V28: le chiavi di stato vincono sulle chiavi nome.
    out = consolidate([{"stations": []}, {"rows": [
        {"description": "X", "state_on": "On", "riga": 1},
    ]}])
    rules = [w["rule"] for w in out["warnings"]]
    assert "ramo_misto" not in rules


def test_blocco_rows_irriconoscibile_resta_errore_forte():
    import pytest
    with pytest.raises(ValueError):
        consolidate([{"stations": []}, {"rows": [{"foo": 1}]}])


def test_blocco_rows_vuoto_dichiarato_mai_silenzioso():
    out = consolidate([{"rows": []}])
    assert out["stations"] == []
    rules = [w["rule"] for w in out["warnings"]]
    assert "blocco_rows_vuoto" in rules


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


def test_copia_reale_di_riga_placeholder_viene_scartata():
    page = {"page_no": 1, "stations": [
        _station("192.168.6.20", [
            _var("CO", 1, reg=40001),
            _var("Temperatura Fumi", 15, reg=40001),
        ]),
        _station("xxx.xxx.xxx.xxx", [
            _var("Temperatura Fumi", 15, reg=40001),
        ]),
    ]}
    out = consolidate([page])
    by_ip = {}
    for s in out["stations"]:
        by_ip[s["ip"]] = sorted(
            v["description"] for v in s["variables"])
    assert by_ip["192.168.6.20"] == ["CO"]
    assert by_ip["xxx.xxx.xxx.xxx"] == ["Temperatura Fumi"]
    rules = [w["rule"] for w in out["warnings"]]
    assert "copia_reale_da_placeholder" in rules


def test_stato_senza_misura_avvisa_stati_orfani():
    page = {"page_no": 1, "stations": [_station("10.0.0.1", [
        _var("A", 1, reg=40001), _var("B", 2, reg=40002),
    ])], "bitstates": {"rows": [
        {"state_on": "X", "state_off": None, "riga": 9},
    ]}}
    out = consolidate([page])
    rules = [w["rule"] for w in out["warnings"]]
    assert "stati_orfani" in rules
    descs = [v["description"] for s in out["stations"]
             for v in s["variables"]]
    assert descs == ["A", "B"]


def test_stati_radi_avvisano_sottocampionamento():
    page = {"page_no": 2, "stations": [_station("10.0.0.1", [
        _var("A", 1, reg=40001, bit=0, kind="DIGITALE_IMPACCATO"),
        _var("B", 2, reg=40001, bit=1, kind="DIGITALE_IMPACCATO"),
        _var("C", 3, reg=40001, bit=2, kind="DIGITALE_IMPACCATO"),
        _var("D", 4, reg=40001, bit=3, kind="DIGITALE_IMPACCATO"),
    ])], "bitstates": {"rows": [
        {"state_on": "X", "state_off": None, "riga": 1},
    ]}}
    out = consolidate([page])
    rules = [w["rule"] for w in out["warnings"]]
    assert "sospetto_sottocampionamento" in rules


def test_stati_assenti_avvisano_sottocampionamento():
    # Comportamento voluto: zero stati su pagina digitale = fallback
    # keyword dichiarato, mai miss silenzioso (solo PDF in output).
    page = {"page_no": 1, "stations": [_station("10.0.0.1", [
        _var("A", 1, reg=40001, bit=0, kind="DIGITALE_IMPACCATO"),
    ])], "bitstates": {"rows": []}}
    out = consolidate([page])
    rules = [w["rule"] for w in out["warnings"]]
    assert "sospetto_sottocampionamento" in rules


def test_coppia_typo_su_stessa_riga_avvisa_refuso():
    page = {"page_no": 1, "stations": [{
        "name": None, "protocol": "ModBus TCP", "ip": "10.0.0.1",
        "port": 502, "modbus_id": None, "variables": [
            _var("Allarme 1 Ossigeno umido", 13, reg=40001, bit=0,
                 kind="DIGITALE_IMPACCATO"),
        ]}], "bitnames": {"rows": [
            {"description": "Allarme 1 Ossiegno umido",
             "modbus_register": 40001, "bit": 0, "riga": 13},
        ]}}
    out = consolidate([page])
    rules = [w["rule"] for w in out["warnings"]]
    assert "refuso_sospetto" in rules
    var = out["stations"][0]["variables"][0]
    assert var["modbus_register"] == 40001


def test_sottocampionamento_conta_anche_i_bit_dei_nomi():
    page = {"page_no": 2, "stations": [_station("10.0.0.1", [
        _var("A", 1, reg=40001, bit=0, kind="DIGITALE_IMPACCATO"),
        _var("B", 2, reg=None, bit=None, kind="ANALOGICA"),
        _var("C", 3, reg=None, bit=None, kind="ANALOGICA"),
        _var("D", 4, reg=None, bit=None, kind="ANALOGICA"),
    ])], "bitnames": {"rows": [
        {"description": "A", "modbus_register": 40001, "bit": 0,
         "riga": 1},
        {"description": "B", "modbus_register": 40001, "bit": 1,
         "riga": 2},
        {"description": "C", "modbus_register": 40001, "bit": 2,
         "riga": 3},
        {"description": "D", "modbus_register": 40001, "bit": 3,
         "riga": 4},
    ]}, "bitstates": {"rows": [
        {"state_on": "X", "state_off": None, "riga": 1},
    ]}}
    out = consolidate([page])
    rules = [w["rule"] for w in out["warnings"]]
    assert "sospetto_sottocampionamento" in rules


def _page_state_join(measures_desc, names_desc, states_desc):
    vars_ = [_var(measures_desc, 1, reg=40001, bit=0,
                  kind="DIGITALE_IMPACCATO")]
    page = {"page_no": 1, "stations": [_station("10.0.0.1", vars_)],
            "bitnames": {"rows": [
                {"description": names_desc, "modbus_register": 40001,
                 "bit": 0, "riga": 1}]},
            "bitstates": {"rows": [
                {"description": states_desc, "state_on": "ON-X",
                 "state_off": None, "riga": 1}]}}
    return consolidate([page])


def test_stati_con_descrizione_diversa_non_applicati():
    out = _page_state_join("Lampada Manutenzione", "Lampada Manutenzione",
                           "Allarme Generatore")
    var = out["stations"][0]["variables"][0]
    assert var["state_on"] is None
    rules = [w["rule"] for w in out["warnings"]]
    assert "stati_disallineati" in rules


def test_stati_con_descrizione_concorde_applicati():
    out = _page_state_join("Lampada Manutenzione", "Lampada Manutenzione",
                           "Lampada Manutenzione")
    var = out["stations"][0]["variables"][0]
    assert var["state_on"] == "ON-X"


def test_stati_senza_descrizione_restano_applicati():
    page = {"page_no": 1, "stations": [_station("10.0.0.1", [
        _var("Lampada", 1, reg=40001, bit=0,
             kind="DIGITALE_IMPACCATO")])], "bitstates": {"rows": [
        {"state_on": "ON-X", "state_off": None, "riga": 1}]}}
    out = consolidate([page])
    assert out["stations"][0]["variables"][0]["state_on"] == "ON-X"


def test_maggioranza_due_rami_ripristina_fedele():
    out = _page_state_join("Allarme 1 Ossigeno umido",
                           "Allarme 1 Ossiegno umido",
                           "Allarme 1 Ossiegno umido")
    var = out["stations"][0]["variables"][0]
    assert var["description"] == "Allarme 1 Ossiegno umido"
    rules = [w["rule"] for w in out["warnings"]]
    assert "refuso_maggioranza" in rules


def test_blocco_stati_v28_va_a_stati_senza_avvisi():
    measures = {"stations": [_station("10.0.0.1", [
        _var("Lampada", 1, reg=40001, bit=0,
             kind="DIGITALE_IMPACCATO")])]}
    states = {"rows": [
        {"description": "Lampada", "state_on": "ON-X",
         "state_off": None, "riga": 1}]}
    out = consolidate([measures, states])
    assert out["stations"][0]["variables"][0]["state_on"] == "ON-X"
    rules = [w["rule"] for w in out["warnings"]]
    assert "ramo_misto" not in rules
    assert "stati_disallineati" not in rules


def test_blocco_veramente_misto_viene_splittao_e_avvisato():
    out = consolidate([{"stations": []}, {"rows": [
        {"description": "A", "modbus_register": 40001, "bit": 0,
         "riga": 1},
        {"description": "B", "state_on": "On", "riga": 2},
    ]}])
    rules = [w["rule"] for w in out["warnings"]]
    assert "ramo_misto" in rules


def test_maggioranza_con_registri_diversi_non_scavalca():
    page = {"page_no": 1, "stations": [_station("10.0.0.1", [
        _var("OVF COT_01", 13, reg=40007, bit=0,
             kind="DIGITALE_IMPACCATO"),
    ])], "bitnames": {"rows": [
        {"description": "OVF COT_02", "modbus_register": 40007, "bit": 1,
         "riga": 13},
    ]}, "bitstates": {"rows": [
        {"description": "OVF COT_02", "state_on": "Errore",
         "state_off": None, "riga": 13}]}}
    out = consolidate([page])
    var = out["stations"][0]["variables"][0]
    assert var["description"] == "OVF COT_01"
    assert (var["modbus_register"], var["bit"]) == (40007, 0)
    rules = [w["rule"] for w in out["warnings"]]
    assert "refuso_maggioranza" not in rules
    assert "riga_disallineata" in rules


def test_nomi_con_registro_diverso_non_applicati():
    page = {"page_no": 11, "stations": [_station("10.0.0.1", [
        _var("Riserva STATI LOGICI", 33, reg=40029, bit=None,
             kind="DIGITALE_SINGOLO"),
    ])], "bitnames": {"rows": [
        {"description": "Riserva STATI LOGICI",
         "modbus_register": 40028, "bit": 7, "riga": 33},
    ]}}
    out = consolidate([page])
    var = out["stations"][0]["variables"][0]
    assert (var["modbus_register"], var["bit"]) == (40029, None)
    rules = [w["rule"] for w in out["warnings"]]
    assert "bit_register_mismatch" in rules


def _station_bit16(variables):
    return {"page_no": 1, "stations": [_station("10.0.0.1", variables)]}


def test_bit16_senza_fratello_viene_rimappato_con_avviso():
    out = consolidate([_station_bit16([
        _var("RUNNING", 1, reg=40023, bit=16,
             kind="DIGITALE_IMPACCATO"),
    ])])
    var = out["stations"][0]["variables"][0]
    assert var["bit"] == 15
    assert out["counters"].get("bit_offset_pagina", 0) >= 1


def test_bit16_con_fratello_resta_e_avvisa():
    out = consolidate([_station_bit16([
        _var("A", 1, reg=40023, bit=15,
             kind="DIGITALE_IMPACCATO"),
        _var("B", 2, reg=40023, bit=16,
             kind="DIGITALE_IMPACCATO"),
    ])])
    bits = sorted(v["bit"] for v in out["stations"][0]["variables"])
    assert bits == [15, 16]
    rules = [w["rule"] for w in out["warnings"]]
    assert "bit_fuori_range" in rules


def test_pagina_tutti_rami_vuoti_avvisa():
    out = consolidate([{"page_no": 12, "stations": [{
        "name": None, "protocol": None, "ip": None, "port": None,
        "modbus_id": None, "variables": []}]},
        {"rows": []}, {"rows": []}])
    rules = [w["rule"] for w in out["warnings"]]
    assert "pagina_vuota_sospetta" in rules


def test_pagina_con_righe_non_avvisa_vuoto():
    out = consolidate([{"page_no": 1, "stations": [_station("10.0.0.1", [
        _var("Riserva", 1, reg=40001)])]}])
    rules = [w["rule"] for w in out["warnings"]]
    assert "pagina_vuota_sospetta" not in rules


def test_stato_misure_non_cancellato_da_stati_nulli():
    page = {"page_no": 1, "stations": [_station("10.0.0.1", [
        _var("Lampada", 1, reg=40001, bit=0,
             kind="DIGITALE_IMPACCATO", state_on="Accesa"),
    ])], "bitstates": {"rows": [
        {"description": "Lampada", "state_on": None, "state_off": None,
         "riga": 1},
    ]}}
    out = consolidate([page])
    assert out["stations"][0]["variables"][0]["state_on"] == "Accesa"


def test_stati_applicati_anche_con_typo_nella_descrizione():
    page = {"page_no": 1, "stations": [_station("10.0.0.1", [
        _var("Allarme 1 Ossigeno umido", 13, reg=40001, bit=0,
             kind="DIGITALE_IMPACCATO"),
    ])], "bitstates": {"rows": [
        {"description": "Allarme 1 Ossiegno umido", "state_on": "ON-X",
         "state_off": None, "riga": 13},
    ]}}
    out = consolidate([page])
    var = out["stations"][0]["variables"][0]
    assert var["state_on"] == "ON-X"
    rules = [w["rule"] for w in out["warnings"]]
    assert "stati_disallineati" not in rules


def test_stato_junk_non_applicato():
    page = {"page_no": 1, "stations": [_station("10.0.0.1", [
        _var("Allarme Sonda riscaldata", 20, reg=40001, bit=0,
             kind="DIGITALE_IMPACCATO"),
    ])], "bitstates": {"rows": [
        {"description": "Allarme Sonda riscaldata", "state_on": "1",
         "state_off": None, "riga": 20},
    ]}}
    out = consolidate([page])
    var = out["stations"][0]["variables"][0]
    assert var["state_on"] is None


def test_stato_parentetico_da_descrizione_non_applicato():
    page = {"page_no": 1, "stations": [_station("10.0.0.1", [
        _var("STATO COM. POMPA M1  (1= RUNNING)", 1, reg=40001, bit=8,
             kind="DIGITALE_IMPACCATO"),
    ])], "bitstates": {"rows": [
        {"description": "STATO COM. POMPA M1  (1= RUNNING)",
         "state_on": "1= RUNNING", "state_off": None, "riga": 1},
    ]}}
    out = consolidate([page])
    var = out["stations"][0]["variables"][0]
    assert var["state_on"] is None


def test_stati_zero_su_pagina_digitale_avvisano():
    # Pagina con digitali ma zero stati: miss silenzioso vietato, il
    # fallback keyword va dichiarato (esattezza: solo PDF in output).
    page = {"page_no": 1, "stations": [_station("10.0.0.1", [
        _var("Over Flow NO", 1, reg=40005, bit=0,
             kind="DIGITALE_IMPACCATO"),
        _var("Rottura Cavo NO", 2, reg=40005, bit=8,
             kind="DIGITALE_IMPACCATO"),
    ])], "bitstates": {"rows": []}}
    out = consolidate([page])
    rules = [w["rule"] for w in out["warnings"]]
    assert "sospetto_sottocampionamento" in rules


def test_blocco_rows_vuoto_non_sparisce_silenzioso():
    # Un blocco {"rows": []} e' il ramo che tace (V27): va dichiarato,
    # mai scartato in silenzio (solo PDF in output).
    page = {"page_no": 1, "stations": [_station("10.0.0.1", [
        _var("Over Flow NO", 1, reg=40005, bit=0,
             kind="DIGITALE_IMPACCATO"),
    ])], "bitnames": {"rows": []}}
    out = consolidate([page, {"rows": []}])
    rules = [w["rule"] for w in out["warnings"]]
    assert "blocco_rows_vuoto" in rules


def test_stati_applicati_con_normalizzazione_v19():
    page = {"page_no": 1, "stations": [_station("10.0.0.1", [
        _var("Valvola  Y1", 3, reg=40001, bit=8,
             kind="DIGITALE_IMPACCATO"),
    ])], "bitstates": {"rows": [
        {"description": '"Valvola Y1 ()"', "state_on": "APERTO",
         "state_off": "CHIUSO", "riga": 3},
    ]}}
    out = consolidate([page])
    var = out["stations"][0]["variables"][0]
    assert var["state_on"] == "APERTO"
    assert var["state_off"] == "CHIUSO"
    rules = [w["rule"] for w in out["warnings"]]
    assert "stati_disallineati" not in rules


def test_stati_veramente_diversi_restano_scartati():
    page = {"page_no": 1, "stations": [_station("10.0.0.1", [
        _var("Pompa M1", 3, reg=40001, bit=8,
             kind="DIGITALE_IMPACCATO"),
    ])], "bitstates": {"rows": [
        {"description": "Valvola Y9", "state_on": "APERTO",
         "state_off": None, "riga": 3},
    ]}}
    out = consolidate([page])
    var = out["stations"][0]["variables"][0]
    assert var["state_on"] is None
    rules = [w["rule"] for w in out["warnings"]]
    assert "stati_disallineati" in rules


def test_duplicato_riga_vince_chi_matcha():
    page = {"page_no": 1, "stations": [_station("10.0.0.1", [
        _var("Pompa M1", 5, reg=40001, bit=8,
             kind="DIGITALE_IMPACCATO"),
    ])], "bitstates": {"rows": [
        {"description": "Valvola Y9", "state_on": "SBAGLIATO",
         "state_off": None, "riga": 5},
        {"description": "Pompa M1", "state_on": "IN MARCIA",
         "state_off": None, "riga": 5},
    ]}}
    out = consolidate([page])
    var = out["stations"][0]["variables"][0]
    assert var["state_on"] == "IN MARCIA"


def test_duplicato_riga_senza_match_tiene_first_wins():
    page = {"page_no": 1, "stations": [_station("10.0.0.1", [
        _var("Pompa M1", 5, reg=40001, bit=8,
             kind="DIGITALE_IMPACCATO"),
    ])], "bitstates": {"rows": [
        {"description": "Valvola Y9", "state_on": "SBAGLIATO",
         "state_off": None, "riga": 5},
        {"description": "Bruciatore Z", "state_on": "ALTRO",
         "state_off": None, "riga": 5},
    ]}}
    out = consolidate([page])
    rules = [w["rule"] for w in out["warnings"]]
    assert "stati_disallineati" in rules


def test_orfano_con_stati_dichiarato_utile():
    page = {"page_no": 1, "stations": [_station("10.0.0.1", [
        _var("Pompa M1", 1, reg=40001, bit=8,
             kind="DIGITALE_IMPACCATO"),
    ])], "bitstates": {"rows": [
        {"description": "Valvola Y9", "state_on": "APERTO",
         "state_off": "CHIUSO", "riga": 9},
    ]}}
    out = consolidate([page])
    by_rule = {}
    for w in out["warnings"]:
        by_rule.setdefault(w["rule"], []).append(w["detail"])
    assert "stati_orfani_utili" in by_rule
    assert any("APERTO" in d for d in by_rule["stati_orfani_utili"])


def test_orfano_nullo_resta_orfano_semplice():
    page = {"page_no": 1, "stations": [_station("10.0.0.1", [
        _var("Pompa M1", 1, reg=40001, bit=8,
             kind="DIGITALE_IMPACCATO"),
    ])], "bitstates": {"rows": [
        {"description": "Valvola Y9", "state_on": None,
         "state_off": None, "riga": 9},
    ]}}
    out = consolidate([page])
    rules = [w["rule"] for w in out["warnings"]]
    assert "stati_orfani" in rules
    assert "stati_orfani_utili" not in rules


def test_orfani_duplicati_entrambi_dichiarati():
    page = {"page_no": 1, "stations": [_station("10.0.0.1", [
        _var("Pompa M1", 1, reg=40001, bit=8,
             kind="DIGITALE_IMPACCATO"),
    ])], "bitstates": {"rows": [
        {"description": "Valvola Y9", "state_on": "APERTO",
         "state_off": None, "riga": 9},
        {"description": "Valvola Y9 bis", "state_on": "CHIUSO",
         "state_off": None, "riga": 9},
    ]}}
    out = consolidate([page])
    details = [w["detail"] for w in out["warnings"]
               if w["rule"] == "stati_orfani_utili"]
    assert len(details) == 2
    assert any("APERTO" in d for d in details)
    assert any("CHIUSO" in d for d in details)


def test_chiave_checklist_ignorata_dal_join():
    vars_ = [_var("Pompa M1", 5, reg=40001, bit=8,
                  kind="DIGITALE_IMPACCATO")]
    base = {"page_no": 1, "stations": [_station("10.0.0.1", vars_)],
            "bitstates": {"rows": [
                {"description": "Pompa M1", "state_on": "IN MARCIA",
                 "state_off": None, "riga": 5}]}}
    import copy
    extended = copy.deepcopy(base)
    extended["bitstates"]["checklist"] = [
        {"riga": 5, "description": "Pompa M1"}]
    extended["bitstates"]["digitali_visti"] = 1
    assert consolidate([base]) == consolidate([extended])


def test_stati_riallineati_su_descrizione_univoca():
    page = {"page_no": 1, "stations": [_station("10.0.0.1", [
        _var("Maintenance MCA10", 42, reg=40003, bit=9,
             kind="DIGITALE_IMPACCATO"),
    ])], "bitstates": {"rows": [
        {"description": "Maintenance MCA10", "state_on": "Manutenzione",
         "state_off": None, "riga": 41},
    ]}}
    out = consolidate([page])
    var = out["stations"][0]["variables"][0]
    assert var["state_on"] == "Manutenzione"
    rules = [w["rule"] for w in out["warnings"]]
    assert "stati_disallineati" not in rules
    assert "stati_riallineati" in rules


def test_riallineamento_ambiguo_resta_scartato():
    page = {"page_no": 1, "stations": [_station("10.0.0.1", [
        _var("Pompa M1", 5, reg=40001, bit=8,
             kind="DIGITALE_IMPACCATO"),
    ])], "bitstates": {"rows": [
        {"description": "Valvola Y9", "state_on": "X",
         "state_off": None, "riga": 5},
        {"description": "Pompa M1", "state_on": "Y",
         "state_off": None, "riga": 6},
        {"description": "Pompa M1", "state_on": "Z",
         "state_off": None, "riga": 8},
    ]}}
    out = consolidate([page])
    var = out["stations"][0]["variables"][0]
    assert var["state_on"] is None
    rules = [w["rule"] for w in out["warnings"]]
    assert "stati_disallineati" in rules
    assert "stati_riallineati" not in rules


def test_riallineato_anche_senza_riga_propre():
    page = {"page_no": 1, "stations": [_station("10.0.0.1", [
        _var("Pompa M1", 7, reg=40001, bit=8,
             kind="DIGITALE_IMPACCATO"),
    ])], "bitstates": {"rows": [
        {"description": "Pompa M1", "state_on": "IN MARCIA",
         "state_off": None, "riga": 6},
    ]}}
    out = consolidate([page])
    var = out["stations"][0]["variables"][0]
    assert var["state_on"] == "IN MARCIA"
    rules = [w["rule"] for w in out["warnings"]]
    assert "stati_riallineati" in rules


def test_chiave_checklist_misure_ignorata_dal_join():
    vars_ = [_var("Pompa M1", 5, reg=40001, bit=8,
                  kind="DIGITALE_IMPACCATO")]
    base = {"page_no": 1, "stations": [_station("10.0.0.1", vars_)]}
    import copy
    extended = copy.deepcopy(base)
    extended["checklist"] = [{"riga": 5, "description": "Pompa M1"}]
    extended["righe_viste"] = 1
    assert consolidate([base]) == consolidate([extended])


def test_nomi_desc_null_non_trasferiscono_bit():
    page = {"page_no": 1, "stations": [_station("10.0.0.1", [
        _var("COG2: AUTOCAL", 30, reg=40022, bit=4,
             kind="DIGITALE_IMPACCATO"),
    ])], "bitnames": {"rows": [
        {"description": None, "modbus_register": 40022, "bit": 5,
         "riga": 30},
    ]}}
    out = consolidate([page])
    var = out["stations"][0]["variables"][0]
    assert var["bit"] == 4
    rules = [w["rule"] for w in out["warnings"]]
    assert "riga_mismatch" in rules
    assert not any(w["rule"] == "bit_register_mismatch" and w.get("riga") == 30
                   for w in out["warnings"])


def test_riga_nomi_senza_descrizione_invisibile():
    page = {"page_no": 1, "stations": [_station("10.0.0.1", [
        _var("COG2: AUTOCAL", 30, reg=40022, bit=4,
             kind="DIGITALE_IMPACCATO"),
    ])], "bitnames": {"rows": [
        {"description": None, "modbus_register": 40022, "bit": 5,
         "riga": 30},
    ]}}
    out = consolidate([page])
    var = out["stations"][0]["variables"][0]
    assert var["bit"] == 4


def test_bit_nomi_vince_su_accordo_normalizzato():
    page = {"page_no": 1, "stations": [_station("10.0.0.1", [
        _var("Valvola Y1", 8, reg=40001, bit=0,
             kind="DIGITALE_IMPACCATO"),
    ])], "bitnames": {"rows": [
        {"description": '"Valvola Y1 ()"', "modbus_register": 40001,
         "bit": 8, "riga": 8},
    ]}}
    out = consolidate([page])
    var = out["stations"][0]["variables"][0]
    assert var["bit"] == 8


def test_digit_diversi_non_sono_typo():
    page = {"page_no": 1, "stations": [_station("10.0.0.1", [
        _var("Condizionatore 1 OFF", 12, reg=40001, bit=10,
             kind="DIGITALE_IMPACCATO"),
    ])], "bitnames": {"rows": [
        {"description": "Condizionatore 2 OFF", "modbus_register": 40001,
         "bit": 11, "riga": 12},
    ]}}
    out = consolidate([page])
    var = out["stations"][0]["variables"][0]
    assert var["bit"] == 10
    rules = [w["rule"] for w in out["warnings"]]
    assert "bit_register_mismatch" in rules


def test_typo_singola_lettera_non_blocca_bit():
    page = {"page_no": 1, "stations": [_station("10.0.0.1", [
        _var("Output DCS Forzatl", 6, reg=40011, bit=7,
             kind="DIGITALE_IMPACCATO"),
    ])], "bitnames": {"rows": [
        {"description": "Output DCS Forzati", "modbus_register": 40011,
         "bit": 6, "riga": 6},
    ]}}
    out = consolidate([page])
    var = out["stations"][0]["variables"][0]
    assert var["bit"] == 6


def test_bit_ancorato_cross_riga_su_descrizione_univoca():
    page = {"page_no": 1, "stations": [_station("10.0.0.1", [
        _var("GC0x: STATO COMANDO POMPA P1", 26, reg=40024, bit=16,
             kind="DIGITALE_IMPACCATO"),
    ])], "bitnames": {"rows": [
        {"description": "GC0x: STATO COMANDO POMPA P1",
         "modbus_register": 40024, "bit": 0, "riga": 25},
    ]}}
    out = consolidate([page])
    var = out["stations"][0]["variables"][0]
    assert var["bit"] == 0
    rules = [w["rule"] for w in out["warnings"]]
    assert "bit_register_mismatch" in rules


def test_ancoraggio_non_scatta_su_descrizione_duplicata():
    page = {"page_no": 1, "stations": [_station("10.0.0.1", [
        _var("Valvola Y1", 26, reg=40001, bit=9,
             kind="DIGITALE_IMPACCATO"),
    ])], "bitnames": {"rows": [
        {"description": "Valvola Y1", "modbus_register": 40001,
         "bit": 0, "riga": 20},
        {"description": "Valvola Y1", "modbus_register": 40001,
         "bit": 1, "riga": 21},
    ]}}
    out = consolidate([page])
    var = out["stations"][0]["variables"][0]
    assert var["bit"] == 9


def test_ancoraggio_non_scatta_su_registro_diverso():
    page = {"page_no": 1, "stations": [_station("10.0.0.1", [
        _var("Valvola Y1", 26, reg=40001, bit=9,
             kind="DIGITALE_IMPACCATO"),
    ])], "bitnames": {"rows": [
        {"description": "Valvola Y1", "modbus_register": 40002,
         "bit": 0, "riga": 25},
    ]}}
    out = consolidate([page])
    var = out["stations"][0]["variables"][0]
    assert var["bit"] == 9


def test_ancoraggio_non_importa_bit_fuori_range():
    """Se la riga nomi shiftata dice bit 16, il bit 15 delle misure resta.

    Caso reale LEGNANO/GC0x OR ALLARMI: misure bit 15 (corretto da PDF),
    nomi riga successiva bit 16. Ancorare il 16 produce un bit ADAS-invalido
    e perde il 15 gia' valido.
    """
    page = {"page_no": 1, "stations": [_station("10.0.0.1", [
        _var("GV0x: OR ALLARMI", 15, reg=40021, bit=15,
             kind="DIGITALE_IMPACCATO"),
    ])], "bitnames": {"rows": [
        {"description": "GV0x: OR ALLARMI", "modbus_register": 40021,
         "bit": 16, "riga": 9},
    ]}}
    out = consolidate([page])
    var = out["stations"][0]["variables"][0]
    assert var["bit"] == 15


def test_ancoraggio_non_scatta_su_registro_gia_valido():
    """Registro con bit validi e unici: le misure vincono sui nomi shiftati.

    Caso reale LEGNANO 40021: misure 13/14/15 (verita' PDF), nomi
    traslati di una riga 14/15/16. Ancorare i nomi sposterebbe tutto.
    """
    page = {"page_no": 1, "stations": [_station("10.0.0.1", [
        _var("COGx: OR ALLARMI", 6, reg=40021, bit=13,
             kind="DIGITALE_IMPACCATO"),
        _var("GC0x: OR ALLARMI", 7, reg=40021, bit=14,
             kind="DIGITALE_IMPACCATO"),
        _var("GV0x: OR ALLARMI", 8, reg=40021, bit=15,
             kind="DIGITALE_IMPACCATO"),
    ])], "bitnames": {"rows": [
        {"description": "COGx: OR ALLARMI", "modbus_register": 40021,
         "bit": 14, "riga": 7},
        {"description": "GC0x: OR ALLARMI", "modbus_register": 40021,
         "bit": 15, "riga": 8},
        {"description": "GV0x: OR ALLARMI", "modbus_register": 40021,
         "bit": 16, "riga": 9},
    ]}}
    out = consolidate([page])
    bits = {v["description"]: v["bit"]
            for v in out["stations"][0]["variables"]}
    assert bits == {"COGx: OR ALLARMI": 13, "GC0x: OR ALLARMI": 14,
                    "GV0x: OR ALLARMI": 15}


def test_ancoraggio_ripara_registro_con_bit_duplicato():
    """Se le misure hanno un bit duplicato, i nomi riallineano il registro.

    Caso reale LUXOTTICA 40023: misure 7/8 con 8 gia' occupato dal THC,
    nomi 6/7 (verita' PDF).
    """
    page = {"page_no": 1, "stations": [_station("10.0.0.1", [
        _var("THC CALIBRAZIONE", 1, reg=40023, bit=8,
             kind="DIGITALE_IMPACCATO"),
        _var('MANUTENZIONE RICH. "O2 WET"', 16, reg=40023, bit=7,
             kind="DIGITALE_IMPACCATO"),
        _var("MANUTENZIONE RICH. ANALIZZATORE POLVERI", 17, reg=40023,
             bit=8, kind="DIGITALE_IMPACCATO"),
    ])], "bitnames": {"rows": [
        {"description": 'MANUTENZIONE RICH. "O2 WET"',
         "modbus_register": 40023, "bit": 6, "riga": 15},
        {"description": "MANUTENZIONE RICH. ANALIZZATORE POLVERI",
         "modbus_register": 40023, "bit": 7, "riga": 16},
    ]}}
    out = consolidate([page])
    bits = {v["description"]: v["bit"]
            for v in out["stations"][0]["variables"]}
    assert bits['MANUTENZIONE RICH. "O2 WET"'] == 6
    assert bits["MANUTENZIONE RICH. ANALIZZATORE POLVERI"] == 7
