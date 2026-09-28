#!/usr/bin/env python3
"""Runner per testare json_creator.py contro una fixture VLM reale.

Uso: python3 tests/run_fixture.py <path_fixture.json>

Carica il fixture come lista di chunk (come MyHydra inietterebbe via edge[3]),
poi inietta il dato in json_creator.py sostituendo `raw = r'''{edge}[3]'''`
con la lista Python vera. Stampa stdout (il payload ADAS) e un report
riepilogativo alla fine.
"""
import sys
import json
import subprocess
import os
import re

if len(sys.argv) < 2:
    print("Uso: python3 tests/run_fixture.py <fixture.json>")
    sys.exit(1)

fixture_path = sys.argv[1]
with open(fixture_path, "r", encoding="utf-8") as f:
    fixture = json.load(f)

# Leggi json_creator.py come testo
creator_path = os.path.join(os.path.dirname(__file__), "..", "src", "nodes", "json_creator.py")
with open(creator_path, "r", encoding="utf-8") as f:
    src = f.read()

# Sostituisci la riga di placeholder con il dato reale
# La riga originale e': raw = r'''{edge}[4]''' (o {edge}[3])
# La sostituiamo con: raw = <repr della fixture>
src_mod = re.sub(r"raw\s*=\s*r?'''\{edge\}\[\d+\]'''", "raw = " + repr(fixture), src)

# Scrivi il sorgente modificato in un file temporaneo
tmp = "/tmp/json_creator_run.py"
with open(tmp, "w", encoding="utf-8") as f:
    f.write(src_mod)

# Esegui
result = subprocess.run(["python3", tmp], capture_output=True, text=True)
stdout = result.stdout
stderr = result.stderr

print("=== STDOUT ===")
print(stdout)
if stderr:
    print("=== STDERR ===")
    print(stderr)

# Report compatto
try:
    out = json.loads(stdout)
except Exception as e:
    print("ERRORE parsing output:", e)
    sys.exit(2)

if isinstance(out, list):
    print("\n=== REPORT ===")
    print("Numero stazioni output:", len(out))
    idx = 0
    total_vars = 0
    total_bits = 0
    while idx < len(out):
        st = out[idx]
        nm = st.get("NAME", "?")
        drv = st.get("DRIVERCONFIG", "")
        # estrai IP da DRIVERCONFIG
        ip = "?"
        try:
            i1 = drv.find('ipaddress="') + 11
            i2 = drv.find('"', i1)
            ip = drv[i1:i2]
        except Exception:
            pass
        try:
            j1 = drv.find('tcpport="') + 9
            j2 = drv.find('"', j1)
            port = drv[j1:j2]
        except Exception:
            port = "?"
        n_m = len(st.get("measures", []))
        n_b = len(st.get("bitinfo", []))
        total_vars = total_vars + n_m
        total_bits = total_bits + n_b
        print(f"  Stazione {idx+1}: NAME={nm!r}  IP={ip}  port={port}  measures={n_m}  bitinfo={n_b}")
        idx = idx + 1
    print(f"TOTALI: measures={total_vars}  bitinfo={total_bits}")
    if len(out) > 0 and "_warnings" in out[0]:
        print("WARNINGS:", out[0]["_warnings"])
    if len(out) > 0 and "_meta" in out[0]:
        print("META:", out[0]["_meta"])
else:
    print("Output non e' una lista (DEBUG?):", out)
