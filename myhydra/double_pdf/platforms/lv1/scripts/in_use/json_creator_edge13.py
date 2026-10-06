# pytool - Json Creator finale (contratto intermedio -> formato ADAS) - v4.4
# Input : edge 13 = chunk JSON del nodo PREPARAZIONE X JSON (11)
# Output: lista di stazioni nel formato finale ADAS (measures + bitinfo)
#
# Change-log v4.3 -> v4.4:
#  - A1: la guardia di copertura (pages>1 and chunks==1) non scattava mai
#    (pages ha un elemento per chunk). Nuovo segnale: piu' stazioni con lo
#    stesso page_no e volume sopra soglia 100 (SIEMENS_2 si, SMA_1 no).
#  - Self-check linkage bitinfo->misure in _warnings (difesa in profondita').
#  - Blocco validazione senza def/ricorsione (solo codice inline per canvas).
# Change-log v4.2 -> v4.3:
#  - Scarta le variabili senza indirizzo Modbus. Prima restavano a zero e
#    producevano una misura con DRIVERPRIVATE "0x0000...", formalmente valida
#    e sostanzialmente inesistente. Sono le grandezze derivate, che nel
#    documento hanno indicazione CALCOLATA e nessun indirizzo.
#  - Segnala gli indirizzi scritti con zeri iniziali ("00033"). Il documento
#    SMA li usa nelle sezioni digitali e "40001" in quelle analogiche: due
#    convenzioni diverse nello stesso file, che la normalizzazione tratta
#    allo stesso modo. Il valore emesso non cambia, la conversione e' una
#    decisione di dominio del cliente: qui viene resa visibile.
#  - Segnala la copertura sospetta: piu' pagine dichiarate in un solo chunk
#    indicano che il motore iterativo ha accorpato le richieste, il modo in
#    cui una perdita di copertura si manifesta senza lasciare traccia nel
#    formato dell'output.
# Change-log v4.1 -> v4.2:
#  - V25/DATA_TYPE: il formato analogico (ultimo blocco DRIVERPRIVATE) dipende
#    dal DataType dichiarato: INT16/UINT16/INT -> 150 (SIGNED_SHORT);
#    REAL32/REAL/DINT/FLOAT/assente -> 250 (FLOAT_SINGLE_BE).
#    WORD resta 250 per parita' con i ground truth SMA/PROTEC.
#  - Flag CAMPO_SCALA_AS_MEASURES (default True): se False scarta le righe
#    "CAMPO SCALA" dalle misure (policy BISON futura).
# Change-log v4 -> v4.1:
#  - P4bis: scarta description contenenti "riservat" (es. "Riservato Read/Write").
# Change-log v3 -> v4 (Piano C):
#  - P1 dedup measures; P2 fold singoli con registro condiviso in gruppo;
#    P3 registro robusto "40001.3"; P4 filtro nomi generici exact;
#    P5 pulizia parentesi duplicate-aware; P6 sanitize stati "1"/"0".
#  - Confermato: guardie A/B, DRIVERDATA=5 per Write, bitinfo singoli BITNO 0,
#    merge stazioni, forward-fill, placeholder mai fusi, rename omonime, _meta.
import json
import re
import struct
import ast

raw = r'''{edge}[13]'''

_injected_obj = None
if isinstance(raw, str):
    s = raw
else:
    _injected_obj = raw
    try:
        s = json.dumps(raw, ensure_ascii=False)
    except Exception:
        s = str(raw)

# ---------- parser multi-JSON ----------
chunks = []
ss = s.strip()
ss = re.sub(r'^```[a-zA-Z]*\s*', '', ss)
ss = re.sub(r'```', '', ss)
ss = ss.strip()
if _injected_obj is not None and not isinstance(_injected_obj, str):
    if isinstance(_injected_obj, list):
        k = 0
        while k < len(_injected_obj):
            el = _injected_obj[k]
            k = k + 1
            if isinstance(el, str):
                try:
                    chunks.append(json.loads(el))
                except Exception:
                    try:
                        chunks.append(ast.literal_eval(el))
                    except Exception:
                        pass
            else:
                chunks.append(el)
    else:
        chunks.append(_injected_obj)
elif len(ss) > 0:
    dec = json.JSONDecoder()
    pos = 0
    n = len(ss)
    while pos < n:
        while pos < n and (ss[pos] == ' ' or ss[pos] == '\n' or ss[pos] == '\r' or ss[pos] == '\t' or ss[pos] == ',' or ss[pos] == ';'):
            pos = pos + 1
        if pos >= n:
            break
        c = ss[pos]
        if c != '{' and c != '[':
            n1 = ss.find('{', pos)
            n2 = ss.find('[', pos)
            cand = -1
            if n1 >= 0 and n2 >= 0:
                if n1 < n2:
                    cand = n1
                else:
                    cand = n2
            elif n1 >= 0:
                cand = n1
            elif n2 >= 0:
                cand = n2
            if cand < 0:
                break
            pos = cand
            continue
        try:
            obj, end = dec.raw_decode(ss, pos)
            chunks.append(obj)
            pos = end
        except Exception:
            n1 = ss.find('{', pos + 1)
            n2 = ss.find('[', pos + 1)
            cand = -1
            if n1 >= 0 and n2 >= 0:
                if n1 < n2:
                    cand = n1
                else:
                    cand = n2
            elif n1 >= 0:
                cand = n1
            elif n2 >= 0:
                cand = n2
            if cand < 0:
                break
            pos = cand
if len(chunks) == 0:
    chunks = [{}]

# ---------- VALIDAZIONE PYDANTIC (Stadio 5, cablaggio opzionale) ----------
# Modulo src.models disponibile solo nell'ambiente di sviluppo/test: su MyHydra
# il pytool viene eseguito come script standalone e il pacchetto non e' presente.
# In quel caso la validazione viene saltata (fallback difensivo identico a prima).
_pydantic_available = False
try:
    import os as _os, sys as _sys
    # Risale la gerarchia di cartelle partendo da __file__ (reale o fittizio)
    # e dalla cwd, fino a trovare una root che contenga src/models/ (ambiente
    # dev/test). Su MyHydra il pytool gira come script standalone senza il
    # pacchetto: l'import fallisce e la validazione viene saltata in modo
    # sicuro (comportamento identico alla v4.2 pre-cablaggio).
    _roots = []
    try:
        _d = _os.path.dirname(_os.path.abspath(__file__))
    except Exception:
        _d = _os.getcwd()
    for _start in (_d, _os.getcwd()):
        while True:
            if _start not in _roots:
                _roots.append(_start)
            _pd = _os.path.dirname(_start)
            if _pd == _start or len(_roots) > 12:
                break
            _start = _pd
    for _cand in _roots:
        if _os.path.isdir(_os.path.join(_cand, "src", "models")) and _cand not in _sys.path:
            _sys.path.insert(0, _cand)
    from src.models.validators import safe_validate_vlm as _safe_validate_vlm
    _pydantic_available = True
except Exception:
    _pydantic_available = False

validation_errors = []
validation_warnings = []
if _pydantic_available:
    # Normalizza i chunk a livello di singola stazione (la fixture puo' essere
    # [{'stations':[...]}] oppure [{station}, {station}, ...]) e valida ogni
    # stazione contro lo schema Variable/Station del contratto intermedio.
    # Senza def/ricorsione: visita iterativa con stack esplicito (i pytool
    # canvas accettano solo codice inline).
    _all_stations = []
    _stack = [chunks]
    while _stack:
        _ch = _stack.pop()
        if isinstance(_ch, dict):
            if isinstance(_ch.get("stations"), list):
                _gi = 0
                while _gi < len(_ch["stations"]):
                    _gx = _ch["stations"][_gi]
                    if isinstance(_gx, dict):
                        _all_stations.append(_gx)
                    _gi = _gi + 1
            elif isinstance(_ch.get("variables"), list):
                _all_stations.append(_ch)
        elif isinstance(_ch, list):
            _li = len(_ch) - 1
            while _li >= 0:
                _stack.append(_ch[_li])
                _li = _li - 1
    _si = 0
    while _si < len(_all_stations):
        _st = _all_stations[_si]
        _si = _si + 1
        try:
            _res = _safe_validate_vlm({"stations": [_st]})
            if not _res.success:
                _nm = str(_st.get("name") or _st.get("NOME") or ("stazione #" + str(_si)))
                validation_errors.append(_nm + ": " + "; ".join(_res.errors[:3]))
            else:
                validation_warnings.extend(_res.warnings)
        except Exception as _e:
            validation_errors.append("eccezione validazione: " + str(_e))
# ---------- normalizzazione chunk -> pagine ----------
pages = []
i = 0
while i < len(chunks):
    ch = chunks[i]
    i = i + 1
    sts = []
    if isinstance(ch, dict):
        if isinstance(ch.get("stations"), list):
            sts = ch["stations"]
        elif isinstance(ch.get("variables"), list):
            sts = [ch]
    elif isinstance(ch, list):
        j = 0
        while j < len(ch):
            el = ch[j]
            j = j + 1
            if isinstance(el, dict):
                if isinstance(el.get("stations"), list):
                    k = 0
                    while k < len(el["stations"]):
                        sts.append(el["stations"][k])
                        k = k + 1
                elif isinstance(el.get("variables"), list):
                    sts.append(el)
    pages.append(sts)

# ---------- forward-fill cross-page + st_in ----------
DEFAULT_NAME = "SME"
DEFAULT_IP = "127.0.0.1"
GENERIC_EXACT = ["disponibile", "disponibile/", "disponible", "riserva", "spare", "reserve", "non utilizzato", "non utilizzata", "non usato", "libero", "---", "/", ""]
last_name = None
last_ip = None
last_port = None
last_mid = None
st_in = []
warn_no_ip = False
page_no = 0
p = 0
while p < len(pages):
    sts = pages[p]
    p = p + 1
    page_no = page_no + 1
    k = 0
    while k < len(sts):
        st = sts[k]
        k = k + 1
        if not isinstance(st, dict):
            continue
        nm = st.get("name")
        if nm is None or str(nm).strip() == "":
            nm = last_name
        else:
            nm = str(nm).strip()
            last_name = nm
        ip = st.get("ip")
        if ip is None or str(ip).strip() == "":
            ip = last_ip
        else:
            ip = str(ip).strip()
            last_ip = ip
        port = st.get("port")
        if port is None or str(port).strip() == "":
            port = last_port
        else:
            last_port = port
        mid = st.get("modbus_id")
        if mid is None or str(mid).strip() == "":
            mid = last_mid
        else:
            last_mid = mid
        vs = st.get("variables")
        if not isinstance(vs, list):
            vs = []
        if len(vs) == 0:
            continue
        st_in.append({"name": nm, "ip": ip, "port": port, "modbus_id": mid, "variables": vs, "page_no": page_no})

# ---------- merge stazioni per (nome, ip); placeholder mai fusi ----------
groups = []
group_index = {}
placeholder_counter = 0
i = 0
while i < len(st_in):
    st = st_in[i]
    i = i + 1
    nm = st["name"]
    if nm is None or str(nm).strip() == "":
        nm = DEFAULT_NAME
    else:
        nm = str(nm).strip()
    ip = st["ip"]
    if ip is None or str(ip).strip() == "":
        ip = DEFAULT_IP
        warn_no_ip = True
    else:
        ip = str(ip).strip()
    nn = nm.upper().replace(" ", "").replace(".", "").replace("-", "")
    is_ph = ("xxx" in ip.lower()) or (ip == ":")
    if is_ph:
        placeholder_counter = placeholder_counter + 1
        merge_key = "__placeholder_" + str(placeholder_counter) + "__"
    else:
        merge_key = nn + "|" + ip
    if merge_key in group_index:
        found = group_index[merge_key]
    else:
        groups.append([nm, ip, st["port"], st["modbus_id"], []])
        found = len(groups) - 1
        group_index[merge_key] = found
    if groups[found][2] is None and st["port"] is not None:
        groups[found][2] = st["port"]
    if groups[found][3] is None and st["modbus_id"] is not None:
        groups[found][3] = st["modbus_id"]
    groups[found][4] = groups[found][4] + st["variables"]

# ---------- costanti di formato ----------
FMT_SHORT = 150
FMT_FLOAT = 250
FMT_INT16 = FMT_SHORT
FMT_REAL32 = FMT_FLOAT
CAMPO_SCALA_AS_MEASURES = True
BIG = 3.40282e+38
NEGBIG = -3.40282e+38
VM_DEFAULT = "if elapsed() then    storep(11);else store(8);fi;"
MCFG = "<configuration SynopticAnalogicFormat=\"%7.2f\"/>"
KW = [
    ["VALVOLA", "APERTO", "CHIUSO"],
    ["BY-PASS", "BYPASS", "CHIUSO"],
    ["BYPASS", "BYPASS", "CHIUSO"],
    ["ALLARME", "ALLARME", "OFF"],
    ["FAULT", "GUASTO", "OFF"],
    ["GUASTO", "GUASTO", "OFF"],
    ["ANOMALIA", "ANOMALIA", "OFF"],
    ["MANUTENZIONE", "MANUTENZIONE", "OFF"],
    ["CALIBRAZIONE", "CALIBRAZIONE", "OFF"],
    ["ZERO", "ZERO", "OFF"],
    ["SPAN", "SPAN", "OFF"]
]

# ---------- generazione misure/bitinfo per stazione ----------
out = []
sid = 0
g = 0
# v4.3: accumulatori globali dei controlli introdotti in questa versione.
# Sono dichiarati qui fuori dal ciclo perche' i controlli valgono sull'output
# nel suo complesso, non per singola stazione: un indirizzo a zeri iniziali in
# una stazione e' un problema dell'intero documento.
zero_padded_tutto = {}
senza_registro_tutto = 0
senza_registro_nomi_tutto = []
link_issues_tutto = []
while g < len(groups):
    nm = groups[g][0]
    ip = groups[g][1]
    port = groups[g][2]
    mid = groups[g][3]
    vs = groups[g][4]
    try:
        port = int(port)
    except Exception:
        port = 502
    try:
        mid = int(mid)
    except Exception:
        mid = 1
    sid = sid + 1
    # P2: pre-conteggio registri tra singoli digitali (registro condiviso?)
    sing_count = {}
    i = 0
    while i < len(vs):
        v = vs[i]
        i = i + 1
        if not isinstance(v, dict):
            continue
        if v.get("kind") == "DIGITALE_SINGOLO":
            rr = v.get("modbus_register")
            if rr is not None:
                mm = re.match(r'\s*([0-9]+)', str(rr))
                if mm is not None:
                    rv = int(mm.group(1))
                    sing_count[rv] = sing_count.get(rv, 0) + 1
    shared_regs = {}
    for kk in sing_count:
        if sing_count[kk] > 1:
            shared_regs[kk] = True
    measures = []
    bitinfo = []
    seen_bits = {}
    seen_analog = {}
    seen_single = {}
    seen_packed = {}
    packed_index = {}
    packed_count = 0
    mid_seq = 0
    # v4.3: due accumulatori per i controlli introdotti in questa versione
    zero_padded_regs = {}
    senza_registro = 0
    senza_registro_nomi = []
    i = 0
    while i < len(vs):
        v = vs[i]
        i = i + 1
        if not isinstance(v, dict):
            continue
        desc = v.get("description")
        if desc is None or str(desc).strip() == "":
            continue
        desc = str(desc).strip()
        if desc.lower() in GENERIC_EXACT:
            continue
        # P4bis: scarta righe "Riservato ..."
        if desc.lower().find("riservat") >= 0:
            continue
        # v4.2: policy CAMPO SCALA (default: restano misure)
        if (not CAMPO_SCALA_AS_MEASURES) and desc.upper().find("CAMPO SCALA") >= 0:
            continue
        # v4.3: una variabile senza indirizzo Modbus non e' leggibile dal PLC.
        # Senza questo controllo restava a zero e produceva una misura con
        # DRIVERPRIVATE "0x0000...", cioe' formalmente valida e sostanzialmente
        # inesistente. Sono le grandezze derivate, che nel documento hanno
        # indicato CALCOLATA e nessun indirizzo: vanno scartate.
        if v.get("modbus_register") is None or str(v.get("modbus_register")).strip() == "":
            senza_registro = senza_registro + 1
            if len(senza_registro_nomi) < 20:
                senza_registro_nomi.append(desc)
            continue
        kind = v.get("kind")
        reg = v.get("modbus_register")
        regval = 0
        bit = v.get("bit")
        bitval = None
        # P3: registro robusto "40001.3" / "40001_3"
        if reg is not None:
            rs = str(reg).strip()
            mm = re.match(r'\s*([0-9]+)', rs)
            if mm is not None:
                regval = int(mm.group(1))
                # v4.3: riconosce gli indirizzi con zeri iniziali.
                # Il documento SMA scrive "00033" nelle sezioni digitali e
                # "40001" in quelle analogiche: due convenzioni diverse nello
                # stesso file. La normalizzazione le tratta allo stesso modo,
                # quindi "00033" diventa 33, che come registro Modbus e'
                # diverso da 40033. Il valore emesso non viene cambiato, perche'
                # la conversione e' una decisione di dominio del cliente: qui
                # si registra l'anomalia, cosi' smette di essere silenziosa.
                raw_digits = mm.group(1)
                if raw_digits.startswith("0") and len(raw_digits) >= 4:
                    zero_padded_regs[raw_digits] = True
                rest = rs[mm.end(1):]
                if rest[:1] == '.' or rest[:1] == '_':
                    frac = rest[1:]
                    fm = re.match(r'\s*([0-9]+)', frac)
                    if fm is not None and bit is None:
                        bitval = int(fm.group(1))
        if bitval is None:
            if bit is not None:
                try:
                    bitval = int(str(bit).strip())
                except Exception:
                    bitval = 0
            else:
                bitval = 0
        units = v.get("units")
        if units is not None:
            units = str(units).strip()
            if units == "":
                units = None
        son = v.get("state_on")
        soff = v.get("state_off")
        if son is not None:
            son = str(son).strip()
            if son == "":
                son = None
        if soff is not None:
            soff = str(soff).strip()
            if soff == "":
                soff = None
        # P6: sanitize stati "1"/"0"
        if son == "1" or son == "0":
            son = None
        if soff == "1" or soff == "0":
            soff = None
        rw = v.get("read_write")
        if rw is not None:
            rw = str(rw).strip().upper()
            if rw.startswith("W"):
                rw = "W"
            elif rw.startswith("R"):
                rw = "R"
            else:
                rw = None
        else:
            rw = None
        # v4.2: formato analogico in base al data_type dichiarato (V25)
        fmt_analog = FMT_REAL32
        dt = v.get("data_type")
        if dt is not None:
            dtu = str(dt).strip().upper()
            if dtu.find("INT16") >= 0 or dtu.find("UINT16") >= 0 or dtu == "INT":
                fmt_analog = FMT_INT16
        # Guardia A
        if kind == "DIGITALE_SINGOLO" and regval == 0 and bit is None:
            kind = "ANALOGICA"
        # Guardia B
        if kind == "DIGITALE_SINGOLO" and bit is None:
            up0 = desc.upper()
            keywords = ["STATO IMPIANTO", "STATO DOSAGGIO", "CONTATORE", "CONTAORE", "WATCHDOG", "LIVE PLC", "LIVEPLC"]
            kw = 0
            hit = False
            while kw < len(keywords):
                if up0.find(keywords[kw]) >= 0:
                    hit = True
                    break
                kw = kw + 1
            if hit:
                kind = "ANALOGICA"
        # P2: singolo con registro condiviso -> diventa impacchettato
        if kind == "DIGITALE_SINGOLO" and regval in shared_regs:
            kind = "DIGITALE_IMPACCATO"
        # P1 dedup
        if kind == "ANALOGICA":
            dkey = desc.lower() + "|" + str(regval)
            if dkey in seen_analog:
                continue
            seen_analog[dkey] = True
        elif kind == "DIGITALE_SINGOLO":
            dkey = str(regval)
            if dkey in seen_single:
                continue
            seen_single[dkey] = True
        else:
            dkey = desc.lower() + "|" + str(regval)
            if dkey in seen_packed:
                continue
            seen_packed[dkey] = True
        up = desc.upper()
        kton = "ATTIVO"
        ktoff = "OFF"
        k = 0
        while k < len(KW):
            if up.find(KW[k][0]) >= 0:
                kton = KW[k][1]
                ktoff = KW[k][2]
                break
            k = k + 1
        ton = son
        if ton is None:
            ton = kton
        ton = ton.upper()
        toff = soff
        if toff is None:
            toff = ktoff
        toff = toff.upper()
        if kind == "DIGITALE_IMPACCATO":
            if regval not in packed_index:
                packed_count = packed_count + 1
                mid_seq = mid_seq + 1
                priv = "0x"
                priv = priv + struct.pack('<I', regval).hex().upper()
                priv = priv + "00000000"
                priv = priv + "00000000"
                priv = priv + struct.pack('<I', 0).hex().upper()
                priv = priv + struct.pack('<I', mid).hex().upper()
                priv = priv + struct.pack('<I', FMT_SHORT).hex().upper()
                measures.append({"STATIONID": sid, "NAME": "Ingressi digitali " + str(packed_count), "DISABLED": 0, "DIGITAL": None, "DOWNLOAD": 0, "SNAPSHOT": 1, "IGNOREERRORS": 0, "LOWCRITICAL": None, "HIGHCRITICAL": None, "LOWRANGE": None, "HIGHRANGE": None, "LOWOFFSET": None, "HIGHOFFSET": None, "SQRAW": None, "SQ1HOURMEAN": None, "SQ3HOURMEAN": None, "SQ8HOURMEAN": None, "SQDAILYMEAN": None, "UNITS": None, "STANDARDRANGEID": None, "DRIVERDATA": 2, "TYPE": 1, "DRIVERPRIVATE": priv, "ONLY_POSITIVES": None, "VM_SOURCE_CODE": VM_DEFAULT, "PERIOD": 5, "SNAPSIZE": 1000, "DRIVERCONFIG": MCFG, "ID": mid_seq, "UNITS2": None})
                packed_index[regval] = mid_seq
            mid_target = packed_index[regval]
            bkey = str(mid_target) + ":" + str(bitval)
            if bkey not in seen_bits:
                seen_bits[bkey] = True
                bitinfo.append({"MEASUREID": mid_target, "BITNO": bitval, "BITNAME": desc.upper(), "TEXTON": ton, "TEXTOFF": toff})
        elif kind == "DIGITALE_SINGOLO":
            mid_seq = mid_seq + 1
            dd = 1
            if rw == "W":
                dd = 5
            priv = "0x"
            priv = priv + struct.pack('<I', regval).hex().upper()
            priv = priv + "00000000"
            priv = priv + "00000000"
            priv = priv + struct.pack('<I', 0).hex().upper()
            priv = priv + struct.pack('<I', mid).hex().upper()
            priv = priv + struct.pack('<I', FMT_SHORT).hex().upper()
            measures.append({"STATIONID": sid, "NAME": desc, "DISABLED": 0, "DIGITAL": None, "DOWNLOAD": 0, "SNAPSHOT": 1, "IGNOREERRORS": 0, "LOWCRITICAL": None, "HIGHCRITICAL": None, "LOWRANGE": None, "HIGHRANGE": None, "LOWOFFSET": None, "HIGHOFFSET": None, "SQRAW": None, "SQ1HOURMEAN": None, "SQ3HOURMEAN": None, "SQ8HOURMEAN": None, "SQDAILYMEAN": None, "UNITS": None, "STANDARDRANGEID": None, "DRIVERDATA": dd, "TYPE": 6, "DRIVERPRIVATE": priv, "ONLY_POSITIVES": None, "VM_SOURCE_CODE": VM_DEFAULT, "PERIOD": 5, "SNAPSIZE": 1000, "DRIVERCONFIG": MCFG, "ID": mid_seq, "UNITS2": None})
            bkey = str(mid_seq) + ":0"
            if bkey not in seen_bits:
                seen_bits[bkey] = True
                bitinfo.append({"MEASUREID": mid_seq, "BITNO": 0, "BITNAME": desc.upper(), "TEXTON": ton, "TEXTOFF": toff})
        else:
            mid_seq = mid_seq + 1
            priv = "0x"
            priv = priv + struct.pack('<I', regval).hex().upper()
            priv = priv + "00000000"
            priv = priv + "00000000"
            priv = priv + struct.pack('<I', 0).hex().upper()
            priv = priv + struct.pack('<I', mid).hex().upper()
            priv = priv + struct.pack('<I', fmt_analog).hex().upper()
            measures.append({"STATIONID": sid, "NAME": desc, "DISABLED": 0, "DIGITAL": None, "DOWNLOAD": 0, "SNAPSHOT": 1, "IGNOREERRORS": 0, "LOWCRITICAL": NEGBIG, "HIGHCRITICAL": BIG, "LOWRANGE": NEGBIG, "HIGHRANGE": BIG, "LOWOFFSET": NEGBIG, "HIGHOFFSET": BIG, "SQRAW": BIG, "SQ1HOURMEAN": BIG, "SQ3HOURMEAN": BIG, "SQ8HOURMEAN": BIG, "SQDAILYMEAN": BIG, "UNITS": units, "STANDARDRANGEID": None, "DRIVERDATA": 0, "TYPE": 0, "DRIVERPRIVATE": priv, "ONLY_POSITIVES": 0, "VM_SOURCE_CODE": VM_DEFAULT, "PERIOD": 5, "SNAPSIZE": 1000, "DRIVERCONFIG": MCFG, "ID": mid_seq, "UNITS2": units})
    # ---------- P5 pulizia parentesi (Nodo 8) duplicate-aware ----------
    all_names = []
    i = 0
    while i < len(measures):
        all_names.append(str(measures[i]["NAME"]))
        i = i + 1
    bases = []
    i = 0
    while i < len(all_names):
        b = all_names[i]
        prev = None
        while prev != b:
            prev = b
            b = re.sub(r'\([^()]*\)', '', b)
        prev = None
        while prev != b:
            prev = b
            b = re.sub(r'\[[^\[\]]*\]', '', b)
        b = b.replace('"', '').replace("'", '')
        b = re.sub(r' {2,}', ' ', b).strip()
        bases.append(b)
        i = i + 1
    i = 0
    while i < len(measures):
        t = str(measures[i]["NAME"])
        if bases.count(bases[i]) > 1:
            prev = None
            while prev != t:
                prev = t
                t = re.sub(r'\(\s*\)', '', t)
        else:
            prev = None
            while prev != t:
                prev = t
                t = re.sub(r'\([^()]*\)', '', t)
        prev = None
        while prev != t:
            prev = t
            t = re.sub(r'\[[^\[\]]*\]', '', t)
        t = t.replace('"', '').replace("'", '')
        t = re.sub(r' {2,}', ' ', t).strip()
        measures[i]["NAME"] = t
        i = i + 1
    i = 0
    while i < len(bitinfo):
        b = bitinfo[i]
        flds = ["BITNAME", "TEXTON", "TEXTOFF"]
        f = 0
        while f < len(flds):
            t = str(b.get(flds[f]))
            prev = None
            while prev != t:
                prev = t
                t = re.sub(r'\([^()]*\)', '', t)
            prev = None
            while prev != t:
                prev = t
                t = re.sub(r'\[[^\[\]]*\]', '', t)
            t = t.replace('"', '').replace("'", '')
            t = re.sub(r' {2,}', ' ', t).strip()
            b[flds[f]] = t
            f = f + 1
        i = i + 1
    # Linkage bitinfo -> misure (difesa in profondita'): ogni MEASUREID deve
    # esistere tra gli ID delle misure; ogni misura packed deve avere almeno
    # una riga bitinfo. Le divergenze (es. paste non aggiornata sul canvas)
    # finiscono in review invece di passare silenziose.
    mids = {}
    mi = 0
    while mi < len(measures):
        mids[measures[mi].get("ID")] = True
        mi = mi + 1
    covered = {}
    bi = 0
    while bi < len(bitinfo):
        bmid = bitinfo[bi].get("MEASUREID")
        covered[bmid] = True
        if bmid not in mids:
            link_issues_tutto.append(str(bitinfo[bi].get("BITNAME")) + " -> misura " + str(bmid))
        bi = bi + 1
    mi = 0
    while mi < len(measures):
        if measures[mi].get("DRIVERDATA") == 2 and measures[mi].get("ID") not in covered:
            link_issues_tutto.append("misura packed senza bitinfo: " + str(measures[mi].get("NAME")))
        mi = mi + 1
    drv = "<configuration><commProto><p0 class=\"Protocollo MODBUS (master) via TCP/IP\" "
    drv = drv + "name=\"Protocollo MODBUS (master) via TCP/IP\" "
    drv = drv + "ipaddress=\"" + ip + "\" "
    drv = drv + "tcpport=\"" + str(port) + "\" "
    drv = drv + "timeout=\"5000\" retries=\"3\" write4XXXX=\"6\"/></commProto>"
    drv = drv + "<recoveryProto/></configuration>"
    out.append({"NAME": nm, "DRIVERNAME": "modbusplc", "XPOSITION": 430, "YPOSITION": 530, "DOWNLOADTYPE": 0, "DOWNLOADPROGRAM": None, "IGNOREERRORS": 0, "SNAPSHOT": None, "NORMALSNAPSHOT": 1, "CRITICSNAPSHOT": 32767, "ALARMSNAPSHOT": 32767, "SYNOBITMAP": None, "LINENAME": None, "AREACODE": None, "ADDRESS": None, "LINECONFIGURATION": None, "TIMELASTCONFIGURATION": None, "TIMELASTDOWNLOAD": None, "EVENTTIME": None, "EVENTCODE": 0, "EVENTORIGIN": None, "CODE": None, "DRIVERPRIVATE": None, "OVERWRITEMEASURES": 1, "DRIVERCONFIG": drv, "ID": sid, "measures": measures, "bitinfo": bitinfo})
    # v4.3: i controlli della stazione confluiscono nei totali del documento
    for kk in zero_padded_regs:
        zero_padded_tutto[kk] = True
    senza_registro_tutto = senza_registro_tutto + senza_registro
    senza_registro_nomi_tutto = senza_registro_nomi_tutto + senza_registro_nomi
    g = g + 1

# ---------- rename stazioni omonime ----------
seen = {}
i = 0
while i < len(out):
    base = out[i]["NAME"]
    if base in seen:
        seen[base] = seen[base] + 1
        out[i]["NAME"] = base + " " + str(seen[base])
    else:
        seen[base] = 0
    i = i + 1

# ---------- output + meta ----------
meta = {"chunks_parsed": len(chunks), "pages_processed": len(pages), "stations_in_input": len(st_in), "stations_output": len(out), "variables_total": 0, "raw_type": str(type(raw)), "raw_len": len(s), "chunk_types": [], "station_details": [], "raw_sample": repr(s[:500])}
i = 0
while i < len(chunks):
    meta["chunk_types"].append(str(type(chunks[i])))
    i = i + 1
tv = 0
i = 0
while i < len(st_in):
    tv = tv + len(st_in[i]["variables"])
    vsd = st_in[i]["variables"]
    fd = ""
    ld = ""
    if len(vsd) > 0 and isinstance(vsd[0], dict) and vsd[0].get("description") is not None:
        fd = str(vsd[0].get("description"))[:80]
    if len(vsd) > 0 and isinstance(vsd[len(vsd) - 1], dict) and vsd[len(vsd) - 1].get("description") is not None:
        ld = str(vsd[len(vsd) - 1].get("description"))[:80]
    meta["station_details"].append({"page_no": st_in[i]["page_no"], "name": st_in[i]["name"], "ip": st_in[i]["ip"], "port": st_in[i]["port"], "modbus_id": st_in[i]["modbus_id"], "num_vars": len(vsd), "first_desc": fd, "last_desc": ld})
    i = i + 1
meta["variables_total"] = tv
meta["variabili_senza_registro"] = senza_registro_tutto
meta["indirizzi_con_zeri_iniziali"] = len(zero_padded_tutto)
if len(out) == 0:
    dbg = {"DEBUG": True, "raw_len": len(s), "chunks_parsed": len(chunks), "pages_processed": len(pages), "raw_head": s[:800]}
    output = json.dumps(dbg, ensure_ascii=False, indent=1)
else:
    i = 0
    while i < len(out):
        out[i]["_meta"] = meta
        i = i + 1
    warnings = []
    if warn_no_ip:
        warnings.append("nessun IP dichiarato nel documento: usato default " + DEFAULT_IP)
    warnings.extend(validation_warnings)
    if len(validation_errors) > 0:
        warnings.append("VALIDAZIONE SCHEMA (Pydantic): " + str(len(validation_errors)) + " stazione/i con errori -> " + " | ".join(validation_errors[:5]))
    # v4.4 (A1): la guardia precedente (pages>1 and chunks==1) non scattava
    # mai: pages ha un elemento per chunk, quindi len(pages)==len(chunks)
    # sempre. Segnale reale di accorpamento: piu' stazioni con lo stesso
    # page_no e volume sopra soglia. Soglia 100: sopra sta SIEMENS_2 (274
    # variabili ricevute in un chunk), sotto restano silenti i documenti
    # piccoli legittimi (SMA_1: 1 pagina, ~50 variabili). La soglia e' una
    # scelta documentata, non un requisito: tararla se cambia il parco
    # documenti. Il pytool non puo' sapere quante righe il documento
    # contiene, ma puo' dire se quello che ha ricevuto e' coerente con
    # un'elaborazione pagina per pagina.
    if len(st_in) > 1:
        _pnos = {}
        _qi = 0
        while _qi < len(st_in):
            _pnos[st_in[_qi].get("page_no")] = True
            _qi = _qi + 1
        if len(_pnos) == 1 and tv > 100:
            warnings.append("COPERTURA SOSPETTA: " + str(tv) + " variabili in " + str(len(st_in)) + " stazioni con stesso page_no (" + str(list(_pnos.keys())[0]) + "). Il motore iterativo dovrebbe inviare un chunk per pagina: verificare che non stia accorpando piu' pagine in una richiesta.")
    if len(zero_padded_tutto) > 0:
        kk = sorted(zero_padded_tutto.keys())
        warnings.append("INDIRIZZI CON ZERI INIZIALI: " + str(len(kk)) + " indirizzi scritti con zeri iniziali nel documento (" + ", ".join(kk[:8]) + ("..." if len(kk) > 8 else "") + "). Dopo la normalizzazione valgono come intero breve, che e' un registro diverso da quello scritto. Verificare se il documento li intende come indirizzi HMI o Modbus: la conversione non viene applicata perche' e' una decisione di dominio.")
    if senza_registro_tutto > 0:
        warnings.append("VARIABILI SENZA INDIRIZZO: " + str(senza_registro_tutto) + " variabili scartate perche' non hanno un indirizzo Modbus, quindi non sono leggibili dal PLC (grandezze derivate, indicazione CALCOLATA). Nomi: " + ", ".join(senza_registro_nomi_tutto[:6]) + ("..." if len(senza_registro_nomi_tutto) > 6 else ""))
    if len(link_issues_tutto) > 0:
        warnings.append("BITINFO NON COLLEGATI: " + str(len(link_issues_tutto)) + " anomalie di linkage misure-bitinfo (" + ", ".join(link_issues_tutto[:6]) + ("..." if len(link_issues_tutto) > 6 else "") + "). Verificare che lo script sul canvas sia identico al repo.")
    if len(warnings) > 0:
        i = 0
        while i < len(out):
            out[i]["_warnings"] = warnings
            i = i + 1
    output = json.dumps(out, indent=1, ensure_ascii=False)

print(output)
