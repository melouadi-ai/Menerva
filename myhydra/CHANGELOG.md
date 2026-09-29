# Changelog MyHydra

## 2026-09-29 — Baseline Single PDF moderno e riassetto del Double PDF

### Single PDF

- Documentato il flusso moderno, Opzione B di ADR-001, in `single_pdf/`.
- Dieci schede nodo: quattro del Livello 1, due del Livello 2, tre di backlog con le schede `DA CONFERMARE` di `pdf_splitter`, `page_classifier` e `merge_pages`, che risultano superati dall'architettura corrente.
- Copiati il prompt `vlm_extraction_v13.md` e il pytool `json_creator_v4_2.py` da `src/`, byte-identici, con l'hash atteso documentato nei rispettivi README.
- Isolato il flusso cloud osservato il 28/09 in `single_pdf/flusso_cloud_osservato.md`, dichiarandolo non implementato e di topologia diversa.
- Aggiunto il caso PROTEC_1 con la fixture VLM reale, l'output osservato del pytool e il ground truth legacy.
- Eseguito il confronto con il ground truth legacy: 10 misure su 10 e 38 bitinfo su 40, con le divergenze classificate in attese e da esaminare.
- Verificato che il refuso `RCHIESTA MNAUTENZIONE` e le 4 unità di misura mancanti provengono entrambi dall'estrazione VLM e non dal pytool.
- Documentate le divergenze fra `docs/contracts/ADAS_FINAL.md` e il codice reale: lunghezza di `DRIVERPRIVATE`, posizione del registro, trattamento dei placeholder e forma dell'output.

### Double PDF

- Unificati i due alberi `LV1/double_pdf/` e `LV2/double_pdf/` in un'unica cartella `double_pdf/`.
- Le schede nodo hanno ora il prefisso `lv1_` o `lv2_`, per non confondere i due livelli.
- Unificati i due README del workflow in un documento unico con una sezione per livello, e i due README del caso 6 in uno solo.
- Corretti i link che puntavano ai vecchi percorsi `LV1/` e `LV2/`.
- Aggiunti i README di convenzioni in `prompts/` e `pytools/`, che mancavano.

### Struttura

- `myhydra/` contiene ora due rami paralleli, `single_pdf/` e `double_pdf/`, autosufficienti ciascuno.
- La distinzione fra i due livelli è nel nome dei file e nella struttura logica, non in directory separate.

### Stato

Nessun test è stato eseguito contro il runtime MyHydra. Il confronto con il ground truth legacy è stato eseguito localmente ed è riportato in `single_pdf/test/caso_2_protec_1/outputs/`.

## 2026-09-29 — Baseline Double PDF caso 6

- Documentata la topologia LV1 e LV2 osservata sul canvas.
- Salvato il prompt VLM di classificazione in versione `v1`.
- Separato il Pytool di associazione chiavi/etichette in `LV2/double_pdf/pytools/`.
- Archiviati output VLM osservato e fixture sanitizzate per 14 pagine/finestre.
- Nessun test è stato eseguito contro il runtime MyHydra; l'esecuzione reale del Pytool resta da verificare.
