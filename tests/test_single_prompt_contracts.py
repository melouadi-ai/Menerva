"""Prompt LV2: il contratto `riga` e' identico nei 3 rami + fedelta' refusi.

Regressione: measures numerava le sole emesse, stati le sopravvissute
incluse le omesse -> join posizionale shiftato (PROTEC 1/2, SIEMENS).
Da qui in poi `riga` e' l'indice fisico di riga ovunque.
"""
from pathlib import Path

PROMPTS = Path(__file__).parent.parent / "src" / "prompts"

ABSOLUTE = "counting EVERY data row INCLUDING V2/V20/V21-skipped rows"


def _flat(name):
    text = (PROMPTS / name).read_text(encoding="utf-8")
    return " ".join(text.split())


def test_riga_assoluta_nei_tre_rami():
    for name in ("vlm_measures_v14.md", "vlm_bitnames_v14.md",
                 "vlm_bitstates_v15.md"):
        text = _flat(name)
        assert ABSOLUTE in text, name
        assert "leave holes" in text, name


def test_fedelta_refusi_nel_ramo_misure():
    text = (PROMPTS / "vlm_measures_v14.md").read_text(encoding="utf-8")
    assert "Ossiegno" in text
    assert "correction is forbidden" in text
    assert "nothing dropped at the end" in text


def test_chiave_descrittiva_negli_stati():
    text = _flat("vlm_bitstates_v15.md")
    assert "DESCRIPTION CHECK-KEY" in text
    assert '"description"' in text


def test_stati_v16_catalogo_header_e_conteggi():
    text = (PROMPTS / "vlm_bitstates_v16.md").read_text(encoding="utf-8")
    flat = " ".join(text.split())
    assert "STATO 1" in text
    assert "ON TEXT" in text
    assert "digitali_visti" in text
    assert "never a state, even when it looks like one" in flat
    for mirror in ("myhydra/single_pdf/prompt/vlm_bitstates_v16.md",
                   "myhydra/single_pdf/platforms/lv2/prompts/current/vlm_bitstates_v16.md"):
        assert (Path(__file__).parent.parent / mirror).read_bytes() == (
            PROMPTS / "vlm_bitstates_v16.md").read_bytes()


def test_misure_nomi_v15_riga_e_checkkey():
    for name in ("vlm_measures_v15.md", "vlm_bitnames_v15.md"):
        flat = " ".join((PROMPTS / name).read_text(encoding="utf-8").split())
        assert "riga 0, not 1" in flat, name
        assert "never restarted" in flat, name


def test_stati_v17_anchored_row_scan():
    text = (PROMPTS / "vlm_bitstates_v17.md").read_text(encoding="utf-8")
    flat = " ".join(text.split())
    assert "ANCHORED ROW SCAN" in text
    assert "never scan the page freeform" in flat
    assert "between \"=\" and the ModBus address" in flat
    for mirror in ("myhydra/single_pdf/prompt/vlm_bitstates_v17.md",
                   "myhydra/single_pdf/platforms/lv2/prompts/current/vlm_bitstates_v17.md"):
        assert (Path(__file__).parent.parent / mirror).read_bytes() == (
            PROMPTS / "vlm_bitstates_v17.md").read_bytes()


def test_stati_v18_scan_in_cima():
    text = (PROMPTS / "vlm_bitstates_v18.md").read_text(encoding="utf-8")
    flat = " ".join(text.split())
    assert text.index("## SCAN") < text.index("## OBJECTIVE")
    assert "For EACH address" in flat
    assert "ANCHORED ROW SCAN" not in text
    for mirror in ("myhydra/single_pdf/prompt/vlm_bitstates_v18.md",
                   "myhydra/single_pdf/platforms/lv2/prompts/current/vlm_bitstates_v18.md"):
        assert (Path(__file__).parent.parent / mirror).read_bytes() == (
            PROMPTS / "vlm_bitstates_v18.md").read_bytes()
