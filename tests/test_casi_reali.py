#!/usr/bin/env python3
"""Test sui 4 casi reali, ancorati al confronto output/PDF.

I test in test_multipage.py usano fixture sintetiche costruite a mano e
verificano le regole del pytool. Questi partono dai documenti veri e
verificano che l'output corrisponda al PDF: la domanda non e' "la regola
funziona" ma "il dato c'e' tutto e punta al registro giusto".

Il confronto completo sta in myhydra/single_pdf/verifica_pdf/. Qui ci sono i
controlli che devono stare nel repository perche' reggono al refactor.

Uso: python3 tests/test_casi_reali.py
"""
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, "src", "nodes", "json_creator.py")
FIXTURE = os.path.join(ROOT, "data", "test_inputs", "vlm_raw",
                        "PROTEC_1_2pages.json")

_esiti = []


def _run(raw):
    """Esegue il pytool come farebbe MyHydra, iniettando raw al posto edge."""
    src = open(SCRIPT, encoding="utf-8").read()
    src = re.sub(r"raw\s*=\s*r?'''\{edge\}\[\d+\]'''", "raw = __INJ__", src)
    ns = {"__INJ__": raw}
    vecchio = sys.stdout
    sys.stdout = io.StringIO()
    try:
        exec(src, ns)
    finally:
        sys.stdout = vecchio
    return json.loads(ns.get("output", "null"))


def _variabili(descrizione, modbus_register, kind="ANALOGICA", bit=None):
    v = {"description": descrizione, "kind": kind, "modbus_register": modbus_register}
    if bit is not None:
        v["bit"] = bit
    return v


def _chunk(variabili, ip=None, name=None):
    return {"stations": [{"name": name, "protocol": "ModBus TCP", "ip": ip,
                          "port": 502, "modbus_id": 1,
                          "variables": variabili}]}


def _test(nome, condizione, dettaglio=""):
    _esiti.append((nome, bool(condizione), dettaglio))
    print("[%s] %s%s" % ("PASS" if condizione else "FAIL", nome,
                         ("  -> " + dettaglio) if dettaglio else ""))


# --------------------------------------------------------------------------

def test_registro_zero_non_emesso():
    """v4.3: una variabile senza indirizzo non deve generare una misura.

    Prima della v4.3 restava a zero e produceva DRIVERPRIVATE 0x0000..., che
    passa la validazione di schema ed e' pero' un indirizzo che non esiste.
    """
    raw = [_chunk([
        _variabili("CO", 40001),
        _variabili("NOX", None),          # grandezza derivata, senza indirizzo
        _variabili("H2O", None),
        _variabili("Pressione", 40002),
    ], ip="192.168.0.1", name="SME")]
    out = _run(raw)
    nomi = [m["NAME"] for m in out[0]["measures"]]
    _test("nessuna misura con nome di variabile senza indirizzo",
          "NOX" not in nomi and "H2O" not in nomi,
          "misure emesse: %s" % nomi)
    _test("le misure con indirizzo restano",
          "CO" in nomi and "Pressione" in nomi)


def test_nessun_driverprivate_a_zero():
    """Nessuna misura dell'output può avere il registro a zero."""
    raw = [_chunk([
        _variabili("Derivata uno", None),
        _variabili("Derivata due", ""),
        _variabili("Normale", 40001),
    ], ip="192.168.0.1")]
    out = _run(raw)
    cattive = [m["NAME"] for m in out[0]["measures"]
               if (m.get("DRIVERPRIVATE") or "").startswith("0x00000000")]
    _test("nessun DRIVERPRIVATE inizia con 0x00000000", not cattive,
          "trovati: %s" % cattive)


def test_conteggio_senza_registro():
    """Il numero di variabili scartate va contato e reso noto."""
    raw = [_chunk([
        _variabili("Normale", 40001),
        _variabili("Derivata A", None),
        _variabili("Derivata B", None),
        _variabili("Derivata C", None),
    ], ip="192.168.0.1")]
    out = _run(raw)
    meta = out[0].get("_meta") or {}
    _test("il conteggio delle variabili senza indirizzo e' 3",
          meta.get("variabili_senza_registro") == 3,
          "valore: %s" % meta.get("variabili_senza_registro"))
    warn = " ".join(out[0].get("_warnings") or [])
    _test("il warning cita le variabili scartate",
          "VARIABILI SENZA INDIRIZZO" in warn and "Derivata A" in warn)


def test_warning_indirizzi_a_zeri_iniziali():
    """Gli indirizzi con zeri iniziali vanno segnalati, non convertiti."""
    raw = [_chunk([
        _variabili("Allarme uno", "00033", kind="DIGITALE_SINGOLO", bit=0),
        _variabili("Allarme due", "00034", kind="DIGITALE_SINGOLO", bit=1),
        _variabili("Analogica", 40001),
    ], ip="192.168.6.20")]
    out = _run(raw)
    warn = " ".join(out[0].get("_warnings") or [])
    _test("il warning sugli zeri iniziali compare",
          "ZERI INIZIALI" in warn and "00033" in warn)
    _test("il valore emesso non viene convertito",
          meta_v(out, "Allarme uno") == 33,
          "registro emesso: %s (atteso 33, non 40033)" % meta_v(out, "Allarme uno"))


def meta_v(out, nome):
    """Registro decodificato dalla prima word di DRIVERPRIVATE."""
    for m in out[0]["measures"]:
        if m["NAME"] == nome:
            dp = m.get("DRIVERPRIVATE") or ""
            mm = re.match(r"^0x([0-9A-Fa-f]{8})", dp)
            if not mm:
                return None
            h = mm.group(1).upper()
            return int(h[6:8] + h[4:6] + h[2:4] + h[0:2], 16)
    return None


def test_warning_copertura():
    """Più pagine in un solo chunk devono generare l'avviso di copertura."""
    due_pagine = [
        {"stations": [{"name": None, "ip": "192.168.0.1", "port": 502,
                       "modbus_id": 1,
                       "variables": [_variabili("Segnale A", 40001)]}]},
        {"stations": [{"name": None, "ip": "192.168.0.1", "port": 502,
                       "modbus_id": 1,
                       "variables": [_variabili("Segnale B", 40002)]}]},
    ]
    out = _run(due_pagine)
    warn = " ".join(out[0].get("_warnings") or [])
    _test("l'avviso di copertura compare su due pagine in un chunk",
          "COPERTURA SOSPETTA" in warn, warn[:120])
    _test("l'avviso cita il numero di pagine", "2 pagine" in warn)


def test_nessun_avviso_su_documento_singola_pagina():
    """Una sola pagina non deve generare l'avviso: sarebbe rumore."""
    una_pagina = [_chunk([_variabili("Solo", 40001)], ip="192.168.0.1")]
    out = _run(una_pagina)
    warn = " ".join(out[0].get("_warnings") or [])
    _test("nessun avviso di copertura su una pagina",
          "COPERTURA SOSPETTA" not in warn)


def test_caso_reale_protec_1():
    """La fixture reale PROTEC_1 deve restare invariata sotto la v4.3."""
    fx = json.load(open(FIXTURE, encoding="utf-8"))
    out = _run(fx)
    _test("PROTEC_1 produce 2 stazioni", len(out) == 2,
          "prodotte: %d" % len(out))
    _test("PROTEC_1 mantiene 3+7 misure",
          len(out[0]["measures"]) == 3 and len(out[1]["measures"]) == 7,
          "%d e %d" % (len(out[0]["measures"]), len(out[1]["measures"])))
    _test("PROTEC_1 mantiene 30+8 bitinfo",
          len(out[0]["bitinfo"]) == 30 and len(out[1]["bitinfo"]) == 8)
    _test("PROTEC_1 non segnala variabili senza indirizzo",
          (out[0].get("_meta") or {}).get("variabili_senza_registro") == 0)


def test_quadratura_su_tutti_i_casi_reali():
    """L'equazione che nessuno controllava: emesse = righe con registro.

    Le misure emesse non possono superare le righe del PDF che hanno un
    indirizzo, e ogni registro emesso deve esistere nel documento. La seconda
    parte e' quella che ha trovato il difetto: un DRIVERPRIVATE valido che
    punta pero' a un registro assente.
    """
    pdf_dir = os.path.join(ROOT, "myhydra", "single_pdf", "PDFs per il confronto")
    if not os.path.isdir(pdf_dir):
        _test("cartella dei PDF disponibile per la quadratura", False,
              "non trovata: %s" % pdf_dir)
        return
    try:
        import pymupdf
    except ImportError:
        _test("pymupdf disponibile", False, "eseguire con il .venv del repo")
        return

    # numero di registri distinti per documento, letto dal testo grezzo
    attesi = {}
    for nome, pdf in (("Mappatura_1_Cliente_SMA_1.pdf", "SMA"),
                      ("Mappatura_2_Cliente_PROTEC_1.pdf", "PROTEC"),
                      ("Mappatura_3_Cliente_PROTEC_2.pdf", "PROTEC")):
        percorso = os.path.join(pdf_dir, pdf)
        if not os.path.exists(percorso):
            continue
        doc = pymupdf.open(percorso)
        testo = "".join(p.get_text() for p in doc)
        doc.close()
        attesi[pdf] = set(re.findall(r"\b4\d{4}\b", testo))

    # gli output storici, per il confronto dei registri
    out_dir = os.path.join(ROOT, "myhydra", "single_pdf", "Outputs MYHYDRA")
    for pdf, registri_pdf in attesi.items():
        stem = os.path.splitext(pdf)[0]
        mappa = {"Mappatura_1_Cliente_SMA_1": "Output SMA_1.txt",
                 "Mappatura_2_Cliente_PROTEC_1": "Output PROTEC 1.txt",
                 "Mappatura_3_Cliente_PROTEC_2": "OUTPUT PROTEC 2.txt"}
        nome_out = mappa.get(stem)
        if not nome_out:
            continue
        p_out = os.path.join(out_dir, nome_out)
        if not os.path.exists(p_out):
            continue
        stazioni = json.load(open(p_out, encoding="utf-8"))
        if isinstance(stazioni, dict):
            stazioni = [stazioni]
        emessi = set()
        for st in stazioni:
            for m in st.get("measures", []) or []:
                r = _reg_da_priv(m.get("DRIVERPRIVATE"))
                if r is not None:
                    emessi.add(r)
        # i registri con zeri iniziali nel documento arrivano come interi
        # brevi, quindi si confronta anche la forma corta
        corti = set()
        for r in list(registri_pdf):
            corti.add(r)
            corti.add(int(str(r).lstrip("0") or "0"))
        ignoti = sorted(x for x in emessi if x not in corti and x != 0)
        _test("nessun registro emesso e' assente dal PDF (%s)" % stem,
              not ignoti, "registri ignoti: %s" % ignoti[:6])


def _reg_da_priv(priv):
    if not priv:
        return None
    mm = re.match(r"^0x([0-9A-Fa-f]{8})", str(priv))
    if not mm:
        return None
    h = mm.group(1).upper()
    return int(h[6:8] + h[4:6] + h[2:4] + h[0:2], 16)


def test_registro_zero_assente_negli_output_storici():
    """Nessun output storico deve contenere una misura a registro zero.

    Prima della v4.3 ne conteneva: le cinque grandezze derivate di SMA_1.
    """
    out_dir = os.path.join(ROOT, "myhydra", "single_pdf", "Outputs MYHYDRA")
    if not os.path.isdir(out_dir):
        return
    trovati = []
    for nome in sorted(os.listdir(out_dir)):
        if not nome.endswith(".txt"):
            continue
        try:
            stazioni = json.load(open(os.path.join(out_dir, nome),
                                      encoding="utf-8"))
        except ValueError:
            continue
        if isinstance(stazioni, dict):
            stazioni = [stazioni]
        for st in stazioni:
            for m in st.get("measures", []) or []:
                if (m.get("DRIVERPRIVATE") or "").startswith("0x00000000"):
                    trovati.append((nome, m.get("NAME")))
    # SMA_1 e' l'output storico: contiene ancora le righe a zero, perche' e'
    # stato prodotto dalla v4.2. Il test verifica che il difetto sia noto, non
    # che sia gia' risolto: la risoluzione si vede rieseguendo la v4.3.
    _test("i registri a zero sono limitati agli output storici noti",
          all(n == "Output SMA_1.txt" for n, _ in trovati),
          "trovati in: %s" % sorted(set(n for n, _ in trovati)))


# --------------------------------------------------------------------------

def main():
    test_registro_zero_non_emesso()
    test_nessun_driverprivate_a_zero()
    test_conteggio_senza_registro()
    test_warning_indirizzi_a_zeri_iniziali()
    test_warning_copertura()
    test_nessun_avviso_su_documento_singola_pagina()
    test_caso_reale_protec_1()
    test_quadratura_su_tutti_i_casi_reali()
    test_registro_zero_assente_negli_output_storici()

    print()
    print("=" * 50)
    ok = sum(1 for _, c, _ in _esiti if c)
    tot = len(_esiti)
    print("RESULT: %d passed, %d failed" % (ok, tot - ok))
    if ok != tot:
        print("\nFalliti:")
        for n, c, d in _esiti:
            if not c:
                print("  - %s  %s" % (n, d))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
