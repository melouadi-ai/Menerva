import json
from pathlib import Path


DOUBLE_PDF_DIR = Path(__file__).resolve().parent.parent
SCRIPT_PATH = DOUBLE_PDF_DIR / "pytools" / "diagnose_dispatch_injection.py"
CASE_OUTPUT = (
    DOUBLE_PDF_DIR
    / "tests"
    / "case_6"
    / "outputs"
    / "observed_prepare_pages_clean_sanitized.json"
)


def execute_probe(payload):
    source = SCRIPT_PATH.read_text(encoding="utf-8")
    source = source.replace("{question}", json.dumps(payload, ensure_ascii=False))
    namespace = {}
    exec(compile(source, str(SCRIPT_PATH), "exec"), namespace)
    return json.loads(namespace["result"])


def test_one_page_per_injection_invocation_is_detectable():
    pages = json.loads(CASE_OUTPUT.read_text(encoding="utf-8"))

    reports = [execute_probe(page) for page in pages]

    assert len(reports) == 14
    assert all(report["input_kind"] == "SINGLE_PAGE" for report in reports)
    assert [report["sequence_index"] for report in reports] == list(range(1, 15))
    assert len({report["page_key"] for report in reports}) == 14


def test_whole_root_array_is_identified_as_not_iterated():
    pages = json.loads(CASE_OUTPUT.read_text(encoding="utf-8"))

    report = execute_probe(pages)

    assert report["input_kind"] == "ROOT_ARRAY"
    assert report["item_count"] == 14


def test_deduplicator_wrapper_is_identified_for_comparison():
    pages = json.loads(CASE_OUTPUT.read_text(encoding="utf-8"))

    report = execute_probe({"status": "OK", "pages": pages})

    assert report["input_kind"] == "LV1_WRAPPER"
    assert report["item_count"] == 14


def test_single_item_array_from_injection_is_identified():
    pages = json.loads(CASE_OUTPUT.read_text(encoding="utf-8"))

    report = execute_probe([pages[0]])

    assert report["input_kind"] == "SINGLE_ITEM_ARRAY"
    assert report["sequence_index"] == 1
    assert report["label"] == "DENSITY_MAP"
