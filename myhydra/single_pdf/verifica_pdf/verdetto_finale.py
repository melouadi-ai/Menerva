"""Verdetto finale-vs-PDF per un run Single (uso: python verdetto_finale.py <FINALE> <caso>).

Confronta OGNI riga verità (registro, bit, nome normalizzato, stato) con il
finale + viceversa (invenzioni/estranei, validità ADAS). Regole motivate
(V2/V20/V21/HW) conteggiate a parte, mai silenziose.
"""
import json
import re
import struct
import sys
from collections import Counter

# Misure packed generate dal creator per ogni registro condiviso da piu'
# digitali: non stanno nella tabella verita' (che si estrae dai PDF) perche'
# nel documento non esistono come riga. Contarle come "straniere" gonfia
# ogni verdetto di 3-15 falsi positivi (PROTEC_1, PROTEC_2, SIEMENS_2).
PACKED_RE = re.compile(r"^INGRESSI DIGITALI \d+$")


def load_any(p):
    s = open(p, encoding="utf-8").read()
    i = s.find("[")
    j = s.find("{")
    return json.JSONDecoder().raw_decode(s, i if i >= 0 and (j < 0 or i < j) else j)[0]


def reg_of(priv):
    try:
        return struct.unpack("<I", bytes.fromhex(priv[2:10]))[0]
    except Exception:
        return None


def norm(s):
    return (s or "").strip().upper().replace("‐", "-").replace("–", "-").replace("_", " ").replace("\xa0", " ")


def match(nt, tt):
    """(coperta, refuso_corretto): come il typo-pair del consolidatore."""
    if nt == tt or tt.startswith(nt) or nt.startswith(tt):
        return True, False
    import re
    na = re.sub(r"[^A-Z0-9]", "", nt)
    nb = re.sub(r"[^A-Z0-9]", "", tt)
    if len(nb) >= 12 and (nb in na or na in nb):
        return True, False
    if na and nb and len(na) >= 4 and abs(len(na) - len(nb)) <= 2 and (
            (na[:3] == nb[:3] and na[-3:] == nb[-3:])
            or na in nb or nb in na):
        return True, True
    return False, False


V2 = ("disponibile", "disponibile/", "disponible", "riserva", "spare",
      "reserve", "non utilizzato", "non utilizzata", "non usato", "libero",
      "---", "misure", "comandi", "impostazioni", "input", "output",
      "parametri", "registri", "segnali", "variabili", "allarmi", "stati")


def main(fin_path, cid):
    fin = load_any(fin_path)
    meas = [(norm(m.get("NAME", "")), reg_of(m.get("DRIVERPRIVATE", "")))
            for st in fin for m in st.get("measures", [])]
    bits = []
    for st in fin:
        priv = {m.get("ID"): m.get("DRIVERPRIVATE", "") for m in st.get("measures", [])}
        for b in st.get("bitinfo", []):
            bits.append((reg_of(priv.get(b.get("MEASUREID"), "")), b.get("BITNO"),
                         norm(b.get("BITNAME", "")), b.get("TEXTON", ""), b.get("TEXTOFF", "")))
    t = json.load(open(f"myhydra/single_pdf/verifica_pdf/per_caso/{cid}/tabella_pdf.json"))
    rows = t["righe"] if isinstance(t, dict) else t
    tot = cop = stato_tot = stato_ok = 0
    hw, persi, refusi = [], [], []
    dichiarati = set()
    for st in fin:
        for w in (st.get("_warnings") or []):
            if isinstance(w, str) and w.startswith("VARIABILI SENZA INDIRIZZO:") and "Nomi:" in w:
                for nm in w.split("Nomi:", 1)[1].split(","):
                    nm = norm(nm)
                    if nm:
                        dichiarati.add(nm)
    for r in rows:
        d = norm(r.get("descrizione"))
        if not d or d in [s.upper() for s in V2]:
            continue
        tot += 1
        reg, bit = r.get("registro"), r.get("bit")
        if bit is None and reg is None:
            hits = [match(n, d) for n, g in meas]
        elif bit is None:
            hits = [match(n, d) if g == reg else (False, False)
                    for n, g in meas]
        else:
            hits = [match(c, d) if (a == reg and b == bit) else (False, False)
                    for a, b, c, _, _ in bits]
        ok = any(h for h, _ in hits)
        cor = any(t2 for _, t2 in hits)
        if cor:
            refusi.append(r)
        vero = (r.get("stato") or r.get("pdf_stato") or "").strip().upper()
        if vero:
            stato_tot += 1
            got = next((t_ for a, b, c, t_, tf in bits
                        if a == reg and b == bit), "")
            if got == vero:
                stato_ok += 1
            elif ok:
                persi.append(r)
                continue
        if ok:
            cop += 1
            continue
        if d.startswith("RISERVA") or d.startswith("-") or d.startswith("`") or r.get("pagina") in (12, 13, 14, 15, 16, 17):
            hw.append(r)
            continue
        if d in dichiarati:
            hw.append(r)
            continue
        persi.append(r)
    tb = {(r.get("registro"), r.get("bit")) for r in rows}
    tb_regs = {r.get("registro") for r in rows}
    stran = [(a, b, c) for a, b, c, _, _ in bits
             if (a, b) not in tb and (a, None) not in tb]
    null_names = {norm(r.get("descrizione")) for r in rows
                  if r.get("registro") is None}
    truth_names = [(norm(r.get("descrizione")), r.get("registro")) for r in rows
                   if norm(r.get("descrizione"))]
    derivate = [x for x in meas if PACKED_RE.match(x[0])]
    for n, g in meas:
        if PACKED_RE.match(n):
            continue
        if g is None:
            if n not in null_names:
                stran.append((g, None, n))
        elif g not in tb_regs:
            stran.append((g, None, n))
        elif not any((tn == n or m_[0]) and tg == g
                     for tn, tg in truth_names
                     for m_ in [match(n, tn)]):
            stran.append((g, None, n))
    bad = [(a, b) for a, b, c, t_, tf in bits
           if b is None or not (0 <= b <= 15) or not t_ or not tf]
    print(f"righe: {cop}/{tot}  stati: {stato_ok}/{stato_tot}  HW/spare motivati: {len(hw)}")
    print(f"BUCHI veri: {len(persi)}  invenzioni: {len(stran)}  ADAS-invalidi: {len(bad)}")
    print(f"refusi_corretti_dal_VLM: {len(refusi)} (presenti, spelling diverso dal PDF)")
    print(f"contabile (coperte+motivate): {cop + len(hw)}/{tot}")
    print(f"misure derivate packed (Ingressi digitali N, fuori verita'): {len(derivate)}")
    for r in persi:
        print("  BUCO:", r.get("pagina"), r.get("registro"), r.get("bit"),
              repr((r.get("descrizione") or "")[:44]))
    for a, b, c in stran[:5]:
        print("  STRANIERO:", a, b, repr(c[:40]))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
