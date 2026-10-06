# Single PDF redesign — design spec (approccio A)

Data: 2026-10-06. Stato: approvato a sezioni in chat, da rivedere su file prima del piano.

## 1. Intento condiviso

Riprogettare il flusso Single PDF da zero restando su MyHydra, riusando l'architettura
verificata del Double PDF. Criterio di successo primario: copertura verificabile —
ogni riga nominata del PDF finisce in ADAS oppure in un report di scarto motivato,
niente perdite silenziose. Perimetro: tutti i formati noti (SMA, PROTEC, SIEMENS)
con le loro convenzioni diverse. Comunicazione in italiano; prompt VLM e codice in inglese.

## 2. Vincoli non negoziabili (da AGENTS.md ed episodi canvas)

- Pytool standalone: solo inline, niente `def`/`class`/`lambda`, output in `result`,
  niente `import src.*`, validazione Pydantic saltata sul canvas per disegno.
- Paste canvas sotto ~32 KB (budget interno 28 KB); oltre il nodo va rosso.
  Copia documentata + copia canvas senza commenti, test di parità AST+output, mai hand-edit.
- `{question}` = input iterazione; `{edge}[N]` testuale e `{edge.media}[N]` con N
  canvas-locale da ricontrollare dopo ogni rewiring; rimuovere match-condition spurie
  (caso `pippo`) che affamano l'injection senza errore.
- Riga non-Python = SyntaxError a compile, `result` mai assegnato, downstream blank
  senza ERROR JSON: serve pulizia del paste + `try/except` di runtime con ERROR JSON.
- Utente senza tap/debug sui nodi (timeout): diagnosi solo via self-check
  (`_warnings`, `_meta`, `review`) su output incollabili.
- `src/` autoritativo; copie `myhydra/` byte-identiche con sha256 nei README.
  Script/prompt passati all'utente sempre come file completo, nodi per nome esatto,
  righe debug marcate `DEBUG`.
- Venv `.venv` per test; `pyproject testpaths=["tests"]`.

## 3. Approcci considerati

- A. Portare il Double nel Single (scelto): VLM a 3 rami, consolidatore, JSON CREATOR slim,
  join per TAG, carry-over, copie canvas con parità, self-check. Più nodi da igienizzare,
  ma meccanismi già verificati sui casi 6 e 7.
- B. Single snello + guardie (scartato): meno rewiring, ma il VLM unico resta il collo
  di bottiglia sulle pagine dense e le unità restano perse senza join TAG.
- C. Micro-batch a finestre (rinviato): solo come fase 2 se i test mostrano troncatura
  VLM su pagine dense.

## 4. Sezione 1 — Architettura e flusso nodi (approvata)

LV1: `pdf2png` → `media2content` (`nkeysgrp:1`, stateless) → motore iterativo
1 giro/pagina → consolidatore (nuovo, come nodo 11 Double) → `JSON CREATOR` slim → output.
Merge nel consolidatore (ADR-001 Opz.B: merge early, transform late).
LV2 per pagina: `content2media` → 3 VLM paralleli (misure+dati tecnici / nomi bit / stati)
→ etichettatori → assemblatore di pagina. Filtri LV1 prima delle iniezioni: scarti
motivati e conteggiati, mai silenzio. Contratto motore→consolidatore: un chunk per
pagina con `page_no`; il consolidatore denuncia buchi in `_warnings`.

## 5. Sezione 2 — Contratti e schema intermedio (approvata)

Unico schema intermedio versionato Single=Double. Per variabile: `description` esatta,
`units` solo da colonna Units, `modbus_register`, `bit` 0–15, `kind`, `data_type`,
`read_write`, `state_on/off` solo copie, più `zona` (conservata per filtri/report, mai
come nome), `tag` (join scale), `pagina`+`riga` (copertura). Decisioni cliente come
config esplicita: zeri iniziali, regola V2 (`Riserva INPUT`), nome stazione (default
`SME` solo se nessun IP), BISON/limiti/divisori (il resto in `review` coi nomi).
Consolidatore: join scale per `tag`, carry-over registro con `registro_applicato`, fold
singoli condivisi in packed. JSON CREATOR: solo trasformazione deterministica
(150/250 da `data_type`, `DRIVERDATA`/`TYPE`, `DRIVERPRIVATE` 48 hex); V19 vince su P5
— niente rimozione di parentesi con contenuto. Output: lista stazioni con
`_meta`+`_warnings` a tassonomia fissa.

## 6. Sezione 3 — Prompt VLM a 3 rami (approvata)

Ramo misure (con `tag` + self-check BIT), ramo nomi-bit (registro+bit+descrizione,
fedeltà V23/V26: mai rinumerare — lezione del bit 40014), ramo stati (solo dove
dichiarati, altrove `null`, stati keyword restano compito dichiarato del pytool).
Scarti unificati e contati: V2, V20 (`NO PC SME`), V21 (`_HW`). Layout invariati
e già verificati: `{edge.media}[N]` solo in Prompt + istruzioni in Powered identity
+ Context vuoto, oppure legacy inline.

## 7. Sezione 4 — Pytool e robustezza canvas (approvata)

Split consolidatore/JSON CREATOR sotto 28 KB, copie canvas + parità, checklist
edge-settings dopo rewiring, ERROR JSON di runtime, self-check in output.
Dettagli ADAS: `DRIVERPRIVATE` 48 hex registro in prima word, 150/250 da `data_type`,
`NAME` troncato a 49, sentinel `±3.40282e38` = nessun limite.

## 8. Sezione 5 — Copertura e verifica (approvata)

Verità dal PDF per famiglia (metodo `test_adas_caso6/7_pdf_truth`), fixture
`observed_` + regressione errori legacy noti; confronto GT mai riallineato senza PDF.
Fix `confronta.py`: match su `(stazione, registro, bit)`; classi
`ok`/`saltata_da_regola`/`scelta_di_progetto`/`difetto`. Guardia copertura
(stesso `page_no` + soglia) e linkage misure→bitinfo. Report KPI riscritto senza
claim insostenibili; punti Single noti da chiudere: V3 con `Unità` fra esempi,
fedeltà refusi con test, niente `127.0.0.1` fabbricato, `registro_suggerito` anche Single.

## 9. Sezione 6 — Organizzazione e ordine (approvata)

Struttura `platforms/` anche per il Single (`prompts/current|history`,
`scripts/in_use|updated_pending_validation|parked`, sha256 nei README).
Ordine: (1) schema, (2) prompt 3 rami, (3) consolidatore, (4) JSON CREATOR + canvas,
(5) verità + `confronta.py`, (6) import ADAS reale + documento mai visto.
Domande cliente (BISON, zeri, V2, stazione) in parallelo come config.

## 10. Self-review dello spec

- Placeholder: nessuno; ogni sezione ha artefatti e criteri.
- Coerenza: V19 vince su P5 in sezioni 2 e 5; `_HW` scartato ma contato (sez. 2–3);
  validazione canvas saltata ma linkage verificato (sez. 4–5).
- Scope: un solo piano di implementazione; micro-batch esplicitamente fase 2.
- Ambiguità: `tag` definito come chiave di join trascritta dal VLM (sez. 2–3);
  soglia copertura da tarare sui volumi SMA/SIEMENS in implementazione.
