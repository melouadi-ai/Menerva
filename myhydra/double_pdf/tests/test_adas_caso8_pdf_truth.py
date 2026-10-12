"""Verdetto di correttezza del caso 8 (Rivoli, CTM-Edison): output ADAS vs verita' PDF.

Terza coppia mai vista prima del 12/10/2026: `IOL.0177.25.pdf` (4 pagine) +
`JOB.0177.25.pdf` (23 pagine). Stesso metodo dei casi 6 e 7: la verita' e' la
coppia IOL+JOB letta riga per riga, non un ground truth legacy (che per questo
caso non esiste proprio).

Verita' PDF IOL.0177.25, colonne DESCRIZIONE | REG | BIT | TIPO:

    p2  Allarmi  REG 1  bit 8,9,10,11,12,0,1,2,3  (DBX 128-129; bianche 13,14,15,4,5,6,7)
    p2  (bianche) REG 2  nessun bit               (DBX 130-131: zero righe con titolo)
    p2  Stati    REG 3  bit 8,9,10,11,12,13,7     (DBX 132-133; bianche 14,15,0-6)
    p2  Stati    REG 4  bit 8,9,10,11,12,13,0,1,2,3,5,6  (DBX 134-135; bianche 14,15,4,7)
    p3  Misure   REG 15..32  TIPO=INT  -> formato 150 (con titolo: 18 NOx, 25 TF, 31 QG, 32 PWR)
    p3  Misure   REG 33..47 dispari  TIPO=REAL  -> formato 250 (con titolo: 33 CO, 37 O2 Secco)
    p3  Impostazioni  REG 193..197  TIPO=INT (193 CO riferito, 194 NO come NO2, 195 O2, 196 O2U, 197 QFNs)
    p3/p4 Comandi  REG 209..222  TIPO=WORD (209,211,212,213,214,216,217,221,222)
    p4  Stimate  REG 226,233,239,240  TIPO=WORD -> formato 250

Regola confermata per la terza volta: le righe bianche (senza TITOLO) non
generano ne' misure ne' bit. REG 2 (16 righe tutte bianche) non produce
nemmeno la packed: gli "Ingressi digitali" sono 1, 3, 4.

La coppia, non il solo IOL (JOB.0177.25):

* **Tabella 7 (indirizzi)**: maschera 192.168.1.xxx; `PC SME` .10, `PLC` **.1
  porta 511**, `MIR9000e` .2. L'output ha una sola stazione col PLC: mask, PC
  e analizzatore correttamente ignorati.
* **Oggetto/Titolo**: `Sistema Analisi Emissioni` (dichiarato, come caso 7).
* **Tabella 8 (campi scala, 4.5.1)**: 6 segnali con campo, unita' e (per CO e
  NOx) limiti. Applicati 5 su 6: resta fuori NOx (vedi test dedicato).
* **4.5.2**: CO e O2 secco gia' in unita' ingegneristiche, resto 0...10000.
  Nessun "dividere x10" in questo JOB: correttamente nessun warning DIVISIONE.
* **Tabella 10 (validazioni)**: matrice con colonne Fermo/Manutenzione/
  Calibrazione/... ma qui REG 4 sta tutto a pagina 2: nessun carry-over oltre
  pagina, nessun bit perso (i bit 4 e 7 assenti sono righe bianche reali, non
  una perdita come i 5 stati del caso 7).
* **5.3**: QAL2/QAL3 non richieste, ma l'IOL porta Start/Stop QAL3: l'output
  li tiene coi nomi del PDF (nessuna inferenza da fare).
"""
import json
import os
import struct

OBSERVED_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "case_8",
        "outputs",
        "observed_adas_case8_run1.json",
    )
)

# (NAME, registro Modbus, formato DRIVERPRIVATE, TYPE, DRIVERDATA)
PDF_MEASURES = [
    ("Ingressi digitali 1", 1, 150, 1, 2),
    ("Ingressi digitali 2", 3, 150, 1, 2),
    ("Ingressi digitali 3", 4, 150, 1, 2),
    ("NOx", 18, 150, 0, 0),
    ("Temperatura fumi", 25, 150, 0, 0),
    ("Portata gas", 31, 150, 0, 0),
    ("Potenza elettrica", 32, 150, 0, 0),
    ("CO", 33, 250, 0, 0),
    ("O2 Secco", 37, 250, 0, 0),
    ("CO riferito", 193, 150, 0, 0),
    ("NO espressi come NO2 riferiti", 194, 150, 0, 0),
    ("O2 secco", 195, 150, 0, 0),
    ("O2 umido", 196, 150, 0, 0),
    ("Portata fumi secca", 197, 150, 0, 0),
    ("Heartbit PLC", 209, 150, 6, 5),
    ("Stop calibrazione", 211, 150, 6, 5),
    ("Start autocal zero", 212, 150, 6, 5),
    ("Start QAL3", 213, 150, 6, 5),
    ("Stop QAL3", 214, 150, 6, 5),
    ("Bypass convertitore", 216, 150, 6, 5),
    ("Ack allarmi", 217, 150, 6, 5),
    ("Superamento media archiviata", 221, 150, 6, 5),
    ("Superamento media previsionale", 222, 150, 6, 5),
    ("Misura stimata NOx", 226, 250, 0, 0),
    ("Misura stimata Temperatura fumi", 233, 250, 0, 0),
    ("Misura stimata Portata gas", 239, 250, 0, 0),
    ("Misura stimata Potenza elettrica", 240, 250, 0, 0),
]

# MEASUREID -> bit con descrizione nel PDF (27 misure, 37 bitinfo).
PDF_BITS = {
    1: [8, 9, 10, 11, 12, 0, 1, 2, 3],
    2: [8, 9, 10, 11, 12, 13, 7],
    3: [8, 9, 10, 11, 12, 13, 0, 1, 2, 3, 5, 6],
    15: [0],
    16: [0],
    17: [0],
    18: [0],
    19: [0],
    20: [0],
    21: [0],
    22: [0],
    23: [0],
}

# Tabella 8 del JOB.0177.25 (4.5.1): segnale -> (campo, unita', limite_g, limite_o)
SCALE_DICHIARATE_NEL_JOB = {
    "CO": ((0.0, 240.0), "mg/Nm3", 120, 150),
    "NOx": ((0.0, 20.0), "mg/Nm3", 8, 10),
    "O2 secco": ((0.0, 25.0), "%", None, None),
    "Temperatura fumi": ((0.0, 600.0), "°C", None, None),
    "Portata gas": ((0.0, 600.0), "Sm³/h", None, None),
    "Potenza elettrica": ((0.0, 2000.0), "kW", None, None),
}


def observed():
    with open(OBSERVED_PATH, encoding="utf-8") as f:
        return json.load(f)[0]


def reg_of(m):
    return struct.unpack("<I", bytes.fromhex(m["DRIVERPRIVATE"][2:10]))[0]


def fmt_of(m):
    return struct.unpack("<I", bytes.fromhex(m["DRIVERPRIVATE"][-8:]))[0]


def test_misure_uguali_al_pdf():
    got = [
        (m["NAME"], reg_of(m), fmt_of(m), m["TYPE"], m["DRIVERDATA"])
        for m in observed()["measures"]
    ]
    assert got == PDF_MEASURES


def test_reg2_tutto_bianco_niente_packed():
    """DBX 130-131 (REG 2): 16 righe tutte senza titolo. Non produce bitinfo
    e nemmeno la packed: gli 'Ingressi digitali' sono 1, 3, 4."""
    st = observed()
    packed = [m for m in st["measures"] if m["TYPE"] == 1]
    assert [(m["NAME"], reg_of(m)) for m in packed] == [
        ("Ingressi digitali 1", 1),
        ("Ingressi digitali 2", 3),
        ("Ingressi digitali 3", 4),
    ]


def test_bitinfo_completi_37():
    got = {}
    for b in observed()["bitinfo"]:
        got.setdefault(b["MEASUREID"], []).append(b["BITNO"])
    assert got == PDF_BITS
    assert len(observed()["bitinfo"]) == 37


def test_formati_da_tipo():
    """INT -> 150 (misure, impostazioni, comandi), REAL/WORD stimati -> 250."""
    st = observed()
    by_name = {m["NAME"]: fmt_of(m) for m in st["measures"]}
    assert by_name["NOx"] == 150
    assert by_name["CO riferito"] == 150
    assert by_name["Heartbit PLC"] == 150
    assert by_name["CO"] == 250
    assert by_name["O2 Secco"] == 250
    assert by_name["Misura stimata NOx"] == 250


def test_texton_e_textoff_sempre_compilati():
    for b in observed()["bitinfo"]:
        assert b["TEXTON"], b
        assert b["TEXTOFF"], b


def test_texton_superamento_COMANDO_da_fissare():
    """I due bit superamento escono con TEXTON 'COMANDO'; la convenzione da
    keyword usata altrove darebbe 'SUPERAMENTO'. Pinnato in attesa di fissare
    la convenzione (non un errore di lettura: i nomi sono giusti)."""
    st = observed()
    got = {b["BITNAME"]: b["TEXTON"] for b in st["bitinfo"]}
    assert got["SUPERAMENTO MEDIA ARCHIVIATA"] == "COMANDO"
    assert got["SUPERAMENTO MEDIA PREVISIONALE"] == "COMANDO"


def test_unita_e_range_collegati_5_su_6():
    """Tabella 8 JOB: 6 scale dichiarate, 5 applicate. Il join per TAG regge
    anche qui (O2S/TF/QG/PWR/CO); le unita' si confrontano normalizzate
    (il VLM alterna 'mg/Nm3' e 'mg/Nm³' tra run)."""
    st = observed()
    norm = lambda u: (u or "").replace("³", "3")
    by_name = {m["NAME"]: m for m in st["measures"]}
    attese = {
        "CO": ("mg/Nm3", (0.0, 240.0)),
        "O2 Secco": ("%", (0.0, 25.0)),
        "Temperatura fumi": ("°C", (0.0, 600.0)),
        "Portata gas": ("Sm3/h", (0.0, 600.0)),
        "Potenza elettrica": ("kW", (0.0, 2000.0)),
    }
    for nome, (u, r) in attese.items():
        m = by_name[nome]
        assert norm(m["UNITS"]) == norm(u), (nome, m["UNITS"])
        assert (m["LOWRANGE"], m["HIGHRANGE"]) == r, nome


def test_nox_senza_scala_difetto_noto():
    """Unico difetto vero della run: NOx (reg 18) esce con sentinel, senza
    unita' e senza warning limiti, mentre il JOB dichiara 0-20 mg/Nm3 e
    limiti 8/10. Ipotesi: TAG IOL 'NO' contro 'NOx' del JOB, il join per TAG
    fallisce. Stessa classe di fragilita' dei casi 6/7, da confermare sul
    chunk."""
    st = observed()
    by_name = {m["NAME"]: m for m in st["measures"]}
    nox = by_name["NOx"]
    assert nox["UNITS"] is None
    assert (nox["LOWRANGE"], nox["HIGHRANGE"]) == (-3.40282e38, 3.40282e38)
    warn = " ".join(st.get("_warnings", []))
    assert "NOx" not in warn


def test_warning_solo_limite_co():
    """Un solo warning LIMITI (CO 120/150). Niente DIVISIONE: questo JOB non
    ne dichiara (4.5.2), a differenza del caso 7."""
    st = observed()
    warns = st.get("_warnings", [])
    assert len(warns) == 1, warns
    assert "CO (giornaliero=120, orario=150)" in warns[0]
    assert "DIVISIONE" not in " ".join(warns)


def test_stazione_dichiarata_e_ip_plc():
    """Nome dichiarato (Oggetto JOB), una sola stazione, IP del PLC con
    porta 511; maschera, PC SME e analizzatore ignorati."""
    st = observed()
    assert st["NAME"] == "Sistema Analisi Emissioni"
    assert 'ipaddress="192.168.1.1"' in st["DRIVERCONFIG"]
    assert 'tcpport="511"' in st["DRIVERCONFIG"]
    blob = json.dumps(st)
    assert "192.168.1.10" not in blob
    assert "192.168.1.2" not in blob
    assert "255.255.255.0" not in blob


def test_refuso_pdf_corretto_da_vlm():
    """Il PDF scrive 'CO rferito' (DBW 512): l'output normalizza in
    'CO riferito'. Stessa classe di 'Ossiegno' nel Single: la politica sui
    refusi (rispettare vs correggere) resta da decidere col cliente."""
    st = observed()
    nomi = [m["NAME"] for m in st["measures"]]
    assert "CO riferito" in nomi
    assert not [n for n in nomi if "rferito" in n]


def test_stimata_nox_ppm_da_descrizione():
    """'Misura stimata NOx (in ppm)' nel PDF: l'unita' ppm viene dalla
    descrizione IOL, non da una scala JOB. Provenienza annotata perche' e'
    l'unica unita' non-JOB della run."""
    st = observed()
    by_name = {m["NAME"]: m for m in st["measures"]}
    assert by_name["Misura stimata NOx"]["UNITS"] == "ppm"
    assert by_name["Misura stimata NOx"]["UNITS2"] == "ppm"


def test_sentinel_su_misure_senza_scala():
    st = observed()
    by_name = {m["NAME"]: m for m in st["measures"]}
    for nome in ("NOx", "CO riferito", "Misura stimata Temperatura fumi"):
        m = by_name[nome]
        assert m["LOWCRITICAL"] == -3.40282e38, nome
        assert m["HIGHCRITICAL"] == 3.40282e38, nome
