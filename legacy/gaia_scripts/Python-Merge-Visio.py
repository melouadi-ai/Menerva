import json

# --- Inputs (JSON strings from the three agents) ---
agent1_output = r'''{edge}[4]'''  # Agent 1: Station Information
agent2_output = r'''{edge}[5]'''  # Agent 2: Measures
agent3_output = r'''{edge}[6]'''  # Agent 3: BitInfo

# ---------------------------------------------------------------------------
# SAFE PARSE — handles empty string, "[]", whitespace-only, invalid JSON
# ---------------------------------------------------------------------------

def safe_parse(raw):
    import json
    if not isinstance(raw, str):
        return []
    raw = raw.strip()
    if not raw:
        return []
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return []
    if isinstance(parsed, dict):
        return [parsed]
    if isinstance(parsed, list):
        return parsed
    return []

raw1 = safe_parse(agent1_output)
raw2 = safe_parse(agent2_output)
raw3 = safe_parse(agent3_output)

# ---------------------------------------------------------------------------
# BUILD BITINFO LOOKUP
# Key: str(modbus_registro)
# Value: list of bitinfo records belonging to that register
# ---------------------------------------------------------------------------

bitinfo_lookup = {}

for block in raw3:
    if not isinstance(block, dict):
        continue
    if block.get("_subkey") != "bitinfo_insert":
        continue
    params = block.get("_params", [])
    if not isinstance(params, list):
        continue
    for record in params:
        if not isinstance(record, dict):
            continue
        reg = record.get("modbus_registro")
        if reg is None:
            continue
        reg_key = str(reg)
        if reg_key not in bitinfo_lookup:
            bitinfo_lookup[reg_key] = []
        bitinfo_lookup[reg_key].append(record)

# ---------------------------------------------------------------------------
# PROCESS AGENT 2 OUTPUT
# ---------------------------------------------------------------------------

merged_measures = []

for block in raw2:
    if not isinstance(block, dict):
        continue
    if block.get("_subkey") != "misura_insert":
        continue
    params = block.get("_params", [])
    if not isinstance(params, list):
        continue

    updated_params = []

    for record in params:
        if not isinstance(record, dict):
            updated_params.append(record)
            continue

        is_packed = record.get("digit_impaccato", 0) == 1
        is_single = record.get("digit_singolo",   0) == 1

        reg     = record.get("modbus_registro")
        reg_key = str(reg) if reg is not None else None

        if is_packed:
            record["stato_off"] = None
            record["stato_on"]  = None

        elif is_single and reg_key is not None and reg_key in bitinfo_lookup:
            bit_pos     = record.get("bit_posizione")
            matched_off = record.get("stato_off")
            matched_on  = record.get("stato_on")
            for bit_record in bitinfo_lookup[reg_key]:
                if bit_record.get("bit_posizione") == bit_pos:
                    matched_off = bit_record.get("stato_off")
                    matched_on  = bit_record.get("stato_on")
                    break
            record["stato_off"] = matched_off
            record["stato_on"]  = matched_on

        updated_params.append(record)

    merged_measures.append({
        "_subkey": "misura_insert",
        "_params": updated_params
    })

# ---------------------------------------------------------------------------
# COLLECT BITINFO BLOCKS
# ---------------------------------------------------------------------------

bitinfo_blocks = [
    block for block in raw3
    if isinstance(block, dict) and block.get("_subkey") == "bitinfo_insert"
]

# ---------------------------------------------------------------------------
# ASSEMBLE FINAL OUTPUT
# Order: stazione_insert → misura_insert → bitinfo_insert
# ---------------------------------------------------------------------------

final_output = []

for block in raw1:
    if isinstance(block, dict) and block.get("_subkey") == "stazione_insert":
        final_output.append(block)

for block in merged_measures:
    final_output.append(block)

for block in bitinfo_blocks:
    final_output.append(block)

# ---------------------------------------------------------------------------
# SERIALIZE
# ---------------------------------------------------------------------------

result = json.dumps(final_output, ensure_ascii=False, indent=2)
print(result)