import json

# Script temporaneo di diagnosi; non modifica e non associa i dati.
# QUESTION: input originale LV1 ricevuto dal ciclo iterativo, dovrebbe contenere le chiavi.
# EDGE #2: output Visiomaru/VLM.
media_raw = r'''{question}'''
vlm_raw = r'''{edge}[2]'''

media_info = {
    "source": "question (LV1 input)",
    "raw_length": len(media_raw),
    "raw_preview": repr(media_raw[:300]),
    "json_valid": False,
    "parsed_type": None,
    "parsed_preview": None,
    "parse_error": None
}

try:
    media_parsed = json.loads(media_raw.strip())
    media_info["json_valid"] = True
    media_info["parsed_type"] = type(media_parsed).__name__
    media_info["parsed_preview"] = repr(media_parsed)[:300]
except Exception as error:
    media_info["parse_error"] = str(error)

vlm_info = {
    "source": "edge #2 (VLM)",
    "raw_length": len(vlm_raw),
    "raw_preview": repr(vlm_raw[:300]),
    "json_valid": False,
    "parsed_type": None,
    "parsed_preview": None,
    "parse_error": None
}

try:
    vlm_parsed = json.loads(vlm_raw.strip())
    vlm_info["json_valid"] = True
    vlm_info["parsed_type"] = type(vlm_parsed).__name__
    vlm_info["parsed_preview"] = repr(vlm_parsed)[:300]
except Exception as error:
    vlm_info["parse_error"] = str(error)

result = json.dumps({
    "diagnostic": "PYTOOL_INPUTS",
    "inputs": [media_info, vlm_info]
}, ensure_ascii=False, indent=2)
