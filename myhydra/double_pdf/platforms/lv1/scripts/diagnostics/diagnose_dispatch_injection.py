import json


# Pytool temporaneo dentro una sottopiattaforma LV2 di prova.
# L'iniezione dovrebbe invocarlo una volta per ogni record dell'array root.
input_raw = r'''{question}'''.strip()

try:
    input_data = json.loads(input_raw)
    while isinstance(input_data, str):
        input_data = json.loads(input_data)

    diagnostic = {
        "probe": "DISPATCH_ITERATION",
        "input_kind": "UNKNOWN",
        "item_count": None,
        "page_key": None,
        "sequence_index": None,
        "document_role": None,
        "label": None,
    }

    if isinstance(input_data, list):
        diagnostic["input_kind"] = "ROOT_ARRAY"
        diagnostic["item_count"] = len(input_data)
        if len(input_data) == 1 and isinstance(input_data[0], dict):
            item = input_data[0]
            if isinstance(item.get("key"), str):
                diagnostic["input_kind"] = "SINGLE_ITEM_ARRAY"
                diagnostic["page_key"] = item.get("key")
                diagnostic["sequence_index"] = item.get("sequence_index")
                diagnostic["document_role"] = item.get("document_role")
                diagnostic["label"] = item.get("label")

    elif isinstance(input_data, dict):
        if isinstance(input_data.get("key"), str):
            diagnostic["input_kind"] = "SINGLE_PAGE"
            diagnostic["item_count"] = 1
            diagnostic["page_key"] = input_data.get("key")
            diagnostic["sequence_index"] = input_data.get("sequence_index")
            diagnostic["document_role"] = input_data.get("document_role")
            diagnostic["label"] = input_data.get("label")
        elif isinstance(input_data.get("pages"), list):
            diagnostic["input_kind"] = "LV1_WRAPPER"
            diagnostic["item_count"] = len(input_data["pages"])
            if len(input_data["pages"]) == 1 and isinstance(input_data["pages"][0], dict):
                item = input_data["pages"][0]
                diagnostic["page_key"] = item.get("key")
                diagnostic["sequence_index"] = item.get("sequence_index")
                diagnostic["document_role"] = item.get("document_role")
                diagnostic["label"] = item.get("label")

    result = json.dumps(diagnostic, ensure_ascii=False)

except Exception as error:
    result = json.dumps({
        "probe": "DISPATCH_ITERATION",
        "input_kind": "PARSE_ERROR",
        "error": str(error),
    }, ensure_ascii=False)
