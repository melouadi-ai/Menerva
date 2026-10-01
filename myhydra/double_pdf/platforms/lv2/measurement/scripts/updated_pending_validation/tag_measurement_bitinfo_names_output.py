import json
import re


BRANCH = "BITINFO_NAMES"
page_raw = r'''{question}'''.strip()
vlm_raw = r'''{edge}[6]'''.strip()

try:
    page = json.loads(page_raw)
    while isinstance(page, str):
        page = json.loads(page)
    if isinstance(page, list):
        if len(page) != 1:
            raise ValueError("Atteso un solo record pagina nell'iterazione corrente.")
        page = page[0]
        while isinstance(page, str):
            page = json.loads(page)
    if not isinstance(page, dict):
        raise ValueError("La question non contiene un record pagina JSON.")
    if not isinstance(page.get("key"), str) or not page["key"].strip():
        raise ValueError("Il record pagina non contiene una key valida.")

    current = vlm_raw
    parsed_output = None
    output_format = None
    unwrap_count = 0
    while unwrap_count < 3:
        try:
            decoded = json.loads(current)
        except Exception:
            break
        if not isinstance(decoded, str):
            parsed_output = decoded
            output_format = "JSON"
            break
        current = decoded.strip()
        unwrap_count += 1

    if output_format is None:
        fenced_blocks = re.findall(
            r"```(?:json)?\s*(.*?)\s*```", current,
            flags=re.IGNORECASE | re.DOTALL
        )
        if fenced_blocks:
            parsed_blocks = []
            block_index = 0
            while block_index < len(fenced_blocks):
                parsed_blocks.append(json.loads(fenced_blocks[block_index]))
                block_index += 1
            if len(parsed_blocks) == 1:
                parsed_output = parsed_blocks[0]
                output_format = "MARKDOWN_JSON"
            else:
                parsed_output = parsed_blocks
                output_format = "MULTIPLE_MARKDOWN_JSON"
        else:
            try:
                parsed_output = json.loads(current)
                output_format = "JSON_TEXT"
            except Exception as parse_error:
                output_format = "RAW_TEXT_PARSE_ERROR"
                parsed_output = None
                parse_message = str(parse_error)

    envelope = {
        "diagnostic": "LV2_MEASUREMENT_BRANCH",
        "status": "OK",
        "branch": BRANCH,
        "page": page,
        "output_format": output_format,
        "vlm_output": parsed_output,
    }
    if output_format == "RAW_TEXT_PARSE_ERROR":
        envelope["parse_error"] = parse_message
        envelope["vlm_output_raw"] = vlm_raw
    result = json.dumps(envelope, ensure_ascii=False)

except Exception as error:
    result = json.dumps(
        {
            "diagnostic": "LV2_MEASUREMENT_BRANCH",
            "branch": BRANCH,
            "status": "ERROR",
            "error": str(error),
            "page_raw": page_raw,
            "vlm_output_raw": vlm_raw,
        },
        ensure_ascii=False,
    )
