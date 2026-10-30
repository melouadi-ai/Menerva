"""Verdetto di correttezza del caso 6: output ADAS osservato vs verita' PDF.

Diversamente da `test_adas_caso6.py` (chunk -> json_creator), qui la
verita' di riferimento non e' il ground truth legacy
`gaia_doublefile_result_6.json` ma il PDF `Mappatura_6_Cliente_SMI_1.pdf`,
letto riga per riga. Il legacy sbaglia: lo dimostra questo test (vedi
`test_legacy_ha_errori_noti_il_nostro_no`).

Verita' PDF, colonne DESCRIZIONE | REG | BIT | TIPO (STRUCT BIT):

    pagina 2  Allarmi   REG 1  bit 8..13   (DBX 64.x, 6 righe con titolo)
    pagina 2  (vuoto)   REG 2  bit 8..15,0..7  (DBX 66-67, senza titolo)
    pagina 2  Stati     REG 3  bit 8..11,15,0..3,5..7   (DBX 68-69)
    pagina 2  Stati     REG 4  bit 8..11,13,0..3,5..7   (DBX 70-71)
    pagina 3  Stati 2   REG 5  bit 8..15,1,2,4,5        (DBX 72-73)
    pagina 3  Stati 2   REG 6  bit 8..13,0..3           (DBX 74-75)
    pagina 3  Misure    REG 9,10,11  TIPO=INT  (QAL3 tempi)   -> formato 150
    pagina 3  Misure raw REG 17 SO2, REG 33 Temperatura fumi, TIPO=REAL -> 250
    pagina 4  Misure ing. REG 49 SO2, REG 65 Temperatura fumi, TIPO=REAL
    pagina 4  Comandi   REG 417,418,419,425,426,427,431,432  TIPO=WORD
    pagina 4  Stimati   REG 433 SO2, pagina 5 REG 441 Temperatura fumi

Le righe bianche (nessun TITOLO) non generano bit: da qui 60 bitinfo
(52 impaccati + 8 comandi), non 78.

Dal 29/10/2026 il `JSON CREATOR` Double scrive nel `DRIVERPRIVATE` il
registro Modbus reale, cioe' `40000 + REG` del PDF (REG 1 -> 40001). La
verita' resta quella del PDF: `reg_raw` legge il valore scritto, `reg_pdf`
lo riporta al REG del documento togliendo l'offset.

Il PDF non contiene una colonna unità di misura: `mg/Nm3` e `°C` nel
ground truth legacy sono inferenze, non dati del documento. Le due `SQ`
delle misure SO2 sono invece limiti dichiarati nel PDF (60) e finiscono
in `SQ1HOURMEAN`/`SQDAILYMEAN`.
"""
import json
import os
import struct

OBSERVED_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "double_pdf_outputs",
        "observed_adas_case6_qwen38_run5.json",
    )
)
LEGACY_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), "..", "data", "test_outputs", "gaia_doublefile_result_6.json"
    )
)

# Offset ADAS Double: il registro scritto e' 40000 + REG del PDF (28/10/2026)
ADAS_REG_OFFSET = 40000

# (NAME, REG del PDF, formato DRIVERPRIVATE, TYPE, DRIVERDATA)
PDF_MEASURES = [
    ("Ingressi digitali 1", 1, 150, 1, 2),
    ("Ingressi digitali 2", 3, 150, 1, 2),
    ("Ingressi digitali 3", 4, 150, 1, 2),
    ("Ingressi digitali 4", 5, 150, 1, 2),
    ("Ingressi digitali 5", 6, 150, 1, 2),
    ("QAL3: Tempo trascorso apertura elettrovalvola N2", 9, 150, 0, 0),
    ("QAL3: Tempo trascorso apertura elettrovalvola ARIA", 10, 150, 0, 0),
    ("QAL3: Tempo trascorso apertura elettrovalvola SO2", 11, 150, 0, 0),
    ("SO2", 17, 250, 0, 0),
    ("Temperatura fumi", 33, 250, 0, 0),
    ("SO2", 49, 250, 0, 0),
    ("Temperatura fumi", 65, 250, 0, 0),
    ("PC life signal", 417, 150, 6, 5),
    ("Start autocal", 418, 150, 6, 5),
    ("Stop autocal", 419, 150, 6, 5),
    ("Ack allarmi", 425, 150, 6, 5),
    ("Impianto in manutenzione", 426, 150, 6, 5),
    ("Impianto fuori servizio per guasto", 427, 150, 6, 5),
    ("Allarme supero ultima media", 431, 150, 6, 5),
    ("Allarme supero media previsionale", 432, 150, 6, 5),
    ("Misura stimata SO2", 433, 250, 0, 0),
    ("Misura stimata Temperatura fumi", 441, 250, 0, 0),
]

# MEASUREID -> bit presenti nel PDF (le righe bianche sono escluse)
PDF_BITS = {
    1: [8, 9, 10, 11, 12, 13],
    2: [8, 9, 10, 11, 15, 0, 1, 2, 3, 5, 6, 7],
    3: [8, 9, 10, 11, 13, 0, 1, 2, 3, 5, 6, 7],
    4: [8, 9, 10, 11, 12, 13, 14, 15, 1, 2, 4, 5],
    5: [8, 9, 10, 11, 12, 13, 0, 1, 2, 3],
    13: [0],
    14: [0],
    15: [0],
    16: [0],
    17: [0],
    18: [0],
    19: [0],
    20: [0],
}


def load(name):
    with open(name, encoding="utf-8") as f:
        return json.load(f)


def reg_raw(m):
    """Registro Modbus scritto nel DRIVERPRIVATE (offset ADAS incluso)."""
    return struct.unpack("<I", bytes.fromhex(m["DRIVERPRIVATE"][2:10]))[0]


def reg_pdf(m):
    """REG del PDF ricavato dall'output, togliendo l'offset ADAS 40000."""
    return reg_raw(m) - ADAS_REG_OFFSET


def fmt_of(m):
    return struct.unpack("<I", bytes.fromhex(m["DRIVERPRIVATE"][-8:]))[0]


def observed():
    return load(OBSERVED_PATH)[0]


def test_stazione_e_driverconfig():
    st = observed()
    assert st["NAME"] == "Sistema Analisi SO2"
    assert 'ipaddress="10.100.50.95"' in st["DRIVERCONFIG"]
    assert 'tcpport="511"' in st["DRIVERCONFIG"]


def test_misure_uguali_al_pdf():
    st = observed()
    got = [
        (m["NAME"], reg_pdf(m), fmt_of(m), m["TYPE"], m["DRIVERDATA"])
        for m in st["measures"]
    ]
    assert got == PDF_MEASURES


def test_registro_adas_e_40000_piu_reg_pdf():
    """Offset introdotto il 28/10/2026: nel DRIVERPRIVATE va 40000 + REG.
    Il caso 6 parte da 40001 e va fino a 40441; nessuna misura resta sul
    REG nudo del PDF."""
    st = observed()
    for m in st["measures"]:
        assert reg_raw(m) == reg_pdf(m) + ADAS_REG_OFFSET, m["NAME"]
    raw = [reg_raw(m) for m in st["measures"]]
    assert min(raw) == 40001
    assert max(raw) == 40441
    assert all(r > ADAS_REG_OFFSET for r in raw)


def test_limiti_orari_e_giornalieri_in_sq_means():
    """Le due SO2 dichiarano 60 (giornaliero e orario) nel PDF: finiscono
    in SQ1HOURMEAN/SQDAILYMEAN. Le misure senza limite restano sentinel,
    cosi' non si inventa una soglia"""
    st = observed()
    for m in st["measures"]:
        if m["NAME"] == "SO2":
            assert m["SQ1HOURMEAN"] == 60.0, m
            assert m["SQDAILYMEAN"] == 60.0, m
        elif m["TYPE"] == 0:
            # analogica senza limite dichiarato: sentinel, non una soglia inventata
            assert m["SQ1HOURMEAN"] == 3.40282e38, m["NAME"]
            assert m["SQDAILYMEAN"] == 3.40282e38, m["NAME"]
        else:
            # digitali e comandi non hanno SQ nel formato ADAS
            assert m["SQ1HOURMEAN"] is None, m["NAME"]
            assert m["SQDAILYMEAN"] is None, m["NAME"]
    warn = " ".join(st.get("_warnings", []))
    assert "LIMITI DICHIARATI APPLICATI IN ADAS" in warn
    assert "LIMITI NON NUMERICI NON APPLICATI" not in warn


def test_bitinfo_uguale_al_pdf():
    st = observed()
    got = {}
    for b in st["bitinfo"]:
        got.setdefault(b["MEASUREID"], []).append(b["BITNO"])
    assert got == PDF_BITS
    assert len(st["bitinfo"]) == 60


def test_nomi_bit_radicati_nel_pdf():
    # "Elettrovalvola cal da sonda" (DBX 70.3): niente "STATO" davanti.
    by_name = {b["BITNAME"]: b for b in observed()["bitinfo"]}
    assert "ELETTROVALVOLA CAL DA SONDA" in by_name
    assert "STATO ELETTROVALVOLA CAL DA SONDA" not in by_name


def test_texton_e_textoff_sempre_compilati():
    for b in observed()["bitinfo"]:
        assert b["TEXTON"], b
        assert b["TEXTOFF"], b


def test_pm302ab_sui_bit_del_pdf():
    """Regressione chiusa con il prompt v5 (run4): PM-302A a BIT 1 e PM-302B
    a BIT 2, come stampato su DBX 73.1/73.2. La run precedente li aveva a
    0/1, sulla riga bianca DBX 73.0."""
    by_name = {b["BITNAME"]: b for b in observed()["bitinfo"]}
    assert by_name["PM-302A IN MARCIA"]["BITNO"] == 1
    assert by_name["PM-302B IN MARCIA"]["BITNO"] == 2
    assert by_name["PM-310A IN MARCIA"]["BITNO"] == 4
    assert by_name["PM-310B IN MARCIA"]["BITNO"] == 5


def test_texton_da_keyword_mai_allarme_su_vita_e_valvole():
    """Decisione 6/10/2026: TEXTON packed da keyword. Il VLM aveva scritto
    ALLARME su heartbeat ed elettrovalvole; il JOB 4.8 descrive l'heartbeat
    come segnale periodico, non un allarme."""
    by_name = {b["BITNAME"]: b for b in observed()["bitinfo"]}
    assert by_name["PLC LIFE SIGNAL"]["TEXTON"] == "ATTIVO"
    assert by_name["STATO ELETTROVALVOLA CAL ZERO"]["TEXTON"] == "APERTO"
    assert by_name["STATO ELETTROVALVOLA N2"]["TEXTON"] == "APERTO"
    assert by_name["STATO ELETTROVALVOLA CAL SPAN"]["TEXTON"] == "APERTO"
    assert by_name["ELETTROVALVOLA CAL DA SONDA"]["TEXTON"] == "APERTO"


def test_textoff_chiuso_sulle_elettrovalvole():
    """Run del 29/10: il VLM ha allineato TEXTOFF a TEXTON (APERTO) sulle
    elettrovalvole, quindi 'CHIUSO' invece di 'OFF'. Nella run4 una di
    queste righe aveva 'ERRORE' (anomalia sparita). Tutte le altre righe
    restano 'OFF': se compare un terzo valore, il chunk e' cambiato."""
    offs = {b["BITNAME"]: b["TEXTOFF"] for b in observed()["bitinfo"]}
    chiuso = {n for n, t in offs.items() if t == "CHIUSO"}
    assert chiuso == {
        "QAL3: ELETTROVALVOLA ARIA",
        "QAL3: ELETTROVALVOLA SPAN SO2",
        "STATO ELETTROVALVOLA CAL ZERO",
        "STATO ELETTROVALVOLA N2",
        "STATO ELETTROVALVOLA CAL SPAN",
        "ELETTROVALVOLA CAL DA SONDA",
    }, chiuso
    altri = {t for n, t in offs.items() if n not in chiuso}
    assert altri == {"OFF"}, altri


def test_nessuna_riga_fantasma_da_riga_bianca():
    names = {b["BITNAME"] for b in observed()["bitinfo"]}
    assert "DBW 922" not in names  # riga senza TITOLO: il legacy la ha trasformata in bit
    assert not any(n.startswith("DBW ") or n.startswith("DBX ") for n in names)


def test_legacy_ha_errori_noti_il_nostro_no():
    """Il legacy non e' un riferimento: sbaglia bit e registri. Fissiamo qui
    dove sbaglia, cosi' il confronto non viene 'corretto' verso il basso."""
    legacy = load(LEGACY_PATH)[0]
    mid2reg = {m["ID"]: reg_raw(m) for m in legacy["measures"]}
    orphans = sorted({b["MEASUREID"] for b in legacy["bitinfo"] if b["MEASUREID"] not in mid2reg})
    assert orphans, "il legacy dovrebbe avere almeno un bitinfo orfano"
    legacy_bits = {
        (mid2reg[b["MEASUREID"]], b["BITNO"]): b["BITNAME"]
        for b in legacy["bitinfo"]
        if b["MEASUREID"] in mid2reg
    }
    st = observed()
    mine = {}
    mid2reg_mine = {m["ID"]: reg_pdf(m) for m in st["measures"]}
    for b in st["bitinfo"]:
        mine[(mid2reg_mine[b["MEASUREID"]], b["BITNO"])] = b["BITNAME"]

    # PM-302A e' DBX 73.1 -> REG 5 BIT 1 (il legacy lo mette a BIT 0)
    assert legacy_bits.get((5, 0)) == "PM-302A IN MARCIA"
    assert mine[(5, 1)] == "PM-302A IN MARCIA"
    # ventilatori: DBX 75.x -> REG 6 BIT 0..3 (il legacy li mette a 4..7)
    assert legacy_bits.get((6, 4)) == "VENTILATORE VN-400 IN MARCIA"
    assert mine[(6, 0)] == "VENTILATORE VN-400 IN MARCIA"
    # comandi: "Allarme supero ultima media" e' DBW 924 -> REG 431
    legacy_reg = {m["NAME"]: reg_raw(m) for m in legacy["measures"]}
    assert legacy_reg["Allarme supero ultima media"] == 430
    assert legacy_reg["Allarme supero media previsionale"] == 431
    our_reg = {m["NAME"]: reg_pdf(m) for m in st["measures"]}
    assert our_reg["Allarme supero ultima media"] == 431
    assert our_reg["Allarme supero media previsionale"] == 432
    # formato: i QAL3 sono INT nel PDF, il legacy li scrive come REAL
    legacy_fmt = {m["NAME"]: fmt_of(m) for m in legacy["measures"]}
    assert legacy_fmt["QAL3: Tempo trascorso apertura elettrovalvola N2"] == 250
    assert fmt_of(next(m for m in st["measures"] if m["NAME"].endswith("elettrovalvola N2"))) == 150
    # conteggio: 78 bit legacy contro 60 reali, e almeno un bitinfo orfano
    assert len(legacy["bitinfo"]) == 78
    assert len(st["bitinfo"]) == 60
    assert not [b for b in st["bitinfo"] if b["MEASUREID"] not in mid2reg_mine]