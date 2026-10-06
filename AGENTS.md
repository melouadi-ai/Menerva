# AGENTS.md — Menerva MAS

Python 3.10. This repo converts PLC/SCADA mapping PDFs into ADAS JSON (Single PDF flow live on a cloud platform; Double PDF IOL+JOB flow in development). The cloud canvas config is NOT fully in this repo — docs describe visible nodes, not their internals.

## Environment: always use the venv

System `python3` lacks dependencies (`pymupdf` missing). Never use it.

```sh
.venv/bin/python -m pytest -q                            # root suite, 13 tests
.venv/bin/python -m pytest myhydra/double_pdf/tests -q  # 33 tests, NOT collected by default
```

`pyproject.toml` sets `testpaths = ["tests"]`, so the Double PDF suite only runs with the explicit path. Ruff (`line-length = 100`, `py310`) is in the venv but nothing enforces it — no CI, no pre-commit.

## Source of truth hierarchy

- `src/` is authoritative. Copies under `myhydra/` (prompts, pytools) must stay **byte-identical**; each has a README with the expected sha256. If hashes diverge, `src/` wins — recopy the file and update the hash.
- `legacy/` is read-only reference material. Never modify it; new work goes in `myhydra/`.
- Docs can be stale — the root README says so explicitly. `data/test_inputs/`, `data/test_outputs/`, and `tests/*/outputs/` contain mixed-provenance files: check a file's role before using it as ground truth. Fixture names starting with `observed_` are pasted runtime outputs (sanitized), `expected_` are derived.

## MyHydra script constraints (non-negotiable on canvas)

Pytool scripts pasted into MyHydra nodes must be standalone: inline code only, **no `def`/`class`/`lambda`**, output assigned to the `result` variable. They cannot import `src.*` — pydantic validation is skipped by design on the platform (`_pydantic_available = False`, pipeline continues identically). Paste clean: a stray non-Python line (e.g. an annotation like `riga 5` copied from chat) is a compile-time SyntaxError — `result` is never assigned, the node exposes nothing and downstream starves **silently** (blank output, not even an ERROR JSON, because `try/except` never runs).
Keep pasted scripts **under ~32 KB**: on 6 Oct 2026 a 34,365-byte paste turned node 12 red while the 32,766-byte predecessor passed and a 26,731-byte AST-identical copy passes. If a script outgrows the limit, ship a comment-stripped canvas copy with a parity test (same AST, same output on fixtures), never hand edits.

- `{question}` = current iteration input; `{edge}[N]` = another node's text output (`N` is canvas-local, re-check after rewiring). **Edges can carry match conditions**: a leftover placeholder condition (seen: `pippo` on a filter→injection edge) silently blocks the wire — the downstream injection starves with no error. After any rewiring, inspect edge settings and remove stray conditions.
- VLM nodes: two verified working layouts — legacy single Prompt field with instructions **and** `{edge.media}[N]` inline (legacy screenshots show `[19]`–`[23]`), and the split layout (`{edge.media}[N]` alone in Prompt, instructions in Powered identity, Context empty; verified 2 Oct 2026 with `image_readable: true`). The empty shells were a Medex input problem, never a field-layout problem.

## Before starting work

Read the current work-state file for the area: `myhydra/single_pdf/PENDENZE.md`, `myhydra/double_pdf/WORKFLOW_DESIGN.md`. Node cards live in `myhydra/*/nodes/` (`lv1_`/`lv2_` prefixes); Double PDF copy-paste material is organized per subplatform in `myhydra/double_pdf/platforms/` (`prompts/current/` vs `prompts/history/`, `scripts/in_use/` vs `updated_pending_validation/` vs `parked/`).

When passing a script or prompt change to the user, always paste the **complete file** with changes applied — never a single line or fragment. They copy-paste into the MyHydra canvas, so fragments slow them down. Mark temporary/debug lines with a `DEBUG` comment so they can be reverted.

Always refer to canvas nodes by their **exact node names** (e.g. `FILTER_MEASUREMENT_TECHNICAL_DATA`, not "the measurement filter"). When providing a prompt, always give the **raw markdown** ready to paste.

Always communicate with the user in **Italian**. VLM prompts and code stay in English (technical artifacts); everything else — chat, docs, commit messages — in Italian.

Sync habit in this repo is `sync.sh`: `git pull origin main`, `git add .`, timestamp commit, `git push origin main`.

## Vincolo operativo utente (6 ott 2026)

- L'utente **non può fare tap sui nodi né usare il debugger** sul canvas MyHydra: va in timeout.
- Non chiedere mai ispezioni via tap/debug. Chiedere solo output già incollabili (testo/JSON completo) o conferme su edge/nomi nodi.
- Le diagnosi devono funzionare con self-check dentro l'output (`_warnings`, `_meta`, `review`) invece che con ispezioni live.

## Confronto con il legacy: il GT non è un riferimento di qualità

`tests/compare_with_gt.py` confronta output vs `data/test_outputs/gaia_doublefile_result_6.json`, ma il legacy **ha errori propri**: letto riga per riga, `Mappatura_6_Cliente_SMI_1.pdf` dà 22 misure e **60** bitinfo, il GT ne ha 78. In dettaglio: 18 bitinfo fantasma (12 su righe senza TITOLO, più `PM-2601A/B` e i 4 ventilatori duplicati), due registri comandi sbagliati (430/431 invece di 431/432, shift di una riga su una riga bianca trattata come misura), `TEXTON` disallineati di una posizione, `QAL3` da `INT` scritti 250 invece di 150, e i nomi `STIMATA SO2`/`… ARI` troncati.

Conseguenza: **le differenze di un confronto col GT non vanno colmate senza verifica sul PDF.** Il metodo è in `tests/test_adas_caso6_pdf_truth.py`, che fissa la tabella verità e registra anche dove il legacy sbaglia (`test_legacy_ha_errori_noti_il_nostro_no`), così nessuna correzione futura li riporta indietro per allineamento.

Attenzione anche alle unità: nel PDF IOL del caso 6 **non esiste la colonna unità**. `mg/Nm3` e `°C` nel GT sono inferenze del legacy; noi emettiamo `mg/Nm3` solo dove la scala SO2 è dichiarata e `null` altrove. Non trattare `°C` come un dato mancante da recuperare: è una decisione di dominio (vedi `reports/CONFRONTO_QUALITA_LEGACY_VS_ATTUALE.md`).

## Stato attuale (5 ott 2026)

- Single PDF: prompt v13 + `src/nodes/json_creator.py` v4.4 (A1 soglia 100, A2 copia `myhydra/` allineata). Registro in `myhydra/single_pdf/PENDENZE.md`.
- Double PDF: catena LV1→LV2→consolidatore→ADAS verificata end-to-end sui casi 6 e 7 con Qwen 3.8. Caso 6 ha il **verdetto completo** (run4: 22 misure + 60 bitinfo, 100% del PDF; PM-302A/B ai bit 1/2; TEXTON da keyword). Fixture `tests/double_pdf_outputs/observed_adas_case6_qwen38_run4.json`, tabella verità `tests/test_adas_caso6_pdf_truth.py`.
- Caso 7: **verdetto completo** (run4: 40 misure + 47 bitinfo, `172.16.1.31:511`, nessun warning).
  47/47 bit del PDF (5 stati recuperati), 16/18 unità per TAG, REG 166 corretto, sentinel e
  `UNITS2` confermati. Fixture `myhydra/double_pdf/tests/case_7/outputs/observed_adas_case7_qwen38_run4.json`,
  verità PDF e test in `myhydra/double_pdf/tests/test_adas_caso7_pdf_truth.py`.

## Tre difetti aperti sul Double PDF — aggiornati alla run4 del caso 7 (6/10)

Chiusi e verificati:
1. ~~Script del nodo 12 divergente~~ — copia canvas AST-identica + test di parità; sentinel confermato in run3/run4.
2. ~~Carry-over oltre pagina~~ — `registro_applicato` nel consolidatore; i 5 stati ci sono (47/47 bit).
3. ~~Join per uguaglianza esatta~~ — TAG IOL nel chunk (prompt v6); 16/18 unità; REG 166 col nome giusto.

Restano, in ordine di gravità:
1. **Limiti mai applicati in ADAS.** Il chunk li porta (`limit_day`, `limit_hour`), `json_creator` scrive costanti sentinella. Vale per entrambi i casi.
2. **Fattori `Dividere x10`** delle 9 misure asteriscate (JOB 4.5.2, colonna RANGE IOL): non raccolti.
3. **O2 Secco/Umido senza unità** (caso 7): le uniche 2 scale non collegate; da investigare sul chunk.
4. **Nome stazione variabile per run** (`Sistema Analisi Emissioni` vs `SME`): il ramo Station a volte dà `null`. Domanda per il cliente insieme a BISON, zeri iniziali, regola V2.
5. **Nessun output Double importato in ADAS reale**; terza coppia mai vista.

## Prossimo passo

1. **Nodo `JSON CREATOR` (12)**: incollare la **copia canvas**
   `myhydra/double_pdf/platforms/lv1/scripts/in_use/json_creator_edge13_canvas.py`
   (fix Double, `{edge}[13]`, hash
   `b004ec4a173b64836eb70d691c2b90b91f1fa108c6cf7c63b07887dac80eb704`).
   Il file documentato `json_creator_edge13.py` NON va incollato: il canvas
   rifiuta i paste oltre ~32 KB (34.365 byte → rosso, 26.731 → verde, stessa
   logica). Parità AST+output garantita da test.

   I due flussi hanno **copie separate** dello stesso trasformatore, perché l'indice dell'edge
   è diverso (`[4]` Single, `[13]` Double) e un file unico costringerebbe a editarlo a ogni switch
   di flusso: è così che la divergenza è entrata. Non mescolarli.
   Subito dopo, prova di importazione di un output in un ADAS reale: è l'unica verifica che manca
   davvero.
2. Prompt misure v6 (`measurement_measures_bison_v6.md`) già nel nodo `ESTRAI MISURE E BISON`
   (TAG trascritto + self-check BIT). Non toccare senza motivo.
3. Applicare `limit_day`/`limit_hour` in `json_creator` (il chunk li porta, l'ADAS riceve costanti).
4. Investigare O2 Secco/Umido senza unità sul chunk della run4.
5. Attendere dal cliente: BISON, zeri iniziali, regola V2, nome stazione in ADAS.
6. Prova di importazione in ADAS reale + terza coppia mai vista.

## Single PDF — non è perfetto (verificato 5/10, nessuna modifica al codice)

Resta aperto tutto il Blocco B/C di `myhydra/single_pdf/PENDENZE.md`. In più, dal confronto coi PDF:

- **`UNITS: "Unità"`** emesso sulla misura `Polveri (GR)` (reg 40008): nel PDF quella cella contiene
  `mg/Nm³` e la parola `Unità` è un'intestazione di sottocolonna. Causa: **V3 del prompt v13 elenca
  `"Unità"` fra gli esempi di unità valide**, quindi insegna l'errore. Il GT legacy ha lo stesso bug.
- **Refuso corretto contro V13**: `Allarme 1 Ossiegno umido` → `Ossigeno` nel PDF, noi correggiamo,
  il legacy no. Comportamento incoerente (D3 dice che su PROTEC_1 il refuso è stato rispettato):
  è affidabilità del VLM, serve un test dedicato.
- **I 2 "difetto" di SMA_1 nel verdetto sono falsi positivi**: `verifica_pdf/confronta.py` confronta
  per registro ignorando la stazione, e 40001 compare in due tabelle diverse. Noi le separiamo
  correttamente.
- **`DATA_TYPE` → formato**: SIEMENS_2 dichiara `INT16` e noi emettiamo 150 su 21 misure, il legacy
  250 su tutte. Chiude C3 con evidenza reale.
- **Copertura SIEMENS_2**: 104 misure contro 339 del legacy su 1116 righe; 129 righe non coperte. È
  B3/C1, a monte dell'estrazione, non difetto del pytool.
- **B2 è più grave di quanto scritto**: PROTEC_1 dichiara 2 IP e ne usa 1, PROTEC_2 dichiara 3 e ne
  usa 1; in entrambi i casi viene emesso `127.0.0.1` come default, cioè un IP fabbricato.
- **Carry-over del registro assente nel prompt Single** (V4 dice `cella vuota → null`): non si è
  mai manifestato sui 4 documenti noti, ma è un buco latente.

Ordine proposto: (1) V3 del prompt, (2) match su `(stazione, registro, bit)` in `confronta.py`,
(3) `registro_suggerito` anche nel Single, (4) test di fedeltà sui refusi, (5) aggiornare
`PENDENZE.md` (dice `13 passed, 2 failed`, oggi è `12 passed, 0 failed`) e la tabella KPI del report,
 dove "Copertura Bitinfo 100%" non è sostenibile.
