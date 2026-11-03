"""Test per l'oracle apply nel consolidatore (redesign v2).

Il LV2 unificato restituisce per pagina:
    {"page_no": int, "stations": [...], "verifica": {...}}
dove ``verifica`` è il JSON difetti dell'oracolo (schema vlm_oracle_v1).

Il consolidatore:
- consolida ``stations`` come oggi;
- applica le correzioni oracolo (SOLO aggiungi/annulla, mai sovrascrive);
- marca ogni tocco con ``_audit_oracolo``;
- emette warning per ogni difetto (anche quelli non corretti).
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from nodes.single_consolidator import consolidate  # noqa: E402


def _page(stations, verifica=None, page_no=1):
    page = {"page_no": page_no, "stations": stations}
    if verifica is not None:
        page["verifica"] = verifica
    return page


def _station(ip="10.0.0.1", variables=None):
    return {"name": "SME", "protocol": "ModBus TCP", "ip": ip,
            "port": 502, "modbus_id": None,
            "variables": variables or []}


def _var(desc, reg, bit=None, units=None, state_on=None, state_off=None,
         riga=1, kind=None):
    return {"description": desc, "units": units,
            "modbus_register": reg, "bit": bit, "kind": kind,
            "data_type": None, "read_write": None, "note": None,
            "state_on": state_on, "state_off": state_off,
            "scale_elec_start": None, "scale_elec_end": None,
            "scale_eng_start": None, "scale_eng_end": None,
            "limit_hour": None, "limit_day": None,
            "zona": None, "tag": None, "pagina": None, "riga": riga}


def test_oracle_apply_aggiunge_mancante():
    """Un difetto 'mancanti' aggiunge la variabile con audit trail."""
    page = _page(
        [_station(variables=[_var("SO2", 49, units="mg/Nm3", riga=1)])],
        verifica={"page_no": 1,
                  "mancanti": [{"description": "NOX", "registro": 50,
                                "bit": None,
                                "evidenza": "riga 2: NOX 40050"}],
                  "unita_inventate": [], "junk_stati": [],
                  "refusi_corretti": [], "ip_dichiarati_non_usati": []})
    out = consolidate([json.loads(json.dumps(page))])
    vars_ = out["stations"][0]["variables"]
    assert len(vars_) == 2
    added = [v for v in vars_ if v["description"] == "NOX"]
    assert len(added) == 1
    assert added[0]["modbus_register"] == 50
    audit = added[0].get("_audit_oracolo")
    assert audit is not None
    assert audit["azione"] == "aggiunta"
    assert audit["evidenza"] == "riga 2: NOX 40050"
    rules = [w["rule"] for w in out["warnings"]]
    assert "oracolo_aggiunta" in rules


def test_oracle_apply_annulla_unita_inventata():
    """Un difetto 'unita_inventate' azzera units con audit trail."""
    page = _page(
        [_station(variables=[_var("SO2", 49, units="mg/Nm3", riga=1)])],
        verifica={"page_no": 1, "mancanti": [],
                  "unita_inventate": [{"description": "SO2",
                                       "unita": "mg/Nm3",
                                       "evidenza": "cella vuota"}],
                  "junk_stati": [], "refusi_corretti": [],
                  "ip_dichiarati_non_usati": []})
    out = consolidate([json.loads(json.dumps(page))])
    var = out["stations"][0]["variables"][0]
    assert var["units"] is None
    audit = var.get("_audit_oracolo")
    assert audit is not None
    assert audit["azione"] == "annullata"
    assert audit["campo"] == "units"
    assert audit["evidenza"] == "cella vuota"
    rules = [w["rule"] for w in out["warnings"]]
    assert "oracolo_annullata" in rules


def test_oracle_apply_annulla_junk_stato():
    """Un difetto 'junk_stati' azzera lo stato con audit trail."""
    page = _page(
        [_station(variables=[_var("Allarme", 50, bit=3, state_on="1",
                                  kind="DIGITALE_IMPACCATO", riga=1)])],
        verifica={"page_no": 1, "mancanti": [], "unita_inventate": [],
                  "junk_stati": [{"description": "Allarme",
                                  "campo": "state_on", "valore": "1",
                                  "evidenza": "cella vuota"}],
                  "refusi_corretti": [], "ip_dichiarati_non_usati": []})
    out = consolidate([json.loads(json.dumps(page))])
    var = out["stations"][0]["variables"][0]
    assert var["state_on"] is None
    audit = var.get("_audit_oracolo")
    assert audit is not None
    assert audit["azione"] == "annullata"
    assert audit["campo"] == "state_on"
    rules = [w["rule"] for w in out["warnings"]]
    assert "oracolo_annullata" in rules


def test_oracle_refuso_solo_warning():
    """Un difetto 'refusi_corretti' NON tocca la descrizione (fedeltà)."""
    page = _page(
        [_station(variables=[_var("Ossigeno", 51, riga=1)])],
        verifica={"page_no": 1, "mancanti": [], "unita_inventate": [],
                  "junk_stati": [],
                  "refusi_corretti": [{"description_finale": "Ossigeno",
                                       "description_pdf": "Ossiegno",
                                       "evidenza": "cella: Ossiegno"}],
                  "ip_dichiarati_non_usati": []})
    out = consolidate([json.loads(json.dumps(page))])
    var = out["stations"][0]["variables"][0]
    assert var["description"] == "Ossigeno"  # non toccata
    assert "_audit_oracolo" not in var
    rules = [w["rule"] for w in out["warnings"]]
    assert "oracolo_refuso" in rules


def test_oracle_ip_solo_warning():
    """Un difetto 'ip_dichiarati_non_usati' NON crea stazioni."""
    page = _page(
        [_station(ip="10.0.0.1",
                  variables=[_var("SO2", 49, riga=1)])],
        verifica={"page_no": 1, "mancanti": [], "unita_inventate": [],
                  "junk_stati": [], "refusi_corretti": [],
                  "ip_dichiarati_non_usati": [{"ip": "10.0.0.2",
                                               "evidenza": "IP PLC: 10.0.0.2"}]})
    out = consolidate([json.loads(json.dumps(page))])
    assert len(out["stations"]) == 1  # nessuna stazione inventata
    rules = [w["rule"] for w in out["warnings"]]
    assert "oracolo_ip" in rules


def test_oracle_senza_verifica_invariato():
    """Senza 'verifica' il consolidatore si comporta come prima."""
    page = _page([_station(variables=[_var("SO2", 49, units="mg/Nm3",
                                           riga=1)])])
    out = consolidate([json.loads(json.dumps(page))])
    var = out["stations"][0]["variables"][0]
    assert var["units"] == "mg/Nm3"
    assert "_audit_oracolo" not in var
    rules = [w["rule"] for w in out["warnings"]]
    assert not any(r.startswith("oracolo_") for r in rules)


def test_oracle_mancante_duplicato_non_aggiunto():
    """Se la riga 'mancante' esiste già, non si duplica."""
    page = _page(
        [_station(variables=[_var("SO2", 49, riga=1)])],
        verifica={"page_no": 1,
                  "mancanti": [{"description": "SO2", "registro": 49,
                                "bit": None, "evidenza": "riga 1"}],
                  "unita_inventate": [], "junk_stati": [],
                  "refusi_corretti": [], "ip_dichiarati_non_usati": []})
    out = consolidate([json.loads(json.dumps(page))])
    vars_ = out["stations"][0]["variables"]
    assert len(vars_) == 1
    rules = [w["rule"] for w in out["warnings"]]
    assert "oracolo_duplicato" in rules


def test_oracle_evidenza_vuota_scartata():
    """Un difetto senza evidenza non viene applicato (D5)."""
    page = _page(
        [_station(variables=[_var("SO2", 49, units="mg/Nm3", riga=1)])],
        verifica={"page_no": 1, "mancanti": [],
                  "unita_inventate": [{"description": "SO2",
                                       "unita": "mg/Nm3",
                                       "evidenza": ""}],
                  "junk_stati": [], "refusi_corretti": [],
                  "ip_dichiarati_non_usati": []})
    out = consolidate([json.loads(json.dumps(page))])
    var = out["stations"][0]["variables"][0]
    assert var["units"] == "mg/Nm3"  # non annullata: evidenza vuota
    assert "_audit_oracolo" not in var
    rules = [w["rule"] for w in out["warnings"]]
    assert "oracolo_evidenza_vuota" in rules
