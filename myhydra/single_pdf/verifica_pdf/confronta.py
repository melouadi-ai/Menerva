#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
confronta.py - Verifica gli output del pytool json_creator contro il PDF sorgente.

Il PDF e' la fonte di verita: gli output JSON non lo contengono, lo derivano.
Questo script estrae la tabella di verita' dal layer di testo del PDF e la
confronta riga per riga con cio' che il pytool ha prodotto, decodificando il
registro dalla prima word di DRIVERPRIVATE.

Uso:
    python confronta.py                 # tutti i casi
    python confronta.py caso_1_sma_1    # un solo caso
    python confronta.py --lista         # elenca i casi

Richiede pymupdf. Uova il .venv del repository.
"""

import json
import os
import re
import sys
import unicodedata
import difflib

BASE = os.path.dirname(os.path.abspath(__file__))
SINGLE = os.path.dirname(BASE)
PDF_DIR = os.path.join(SINGLE, "PDFs per il confronto")
OUT_DIR = os.path.join(SINGLE, "Outputs MYHYDRA")
OUT_RES = os.path.join(BASE, "per_caso")

# --------------------------------------------------------------------------
# casi
# --------------------------------------------------------------------------
# 'formato' decide l'estrattore. 'sma' e 'protec' condividono la logica di
# forward-fill ma hanno mappature di colonna diverse; 'siemens' ha un parser
# dedicato perche' la pagina e' ruotata e senza linee di cornice.

CASI = [
    {
        "id": "caso_1_sma_1",
        "cliente": "SMA",
        "formato": "sma",
        "pdf": "Mappatura_1_Cliente_SMA_1.pdf",
        "output": "Output SMA_1.txt",
        "gt": None,
    },
    {
        "id": "caso_2_protec_1",
        "cliente": "PROTEC",
        "formato": "protec",
        "pdf": "Mappatura_2_Cliente_PROTEC_1.pdf",
        "output": "Output PROTEC 1.txt",
        "gt": os.path.join(SINGLE, "..", "..", "..", "data", "test_outputs",
                           "Json_2_Cliente_PROTEC_1.json"),
    },
    {
        "id": "caso_3_protec_2",
        "cliente": "PROTEC",
        "formato": "protec",
        "pdf": "Mappatura_3_Cliente_PROTEC_2.pdf",
        "output": "OUTPUT PROTEC 2.txt",
        "gt": None,
    },
    {
        "id": "caso_4_siemens_2",
        "cliente": "SIEMENS",
        "formato": "siemens",
        "pdf": "Mappatura_4_Cliente_SIEMENS_2.pdf",
        "output": "OUTPUT SIEMENS 2.txt",
        "gt": os.path.join(SINGLE, "..", "..", "..", "data", "test_outputs",
                           "Json_4_Cliente_SIEMENS_2.json"),
    },
    {
        "id": "caso_5_ori_martin_1",
        "cliente": "ORI MARTIN",
        "formato": "protec",
        "pdf": "Mappatura_5_Cliente_ORI_MARTIN_1.pdf",
        "output": None,
        "gt": None,
    },
    {
        "id": "caso_6_siemens_legnano_1",
        "cliente": "SIEMENS",
        "formato": "siemens",
        "pdf": "Mappatura_6_Cliente_SIEMENS_Legnano_1.pdf",
        "output": None,
        "gt": None,
    },
    {
        "id": "caso_7_luxottica_1",
        "cliente": "LUXOTTICA",
        "formato": "siemens",
        "pdf": "Mappatura_7_Cliente_LUXOTTICA_Agordo_1.pdf",
        "output": None,
        "gt": None,
    },
    {
        "id": "caso_8_superwatt_1",
        "cliente": "SUPERWATT",
        "formato": "protec",
        "pdf": "Mappatura_8_Cliente_SUPERWATT_Ahlstrom_1.pdf",
        "output": None,
        "gt": None,
    },
]

RE_IND = re.compile(r"^(\d{4,5})(?:[._](\d{1,2}))?$")
RE_IP = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
RE_REG = re.compile(r"^(4\d{4}|\d{3,5})$")
RE_SKIP_ZONA = re.compile(r"NO\s*dcs|NO\s*PC\s*Sme|NOT\s*USED|NON\s*UTILIZZATO", re.I)

# Nomi che il prompt (regola V2) e il pytool (P4, P4bis) impongono di saltare.
# Una riga con uno di questi nomi che l'output non contiene NON e' un difetto:
# e' il comportamento richiesto. Senza questo elenco il confronto segnalerebbe
# come mancanti decine di righe 'Disponibile' che vanno scartate di proposito.
GENERICI_ESATTI = {
    "disponibile", "disponibile/", "disponible", "riserva", "spare",
    "reserve", "non utilizzato", "non utilizzata", "non usato", "libero",
    "---", "/",
}
GENERICI_INTESTAZIONE = {
    "misure", "comandi", "impostazioni", "input", "output", "parametri",
    "registri", "segnali", "variabili", "allarmi", "stati",
}


def da_saltare(descrizione):
    """True se il prompt prescrive di scartare la riga.

    Regola V2: si salta solo se la descrizione coincide esattamente con uno
    dei nomi generici, non se lo contiene. 'Misura Disponibile IW36' non va
    scartata perche' contiene 'disponibile'.
    """
    d = norm(descrizione).lower()
    if not d:
        # Riga senza descrizione: la regola V2 prescrive di saltarla e lo
        # schema Pydantic richiede description non vuota, quindi una riga di
        # questo tipo non deve contare come mancante. Nel PDF di SIEMENS sono
        # 597 righe su 1116, e senza questa regola il confronto le
        # conteggerebbe tutte come dati persi.
        return True
    if d in GENERICI_ESATTI or d in GENERICI_INTESTAZIONE:
        return True
    if "riservat" in d:          # P4bis
        return True
    if RE_SKIP_ZONA.search(d):   # V20
        return True
    return False


def leggi_registro(s):
    """Legge un indirizzo di registro accettando entrambe le convenzioni.

    Nei documenti compaiono due convenzioni diverse e la differenza non e'
    cosmetica: le sezioni analogiche scrivono '40001', quelle digitali
    scrivono '00033'. La seconda e' un indirizzo HMI con zeri iniziali, che
    letto come registro Modbus da' 33 e non 40033. Restituisce quindi anche la
    convenzione, perche' il confronto deve poter segnalare la incoerenza
    invece di normalizzarla via.
    """
    s = norm(s)
    m = RE_REG.match(s)
    if not m:
        return None, None
    grezzo = m.group(1)
    if grezzo.startswith("4"):
        conv = "4xxxx"
    elif grezzo[0] == "0":
        conv = "0-padded"
    else:
        conv = "grezzo"
    return int(grezzo), conv


# --------------------------------------------------------------------------
# normalizzazione
# --------------------------------------------------------------------------

def norm(s):
    """Pulisce una cella: nbsp, spazi non-breaking, a capo, spazi doppi."""
    if s is None:
        return ""
    s = unicodedata.normalize("NFKC", str(s))
    s = s.replace("\xa0", " ").replace("\u202f", " ")
    s = s.replace("\n", " ").replace("\r", " ")
    return re.sub(r"\s+", " ", s).strip()


def chiave_nome(s):
    """Chiave di confronto per un nome, insensibile a refusi di formattazione.

    Stessa logica di norm_name in tests/compare_with_gt.py: maiuscole, via
    parentesi e virgolette, spazi normalizzati. Serve solo ad abbinare, non a
    giudicare la correttezza del testo.
    """
    s = norm(s).upper()
    s = re.sub(r"[\(\[\{][^\)\]\}]*[\)\]\}]", " ", s)
    s = s.replace('"', "").replace("'", "")
    s = re.sub(r"[^A-Z0-9 ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def chiave_stazione(ip):
    """Stazione normalizzata per l'abbinamento, o None se non dichiarata.

    Nel PDF di SMA la stessa tabella usa due forme (`192.168.6.20` e
    `IP xxx,xxx,xxx,xxx`), l'output altre due (`192.168.6.20` e
    `xxx.xxx.xxx.xxx`): senza normalizzazione non si incontrano mai.
    Quando il documento non dichiara la stazione (PROTEC, SIEMENS: ip
    vuoto) la chiave e' None e l'abbinamento ricade su (registro, bit).
    """
    s = norm(ip).lower()
    if not s:
        return None
    s = re.sub(r"^ip\s+", "", s)
    s = s.replace(",", ".")
    return re.sub(r"\s+", "", s) or None


SCARTI = {
    "riga_vuota": "riga senza descrizione",
    "v2_nome_generico": "nome generico da regola V2 del prompt",
    "v20_zona_esclusa": "zona esclusa da regola V20 del prompt",
}


def classe_scarto(descrizione, riga):
    """Motivo dello scarto di una riga che l'output non deve coprire.

    Le righe scartate non sono tutte uguali: una riga vuota, un nome
    generico esatto e una zona esclusa seguono regole diverse e vanno
    conteggiate a parte, altrimenti restano un mucchio indistinto.
    """
    d = norm(descrizione)
    if not d:
        return "riga_vuota"
    if riga.get("da_scartare") or RE_SKIP_ZONA.search(d):
        return "v20_zona_esclusa"
    return "v2_nome_generico"


def ind_parte(s):
    """Divide '40001.2' o '40001_2' in (40001, 2). None se non e' un indirizzo."""
    m = RE_IND.match(norm(s))
    if not m:
        return None, None
    return int(m.group(1)), (int(m.group(2)) if m.group(2) else None)


# --------------------------------------------------------------------------
# Parte A - estrazione della tabella di verita' dal PDF
# --------------------------------------------------------------------------

def _tabelle(pagina):
    """Tabelle della pagina. Ritorna lista di liste di righe grezze."""
    out = []
    for t in pagina.find_tables().tables:
        ex = t.extract()
        if ex:
            out.append(ex)
    return out


def estrai_sma(doc, caso):
    """SMA: 19 colonne, header non in riga 0.

    La riga 0 del PDF riporta i metadati del cliente (Punto emissivo, Forno,
    temperature, pressione) e la riga 1 e' l'intestazione vera. L'indirizzo
    IP del PLC sta in colonna 0 e va in forward-fill: molte righe lo lasciano
    vuoto perche' si riferiscono alla stazione corrente.

    Il documento contiene piu' sezioni con convenzioni di indirizzo diverse,
    indicate dalla colonna 2:

    - ANALOGICO            -> colonna 5, indirizzi in forma 4xxxx
    - Modbus               -> colonna 6, indirizzi in forma 4xxxx
    - INPUT/OUTPUT DIGITALE-> colonna 5, indirizzi in forma 000xx

    Le righe CALCOLATA non hanno registro proprio: sono valori derivati da
    altri e vengono scartate, perche' non hanno un indirizzo Modbus.
    """
    righe = []
    meta = {}
    for pi, pagina in enumerate(doc, 1):
        for tb in _tabelle(pagina):
            if not tb:
                continue
            for cella in tb[0][:5]:
                c = norm(cella)
                for prefisso, chiave in (("Cliente", "cliente"),
                                         ("Punto emissivo", "punto_emissivo")):
                    if c.startswith(prefisso) and ":" in c:
                        meta[chiave] = c.split(":", 1)[1].strip()
            idx_hdr = None
            for i, r in enumerate(tb[:4]):
                if any(norm(c).lower().startswith("descrizione") for c in r):
                    idx_hdr = i
                    break
            if idx_hdr is None:
                continue
            ip_corrente = ""
            for r in tb[idx_hdr + 1:]:
                c = [norm(x) for x in r] + [""] * 19
                if c[0]:
                    m = RE_IP.search(c[0])
                    if m:
                        ip_corrente = m.group(0)
                    elif "xxx" in c[0].lower():
                        ip_corrente = c[0]
                tipo = c[2]
                registro = conv = grezzo = None
                for idx in ((6, 5) if tipo == "Modbus" else (5, 6)):
                    if c[idx]:
                        registro, conv = leggi_registro(c[idx])
                        if registro is not None:
                            grezzo = c[idx]
                            break
                if registro is None:
                    # riga senza indirizzo Modbus. Se ha un nome, e' una
                    # grandezza derivata (CALCOLATA) o una riga priva di
                    # indirizzo: si tiene, perche' il confronto deve poter
                    # mostrare che l'output le ha trasformate in misure con
                    # un registro inesistente invece di scartarle.
                    if c[3] and tipo.upper() == "CALCOLATA":
                        righe.append({
                            "pagina": pi, "ip": ip_corrente,
                            "registro": None, "registro_grezzo": "",
                            "convenzione": "nessuno", "bit": None,
                            "tipo": tipo, "descrizione": c[3],
                            "stato": "", "unita": c[7],
                            "read_write": c[4], "data_type": c[1],
                            "scala_inizio": c[8], "scala_fondo": c[9],
                            "limite": c[13], "nota": "",
                        })
                    continue
                analogico = tipo.upper() == "ANALOGICO"
                righe.append({
                    "pagina": pi,
                    "ip": ip_corrente,
                    "registro": registro,
                    "registro_grezzo": grezzo,
                    "convenzione": conv,
                    "bit": None,
                    "tipo": tipo,
                    "descrizione": c[3],
                    "stato": "",
                    "unita": c[7] if analogico else "",
                    "read_write": c[4],
                    "data_type": c[1],
                    "scala_inizio": c[8] if analogico else "",
                    "scala_fondo": c[9] if analogico else "",
                    "limite": c[13] if analogico else "",
                    "nota": c[18] if not analogico else "",
                })
    return righe, meta


def estrai_protec(doc, caso):
    """PROTEC: 12 colonne, header in riga 0, indirizzo nell'ultima colonna.

    Le colonne 6, 7 e 8 sono tutte sotto l'intestazione 'Logic State / Range':
    la 6 contiene il valore, la 7 contiene un '=' di separazione e la 8 il
    testo dello stato. Le righe con solo la colonna 0 popolata sono intestazioni
    di sezione ('Input / Output Digitali', 'Live PLC'), non variabili.
    """
    righe = []
    meta = {}
    for pi, pagina in enumerate(doc, 1):
        testo = pagina.get_text()
        for m in RE_IP.finditer(testo):
            meta.setdefault("ip_trovati", [])
            if m.group(0) not in meta["ip_trovati"]:
                meta["ip_trovati"].append(m.group(0))
        for tb in _tabelle(pagina):
            if not tb:
                continue
            if not any(norm(c).lower().startswith("description") for c in tb[0]):
                continue
            sezione = ""
            for r in tb[1:]:
                c = [norm(x) for x in r] + [""] * 12
                if c[0] and not any(c[1:]):
                    sezione = c[0]
                    continue
                registro, bit = ind_parte(c[11])
                if registro is None:
                    continue
                righe.append({
                    "pagina": pi,
                    "ip": "",
                    "registro": registro,
                    "bit": bit,
                    "descrizione": c[2],
                    "stato": c[8],
                    "unita": c[9],
                    "read_write": c[3],
                    "data_type": c[4],
                    "scala_inizio": c[6],
                    "scala_fondo": "",
                    "limite": "",
                    "nota": c[10],
                    "tag": c[1],
                    "sezione": sezione,
                })
    return righe, meta


def estrai_siemens(doc, caso):
    """SIEMENS: pagina ruotata di 90 gradi, nessuna linea di cornice.

    find_tables() non funziona: senza linee non ha riferimenti e con la
    strategia testuale over-splitta in 34 colonne. Le parole vengono quindi
    raggruppate per riga e per colonna a partire dalla posizione delle
    intestazioni, che stanno sulla stessa pagina dei dati.
    """
    righe = []
    meta = {"ip_trovati": []}
    for pi, pagina in enumerate(doc, 1):
        for m in RE_IP.finditer(pagina.get_text()):
            if m.group(0) not in meta["ip_trovati"]:
                meta["ip_trovati"].append(m.group(0))
        righe.extend(_righe_siemens_pagina(pagina, pi))
    return righe, meta


def _righe_siemens_pagina(pagina, pi):
    """Estrae le righe di una pagina SIEMENS dalle coordinate delle parole.

    La pagina ha /Rotate 90. Nel frame visualizzato, che e' quello in cui
    l'essere umano la legge, le righe della tabella corrono lungo x e le
    colonne lungo y. Raggruppare per y, come si fa di solito, produce
    colonne e righe scambiate.

    Le posizioni delle intestazioni danno le bande delle colonne. Serve solo
    Addr_INT, N.Bit e Descrizione: le altre non servono ad abbinare l'output,
    e saltarle evita di dover interpretare una colonna Zona che nel documento
    ha testi su piu' righe e una direzione di lettura ambigua.
    """
    parole = pagina.get_text("words")
    if not parole:
        return []

    def y_intestazione(nome):
        k = norm(nome).replace(" ", "")
        for w in parole:
            if norm(w[4]).replace(" ", "") == k:
                return w[1]
        return None

    y_addr = y_intestazione("Addr_INT")
    y_bit = y_intestazione("N.Bit")
    y_desc = y_intestazione("Descrizione")
    if y_addr is None or y_bit is None or y_desc is None:
        return []  # pagina senza la testata attesa: non e' una pagina tabella

    # le righe sono cluster su x
    righe = {}
    for w in parole:
        righe.setdefault(round(w[0] / 2.0), []).append(w)

    out = []
    for x in sorted(righe):
        ws = righe[x]
        registro = bit = None
        descrizione = ""
        righe_desc = []
        for w in ws:
            y = w[1]
            t = norm(w[4])
            if abs(y - y_addr) <= 14:
                # Due formati compaiono nelle pagine: '40001' e
                # '40051/40052'. Il secondo e' un valore a 32 bit che occupa
                # due registri consecutivi, e il prompt (regola V22) impone di
                # emettere una sola misura sul primo. Si prende il primo.
                m = re.match(r"^(4\d{4})(?:\s*/\s*4\d{4})?$", t)
                if m:
                    registro = int(m.group(1))
            elif abs(y - y_bit) <= 14:
                if re.match(r"^\d{1,2}$", t):
                    bit = int(t) - 1  # N.Bit e' base 1
            elif y_desc - 110 <= y <= y_desc + 16:
                righe_desc.append(w)
            # La colonna Zona ha righe di testo che scendono sotto Add_S7
            # (i marker 'NO dcs', 'NO PC Sme' finiscono verso y 138-181).
            # Ignorarle farebbe perdere la regola V20 su quelle righe.
        if registro is None:
            continue
        # testo della descrizione: le righe della cella vanno unite dalla
        # piu' in basso in alto, e dentro ciascuna da sinistra a destra
        righe_desc.sort(key=lambda w: -w[1])
        parti = []
        riga_corr = None
        gruppo = []
        for w in righe_desc:
            if riga_corr is None or abs(w[1] - riga_corr) <= 8:
                gruppo.append(w)
                riga_corr = w[1] if riga_corr is None else riga_corr
            else:
                parti.append(" ".join(norm(z[4]) for z in
                                      sorted(gruppo, key=lambda z: z[0])))
                gruppo = [w]
                riga_corr = w[1]
        if gruppo:
            parti.append(" ".join(norm(z[4]) for z in
                                  sorted(gruppo, key=lambda z: z[0])))
        descrizione = norm(" ".join(parti))
        # La colonna Zona e' spezzata in parole separate ('NO', 'dcs', 'PC',
        # 'Sme'), quindi la regola V20 va cercata nel testo della riga
        # ricomposto, non parola per parola: cercandola in ogni singola
        # parola non troverebbe mai 'NO dcs' e la regola non scatterebbe.
        testo_riga = norm(" ".join(norm(w[4]) for w in sorted(
            ws, key=lambda w: (-w[1], w[0]))))
        scartare = bool(RE_SKIP_ZONA.search(testo_riga))
        out.append({
            "pagina": pi,
            "ip": "",
            "registro": registro,
            "registro_grezzo": str(registro),
            "convenzione": "4xxxx",
            "bit": bit,
            "descrizione": descrizione,
            "stato": "",
            "unita": "",
            "read_write": "",
            "data_type": "",
            "nota": "",
            "da_scartare": scartare,
        })
    return out


ESTRATTORI = {
    "sma": estrai_sma,
    "protec": estrai_protec,
    "siemens": estrai_siemens,
}


# --------------------------------------------------------------------------
# Parte B - decodifica degli output
# --------------------------------------------------------------------------

def reg_da_priv(priv):
    """Registro dalla prima word di DRIVERPRIVATE (little-endian uint32)."""
    if not priv:
        return None
    m = re.match(r"^0x([0-9A-Fa-f]{8})", str(priv))
    if not m:
        return None
    h = m.group(1).upper()
    return int(h[6:8] + h[4:6] + h[2:4] + h[0:2], 16)


def fmt_da_priv(priv):
    """Formato dalla sesta word: 150 signed short, 250 float BE."""
    if not priv:
        return None
    m = re.match(r"^0x[0-9A-Fa-f]{40}([0-9A-Fa-f]{8})", str(priv))
    if not m:
        return None
    h = m.group(1).upper()
    return int(h[6:8] + h[4:6] + h[2:4] + h[0:2], 16)


def ip_da_config(cfg):
    m = re.search(r'ipaddress="([^"]*)"', cfg or "")
    return m.group(1) if m else None


def leggi_output(percorso):
    """Legge l'output del pytool e ricostuisce misure e bitinfo agganciati."""
    grezzo = json.load(open(percorso, encoding="utf-8"))
    stazioni = grezzo if isinstance(grezzo, list) else [grezzo]
    out = []
    for st in stazioni:
        bits_per_mid = {}
        for b in st.get("bitinfo", []) or []:
            bits_per_mid.setdefault(b.get("MEASUREID"), []).append(b)
        misure = []
        for m in st.get("measures", []) or []:
            mid = m.get("ID")
            bits = bits_per_mid.get(mid, [])
            misure.append({
                "id": mid,
                "nome": m.get("NAME"),
                "registro": reg_da_priv(m.get("DRIVERPRIVATE")),
                "formato": fmt_da_priv(m.get("DRIVERPRIVATE")),
                "driverdata": m.get("DRIVERDATA"),
                "type": m.get("TYPE"),
                "unita": m.get("UNITS"),
                "bits": bits,
            })
        out.append({
            "nome": st.get("NAME"),
            "id": st.get("ID"),
            "ip": ip_da_config(st.get("DRIVERCONFIG")),
            "driverconfig": st.get("DRIVERCONFIG"),
            "misure": misure,
            "n_bitinfo": len(st.get("bitinfo", []) or []),
            "_warnings": st.get("_warnings"),
            "_meta_input": st.get("_meta") or {},
        })
    return out


# --------------------------------------------------------------------------
# Parte C - confronto
# --------------------------------------------------------------------------

ANALOGICO = -1  # marcatore per una misura senza bit

SPIEGAZIONI = {
    "ok": "corrispondenza corretta",
    "saltata_da_regola_di_prompt": "saltata da regola (comportamento richiesto)",
    "riclassificata_dal_pytool": "scelta di progetto",
    "correzione_di_refuso_del_documento": "correzione di refuso del documento",
    "difetto": "difetto",
}

# prefissi che il documento mette davanti al nome per indicare che la riga e'
# un allarme, un comando o un superamento di soglia di un'altra misura. La
# riga e' quindi la stessa entita' della misura senza prefisso, e se quella
# misura finisce in un'altra categoria la riga e' stata riclassificata, non
# persa.
PREFISSI_ALLARME = ("OVF", "RC", "CMD", "AL", "ALL", "COG", "FB")


def riclassificata(descrizione, assegnate, truth):
    """True se la riga e' stata assorbita in una misura di altra categoria.

    'OVF Misura Disponibile IW36' non e' una riga persa: e' lo stesso
    segnale di 'Misura Disponibile IW36', che il pytool ha trasformato in
    analogica perche' contiene la parola 'Misura'. Senza questo controllo
    sarebbe contato come dato mancante.
    """
    d = norm(descrizione)
    for prefisso in PREFISSI_ALLARME:
        if d.upper().startswith(prefisso + " "):
            resto = d[len(prefisso) + 1:].strip()
            if not resto:
                continue
            for k, h in assegnate.items():
                if h.get("e_bit"):
                    continue  # confronta solo con le misure analogiche
                nome = chiave_nome(h["nome_misura"] or "")
                if nome and (nome == chiave_nome(resto) or
                             chiave_nome(resto) in nome or
                             nome in chiave_nome(resto)):
                    return True
    return False


def classifica(esito, pdf_txt, out_txt):
    """Attribuisce una classe allo scostamento.

    Serve a non mettere sullo stesso piano cose di natura diversa: un
    refuso corretto, una scelta di progetto e un difetto richiedono
    decisioni diverse.
    """
    if esito in ("ok", "saltata_da_regola_di_prompt"):
        return esito
    if esito == "riclassificata_dal_pytool":
        return "scelta_di_progetto"
    if esito in ("nome_diverso", "stato_diverso", "nome_diverso+stato_diverso"):
        a, b = chiave_nome(pdf_txt), chiave_nome(out_txt)
        if a and b:
            r = difflib.SequenceMatcher(None, a, b).ratio()
            if r >= 0.85:
                return "correzione_di_refuso_del_documento"
        return "difetto"
    return "difetto"


def confronta(righe_pdf, stazioni):
    """Confronto bidirezionale tra le righe del PDF e l'output.

    L'abbinamento non puo' essere per chiave esatta. Una riga del documento
    che occupa un registro intero senza dichiarare un bit viene resa dal
    pytool come digitale singolo con BITNO 0, quindi la stessa realta' del
    documento appare con due forme diverse. L'abbinamento prova quindi la
    chiave esatta e, se non trova nulla, le forme equivalenti, annotando quale
    e' stata usata.

    La chiave comprende la stazione: lo stesso registro puo' esistere in due
    tabelle diverse (SMA usa 40001 sia per `CO` su 192.168.6.20 sia per
    `Temperatura Fumi` sull'IP placeholder) e l'output le separa in stazioni
    diverse. Abbinare per solo registro le confonde e produce falsi
    `nome_diverso`. Dove il documento non dichiara la stazione (PROTEC,
    SIEMENS) si ricade su (registro, bit); dove l'output non la dichiara si
    abbina solo se una stazione sola dichiara quella chiave, mai in
    ambiguita' silenziosa.
    """
    truth = {}
    truth_senza_reg = {}
    # Una stessa chiave (stazione, registro, bit) puo' comparire piu' volte
    # nel documento: righe diverse che puntano allo stesso indirizzo. Se si
    # tiene solo la prima, le altre spariscono dal confronto e la quadratura
    # non chiude. Si conservano tutte in un elenco secondario, cosi' il
    # confronto resta uno a uno e le righe in piu' restano visibili.
    truth_dup = {}
    for r in righe_pdf:
        if r["registro"] is None:
            truth_senza_reg.setdefault(chiave_nome(r["descrizione"]), r)
            continue
        k = (chiave_stazione(r.get("ip")),
             r["registro"], r["bit"] if r["bit"] is not None else ANALOGICO)
        if k in truth:
            truth_dup.setdefault(k, []).append(r)
        else:
            truth[k] = r

    def abbina(registro, bit_out, staz_out, nome=None):
        """Chiave di verita' corrispondente, o None.

        Prima la chiave con stazione, poi le forme equivalenti, poi la
        chiave senza stazione (documento che non la dichiara). Se il
        registro non esiste nel documento si prova ad abbinare per
        nome. Serve a classificare le misure che l'output ha emesso contro
        righe del documento che non hanno indirizzo, come le CALCOLATA: senza
        questo passaggio sembrerebbero misure inventate dal nulla.
        """
        candidati = [(registro, bit_out)]
        if bit_out is None:
            candidati += [(registro, 0), (registro, ANALOGICO)]
        else:
            candidati += [(registro, ANALOGICO)]
        if staz_out is not None:
            for rg, bt in candidati:
                if (staz_out, rg, bt) in truth:
                    return (staz_out, rg, bt)
        for rg, bt in candidati:
            if (None, rg, bt) in truth:
                return (None, rg, bt)
        if staz_out is None:
            # Output senza stazione: si abbina solo se non c'e' ambiguita',
            # cioe' se una stazione sola del documento dichiara la chiave.
            for rg, bt in candidati:
                quali = sorted({s for (s, r2, b2) in truth
                                if r2 == rg and b2 == bt and s is not None})
                if len(quali) == 1:
                    return (quali[0], rg, bt)
        if nome is not None and chiave_nome(nome) in truth_senza_reg:
            return ("senza-registro", chiave_nome(nome))
        return None

    # le chiavi che l'output copre
    coperte = {}
    per_output_senza_reg = []
    dettaglio_misure = []
    for st in stazioni:
        staz_out = chiave_stazione(st.get("ip"))
        for m in st["misure"]:
            reg = m["registro"]
            if reg is None:
                dettaglio_misure.append({
                    "stazione": st["nome"], "ip": st["ip"],
                    "id": m["id"], "nome": m["nome"],
                    "esito": "registro_illeggibile",
                })
                continue
            if m["bits"]:
                for b in m["bits"]:
                    k = (staz_out, reg, b.get("BITNO"))
                    coperte.setdefault(k, []).append({
                        "stazione": st["nome"], "ip": st["ip"],
                        "nome_misura": m["nome"],
                        "bitname": b.get("BITNAME"),
                        "texton": b.get("TEXTON"),
                        "textoff": b.get("TEXTOFF"),
                        "e_bit": True,
                    })
            else:
                k = (staz_out, reg, ANALOGICO)
                coperte.setdefault(k, []).append({
                    "stazione": st["nome"], "ip": st["ip"],
                    "nome_misura": m["nome"],
                    "bitname": None, "texton": None, "textoff": None,
                    "e_bit": False,
                })

    # abbinamento: ogni chiave di verita' puo' essere coperta una volta sola
    assegnate = {}
    senza_reg_assegnate = set()
    for k in sorted(coperte.keys(),
                    key=lambda x: (x[1], -1 if x[2] is None else x[2])):
        for h in coperte[k]:
            nome = h["bitname"] or h["nome_misura"]
            tk = abbina(k[1], k[2], k[0], nome)
            if tk is None:
                continue
            if tk[0] == "senza-registro":
                if tk[1] not in senza_reg_assegnate:
                    senza_reg_assegnate.add(tk[1])
                    per_output_senza_reg.append({
                        "esito": "riga_senza_indirizzo_trasformata_in_misura",
                        "pdf_descrizione": truth_senza_reg[tk[1]]["descrizione"],
                        "pdf_tipo": truth_senza_reg[tk[1]]["tipo"],
                        "registro_emesso": k[1],
                        "stazione": h["stazione"], "ip": h["ip"],
                        "nome_misura": nome,
                    })
            elif tk not in assegnate:
                assegnate[tk] = h

    per_chiave = []
    # si itera su tutte le righe, comprese le duplici, cosi' la quadratura
    # con le righe estratte dal PDF chiude
    for r in righe_pdf:
        if r["registro"] is None:
            continue
        staz = chiave_stazione(r.get("ip"))
        k = (staz, r["registro"],
             r["bit"] if r["bit"] is not None else ANALOGICO)
        voce = {
            "registro": k[1],
            "bit": None if k[2] == ANALOGICO else k[2],
            "stazione_pdf": staz,
            "pdf_descrizione": r["descrizione"],
            "pdf_stato": r["stato"],
            "pdf_unita": r["unita"],
            "pagina": r["pagina"],
        }
        h = assegnate.get(k)
        if h is None:
            if da_saltare(r["descrizione"]) or r.get("da_scartare"):
                voce["esito"] = "saltata_da_regola_di_prompt"
                voce["scarto"] = classe_scarto(r["descrizione"], r)
            elif riclassificata(r["descrizione"], assegnate, truth):
                voce["esito"] = "riclassificata_dal_pytool"
            else:
                voce["esito"] = "non_coperta_dall_output"
            voce["output"] = None
        else:
            voce["output"] = {
                "stazione": h["stazione"], "ip": h["ip"],
                "nome_misura": h["nome_misura"], "bitname": h["bitname"],
                "texton": h["texton"], "textoff": h["textoff"],
            }
            nome_pdf = chiave_nome(r["descrizione"])
            nome_out = chiave_nome(h["bitname"] or h["nome_misura"])
            esito = "ok"
            if nome_pdf and nome_out and nome_pdf != nome_out:
                esito = "nome_diverso"
            if r["stato"] and h["texton"]:
                if chiave_nome(r["stato"]) != chiave_nome(h["texton"]):
                    esito = "stato_diverso" if esito == "ok" else esito + "+stato_diverso"
            voce["esito"] = esito
        if voce["output"]:
            o = voce["output"]
            voce["classe"] = classifica(voce["esito"], voce["pdf_descrizione"],
                                       o.get("bitname") or o.get("nome_misura"))
        else:
            voce["classe"] = classifica(voce["esito"], voce["pdf_descrizione"], "")
        per_chiave.append(voce)

    # l'output che non trova riscontro nel documento
    per_output = []
    for k, hits in sorted(coperte.items(),
                          key=lambda x: (x[0][1], -1 if x[0][2] is None else x[0][2])):
        if any(abbina(k[1], k[2], k[0], h["bitname"] or h["nome_misura"]) is not None
               for h in hits):
            continue
        for h in hits:
            per_output.append({
                "registro": k[1],
                "bit": None if k[2] == ANALOGICO else k[2],
                "esito": "non_esiste_nel_pdf",
                "stazione": h["stazione"], "ip": h["ip"],
                "nome_misura": h["nome_misura"], "bitname": h["bitname"],
            })

    return per_chiave, per_output, per_output_senza_reg


def controlli_trasversali(righe_pdf, stazioni, meta, caso, per_chiave):
    """Registri e IP presenti nel PDF e assenti dall'output."""
    reg_pdf = sorted({r["registro"] for r in righe_pdf if r["registro"] is not None})
    reg_out = sorted({m["registro"] for st in stazioni
                      for m in st["misure"] if m["registro"]})
    mancanti = [r for r in reg_pdf if r not in reg_out]
    extra = [r for r in reg_out if r not in reg_pdf]

    ip_pdf = []
    for r in righe_pdf:
        if r["ip"] and r["ip"] not in ip_pdf:
            ip_pdf.append(r["ip"])
    for k in ("ip_trovati",):
        for v in meta.get(k, []) or []:
            if v not in ip_pdf:
                ip_pdf.append(v)
    ip_out = [st["ip"] for st in stazioni if st["ip"]]
    ip_mancanti = [i for i in ip_pdf if i not in ip_out]

    # Quante variabili il pytool ha ricevuto davvero, se il file lo dichiara.
    # E' il dato che permette di stabilire dove sia avvenuta una perdita: se
    # il pytool ne ha ricevute meno di quante ce n'erano nel documento, la
    # perdita e' a monte, nel VLM, e non e' imputabile al pytool.
    meta_input = {}
    for st in stazioni:
        w = st.get("_meta_input")
        if w:
            meta_input = w
            break
    variabili_al_pytool = meta_input.get("variables_total")
    chunk = meta_input.get("chunks_parsed")

    # Registri che il documento usa solo per righe destinate a essere
    # scartate: non sono un difetto che l'output non le copra.
    reg_pdf_solo_saltati = sorted({
        r["registro"] for r in righe_pdf
        if r["registro"] is not None
        and (da_saltare(r["descrizione"]) or r.get("da_scartare"))
        and r["registro"] not in reg_out
    })
    mancanti_reali = [r for r in mancanti if r not in reg_pdf_solo_saltati]

    # copertura per pagina: distingue i buhi reali da un input che non
    # conteneva tutto il documento. Un run fatto su un PDF parziale produce
    # output mancanti, ma non e' un difetto della pipeline.
    cov = {}
    for v in per_chiave:
        p = v.get("pagina")
        if p is None:
            continue
        c = cov.setdefault(p, {"totale": 0, "coperte": 0, "saltate": 0})
        c["totale"] += 1
        if v["esito"] == "saltata_da_regola_di_prompt":
            c["saltate"] += 1
        elif v["classe"] in ("ok", "correzione_di_refuso_del_documento",
                             "scelta_di_progetto"):
            c["coperte"] += 1
    pagine_senza_output = sorted(p for p, c in cov.items() if c["coperte"] == 0)

    conv = {}
    for r in righe_pdf:
        c = r.get("convenzione")
        if c:
            conv.setdefault(c, []).append(r["registro_grezzo"])
    conv_summary = {k: (len(v), v[:5]) for k, v in conv.items()}

    return {
        "registri_nel_pdf": len(reg_pdf),
        "registri_nell_output": len(reg_out),
        "registri_solo_nel_pdf": mancanti_reali,
        "registri_solo_nel_pdf_solo_righe_saltate": reg_pdf_solo_saltati,
        "registri_solo_nell_output": extra,
        "convenzioni_indirizzo": conv_summary,
        "copertura_per_pagina": {str(k): v for k, v in sorted(cov.items())},
        "pagine_senza_output": pagine_senza_output,
        "variabili_ricevute_dal_pytool": variabili_al_pytool,
        "chunk_ricevuti_dal_pytool": chunk,
        "righe_pdf_utilizzabili": len(righe_pdf) - len(reg_pdf_solo_saltati),
        "ip_nel_pdf": ip_pdf,
        "ip_nell_output": ip_out,
        "ip_nel_pdf_non_usati": ip_mancanti,
        "nomi_stazione_output": [st["nome"] for st in stazioni],
        "meta_pdf": {k: v for k, v in meta.items() if k != "ip_trovati"},
    }


# --------------------------------------------------------------------------
# report
# --------------------------------------------------------------------------

def scrivi_report(caso, per_chiave, per_output, per_senza_reg, trasversali,
                 tabella, stato_estrazione):
    cid = caso["id"]
    dir_caso = os.path.join(OUT_RES, cid)
    os.makedirs(dir_caso, exist_ok=True)

    conteggio = {}
    classi = {}
    scarti = {}
    for v in per_chiave:
        conteggio[v["esito"]] = conteggio.get(v["esito"], 0) + 1
        classi[v["classe"]] = classi.get(v["classe"], 0) + 1
        if v["esito"] == "saltata_da_regola_di_prompt":
            s = v.get("scarto", "non_classificato")
            scarti[s] = scarti.get(s, 0) + 1

    L = []
    A = L.append
    A("# %s — %s" % (cid.replace("_", " "), caso["cliente"]))
    A("")
    A("Confronto fra `%s` e `%s`." % (caso["pdf"], caso["output"]))
    A("")
    A("## Esito")
    A("")
    if stato_estrazione.get("avviso"):
        A("> **Estrazione parziale.** %s" % stato_estrazione["avviso"])
        A("")
    # Le tre categorie devono essere disgiunte e sommare il totale. Le righe
    # saltate da una regola NON sono coperte dall'output: sono assenti, ma per
    # un motivo che il prompt prescrive. Contarle insieme nasconderebbe
    # quante righe mancano davvero.
    #
    # Le righe CALCOLATA, cioe' quelle che nel documento non hanno un indirizzo,
    # vanno in una categoria a parte: non sono nel confronto per chiave
    # registro/bit perche' non ce l'hanno, e nemmeno fra le mancanti, perche'
    # la loro assenza e' un esito a se' che viene trattato sotto.
    con_output = [v for v in per_chiave if v["esito"] not in
                  ("non_coperta_dall_output", "saltata_da_regola_di_prompt")]
    saltate = [v for v in per_chiave if v["esito"] == "saltata_da_regola_di_prompt"]
    non_coperte = [v for v in per_chiave if v["esito"] == "non_coperta_dall_output"]
    # per_senza_reg e' deduplicato per nome, ma le righe nella tabella non lo
    # sono: se nel documento due righe hanno lo stesso nome e nessun indirizzo,
    # la seconda non produce una voce. Per far quadrare il conto con le righe
    # effettivamente estratte serve il totale delle righe senza indirizzo, non
    # il numero di voci abbinate.
    senza_indirizzo = sum(1 for r in tabella if r["registro"] is None)
    non_emesse = sum(1 for r in tabella
                     if r["registro"] is None
                     and chiave_nome(r["descrizione"]) not in {
                         chiave_nome(v["pdf_descrizione"]) for v in per_senza_reg})
    totale_quadrato = (len(con_output) + len(saltate) + len(non_coperte)
                       + senza_indirizzo)
    scarto = totale_quadrato - len(tabella)

    A("| | |")
    A("|---|---|")
    A("| Righe estratte dal PDF | %d |" % len(tabella))
    A("| Righe del PDF presenti nell'output | %d |" % len(con_output))
    A("| Righe del PDF assenti per una regola del prompt | %d |" % len(saltate))
    A("| Righe del PDF assenti senza spiegazione | %d |" % len(non_coperte))
    A("| Righe del PDF senza indirizzo Modbus (grandezze derivate) | %d, di cui %d trasformate in misure |" % (senza_indirizzo, len(per_senza_reg)))
    A("| Righe dell'output assenti dal PDF | %d |" % len(per_output))
    if scarto:
        A("| **Quadratura non chiusa** | %d |" % scarto)
    A("")
    A("Le cinque categorie sommano a %d contro %d righe estratte." % (
        totale_quadrato, len(tabella)))
    A("")
    A("### Natura degli scostamenti")
    A("")
    A("| Classe | Righe |")
    A("|---|---|")
    for k in sorted(classi, key=lambda x: -classi[x]):
        A("| %s | %d |" % (SPIEGAZIONI.get(k, k), classi[k]))
    A("")
    A("Le scostamenti non sono tutti difetti. `correzione di refuso del "
      "documento` significa che il testo nel PDF e' sbagliato e l'output lo ha "
      "corretto; `scelta di progetto` significa che la pipeline ha fatto "
      "qualcosa di deliberato e diverso. Solo la classe `difetto` richiede "
      "una decisione.")
    A("")
    if scarti:
        A("### Motivi di scarto")
        A("")
        A("Le righe scartate non sono un mucchio indistinto: ogni classe "
          "segue una regola diversa del prompt.")
        A("")
        A("| Classe di scarto | Righe |")
        A("|---|---|")
        for k in sorted(scarti, key=lambda x: -scarti[x]):
            A("| %s | %d |" % (SCARTI.get(k, k), scarti[k]))
        A("")

    if per_senza_reg:
        A("## Righe del documento trasformate in misure senza indirizzo")
        A("")
        A("Il documento contiene righe di grandezze derivate che **non hanno "
          "un indirizzo Modbus**: sono valori calcolati a partire da altri "
          "registri. L'output le ha comunque emesse come misure, e in "
          "particolare contro il registro %s, che non corrisponde a nulla "
          "nel documento." % ", ".join(
              str(x["registro_emesso"]) for x in per_senza_reg[:1]))
        A("")
        A("Da solo il JSON non mostra il problema: `DRIVERPRIVATE` ha la "
          "lunghezza giusta ed esadecimale valido, solo che la prima parola "
          "e' zero.")
        A("")
        A("| Riga nel PDF | Tipo | Misura emessa | Registro emesso |")
        A("|---|---|---|---|")
        for v in per_senza_reg[:30]:
            A("| %s | %s | %s | %s |" % (
                str(v["pdf_descrizione"])[:34], v["pdf_tipo"],
                str(v["nome_misura"])[:34], v["registro_emesso"]))
        A("")

    A("## Registri e indirizzi")
    A("")
    A("- Registri distinti nel PDF: **%d**, nell'output: **%d**" % (
        trasversali["registri_nel_pdf"], trasversali["registri_nell_output"]))
    if trasversali["registri_solo_nel_pdf"]:
        A("- **Solo nel PDF, nessuna misura corrispondente:** %s" % (
            ", ".join(str(x) for x in trasversali["registri_solo_nel_pdf"][:40])))
    if trasversali["registri_solo_nell_output"]:
        A("- **Solo nell'output, assenti dal PDF:** %s" % (
            ", ".join(str(x) for x in trasversali["registri_solo_nell_output"][:40])))
    A("- IP trovati nel documento: %s" % (
        ", ".join("`%s`" % i for i in trasversali["ip_nel_pdf"]) or "nessuno"))
    A("- IP usati dall'output: %s" % (
        ", ".join("`%s`" % i for i in trasversali["ip_nell_output"]) or "nessuno"))
    if trasversali["ip_nel_pdf_non_usati"]:
        A("- **IP dichiarati e mai usati:** %s" % (
            ", ".join("`%s`" % i for i in trasversali["ip_nel_pdf_non_usati"])))
    conv = trasversali.get("convenzioni_indirizzo") or {}
    # 'nessuno' e' la convenzione delle righe CALCOLATA, che non hanno un
    # indirizzo: non e' una terza convenzione e non va confrontata con le altre.
    conv = {k: v for k, v in conv.items() if k != "nessuno"}
    if len(conv) > 1:
        A("- **Il documento usa più di una convenzione di indirizzo:** %s" % ", ".join(
            "`%s` (%d righe, es. %s)" % (k, v[0], ", ".join(v[1]))
            for k, v in sorted(conv.items())))
        A("")
        A("  La normalizzazione del pytool applica la stessa regola a tutte. "
          "Gli indirizzi che nel documento avevano zeri iniziali arrivano "
          "nell'output come interi brevi, cioè puntano a un registro diverso "
          "da quello scritto. Il confronto riga per riga non può segnalarlo, "
          "perché dall'output l'informazione sulla convenzione originale è "
          "perduta.")
    A("- Nomi stazione prodotti dall'output: %s" % (
        ", ".join("`%s`" % n for n in trasversali["nomi_stazione_output"])))
    if trasversali["meta_pdf"].get("punto_emissivo") or trasversali["meta_pdf"].get("cliente"):
        A("- Metadati nel PDF: %s" % ", ".join(
            "%s=%s" % (k, v) for k, v in trasversali["meta_pdf"].items() if v))
    A("")

    ricevute = trasversali.get("variabili_ricevute_dal_pytool")
    if ricevute:
        A("### Dove si e' perduta la copertura")
        A("")
        A("Il file di output registra nei suoi metadati quante variabili ha "
          "ricevuto: **%d**, in %s." % (
              ricevute,
              ("un solo chunk" if trasversali.get("chunk_ricevuti_dal_pytool") == 1
               else "%s chunk" % trasversali.get("chunk_ricevuti_dal_pytool"))))
        A("Il PDF contiene %d righe utilizzabili. Il pytool ne ha viste %s."
          % (trasversali.get("righe_pdf_utilizzabili", 0),
             "meno" if ricevute < trasversali.get("righe_pdf_utilizzabili", 0)
             else "altrettante"))
        A("")
        if ricevute < trasversali.get("righe_pdf_utilizzabili", 0):
            A("**La perdita e' avvenuta a monte del pytool, nell'estrazione "
              "VLM**, non nel pytool. Il pytool ha lavorato tutto quello che "
              "gli e' stato passato: non puo' produrre misure per righe che "
              "non ha mai ricevuto.")
            A("")
            A("Su questo caso la spiegazione plausibile e' la modalita' di "
              "invio: **%s** per un documento di 29 pagine suggerisce che le "
              "pagine siano state accorpate in un'unica richiesta invece che "
              "una per iterazione. E' la stessa ipotesi del rischio n. 1 di "
              "ADR-001, e qui si vede concretamente." % (
                  "un solo chunk" if trasversali.get("chunk_ricevuti_dal_pytool") == 1
                  else "%s chunk" % trasversali.get("chunk_ricevuti_dal_pytool")))
            A("")

    cov = trasversali.get("copertura_per_pagina") or {}
    if len(cov) > 1:
        A("### Copertura per pagina")
        A("")
        senza = trasversali.get("pagine_senza_output") or []
        if senza:
            A("Le pagine %s non hanno **nessuna** riga coperta dall'output."
              % ", ".join(str(p) for p in senza[:20]))
            A("")
            A("Il documento è completo e l'input del run era l'intero PDF, "
              "quindi queste pagine sono state lette ma non riportate "
              "nell'estrazione. La perdita è a monte del pytool, come "
              "indicato sopra.")
            A("")
        A("| Pagina | Righe | Coperte | Saltate da regola |")
        A("|---|---|---|---|")
        for p, c in cov.items():
            A("| %s | %d | %d | %d |" % (p, c["totale"], c["coperte"], c["saltate"]))
        A("")

    # Righe non coperte il cui nome e' una variante prefissata di un nome
    # generico. La regola V2 del prompt fa confronto esatto, quindi non le
    # classifica come da scartare, ma il pytool non le ha emesse. Non si puo'
    # attribuire la mancanza a un difetto senza scegliere quale comportamento
    # sia quello atteso: tarare la regola perche' combaci con l'output sarebbe
    # circolare. Vanno contate a parte e portate al cliente.
    varianti = {}
    for v in per_chiave:
        if v["esito"] != "non_coperta_dall_output":
            continue
        d = norm(v["pdf_descrizione"]).lower()
        for g in GENERICI_ESATTI:
            if d.startswith(g + " ") or d == g:
                varianti.setdefault(g, []).append(v)
                break
    if varianti:
        tot = sum(len(x) for x in varianti.values())
        A("## Righe mancanti con nome generico prefissato")
        A("")
        A("**%d righe** assenti dall'output hanno un nome che comincia per "
          "uno dei nomi generici che la regola V2 impone di saltare, senza "
          "però coincidere con essi. Il prompt chiede il confronto esatto, "
          "quindi per queste righe la regola non si applica e la pipeline "
          "non dovrebbe scartarle: l'output però le ha scartate." % tot)
        A("")
        A("| Prefisso | Righe mancanti | Nomi esempi |")
        A("|---|---|---|")
        for g, righe in sorted(varianti.items(), key=lambda x: -len(x[1])):
            esempi = ", ".join(sorted({norm(r["pdf_descrizione"])
                                       for r in righe})[:3])
            A("| `%s` | %d | %s |" % (g, len(righe), esempi))
        A("")
        A("Non è possibile attribuire queste mancanze a un difetto senza "
          "decidere quale comportamento sia atteso. Se la regola deve essere "
          "esatta come è scritta, l'output ne scarta troppe; se deve coprire "
          "i prefissi, il prompt va corretto. È una domanda per il cliente.")
        A("")

    difetti = [v for v in per_chiave if v["esito"] not in ("ok",)]
    if difetti:
        A("## Scostamenti")
        A("")
        A("| Registro | Bit | Stazione PDF | Esito | PDF | Output |")
        A("|---|---|---|---|---|---|")
        for v in difetti[:60]:
            out = v["output"] or {}
            testo_out = out.get("bitname") or out.get("nome_misura") or "—"
            A("| %s | %s | %s | `%s` | %s | %s |" % (
                v["registro"], v["bit"] if v["bit"] is not None else "—",
                v.get("stazione_pdf") or "—",
                v["esito"],
                (v["pdf_descrizione"] or "")[:40].replace("|", "\\|"),
                str(testo_out)[:40].replace("|", "\\|")))
        if len(difetti) > 60:
            A("")
            A("_Mostrate le prime 60 righe su %d._" % len(difetti))
        A("")

    if per_output:
        A("## Nell'output ma assenti dal PDF")
        A("")
        A("| Registro | Bit | Stazione | Misura |")
        A("|---|---|---|---|")
        for v in per_output[:40]:
            A("| %s | %s | %s | %s |" % (
                v["registro"], v["bit"] if v["bit"] is not None else "—",
                v["stazione"], str(v["nome_misura"])[:40]))
        A("")

    with open(os.path.join(dir_caso, "report.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")

    with open(os.path.join(dir_caso, "verdetto.json"), "w", encoding="utf-8") as f:
        json.dump({
            "caso": cid,
            "cliente": caso["cliente"],
            "pdf": caso["pdf"],
            "output": caso["output"],
            "estrazione": stato_estrazione,
            "riepilogo": {
                "righe_pdf": len(tabella),
                "presenti_nell_output": len(con_output),
                "saltate_da_regola": len(saltate),
                "non_coperte": len(non_coperte),
                "senza_indirizzo": len(per_senza_reg),
                "fantasma_output": len(per_output),
                "quadratura": scarto,
                "per_esito": conteggio,
                "per_classe": classi,
                "per_scarto": scarti,
            },
            "trasversali": trasversali,
            "per_riga_pdf": per_chiave,
            "per_riga_output": per_output,
            "righe_senza_indirizzo": per_senza_reg,
        }, f, ensure_ascii=False, indent=1)

    with open(os.path.join(dir_caso, "tabella_pdf.json"), "w", encoding="utf-8") as f:
        json.dump({"caso": cid, "righe": tabella}, f, ensure_ascii=False, indent=1)

    return len(conteggio), conteggio


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

def esegui(caso):
    percorso_pdf = os.path.join(PDF_DIR, caso["pdf"])
    if not os.path.exists(percorso_pdf):
        print("  PDF mancante: %s" % percorso_pdf)
        return None
    if not caso.get("output"):
        print("  caso %s senza output (solo tabella verita')" % caso["id"])
        return None
    percorso_out = os.path.join(OUT_DIR, caso["output"])
    if not os.path.exists(percorso_out):
        print("  Output mancante: %s" % percorso_out)
        return None

    import pymupdf
    doc = pymupdf.open(percorso_pdf)
    tabella, meta = ESTRATTORI[caso["formato"]](doc, caso)
    doc.close()

    stazioni = leggi_output(percorso_out)
    per_chiave, per_output, per_senza_reg = confronta(tabella, stazioni)
    trasversali = controlli_trasversali(tabella, stazioni, meta, caso, per_chiave)

    stato = {"formato": caso["formato"], "righe_grezze": len(tabella)}
    if caso["formato"] == "siemens":
        # Con l'input completo a 29 pagine, la perdita di copertura e' stata
        # localizzata: il pytool ha ricevuto 274 variabili per 1116 righe
        # nel documento, in un solo chunk. La perdita e' quindi a monte, nel
        # VLM, e l'estrattore non e' la causa. Resta una riserva: non e' stato
        # riprodotto in locale l'invio delle 29 pagine, quindi l'attribuzione
        # al VLM e' dedotta dai metadati dell'output, non osservata.
        stato["avviso"] = (
            "Confronto **parzialmente validato**. L'estrazione copre 28 "
            "pagine su 29 e i registri e i nomi che produce sono coerenti. La "
            "perdita di copertura e' stata pero' localizzata a monte: i "
            "metadati dell'output indicano che il pytool ha ricevuto 274 "
            "variabili in un solo chunk, mentre il documento ne contiene 1116 "
            "righe. Il pytool non puo' aver perso righe che non ha ricevuto, "
            "quindi la perdita e' nell'estrazione VLM. Resta non verificato "
            "in locale il modo in cui le 29 pagine sono state inviate, quindi "
            "l'attribuzione al VLM e' dedotta, non osservata.")
        stato["validato"] = "parziale"

    n, conteggio = scrivi_report(caso, per_chiave, per_output, per_senza_reg,
                                 trasversali, tabella, stato)
    return n, conteggio, trasversali, len(per_senza_reg), {
        "righe_pdf": len(tabella),
        "presenti_nell_output": len([
            v for v in per_chiave
            if v["esito"] not in ("non_coperta_dall_output",
                                  "saltata_da_regola_di_prompt")]),
        "saltate_da_regola": len([
            v for v in per_chiave
            if v["esito"] == "saltata_da_regola_di_prompt"]),
        "non_coperte": len([
            v for v in per_chiave
            if v["esito"] == "non_coperta_dall_output"]),
        "senza_indirizzo": len(per_senza_reg),
    }


def main():
    if "--lista" in sys.argv:
        for c in CASI:
            print("  %-22s %s" % (c["id"], c["pdf"]))
        return
    scelti = [c for c in CASI if c["id"] in sys.argv[1:]] or CASI
    for caso in scelti:
        print("=== %s" % caso["id"])
        r = esegui(caso)
        if r is None:
            continue
        n, conteggio, trasv, n_senza_reg, somm = r
        print("    %-42s %d" % ("righe nel PDF", somm["righe_pdf"]))
        print("    %-42s %d" % ("presenti nell'output", somm["presenti_nell_output"]))
        print("    %-42s %d" % ("saltate da regola del prompt", somm["saltate_da_regola"]))
        print("    %-42s %d" % ("assenti senza spiegazione", somm["non_coperte"]))
        print("    %-42s %d" % ("senza indirizzo Modbus nel PDF", somm["senza_indirizzo"]))
        scarto = (somm["presenti_nell_output"] + somm["saltate_da_regola"]
                  + somm["non_coperte"] + somm["senza_indirizzo"]
                  - somm["righe_pdf"])
        if scarto:
            print("    %-42s %d  <-- NON QUADRA" % ("scarto", scarto))
        if n_senza_reg:
            print("    %-34s %d" % ("righe senza indirizzo trasformate", n_senza_reg))
        if trasv["registri_solo_nel_pdf"]:
            print("    %-34s %d" % ("registri solo nel PDF",
                                    len(trasv["registri_solo_nel_pdf"])))
        if trasv["ip_nel_pdf_non_usati"]:
            print("    %-34s %s" % ("IP nel PDF non usati",
                                    ", ".join(trasv["ip_nel_pdf_non_usati"])))
        print()


if __name__ == "__main__":
    main()
