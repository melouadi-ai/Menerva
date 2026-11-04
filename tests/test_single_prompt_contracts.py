"""Prompt LV2 storici (3 rami): regole chiave + un solo posto per versione.

Regressione: measures numerava le sole emesse, stati le sopravvissute
incluse le omesse -> join posizionale shiftato (PROTEC 1/2, SIEMENS).
Da qui in poi `riga` e' l'indice fisico di riga ovunque.

Dopo la riorganizzazione del 4/11/2026 i prompt dei 3 rami vivono **solo**
in `src/prompts/archive/`: sono riferimento storico, non si incollano piu'.
I due prompt correnti (UNIFIED, ORACOLO) restano in `src/prompts/` e hanno
una copia di paste in `myhydra/single_pdf/prompt/`.
"""
from pathlib import Path

REPO = Path(__file__).parent.parent
PROMPTS = REPO / "src" / "prompts" / "archive"
PASTE = REPO / "myhydra" / "single_pdf" / "prompt"

ABSOLUTE = "counting EVERY data row INCLUDING V2/V20/V21-skipped rows"

HISTORICAL = ("vlm_measures_v14.md", "vlm_measures_v15.md",
              "vlm_measures_v16.md", "vlm_measures_v17.md",
              "vlm_measures_v18.md", "vlm_bitnames_v14.md",
              "vlm_bitnames_v15.md", "vlm_bitnames_v16.md",
              "vlm_bitstates_v14.md", "vlm_bitstates_v15.md",
              "vlm_bitstates_v16.md", "vlm_bitstates_v17.md",
              "vlm_bitstates_v18.md", "vlm_bitstates_v19.md",
              "vlm_extraction_v11.md", "vlm_extraction_v12.md",
              "vlm_extraction_v13.md")


def _flat(name):
    text = (PROMPTS / name).read_text(encoding="utf-8")
    return " ".join(text.split())


def test_storico_vive_solo_nell_archivio():
    for name in HISTORICAL:
        assert (PROMPTS / name).is_file(), name
        assert not (REPO / "src" / "prompts" / name).exists(), name
        assert not (PASTE / name).exists(), name


def test_prompt_correnti_copia_di_paste_identica():
    for name in ("vlm_unified_v1.md", "vlm_oracle_v1.md"):
        assert ((REPO / "src" / "prompts" / name).read_bytes()
                == (PASTE / name).read_bytes()), name


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


def test_stati_v18_scan_in_cima():
    text = (PROMPTS / "vlm_bitstates_v18.md").read_text(encoding="utf-8")
    flat = " ".join(text.split())
    assert text.index("## SCAN") < text.index("## OBJECTIVE")
    assert "For EACH address" in flat
    assert "ANCHORED ROW SCAN" not in text


def test_stati_v19_checklist_prima_degli_stati():
    text = (PROMPTS / "vlm_bitstates_v19.md").read_text(encoding="utf-8")
    flat = " ".join(text.split())
    assert text.index("checklist") < text.index('"rows"')
    assert "write it FIRST, before reading a single state cell" in flat


def test_misure_v16_checklist_prima_delle_variabili():
    text = (PROMPTS / "vlm_measures_v16.md").read_text(encoding="utf-8")
    flat = " ".join(text.split())
    assert text.index("checklist") < text.index('"stations"')
    assert "write the `checklist`" in flat
    assert "righe_viste" in text


def test_bit_source_vieta_coil():
    flat = " ".join((PROMPTS / "vlm_measures_v17.md")
                    .read_text(encoding="utf-8").split())
    bitnames = " ".join((PROMPTS / "vlm_bitnames_v16.md")
                        .read_text(encoding="utf-8").split())
    assert "V23" in bitnames
    assert "BIT FIDELITY" in bitnames
    assert flat


def test_misure_v18_vieta_variabili_senza_descrizione():
    flat = " ".join((PROMPTS / "vlm_measures_v18.md")
                    .read_text(encoding="utf-8").split())
    assert "Never emit a variable for a bare register" in flat
