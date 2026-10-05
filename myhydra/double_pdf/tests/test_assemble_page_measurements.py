import json
from pathlib import Path


DOUBLE_PDF_DIR = Path(__file__).resolve().parent.parent
SCRIPT_PATH = (
    DOUBLE_PDF_DIR
    / "platforms"
    / "lv2"
    / "measurement"
    / "scripts"
    / "updated_pending_validation"
    / "assemble_page_measurements.py"
)
CASE_DIR = DOUBLE_PDF_DIR / "tests" / "case_6"


def run_assembler(page, measures_out, bitinfo_out, states_out):
    source = SCRIPT_PATH.read_text(encoding="utf-8")
    source = source.replace(
        "page_raw = r'''{question}'''.strip()",
        "page_raw = " + json.dumps(json.dumps(page, ensure_ascii=False)),
        1,
    )
    source = source.replace(
        "meas_raw = r'''{edge}[7]'''.strip()",
        "meas_raw = " + json.dumps(json.dumps(measures_out, ensure_ascii=False)),
        1,
    )
    source = source.replace(
        "bitn_raw = r'''{edge}[8]'''.strip()",
        "bitn_raw = " + json.dumps(json.dumps(bitinfo_out, ensure_ascii=False)),
        1,
    )
    source = source.replace(
        "bits_raw = r'''{edge}[9]'''.strip()",
        "bits_raw = " + json.dumps(json.dumps(states_out, ensure_ascii=False)),
        1,
    )
    namespace = {}
    exec(compile(source, str(SCRIPT_PATH), "exec"), namespace)
    return json.loads(namespace["result"])


def envelope(branch, page, vlm_output):
    return {
        "diagnostic": "LV2_MEASUREMENT_BRANCH",
        "status": "OK",
        "branch": branch,
        "page": page,
        "output_format": "JSON",
        "vlm_output": vlm_output,
    }


def station_shell(bitinfo_rows):
    return [{
        "NAME": "SME", "DRIVERNAME": "modbusplc", "DRIVERCONFIG": ":",
        "ID": 1, "measures": [], "bitinfo": bitinfo_rows,
    }]


def bitinfo_row(mid, bitno, name):
    return {"MEASUREID": mid, "BITNO": bitno, "BITNAME": name}


def states_row(mid, bitno, texton, textoff="OFF"):
    return {"MEASUREID": mid, "BITNO": bitno, "TEXTON": texton, "TEXTOFF": textoff}


SERIE_BITINFO_P2 = [
    (1, 8, "Allarme sonda riscaldata"), (1, 9, "Allarme linea riscaldata"),
    (1, 10, "Allarme frigorifero"), (1, 11, "Allarme presenza condensa"),
    (1, 12, "Allarme mancanza flusso"), (1, 13, "Allarme analizzatore SO2"),
    (1, 0, "Sistema in misura"), (1, 1, "Calibrazione automatica in corso"),
    (1, 2, "Analizzatore SO2 in calibrazione di zero"),
    (1, 3, "Analizzatore SO2 in calibrazione di span"),
    (1, 7, "Secondo campo SO2"),
    (1, 8, "QAL3 in corso"), (1, 9, "QAL3: elettrovalvola ARIA"),
    (1, 10, "QAL3: elettrovalvola span SO2"), (1, 11, "QAL3: lavaggio con N2"),
    (1, 13, "QAL3: ciclo concluso senza errori"),
    (1, 14, "QAL3: ciclo concluso con errori"), (1, 15, "Pompa analisi"),
    (4, 8, "Stato elettrovalvola cal zero"), (4, 9, "Stato elettrovalvola N2"),
    (4, 10, "Stato elettrovalvola cal span"), (4, 11, "Elettrovalvola cal da sonda"),
    (4, 13, "PLC life signal"),
    (4, 0, "Impianto in marcia"),
    (4, 1, "Impianto in minimo tecnico/funzionamento anomalo"),
    (4, 2, "Impianto in avviamento"), (4, 3, "Impianto in spegnimento"),
    (4, 5, "SME in manutenzione"), (4, 6, "Impianto in manutenzione"),
    (4, 7, "Impianto fuori servizio per guasto"),
]

SERIE_STATES_P2 = (
    [(1, b, "Allarme") for b in (8, 9, 10, 11, 12, 13)]
    + [(1, b, "Allarme") for b in (8, 9, 10, 11, 12, 13, 14, 15)]
    + [(2, b, "Allarme") for b in (8, 9, 10, 11, 12, 13, 14, 15)]
    + [(3, 8, "Misura"), (3, 9, "Calibrazione"), (3, 10, "Zero"), (3, 11, "Span"),
       (3, 15, "Attivo"), (3, 0, "Attivo"), (3, 1, "Aperto"), (3, 2, "Aperto"),
       (3, 3, "Attivo"), (3, 5, "OK"), (3, 6, "Guasto"), (3, 7, "Attivo")]
    + [(4, 8, "Aperto"), (4, 9, "Aperto"), (4, 10, "Aperto"), (4, 11, "Aperto"),
       (4, 13, "Attivo"), (4, 0, "Marcia"), (4, 1, "Anomalia"), (4, 2, "Avviamento"),
       (4, 3, "Spegnimento"), (4, 4, "Spegnimento"), (4, 5, "Manutenzione"),
       (4, 6, "Manutenzione"), (4, 7, "Guasto")]
)

SERIE_BITINFO_P3 = (
    [(5, 8, "Blocco da BSS2"), (5, 9, "Allarme bassa portata FT-2611"),
     (5, 10, "Allarme bassa portata FT-310"), (5, 11, "Allarme bassa portata FT-313"),
     (5, 12, "AI303A allarme basso pH"), (5, 13, "AI303B allarme basso pH"),
     (5, 14, "AI2602A allarme basso pH"), (5, 15, "AI2602B allarme basso pH"),
     (5, 0, "PM-302A in marcia"), (5, 1, "PM-302B in marcia"),
     (5, 2, "PM-310A in marcia"), (5, 3, "PM-310B in marcia"),
     (5, 4, "PM-2600A in marcia"), (5, 5, "PM-2600B in marcia"),
     (5, 6, "PM-2601A in marcia"), (5, 7, "PM-2601B in marcia"),
     (6, 8, "PM-2604A in marcia"), (6, 9, "PM-2604B in marcia"),
     (6, 10, "Ventilatore VN-400 in marcia"), (6, 11, "Ventilatore VN-2504 in marcia"),
     (6, 12, "Ventilatore 514K1 in marcia"), (6, 13, "Ventilatore 514K2 in marcia"),
     (6, 0, "Ventilatore VN-400 in marcia"), (6, 1, "Ventilatore VN-2504 in marcia"),
     (6, 2, "Ventilatore 514K1 in marcia"), (6, 3, "Ventilatore 514K2 in marcia")]
)

SERIE_STATES_P3 = (
    [(5, b, "Allarme") for b in (8, 9, 10, 11, 12, 13, 14, 15)]
    + [(5, 1, "Marcia"), (5, 2, "Marcia"), (5, 4, "Marcia"), (5, 5, "Marcia")]
    + [(6, b, "Marcia") for b in (8, 9, 10, 11, 12, 13)]
    + [(6, b, "Marcia") for b in (0, 1, 2, 3)]
)

SERIE_BITINFO_P4 = [
    (417, 0, "PC life signal"), (418, 0, "Start autocal"),
    (419, 0, "Stop autocal"), (425, 0, "Ack allarmi"),
    (426, 0, "Impianto in manutenzione"),
    (427, 0, "Impianto fuori servizio per guasto"),
    (431, 0, "Allarme supero ultima media"),
    (432, 0, "Allarme supero media previsionale"),
]

SERIE_STATES_P4 = (
    [(417, 0, "Attivo"), (418, 0, "Start"), (419, 0, "Stop")]
    + [(b, 0, "Attivo") for b in (420, 421, 422, 423, 424)]
    + [(425, 0, "Ack"), (426, 0, "Manutenzione"), (427, 0, "Guasto")]
    + [(b, 0, "Attivo") for b in (428, 429, 430)]
    + [(431, 0, "Allarme"), (432, 0, "Allarme")]
)


def load_serie_measures():
    data = json.loads(
        (CASE_DIR / "outputs" / "observed_lv2_measurement_qwen38_serie_measures_sanitized.json")
        .read_text(encoding="utf-8")
    )
    return {r["page"]["sequence_index"]: r for r in data["records"]}


def test_page_2_attaches_bits_and_flags_conflicts():
    serie = load_serie_measures()
    page = serie[2]["page"]
    measures_out = serie[2]["vlm_output"]
    bitinfo_out = station_shell([bitinfo_row(*t) for t in SERIE_BITINFO_P2])
    states_out = station_shell([states_row(m, b, t) for m, b, t in SERIE_STATES_P2])
    result = run_assembler(page, measures_out, bitinfo_out, states_out)
    assert result["status"] == "OK", result
    out_page = result["page"]
    assert out_page["review_required"] is True
    measures = out_page["stations"][0]["measures"]
    assert len(measures) == 30
    by_name = {m["NAME"]: m for m in measures}
    assert by_name["Allarme sonda riscaldata"]["BIT"] == 8
    assert by_name["Allarme sonda riscaldata"]["TEXTON"] == "Allarme"
    assert by_name["QAL3 in corso"]["BIT"] == 0
    assert by_name["Secondo campo SO2"]["BIT"] == 15
    assert by_name["Pompa analisi"]["BIT"] == 7
    rules = [r["rule"] for r in result["review"]]
    assert "bit_conflicts" in rules
    assert result["counters"]["dropped_empty_bitinfo"] == 0


def test_page_3_merges_stations_and_uses_measures_bit():
    serie = load_serie_measures()
    page = serie[3]["page"]
    measures_out = serie[3]["vlm_output"]
    assert len(measures_out) == 3
    bitinfo_out = station_shell([bitinfo_row(*t) for t in SERIE_BITINFO_P3])
    states_out = station_shell([states_row(*t) for t in SERIE_STATES_P3])
    result = run_assembler(page, measures_out, bitinfo_out, states_out)
    assert result["status"] == "OK", result
    stations = result["page"]["stations"]
    assert len(stations) == 1
    measures = stations[0]["measures"]
    assert len(measures) == 27
    by_name = {m["NAME"]: m for m in measures}
    assert by_name["PM-302A in marcia"]["BIT"] == 1
    assert by_name["PM-302A in marcia"]["TEXTON"] is None
    assert by_name["Blocco da BSS2"]["BIT"] == 8
    assert by_name["Blocco da BSS2"]["TEXTON"] == "Allarme"
    assert by_name["Ventilatore VN-400 in marcia"]["BIT"] == 0
    assert result["counters"]["merged_stations"] == 2
    rules = [r["rule"] for r in result["review"]]
    assert "bit_conflicts" in rules
    assert "unverified_bits" not in rules


def test_page_4_cmd_rows_get_bit_zero_and_reserved_states_dropped():
    serie = load_serie_measures()
    page = serie[4]["page"]
    measures_out = serie[4]["vlm_output"]
    bitinfo_out = station_shell([bitinfo_row(*t) for t in SERIE_BITINFO_P4])
    states_out = station_shell([states_row(*t) for t in SERIE_STATES_P4])
    result = run_assembler(page, measures_out, bitinfo_out, states_out)
    assert result["status"] == "OK", result
    measures = result["page"]["stations"][0]["measures"]
    assert len(measures) == 11
    by_name = {m["NAME"]: m for m in measures}
    assert by_name["PC life signal"]["BIT"] == 0
    assert by_name["PC life signal"]["TEXTON"] == "Attivo"
    assert by_name["Ack allarmi"]["BIT"] == 0
    assert by_name["SO2"]["BIT"] is None
    assert by_name["SO2"]["TEXTON"] is None
    assert result["counters"]["dropped_reserved_states"] == 8
    assert result["review"] == []


def test_empty_branches_assemble_to_empty_stations():
    serie = load_serie_measures()
    page = serie[8]["page"]
    result = run_assembler(page, serie[8]["vlm_output"], [], [])
    assert result["status"] == "OK", result
    assert result["page"]["stations"] == []
    assert result["page"]["review_required"] is False


def test_branch_error_fails_fast_with_branch_name():
    serie = load_serie_measures()
    page = serie[2]["page"]
    result = run_assembler(
        page, "non json {", serie[2]["vlm_output"], serie[2]["vlm_output"]
    )
    assert result["status"] == "ERROR"
    assert "MEASURES_BISON" in result["error"]
