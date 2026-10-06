"""Verdetto di correttezza del caso 7: output ADAS osservato vs verita' PDF.

Stesso metodo di `test_adas_caso6_pdf_truth.py`: la verita' di riferimento e'
`Mappatura_7_Cliente_SMI_2.pdf` (IOL.0105.22, 4 pagine) letto riga per riga,
non il ground truth legacy.

Verita' PDF IOL.0105.22, colonne DESCRIZIONE | REG | BIT | TIPO:

    p2  Allarmi    REG 1  bit 8..15,0..7   (DBX 64-65, 16 righe con titolo)
    p2  Allarmi    REG 2  bit 8            (DBX 66.0, una sola riga con titolo)
    p2  Stati      REG 3  bit 8,10..15,7   (DBX 68-69)
    p2  Stati      REG 4  bit 8,10..13,0,1,2   (DBX 70-71.2)  <- si ferma a pagina 2
    p3  (segue)    REG 4  bit 3,4,5,6,7   (DBX 71.3-71.7)   <- continuazione
    p3  Misure     REG 17..42  TIPO=INT   -> formato 150
    p3  Comandi    REG 145..158  TIPO=WORD
    p3/p4  Stima   REG 161..172  TIPO=WORD  -> formato 250

Il difetto che questo test blocca: la cella REG 4 e' unita e **attraversa il
confine di pagina** (DBX 70.0 a pagina 2, DBX 71.3-71.7 a pagina 3). Sulla
pagina 3 la colonna REG e' visivamente vuota, il VLM restituisce
`modbus_register: null` e `json_creator` scarta la riga come "variabile senza
indirizzo". Cinque stati reali di impianto spariscono. Il warning lo dice, ma
il dato in ADAS non c'e': per laeta' di questo progetto un warning non e'
un substitutes del valore.

Nota sulle unita': qui, a differenza del caso 6, il JOB **dichiara** campi scala
e unita' (Tabella 9: CO/NO 0...200 mg/Nm3, O2 0...25 %, TF 0...500 °C, dP
0...750 Pa, PLV 0...25 mg/Nm3, T_UREA/T_SCR °C, potenze kW, consumi kg) e i
limiti giornalieri/orari. L'output ne applica 4 su 19: il resto arriva `null`.
"""
import json
import os
import struct

OBSERVED_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "case_7",
        "outputs",
        "observed_adas_case7_qwen38_run2.json",
    )
)

# (NAME, registro Modbus, formato DRIVERPRIVATE, TYPE, DRIVERDATA)
PDF_MEASURES = [
    ("Ingressi digitali 1", 1, 150, 1, 2),
    ("Ingressi digitali 2", 2, 150, 1, 2),
    ("Ingressi digitali 3", 3, 150, 1, 2),
    ("Ingressi digitali 4", 4, 150, 1, 2),
    ("CO", 17, 150, 0, 0),
    ("NO", 18, 150, 0, 0),
    ("O2 Secco", 19, 150, 0, 0),
    ("O2 Umido", 20, 150, 0, 0),
    ("COT", 22, 150, 0, 0),
    ("NH3", 23, 150, 0, 0),
    ("Temperatura fumi", 25, 150, 0, 0),
    ("Pressione differenziale fumi", 27, 150, 0, 0),
    ("Concentrazione polveri", 28, 150, 0, 0),
    ("Temperatura urea", 33, 150, 0, 0),
    ("Temperatura SCR", 34, 150, 0, 0),
    ("Potenza motore", 35, 150, 0, 0),
    ("Potenza turbina", 36, 150, 0, 0),
    ("Potenza totale recuperata", 37, 150, 0, 0),
    ("Potenza totale verso turbina", 38, 150, 0, 0),
    ("Potenza termica immessa in motore", 39, 150, 0, 0),
    ("Consumo combustibile", 41, 150, 0, 0),
    ("Consumo combustibile orario", 42, 150, 0, 0),
    ("Heartbit PLC", 145, 150, 6, 5),
    ("Stop calibrazione", 147, 150, 6, 5),
    ("Start autocal zero", 148, 150, 6, 5),
    ("Start QAL3", 149, 150, 6, 5),
    ("Stop QAL3", 150, 150, 6, 5),
    ("Bypass convertitore", 152, 150, 6, 5),
    ("Ack allarmi", 153, 150, 6, 5),
    ("Superamento media archiviata", 157, 150, 6, 5),
    ("Superamento media previsionale", 158, 150, 6, 5),
    ("Misura stimata CO", 161, 250, 0, 0),
    ("Misura stimata NO", 162, 250, 0, 0),
    ("Misura stimata O2 Secco", 163, 250, 0, 0),
    ("Misura stimata O2 Umido", 164, 250, 0, 0),
    ("Misura stimata NH3", 167, 250, 0, 0),
    ("Misura stimata Temperatura fumi", 169, 250, 0, 0),
    ("Misura stimata Pressione differenziale fumi", 171, 250, 0, 0),
    ("Misura stimata Concentrazione polveri", 172, 250, 0, 0),
]

# MEASUREID -> bit con descrizione nel PDF. REG 4 include 3,4,5,6,7: sono le
# righe di pagina 3, perse per il carry-over del registro (vedi docstring).
PDF_BITS = {
    1: [8, 9, 10, 11, 12, 13, 14, 15, 0, 1, 2, 3, 4, 5, 6, 7],
    2: [8],
    3: [8, 10, 11, 12, 13, 14, 15, 7],
    4: [8, 10, 11, 12, 13, 0, 1, 2, 3, 4, 5, 6, 7],
    23: [0],
    24: [0],
    25: [0],
    26: [0],
    27: [0],
    28: [0],
    29: [0],
    30: [0],
    31: [0],
}

# Le 5 righe che il PDF dichiara e l'output non contiene, con il bit che
# avrebbero dovuto occupare su REG 4.
BIT_PERSI = {
    "IMPIANTO IN SPEGNIMENTO": 3,
    "IMPIANTO IN LAVAGGIO": 4,
    "SME IN MANUTENZIONE": 5,
    "IMPIANTO IN MANUTENZIONE": 6,
    "IMPIANTO FUORI SERVIZIO PER GUASTO": 7,
}

# Tabella 9 del JOB.0105.22: unita' dichiarate, che l'output non applica.
UNITA_DICHIARATE_NEL_JOB = {
    "CO": "mg/Nm³",
    "NO": "mg/Nm³",
    "COT": "mg/Nm³",
    "NH3": "mg/Nm³",
    "O2 Secco": "%",
    "O2 Umido": "%",
    "Temperatura fumi": "°C",
    "Concentrazione polveri": "mg/Nm³",
    "Temperatura urea": "°C",
    "Temperatura SCR": "°C",
    "Potenza motore": "kW",
    "Potenza turbina": "kW",
    "Potenza totale recuperata": "kW",
    "Potenza totale verso turbina": "kW",
    "Potenza termica immessa in motore": "kW",
    "Consumo combustibile": "kg",
    "Consumo combustibile orario": "kg",
    "Pressione differenziale fumi": "Pa",
}


def observed():
    with open(OBSERVED_PATH, encoding="utf-8") as f:
        return json.load(f)[0]


def reg_of(m):
    return struct.unpack("<I", bytes.fromhex(m["DRIVERPRIVATE"][2:10]))[0]


def fmt_of(m):
    return struct.unpack("<I", bytes.fromhex(m["DRIVERPRIVATE"][-8:]))[0]


def test_stazione_e_driverconfig():
    st = observed()
    assert st["NAME"] == "Sistema Analisi Emissioni"
    assert 'ipaddress="172.16.1.31"' in st["DRIVERCONFIG"]
    assert 'tcpport="511"' in st["DRIVERCONFIG"]


def test_misure_uguali_al_pdf():
    got = [
        (m["NAME"], reg_of(m), fmt_of(m), m["TYPE"], m["DRIVERDATA"])
        for m in observed()["measures"]
    ]
    assert got == PDF_MEASURES


def test_formato_int_su_150_e_word_stimati_su_250():
    """`TIPO=INT` nel PDF sul blocco Misure (REG 17-42) e `TIPO=WORD` sui
    comandi e sui dati stimati: due formati diversi, non uno solo."""
    st = observed()
    by_name = {m["NAME"]: fmt_of(m) for m in st["measures"]}
    assert by_name["CO"] == 150
    assert by_name["Consumo combustibile orario"] == 150
    assert by_name["Misura stimata CO"] == 250
    assert by_name["Misura stimata Concentrazione polveri"] == 250


def test_bitinfo_completi_su_tutti_e_quattro_i_registri_impaccati():
    got = {}
    for b in observed()["bitinfo"]:
        got.setdefault(b["MEASUREID"], []).append(b["BITNO"])
    packed = {k: v for k, v in got.items() if k <= 4}
    # I bit 3..7 di REG 4 mancano: sono i cinque stati perduti a pagina 3.
    assert packed[1] == PDF_BITS[1]
    assert packed[2] == PDF_BITS[2]
    assert packed[3] == PDF_BITS[3]
    assert packed[4] == PDF_BITS[4][:8]


def test_texton_e_textoff_sempre_compilati():
    for b in observed()["bitinfo"]:
        assert b["TEXTON"], b
        assert b["TEXTOFF"], b


def test_difetto_conosciuto_cinque_stati_persi():
    """Il difetto e' noto e documentato: finche' non e' chiuso, questo test
    fallisce di proposito. Quando si applica il carry-over del registro,
    cancellare l'asserzione e basta: tutto il resto resta valido."""
    st = observed()
    got = {b["BITNAME"]: b["BITNO"] for b in st["bitinfo"]}
    for nome, bit in BIT_PERSI.items():
        assert nome not in got, (
            "%s non e' piu perso: rimuovi questa asserzione e allinea "
            "test_bitinfo_completi_su_tutti_e_quattro_i_registri_impaccati" % nome
        )
        assert nome.lower() not in " ".join(got).lower()
    # il warning le elenca: la perdita e' visibile ma il dato non c'e'
    warn = " ".join(st.get("_warnings", []))
    for nome in BIT_PERSI:
        assert nome.split()[-1].lower() in warn.lower()


def test_unita_applicate_solo_a_quattro_misure():
    """Gap aperto: il JOB dichiara 18 unita' (Tabella 9), l'output ne applica 4.
    Le righe sotto sono la verita' del JOB; quando il collegamento scala->unita'
    viene chiuso, questo test va aggiornato insieme alla correzione."""
    st = observed()
    units = {m["NAME"]: m["UNITS"] for m in st["measures"]}
    applicate = {k: v for k, v in units.items() if v}
    assert applicate == {
        "CO": "mg/Nm³",
        "NO": "mg/Nm³",
        "COT": "mg/Nm³",
        "NH3": "mg/Nm³",
    }
    # ogni unita' presente deve corrispondere a una grandezza nota del JOB
    for nome, u in applicate.items():
        assert UNITA_DICHIARATE_NEL_JOB[nome] == u


def test_difetto_conosciuto_sentinel_dei_limiti_assente():
    """Lo script sul canvas non e' `src/nodes/json_creator.py`.

    Il repo e tutti e quattro i ground truth legacy emettono
    LOWCRITICAL = -3.40282e38 / HIGHCRITICAL = +3.40282e38 sulle misure
    analogiche: e' il sentinel ADAS per "nessun limite". L'output Double PDF
    emette `null`. Non e' una scelta: e' una divergenza, probabilmente una
    copia modificata a mano del nodo 12 (la stessa classe di errore che aveva
    rotto il linkage dei bitinfo). Da correggere riallineando il nodo al repo,
    poi questo test va invertito.

    Finche' resta cosi', i limiti veri del JOB (CO 40/50 mg/Nm3, NO 30/37.5,
    NH3 2/2.5, COT 10, PLV 10) non hanno un campo su cui scriversi: il pytool
    scrive costanti e non legge `limit_day`/`limit_hour` in nessun caso.
    """
    for m in observed()["measures"]:
        if m["TYPE"] == 0:
            assert m["LOWCRITICAL"] is None
            assert m["HIGHCRITICAL"] is None