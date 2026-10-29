"""Regressioni note Single PDF: bit 40014, unita, IP, refusi (Task 6).

Pinnano, sulla pipeline consolidatore (Task 4) + JSON CREATOR v15 (Task 5),
i quattro difetti diagnosticati sugli output storici:

- 40014: il PDF (SIEMENS_2, pagina 5) ha 16 bit in ordine 8..15, 0..7;
  la pipeline non deve rinumerare, perdere o copiare bit dalla riga
  sbagliata (fedelta V23/V26 + precedenza ramo nomi-bit, Task 2/4).
- Unita: la cella con la sola parola-intestazione "Unita" non e' un'unita
  (V3 v14); le unita reali ("mg/Nm3", "%") arrivano in UNITS oppure il
  nome resta intatto con le parentesi (V19 vince su P5, Task 5).
- IP: nessun 127.0.0.1 fabbricato senza warning (il creator avvisa).
- Refusi: policy esplicita di trascrizione fedele — il codice
  deterministico non corregge mai l'ortografia ("Ossiegno" resta);
  l'unica trasformazione sui bit e' l'uppercase del BITNAME.
"""

import io
import json
import re
import struct
import sys
from pathlib import Path

REPO = Path(__file__).parent.parent
sys.path.insert(0, str(REPO / "src"))

from nodes.single_consolidator import consolidate  # noqa: E402

SRC = REPO / "src" / "nodes" / "json_creator.py"
MEASURES_PROMPT = REPO / "src" / "prompts" / "vlm_measures_v14.md"

EXPECTED_BITS_40014 = [8, 9, 10, 11, 12, 13, 14, 15, 0, 1, 2, 3, 4, 5, 6, 7]

# Verita dal PDF: myhydra/single_pdf/verifica_pdf/per_caso/caso_4_siemens_2/
# tabella_pdf.json, registro 40014, pagina 5, nell'ordine di riga del PDF.
PDF_40014_ROWS = [
    (8, "COG2: ALLARME TEMPERATURA SONDA DI PRELIEVO"),
    (9, "COG2: ALLARME TEMPERATURA LINEA DI PRELIEVO"),
    (10, "COG2: BLOCCO ALTISSIME TEMPERATURE In"),
    (11, "COG2: ALLARME FRIGO"),
    (12, "COG2: ALLARME PRESENZA CONDENSA"),
    (13, "COG2: MEMORIA PRESENZA CONDENSA (Da"),
    (14, "COG2: PSL BASSA PRESSIONE GAS DI MISURA"),
    (15, "COG2: SELETTORE MANUTENZIONE"),
    (0, "COG2: SCATTO INTERRUTTORI"),
    (1, "COG2: ALLARME CONVERTITORE NO2/NO"),
    (2, 'COG2: ANOMALIA ANALIZZATORE U23 "CO"'),
    (3, 'COG2: ALLARME BAD_QUALITY MISURA "CO"'),
    (4, 'COG2: ANOMALIA ANALIZZATORE U23 "NO"'),
    (5, 'COG2: ALLARME BAD_QUALITY MISURA "NO"'),
    (6, 'COG2: ANOMALIA ANALIZZATORE U23 "O2"'),
    (7, 'COG2: ALLARME BAD_QUALITY MISURA "O2"'),
]


def _var(description, riga, reg=None, bit=None, kind="ANALOGICA",
         zona="ALLARMI", units=None, **extra):
    v = {"description": description, "units": units,
         "modbus_register": reg, "bit": bit, "data_type": None,
         "kind": kind, "read_write": "R", "state_on": None,
         "state_off": None, "scale_elec_start": None,
         "scale_elec_end": None, "scale_eng_start": None,
         "scale_eng_end": None, "limit_hour": None, "limit_day": None,
         "zona": zona, "tag": None, "pagina": None, "riga": riga}
    v.update(extra)
    return v


def _station(ip, variables, name="SME"):
    return {"name": name, "protocol": "ModBus TCP", "ip": ip, "port": 502,
            "modbus_id": 1, "variables": variables}


def run_creator(intermediate):
    source = SRC.read_text(encoding="utf-8")
    patched = re.sub(r"raw\s*=\s*r?'''\{edge\}\[\d+\]'''",
                     "raw = __INJECTED_RAW__", source)
    assert patched != source
    ns = {"__INJECTED_RAW__": intermediate}
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        exec(compile(patched, str(SRC), "exec"), ns)
    finally:
        sys.stdout = old_stdout
    return json.loads(ns.get("output", "null"))


def pipeline(pages):
    unified = consolidate(pages)
    return run_creator({"stations": unified["stations"]})


def page_40014_pdf_truth():
    measures = [_var(desc, riga + 1, reg=40014, bit=bit,
                     kind="DIGITALE_IMPACCATO")
                for riga, (bit, desc) in enumerate(PDF_40014_ROWS)]
    bitnames = [{"description": desc, "modbus_register": 40014,
                 "bit": bit, "riga": riga + 1}
                for riga, (bit, desc) in enumerate(PDF_40014_ROWS)]
    return {"page_no": 5,
            "stations": [_station("192.168.2.11", measures)],
            "bitnames": {"rows": bitnames}}


def output_40014():
    return pipeline([page_40014_pdf_truth()])


def reg_of_measure(measure):
    return struct.unpack(
        "<I", bytes.fromhex(measure["DRIVERPRIVATE"][2:10]))[0]


def bits_of(output, reg):
    target = next(m["ID"] for m in output[0]["measures"]
                  if reg_of_measure(m) == reg)
    return [b["BITNO"] for b in output[0]["bitinfo"]
            if b["MEASUREID"] == target]


def bitnames_of(output, reg):
    target = next(m["ID"] for m in output[0]["measures"]
                  if reg_of_measure(m) == reg)
    return [b["BITNAME"] for b in output[0]["bitinfo"]
            if b["MEASUREID"] == target]


def test_40014_sedici_bit_come_pdf():
    assert bits_of(output_40014(), 40014) == EXPECTED_BITS_40014


def test_40014_nomi_bit_fedeli_alla_riga_del_pdf():
    got = bitnames_of(output_40014(), 40014)
    assert got == [desc.upper() for _, desc in PDF_40014_ROWS]


def test_unita_reali_in_units_e_nome_con_parentesi_intatto():
    out = pipeline([{"page_no": 1, "stations": [_station("10.0.0.1", [
        _var("Polveri", 1, reg=40001, units="mg/Nm3", zona="MISURE"),
        _var("Polveri (GR)", 2, reg=40002, units="mg/Nm3", zona="MISURE"),
        _var("O2 secco", 3, reg=40003, units="%", zona="MISURE"),
    ])]}])
    by_name = {m["NAME"]: m for m in out[0]["measures"]}
    assert by_name["Polveri"]["UNITS"] == "mg/Nm3"
    assert by_name["Polveri"]["UNITS2"] == "mg/Nm3"
    assert "Polveri (GR)" in by_name
    assert by_name["Polveri (GR)"]["UNITS"] == "mg/Nm3"
    assert by_name["O2 secco"]["UNITS"] == "%"


def test_v14_v3_parola_unita_non_e_unita_valida():
    text = MEASURES_PROMPT.read_text(encoding="utf-8")
    assert 'header word "Unità" with no real unit → null' in text
    assert '"Nm³/h", "Unità"' not in text


def test_parola_intestazione_unita_non_finisce_in_units():
    out = pipeline([{"page_no": 1, "stations": [_station("10.0.0.1", [
        _var("Polveri (GR)", 1, reg=40001, units="Unità", zona="MISURE"),
        _var("Polveri TQ", 2, reg=40002, units="Unita", zona="MISURE"),
    ])]}])
    by_name = {m["NAME"]: m for m in out[0]["measures"]}
    assert by_name["Polveri (GR)"]["UNITS"] is None
    assert by_name["Polveri (GR)"]["UNITS2"] is None
    assert by_name["Polveri TQ"]["UNITS"] is None
    assert by_name["Polveri TQ"]["UNITS2"] is None


def test_nessun_ip_fabbricato():
    out = pipeline([{"page_no": 1, "stations": [_station(None, [
        _var("Polveri", 1, reg=40001, zona="MISURE"),
    ])]}])
    assert 'ipaddress="127.0.0.1"' not in out[0]["DRIVERCONFIG"]
    assert 'ipaddress=""' in out[0]["DRIVERCONFIG"]
    warnings = out[0].get("_warnings", [])
    assert any("nessun IP dichiarato nel documento" in w
               for w in warnings)


def test_ip_dichiarato_usato_senza_default():
    out = pipeline([{"page_no": 1, "stations": [_station("192.168.0.1", [
        _var("Polveri", 1, reg=40001, zona="MISURE"),
    ])]}])
    assert 'ipaddress="192.168.0.1"' in out[0]["DRIVERCONFIG"]
    assert all("nessun IP dichiarato" not in w
               for w in out[0].get("_warnings", []))


def test_refusi_trascritti_fedelmente_mai_corretti():
    out = pipeline([{"page_no": 1, "stations": [_station("10.0.0.1", [
        _var("Allarme 1 Ossiegno umido", 1, reg=40001, bit=2,
             kind="DIGITALE_IMPACCATO", zona="MISURE"),
        _var("Allarme 1 Ossiegno umido", 2, reg=40002, zona="MISURE"),
    ])], "bitnames": {"rows": [
        {"description": "Allarme 1 Ossiegno umido",
         "modbus_register": 40001, "bit": 2, "riga": 1},
    ]}}])
    bitname = bitnames_of(out, 40001)[0]
    assert bitname == "ALLARME 1 OSSIEGNO UMIDO"
    assert "OSSIGENO" not in bitname
    names = [m["NAME"] for m in out[0]["measures"]]
    assert "Allarme 1 Ossiegno umido" in names
