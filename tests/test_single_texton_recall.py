"""Pin del recall TEXTON==stato PDF (caratterizzazione, mai peggiorare).

Replay deterministico dai TAP_MERGE congelati (pinna il codice, non i run
VLM). PROTEC_2 non ha tap merge: pinnato dal finale congelato.
Soglie = recall misurato il 2026-10-13 dopo P1-P3 (migliorabile, mai sotto).
"""
import json
import struct
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).parent.parent
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "tests"))

from nodes.single_consolidator import consolidate
from test_single_creator_v15 import run_script, SRC

TESTS = REPO / "myhydra" / "single_pdf" / "TESTS"
TRUTH = REPO / "myhydra" / "single_pdf" / "verifica_pdf" / "per_caso"


def _load_any(path):
    text = Path(path).read_text(encoding="utf-8")
    i = text.find("[")
    j = text.find("{")
    return json.JSONDecoder().raw_decode(
        text, i if i >= 0 and (j < 0 or i < j) else j)[0]


def _reg_of(priv):
    try:
        return struct.unpack("<I", bytes.fromhex(priv[2:10]))[0]
    except Exception:
        return None


def _texton_by_regbit(finale):
    got = {}
    for station in finale:
        priv_by_id = {m.get("ID"): m.get("DRIVERPRIVATE", "")
                      for m in station.get("measures", [])}
        for bit in station.get("bitinfo", []):
            reg = _reg_of(priv_by_id.get(bit.get("MEASUREID"), ""))
            got[(reg, bit.get("BITNO"))] = bit.get("TEXTON", "")
    return got


def _truth_rows(cid):
    truth = json.loads((TRUTH / cid / "tabella_pdf.json").read_text(
        encoding="utf-8"))
    return truth["righe"] if isinstance(truth, dict) else truth


def _score(got, cid):
    total = exact = 0
    for row in _truth_rows(cid):
        vero = (row.get("stato") or row.get("pdf_stato") or "").strip().upper()
        if not vero:
            continue
        total += 1
        if got.get((row.get("registro"), row.get("bit")), "") == vero:
            exact += 1
    return exact, total


def _replay(folder):
    leaves = sorted((TESTS / folder).iterdir(), key=lambda p: p.name)
    merge = [p for p in leaves
             if "MERGE" in p.name.upper() or p.name.upper() == "TAP ABC.TXT"]
    assert merge, folder
    abc = _load_any(merge[0])
    con = consolidate(abc)
    return run_script(SRC, {"stations": con["stations"]})


CASES = [
    ("caso_5_ori_martin_1", "ORI MARTIN 5 NUOVO", 33, 45),
    ("caso_2_protec_1", "PROTEC 1 NUOVO", 29, 36),
    ("caso_8_superwatt_1", "SUPERWATT 8 NUOVO", 47, 59),
]


@pytest.mark.parametrize("cid,folder,floor,total", CASES)
def test_recall_texton_non_peggiora(cid, folder, floor, total):
    exact, counted = _score(_texton_by_regbit(_replay(folder)), cid)
    assert counted == total
    assert exact >= floor


def test_protec_2_frozen_non_peggiora():
    finale = _load_any(TESTS / "PROTEC 2 NUOVO" / "FINALE.txt")
    assert _score(_texton_by_regbit(finale), "caso_3_protec_2") == (6, 22)
