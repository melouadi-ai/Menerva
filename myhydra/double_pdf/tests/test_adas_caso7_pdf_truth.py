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

## La coppia, non il solo IOL

Il JOB.0105.22 (7 pagine) e' parte della verita' quanto l'IOL.0105.22:

* **Tabella 8 (indirizzi)**: `PC SME` due schede (192.168.70.103 e 172.16.1.10),
  `PLC` **172.16.1.31 porta 511** (comunicazione ADAS). L'output ha la
  combinazione giusta e una sola stazione: i due IP del PC SME non devono
  generare due stazioni.
* **Oggetto/Titolo**: `Sistema Analisi Emissioni`. Il nome stazione dell'output
  coincide con il titolo del JOB: qui il nome e' **dichiarato**, non dedotto
  (nel caso 6 invece non lo e').
* **Tabella 9 (campi scala)**: 19 righe, unita' e limiti per 18 segnali. Sono
  applicate 4.
* **Tabella 12 (validazioni)**: la matrice che dice quando una misura non e'
  valida ha come colonne gli stati d'impianto `Fermo`, `Manutenzione`, `Fuori
  servizio`, `Lavaggio`. **Sono esattamente i bit 3-7 di REG 4**, cioe' i cinque
  che perdiamo. La perdita non e' cosmetica: distrugge l'input della matrice di
  validazione che il cliente ha specificato.
* **4.5.2 e le asteriscate**: le misure non asteriscate si acquisiscono con
  campo 0...10000 da riscalare; le asteriscate (T_UREA, T_SCR, P_MTR, P_TRB,
  P_TOT, P_TOT_TRB, PT_MTR, Q_OIL, Q_OIL_H: 9) sono gia' in unita'
  ingegneristiche e vanno divise per 10. La stessa istruzione "Dividere x10" e'
  scritta nella colonna RANGE dell'IOL sui registri 33-39 e 41-42. Non la
  raccogliamo da nessuna delle due fonti.

## Perche' le unita' sono 4 e non 18

Il JOB identifica i segnali con i **tag** (`CO`, `O2S`, `TF`, `P_MTR`, ...),
l'IOL li descrive a parole (`CO`, `O2 Secco`, `Temperatura fumi`, `Potenza
motore`). Il join del consolidatore (`consolidate_to_intermediate.py`) e'
esatto: `description == tag` oppure `description == tag + " Raw"`. Le 4 unita'
applicate sono esattamente i 4 tag che coincidono col testo della descrizione.
Quindi il join scarta 14 righe su 18. Il campo giusto su cui agganciare e' il
**tag dell'IOL**, che il consolidatore non porta nel chunk.
"""
import json
import os
import struct

OBSERVED_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "case_7",
        "outputs",
        "observed_adas_case7_qwen38_run5.json",
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
    "CO": "mg/Nm3",
    "NO": "mg/Nm3",
    "COT": "mg/Nm3",
    "NH3": "mg/Nm3",
    "O2 Secco": "%",
    "O2 Umido": "%",
    "Temperatura fumi": "°C",
    "Concentrazione polveri": "mg/Nm3",
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


def test_misure_uguali_al_pdf_tranne_166():
    got = [
        (m["NAME"], reg_of(m), fmt_of(m), m["TYPE"], m["DRIVERDATA"])
        for m in observed()["measures"]
    ]
    # REG 166 (DBW 394, TAG COT_XTM, descrizione vuota) trattato a parte:
    # il resto coincide riga per riga.
    assert [g for g in got if g[1] != 166] == PDF_MEASURES


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
    assert packed == {k: PDF_BITS[k] for k in (1, 2, 3, 4)}
    assert len(observed()["bitinfo"]) == 47


def test_texton_e_textoff_sempre_compilati():
    for b in observed()["bitinfo"]:
        assert b["TEXTON"], b
        assert b["TEXTOFF"], b


def test_misura_166_nome_variabile_per_run():
    """REG 166 esiste (DBW 394, TAG COT_XTM, descrizione vuota) ma il nome
    cambia per run: 'Misura stimata CO' (run3, run5) o 'Misura stimata COT'
    (run4). E' variabilita' VLM su riga ambigua, non un difetto di script:
    il registro e' giusto in tutte le run. Se esce un terzo nome, rivalutare.
    """
    st = observed()
    reg166 = [m for m in st["measures"] if reg_of(m) == 166]
    assert len(reg166) == 1
    assert reg166[0]["NAME"] in ("Misura stimata CO", "Misura stimata COT")
    assert fmt_of(reg166[0]) == 250


def test_stati_recuperati_con_carry_over():
    """Chiuso con il consolidatore del 6/10 (registro_applicato): i cinque
    stati di REG 4 (bit 3-7) ci sono, con i TEXTON da keyword. Erano le
    colonne STATI IMPIANTO della Tabella 12 del JOB."""
    st = observed()
    got = {b["BITNAME"]: (b["BITNO"], b["TEXTON"]) for b in st["bitinfo"]}
    for nome, bit in BIT_PERSI.items():
        assert got[nome][0] == bit, (nome, got.get(nome))
    assert got["IMPIANTO IN SPEGNIMENTO"][1] == "SPEGNIMENTO"
    assert got["IMPIANTO IN LAVAGGIO"][1] == "ATTIVO"
    assert got["IMPIANTO FUORI SERVIZIO PER GUASTO"][1] == "GUASTO"
    warn = " ".join(st.get("_warnings", []))
    assert "VARIABILI SENZA INDIRIZZO" not in warn, warn


def test_stazione_nome_variabile_ip_e_porta_fissi():
    """IP/porta dal JOB Tabella 8 (PLC 172.16.1.31:511) e una sola stazione
    sono stabili. Il NAME invece varia per run: il ramo Station a volte
    restituisce null e il merge ripiega su 'SME'. Le due forme viste sono
    'Sistema Analisi Emissioni' (dichiarato nel JOB) e 'SME': la scelta del
    nome atteso resta aperta per il cliente."""
    out = [observed()]
    assert len(out) == 1
    st = out[0]
    assert st["NAME"] in ("Sistema Analisi Emissioni", "SME"), st["NAME"]
    assert 'ipaddress="172.16.1.31"' in st["DRIVERCONFIG"]
    assert 'tcpport="511"' in st["DRIVERCONFIG"]
    assert "192.168.70.103" not in json.dumps(st)


def test_unita_collegate_per_tag():
    """Join per TAG (consolidatore + prompt v6): il JOB dichiara 18 unita'
    (Tabella 9). Nella run5 ne arrivano 17: resta fuori solo Consumo
    combustibile orario (la scala c'e', l'unita' no: riga scala incompleta
    dal ramo Station). Nella run4 mancavano anche le due O2.
    Le unita' si confrontano normalizzate: il VLM scrive 'mg/Nm3' o 'mg/Nm³'
    a seconda della run, il JOB usa ASCII."""
    st = observed()
    norm = lambda u: (u or "").replace("³", "3")
    units = {m["NAME"]: norm(m["UNITS"]) for m in st["measures"]}
    applicate = {k: v for k, v in units.items() if v}
    attese = {
        "CO": "mg/Nm3", "NO": "mg/Nm3", "COT": "mg/Nm3", "NH3": "mg/Nm3",
        "O2 Secco": "%", "O2 Umido": "%",
        "Temperatura fumi": "°C", "Pressione differenziale fumi": "Pa",
        "Concentrazione polveri": "mg/Nm3", "Temperatura urea": "°C",
        "Temperatura SCR": "°C", "Potenza motore": "kW", "Potenza turbina": "kW",
        "Potenza totale recuperata": "kW", "Potenza totale verso turbina": "kW",
        "Potenza termica immessa in motore": "kW", "Consumo combustibile": "kg",
    }
    assert applicate == attese
    for nome, u in applicate.items():
        assert norm(UNITA_DICHIARATE_NEL_JOB[nome]) == u
    mancanti = [n for n in UNITA_DICHIARATE_NEL_JOB if not units.get(n)]
    assert mancanti == ["Consumo combustibile orario"], mancanti


def test_range_da_fondo_scala_e_warning_limiti_divisioni():
    """v4.5: il fondo scala dichiarato va in LOWRANGE/HIGHRANGE; limiti e
    divisori restano nel chunk e compaiono in review coi nomi (mapping BISON
    col cliente, decisione 6/10/2026)."""
    st = observed()
    by_name = {m["NAME"]: m for m in st["measures"]}
    assert (by_name["CO"]["LOWRANGE"], by_name["CO"]["HIGHRANGE"]) == (0.0, 200.0)
    assert (by_name["Temperatura fumi"]["LOWRANGE"], by_name["Temperatura fumi"]["HIGHRANGE"]) == (0.0, 500.0)
    assert (by_name["Consumo combustibile"]["LOWRANGE"], by_name["Consumo combustibile"]["HIGHRANGE"]) == (0.0, 110000.0)
    assert (by_name["Misura stimata CO"]["LOWRANGE"], by_name["Misura stimata CO"]["HIGHRANGE"]) == (-3.40282e38, 3.40282e38)
    warn = " ".join(st.get("_warnings", []))
    assert "LIMITI DICHIARATI NON APPLICATI IN ADAS" in warn
    assert "CO (giornaliero=40, orario=50)" in warn
    assert "DIVISIONE NON APPLICATA IN ADAS" in warn
    assert "Temperatura urea (divisione x10)" in warn


def test_sentinel_limiti_conforme_al_repo():
    """Chiuso con la copia canvas del 6/10: le analogiche escono con il
    sentinel `-3.40282e38` / `+3.40282e38` come il repo e tutti i GT legacy.
    Se torna `null`, lo script sul canvas non e' la copia canvas del repo.
    """
    for m in observed()["measures"]:
        if m["TYPE"] == 0:
            assert m["LOWCRITICAL"] == -3.40282e38
            assert m["HIGHCRITICAL"] == 3.40282e38