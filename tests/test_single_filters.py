"""Filtri LV1 Single: scarti V2/V20/V21 conteggiati, mai silenti."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from nodes.single_filters import classify_row


def test_riserva_input_contata_non_silente():
    assert classify_row({"description": "Riserva INPUT", "zona": "INPUT_HW"}) in ("V2", "V21")
    assert classify_row({"description": "COG2: ALLARME FRIGO", "zona": "ALLARMI"}) == "keep"
