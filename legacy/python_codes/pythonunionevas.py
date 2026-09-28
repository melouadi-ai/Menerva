"""
plc_merger_strings.py
=====================
Merges the string outputs of the five Qwen models into the final
station/measures/bitinfo structure required by the PLC monitoring system.

No functions, no classes — pure sequential imperative code.

MODEL ROLES:
  M1 — Stations (one per distinct IP)
  M2 — Analog / WORD measures only        (DRIVERDATA=0, TYPE=0)
  M3 — Single digital + Packed digital    (DRIVERDATA=1,TYPE=6  OR  DRIVERDATA=2,TYPE=1)
  M4 — Bitinfo entries (packed bits only)
  M5 — NAME / UNITS lookup table

INPUTS: assign the raw string output from each model to the five variables
        below (M1_STRING … M5_STRING).

OUTPUT: the variable `result` holds the final list of station dicts,
        ready for json.dumps() or direct use.
"""

import json
import re
from copy import deepcopy

# ---------------------------------------------------------------------------
# CONFIGURATION — paste each model's raw string output here
# ---------------------------------------------------------------------------

M1_STRING = r"""{edge}[14]"""   # Stations

M2_STRING = r"""{edge}[13]"""   # Analogs (DRIVERDATA=0)

M3_STRING = r"""{edge}[12]"""   # Single digital (DRIVERDATA=1) + Packed (DRIVERDATA=2)

M4_STRING = r"""{edge}[11]"""   # Bitinfo

M5_STRING = r"""{edge}[10]"""   # Names lookup

# ---------------------------------------------------------------------------
# STEP 0 — Parse all five model strings
# Markdown fences are stripped automatically.
# ---------------------------------------------------------------------------

_raw_text_m1 = M1_STRING.strip()
_raw_text_m1 = re.sub(r"^```(?:json)?\s*", "", _raw_text_m1)
_raw_text_m1 = re.sub(r"\s*```$", "", _raw_text_m1)
m1 = json.loads(_raw_text_m1)

_raw_text_m2 = M2_STRING.strip()
_raw_text_m2 = re.sub(r"^```(?:json)?\s*", "", _raw_text_m2)
_raw_text_m2 = re.sub(r"\s*```$", "", _raw_text_m2)
m2 = json.loads(_raw_text_m2)

_raw_text_m3 = M3_STRING.strip()
_raw_text_m3 = re.sub(r"^```(?:json)?\s*", "", _raw_text_m3)
_raw_text_m3 = re.sub(r"\s*```$", "", _raw_text_m3)
m3 = json.loads(_raw_text_m3)

_raw_text_m4 = M4_STRING.strip()
_raw_text_m4 = re.sub(r"^```(?:json)?\s*", "", _raw_text_m4)
_raw_text_m4 = re.sub(r"\s*```$", "", _raw_text_m4)
m4 = json.loads(_raw_text_m4)

_raw_text_m5 = M5_STRING.strip()
_raw_text_m5 = re.sub(r"^```(?:json)?\s*", "", _raw_text_m5)
_raw_text_m5 = re.sub(r"\s*```$", "", _raw_text_m5)
m5 = json.loads(_raw_text_m5)

_m3_analog_leaked   = [x for x in m3 if x.get("DRIVERDATA") == 0]
_m3_single_digital  = [x for x in m3 if x.get("DRIVERDATA") == 1]
_m3_packed          = [x for x in m3 if x.get("DRIVERDATA") == 2]

print(f"[INFO] Loaded — M1:{len(m1)} stations | M2:{len(m2)} analogs | "
      f"M3:{len(m3)} total ({len(_m3_single_digital)} single-digital, "
      f"{len(_m3_packed)} packed, {len(_m3_analog_leaked)} analog-leaked) | "
      f"M4:{len(m4)} bits | M5:{len(m5)} names")

if _m3_analog_leaked:
    print(f"[WARN] M3 contains {len(_m3_analog_leaked)} analog rows (DRIVERDATA=0) — "
          f"they will be ignored. These should come from M2.")

# ---------------------------------------------------------------------------
# STEP 1 — Build station map from Model 1
# ---------------------------------------------------------------------------

stations = {}

for _raw_station in m1:
    _sid = int(_raw_station["ID"])
    _cfg = _raw_station.get("DRIVERCONFIG", ":")
    _ip_part = _cfg.split(":")[0] if ":" in _cfg else _cfg
    _ip_norm = _ip_part.replace(",", ".").strip()

    stations[_sid] = {
        "NAME":         _raw_station.get("NAME", "SME"),
        "DRIVERNAME":   _raw_station.get("DRIVERNAME", "modbusplc"),
        "DRIVERCONFIG": _cfg,
        "ID":           _sid,
        "_ip":          _ip_norm,
        "measures":     [],
        "bitinfo":      [],
    }

print(f"[INFO] Stations found: {len(stations)}")

# ---------------------------------------------------------------------------
# STEP 2 — Build NAME / UNITS lookup table from Model 5
# ---------------------------------------------------------------------------

name_lookup = {}

for _entry in m5:
    _raw_key = _entry.get("RAW", "").strip().lower()
    name_lookup[_raw_key] = {
        "NAME":  _entry.get("NAME"),
        "UNITS": _entry.get("UNITS"),
    }

print(f"[INFO] Name lookup entries: {len(name_lookup)}")

# ---------------------------------------------------------------------------
# STEP 3 — Shared NAME normalisation (inline, applied to any raw name)
# ---------------------------------------------------------------------------

SKIP_DESCRIPTIONS = {
    "available", "disponibile", "not used", "reserve",
    "spare", "input", "output", "parameter",
}

# ---------------------------------------------------------------------------
# STEP 4 — Process ANALOG measures from Model 2  (DRIVERDATA=0, TYPE=0)
# ---------------------------------------------------------------------------

all_measures = []

print(f"[INFO] Analog measures (M2): {len(m2)}")

for _raw_m in m2:

    _desc = _raw_m.get("NAME")
    if _desc is None:
        continue
    _desc_lower = _desc.strip().lower()
    if _desc_lower in SKIP_DESCRIPTIONS:
        continue
    if "disponibile" in _desc_lower:
        continue

    _m = deepcopy(_raw_m)
    _raw_name = _m.get("NAME", "")
    _lookup_key = _raw_name.strip().lower()

    if _lookup_key in name_lookup and name_lookup[_lookup_key]["NAME"] is not None:
        _m["NAME"] = name_lookup[_lookup_key]["NAME"]
    else:
        _n = _raw_name
        _n = re.sub(r"\([^)]*\)", "", _n)
        _n = re.sub(r"\[[^\]]*\]", "", _n)
        _n = _n.strip()
        _n = re.sub(r"\b(di|del|della|in|da|per|con)\b", "", _n, flags=re.IGNORECASE).strip()
        _n = re.sub(r"\s{2,}", " ", _n)
        if len(_n) > 25: _n = re.sub(r"\bAnalizzatore\b", "Anal.",   _n, flags=re.IGNORECASE)
        if len(_n) > 25: _n = re.sub(r"\bConvertitore\b", "Conv.",   _n, flags=re.IGNORECASE)
        if len(_n) > 25: _n = re.sub(r"\bManutenzione\b", "Manut.",  _n, flags=re.IGNORECASE)
        if len(_n) > 25: _n = re.sub(r"\bCalibrazione\b", "Calib.",  _n, flags=re.IGNORECASE)
        if len(_n) > 25: _n = re.sub(r"\bTemperatura\b",  "Temp.",   _n, flags=re.IGNORECASE)
        if len(_n) > 25: _n = re.sub(r"\bCollegamento\b", "Colleg.", _n, flags=re.IGNORECASE)
        if len(_n) > 25: _n = re.sub(r"\bComunicazione\b","Comm.",   _n, flags=re.IGNORECASE)
        if len(_n) > 25: _n = re.sub(r"\bOssigeno\b",     "O2",      _n, flags=re.IGNORECASE)
        if len(_n) > 25: _n = re.sub(r"\bAllarme\b",      "All.",    _n, flags=re.IGNORECASE)
        if len(_n) > 25: _n = re.sub(r"\brichiesta\b",    "rich.",   _n, flags=re.IGNORECASE)
        if len(_n) > 25: _n = re.sub(r"\bpresenza\b",     "pres.",   _n, flags=re.IGNORECASE)
        if len(_n) > 25: _n = re.sub(r"\bComando\b",      "Cmd",     _n, flags=re.IGNORECASE)
        _n = _n[:25].strip()
        _m["NAME"] = _n

    _declared_units = _m.get("UNITS")
    if _declared_units is None:
        _uk = _raw_name.strip().lower()
        if _uk in name_lookup:
            _m["UNITS"] = name_lookup[_uk]["UNITS"]

    # Force analog type
    _m["DRIVERDATA"] = 0
    _m["TYPE"]       = 0

    if "MODBUSREGISTRO" not in _m:
        _m["MODBUSREGISTRO"] = None
    _reg = _m["MODBUSREGISTRO"]
    # Coil strings with leading zeros must stay strings; plain integers stay int
    if isinstance(_reg, str) and re.match(r"^[1-9]\d*$", _reg):
        _m["MODBUSREGISTRO"] = int(_reg)

    try:
        _sid = int(_raw_m.get("STATIONID", 1))
    except (TypeError, ValueError):
        _sid = 1
    if _sid not in stations:
        _sid = min(stations.keys())
    _m["STATIONID"] = _sid
    _m.pop("_raw_desc", None)

    all_measures.append(_m)

# ---------------------------------------------------------------------------
# STEP 5 — Process SINGLE DIGITAL measures from Model 3  (DRIVERDATA=1, TYPE=6)
# ---------------------------------------------------------------------------

print(f"[INFO] Single-digital measures (M3 subset): {len(_m3_single_digital)}")

for _raw_m in _m3_single_digital:

    _desc = _raw_m.get("NAME")
    if _desc is None:
        continue
    _desc_lower = _desc.strip().lower()
    if _desc_lower in SKIP_DESCRIPTIONS:
        continue
    if "disponibile" in _desc_lower:
        continue

    _m = deepcopy(_raw_m)
    _raw_name = _m.get("NAME", "")
    _lookup_key = _raw_name.strip().lower()

    if _lookup_key in name_lookup and name_lookup[_lookup_key]["NAME"] is not None:
        _m["NAME"] = name_lookup[_lookup_key]["NAME"]
    else:
        _n = _raw_name
        _n = re.sub(r"\([^)]*\)", "", _n)
        _n = re.sub(r"\[[^\]]*\]", "", _n)
        _n = _n.strip()
        _n = re.sub(r"\b(di|del|della|in|da|per|con)\b", "", _n, flags=re.IGNORECASE).strip()
        _n = re.sub(r"\s{2,}", " ", _n)
        if len(_n) > 25: _n = re.sub(r"\bAnalizzatore\b", "Anal.",   _n, flags=re.IGNORECASE)
        if len(_n) > 25: _n = re.sub(r"\bConvertitore\b", "Conv.",   _n, flags=re.IGNORECASE)
        if len(_n) > 25: _n = re.sub(r"\bManutenzione\b", "Manut.",  _n, flags=re.IGNORECASE)
        if len(_n) > 25: _n = re.sub(r"\bCalibrazione\b", "Calib.",  _n, flags=re.IGNORECASE)
        if len(_n) > 25: _n = re.sub(r"\bTemperatura\b",  "Temp.",   _n, flags=re.IGNORECASE)
        if len(_n) > 25: _n = re.sub(r"\bCollegamento\b", "Colleg.", _n, flags=re.IGNORECASE)
        if len(_n) > 25: _n = re.sub(r"\bComunicazione\b","Comm.",   _n, flags=re.IGNORECASE)
        if len(_n) > 25: _n = re.sub(r"\bOssigeno\b",     "O2",      _n, flags=re.IGNORECASE)
        if len(_n) > 25: _n = re.sub(r"\bAllarme\b",      "All.",    _n, flags=re.IGNORECASE)
        if len(_n) > 25: _n = re.sub(r"\brichiesta\b",    "rich.",   _n, flags=re.IGNORECASE)
        if len(_n) > 25: _n = re.sub(r"\bpresenza\b",     "pres.",   _n, flags=re.IGNORECASE)
        if len(_n) > 25: _n = re.sub(r"\bComando\b",      "Cmd",     _n, flags=re.IGNORECASE)
        _n = _n[:25].strip()
        _m["NAME"] = _n

    # Force single-digital type
    _m["DRIVERDATA"] = 1
    _m["TYPE"]       = 6
    _m["UNITS"]      = None

    # Coil addresses MUST stay as zero-padded strings
    _reg = _m.get("MODBUSREGISTRO")
    if _reg is None:
        pass  # keep null
    elif isinstance(_reg, int):
        # If the model returned an integer for a coil, re-pad it
        if _reg < 10000:
            _m["MODBUSREGISTRO"] = f"{_reg:05d}"
        # else it's a holding register — warn but keep
    elif isinstance(_reg, str):
        # Keep string as-is (preserves leading zeros)
        pass

    # Single digitals never have GROUP
    _m.pop("GROUP", None)

    try:
        _sid = int(_raw_m.get("STATIONID", 1))
    except (TypeError, ValueError):
        _sid = 1
    if _sid not in stations:
        _sid = min(stations.keys())
    _m["STATIONID"] = _sid
    _m.pop("_raw_desc", None)

    all_measures.append(_m)

# ---------------------------------------------------------------------------
# STEP 6 — Process PACKED DIGITAL measures from Model 3  (DRIVERDATA=2, TYPE=1)
# ---------------------------------------------------------------------------

print(f"[INFO] Packed measures (M3 subset): {len(_m3_packed)}")

for _raw_m in _m3_packed:

    _m = deepcopy(_raw_m)
    _raw_name = _m.get("NAME", "")
    _lookup_key = _raw_name.strip().lower()

    if _lookup_key in name_lookup and name_lookup[_lookup_key]["NAME"] is not None:
        _m["NAME"] = name_lookup[_lookup_key]["NAME"]
    else:
        _n = _raw_name
        _n = re.sub(r"\([^)]*\)", "", _n)
        _n = re.sub(r"\[[^\]]*\]", "", _n)
        _n = _n.strip()
        _n = re.sub(r"\b(di|del|della|in|da|per|con)\b", "", _n, flags=re.IGNORECASE).strip()
        _n = re.sub(r"\s{2,}", " ", _n)
        if len(_n) > 25: _n = re.sub(r"\bAnalizzatore\b", "Anal.",   _n, flags=re.IGNORECASE)
        if len(_n) > 25: _n = re.sub(r"\bConvertitore\b", "Conv.",   _n, flags=re.IGNORECASE)
        if len(_n) > 25: _n = re.sub(r"\bManutenzione\b", "Manut.",  _n, flags=re.IGNORECASE)
        if len(_n) > 25: _n = re.sub(r"\bCalibrazione\b", "Calib.",  _n, flags=re.IGNORECASE)
        if len(_n) > 25: _n = re.sub(r"\bTemperatura\b",  "Temp.",   _n, flags=re.IGNORECASE)
        if len(_n) > 25: _n = re.sub(r"\bCollegamento\b", "Colleg.", _n, flags=re.IGNORECASE)
        if len(_n) > 25: _n = re.sub(r"\bComunicazione\b","Comm.",   _n, flags=re.IGNORECASE)
        if len(_n) > 25: _n = re.sub(r"\bOssigeno\b",     "O2",      _n, flags=re.IGNORECASE)
        if len(_n) > 25: _n = re.sub(r"\bAllarme\b",      "All.",    _n, flags=re.IGNORECASE)
        if len(_n) > 25: _n = re.sub(r"\brichiesta\b",    "rich.",   _n, flags=re.IGNORECASE)
        if len(_n) > 25: _n = re.sub(r"\bpresenza\b",     "pres.",   _n, flags=re.IGNORECASE)
        if len(_n) > 25: _n = re.sub(r"\bComando\b",      "Cmd",     _n, flags=re.IGNORECASE)
        _n = _n[:25].strip()
        _m["NAME"] = _n

    _m["DRIVERDATA"] = 2
    _m["TYPE"]       = 1
    _m["UNITS"]      = None

    if "GROUP" in _m and not _m["GROUP"]:
        del _m["GROUP"]

    # Packed holding registers are integers; coil-based packed would be strings
    _reg = _m.get("MODBUSREGISTRO")
    if isinstance(_reg, str) and re.match(r"^[1-9]\d*$", _reg):
        _m["MODBUSREGISTRO"] = int(_reg)

    try:
        _sid = int(_raw_m.get("STATIONID", 1))
    except (TypeError, ValueError):
        _sid = 1
    if _sid not in stations:
        _sid = min(stations.keys())
    _m["STATIONID"] = _sid
    _m.pop("_raw_desc", None)

    all_measures.append(_m)

# ---------------------------------------------------------------------------
# STEP 7 — Deduplicate
#
# Rules:
#   - Packed (DRIVERDATA=2): one entry per (station, register). Keep first seen.
#   - Single digital (DRIVERDATA=1): one entry per (station, register). Keep first.
#   - Analog (DRIVERDATA=0): may freely share registers — no dedup.
#   - If M2 produced an analog for a register that M3 claims as packed → drop analog.
#   - Analog rows leaked into M3 (DRIVERDATA=0) are already ignored above.
# ---------------------------------------------------------------------------

_packed_keys   = set()
_digital_keys  = set()

for _m in all_measures:
    if _m.get("DRIVERDATA") == 2:
        _packed_keys.add((_m.get("STATIONID"), _m.get("MODBUSREGISTRO")))
    elif _m.get("DRIVERDATA") == 1:
        _digital_keys.add((_m.get("STATIONID"), _m.get("MODBUSREGISTRO")))

_seen_packed  = set()
_seen_digital = set()
_deduped_measures = []

for _m in all_measures:
    _dd = _m.get("DRIVERDATA")
    _key = (_m.get("STATIONID"), _m.get("MODBUSREGISTRO"))

    if _dd == 2:
        if _key in _seen_packed:
            continue
        _seen_packed.add(_key)
        _deduped_measures.append(_m)

    elif _dd == 1:
        if _key in _seen_digital:
            continue
        _seen_digital.add(_key)
        _deduped_measures.append(_m)

    elif _dd == 0:
        # Drop if M3 already claimed this register as packed
        if _key in _packed_keys and _m["MODBUSREGISTRO"] is not None:
            continue
        _deduped_measures.append(_m)

    else:
        _deduped_measures.append(_m)

all_measures = _deduped_measures

# ---------------------------------------------------------------------------
# STEP 8 — Assign measures to their stations
# ---------------------------------------------------------------------------

for _m in all_measures:
    _sid = _m["STATIONID"]
    stations[_sid]["measures"].append(_m)

# ---------------------------------------------------------------------------
# STEP 9 — Process bitinfo entries from Model 4
# ---------------------------------------------------------------------------

print(f"[INFO] Bitinfo entries (M4): {len(m4)}")

for _raw_b in m4:

    _b = deepcopy(_raw_b)

    _mid = _b.get("MEASUREID")
    if isinstance(_mid, str) and re.match(r"^[1-9]\d*$", _mid):
        _b["MEASUREID"] = int(_mid)

    _b["BITNO"] = int(_b.get("BITNO", 0))

    if not _b.get("BITNAME", "").strip():
        _b["BITNAME"] = f"Bit {_b['BITNO']}"

    if _b.get("TEXTON") == _b.get("TEXTOFF"):
        _b["TEXTOFF"] = "OFF" if _b["TEXTON"] != "OFF" else "Attivo"

    try:
        _sid = int(_raw_b.get("STATIONID", 1))
    except (TypeError, ValueError):
        _sid = 1
    if _sid not in stations:
        _sid = min(stations.keys())
    _b["STATIONID"] = _sid

    stations[_sid]["bitinfo"].append(_b)

# ---------------------------------------------------------------------------
# STEP 10 — Assign sequential IDs per station (internal)
# ---------------------------------------------------------------------------

for _sid, _station in stations.items():
    for _idx, _measure in enumerate(_station["measures"], start=1):
        _measure["_measure_seq"] = _idx

# ---------------------------------------------------------------------------
# STEP 11 — Serialise to final output structure
# ---------------------------------------------------------------------------

INTERNAL_KEYS = {"_ip", "_measure_seq", "_raw_desc", "STATIONID"}

result = []

for _sid in sorted(stations.keys()):
    _station = stations[_sid]

    _out_station = {
        "NAME":         _station["NAME"],
        "DRIVERNAME":   _station["DRIVERNAME"],
        "DRIVERCONFIG": _station["DRIVERCONFIG"],
        "ID":           _station["ID"],
        "measures":     [],
        "bitinfo":      [],
    }

    for _m in _station["measures"]:
        _entry = {_k: _v for _k, _v in _m.items() if _k not in INTERNAL_KEYS}
        if "UNITS" not in _entry:
            _entry["UNITS"] = None
        _out_station["measures"].append(_entry)

    for _b in _station["bitinfo"]:
        _entry = {_k: _v for _k, _v in _b.items() if _k not in INTERNAL_KEYS}
        _out_station["bitinfo"].append(_entry)

    result.append(_out_station)

# ---------------------------------------------------------------------------
# STEP 12 — Validation summary + warnings
# ---------------------------------------------------------------------------

_total_measures  = sum(len(_s["measures"]) for _s in result)
_total_bits      = sum(len(_s["bitinfo"])  for _s in result)
_count_analog    = sum(1 for _s in result for _m in _s["measures"] if _m.get("DRIVERDATA") == 0)
_count_digital   = sum(1 for _s in result for _m in _s["measures"] if _m.get("DRIVERDATA") == 1)
_count_packed    = sum(1 for _s in result for _m in _s["measures"] if _m.get("DRIVERDATA") == 2)

print(f"[INFO] Final: {len(result)} stations | {_total_measures} measures "
      f"(analog:{_count_analog} digital:{_count_digital} packed:{_count_packed}) | "
      f"{_total_bits} bitinfo entries")

for _s in result:
    for _m in _s["measures"]:
        if not _m.get("NAME"):
            print(f"[WARN] Empty NAME in station {_s['ID']}: {_m}")
        # Single digital coil addresses should be strings
        if _m.get("DRIVERDATA") == 1 and isinstance(_m.get("MODBUSREGISTRO"), int):
            print(f"[WARN] Single-digital measure has integer register "
                  f"(should be string '0xxxx'): {_m.get('NAME')} = {_m.get('MODBUSREGISTRO')}")

# ---------------------------------------------------------------------------
# result  ←  final list of station dicts, ready for use
# ---------------------------------------------------------------------------
output_json_final = json.dumps(result, ensure_ascii=False, indent=2)