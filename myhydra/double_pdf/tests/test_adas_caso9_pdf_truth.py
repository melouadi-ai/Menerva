"""Verdetto di correttezza del caso 9 (San Marco, Catania): output ADAS vs verita' PDF.

Quinta coppia: `IOL.0007.18.02` (7 pp) + `JOB.0007.18` (21 pp). Metodo solito:
verita' = coppia letta riga per riga. Due avvertenze sul documento:

* Il file si chiama `.02` ma dentro dichiara `IOL.0187.25` (stale/rinumerata).
  Il JOB assegna `.01` alle caldaie e **`.02` ai motori**: i fogli dicono
  "Caldaia GV2/GV3" ma il riferimento ufficiale e' motori (vedi test stazione).
* La scheda pre-run aveva due errori di lettura (SET 401/402 con titolo
  dimenticati; righe Scansione 0-3 non viste): l'output ha ragione lui,
  qui valgono **35 misure e 50 bitinfo**.

Verita' PDF, righe con titolo:

    GV2  REG 1  bit 8-15 (8 allarmi) · REG 2 nessuno · REG 3 bit 8,9,10,11,0,1,2,3,6,7 (10)
    GV2  REG 4  bit 8,10,11,12,13,14,0,1,2,3,5,6 (12)
    GV2  REAL 17 CO, 19 NO, 21 O2 Secco, 33 Temp. fumi (250)
    GV2  SET 401,402,409,410,411,412 (150) · CMD 417,418,419,424,425,429,430,431,432
    GV3  REG 81 bit 8-15 (8) · REG 82/83/84 nessuno
    GV3  REAL 97 CO, 99 NO, 101 O2 Secco, 113 Temp. fumi, 125 Portata gas (250, senza scala)
    GV3  SET 457-460 · CMD 478,479,480 · XTM 481-496 tutte bianche (zero stimate)

JOB (motori, Tab 13): CO 0-600 (200/250), NO 0-500 (100/125), O2S 0-25%,
TF 0-600. Misure in float ingegneristici: nessuna divisione.
"""
import json
import os
import struct

OBSERVED_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "case_9",
        "outputs",
        "observed_adas_case9_run1.json",
    )
)

# (NAME, registro, formato, TYPE, DRIVERDATA) — DD=1 sulle 5 del test dedicato.
PDF_MEASURES = [
    ("Ingressi digitali 1", 1, 150, 1, 2),
    ("Ingressi digitali 2", 3, 150, 1, 2),
    ("Ingressi digitali 3", 4, 150, 1, 2),
    ("CO", 17, 250, 0, 0),
    ("NO", 19, 250, 0, 0),
    ("O2 Secco", 21, 250, 0, 0),
    ("Temperatura fumi", 33, 250, 0, 0),
    ("Tempo di scansione", 401, 150, 0, 0),
    ("Tempo di lavaggio", 402, 150, 0, 0),
    ("CO: media oraria previsionale", 409, 150, 0, 0),
    ("CO: ultima media oraria archiviata", 410, 150, 0, 0),
    ("NOx: media oraria previsionale", 411, 150, 0, 0),
    ("NOx: ultima media oraria archiviata", 412, 150, 0, 0),
    ("PC life signal", 417, 150, 6, 5),
    ("Start autocal", 418, 150, 6, 5),
    ("Stop autocal", 419, 150, 6, 5),
    ("Bypass convertitore", 424, 150, 6, 5),
    ("Ack allarmi", 425, 150, 6, 1),
    ("Scansione automatica", 429, 150, 6, 1),
    ("Scansione manuale", 430, 150, 6, 1),
    ("Allarme supero ultima media", 431, 150, 6, 1),
    ("Allarme supero media previsionale", 432, 150, 6, 1),
    ("Ingressi digitali 4", 81, 150, 1, 2),
    ("CO", 97, 250, 0, 0),
    ("NO", 99, 250, 0, 0),
    ("O2 Secco", 101, 250, 0, 0),
    ("Temperatura fumi", 113, 250, 0, 0),
    ("Portata gas", 125, 250, 0, 0),
    ("Media oraria previsionale CO-R", 457, 150, 0, 0),
    ("Media giornaliera previsionale CO-R", 458, 150, 0, 0),
    ("Media oraria previsionale NOx-R", 459, 150, 0, 0),
    ("Media giornaliera previsionale NOx-R", 460, 150, 0, 0),
    ("Scansione manuale", 478, 150, 6, 5),
    ("Superamento media archiviata", 479, 150, 6, 5),
    ("Superamento media previsionale", 480, 150, 6, 5),
]

# MEASUREID -> bit con descrizione nel PDF (50 bitinfo totali).
PDF_BITS = {
    1: [8, 9, 10, 11, 12, 13, 14, 15],
    2: [8, 9, 10, 11, 0, 1, 2, 3, 6, 7],
    3: [8, 10, 11, 12, 13, 14, 0, 1, 2, 3, 5, 6],
    14: [0], 15: [0], 16: [0], 17: [0], 18: [0],
    19: [0], 20: [0], 21: [0], 22: [0],
    23: [8, 9, 10, 11, 12, 13, 14, 15],
    33: [0], 34: [0], 35: [0],
}


def observed():
    with open(OBSERVED_PATH, encoding="utf-8") as f:
        return json.load(f)[0]


def reg_of(m):
    return struct.unpack("<I", bytes.fromhex(m["DRIVERPRIVATE"][2:10]))[0]


def fmt_of(m):
    return struct.unpack("<I", bytes.fromhex(m["DRIVERPRIVATE"][-8:]))[0]


def test_misure_uguali_al_pdf_35():
    got = [
        (m["NAME"], reg_of(m), fmt_of(m), m["TYPE"], m["DRIVERDATA"])
        for m in observed()["measures"]
    ]
    assert got == PDF_MEASURES


def test_bitinfo_completi_50():
    got = {}
    for b in observed()["bitinfo"]:
        got.setdefault(b["MEASUREID"], []).append(b["BITNO"])
    assert got == PDF_BITS
    assert len(observed()["bitinfo"]) == 50


def test_driverdata_1_su_5_comandi_da_sciogliere():
    """Ack, Scansioni e Superi GV2 escono con DRIVERDATA=1 (read) invece di 5
    (write): il VLM ha inferito read_write=R, mentre le stesse righe negli
    altri casi escono W. L'IOL non ha colonna R/W, quindi e' inferenza pura e
    incoerente tra run. Pinnato: la regola 'comandi = W' va nel prompt o la
    distinzione va chiarita col cliente (BISON)."""
    st = observed()
    by_reg = {reg_of(m): m for m in st["measures"]}
    for r in (425, 429, 430, 431, 432):
        assert by_reg[r]["DRIVERDATA"] == 1, r
    for r in (417, 418, 419, 424, 478, 479, 480):
        assert by_reg[r]["DRIVERDATA"] == 5, r


def test_stazione_ip_ambiguo_da_sciogliere_col_cliente():
    """Una sola stazione, porta 511, niente mask/PC/secondo PLC nel blob.
    MA l'IP e' .11 (PLC caldaie) mentre il JOB assegna questo IOL (.02) ai
    **motori** (PLC .21/.22): uno tra fogli ('Caldaia GV2/GV3'), intestazione
    (0187.25) e scelta del ramo Station e' sbagliato. Pinnato il comportamento
    attuale, NON la correttezza: si scioglie solo col cliente/pianta."""
    st = observed()
    assert st["NAME"] == "Sistema Analisi Emissioni"
    assert 'tcpport="511"' in st["DRIVERCONFIG"]
    assert 'ipaddress="192.168.1.11"' in st["DRIVERCONFIG"]
    blob = json.dumps(st)
    for vietato in ("192.168.1.10", "192.168.1.12", "192.168.1.21", "192.168.1.22", "255.255.255.0"):
        assert vietato not in blob


def test_texton_supero_diversi_tra_blocchi_stessa_run():
    """Stessa run, due convenzioni: supero GV2 -> ALLARME (keyword), supero
    GV3 -> eco del nome ('SUPERAMENTO MEDIA ...', da state_on). Variabilita'
    VLM interna, non tra run. Da fissare (cliente/BISON) insieme a COMANDO
    (Rivoli)."""
    st = observed()
    got = {b["BITNAME"]: b["TEXTON"] for b in st["bitinfo"]}
    assert got["ALLARME SUPERO ULTIMA MEDIA"] == "ALLARME"
    assert got["SUPERAMENTO MEDIA ARCHIVIATA"] == "SUPERAMENTO MEDIA ARCHIVIATA"
    assert got["SUPERAMENTO MEDIA PREVISIONALE"] == "SUPERAMENTO MEDIA PREVISIONALE"


def test_unita_e_limiti_su_entrambi_i_blocchi():
    """Join per TAG regge anche qui: NO collegato (TAG == descrizione).
    QG senza scala noto: il JOB non la dichiara (sentinel corretto)."""
    st = observed()
    by_id = {m["ID"]: m for m in st["measures"]}
    assert (by_id[4]["UNITS"], by_id[4]["LOWRANGE"], by_id[4]["HIGHRANGE"]) == ("mg/Nm3", 0.0, 600.0)
    assert (by_id[5]["UNITS"], by_id[5]["LOWRANGE"], by_id[5]["HIGHRANGE"]) == ("mg/Nm3", 0.0, 500.0)
    assert (by_id[24]["UNITS"], by_id[24]["HIGHRANGE"]) == ("mg/Nm3", 600.0)
    assert (by_id[25]["UNITS"], by_id[25]["HIGHRANGE"]) == ("mg/Nm3", 500.0)
    assert by_id[28]["UNITS"] is None
    assert (by_id[28]["LOWRANGE"], by_id[28]["HIGHRANGE"]) == (-3.40282e38, 3.40282e38)
    warn = " ".join(st.get("_warnings", []))
    assert "CO (giornaliero=200, orario=250)" in warn
    assert "NO (giornaliero=100, orario=125)" in warn
    assert warn.count("giornaliero=") == 4
    assert "DIVISIONE" not in warn
    assert "VARIABILI SENZA INDIRIZZO" not in warn


def test_prefissi_caldaia_rispettati_e_texton_compilati():
    st = observed()
    nomi = [b["BITNAME"] for b in st["bitinfo"]]
    assert "CALDAIA 1: ALLARME SONDA RISCALDATA" in nomi
    assert "CALDAIA 2: ALLARME SONDA RISCALDATA" in nomi
    for b in st["bitinfo"]:
        assert b["TEXTON"] and b["TEXTOFF"], b
