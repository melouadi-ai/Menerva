# Single PDF — materiali canvas (redesign v14/v15)

Copie pronte da incollare nei nodi MyHydra del flusso Single PDF ridisegnato
(3 rami VLM v14 + consolidatore + JSON CREATOR v15). Organizzazione modellata
su `myhydra/double_pdf/platforms/` (i due flussi condividono il trasformatore
ma non gli indici degli edge: le copie restano separate, non mescolarle).

## Mappa

- [`lv1/`](lv1/README.md): catena LV1 e script Pytool da incollare.
- [`lv2/`](lv2/README.md): i 3 rami VLM v14 (prompt da mettere in Powered identity).
- `lv1/scripts/updated_pending_validation/`: le 2 copie canvas da incollare
  al rewiring (mai incollate sul canvas: la prima run MyHydra resta da fare).
- `lv1/scripts/in_use/`: vuoto finché il rewiring non è fatto e validato —
  il canvas attivo esegue ancora materiale pre-redesign (prompt v13 +
  creator precedente). Dopo la run, le copie validate migrano qui.
- `lv1/scripts/parked/`: vuoto; prove non collegate. Lo storico versionato
  (`json_creator_v4_2/v4_4/v4_5`) resta in `../../pytools/`.
- `lv2/prompts/current/`: i 3 prompt v14 (produzione del redesign).
- `lv2/prompts/history/`: `vlm_extraction_v13.md` (storico, immutato).

## Contratto I/O dei Pytool — chiarito una volta sola qui

I due Pytool usano due meccanismi di emissione diversi. È intenzionale e
verificato a metà: non uniformare senza motivo.

| Nodo | Emissione | Errore | Stato verifica |
|---|---|---|---|
| CONSOLIDATORE (nuovo, LV1-04) | `result = json.dumps(...)` | ERROR JSON in `result`: `{"status": "ERROR", "error": ...}` — mai blank | Mai eseguito sul canvas: alla prima run confermare che il nodo esponga `result` |
| JSON CREATOR v15 (LV1-05) | `print(output)` + variabile `output` | `try/except` globale: in errore stampa `{"status": "ERROR", ...}`, mai blank (fix Task 8 round 1/5) | Meccanismo legacy, verificato sul canvas dal Double (nodo 12, run3/run4 casi 6/7) |

Regola per il futuro: i nuovi Pytool usano `result` + ERROR JSON
(convenzione corrente). Il creator v15 resta `print`-based perché è il
meccanismo che ha già funzionato sul canvas; cambiarlo significherebbe
ritestare l'emissione su piattaforma.

## Checklist edge-settings — a ogni rewiring

1. **Ricontrollare ogni `N` in `{edge}[N]`**: l'indice è locale al canvas e
   cambia quando si aggiungono o spostano nodi. Valori attesi nel flusso
   ridisegnato: consolidatore `{edge}[5]`, creator `{edge}[4]`. L'inserimento
   del consolidatore sposta gli indici a valle: ricontrollare anche il creator.
2. **Ispezionare le impostazioni di OGNI edge** dopo il ricablaggio e
   rimuovere le match-condition spurie: un placeholder residuo (precedente
   visto: `pippo` su un edge filtro→iniezione nel Double) blocca il wire in
   silenzio — il nodo a valle muore di fame senza errori.
3. **Mai cambiare l'indice dentro il file**: se un edge è quello sbagliato,
   si ricabla il canvas, non si edita la copia (le copie sono pinnate dai test).
4. **Budget paste**: copie canvas sotto i 28 KB (soglia di sicurezza; oltre
   ~32 KB il paste fallisce a parità di logica). Dopo l'incollaggio il nodo
   deve restare verde.
5. **Output blank senza errori**: diagnosi in ordine — indice edge sbagliato?
   match-condition spuria? eccezione nel creator (senza ERROR JSON)? Non si
   può fare tap sui nodi né usare il debugger (timeout): la diagnosi viaggia
   con self-check dentro l'output (`_warnings`, `_meta`, `review`), mai con
   ispezioni live.

## Regole delle copie (non negoziabili sul canvas)

- Script standalone: solo codice inline, niente `def`/`class`/`lambda`,
  niente import di `src.*` (validazione Pydantic saltata by design).
- Incollare pulito: una riga non-Python nel paste è un SyntaxError a
  compile-time — `result` non viene mai assegnato e il nodo a valle muore
  di fame in silenzio.
- Fonte autorevole in caso di divergenza: `src/nodes/` (per i Pytool),
  `src/prompts/` (per i prompt). Le copie qui sono byte-identiche e pinnate
  da `tests/test_single_canvas_hygiene.py`.

## Riferimenti

- Schede dei nodi: [`../nodes/`](../nodes/) (`lv1_04_consolidatore.md`,
  `lv1_05_json_creator.md`, rami VLM in `lv2_02_*`).
- Vincoli operativi e di formato: `AGENTS.md` (sezione MyHydra).
- Report del redesign: `.superpowers/sdd/2026-10-06-single-pdf-redesign/`.
