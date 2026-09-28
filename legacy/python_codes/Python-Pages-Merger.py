



"""
merge_pages.py
==============
Merges the JSON outputs of multiple page-agents into one final JSON.

Each page-agent produces a list of station objects (one per IP).
This script:
  1. Collects all station objects across all pages
  2. Merges stations that share the same DRIVERCONFIG (same IP:PORT)
     — combines their measures lists (no duplicates by MODBUSREGISTRO+NAME)
     — combines their bitinfo lists (no duplicates by MEASUREID+BITNO)
  3. Re-sequences station IDs and measure IDs
  4. Outputs the final merged JSON

No functions, no classes — pure sequential imperative code.

USAGE:
  Set PAGE_OUTPUTS below to the list of raw JSON strings from each page-agent.
  The variable `final_result` holds the merged output.
"""

import json
import re
from copy import deepcopy

# ---------------------------------------------------------------------------
# CONFIGURATION — paste each page-agent's raw output string here
# ---------------------------------------------------------------------------

PAGE_OUTPUTS = [r'''{edge}[9]''']


# ---------------------------------------------------------------------------
# STEP 0 — Parse all page outputs into Python objects
# Each page output is either:
#   - A list of station objects:       [{station}, {station}]
#   - A list of lists of stations:    [[{station}], [{station}]]
# We normalise everything into a flat list of station dicts.
# ---------------------------------------------------------------------------

all_station_objects = []


for _page_idx, _raw in enumerate(PAGE_OUTPUTS, start=1):
    _text = _raw.strip()

    # Rimuovi wrapper esterno [```json ... ```]
    _text = re.sub(r"^\[```(?:json)?\s*", "", _text)
    _text = re.sub(r"\s*```\]$", "", _text)

    # Splitta sui separatori ```json interni (multi-pagina)
    _chunks = re.split(r"\s*```(?:json)?\s*", _text)
    _chunks = [c.strip() for c in _chunks if c.strip()]

    for _chunk in _chunks:
        try:
            _parsed = json.loads(_chunk)
        except json.JSONDecodeError as _exc:
            print(f"[ERROR] Page {_page_idx}: could not parse JSON: {_exc}")
            continue

        if isinstance(_parsed, list):
            for _item in _parsed:
                if isinstance(_item, list):
                    for _s in _item:
                        if isinstance(_s, dict):
                            all_station_objects.append((_page_idx, deepcopy(_s)))
                elif isinstance(_item, dict):
                    all_station_objects.append((_page_idx, deepcopy(_item)))

print(f"[INFO] Total station objects collected across all pages: {len(all_station_objects)}")

# ---------------------------------------------------------------------------
# STEP 1 — Group stations by DRIVERCONFIG (normalised)
# Two stations with the same DRIVERCONFIG are the same physical device.
# We use DRIVERCONFIG as the merge key, normalising commas→dots in IP.
# ---------------------------------------------------------------------------

# ordered list of unique keys (preserves first-appearance order)
_station_key_order = []
# map: normalised_driverconfig → merged station dict
_merged_stations = {}

for _page_idx, _station in all_station_objects:
    _raw_cfg = _station.get("DRIVERCONFIG", ":")
    # Normalise: replace comma-separated IP notation with dots
    _norm_cfg = _raw_cfg.replace(",", ".")

    if _norm_cfg not in _merged_stations:
        _station_key_order.append(_norm_cfg)
        _merged_stations[_norm_cfg] = {
            "NAME":         _station.get("NAME", "SME"),
            "DRIVERNAME":   _station.get("DRIVERNAME", "modbusplc"),
            "DRIVERCONFIG": _raw_cfg,   # keep original formatting
            "_measures":    [],
            "_bitinfo":     [],
        }
        print(f"[INFO]   New station found: {_norm_cfg}  (page {_page_idx})")
    else:
        print(f"[INFO]   Station {_norm_cfg} already exists — merging page {_page_idx}")

    # Accumulate measures and bitinfo (raw, dedup happens in step 2)
    _merged_stations[_norm_cfg]["_measures"].extend(
        deepcopy(_station.get("measures", []))
    )
    _merged_stations[_norm_cfg]["_bitinfo"].extend(
        deepcopy(_station.get("bitinfo", []))
    )

print(f"[INFO] Distinct stations after grouping: {len(_merged_stations)}")

# ---------------------------------------------------------------------------
# STEP 2 — Deduplicate measures within each merged station
#
# Dedup key for each type:
#   Analog   (DRIVERDATA=0): (NAME, MODBUSREGISTRO)
#             — two analogs can share a register but same name+reg = duplicate
#   Digital  (DRIVERDATA=1): (MODBUSREGISTRO,)
#             — one coil address = one measure
#   Packed   (DRIVERDATA=2): (MODBUSREGISTRO,)
#             — one base register = one measure
#
# For each duplicate, keep the FIRST occurrence (from the lowest page number).
# ---------------------------------------------------------------------------

for _cfg, _station in _merged_stations.items():

    _seen_analog  = set()   # (name_lower, reg)
    _seen_digital = set()   # (reg,)
    _seen_packed  = set()   # (reg,)
    _deduped = []

    for _m in _station["_measures"]:
        _dd  = _m.get("DRIVERDATA", 0)
        _reg = _m.get("MODBUSREGISTRO")
        # Normalise register for key: None stays None, strings stay strings
        _reg_key = str(_reg) if _reg is not None else None

        if _dd == 0:
            # L'uso di "or """ garantisce che se il valore è None, diventi una stringa vuota
            _name_val = _m.get("NAME") or ""
            _key = (_name_val.strip().lower(), _reg_key)
            if _key in _seen_analog:
                continue
            _seen_analog.add(_key)

        elif _dd == 1:
            _key = (_reg_key,)
            if _key in _seen_digital:
                continue
            _seen_digital.add(_key)

        elif _dd == 2:
            _key = (_reg_key,)
            if _key in _seen_packed:
                continue
            _seen_packed.add(_key)

        _deduped.append(_m)

    _before = len(_station["_measures"])
    _station["_measures"] = _deduped
    _after  = len(_deduped)
    if _before != _after:
        print(f"[INFO] Station {_cfg}: measures {_before} → {_after} after dedup "
              f"({_before - _after} duplicates removed)")

# ---------------------------------------------------------------------------
# STEP 3 — Deduplicate bitinfo within each merged station
#
# Dedup key: (MEASUREID, BITNO)
# Keep first occurrence.
# ---------------------------------------------------------------------------

for _cfg, _station in _merged_stations.items():

    _seen_bits = set()
    _deduped_bits = []

    for _b in _station.get("_bitinfo",[]):
        _key = (_b.get("MEASUREID"), int(_b.get("BITNO", 0)))
        if _key in _seen_bits:
            continue
        _seen_bits.add(_key)
        _deduped_bits.append(_b)

    _before = len(_station["_bitinfo"])
    _station["_bitinfo"] = _deduped_bits
    _after  = len(_deduped_bits)
    if _before != _after:
        print(f"[INFO] Station {_cfg}: bitinfo {_before} → {_after} after dedup")

# ---------------------------------------------------------------------------
# STEP 4 — Re-sequence station IDs and measure IDs
#
# Stations: sequential starting at 1, in order of first appearance.
# Measures within each station: sequential starting at 1.
# STATIONID on each measure updated to match the new station ID.
# ---------------------------------------------------------------------------

final_result = []

for _new_sid, _cfg in enumerate(_station_key_order, start=1):
    _station = _merged_stations[_cfg]

    _out_measures = []
    for _new_mid, _m in enumerate(_station["_measures"], start=1):
        _entry = deepcopy(_m)
        _entry["ID"]        = _new_mid
        _entry["STATIONID"] = _new_sid
        # Ensure UNITS key exists
        if "UNITS" not in _entry:
            _entry["UNITS"] = None
        _out_measures.append(_entry)

    _out_bitinfo = []
    for _b in _station.get("_bitinfo",[]):
        _entry = deepcopy(_b)
        _entry["STATIONID"] = _new_sid
        _out_bitinfo.append(_entry)

    final_result.append({
        "NAME":         _station["NAME"],
        "DRIVERNAME":   _station["DRIVERNAME"],
        "DRIVERCONFIG": _station["DRIVERCONFIG"],
        "ID":           _new_sid,
        "measures":     _out_measures,
        "bitinfo":      _out_bitinfo,
    })

# ---------------------------------------------------------------------------
# STEP 5 — Summary
# ---------------------------------------------------------------------------

for _s in final_result:
    _a = sum(1 for _m in _s["measures"] if _m.get("DRIVERDATA") == 0)
    _d = sum(1 for _m in _s["measures"] if _m.get("DRIVERDATA") == 1)
    _p = sum(1 for _m in _s["measures"] if _m.get("DRIVERDATA") == 2)
    print(f"[INFO] Station {_s['ID']} ({_s['DRIVERCONFIG']}): "
          f"{len(_s['measures'])} measures "
          f"(analog:{_a} digital:{_d} packed:{_p}), "
          f"{len(_s['bitinfo'])} bitinfo")

# ---------------------------------------------------------------------------
# final_result  ←  ready for use or json.dumps()
# ---------------------------------------------------------------------------
output_json_final = json.dumps(final_result, ensure_ascii=False, indent=2)

with open('localoutput28page1.json', 'w') as file:
    json.dump(final_result, file, ensure_ascii=False, indent=4)