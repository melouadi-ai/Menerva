"""Test contract per il prompt oracolo vlm_oracle_v1.md."""

from pathlib import Path

SRC = Path(__file__).parent.parent / "src" / "prompts" / "vlm_oracle_v1.md"
PLATFORM = (Path(__file__).parent.parent / "myhydra" / "single_pdf"
            / "platforms" / "lv2" / "prompts" / "current"
            / "vlm_oracle_v1.md")
PYTOOLS = (Path(__file__).parent.parent / "myhydra" / "single_pdf"
           / "prompt" / "vlm_oracle_v1.md")


def _flat(path):
    return path.read_text(encoding="utf-8")


def test_prompt_esiste():
    assert SRC.exists()
    assert PLATFORM.exists()
    assert PYTOOLS.exists()


def test_regole_presenti():
    flat = _flat(SRC)
    assert "R1. MANCANTI" in flat
    assert "R2. UNITA INVENTATE" in flat
    assert "R3. JUNK STATI" in flat
    assert "R4. REFUSI CORRETTI" in flat
    assert "R5. IP DICHIARATI NON USATI" in flat


def test_mai_sovrascrivere():
    flat = _flat(SRC)
    assert "never rewrite" in flat
    assert "never correct" in flat
    assert "Never invent" in flat


def test_evidenza_obbligatoria():
    flat = _flat(SRC)
    assert "evidenza" in flat
    assert "D5. Never emit a discrepancy without `evidenza`" in flat


def test_junk_patterns():
    flat = _flat(SRC)
    assert '"1"' in flat
    assert '"0"' in flat
    assert '"1="' in flat
    assert '"0="' in flat


def test_copie_byte_identiche():
    src = SRC.read_bytes()
    assert PLATFORM.read_bytes() == src
    assert PYTOOLS.read_bytes() == src


def test_schema_output():
    flat = _flat(SRC)
    assert '"mancanti"' in flat
    assert '"unita_inventate"' in flat
    assert '"junk_stati"' in flat
    assert '"refusi_corretti"' in flat
    assert '"ip_dichiarati_non_usati"' in flat


def test_self_check():
    flat = _flat(SRC)
    assert "SELF-CHECK" in flat
    assert "If any check fails, remove the entry" in flat


def test_regola_r0_context_gate():
    """L'oracolo riceve il JSON di UNIFIED nel Context: senza, non puo'
    verificare nulla e deve dirlo, non inventare."""
    flat = _flat(SRC)
    assert "R0. CONTEXT GATE" in flat
    assert "delivered in the" in flat and "Context" in flat
    assert "errore_input" in flat
    assert "Never guess the extraction" in flat
