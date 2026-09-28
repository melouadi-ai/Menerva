#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
compare_with_gt.py - Confronta output MyHydra/pytool (JSON o DOCX) con i ground truth.

Uso:  python3 tests/compare_with_gt.py <file_output> [--gt Json_2_Cliente_PROTEC_1.json]
Se --gt omesso, deduce il GT dal nome file (PROTEC_1 -> Json_2_Cliente_PROTEC_1.json,
SIEMENS_2 -> Json_4_Cliente_SIEMENS_2.json).

Estrae JSON da .json/.txt/.docx (python-docx opzionale), normalizza struttura
GT(dict singola stazione) vs pytool(lista stazioni), confronta per registro/bit.
"""
import json, re, sys, os, glob

def extract_text(path):
    if path.lower().endswith('.docx'):
        try:
            import docx
            return "\n".join(p.text for p in docx.Document(path).paragraphs)
        except ImportError:
            raise SystemExit("Installa python-docx per i .docx: pip install python-docx")
    with open(path, encoding='utf-8', errors='replace') as f:
        return f.read()

def parse_json_objects(s):
    s = re.sub(r'^```[a-zA-Z]*\s*', '', s.strip()); s = re.sub(r'```', '', s).strip()
    objs = []; dec = json.JSONDecoder(); pos = 0; n = len(s)
    while pos < n:
        while pos < n and s[pos] not in '{[': pos += 1
        if pos >= n: break
        try:
            obj, end = dec.raw_decode(s, pos); objs.append(obj); pos = end
        except Exception:
            pos += 1
    return objs

def reg_from_priv(dp):
    m = re.search(r'0x([0-9A-Fa-f]{8})', str(dp))
    if not m: return None
    h = m.group(1).upper()  # es. '119CA000' = 40001 in little-endian
    return int(h[6:8]+h[4:6]+h[2:4]+h[0:2], 16)
def fmt_from_priv(dp):
    m = re.search(r'0x[0-9A-F]{8}[0-9A-F]{8}[0-9A-F]{8}[0-9A-F]{8}[0-9A-F]{8}([0-9A-F]{8})', str(dp))
    if not m: return None
    h = m.group(1)  # es. '96000000' = 150 LE
    return int(h[6:8]+h[4:6]+h[2:4]+h[0:2], 16)

def norm_name(n):
    t = str(n)
    prev = None
    while prev != t:
        prev = t; t = re.sub(r'\([^()]*\)', '', t)
    prev = None
    while prev != t:
        prev = t; t = re.sub(r'\[[^\[\]]*\]', '', t)
    return re.sub(r' {2,}', ' ', t.replace('"','').replace("'",'')).strip().upper()

def collect(objs):
    measures = {}; bitinfo = []
    def add_station(st):
        for m in st.get('measures', []) or []:
            r = reg_from_priv(m.get('DRIVERPRIVATE'))
            key = (r, norm_name(m.get('NAME')))
            measures[key] = {'reg': r, 'name': norm_name(m.get('NAME')),
                             'fmt': fmt_from_priv(m.get('DRIVERPRIVATE')),
                             'DRIVERDATA': m.get('DRIVERDATA'), 'TYPE': m.get('TYPE'),
                             'UNITS': m.get('UNITS')}
        mid2reg = {m['ID']: reg_from_priv(m.get('DRIVERPRIVATE')) for m in st.get('measures', []) or []}
        for b in st.get('bitinfo', []) or []:
            bitinfo.append({'reg': mid2reg.get(b.get('MEASUREID')), 'BITNO': b.get('BITNO'),
                            'BITNAME': str(b.get('BITNAME','')).upper(),
                            'TEXTON': str(b.get('TEXTON','')).upper(), 'TEXTOFF': str(b.get('TEXTOFF','')).upper()})
    for o in objs:
        if isinstance(o, dict):
            if 'measures' in o: add_station(o)                      # GT dict singola stazione
            elif 'stations' in o:                                    # intermedio VLM
                print("[WARN] input = JSON INTERMEDIO VLM, non ADAS finale: estrarre edge[4] del pytool")
            for st in (o.get('stations') or []) if isinstance(o.get('stations'), list) else []:
                pass
            if isinstance(o, dict) and 'ID' in o and 'measures' in o: pass
        elif isinstance(o, list):
            for el in o:
                if isinstance(el, dict) and 'measures' in el: add_station(el)
    return measures, bitinfo

def main():
    args = sys.argv[1:]
    if not args: raise SystemExit(__doc__)
    path = args[0]; gt_path = None
    if '--gt' in args: gt_path = args[args.index('--gt')+1]
    if not gt_path:
        up = os.path.basename(path).upper()
        for tag, fn in [('PROTEC_1','Json_2_Cliente_PROTEC_1.json'), ('SIEMENS','Json_4_Cliente_SIEMENS_2.json')]:
            if tag in up: gt_path = 'data/test_outputs/'+fn
    if not gt_path or not os.path.exists(gt_path):
        raise SystemExit("GT non trovato per '%s': passa --gt <file>" % path)
    print("OUTPUT: %s\nGT    : %s\n" % (path, gt_path))
    mine_m, mine_b = collect(parse_json_objects(extract_text(path)))
    gt_objs = parse_json_objects(extract_text(gt_path))
    gt_m, gt_b = collect(gt_objs)
    print("MISURE  -> pytool: %d | GT: %d" % (len(mine_m), len(gt_m)))
    only_gt  = [k for k in gt_m if k not in mine_m]
    only_mine= [k for k in mine_m if k not in gt_m]
    for k in sorted(only_gt, key=str):  print("  MANCANO AL MIO  : reg=%s %s" % (k[0], k[1]))
    for k in sorted(only_mine, key=str):print("  EXTRA NEL MIO   : reg=%s %s" % (k[0], k[1]))
    diffs = 0
    for k in gt_m:
        if k in mine_m:
            a, b = gt_m[k], mine_m[k]
            d = [f for f in ('fmt','DRIVERDATA','TYPE','UNITS') if str(a[f]) != str(b[f])]
            if d:
                diffs += 1
                print("  DIFF %-40s %s" % (k[1][:40], ", ".join("%s: GT=%s mio=%s" % (f,a[f],b[f]) for f in d)))
    print("\nBITINFO -> pytool: %d | GT: %d" % (len(mine_b), len(gt_b)))
    gk = lambda x: (x['reg'], x['BITNO'])
    mb = {gk(x): x for x in mine_b}; gb = {gk(x): x for x in gt_b}
    miss = [k for k in gb if k not in mb]; extra = [k for k in mb if k not in gb]
    print("  bit mancanti nel mio: %d | extra: %d" % (len(miss), len(extra)))
    for k in sorted(miss, key=str)[:15]:  print("    MANCA  reg=%s bit=%s  %s" % (k[0], k[1], gb[k]['BITNAME'][:50]))
    for k in sorted(extra, key=str)[:15]: print("    EXTRA  reg=%s bit=%s  %s" % (k[0], k[1], mb[k]['BITNAME'][:50]))
    txt_diff = 0
    for k in gb:
        if k in mb:
            for f in ('BITNAME','TEXTON','TEXTOFF'):
                if gb[k][f] != mb[k][f]:
                    txt_diff += 1; print("    TEXT %-28s %s: GT=%r mio=%r" % (gb[k]['BITNAME'][:28], f, gb[k][f], mb[k][f])); break
    ok = not only_gt and not only_mine and not diffs and not miss and not extra and not txt_diff
    print("\n=== ESITO: %s ===" % ("PERFETTA CORRISPONDENZA" if ok else "DIFFERENZE TROVATE (vedi sopra)"))
    return 0 if ok else 1

if __name__ == '__main__':
    sys.exit(main())
