"""Verita' PDF Single: SMA a due stazioni, SIEMENS 40014, GT solo regressione.

Metodo di `test_adas_caso6_pdf_truth.py` e `test_adas_caso7_pdf_truth.py`:
la verita' e' il PDF letto riga per riga, non il ground truth legacy.
Qui i PDF sono `Mappatura_1_Cliente_SMA_1.pdf` (1 pagina, due tabelle con
gli stessi registri su stazioni diverse) e `Mappatura_4_Cliente_SIEMENS_2.pdf`
(29 pagine ruotate, verita' del registro 40014 a pagina 5).

Verita' PDF SMA_1, colonne IP | TIPO | DESCRIZIONE | REGISTRO:

    192.168.6.20       ANALOGICO  CO                 40001
    192.168.6.20       ANALOGICO  Pressione          40005
    IP xxx,xxx,xxx,xxx Modbus     Temperatura Fumi   40001
    IP xxx,xxx,xxx,xxx Modbus     CO                 40005
    192.168.6.20       INPUT DIGITALE  Allarme 1 Ossiegno umido  00045

Lo stesso registro esiste in due tabelle diverse: l'abbinamento va fatto
su (stazione, registro, bit), non sul solo registro. L'output storico
`Output SMA_1.txt` le separa correttamente (`E1` @ 192.168.6.20 con CO e
Pressione, `E1 1` @ xxx con Temperatura Fumi e CO): il confronto che
ignora la stazione segnala 2 falsi `nome_diverso`.

Verita' PDF SIEMENS_2 pagina 5, registro 40014, 16 righe con N.Bit 9..16
poi 1..8 (N.Bit e' base 1, quindi bit 8..15 poi 0..7). Il testo pieno e'
letto dal layer del PDF, non dall'estrattore coordinato che tronca le
descrizioni lunghe a 110 punti (`BL1` e `(Da Resettare)` cadono fuori
banda: l'output storico e il legacy li hanno, l'estrazione no).

Il GT legacy `Json_4_Cliente_SIEMENS_2.json` non e' un riferimento: sul
40014 numera i bit 1..16 (N.Bit grezzo, senza -1) e scrive `SONDADI`.
"""
import importlib.util
import json
import os
import struct

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFRONTA_PATH = os.path.join(
    REPO, "myhydra", "single_pdf", "verifica_pdf", "confronta.py")
PER_CASO = os.path.join(
    REPO, "myhydra", "single_pdf", "verifica_pdf", "per_caso")
OUT_DIR = os.path.join(REPO, "myhydra", "single_pdf", "Outputs MYHYDRA")
GT_SIEMENS = os.path.join(
    REPO, "data", "test_outputs", "Json_4_Cliente_SIEMENS_2.json")


def _load_confronta():
    spec = importlib.util.spec_from_file_location("confronta", CONFRONTA_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


cf = _load_confronta()

# (registro, ip come sta nel PDF, descrizione come sta nel PDF)
SMA_PIN_ROWS = [
    (40001, "192.168.6.20", "CO"),
    (40005, "192.168.6.20", "Pressione"),
    (40001, "IP xxx,xxx,xxx,xxx", "Temperatura Fumi"),
    (40005, "IP xxx,xxx,xxx,xxx", "CO"),
    (45, "192.168.6.20", "Allarme 1 Ossiegno umido"),
]

# (bit, descrizione piena dal layer del PDF, pagina 5, ordine di riga)
PDF_40014_ROWS = [
    (8, "COG2: ALLARME TEMPERATURA SONDA DI PRELIEVO"),
    (9, "COG2: ALLARME TEMPERATURA LINEA DI PRELIEVO BL1"),
    (10, "COG2: BLOCCO ALTISSIME TEMPERATURE In REGOLAZIONE BL1"),
    (11, "COG2: ALLARME FRIGO"),
    (12, "COG2: ALLARME PRESENZA CONDENSA"),
    (13, "COG2: MEMORIA PRESENZA CONDENSA (Da Resettare)"),
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
PDF_40014_BITS = [b for b, _ in PDF_40014_ROWS]


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def tabella(caso):
    return load_json(os.path.join(PER_CASO, caso, "tabella_pdf.json"))["righe"]


def output_storico(nome_file):
    return cf.leggi_output(os.path.join(OUT_DIR, nome_file))


def verdetto(tab, stazioni):
    per_chiave, per_output, per_senza_reg = cf.confronta(tab, stazioni)
    return per_chiave, per_output, per_senza_reg


def _riga_pdf(registro, bit, descrizione, ip="", pagina=1):
    return {"pagina": pagina, "ip": ip, "registro": registro,
            "registro_grezzo": str(registro), "convenzione": "4xxxx",
            "bit": bit, "descrizione": descrizione, "stato": "",
            "unita": "", "read_write": "", "data_type": "",
            "scala_inizio": "", "scala_fondo": "", "limite": "", "nota": ""}


def _stazione(nome, ip, misure):
    return {"nome": nome, "id": 1, "ip": ip, "driverconfig": "",
            "misure": misure, "n_bitinfo": 0, "_warnings": None,
            "_meta_input": {}}


def _misura(mid, nome, registro):
    return {"id": mid, "nome": nome, "registro": registro, "formato": 150,
            "driverdata": 0, "type": 0, "unita": None, "bits": []}


def test_pin_sma_coerenti_con_estrazione_pdf():
    tab = tabella("caso_1_sma_1")
    for registro, ip, descrizione in SMA_PIN_ROWS:
        uguali = [r for r in tab
                  if r["registro"] == registro and r["descrizione"] == descrizione]
        assert uguali, (registro, descrizione)
        assert any(r["ip"] == ip for r in uguali), (registro, descrizione, ip)


def test_pin_40014_coerenti_con_estrazione_pdf():
    """Le righe pinnate sono quelle estratte, nello stesso ordine di riga.

    Il testo pinnato e' quello pieno del PDF: dove l'estrattore coordinato
    tronca (banda di 110 punti), il suo testo e' un troncamento del pieno,
    non un testo diverso.
    """
    tab = tabella("caso_4_siemens_2")
    righe = [r for r in tab if r["registro"] == 40014]
    assert [r["bit"] for r in righe] == PDF_40014_BITS
    assert [r["pagina"] for r in righe] == [5] * 16
    for riga_pdf, (_, pieno) in zip(righe, PDF_40014_ROWS):
        estratto = riga_pdf["descrizione"]
        assert estratto == pieno or estratto in pieno, (estratto, pieno)


def test_sma_stesso_registro_due_stazioni_ok():
    """Il cuore del fix: (stazione, registro) distingue, registro no."""
    tab = [_riga_pdf(40001, None, "CO", ip="192.168.6.20"),
           _riga_pdf(40001, None, "Temperatura Fumi",
                      ip="IP xxx,xxx,xxx,xxx")]
    stazioni = [_stazione("E1", "192.168.6.20",
                          [_misura(1, "CO", 40001)]),
                _stazione("E1 1", "xxx.xxx.xxx.xxx",
                          [_misura(1, "Temperatura Fumi", 40001)])]
    per_chiave, per_output, _ = cf.confronta(tab, stazioni)
    assert per_output == []
    assert [v["esito"] for v in per_chiave] == ["ok", "ok"]
    stazioni_pdf = sorted(v["stazione_pdf"] for v in per_chiave)
    assert stazioni_pdf == ["192.168.6.20", "xxx.xxx.xxx.xxx"]


def test_verdetto_sma_zero_difetti():
    """I 2 `nome_diverso` su 40001/40005 erano falsi positivi da match
    senza stazione: l'output separa correttamente le due tabelle."""
    per_chiave, per_output, _ = verdetto(
        tabella("caso_1_sma_1"), output_storico("Output SMA_1.txt"))
    assert per_output == []
    difetti = [v for v in per_chiave if v["classe"] == "difetto"]
    assert difetti == []
    ok = [v for v in per_chiave if v["esito"] == "ok"]
    assert len(ok) == 44


def test_40014_output_storico_uguale_al_pdf():
    stazioni = output_storico("OUTPUT SIEMENS 2.txt")
    misura = next(m for m in stazioni[0]["misure"] if m["registro"] == 40014)
    assert [b["BITNO"] for b in misura["bits"]] == PDF_40014_BITS
    attesi = [cf.chiave_nome(d) for _, d in PDF_40014_ROWS]
    assert [cf.chiave_nome(b["BITNAME"]) for b in misura["bits"]] == attesi


def test_gt_ha_errori_noti_il_nostro_no():
    """Il legacy non e' un riferimento: fissa dove sbaglia sul 40014."""
    gt = load_json(GT_SIEMENS)
    st = gt[0] if isinstance(gt, list) else gt

    def reg(m):
        return struct.unpack("<I", bytes.fromhex(m["DRIVERPRIVATE"][2:10]))[0]

    mid_gt = next(m["ID"] for m in st["measures"] if reg(m) == 40014)
    bit_gt = sorted(b["BITNO"] for b in st["bitinfo"]
                    if b["MEASUREID"] == mid_gt)
    assert bit_gt == list(range(1, 17))
    nomi_gt = [b["BITNAME"] for b in st["bitinfo"]
               if b["MEASUREID"] == mid_gt]
    assert any("SONDADI" in n for n in nomi_gt)

    misura = next(m for m in output_storico("OUTPUT SIEMENS 2.txt")[0]["misure"]
                  if m["registro"] == 40014)
    assert [b["BITNO"] for b in misura["bits"]] == PDF_40014_BITS
    assert not any("SONDADI" in b["BITNAME"] for b in misura["bits"])


def test_protec_verdetti_senza_difetti_e_con_scarti():
    attesi = {"caso_2_protec_1": ("Output PROTEC 1.txt", 89, 44,
                                  {"v2_nome_generico"}),
              "caso_3_protec_2": ("OUTPUT PROTEC 2.txt", 79, 40,
                                  {"v2_nome_generico",
                                   "v20_zona_esclusa"})}
    for caso, (output, n_righe, n_saltate, scarti_attesi) in attesi.items():
        tab = tabella(caso)
        assert len(tab) == n_righe
        per_chiave, per_output, _ = verdetto(tab, output_storico(output))
        assert per_output == []
        assert [v for v in per_chiave if v["classe"] == "difetto"] == []
        assert [v for v in per_chiave
                if v["esito"] == "non_coperta_dall_output"] == []
        saltate = [v for v in per_chiave
                   if v["esito"] == "saltata_da_regola_di_prompt"]
        assert len(saltate) == n_saltate
        # PROTEC_2 scarta anche 8 righe `Non Utilizzato` per zona V20,
        # PROTEC_1 solo nomi generici V2: le classi lo mostrano.
        assert {v["scarto"] for v in saltate} == scarti_attesi


def test_classi_di_scarti_siemens():
    """Le righe scartate portano la classe del motivo: generico V2, zona
    esclusa V20, riga vuota. Senza, sono un unico mucchio indistinto."""
    per_chiave, _, _ = verdetto(tabella("caso_4_siemens_2"),
                                output_storico("OUTPUT SIEMENS 2.txt"))
    saltate = { (v["registro"], v["bit"]): v["scarto"] for v in per_chiave
                if v["esito"] == "saltata_da_regola_di_prompt" }
    assert saltate[(40037, None)] == "v2_nome_generico"
    # Pagina 12 senza copertura: righe di zona esclusa, mai emesse.
    assert saltate[(40031, 8)] == "v20_zona_esclusa"
    vuote = {v["scarto"] for v in per_chiave
             if v["esito"] == "saltata_da_regola_di_prompt"
             and v["pdf_descrizione"] == ""}
    assert vuote == {"riga_vuota"}
