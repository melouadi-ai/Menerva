import json
from pathlib import Path


DOUBLE_PDF_DIR = Path(__file__).resolve().parent.parent
SCRIPT_PATH = DOUBLE_PDF_DIR / "pytools" / "dispatch_classified_pages.py"


def execute_dispatcher(page_input):
    source = SCRIPT_PATH.read_text(encoding="utf-8")
    source = source.replace("{question}", json.dumps(page_input, ensure_ascii=False))
    namespace = {}
    exec(compile(source, str(SCRIPT_PATH), "exec"), namespace)
    return namespace["result"]


def test_case_6_pages_emit_exact_category_strings():
    path = (
        DOUBLE_PDF_DIR
        / "tests"
        / "case_6"
        / "outputs"
        / "observed_role_v2_dedup_sanitized.json"
    )
    observed = json.loads(path.read_text(encoding="utf-8"))

    results = [execute_dispatcher(page) for page in observed["pages"]]

    assert results == [page["label"] for page in observed["pages"]]
    assert results.count("DENSITY_MAP") == 1
    assert results.count("MEASUREMENT_TECHNICAL_DATA") == 7
    assert results.count("STATION_INFORMATION") == 6


def test_case_7_pages_emit_exact_category_strings():
    path = (
        DOUBLE_PDF_DIR
        / "tests"
        / "case_7"
        / "outputs"
        / "observed_role_v2_dedup_sanitized.json"
    )
    observed = json.loads(path.read_text(encoding="utf-8"))

    results = [execute_dispatcher(page) for page in observed["pages"]]

    assert results == [page["label"] for page in observed["pages"]]
    assert results.count("DENSITY_MAP") == 1
    assert results.count("MEASUREMENT_TECHNICAL_DATA") == 5
    assert results.count("STATION_INFORMATION") == 5


def test_single_page_lv1_wrapper_is_accepted():
    result = execute_dispatcher({
        "status": "OK",
        "pages": [{
            "key": "CASE_PAGE_01",
            "sequence_index": 1,
            "document_role": "IOL",
            "label": "DENSITY_MAP",
        }],
    })

    assert result == "DENSITY_MAP"


def test_multiple_pages_in_one_iteration_return_nonmatching_error_string():
    result = execute_dispatcher({
        "status": "OK",
        "pages": [
            {"key": "PAGE_01", "label": "DENSITY_MAP"},
            {"key": "PAGE_02", "label": "STATION_INFORMATION"},
        ],
    })

    assert result.startswith("ERROR: ")
    assert "una pagina per iterazione" in result


def test_unknown_category_does_not_match_any_conditional_branch():
    result = execute_dispatcher({
        "key": "PAGE_UNKNOWN",
        "label": "UNKNOWN",
    })

    assert result.startswith("ERROR: ")
    assert "Categoria non ammessa" in result
