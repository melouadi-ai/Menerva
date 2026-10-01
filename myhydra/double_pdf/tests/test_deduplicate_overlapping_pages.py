import json
from pathlib import Path


DOUBLE_PDF_DIR = Path(__file__).resolve().parent.parent
SCRIPT_PATH = (
    DOUBLE_PDF_DIR
    / "platforms"
    / "lv1"
    / "scripts"
    / "in_use"
    / "deduplicate_overlapping_pages.py"
)
CASE_DIR = Path(__file__).resolve().parent / "case_6"


def execute_pytool(aggregated_output):
    """Esegue localmente lo script dopo aver simulato il placeholder MyHydra."""
    source = SCRIPT_PATH.read_text(encoding="utf-8")
    source = source.replace(
        "{edge}[3]",
        json.dumps(aggregated_output, ensure_ascii=False),
    )
    namespace = {}
    exec(compile(source, str(SCRIPT_PATH), "exec"), namespace)
    return json.loads(namespace["result"])


def test_case_6_aggregated_runtime_output_deduplicates_to_14_pages():
    aggregated_output = json.loads(
        (CASE_DIR / "outputs" / "observed_pytool_sanitized.json").read_text(
            encoding="utf-8"
        )
    )

    result = execute_pytool(aggregated_output)

    assert result["status"] == "OK", result
    assert result["page_count"] == 14
    assert result["review_required"] is False
    assert result["warnings"] == []
    assert len(result["pages"]) == 14
    assert result["pages"][0] == {
        "key": "CASE6_PAGE_01",
        "sequence_index": 1,
        "document_role": "UNKNOWN",
        "label": "DENSITY_MAP",
    }
    assert result["pages"][-1] == {
        "key": "CASE6_PAGE_14",
        "sequence_index": 14,
        "document_role": "UNKNOWN",
        "label": "MEASUREMENT_TECHNICAL_DATA",
    }


def test_conflicting_labels_use_legacy_priority_and_add_warning():
    aggregated_output = [
        {
            "status": "OK",
            "pages": [{"key": "PAGE_01", "index": 0, "label": "STATION_INFORMATION"}],
        },
        {
            "status": "OK",
            "pages": [{"key": "PAGE_01", "index": 0, "label": "MEASUREMENT_TECHNICAL_DATA"}],
        },
    ]

    result = execute_pytool(aggregated_output)

    assert result["status"] == "OK", result
    assert result["review_required"] is True
    assert result["pages"][0]["label"] == "STATION_INFORMATION"
    assert result["warnings"] == [
        {
            "key": "PAGE_01",
            "field": "label",
            "observed": ["STATION_INFORMATION", "MEASUREMENT_TECHNICAL_DATA"],
            "resolved": "STATION_INFORMATION",
            "rule": "legacy_category_priority",
        }
    ]


def test_conflicting_document_roles_are_set_unknown_and_add_warning():
    aggregated_output = [
        {
            "status": "OK",
            "pages": [
                {
                    "key": "PAGE_01",
                    "index": 0,
                    "document_role": "IOL",
                    "label": "DENSITY_MAP",
                }
            ],
        },
        {
            "status": "OK",
            "pages": [
                {
                    "key": "PAGE_01",
                    "index": 0,
                    "document_role": "JOB",
                    "label": "DENSITY_MAP",
                }
            ],
        },
    ]

    result = execute_pytool(aggregated_output)

    assert result["status"] == "OK", result
    assert result["review_required"] is True
    assert result["pages"][0]["document_role"] == "UNKNOWN"
    assert result["warnings"][0]["field"] == "document_role"
    assert result["warnings"][0]["resolved"] == "UNKNOWN"


def test_document_roles_are_preserved_for_distinct_pages():
    aggregated_output = [
        {
            "status": "OK",
            "pages": [
                {
                    "key": "IOL_PAGE",
                    "index": 0,
                    "document_role": "IOL",
                    "label": "DENSITY_MAP",
                },
                {
                    "key": "JOB_PAGE",
                    "index": 1,
                    "document_role": "JOB",
                    "label": "STATION_INFORMATION",
                },
            ],
        }
    ]

    result = execute_pytool(aggregated_output)

    assert result["status"] == "OK", result
    assert result["pages"][0]["document_role"] == "IOL"
    assert result["pages"][1]["document_role"] == "JOB"


def test_iterative_error_is_not_silently_dropped():
    aggregated_output = [
        {"status": "ERROR", "error": "classificazione fallita"}
    ]

    result = execute_pytool(aggregated_output)

    assert result["status"] == "ERROR"
    assert "classificazione fallita" in result["error"]
