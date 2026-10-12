"""Verdetto di correttezza del caso 10 (Essity, Collodi): output ADAS vs verita' PDF.

Quarta coppia: `IOL.0188.25` (9 pp) + `JOB.0188.25` (22 pp). Stesso metodo:
verita' = coppia IOL+JOB letta riga per riga.

Particolarita' di questo caso: l'IOL ha **due layout**. Pagine 2-5 mappa DB50
(colonne TAG|DESCRIZIONE|STRUCT|BIT|TIPO|DBX, struct SB/ST2/HW4/HW20/AI/AO),
pagine 7-9 mappa DB100 classica (REG|BIT, ALM/ST). La parte DB100 e' la mappa
di scambio ADAS; la DB50 non ha colonna REG.

Verita' PDF, righe con titolo:

    DB100  REG 1  bit 8,9,10,11,12,13   (DBX 64, 6 allarmi; bianche 14,15,0-7)
    DB100  REG 2  nessun bit            (DBX 66-67 tutte bianche)
    DB100  REG 3  bit 8,10,11,7         (DBX 68-69)
    DB100  REG 4  bit 8,10,13,0,1,2,3,5,6  (DBX 70-71)
    DB100  Misure raw REAL 17 CO, 21 O2 Secco, 33 Temp. fumi  -> 250
    DB100  Misure ing. INT 49 CO, 53 O2 Secco, 65 Temp. fumi  -> 150
    DB100  SET 409-414 (medie CO/NOx/NH3) · CMD 417,418,425,431,432
    (niente XTM/PRM di dettaglio nel documento: zero stimate attese)

JOB.0188.25: stazione `Sistema Analisi Emissioni`; PLC **192.168.1.1:511**
(+502 DCS); gateway 192.168.10.250 e PC .10/MIR .2 da ignorare. Tabella 6:
CO 0-150 (lim 300/375!), O2S 0-25, TF 0-200. QAL non richieste (infatti nessun
comando QAL). Misure 4-20 mA 0...10000 da riscalare: nessuna divisione.
"""
import json
import os
import struct

OBSERVED_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "case_10",
        "outputs",
        "observed_adas_case10_run1.json",
    )
)

# (NAME, registro, formato, TYPE, DRIVERDATA) — solo parte DB100 (20 misure).
PDF_MEASURES_DB100 = [
    ("Ingressi digitali 1", 1, 150, 1, 2),
    ("Ingressi digitali 2", 3, 150, 1, 2),
    ("Ingressi digitali 3", 4, 150, 1, 2),
    ("CO", 17, 250, 0, 0),
    ("O2 Secco", 21, 250, 0, 0),
    ("Temperatura fumi", 33, 250, 0, 0),
    ("CO", 49, 150, 0, 0),
    ("O2 Secco", 53, 150, 0, 0),
    ("Temperatura fumi", 65, 150, 0, 0),
    ("CO: media oraria previsionale", 409, 150, 0, 0),
    ("CO: ultima media oraria archiviata", 410, 150, 0, 0),
    ("NOx: media oraria previsionale", 411, 150, 0, 0),
    ("NOx: ultima media oraria archiviata", 412, 150, 0, 0),
    ("NH3: media oraria previsionale", 413, 150, 0, 0),
    ("NH3: ultima media oraria archiviata", 414, 150, 0, 0),
    ("PC life signal", 417, 150, 6, 5),
    ("Start autocal", 418, 150, 6, 5),
    ("Ack allarmi", 425, 150, 6, 5),
    ("Allarme supero ultima media", 431, 150, 6, 5),
    ("Allarme supero media previsionale", 432, 150, 6, 5),
]

# MEASUREID -> bit con descrizione nel PDF (24 bitinfo totali).
PDF_BITS = {
    4: [8, 9, 10, 11, 12, 13],
    5: [8, 10, 11, 7],
    6: [8, 10, 13, 0, 1, 2, 3, 5, 6],
    19: [0],
    20: [0],
    21: [0],
    22: [0],
    23: [0],
}


def observed():
    with open(OBSERVED_PATH, encoding="utf-8") as f:
        return json.load(f)[0]


def reg_of(m):
    return struct.unpack("<I", bytes.fromhex(m["DRIVERPRIVATE"][2:10]))[0]


def fmt_of(m):
    return struct.unpack("<I", bytes.fromhex(m["DRIVERPRIVATE"][-8:]))[0]


def test_parte_db100_uguale_al_pdf():
    """La parte DB100 (20 misure) coincide riga per riga col PDF."""
    got = [
        (m["NAME"], reg_of(m), fmt_of(m), m["TYPE"], m["DRIVERDATA"])
        for m in observed()["measures"]
        if reg_of(m) not in (160, 168, 192)
    ]
    assert got == PDF_MEASURES_DB100


def test_bitinfo_completi_24():
    got = {}
    for b in observed()["bitinfo"]:
        got.setdefault(b["MEASUREID"], []).append(b["BITNO"])
    assert got == PDF_BITS
    assert len(observed()["bitinfo"]) == 24


def test_misure_ai_db50_registri_inventati_difetto_noto():
    """Difetto nuovo di questa run (classe mai vista): le 3 misure AI della
    mappa DB50 (CO, O2 Secco, Temp. fumi) escono con registri 160/168/192
    copiati dai DBD, ma la mappa DB50 **non ha colonna MODBUS** (verificato
    sulle coordinate: dopo il 16 non c'e' numero). Senza indirizzo di scambio
    non possono stare in ADAS: vanno scartate come le altre righe DB50.
    Il VLM ha inventato il registro e il controllo non l'ha preso perche' e'
    diverso da null/0. Da correggere nel prompt (REG solo da colonna REG)."""
    st = observed()
    by_reg = {reg_of(m): m for m in st["measures"]}
    for r, nome in ((160, "CO"), (168, "O2 Secco"), (192, "Temperatura fumi")):
        assert by_reg[r]["NAME"] == nome
        assert fmt_of(by_reg[r]) == 150


def test_righe_db50_senza_registro_scartate_con_warning():
    """Le 18 righe DB50 senza REG (comandi SB, XTM, stati ST/ST2) sono
    scartate e elencate: la guardia funziona, il difetto sopra e' solo il
    fallback inventato sulle 3 AI."""
    st = observed()
    warn = " ".join(st.get("_warnings", []))
    assert "VARIABILI SENZA INDIRIZZO: 18 variabili" in warn
    for nome in ("PC life signal", "Sistema in misura"):
        assert nome in warn


def test_texton_e_casi_nuovi_pinnati():
    """FAILURE -> ATTIVO (sospetto: da rivedere contro la tabella keyword),
    FAULT -> GUASTO (ok). I due supero escono ALLARME: terza variante dopo
    COMANDO (Rivoli) — la convenzione va fissata col cliente."""
    st = observed()
    got = {b["BITNAME"]: b["TEXTON"] for b in st["bitinfo"]}
    assert got["FAILURE ANALIZZATORE"] == "ATTIVO"
    assert got["FAULT ANALIZZATORE"] == "GUASTO"
    assert got["ALLARME SUPERO ULTIMA MEDIA"] == "ALLARME"
    assert got["ALLARME SUPERO MEDIA PREVISIONALE"] == "ALLARME"
    for b in st["bitinfo"]:
        assert b["TEXTON"] and b["TEXTOFF"], b


def test_unita_range_e_limiti_co():
    """Scale Tabella 6 su tutte le 6 analogiche + le 3 AI (stesso TAG).
    Warning limiti solo CO 300/375, ripetuto sulle 3 misure CO."""
    st = observed()
    by_id = {m["ID"]: m for m in st["measures"]}
    assert (by_id[1]["UNITS"], by_id[1]["LOWRANGE"], by_id[1]["HIGHRANGE"]) == ("mg/Nm3", 0.0, 150.0)
    assert (by_id[2]["UNITS"], by_id[2]["LOWRANGE"], by_id[2]["HIGHRANGE"]) == ("%", 0.0, 25.0)
    assert (by_id[3]["UNITS"], by_id[3]["LOWRANGE"], by_id[3]["HIGHRANGE"]) == ("°C", 0.0, 200.0)
    assert (by_id[7]["UNITS"], by_id[10]["UNITS"]) == ("mg/Nm3", "mg/Nm3")
    warn = " ".join(st.get("_warnings", []))
    assert warn.count("giornaliero=300, orario=375") == 3
    assert "DIVISIONE" not in warn


def test_stazione_e_ip_senza_gateway():
    st = observed()
    assert st["NAME"] == "Sistema Analisi Emissioni"
    assert 'ipaddress="192.168.1.1"' in st["DRIVERCONFIG"]
    assert 'tcpport="511"' in st["DRIVERCONFIG"]
    blob = json.dumps(st)
    for vietato in ("192.168.10.250", "192.168.1.2", "192.168.1.10"):
        assert vietato not in blob
    assert len([st]) == 1
