"""
Test multi-pagina per src/nodes/json_creator.py (v3).

Esegue lo script iniettando `raw` con diversi input sintetici e valida
che l'output ADAS sia corretto. Non dipende da MyHydra, solo stdlib.

Uso: python3 tests/test_multipage.py

Ogni test produce un report [PASS/FAIL] con breve descrizione.
"""
import json
import re
import sys
import os
import io

SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "..", "src", "nodes", "json_creator.py")
SCRIPT_PATH = os.path.abspath(SCRIPT_PATH)

# --------------------------------------------------------------
# helper: run script with custom `raw` value, return parsed output
# --------------------------------------------------------------
def run_script(raw_value):
    with open(SCRIPT_PATH) as f:
        source = f.read()
    # Rimpiazza l'assegnamento MyHydra-template con un placeholder sicuro
    src2 = re.sub(r"raw\s*=\s*r?'''\{edge\}\[\d+\]'''", "raw = __INJECTED_RAW__", source)
    ns = {"__INJECTED_RAW__": raw_value}
    # sopprimi il print finale per non inquinare stdout
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        exec(src2, ns)
    finally:
        sys.stdout = old_stdout
    out = ns.get("output", "null")
    return json.loads(out)


# --------------------------------------------------------------
# report helper
# --------------------------------------------------------------
passed = 0
failed = 0
def check(name, cond, msg=""):
    global passed, failed
    if cond:
        print("[PASS] " + name)
        passed = passed + 1
    else:
        print("[FAIL] " + name + (" :: " + str(msg) if msg else ""))
        failed = failed + 1


# --------------------------------------------------------------
# fixture builders
# --------------------------------------------------------------
def make_vlm_chunk(name, ip, port, modbus_id, variables):
    """Costruisce un chunk VLM (una pagina) con la struttura del contratto."""
    return {"stations": [{
        "name": name,
        "protocol": "ModBus TCP",
        "ip": ip,
        "port": port,
        "modbus_id": modbus_id,
        "variables": variables
    }]}

def ana(desc, reg, units="mA", e_start=None, e_end=None, g_start=None, g_end=None):
    return {
        "description": desc, "units": units,
        "modbus_register": reg, "bit": None,
        "kind": "ANALOGICA", "read_write": "R",
        "state_on": None, "state_off": None,
        "scale_elec_start": e_start, "scale_elec_end": e_end,
        "scale_eng_start": g_start, "scale_eng_end": g_end,
        "limit_hour": None, "limit_day": None
    }

def digit_single(desc, reg, rw="R"):
    return {
        "description": desc, "units": None,
        "modbus_register": reg, "bit": None,
        "kind": "DIGITALE_SINGOLO", "read_write": rw,
        "state_on": None, "state_off": None,
        "scale_elec_start": None, "scale_elec_end": None,
        "scale_eng_start": None, "scale_eng_end": None,
        "limit_hour": None, "limit_day": None
    }

def digit_packed(desc, reg, bit):
    return {
        "description": desc, "units": None,
        "modbus_register": reg, "bit": bit,
        "kind": "DIGITALE_IMPACCATO", "read_write": "R",
        "state_on": None, "state_off": None,
        "scale_elec_start": None, "scale_elec_end": None,
        "scale_eng_start": None, "scale_eng_end": None,
        "limit_hour": None, "limit_day": None
    }


# ==================================================================
# TEST 1: compatibilita' backward (singola pagina, come v2)
# ==================================================================
chunk = make_vlm_chunk("E1", "192.168.0.1", 502, 1, [
    ana("Temperatura fumi", 40001, units="°C"),
    ana("Pressione caldaia", 40002, units="mbar"),
    digit_single("Allarme generale", 40010)
])
out = run_script(json.dumps(chunk))
check("T1 - singola pagina: 1 stazione", len(out) == 1)
check("T1 - nome stazione", out[0]["NAME"] == "E1")
check("T1 - IP in DRIVERCONFIG", "192.168.0.1" in out[0]["DRIVERCONFIG"])
check("T1 - 3 misure", len(out[0]["measures"]) == 3)
check("T1 - 1 bitinfo (singolo BITNO=0)", len(out[0]["bitinfo"]) == 1
      and out[0]["bitinfo"][0]["BITNO"] == 0)


# ==================================================================
# TEST 2: multi-pagina con forward-fill
#   pagina 1: ha nome, ip, port, modbus_id + 2 variabili
#   pagina 2: name=null, ip=null + 3 variabili -> deve ereditare
#   pagina 3: name=null, ip=null + 1 variabile -> deve ereditare
# ==================================================================
p1 = make_vlm_chunk("E1", "10.0.0.5", 502, 7, [
    ana("Temp camera", 40001, units="°C"),
    ana("Press camera", 40002, units="mbar")
])
p2 = make_vlm_chunk(None, None, None, None, [
    ana("Umidita", 40003, units="%"),
    ana("Flusso gas", 40004, units="Nm3/h"),
    ana("Livello", 40005, units="%")
])
p3 = make_vlm_chunk(None, None, None, None, [
    ana("Temperatura scambiatore", 40010, units="°C")
])
raw_concat = json.dumps(p1) + json.dumps(p2) + json.dumps(p3)
out = run_script(raw_concat)
check("T2 - 1 sola stazione (non 3)", len(out) == 1, msg="got " + str(len(out)))
check("T2 - nome forward-fill = E1", out[0]["NAME"] == "E1")
check("T2 - IP forward-fill 10.0.0.5", "10.0.0.5" in out[0]["DRIVERCONFIG"])
check("T2 - 6 misure totali", len(out[0]["measures"]) == 6,
      msg="got " + str(len(out[0]["measures"])))
check("T2 - meta: 3 chunks", out[0]["_meta"]["chunks_parsed"] == 3)


# ==================================================================
# TEST 3: pagina vuota (frontespizio) NON crea stazione spuria
# ==================================================================
cover = {"stations": []}
real = make_vlm_chunk("SAE-1", "172.16.0.1", 502, 2, [
    ana("SO2", 40001, units="mg/Nm3")
])
raw_concat = json.dumps(cover) + json.dumps(real)
out = run_script(raw_concat)
check("T3 - 1 sola stazione (frontespizio skippato)", len(out) == 1)
check("T3 - nome = SAE-1", out[0]["NAME"] == "SAE-1")


# ==================================================================
# TEST 4: documento con 2 IP REALI -> 2 stazioni separate
# ==================================================================
p1 = make_vlm_chunk("E1", "192.168.1.10", 502, 1, [
    ana("Temp1", 40001, units="°C")
])
p2 = make_vlm_chunk("E2", "192.168.1.20", 502, 2, [
    ana("Temp2", 40001, units="°C")
])
raw_concat = json.dumps(p1) + json.dumps(p2)
out = run_script(raw_concat)
check("T4 - 2 stazioni (multi-IP)", len(out) == 2,
      msg="got " + str(len(out)))
names = [o["NAME"] for o in out]
check("T4 - nomi E1 e E2", sorted(names) == ["E1", "E2"])
check("T4 - IP distinti nei DRIVERCONFIG",
      any("192.168.1.10" in o["DRIVERCONFIG"] for o in out)
      and any("192.168.1.20" in o["DRIVERCONFIG"] for o in out))


# ==================================================================
# TEST 5: IP placeholder (xxx.xxx.xxx.xxx) -> stazione separata
#   (regola S8 del prompt VLM)
# ==================================================================
p1 = make_vlm_chunk("E1", "10.0.0.1", 502, 1, [
    ana("Temp1", 40001, units="°C")
])
p2 = make_vlm_chunk(None, "xxx.xxx.xxx.xxx", 502, None, [
    ana("Parametro futuro", 40100, units="%")
])
raw_concat = json.dumps(p1) + json.dumps(p2)
out = run_script(raw_concat)
check("T5 - 2 stazioni (real + placeholder)", len(out) == 2)
ips = []
for o in out:
    if "10.0.0.1" in o["DRIVERCONFIG"]:
        ips.append("real")
    if "xxx.xxx.xxx.xxx" in o["DRIVERCONFIG"]:
        ips.append("placeholder")
check("T5 - entrambi gli IP preservati", sorted(ips) == ["placeholder", "real"])


# ==================================================================
# TEST 6: digitali impacchettati a cavallo di pagina
#   pagina 1: registro 40001, bit 0..7
#   pagina 2: registro 40001, bit 8..15 (stessa stazione)
#   -> deve produrre 1 sola measure "Ingressi digitali 1" con 16 bitinfo
# ==================================================================
p1_vars = [digit_packed("Bit " + str(b), 40001, b) for b in range(8)]
p2_vars = [digit_packed("Bit " + str(b), 40001, b) for b in range(8, 16)]
p1 = make_vlm_chunk("PLC", "10.0.0.1", 502, 1, p1_vars)
p2 = make_vlm_chunk(None, None, None, None, p2_vars)
raw_concat = json.dumps(p1) + json.dumps(p2)
out = run_script(raw_concat)
check("T6 - 1 stazione", len(out) == 1)
check("T6 - 1 misura impacchettata", len(out[0]["measures"]) == 1,
      msg="got " + str(len(out[0]["measures"])))
check("T6 - misura = 'Ingressi digitali 1'",
      out[0]["measures"][0]["NAME"] == "Ingressi digitali 1")
check("T6 - 16 bitinfo (bit 0..15)", len(out[0]["bitinfo"]) == 16,
      msg="got " + str(len(out[0]["bitinfo"])))
bitnos = sorted([b["BITNO"] for b in out[0]["bitinfo"]])
check("T6 - bit 0..15 tutti presenti", bitnos == list(range(16)),
      msg="got " + str(bitnos))


# ==================================================================
# TEST 7: dedup bitinfo quando stessa (MEASUREID, BITNO) duplicata
#   (caso di header ripetuti / riga duplicata a cavallo di pagina)
# ==================================================================
p1 = make_vlm_chunk("PLC", "10.0.0.1", 502, 1, [
    digit_packed("Allarme A", 40001, 0),
    digit_packed("Allarme B", 40001, 1),
])
p2 = make_vlm_chunk(None, None, None, None, [
    digit_packed("Allarme A", 40001, 0),   # DUPLICATO
    digit_packed("Allarme C", 40001, 2),
])
raw_concat = json.dumps(p1) + json.dumps(p2)
out = run_script(raw_concat)
check("T7 - 1 sola misura", len(out[0]["measures"]) == 1)
check("T7 - 3 bitinfo dopo dedup (A, B, C)",
      len(out[0]["bitinfo"]) == 3,
      msg="got " + str(len(out[0]["bitinfo"])))


# ==================================================================
# TEST 8: formato JSONL (un JSON per riga)
# ==================================================================
p1 = make_vlm_chunk("E1", "10.0.0.1", 502, 1, [ana("A", 40001, units="mA")])
p2 = make_vlm_chunk(None, None, None, None, [ana("B", 40002, units="mA")])
raw_jsonl = json.dumps(p1) + "\n" + json.dumps(p2)
out = run_script(raw_jsonl)
check("T8 - JSONL: 1 stazione, 2 misure",
      len(out) == 1 and len(out[0]["measures"]) == 2)


# ==================================================================
# TEST 9: formato array JSON esterno  [{...}, {...}]
# ==================================================================
p1 = make_vlm_chunk("E1", "10.0.0.1", 502, 1, [ana("A", 40001, units="mA")])
p2 = make_vlm_chunk(None, None, None, None, [ana("B", 40002, units="mA")])
raw_arr = json.dumps([p1, p2])
out = run_script(raw_arr)
check("T9 - array esterno: 1 stazione, 2 misure",
      len(out) == 1 and len(out[0]["measures"]) == 2)


# ==================================================================
# TEST 10: gia' parsato (MyHydra inietta oggetto/lista)
# ==================================================================
p1 = make_vlm_chunk("E1", "10.0.0.1", 502, 1, [ana("A", 40001, units="mA")])
p2 = make_vlm_chunk(None, None, None, None, [ana("B", 40002, units="mA")])
out = run_script([p1, p2])  # oggetto Python, non stringa
check("T10 - iniezione lista dict: 1 stazione, 2 misure",
      len(out) == 1 and len(out[0]["measures"]) == 2)


# ==================================================================
# TEST 11: comando Write -> DRIVERDATA=5
# ==================================================================
p1 = make_vlm_chunk("E1", "10.0.0.1", 502, 1, [
    digit_single("Valvola comando", 40100, rw="W")
])
out = run_script(json.dumps(p1))
m = out[0]["measures"][0]
check("T11 - Write -> DRIVERDATA=5", m["DRIVERDATA"] == 5,
      msg="got " + str(m["DRIVERDATA"]))


# ==================================================================
# TEST 12: documento senza IP -> warning + default 127.0.0.1
# ==================================================================
p1 = make_vlm_chunk("E1", None, 502, 1, [ana("A", 40001, units="mA")])
p2 = make_vlm_chunk(None, None, None, None, [ana("B", 40002, units="mA")])
raw_concat = json.dumps(p1) + json.dumps(p2)
out = run_script(raw_concat)
check("T12 - 1 stazione, IP default", len(out) == 1 and "127.0.0.1" in out[0]["DRIVERCONFIG"])
check("T12 - _warnings presente", "_warnings" in out[0] and len(out[0]["_warnings"]) > 0)


# ==================================================================
# TEST 13: rinomina stazioni omonime con IP diversi
# ==================================================================
p1 = make_vlm_chunk("SME", "10.0.0.1", 502, 1, [ana("A", 40001, units="mA")])
p2 = make_vlm_chunk("SME", "10.0.0.2", 502, 1, [ana("B", 40001, units="mA")])
raw_concat = json.dumps(p1) + json.dumps(p2)
out = run_script(raw_concat)
check("T13 - 2 stazioni (stesso nome, IP diversi)", len(out) == 2)


# ==================================================================
# TEST 14: input vuoto -> DEBUG
# ==================================================================
out = run_script("")
check("T14 - input vuoto: DEBUG", isinstance(out, dict) and out.get("DEBUG") is True)


# ==================================================================
# TEST 15: input garbage -> DEBUG
# ==================================================================
out = run_script("questo non e' json e non ha parentesi graffe")
check("T15 - garbage: DEBUG", isinstance(out, dict) and out.get("DEBUG") is True)


# ==================================================================
# report finale
# ==================================================================
print("")
print("=" * 50)
print("RESULT: " + str(passed) + " passed, " + str(failed) + " failed")
print("=" * 50)
if failed > 0:
    sys.exit(1)
