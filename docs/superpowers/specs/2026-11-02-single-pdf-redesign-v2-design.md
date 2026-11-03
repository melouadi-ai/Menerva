# Single PDF — Redesign v2: estrazione unificata + oracolo per shard

Data: 2026-11-02. Stato: approvato in chat (12 decisioni), da implementare.

## Obiettivo

Risollevare alla radice i difetti aperti del flusso Single PDF:
copertura discontinua, join fragile a 3 rami, stati junk, unità inventate,
refusi corretti, IP fabbricati. Successo = ogni run passa il gate v6
(copertura 100% o scarto motivato, stati esatti, zero junk/invenzioni,
ADAS valido) su tutti gli 8 documenti, in modo ripetibile.

## Vincoli piattaforma (non negoziabili)

- Canvas pytool: standalone, no `def`/`class`/`lambda`, output in `result`,
  paste <34KB (limite empirico: 34.365 rosso, 33.520 verde).
- `{edge}[N]` canvas-local, si spostano a ogni rewiring.
- VLM: layout `{edge.media}[N]` nel Prompt, istruzioni in Powered identity,
  Context vuoto.
- Nessun PyMuPDF sul canvas.
- Parità src ↔ documentata ↔ canvas pinnata da `render_canvas.py`.
- Comunicazione in italiano; prompt e codice in inglese.

## Topologia reale (confermata da screenshot 02/11)

```
LV1:
  1 medex PDF2PNG → 3 medex MEDIA2CONTENT (nkeysgrp=1)
        ├─ #4 → 8 pytool SLICE-A ─┐
        ├─ #5 → 7 pytool SLICE-B ─┤
        └─ #6 → 9 pytool SLICE-C ─┘
             ↓          ↓          ↓
        2 ENGINE A  12 ENGINE A  13 ENGINE A     ← invocano LV2
             ↓          ↓          ↓
        10 pytool MERGE_AB → 11 pytool MERGE_ABC
             ↓
        14 naive (tap) → 4 pytool CONSOLIDATORE
             ├─ #3 → 15 naive (tap)
             └─ #4 → 6 pytool JSON CREATOR → 5 naive (FINALE)

LV2 (sottomotore, invocato da tutti e 3 i motori):
  1 medex CONTENT2MEDIA
        └─ #1 → 2 visiomaru UNIFIED → 3 naive → 4 naive
```

Il LV2 è già convertito a UNIFIED (1 visiomaru, non 3 rami). Il flusso a
3 rami esiste solo nella documentazione, non più sul canvas.

## Le 12 decisioni

| # | Decisione | Scelta |
|---|---|---|
| 1 | Approccio | A — estensione incrementale |
| 2 | Oracolo dove | A2c — VLM su canvas |
| 3 | Oracolo livello | A — per shard (3 chiamate parallele) |
| 4 | Oracolo comportamento | B — rapporto + correzioni automatiche |
| 5 | Oracolo potere | A — solo aggiungi/annulla, mai sovrascrive |
| 6 | Refusi | A — fedeltà assoluta, oracolo segnala senza toccare |
| 7 | IP/stazioni | A — regola S5 esplicita + oracolo segnala, nessuna stazione inventata |
| 8 | Scope | A — completo (tutto in una volta) |
| 9 | Lentezza | sharding in 3 parti già esistente (A/B/C paralleli) |
| 10 | Chunking | fisso (già fatto: SLICE-A 1-10, B 11-20, C 21-fine) |
| 11 | Oracolo topologia | A — dentro LV2, 2° visiomaru in parallelo al primo |
| 12 | oracle_apply | A — dentro il consolidatore (nodo 4) |

## Architettura target

```
LV2 (sottomotore, invocato da tutti e 3 i motori):
  1 medex CONTENT2MEDIA
        ├─ #1 → 2 visiomaru UNIFIED ──┐
        │                             │
        └─ #2 → 5 visiomaru ORACOLO ←─┘  (immagine + output UNIFIED)
                    ↓
              3 naive (assemblatore: {estrazione, verifica})
                    ↓
              4 naive (uscita LV2)
```

Cosa cambia sul canvas:
1. **LV2**: aggiungi un 2° visiomaru `ORACOLO` (nodo 5) che riceve la stessa
   immagine (`{edge.media}[1]`) + l'output di UNIFIED (edge interno).
   Modifichi il naive 3 perché assembla `{estrazione, verifica}`.
2. **LV1**: invariato — slicer, motori, merger, consolidatore, creator
   restano dove sono.
3. **Consolidatore**: separa `estrazione` da `verifica` nel payload
   aggregato, consolida l'estrazione come oggi, applica le correzioni
   della verifica (aggiungi/annulla solo) con audit trail.

## Componenti nuovi

### 1. Prompt oracolo `vlm_oracle_v1.md`

Il VLM-oracolo riceve:
- L'immagine della pagina (stessa di UNIFIED)
- L'output UNIFIED della pagina (JSON con le variabili estratte)

Deve produrre un JSON di difetti:
```json
{
  "page_no": int|null,
  "mancanti": [
    {"description": str, "registro": int|null, "bit": int|null,
     "evidenza": str}
  ],
  "unita_inventate": [
    {"description": str, "unita": str, "evidenza": str}
  ],
  "junk_stati": [
    {"description": str, "campo": "state_on"|"state_off",
     "valore": str, "evidenza": str}
  ],
  "refusi_corretti": [
    {"description_finale": str, "description_pdf": str,
     "evidenza": str}
  ],
  "ip_dichiarati_non_usati": [
    {"ip": str, "evidenza": str}
  ]
}
```

Regole:
- **Mai sovrascrivere**: l'oracolo segnala, non corregge.
- **Fedeltà**: se il FINALE ha `Ossigeno` ma il PDF dice `Ossiegno`,
  warning `refuso_corretto` con evidenza, non correzione.
- **Unità**: se il FINALE ha `mg/m3` ma il PDF non ha unità, warning
  `unita_inventata`.
- **Junk**: se lo stato è `"1"`, `"0"`, `"1=…"`, `"0=…"`, warning `junk_stato`.
- **Mancanti**: se il PDF ha una riga che non è nel FINALE, warning
  `mancante` con evidenza.
- **IP**: se il PDF dichiara un IP che non è nel FINALE, warning
  `ip_dichiarato_non_usato`.

### 2. Oracle apply nel consolidatore

Dopo aver consolidato l'estrazione, il consolidatore:
1. Riceve la `verifica` (JSON difetti) della stessa pagina.
2. Per ogni difetto:
   - `mancanti`: **aggiunge** la variabile (verbatim dal PDF, con
     `_audit_oracolo: {"azione": "aggiunta", "evidenza": "..."}`).
   - `unita_inventate`: **annulla** l'unità (`units = null`, con
     `_audit_oracolo: {"azione": "annullata", "campo": "units",
     "evidenza": "..."}`).
   - `junk_stati`: **annulla** lo stato (`state_on/off = null`, con
     `_audit_oracolo`).
   - `refusi_corretti`: **non tocca** (fedeltà), solo warning.
   - `ip_dichiarati_non_usati`: **non tocca** (nessuna stazione inventata),
     solo warning.
3. L'audit trail è nel FINALE: ogni variabile toccata dall'oracolo ha
   `_audit_oracolo`.

### 3. Gate v6

Estensione del gate v5 con:
- **§16. Oracolo**: ogni correzione oracolo deve essere verificabile
  contro il PDF. Se l'oracolo aggiunge una riga che nel PDF non c'è,
  è un'invenzione e il gate la blocca.
- **§17. Audit trail**: ogni variabile con `_audit_oracolo` deve avere
  `evidenza` non vuota.
- **§18. Refusi**: i refusi corretti dal VLM sono warning, non errori.
  Il gate li conta ma non li blocca.

## File da creare/modificare

### Creare
- `src/prompts/vlm_oracle_v1.md` — prompt oracolo
- `myhydra/single_pdf/platforms/lv2/prompts/current/vlm_oracle_v1.md` — copia
- `myhydra/single_pdf/prompt/vlm_oracle_v1.md` — copia
- `tests/test_single_oracle.py` — test oracolo
- `tests/test_single_oracle_apply.py` — test apply nel consolidatore

### Modificare
- `src/nodes/single_consolidator.py` — separa `estrazione`/`verifica`,
  applica correzioni
- `myhydra/single_pdf/pytools/consolidator.py` — stesso
- `myhydra/single_pdf/pytools/consolidator_canvas.py` — rigenerare
- `myhydra/single_pdf/nodes/lv2_02_vlm_parsing_json_principale.md` —
  scheda nodo aggiornata (2 visiomaru)
- `myhydra/single_pdf/nodes/lv1_04_consolidatore.md` — scheda nodo
  aggiornata (apply oracolo)
- `myhydra/single_pdf/verifica_pdf/BENCHMARK_GATE.md` — gate v6
- `myhydra/single_pdf/pytools/README.md` — hash aggiornati
- `myhydra/single_pdf/platforms/lv1/scripts/updated_pending_validation/README.md` — hash

### Archiviare
- `myhydra/single_pdf/platforms/lv2/prompts/history/vlm_measures_v18.md`
- `myhydra/single_pdf/platforms/lv2/prompts/history/vlm_bitnames_v16.md`
- `myhydra/single_pdf/platforms/lv2/prompts/history/vlm_bitstates_v19.md`

## Test

- `test_single_oracle.py`: prompt oracolo ha le regole giuste, copie
  byte-identiche.
- `test_single_oracle_apply.py`: consolidatore applica aggiungi/annulla
  correttamente, audit trail presente, mai sovrascrive.
- `test_single_consolidator_canvas.py`: parità AST, budget <34KB.
- `test_single_canvas_hygiene.py`: hash README aggiornati.
- Suite completa: `./run_tests.sh` + `./run_tests.sh double` verdi.

## Verifica

- Run su SIEMENS_2 con il nuovo LV2 (UNIFIED + ORACOLO) → verdetto.
- Target: ≥235/431, 0 buchi reali, 0 invenzioni, 0 ADAS-invalidi.
- Se il verdetto è peggiore della baseline, analizzare i warning e
  rafforzare il prompt.

## Rischi

- **Oracolo VLM che verifica VLM**: stesso rischio di sotto-campionamento.
  Mitigato da: 1 giro = 1 pagina (massima precisione), checklist come
  secondo segnale indipendente.
- **Consolidatore vicino al limite 34KB**: l'apply oracolo è compatto,
  test di budget lo pinna.
- **Refusi**: l'oracolo non li corregge (fedeltà), solo li segnala.
  Il gate li conta ma non li blocca.
