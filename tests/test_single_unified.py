"""Test contract per il prompt unico `vlm_unified_v1.md`."""

from pathlib import Path

REPO = Path(__file__).parent.parent
SRC = REPO / "src" / "prompts" / "vlm_unified_v1.md"
MIRRORS = [
    REPO / "myhydra" / "single_pdf" / "prompt" / "vlm_unified_v1.md",
    REPO / "myhydra" / "single_pdf" / "platforms" / "lv2" / "prompts"
    / "current" / "vlm_unified_v1.md",
]

CAMPI = (
    "description", "units", "modbus_register", "bit", "kind", "data_type",
    "read_write", "note", "state_on", "state_off", "scale_elec_start",
    "scale_elec_end", "scale_eng_start", "scale_eng_end", "limit_hour",
    "limit_day", "zona", "tag", "pagina", "riga",
)


def _flat():
    return " ".join(SRC.read_text(encoding="utf-8").split())


def test_prompt_esiste_e_copie_byte_identiche():
    assert SRC.exists()
    for mirror in MIRRORS:
        assert mirror.read_bytes() == SRC.read_bytes(), mirror


def test_estrattore_unico_senza_rami():
    flat = _flat()
    assert "SINGLE extractor" in flat
    assert "There are no other branches" in flat
    assert "bitnames" not in flat
    assert "bitstates" not in flat


def test_checklist_prima_delle_variabili():
    text = SRC.read_text(encoding="utf-8")
    assert text.index("checklist") < text.index('"righe_viste"')
    flat = _flat()
    assert "write the `checklist`" in flat
    assert "checklist length equals" in flat


def test_schema_unico_con_tutti_i_campi():
    flat = _flat()
    for campo in CAMPI:
        assert '"' + campo + '"' in flat, campo
    assert '"kind": "ANALOGICA"' in flat
    assert "DIGITALE_SINGOLO" in flat
    assert "DIGITALE_IMPACCATO" in flat


def test_regole_che_reggono_i_difetti_chiusi():
    flat = _flat()
    # C3: formato copiato, mai dedotto (V25).
    assert "V25. data_type: copy EXACTLY" in flat
    # V30: bit solo da suffisso/N.Bit.
    assert "V30. BIT SOURCE" in flat
    # V13: fedelta' ai refusi del PDF.
    assert "no typo correction" in flat
    # V3: "Unita" non e' un'unita'.
    assert 'NEVER emit "Unità" or "Unita" as a unit' in flat
    # V26: nessuna rinumerazione dei bit.
    assert "NEVER renumber, NEVER reorder, NEVER interpolate" in flat


def test_riga_indice_fisico_e_buche():
    flat = _flat()
    assert "1-based position of the row in the page top-to-bottom" in flat
    assert "skipped rows included, header excluded" in flat
    assert "leave holes" in flat or "skipped description still gets its checklist turn" in flat


def test_stati_mai_junk():
    flat = _flat()
    assert "NEVER write \"1\" or \"0\" as a state" in flat
    assert 'starting with "0="/ "1=" is junk' in flat


def test_nessun_fence_in_risposta():
    flat = _flat()
    assert "no text before or after, no fences" in flat.lower()
