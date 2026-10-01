import json
from pathlib import Path


DOUBLE_PDF_DIR = Path(__file__).resolve().parent.parent
SCRIPT_PATH = (
    DOUBLE_PDF_DIR
    / "platforms"
    / "lv1"
    / "scripts"
    / "in_use"
    / "prepare_pages_for_dispatch.py"
)


def execute_preparer(lv1_output):
    source = SCRIPT_PATH.read_text(encoding="utf-8")
    source = source.replace("{edge}[4]", json.dumps(lv1_output, ensure_ascii=False))
    namespace = {}
    exec(compile(source, str(SCRIPT_PATH), "exec"), namespace)
    return json.loads(namespace["result"])


def load_case(case_name):
    path = (
        DOUBLE_PDF_DIR
        / "tests"
        / case_name
        / "outputs"
        / "observed_role_v2_dedup_sanitized.json"
    )
    return json.loads(path.read_text(encoding="utf-8"))


def test_case_6_unwraps_pages_and_attaches_warnings_by_key():
    result = execute_preparer(load_case("case_6"))

    assert isinstance(result, list)
    assert len(result) == 14
    flagged = [page for page in result if page["review_required"]]
    assert [page["key"] for page in flagged] == ["CASE6_PAGE_11", "CASE6_PAGE_12"]
    assert len(flagged[0]["review_warnings"]) == 1
    assert flagged[0]["document_role"] == "JOB"


def test_case_7_unwraps_pages_and_marks_the_single_conflict():
    result = execute_preparer(load_case("case_7"))

    assert isinstance(result, list)
    assert len(result) == 11
    flagged = [page for page in result if page["review_required"]]
    assert [page["key"] for page in flagged] == ["CASE7_PAGE_10"]


def test_non_ok_lv1_output_is_forwarded_as_json_error():
    result = execute_preparer({"status": "ERROR", "error": "bad LV1"})

    assert result["status"] == "ERROR"
    assert "bad LV1" in result["error"]


def test_unknown_role_is_flagged_for_review_without_changing_record():
    result = execute_preparer({
        "status": "OK",
        "warnings": [],
        "pages": [{
            "key": "PAGE_UNKNOWN_ROLE",
            "sequence_index": 1,
            "document_role": "UNKNOWN",
            "label": "MEASUREMENT_TECHNICAL_DATA",
        }],
    })

    assert len(result) == 1
    assert result[0]["label"] == "MEASUREMENT_TECHNICAL_DATA"
    assert result[0]["review_required"] is True
