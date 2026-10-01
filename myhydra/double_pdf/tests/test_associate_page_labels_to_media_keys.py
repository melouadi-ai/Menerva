import json
from pathlib import Path


DOUBLE_PDF_DIR = Path(__file__).resolve().parent.parent
SCRIPT_PATH = (
    DOUBLE_PDF_DIR
    / "platforms"
    / "lv2"
    / "page_classifier"
    / "scripts"
    / "history"
    / "associate_page_labels_to_media_keys.py"
)
CASE_DIR = Path(__file__).resolve().parent / "case_6"


def execute_pytool(question_payload, vlm_payload):
    """Esegue localmente il sorgente Pytool dopo aver simulato i placeholder MyHydra."""
    source = SCRIPT_PATH.read_text(encoding="utf-8")
    source = source.replace(
        "{question}",
        json.dumps(question_payload, ensure_ascii=False),
    )
    source = source.replace(
        "{edge}[2]",
        json.dumps(vlm_payload, ensure_ascii=False),
    )
    namespace = {}
    exec(compile(source, str(SCRIPT_PATH), "exec"), namespace)
    return json.loads(namespace["result"])


def test_all_case_6_windows_associate_all_keys_and_labels():
    windows = json.loads(
        (CASE_DIR / "inputs" / "medex_windows_sanitized.json").read_text(
            encoding="utf-8"
        )
    )
    classifier_outputs = json.loads(
        (CASE_DIR / "outputs" / "observed_classifier.json").read_text(
            encoding="utf-8"
        )
    )

    assert len(windows) == 14
    assert len(classifier_outputs) == 14

    all_associations = []
    for window, classification in zip(windows, classifier_outputs, strict=True):
        # MyHydra fornisce _medexkeys come stringa JSON annidata nel question.
        question_payload = {
            "_medexkeys": json.dumps(window["_medexkeys"], ensure_ascii=False)
        }
        result = execute_pytool(question_payload, classification)
        assert result["status"] == "OK", result
        assert len(result["pages"]) == len(window["_medexkeys"])
        all_associations.extend(result["pages"])

    assert len(all_associations) == 27

    # Verifica che le pagine duplicate dall'overlap conservino la stessa classe.
    labels_by_key = {}
    for association in all_associations:
        key = association["key"]
        label = association["label"]
        if key in labels_by_key:
            assert labels_by_key[key] == label
        else:
            labels_by_key[key] = label

    assert len(labels_by_key) == 14


def test_last_window_accepts_one_medex_key():
    question_payload = {
        "_medexkeys": json.dumps(
            {"key": "CASE6_PAGE_14"},
            ensure_ascii=False,
        )
    }
    vlm_payload = {
        "pages": [{"index": 0, "label": "MEASUREMENT_TECHNICAL_DATA"}]
    }

    result = execute_pytool(question_payload, vlm_payload)

    assert result == {
        "status": "OK",
        "pages": [
            {
                "key": "CASE6_PAGE_14",
                "index": 0,
                "document_role": "UNKNOWN",
                "label": "MEASUREMENT_TECHNICAL_DATA",
            }
        ],
    }


def test_document_role_is_preserved_from_classifier_output():
    question_payload = {
        "_medexkeys": json.dumps({"key": "CASE6_PAGE_01"}, ensure_ascii=False)
    }
    vlm_payload = {
        "pages": [
            {
                "index": 0,
                "document_role": "IOL",
                "label": "DENSITY_MAP",
            }
        ]
    }

    result = execute_pytool(question_payload, vlm_payload)

    assert result["status"] == "OK"
    assert result["pages"][0]["document_role"] == "IOL"
    assert result["pages"][0]["label"] == "DENSITY_MAP"


def test_nested_medex_key_with_escaped_slash_is_decoded():
    question_payload = {
        "_medexkeys": r'{"key":"CASE6_NAMESPACE\/media-001"}'
    }
    vlm_payload = {
        "pages": [{"index": 0, "label": "DENSITY_MAP"}]
    }

    result = execute_pytool(question_payload, vlm_payload)

    assert result["status"] == "OK"
    assert result["pages"][0]["key"] == "CASE6_NAMESPACE/media-001"


def test_key_and_classification_count_mismatch_returns_error_json():
    question_payload = {
        "_medexkeys": json.dumps(
            [
                {"key": "CASE6_PAGE_01"},
                {"key": "CASE6_PAGE_02"},
            ],
            ensure_ascii=False,
        )
    }
    vlm_payload = {
        "pages": [{"index": 0, "label": "DENSITY_MAP"}]
    }

    result = execute_pytool(question_payload, vlm_payload)

    assert result["status"] == "ERROR"
    assert "2 chiavi" in result["error"]
    assert "1 classificazioni" in result["error"]
