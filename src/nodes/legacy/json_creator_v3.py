# pytool - Json Creator finale (contratto intermedio -> formato ADAS) - v3 MULTI-PAGE
# Input : edge 3 = JSON intermedio prodotto dal VLM (stations/variables),
#         potenzialmente aggregato su PIU' PAGINE (una per iterazione VLM).
# Output: lista di stazioni nel formato finale ADAS (measures + bitinfo).
#
# Change-log rispetto a v2 PATCHED:
#  - parser multi-JSON (raw_decode in loop): accetta concatenazione, JSONL,
#    array esterno, repr Python, oggetto gia' parsato.
#  - FORWARD-FILL CROSS-PAGE: name/ip/port/modbus_id null ereditano l'ultimo
#    valore valido del documento, cosi' le righe di pagine successive che
#    continuano la stessa stazione NON vengono create come stazioni spurie.
#    Regole di priorita':
#       * valore proprio NON null -> usato (e diventa il nuovo "ultimo valido")
#       * valore null -> eredita dall'ultimo valido
#       * pagina con variables=[] (frontespizio/pagina vuota) -> skippata
#       * IP placeholder (xxx.xxx.xxx.xxx) -> trattato come valore proprio
#         (regola S8 del prompt: stazione separata, mai fuso con IP reale)
#  - dedup bitinfo per (MEASUREID, BITNO): gestisce registri impacchettati
#    che continuano su pagine successive (es. 40001 bits 0..7 pag1 + 8..15 pag2).
#  - DEBUG output potenziato: conta JSON chunks, variabili totali, per-chunk info.
#  - WARNING per documenti senza IP (invece di default 127.0.0.1 silenzioso):
#    il warning viene incluso nel payload di output come chiave "_warnings"
#    (solo se ci sono warning, cosi' i casi normali non cambiano).
#
# BISON: ancora hardcodata al default. La linearizzazione con scale
# (ZE/SE/ZI/SI) richiede specifiche dal cliente (TODO).
#
# NOTA STILE: solo while loop, niente f-string, niente `def`, niente for:
# il pytool MyHydra ha un runtime limitato che potrebbe non accettarli.

import json
import re
import struct
import ast

# ---------- ingresso: placeholder MyHydra ----------
raw = r'''{edge}[3]'''

# ---------- normalizzazione iniziale (oggetto vs stringa) ----------
# Se MyHydra inietta un oggetto/lista/dict gia' parsato, trattiamolo come tale.
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
# Accetta: JSON singolo, concatenazione "{...}{...}", JSONL, array "[{...}]",
# oppure stringhe python-repr. Raccoglie i chunk in ordine (1 chunk = 1 pagina).
chunks = []
ss = s.strip()
ss = re.sub(r'^```[a-zA-Z]*\s*', '', ss)
# rimuove eventuali fence markdown INTERNE (possono comparire tra chunk)
ss = re.sub(r'```', '', ss)
ss = ss.strip()

if _injected_obj is not None and not isinstance(_injected_obj, str):
    # percorso veloce: gia' oggetto
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
        # salta separatori tra chunk
        while pos < n and (ss[pos] == ' ' or ss[pos] == '\n' or ss[pos] == '\r' \
                          or ss[pos] == '\t' or ss[pos] == ',' or ss[pos] == ';'):
            pos = pos + 1
        if pos >= n:
            break
        c = ss[pos]
        if c != '{' and c != '[':
            # salta testo spazzatura fino al prossimo { o [
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
            # parse fallito: salta e riprova al prossimo {/[
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

# ---------- normalizzazione chunk -> pagine (preserva ordine) ----------
# Ogni chunk diventa una lista di stazioni; chunks vuoti danno [].
# La struttura di output 'pages' preserva l'ordine dei chunk = ordine delle pagine.
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
        # lista di stazioni o di sotto-chunk annidati
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

# ---------- FORWARD-FILL cross-page + st_in ----------
# Costruisce st_in: lista di {name, ip, port, modbus_id, variables, page_no}
# - name/ip/port/modbus_id null o vuoti ereditano l'ultimo valore valido
# - pagine con variables=[] (frontespizio) NON entrano in st_in
# - placeholder IP (xxx.xxx...) sono considerati valori propri
DEFAULT_NAME = "SME"
DEFAULT_IP = "127.0.0.1"

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

        # --- name
        nm = st.get("name")
        if nm is None or str(nm).strip() == "":
            nm = last_name
        else:
            nm = str(nm).strip()
            last_name = nm

        # --- ip
        ip = st.get("ip")
        if ip is None or str(ip).strip() == "":
            ip = last_ip
        else:
            ip = str(ip).strip()
            last_ip = ip

        # --- port
        port = st.get("port")
        if port is None or str(port).strip() == "":
            port = last_port
        else:
            last_port = port

        # --- modbus_id
        mid = st.get("modbus_id")
        if mid is None or str(mid).strip() == "":
            mid = last_mid
        else:
            last_mid = mid

        vs = st.get("variables")
        if not isinstance(vs, list):
            vs = []

        # skip pagine senza variabili (frontespizio, pagina di testo, ecc.)
        if len(vs) == 0:
            continue

        st_in.append({
            "name": nm,
            "ip": ip,
            "port": port,
            "modbus_id": mid,
            "variables": vs,
            "page_no": page_no
        })

# ---------- merge stazioni per (nome, ip) ----------
# Dopo il forward-fill, le righe della stessa stazione su pagine diverse
# hanno name+ip coerenti, quindi il merge li raggruppa correttamente.
groups = []   # ogni elemento: [name, ip, port, modbus_id, [variables]]
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
    port = st["port"]
    mid = st["modbus_id"]
    vs = st["variables"]

    # cerca gruppo esistente
    g = 0
    found = -1
    while g < len(groups):
        if groups[g][0] == nm and groups[g][1] == ip:
            found = g
            break
        g = g + 1
    if found < 0:
        groups.append([nm, ip, port, mid, []])
        found = len(groups) - 1
    if groups[found][2] is None and port is not None:
        groups[found][2] = port
    if groups[found][3] is None and mid is not None:
        groups[found][3] = mid
    groups[found][4] = groups[found][4] + vs

# ---------- costanti di formato ----------
FMT_SHORT = 150
FMT_FLOAT = 250
BIG = 3.40282e+38
NEGBIG = -3.40282e+38
VM_DEFAULT = "if elapsed() then    storep(11);else store(8);fi;"
MCFG = "<configuration SynopticAnalogicFormat=\"%7.2f\"/>"

# ---------- tabella keyword per TEXTON/TEXTOFF di fallback ----------
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

    measures = []
    bitinfo = []
    seen_bits = {}           # FIX v3: dedup bitinfo (MEASUREID, BITNO)
    packed_index = {}        # registro -> ID measure impacchettata
    packed_count = 0
    mid_seq = 0

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
        kind = v.get("kind")
        reg = v.get("modbus_register")
        if reg is not None:
            try:
                reg = int(str(reg).strip())
            except Exception:
                reg = None
        bit = v.get("bit")
        if bit is not None:
            try:
                bit = int(str(bit).strip())
            except Exception:
                bit = None
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

        # ---- Guardia A: digitale singolo senza indirizzo -> analogica ----
        if kind == "DIGITALE_SINGOLO" and reg is None and bit is None:
            kind = "ANALOGICA"
        # ---- Guardia B: codici di stato / contatori -> analogica ----
        if kind == "DIGITALE_SINGOLO" and bit is None:
            up0 = desc.upper()
            keywords = ["STATO IMPIANTO", "STATO DOSAGGIO", "CONTATORE",
                        "CONTAORE", "WATCHDOG", "LIVE PLC", "LIVEPLC"]
            kw = 0
            hit = False
            while kw < len(keywords):
                if up0.find(keywords[kw]) >= 0:
                    hit = True
                    break
                kw = kw + 1
            if hit:
                kind = "ANALOGICA"

        regval = reg
        if regval is None:
            regval = 0
        bitval = bit
        if bitval is None:
            bitval = 0

        # ---- fallback TEXTON/TEXTOFF da keyword quando gli stati mancano ----
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
            # raggruppa per registro in una measure "Ingressi digitali N"
            if reg not in packed_index:
                packed_count = packed_count + 1
                mid_seq = mid_seq + 1
                priv = "0x"
                priv = priv + struct.pack('<I', regval).hex().upper()
                priv = priv + "00000000"
                priv = priv + "00000000"
                priv = priv + struct.pack('<I', 0).hex().upper()
                priv = priv + struct.pack('<I', mid).hex().upper()
                priv = priv + struct.pack('<I', FMT_SHORT).hex().upper()
                measures.append({
                    "STATIONID": sid,
                    "NAME": "Ingressi digitali " + str(packed_count),
                    "DISABLED": 0,
                    "DIGITAL": None,
                    "DOWNLOAD": 0,
                    "SNAPSHOT": 1,
                    "IGNOREERRORS": 0,
                    "LOWCRITICAL": None,
                    "HIGHCRITICAL": None,
                    "LOWRANGE": None,
                    "HIGHRANGE": None,
                    "LOWOFFSET": None,
                    "HIGHOFFSET": None,
                    "SQRAW": None,
                    "SQ1HOURMEAN": None,
                    "SQ3HOURMEAN": None,
                    "SQ8HOURMEAN": None,
                    "SQDAILYMEAN": None,
                    "UNITS": None,
                    "STANDARDRANGEID": None,
                    "DRIVERDATA": 2,
                    "TYPE": 1,
                    "DRIVERPRIVATE": priv,
                    "ONLY_POSITIVES": None,
                    "VM_SOURCE_CODE": VM_DEFAULT,
                    "PERIOD": 5,
                    "SNAPSIZE": 1000,
                    "DRIVERCONFIG": MCFG,
                    "ID": mid_seq,
                    "UNITS2": None
                })
                packed_index[reg] = mid_seq
            mid_target = packed_index[reg]
            bkey = str(mid_target) + ":" + str(bitval)
            if bkey not in seen_bits:
                seen_bits[bkey] = True
                bitinfo.append({
                    "MEASUREID": mid_target,
                    "BITNO": bitval,
                    "BITNAME": desc.upper(),
                    "TEXTON": ton,
                    "TEXTOFF": toff
                })
        elif kind == "DIGITALE_SINGOLO":
            mid_seq = mid_seq + 1
            # comando in Write -> DRIVERDATA 5 (README)
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
            measures.append({
                "STATIONID": sid,
                "NAME": desc,
                "DISABLED": 0,
                "DIGITAL": None,
                "DOWNLOAD": 0,
                "SNAPSHOT": 1,
                "IGNOREERRORS": 0,
                "LOWCRITICAL": None,
                "HIGHCRITICAL": None,
                "LOWRANGE": None,
                "HIGHRANGE": None,
                "LOWOFFSET": None,
                "HIGHOFFSET": None,
                "SQRAW": None,
                "SQ1HOURMEAN": None,
                "SQ3HOURMEAN": None,
                "SQ8HOURMEAN": None,
                "SQDAILYMEAN": None,
                "UNITS": None,
                "STANDARDRANGEID": None,
                "DRIVERDATA": dd,
                "TYPE": 6,
                "DRIVERPRIVATE": priv,
                "ONLY_POSITIVES": None,
                "VM_SOURCE_CODE": VM_DEFAULT,
                "PERIOD": 5,
                "SNAPSIZE": 1000,
                "DRIVERCONFIG": MCFG,
                "ID": mid_seq,
                "UNITS2": None
            })
            bkey = str(mid_seq) + ":0"
            if bkey not in seen_bits:
                seen_bits[bkey] = True
                bitinfo.append({
                    "MEASUREID": mid_seq,
                    "BITNO": 0,
                    "BITNAME": desc.upper(),
                    "TEXTON": ton,
                    "TEXTOFF": toff
                })
        else:
            # analogica
            mid_seq = mid_seq + 1
            priv = "0x"
            priv = priv + struct.pack('<I', regval).hex().upper()
            priv = priv + "00000000"
            priv = priv + "00000000"
            priv = priv + struct.pack('<I', 0).hex().upper()
            priv = priv + struct.pack('<I', mid).hex().upper()
            priv = priv + struct.pack('<I', FMT_FLOAT).hex().upper()
            measures.append({
                "STATIONID": sid,
                "NAME": desc,
                "DISABLED": 0,
                "DIGITAL": None,
                "DOWNLOAD": 0,
                "SNAPSHOT": 1,
                "IGNOREERRORS": 0,
                "LOWCRITICAL": NEGBIG,
                "HIGHCRITICAL": BIG,
                "LOWRANGE": NEGBIG,
                "HIGHRANGE": BIG,
                "LOWOFFSET": NEGBIG,
                "HIGHOFFSET": BIG,
                "SQRAW": BIG,
                "SQ1HOURMEAN": BIG,
                "SQ3HOURMEAN": BIG,
                "SQ8HOURMEAN": BIG,
                "SQDAILYMEAN": BIG,
                "UNITS": units,
                "STANDARDRANGEID": None,
                "DRIVERDATA": 0,
                "TYPE": 0,
                "DRIVERPRIVATE": priv,
                "ONLY_POSITIVES": 0,
                "VM_SOURCE_CODE": VM_DEFAULT,
                "PERIOD": 5,
                "SNAPSIZE": 1000,
                "DRIVERCONFIG": MCFG,
                "ID": mid_seq,
                "UNITS2": units
            })

    # ---------- anagrafica stazione ----------
    drv = "<configuration><commProto><p0 class=\"Protocollo MODBUS (master) via TCP/IP\" "
    drv = drv + "name=\"Protocollo MODBUS (master) via TCP/IP\" "
    drv = drv + "ipaddress=\"" + ip + "\" "
    drv = drv + "tcpport=\"" + str(port) + "\" "
    drv = drv + "timeout=\"5000\" retries=\"3\" write4XXXX=\"6\"/></commProto>"
    drv = drv + "<recoveryProto/></configuration>"
    out.append({
        "NAME": nm,
        "DRIVERNAME": "modbusplc",
        "XPOSITION": 430,
        "YPOSITION": 530,
        "DOWNLOADTYPE": 0,
        "DOWNLOADPROGRAM": None,
        "IGNOREERRORS": 0,
        "SNAPSHOT": None,
        "NORMALSNAPSHOT": 1,
        "CRITICSNAPSHOT": 32767,
        "ALARMSNAPSHOT": 32767,
        "SYNOBITMAP": None,
        "LINENAME": None,
        "AREACODE": None,
        "ADDRESS": None,
        "LINECONFIGURATION": None,
        "TIMELASTCONFIGURATION": None,
        "TIMELASTDOWNLOAD": None,
        "EVENTTIME": None,
        "EVENTCODE": 0,
        "EVENTORIGIN": None,
        "CODE": None,
        "DRIVERPRIVATE": None,
        "OVERWRITEMEASURES": 1,
        "DRIVERCONFIG": drv,
        "ID": sid,
        "measures": measures,
        "bitinfo": bitinfo
    })
    g = g + 1

# ---------- rinomina stazioni omonime con suffisso incrementale ----------
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

# ---------- output (mai vuoto: se out e' vuoto emette DEBUG dettagliato) ----------
# FIX v3: includo metadati diagnostici anche nel caso normale (_meta).
# Se il caso normale ha dei warning (es. IP mancante nel documento), li
# includo in _warnings. Se out e' vuoto, produco un oggetto DEBUG completo.
meta = {
    "chunks_parsed": len(chunks),
    "pages_processed": len(pages),
    "stations_in_input": len(st_in),
    "stations_output": len(out),
    "variables_total": 0,
    "raw_type": str(type(raw)),
    "raw_len": len(s),
    "chunk_types": [],
    "station_details": [],
    "raw_sample": repr(s[:500])
}
# dettaglio chunk types
i = 0
while i < len(chunks):
    meta["chunk_types"].append(str(type(chunks[i])))
    i = i + 1
# conteggio variabili totali + dettaglio stazioni
tv = 0
i = 0
while i < len(st_in):
    st = st_in[i]
    vs = st["variables"]
    tv = tv + len(vs)
    first_desc = ""
    last_desc = ""
    if len(vs) > 0:
        if isinstance(vs[0], dict):
            fd = vs[0].get("description")
            if fd is not None:
                first_desc = str(fd)[:80]
        if isinstance(vs[len(vs)-1], dict):
            ld = vs[len(vs)-1].get("description")
            if ld is not None:
                last_desc = str(ld)[:80]
    meta["station_details"].append({
        "page_no": st.get("page_no"),
        "name": st["name"],
        "ip": st["ip"],
        "port": st["port"],
        "modbus_id": st["modbus_id"],
        "num_vars": len(vs),
        "first_desc": first_desc,
        "last_desc": last_desc
    })
    i = i + 1
meta["variables_total"] = tv

if len(out) == 0:
    head = s[:800]
    dbg = {
        "DEBUG": True,
        "raw_len": len(s),
        "chunks_parsed": len(chunks),
        "pages_processed": len(pages),
        "raw_head": head
    }
    output = json.dumps(dbg, ensure_ascii=False, indent=1)
else:
    # inietta _meta in ciascuna stazione (informazione non invasiva)
    i = 0
    while i < len(out):
        out[i]["_meta"] = meta
        i = i + 1
    # aggiungi _warnings se ci sono
    warnings = []
    if warn_no_ip:
        warnings.append("nessun IP dichiarato nel documento: usato default " + DEFAULT_IP)
    if len(warnings) > 0:
        i = 0
        while i < len(out):
            out[i]["_warnings"] = warnings
            i = i + 1
    output = json.dumps(out, indent=1, ensure_ascii=False)

print(output)
