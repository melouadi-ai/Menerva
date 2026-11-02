# Brief di redesign — flusso Single PDF (da passare a un'AI)

> Documento di lavoro per ripensare da capo il flusso Single PDF.
> Lingua: italiano per il ragionamento; prompt VLM e codice restano in inglese.
> Data di riferimento: 2 nov 2026. Basato su AGENTS.md, PENDENZE.md, src/, myhydra/single_pdf/.

## 1. Missione

Il flusso **Single PDF** converte un PDF di mappatura PLC/SCADA (tabelle Modbus con stazioni, misure analogiche/digitali, bit impacchettati, unità, scale, limiti, stati TEXTON/TEXTOFF) in un JSON conforme al database **ADAS** (stazioni + misure + bitinfo), importabile sulla piattaforma.

L'obiettivo del redesign: ripensare l'architettura **da capo**, non fare patch. L'AI che riceve questo brief deve proporre una nuova struttura (pipeline, contratti, prompt, trasformazioni, verifica) che risolva i difetti noti e i vincoli della piattaforma, mantenendo il risultato atteso (copertura 100% delle righe del PDF, registri corretti, nessun inventato).

## 2. Contesto piattaforma (vincoli non negoziabili)

- **MyHydra canvas**: nodi Python ("pytool") eseguiti come script standalone, inline, **senza `def`/`class`/`lambda`**. Output assegnato alla variabile `result` (o `print(output)`). Non possono importare `src.*` in produzione (pydantic validation viene saltata, pipeline identica). Paste **sotto ~32 KB** (34.365 byte rosso, 26.731 verde).
- Input tra nodi: `{question}` = iterazione corrente; `{edge}[N]` = output testuale di un altro nodo. Gli edge possono avere **match conditions** residue che bloccano il wire in silenzio.
- VLM nodes: due layout verificati (prompt singolo con `{edge.media}[N]` inline; split layout con Prompt solo media, istruzioni in Powered identity, Context vuoto). I gusci vuoti erano problema input Medex, non layout.
- L'utente **non può toccare nodi né usare debugger** (timeout). Le diagnosi devono essere self-check nell'output (`_warnings`, `_meta`, `review`).
- `src/` è autoritativo; copie in `myhydra/` devono essere byte-identiche con hash documentato. `legacy/` read-only.
- Python 3.10, venv `.venv`. Test: `./run_tests.sh` (root, 193 test), `./run_tests.sh double` (82), `all`. Pydantic optional su canvas.

## 3. Architettura attuale (Single PDF)

### 3.1 Pipeline LV1 (redesign v14/v15)

```
LV1-01 pdf2png --> LV1-02 media2content --> LV1-03 SINGLE PDF ENGINE (iterativo, 1 giro/pagina)
    --> LV1-04 CONSOLIDATORE (nuovo) --> LV1-05 JSON CREATOR --> JSON ADAS
```

Ogni giro del motore invoca il Livello 2 su una pagina e accumula il chunk.

### 3.2 Livello 2 (per pagina, 3 rami VLM)

- `content2media` (conversione)
- VLM ramo **misure + dati tecnici** (prompt `vlm_measures_v18.md`)
- VLM ramo **nomi bit** (prompt `vlm_bitnames_v16.md`)
- VLM ramo **stati TEXTON/TEXTOFF** (prompt `vlm_bitstates_v19.md`)

I 3 rami producono JSON intermedio per pagina, uniti dal consolidatore sulla chiave `riga`.

### 3.3 Consolidatore (`src/nodes/single_consolidator.py`)

- Join dei 3 rami per pagina su `riga`; precedenze: nomi-bit vince bit/registro solo a descrizioni concordi; misure tutto il resto; stati vince state_on/off solo a descrizione concorde; `riga_mismatch` sempre se gli insiemi divergono.
- Join scale per `tag` (solo riempimento null).
- Carry-over registro per stazione in ordine di pagina (`registro_applicato`).
- Fold packed (singoli con registro condiviso → IMPACCATO).
- Filtri V2/V20/V21 inline (scarti contati, mai silenzio).
- Merge stazioni per (nome, ip); placeholder mai fusi.
- Bit 1-based page handling (`bit_offset_pagina`).
- Output: `{"stations", "warnings", "counters"}`.

### 3.4 JSON Creator (`src/nodes/json_creator.py` v15)

Trasforma intermedio → ADAS: merge stazioni per IP, calcolo DRIVERPRIVATE hex (48 char), XML DRIVERCONFIG, rinumerazione ID, VM_SOURCE_CODE, campi fissi, warning di copertura/zeri/limiti/divisioni/linkage.

### 3.5 Filtri (`src/nodes/single_filters.py`)

`classify_row_with_reason`: V2 (spare/header esatti), V20 (annotazioni), V21 (zone hardware). Precedenza V2 > V21 > V20.

### 3.6 Modelli (`src/models/vlm_schema.py`, `validators.py`)

Pydantic: Variable, Station, VLMOutput, MeasureADAS, BitInfoADAS, StationADAS, ADASOutput. `safe_validate_vlm` con retry. Campi extra ignorati (default pydantic) perché il creator legge `Division`/`Division_value`.

### 3.7 Motore iterativo (LV1-03)

Un giro per pagina. **Mai verificato su PDF reale** come aggregazione (rischio #1 ADR-001). Il creator è difensivo (accetta 4 formati di ingresso).

## 4. Contratti

### 4.1 Intermedio (VLM)

Schema in `docs/contracts/VLM_INTERMEDIATE.md` (stale: dichiara v11 come riferimento). Campi: stations (name, protocol, ip, port, modbus_id, variables[] con description, units, modbus_register, bit, data_type, kind, read_write, state_on/off, scale_*, limit_*, zona, tag, pagina, riga).

### 4.2 ADAS finale

Schema in `docs/contracts/ADAS_FINAL.md` (stale e in conflitto col codice, vedi D2): dice oggetto stazione singolo, DRIVERPRIVATE 52 char, registro ultimo blocco, ecc. Il codice emette lista di stazioni, 48 char, registro primo blocco.

### 4.3 Mismatch contratto/codice noti (PENDENZE D2)

| Punto | Contratto | Codice |
|---|---|---|
| Lunghezza DRIVERPRIVATE | 52 | 48 |
| Primo blocco 8 hex | tipo misura | solo registro, little-endian |
| Posizione registro | ultimo blocco | primo blocco |
| Quarta word | non descritta | sempre 00000000 |
| Misure con IP placeholder | scartate, IP reale primario | sempre stazioni separate, mai scartate |
| Forma output | oggetto stazione singolo | lista di stazioni |

## 5. Difetti noti (da PENDENZE + AGENTS)

### Blocco A — bloccanti (stato attuale)
- **A1 Avviso copertura mai attivabile**: guardia `len(pages)>1 and len(chunks)==1` falsa per costruzione. Risolto v4.4 con segnale "più stazioni stesso page_no + volume >100". (Ora chiuso, ma architettura fragile.)
- **A2 Copia pytool in myhydra/ non allineata**: risolto 5/10.
- **A3 Fixture storiche contengono il difetto v4.3** (6 misure DRIVERPRIVATE a zero su SMA_1): da mantenere come baseline.

### Blocco B — difetti dal confronto
- **B1 Zeri iniziali negli indirizzi**: `00033` (digitali) vs `40001` (analogiche) nello stesso PDF; normalizzazione produce 33 ≠ 40033. Avviso aggiunto, conversione è decisione di dominio. Da decidere col cliente.
- **B2 IP dichiarati e mai usati**: PROTEC_1 dichiara 2 IP usa 1; PROTEC_2 dichiara 3 usa 1; SIEMENS_2 dichiara 5 + subnet mask. Causa: prompt, non pytool (regola S5 "una stazione per IP" letta come "solo dove ho variabili"). Subnet mask non filtrata.
- **B3 Perdita copertura SIEMENS_2**: 1116 righe PDF, 274 variabili ricevute dal pytool, 251 prodotte. `_meta.chunks_parsed=1` su 29 pagine → accorpamento. Attribuzione a VLM dedotta, non osservata. Ora motore iterativo invia 1 richiesta/pagina (ADR-001 Opzione B), quindi accorpamento strutturalmente escluso; resta da verificare con nuova pipeline.

### Blocco C — verifiche non riproducibili
- **C1 SIEMENS_2 non validato**: copertura discontinua (alcune pagine intere scoperte). Non distinguibile perdita pipeline vs estrattore.
- **C2 Regola V2 e nomi prefissati**: output scarta anche `Riserva INPUT` (129 righe su SIEMENS_2) ma regola dice esatto. Da decidere col cliente.
- **C3 `data_type` mai esercitato**: nessuna fixture con campo data_type; regola V25 (formato 150 vs 250) mai provata su dati reali.

### Blocco D — igiene
- **D1 Comandi test non standard**: `pyproject.toml` testpaths=["tests"]; pymupdf solo nel venv.
- **D2 Contratti in conflitto col codice** (vedi 4.3).
- **D3 Refuso nel documento, non nel VLM**: PROTEC_1 riga `40001.2` ha `Rchiesta Mnautenzione` nel PDF (refuso reale); legacy lo ha corretto di nascosto. Nota in `test/caso_2_protec_1/README.md` ancora opposta.

### Osservazioni AGENTS (Single PDF, verificate 5/10)
- **`UNITS: "Unità"`** emesso su misura `Polveri (GR)` (reg 40008): la cella contiene `mg/Nm³`, "Unità" è intestazione di sottocolonna. Causa: V3 del prompt v13 elenca `"Unità"` tra esempi di unità valide → insegna l'errore. GT legacy ha lo stesso bug.
- **Refuso corretto contro V13**: `Allarme 1 Ossiegno umido` → `Ossigeno` nel PDF; noi correggiamo, legacy no. Comportamento incoerente (D3 dice che su PROTEC_1 il refuso è stato rispettato): affidabilità VLM, serve test dedicato.
- **I 2 "difetto" di SMA_1 nel verdetto sono falsi positivi**: `verifica_pdf/confronta.py` confronta per registro ignorando stazione, e 40001 compare in due tabelle diverse. Noi le separiamo correttamente.
- **`DATA_TYPE` → formato**: SIEMENS_2 dichiara `INT16` e noi emettiamo 150 su 21 misure, legacy 250 su tutte. Chiude C3 con evidenza reale.
- **Copertura SIEMENS_2**: 104 misure contro 339 del legacy su 1116 righe; 129 righe non coperte. B3/C1, a monte dell'estrazione, non difetto del pytool.
- **B2 più grave del scritto**: PROTEC_1 dichiara 2 IP e ne usa 1, PROTEC_2 dichiara 3 e ne usa 1; in entrambi viene emesso `127.0.0.1` come default, cioè IP fabbricato. (Nota: in v15 B2 è stato corretto a "mai IP fabbricato, warning + vuoto".)
- **Carry-over del registro assente nel prompt Single** (V4 dice cella vuota → null): mai manifestatosi sui 4 documenti noti, ma buco latente.

### Decisioni aperte per il cliente
- B1: `00033` è indirizzo HMI o registro Modbus con zeri di formattazione?
- B2: regola prompt per IP multipli sulla stessa pagina.
- C2: regola V2 esatta vs prefissi.
- Nome stazione variabile per run (Single: `Sistema Analisi Emissioni` vs `SME`).
- BISON, zeri iniziali, regola V2 (condivisi col Double).

## 6. Test e verifica

- Root: `tests/test_casi_reali.py` (12 passed, 0 failed), `test_multipage.py` (33 passed).
- Verità PDF: `tests/test_adas_caso6_pdf_truth.py` (confronta `reg_raw - 40000`), `myhydra/double_pdf/tests/test_adas_caso7_pdf_truth.py`.
- Confronto con GT legacy: `tests/compare_with_gt.py` (GT ha errori propri: 18 bitinfo fantasma, 2 registri comandi sbagliati, TEXTON disallineati, QAL3 INT scritti 250 invece di 150, nomi troncati). **Le differenze col GT non vanno colmate senza verifica sul PDF.**
- Metodologia: `tests/test_adas_caso6_pdf_truth.py` fissa tabella verità e registra dove il legacy sbaglia (`test_legacy_ha_errori_noti_il_nostro_no`).
- Verifica PDF: `myhydra/single_pdf/verifica_pdf/confronta.py` (usa pymupdf, eseguire con `.venv/bin/python`).
- Canvas hygiene: `tests/test_single_canvas_hygiene.py`, test di parità AST+output.
- Verdetto finale: `myhydra/single_pdf/verifica_pdf/verdetto_finale.py`.

### Fixture
- Input: `data/test_inputs/Mappatura_{1..4}_Cliente_{SMA_1,PROTEC_1,PROTEC_2,SIEMENS_2}.json` (intermedio), PDF in `myhydra/single_pdf/PDFs per il confronto/`.
- Output storici: `tests/single_pdf_outputs/`, `myhydra/single_pdf/Outputs MYHYDRA/`.
- Observed (sanitized runtime): `tests/single_pdf_outputs/`, nomi `observed_`/`expected_`.

## 7. Cosa il redesign deve produrre

L'AI deve proporre (e, su approvazione, implementare) almeno:

1. **Architettura pipeline** (nodi, responsabilità, contratti I/O) con decisione su:
   - motore iterativo (1 giro/pagina) vs sharding (già previsto in LV1 con slicer/merger) e gestione errori/retry/timeout per pagina;
   - dove vive il merge dei rami (consolidatore separato vs creator);
   - come si gestiscono documenti multi-pagina e stazioni multi-IP.
2. **Contratto intermedio v15+** (schema, validazione, campi) e **contratto ADAS finale** allineato al codice (correggere D2).
3. **Strategia prompt VLM** (uno o più rami; regole V2/V20/V21/V19; gestione refusi, unità, zeri, IP multipli, nomi prefissati) con versioning e hash.
4. **Trasformazioni deterministiche** (DRIVERPRIVATE, XML, merge, fold, carry-over) con spec esatta e test.
5. **Self-check** nell'output (`_warnings`, `_meta`, `review`) per diagnosi senza debugger.
6. **Verifica** (test unit + truth PDF + confronto) e procedura di validazione su canvas.
7. **Vincoli canvas** rispettati: standalone, no def/class/lambda, <32KB, edge indices verificati, match conditions rimosse.

### Domande aperte da porre al cliente (non decidere per convenienza)
- B1 (zeri iniziali), B2 (IP multipli), C2 (prefissi V2), nome stazione, BISON/zeri/regola V2, unità (°C come null?).

### Cosa NON toccare
- `legacy/` (read-only).
- Non colmare differenze col GT senza verifica sul PDF.
- Non trattare `°C` come dato mancante da recuperare (decisione di dominio).
- Non mescolare copie Single/Double del creator (edge index diverso).

## 8. Riferimenti rapidi

- AGENTS.md (root) — vincoli, stato, difetti.
- `myhydra/single_pdf/PENDENZE.md` — registro lavoro.
- `myhydra/single_pdf/platforms/lv1/README.md` — catena e script.
- `myhydra/single_pdf/nodes/lv1_03..05*.md` — schede nodi.
- `myhydra/single_pdf/flusso_cloud_osservato.md` — flusso cloud osservato.
- `docs/contracts/VLM_INTERMEDIATE.md`, `docs/contracts/ADAS_FINAL.md`.
- `docs/architettura/ADR-001-merge-multi-page.md` (se presente).
- `src/nodes/json_creator.py`, `src/nodes/single_consolidator.py`, `src/nodes/single_filters.py`.
- `src/models/vlm_schema.py`, `src/models/validators.py`.
- `src/prompts/vlm_extraction_v13.md`, `vlm_measures_v18.md`, `vlm_bitnames_v16.md`, `vlm_bitstates_v19.md`.
- `myhydra/single_pdf/pytools/` — copie canvas.
- `tests/` — suite.

## 9. Checklist per l'AI che ripensa

- [ ] Leggere AGENTS.md + PENDENZE.md + questo brief.
- [ ] Esplorare src/, tests/, myhydra/single_pdf/ (nodes, platforms, pytools, prompt).
- [ ] Identificare i 3-5 problemi strutturali (non solo bug) e proporre 2-3 approcci con trade-off.
- [ ] Presentare design in sezioni, approvazione utente dopo ogni sezione.
- [ ] Scrivere spec in `docs/superpowers/specs/YYYY-MM-DD-single-pdf-redesign-design.md`.
- [ ] Self-review spec (placeholder, consistenza, scope, ambiguità).
- [ ] Review utente.
- [ ] Piano implementazione via writing-plans (non altri skill).
- [ ] Rispettare vincoli canvas e test.

---

**Nota finale**: questo brief è un punto di partenza, non una specifica. L'AI deve interrogare l'utente sulle decisioni aperte (B1, B2, C2, ecc.) prima di fissare scelte irreversibili.
