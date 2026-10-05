import json
from pathlib import Path


DOUBLE_PDF_DIR = Path(__file__).resolve().parent.parent
SCRIPT_PATH = (
    DOUBLE_PDF_DIR
    / "platforms"
    / "lv1"
    / "scripts"
    / "updated_pending_validation"
    / "consolidate_to_intermediate.py"
)
CASE_DIR = DOUBLE_PDF_DIR / "tests" / "case_6"


def run_consolidator(station_pages, measure_pages, density_pages):
    source = SCRIPT_PATH.read_text(encoding="utf-8")
    source = source.replace(
        "station_raw = r'''{edge}[10]'''.strip()",
        "station_raw = " + json.dumps(json.dumps(station_pages, ensure_ascii=False)),
        1,
    )
    source = source.replace(
        "measure_raw = r'''{edge}[11]'''.strip()",
        "measure_raw = " + json.dumps(json.dumps(measure_pages, ensure_ascii=False)),
        1,
    )
    source = source.replace(
        "density_raw = r'''{edge}[12]'''.strip()",
        "density_raw = " + json.dumps(json.dumps(density_pages, ensure_ascii=False)),
        1,
    )
    namespace = {}
    exec(compile(source, str(SCRIPT_PATH), "exec"), namespace)
    return json.loads(namespace["result"])


def assembled_page(sequence_index, stations, review=None):
    return {
        "diagnostic": "LV2_MEASUREMENT_ASSEMBLY",
        "status": "OK",
        "page": {
            "key": "CASE6_PAGE_%02d" % sequence_index,
            "sequence_index": sequence_index,
            "document_role": "JOB",
            "label": "MEASUREMENT_TECHNICAL_DATA",
            "stations": stations,
            "review_required": bool(review),
        },
        "review": review or [],
        "counters": {},
    }


def station_page(station_info):
    return {
        "key": "CASE6_PAGE_06",
        "sequence_index": 6,
        "document_role": "JOB",
        "label": "STATION_INFORMATION",
        "review_required": 0,
        "review_warnings": "[ ]",
        "station_info": station_info,
    }


def test_single_plc_links_scales_and_maps_kinds():
    station_pages = [
        station_page([{
            "nome_stazione": None, "stazione": None, "protocollo": "ModBus TCP",
            "ip_plc": "10.100.50.95", "port": 511, "campi_scala": [],
        }]),
        station_page([{
            "nome_stazione": None, "stazione": None, "protocollo": None,
            "ip_plc": None, "port": None,
            "campi_scala": [
                {"segnale": "SO2", "tag": "SO2", "campo_da": 0, "campo_a": 300},
                {"segnale": "Temperatura fumi", "tag": "TF", "campo_da": 0, "campo_a": 100},
            ],
        }]),
    ]
    measure_pages = [
        assembled_page(2, [{
            "NAME": "SME", "DRIVERNAME": "modbusplc", "DRIVERCONFIG": ":",
            "ID": 1,
            "measures": [
                {"NAME": "SO2", "UNITS": None, "DRIVERDATA": 0, "TYPE": 0,
                 "ID": 1, "MODBUSREGISTRO": 49, "BIT": None,
                 "TEXTON": None, "TEXTOFF": None},
                {"NAME": "SO2 Raw", "UNITS": None, "DRIVERDATA": 0, "TYPE": 0,
                 "ID": 1, "MODBUSREGISTRO": 17, "BIT": None,
                 "TEXTON": None, "TEXTOFF": None},
                {"NAME": "PC life signal", "UNITS": None, "DRIVERDATA": 5,
                 "TYPE": 6, "ID": 1, "MODBUSREGISTRO": 417, "BIT": 0,
                 "TEXTON": "Attivo", "TEXTOFF": "OFF"},
                {"NAME": "Allarme sonda riscaldata", "UNITS": None,
                 "DRIVERDATA": 2, "TYPE": 1, "ID": 1, "MODBUSREGISTRO": 1,
                 "BIT": 8, "TEXTON": "Allarme", "TEXTOFF": "OFF"},
            ],
        }]),
    ]
    result = run_consolidator(station_pages, measure_pages, [])
    assert result["status"] == "OK", result
    assert len(result["stations"]) == 1
    station = result["stations"][0]
    assert station["ip"] == "10.100.50.95"
    assert station["port"] == 511
    assert station["protocol"] == "ModBus TCP"
    assert len(station["variables"]) == 4
    by_name = {v["description"]: v for v in station["variables"]}
    assert by_name["SO2"]["kind"] == "ANALOGICA"
    assert by_name["SO2"]["scale_eng_start"] == 0
    assert by_name["SO2"]["scale_eng_end"] == 300
    assert by_name["SO2 Raw"]["scale_eng_start"] == 0
    assert by_name["PC life signal"]["kind"] == "DIGITALE_SINGOLO"
    assert by_name["PC life signal"]["read_write"] == "W"
    assert by_name["Allarme sonda riscaldata"]["kind"] == "DIGITALE_IMPACCATO"
    assert by_name["Allarme sonda riscaldata"]["bit"] == 8
    assert by_name["Allarme sonda riscaldata"]["state_on"] == "Allarme"
    assert [s["tag"] for s in result["unmatched_scales"]] == ["TF"]
    assert result["counters"]["scales_linked"] == 2
    assert result["counters"]["variables_total"] == 4


def test_multi_ip_keeps_first_and_flags_review():
    station_pages = [
        station_page([{
            "nome_stazione": "A", "stazione": None, "protocollo": "ModBus TCP",
            "ip_plc": "10.0.0.1", "port": 502, "campi_scala": [],
        }]),
        station_page([{
            "nome_stazione": "B", "stazione": None, "protocollo": "ModBus TCP",
            "ip_plc": "10.0.0.2", "port": 502, "campi_scala": [],
        }]),
    ]
    measure_pages = [
        assembled_page(2, [{
            "NAME": "X", "DRIVERNAME": "modbusplc", "DRIVERCONFIG": ":",
            "ID": 1, "measures": [
                {"NAME": "M", "UNITS": None, "DRIVERDATA": 0, "TYPE": 0,
                 "ID": 1, "MODBUSREGISTRO": 1, "BIT": None,
                 "TEXTON": None, "TEXTOFF": None},
            ],
        }]),
    ]
    result = run_consolidator(station_pages, measure_pages, [])
    assert result["status"] == "OK", result
    assert len(result["stations"]) == 1
    assert result["stations"][0]["ip"] == "10.0.0.1"
    rules = [r["rule"] for r in result["review"]]
    assert "multi_plc_unresolved" in rules


def test_empty_branches_and_dict_inputs_tolerated():
    result = run_consolidator([], [], [])
    assert result["status"] == "OK", result
    assert result["stations"][0]["variables"] == []
    assert result["stations"][0]["ip"] is None
    result = run_consolidator(
        [], [],
        {"key": "K", "sequence_index": 1, "document_role": "JOB",
         "label": "DENSITY_MAP", "review_required": False, "review_warnings": []},
    )
    assert result["status"] == "OK", result
    assert result["counters"]["density_pages"] == 1


def test_error_page_fails_fast_with_sequence():
    bad_page = assembled_page(8, [])
    bad_page["status"] = "ERROR"
    bad_page["error"] = "boom"
    result = run_consolidator([], [bad_page], [])
    assert result["status"] == "ERROR"
    assert "8" in result["error"]


def test_duplicate_measures_kept_with_review():
    measures = [
        {"NAME": "M", "UNITS": None, "DRIVERDATA": 0, "TYPE": 0,
         "ID": 1, "MODBUSREGISTRO": 1, "BIT": None,
         "TEXTON": None, "TEXTOFF": None},
    ]
    measure_pages = [
        assembled_page(2, [{
            "NAME": "S", "DRIVERNAME": "modbusplc", "DRIVERCONFIG": ":",
            "ID": 1, "measures": measures,
        }]),
        assembled_page(3, [{
            "NAME": "S", "DRIVERNAME": "modbusplc", "DRIVERCONFIG": ":",
            "ID": 1, "measures": measures,
        }]),
    ]
    result = run_consolidator([], measure_pages, [])
    assert result["status"] == "OK", result
    assert len(result["stations"][0]["variables"]) == 2
    rules = [r["rule"] for r in result["review"]]
    assert "duplicate_measures_kept" in rules
