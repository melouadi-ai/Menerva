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

- `{question}` = current iteration input; `{edge}[N]` = another node's text output (`N` is canvas-local, re-check after rewiring). **Edges can carry match conditions**: a leftover placeholder condition (seen: `pippo` on a filter→injection edge) silently blocks the wire — the downstream injection starves with no error. After any rewiring, inspect edge settings and remove stray conditions.
- VLM nodes: two verified working layouts — legacy single Prompt field with instructions **and** `{edge.media}[N]` inline (legacy screenshots show `[19]`–`[23]`), and the split layout (`{edge.media}[N]` alone in Prompt, instructions in Powered identity, Context empty; verified 2 Oct 2026 with `image_readable: true`). The empty shells were a Medex input problem, never a field-layout problem.

## Before starting work

Read the current work-state file for the area: `myhydra/single_pdf/PENDENZE.md`, `myhydra/double_pdf/WORKFLOW_DESIGN.md`. Node cards live in `myhydra/*/nodes/` (`lv1_`/`lv2_` prefixes); Double PDF copy-paste material is organized per subplatform in `myhydra/double_pdf/platforms/` (`prompts/current/` vs `prompts/history/`, `scripts/in_use/` vs `updated_pending_validation/` vs `parked/`).

When passing a script or prompt change to the user, always paste the **complete file** with changes applied — never a single line or fragment. They copy-paste into the MyHydra canvas, so fragments slow them down. Mark temporary/debug lines with a `DEBUG` comment so they can be reverted.

Always refer to canvas nodes by their **exact node names** (e.g. `FILTER_MEASUREMENT_TECHNICAL_DATA`, not "the measurement filter"). When providing a prompt, always give the **raw markdown** ready to paste.

Always communicate with the user in **Italian**. VLM prompts and code stay in English (technical artifacts); everything else — chat, docs, commit messages — in Italian.

Sync habit in this repo is `sync.sh`: `git pull origin main`, `git add .`, timestamp commit, `git push origin main`.

## Confronto con il legacy: il GT non è un riferimento di qualità

`tests/compare_with_gt.py` confronta output vs `data/test_outputs/gaia_doublefile_result_6.json`, ma il legacy **ha errori propri**: letto riga per riga, `Mappatura_6_Cliente_SMI_1.pdf` dà 22 misure e **60** bitinfo, il GT ne ha 78. In dettaglio: 18 bitinfo fantasma (12 su righe senza TITOLO, più `PM-2601A/B` e i 4 ventilatori duplicati), due registri comandi sbagliati (430/431 invece di 431/432, shift di una riga su una riga bianca trattata come misura), `TEXTON` disallineati di una posizione, `QAL3` da `INT` scritti 250 invece di 150, e i nomi `STIMATA SO2`/`… ARI` troncati.

Conseguenza: **le differenze di un confronto col GT non vanno colmate senza verifica sul PDF.** Il metodo è in `tests/test_adas_caso6_pdf_truth.py`, che fissa la tabella verità e registra anche dove il legacy sbaglia (`test_legacy_ha_errori_noti_il_nostro_no`), così nessuna correzione futura li riporta indietro per allineamento.

Attenzione anche alle unità: nel PDF IOL del caso 6 **non esiste la colonna unità**. `mg/Nm3` e `°C` nel GT sono inferenze del legacy; noi emettiamo `mg/Nm3` solo dove la scala SO2 è dichiarata e `null` altrove. Non trattare `°C` come un dato mancante da recuperare: è una decisione di dominio (vedi `reports/CONFRONTO_QUALITA_LEGACY_VS_ATTUALE.md`).

## Stato attuale (5 ott 2026)

- Single PDF: prompt v13 + `src/nodes/json_creator.py` v4.4 (A1 soglia 100, A2 copia `myhydra/` allineata). Registro in `myhydra/single_pdf/PENDENZE.md`.
- Double PDF: catena LV1→LV2→consolidatore→ADAS verificata end-to-end sui casi 6 e 7 con Qwen 3.8. Caso 6 ha il **verdetto completo**: 22 misure + 60 bitinfo confrontati riga per riga col PDF, 22/22 registri, tutti i bit, formati `INT`→150 e `REAL`→250, `UNITS mg/Nm3` su SO2/SO2 Raw, linkage intatto. Fixture `tests/double_pdf_outputs/observed_adas_case6_qwen38_datatype.json`, tabella verità `tests/test_adas_caso6_pdf_truth.py`.
- Caso 7: **verdetto completo** (39 misure + 42 bitinfo, `172.16.1.31:511`). Tutti i 39 registri
  conformi al PDF IOL e `DATA_TYPE` applicato (`INT`→150, `WORD` stimate→250), ma 47 bit attesi
  contro 42 emessi. Fixture `myhydra/double_pdf/tests/case_7/outputs/observed_adas_case7_qwen38_run2.json`,
  verità PDF e test in `myhydra/double_pdf/tests/test_adas_caso7_pdf_truth.py`.

## Tre difetti aperti sul Double PDF, in ordine di gravità

1. **Lo script del nodo `JSON CREATOR` (12) non è `src/nodes/json_creator.py`.** Misure analogiche
   con `LOWCRITICAL/HIGHCRITICAL/LOWRANGE/HIGHRANGE/LOWOFFSET/HIGHOFFSET/SQ* = null`, mentre repo e
   tutti i GT legacy usano il sentinel `∓3.40282e38`. È la stessa classe dell'errore di linkage
   bitinfo: copia modificata a mano sul canvas. **Nessun output Double è mai stato importato in un
   ADAS reale**: la validazione è contro PDF e schema, non contro l'applicazione. Prima di ogni
   altra cosa: riallineare il nodo 12 al repo e rifare le due run.
2. **Carry-over del registro oltre il confine di pagina** (caso 7): la cella `REG 4` è unita e
   copre DBX 70.0 (p2) → 71.7 (p3). A p3 la colonna è vuota, il VLM dà `null`, il pytool scarta:
   5 stati d'impianto persi. Sono `Fermo`, `Lavaggio`, `SME in manutenzione`, `Impianto in
   manutenzione`, `Fuori servizio`, cioè **le colonne `STATI IMPIANTO` della Tabella 12 del JOB**
   (4.7 Validazioni): la matrice di invalidazione delle misure perde il suo input. Il Double ha già
   `registro_suggerito` (suggerisce, non applica): va esteso al salto di pagina.
3. **Il join scala↔misura è per uguaglianza esatta di stringa.** Nel `consolidate_to_intermediate.py`
   la scala del JOB si aggancia con `description == tag` o `description == tag + " Raw"`. Ma il JOB
   identifica i segnali per **tag** (`TF`, `O2S`, `P_MTR`) e l'IOL li descrive a parole
   (`Temperatura fumi`, `O2 Secco`, `Potenza motore`). Sul caso 7 le 4 unità applicate sono
   **esattamente** i 4 tag che coincidono col testo: le altre 14 righe di Tabella 9 muoiono nel
   join, non nell'estrazione. **Il fix non è nel prompt**: è portare il `tag` dell'IOL nel chunk e
   agganciare su quello. Vale anche per i limiti (5 dichiarati, 0 applicati) e per i fattori
   "Dividere x10" delle 9 misure asteriscate (JOB 4.5.2, anche nella colonna RANGE dell'IOL).
   Manca inoltre un warning per "il JOB dichiara unità e non le troviamo", così la lacuna resta
   silenziosa invece di essere un `null` inerte.

## Prossimo passo

1. **Riallineare il nodo `JSON CREATOR` (12)** incollando
   `myhydra/double_pdf/platforms/lv1/scripts/in_use/json_creator_edge13.py` (v4.4, `{edge}[13]`),
   e rifare le due run (6 e 7). Consegnare il file **per intero**, mai un frammento.

   I due flussi hanno **copie separate** dello stesso trasformatore, perché l'indice dell'edge
   è diverso (`[4]` Single, `[13]` Double) e un file unico costringerebbe a editarlo a ogni switch
   di flusso: è così che la divergenza è entrata. Non mescolarli.
   Hash Double: `e75c101395dcfaf9086edc393c4ea32ee8c0008333e88699b7869d471c629c91`.
   Subito dopo, prova di importazione di un output in un ADAS reale: è l'unica verifica che manca
   davvero.
2. Estendere `registro_suggerito` al salto di pagina nel consolidatore LV1 (nodo 11).
3. Applicare `units`/`scale_eng_*`/`limit_day`/`limit_hour` in `json_creator`, con un warning
   esplicito per "il JOB dichiara unità e non le troviamo" invece di un `null` silenzioso.
4. Attendere dal cliente: BISON, zeri iniziali, regola V2, nome stazione in ADAS.
5. Terza coppia IOL+JOB mai vista, per allargare il campione oltre 6 e 7.

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
