#!/usr/bin/env python3
"""Runner per testare src/nodes/json_creator.py con un fixture realistico.

Sostituisce il placeholder `{edge}[3]` con il contenuto JSON del fixture
ed esegue lo script esattamente come farebbe MyHydra.
"""
import sys
import os

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(PROJ, "src", "nodes", "json_creator.py")

fixture = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    PROJ, "data", "test_inputs", "vlm_raw", "PROTEC_1_2pages.json")

with open(fixture, "r", encoding="utf-8") as f:
    fixture_text = f.read()

with open(SCRIPT, "r", encoding="utf-8") as f:
    script = f.read()

# Sostituisce il placeholder MyHydra con il JSON reale come stringa Python
replacement = "r'''" + fixture_text.replace("\\", "\\\\").replace("'", "\\'") + "'''"
script_replaced = script.replace("r'''{edge}[3]'''", replacement)

# Esegue lo script con lo stdout catturato
exec(compile(script_replaced, SCRIPT, "exec"), {"__name__": "__main__"})
