"""Prompt VLM Single a 3 rami v14: regole chiave presenti per file (non LLM)."""

import pathlib


def test_tre_prompt_con_regole_chiave():
    import pathlib
    base = pathlib.Path("src/prompts")
    assert "tag" in (base / "vlm_measures_v14.md").read_text()
    assert "V23" in (base / "vlm_bitnames_v14.md").read_text()
    assert "state_on" in (base / "vlm_bitstates_v14.md").read_text()


def test_rami_separati_e_tracciabilita_v14():
    base = pathlib.Path("src/prompts")
    measures = (base / "vlm_measures_v14.md").read_text()
    bitnames = (base / "vlm_bitnames_v14.md").read_text()
    bitstates = (base / "vlm_bitstates_v14.md").read_text()
    # Ramo misure: tag + tracciabilita v14 + scarti unificati, nessuno stato.
    assert "zona" in measures
    assert "pagina" in measures
    assert "riga" in measures
    assert "V2" in measures and "V20" in measures and "V21" in measures
    assert "state_on" not in measures
    # Ramo nomi-bit: fedelta bit V23/V26, solo registro/bit/descrizione.
    assert "V26" in bitnames
    assert "modbus_register" in bitnames
    assert "state_on" not in bitnames
    assert "limit_hour" not in bitnames
    # Ramo stati: solo copie esatte V7/V8, mai registro.
    assert "state_off" in bitstates
    assert "V7" in bitstates
    assert "modbus_register" not in bitstates


def test_stati_sparsi_v15_solo_righe_valorizzate():
    base = pathlib.Path("src/prompts")
    v15 = (base / "vlm_bitstates_v15.md").read_text()
    assert "V27" in v15
    assert "D7" in v15
    assert "state_off" in v15
    assert "modbus_register" not in v15
    current = pathlib.Path(
        "myhydra/single_pdf/platforms/lv2/prompts/current/"
        "vlm_bitstates_v15.md").read_text()
    assert current == v15
