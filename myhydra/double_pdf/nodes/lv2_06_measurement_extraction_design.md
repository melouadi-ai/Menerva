# Progettazione LV2 Measurement Technical Data

**Stato:** cablaggio confermato e output del ramo `MEASURES_BISON` raccolto in due run Qwen 3.8. Il Pytool associa tutte e 7 le risposte alla pagina e al ramo corretti, ma l'estrazione non produce righe: sei risposte sono gusci stazione vuoti e una è `[]`. Non progettare ancora il merge; prima verificare la lettura di una tabella con una prova VLM breve.

## Obiettivo della sottopiattaforma

Ricevere una pagina `MEASUREMENT_TECHNICAL_DATA` per iterazione e ricavarne misure analogiche/digitali e informazioni `bitinfo`, mantenendo la provenienza della pagina (`key`, `sequence_index`, `document_role`, `label`, avvisi). La LV2 non deve unire pagine diverse solo perché riportano lo stesso IP.

## Sequenza proposta sul canvas

| Ordine logico | Tipo | Nome proposto | Funzione |
|---:|---|---|---|
| 1 | Pytool | `ESTRAI CHIAVE PAGINA` | Riusa [`../platforms/lv2/shared/scripts/in_use/extract_page_key.py`](../platforms/lv2/shared/scripts/in_use/extract_page_key.py): estrae la chiave dal record iterativo `{question}`. |
| 2 | Medex | `RECUPERA IMMAGINE PAGINA` | `content2media` sulla chiave del nodo 1. |
| 3 | Visiomaru/VLM | `ESTRAI MISURE E BISON` | Parte dal legacy Nodo 3; estrae le righe di misura e i campi BISON richiesti, con ordine sorgente conservato. |
| 4 | Visiomaru/VLM | `ESTRAI BITINFO E NOMI` | Parte dal legacy Nodo 4; identifica i digitali packed e standalone/CMD e restituisce `MEASUREID`, `BITNO`, `BITNAME`. |
| 5 | Visiomaru/VLM | `ESTRAI STATI TEXTON TEXTOFF` | Parte dal legacy Nodo 5; restituisce `MEASUREID`, `BITNO`, `TEXTON`, `TEXTOFF` per gli stessi bitinfo. |
| 6 | Naive | `OUTPUT TEST MISURE` | Nella prima prova inoltra il risultato grezzo del VLM 3. |
| 7 | Naive | `OUTPUT TEST BITINFO` | Nella prima prova inoltra il risultato grezzo del VLM 4. |
| 8 | Naive | `OUTPUT TEST STATI DIGITALI` | Nella prima prova inoltra il risultato grezzo del VLM 5. |
| 9 | Pytool | `ETICHETTA OUTPUT MISURE` | Etichetta il ramo del VLM 3 e aggiunge la pagina iterativa; edge VLM #5 nello screenshot aggiornato. |
| 10 | Pytool | `ETICHETTA OUTPUT BITINFO` | Etichetta il ramo del VLM 4 e aggiunge la pagina iterativa; edge VLM #6 nello screenshot aggiornato. |
| 11 | Pytool | `ETICHETTA OUTPUT STATI` | Etichetta il ramo del VLM 5 e aggiunge la pagina iterativa; edge VLM #7 nello screenshot aggiornato. |

I nodi 3–5 ricevono la stessa immagine prodotta dal nodo 2 e lavorano in parallelo. I nodi 9–11 si inseriscono tra ciascun VLM e il Naive corrispondente. Aggiungono ramo e record pagina letto dalla `{question}` iterativa; trasformano le fence JSON in dati JSON quando possibile, mantenendo la risposta grezza se il parsing fallisce. Non sono il Pytool finale di merge.

### Cablaggio osservato sul canvas

Gli screenshot inviati dall'utente confermano la catena nodo 1 → nodo 2, il fan-out dell'immagine Medex ai tre VLM, i tre Pytool etichettatori e un Naive distinto a valle di ciascun Pytool. Nel canvas aggiornato i collegamenti VLM→Pytool sono #5, #6, #7 e quelli Pytool→Naive sono #8, #9, #10. La verifica riguarda la topologia visibile; gli script etichettatori devono ancora essere eseguiti su MyHydra.

## Contenuto da configurare nei nodi

### Nodo 1 — Pytool `ESTRAI CHIAVE PAGINA`

Incollare il contenuto completo di [`../platforms/lv2/shared/scripts/in_use/extract_page_key.py`](../platforms/lv2/shared/scripts/in_use/extract_page_key.py). Legge la `{question}` della singola iterazione e restituisce la chiave media come stringa semplice.

### Nodo 2 — Medex `RECUPERA IMMAGINE PAGINA`

Usare la chiave passata dall'edge #1:

```text
{"request":"content2media","nume":1,"content":{edge}[1]}
```

L'indice `[1]` corrisponde al collegamento Pytool→Medex #1 mostrato nello screenshot. Se MyHydra rinumera l'edge dopo modifiche al canvas, aggiornare l'indice.

### Nodi 3–5 — prompt VLM

Incollare il contenuto completo del file corrispondente:

| Nodo | Prompt |
|---:|---|
| 3 — `ESTRAI MISURE E BISON` | Powered identity [`measurement_measures_bison_v3.md`](../platforms/lv2/measurement/prompts/current/measurement_measures_bison_v3.md); campo Prompt `{edge.media}[2]` |
| 4 — `ESTRAI BITINFO E NOMI` | Powered identity [`measurement_bitinfo_names_v3.md`](../platforms/lv2/measurement/prompts/current/measurement_bitinfo_names_v3.md); campo Prompt `{edge.media}[3]` |
| 5 — `ESTRAI STATI TEXTON TEXTOFF` | Powered identity [`measurement_bitinfo_states_v3.md`](../platforms/lv2/measurement/prompts/current/measurement_bitinfo_states_v3.md); campo Prompt `{edge.media}[4]` |

Per tutti e tre i VLM lasciare **Context** vuoto e incollare nei rispettivi campi **Powered identity** il contenuto dei file indicati. Gli indici media #2, #3 e #4 sono locali ai collegamenti Medex→VLM di questo canvas. Le versioni v2 sono storiche: avevano messo il riferimento media dentro il testo di istruzioni invece che nel campo Prompt.

### Nodi 9–11 — Pytool etichettatori

Incollare gli script indicati, rispettando gli edge VLM in ingresso osservati nello screenshot aggiornato:

| Nodo | Script | Edge VLM in ingresso |
|---:|---|---:|
| 9 — `ETICHETTA OUTPUT MISURE` | [`../platforms/lv2/measurement/scripts/updated_pending_validation/tag_measurement_measures_output.py`](../platforms/lv2/measurement/scripts/updated_pending_validation/tag_measurement_measures_output.py) | #5 |
| 10 — `ETICHETTA OUTPUT BITINFO` | [`../platforms/lv2/measurement/scripts/updated_pending_validation/tag_measurement_bitinfo_names_output.py`](../platforms/lv2/measurement/scripts/updated_pending_validation/tag_measurement_bitinfo_names_output.py) | #6 |
| 11 — `ETICHETTA OUTPUT STATI` | [`../platforms/lv2/measurement/scripts/updated_pending_validation/tag_measurement_bitinfo_states_output.py`](../platforms/lv2/measurement/scripts/updated_pending_validation/tag_measurement_bitinfo_states_output.py) | #7 |

Ogni script legge anche `{question}` come record pagina dell'iterazione. Se il VLM restituisce JSON in fence Markdown, prova a decodificarlo; in caso di testo non parsabile, conserva risposta grezza ed errore insieme ai metadati della pagina.

### Nodi 6–8 — Naive di prova

Non inserire prompt o codice: lasciare il nodo Naive come forwarding dell'output del rispettivo VLM. Conservare i tre rami separati per poter controllare i payload grezzi.

| Naive | Ingresso |
|---|---|
| Nodo 6 — `OUTPUT TEST MISURE` | Edge #8 dal nodo 9 |
| Nodo 7 — `OUTPUT TEST BITINFO` | Edge #9 dal nodo 10 |
| Nodo 8 — `OUTPUT TEST STATI DIGITALI` | Edge #10 dal nodo 11 |

## Impostazioni e modello VLM osservati

Screenshot condiviso durante la prima elaborazione, per un nodo Visiomaru:

Modelli mostrati nel selettore `Core`:

- `mary - Qwen 3 Next 80B Q4`
- `marycoder - Qwen 3.5 35B Q8.0` (selezionato nello screenshot precedente)
- `marygpt - GPT OSS 120B Q4`
- `maryvl - Qwen 3.5 35B Q8.0 - Vision Language`

Correzione fornita dall'utente dopo aver consultato il tutor: il core attualmente selezionato (`marycoder - Qwen 3.5 35B Q8.0` nell'etichetta UI) corrisponde in realtà al modello Qwen 3.8; il nome mostrato non è stato aggiornato. Perciò mantenere il core già selezionato per questa prova, senza passare a `maryvl`. Applicare lo stesso core nei tre VLM e valutare l'output della run.

| Impostazione | Valore osservato | Indicazione per la prova |
|---|---|---|
| Core da usare nei VLM (confermato da screenshot il 2 ott 2026) | `marycoder - Qwen 3.8 Flash Next 180B 4 bit` | Etichetta UI precedente (`Qwen 3.5 35B Q8.0`) non aggiornata: secondo il tutor il modello effettivo è Qwen 3.8. Applicare lo stesso core nei tre VLM Measurement e nel classifier. |
| Message type | `Text` | Lasciare com'è per ora: il VLM riceve l'immagine dal collegamento Medex; verificare il comportamento dall'output. |
| Temperature | `0,1` | Mantenere bassa per contenere variazioni nell'estrazione. |
| Top P | `0,6` | Mantenere per la run comparativa iniziale. |
| Add current time | Attivo | Disattivare: l'ora corrente non è un dato richiesto dal documento. |
| Use history | Disattivo | Mantenere disattivo perché ogni iterazione tratta una pagina autonoma. |
| Thinker Mode | `0` | Lasciare invariato per questa prova; non è ancora stato confrontato con altre impostazioni. |

La schermata non conferma se i tre VLM hanno identiche impostazioni: controllare nei rispettivi nodi. La qualità di estrazione e l'effettiva ricezione dell'immagine saranno valutate dagli output della run.

### Prova con modello leggero (2 ott 2026, caso 6)

Per corse più veloci è stato provato un VLM più leggero in via globale (quindi anche sul classifier). Esito ramo `MEASURES_BISON`: 9 record `OK`, tutti con `vlm_output: []` e `output_format: JSON`, incluse le pagine IOL 2–4 che contengono tabelle `DESCRIZIONE`/`REG`/`BIT` da 2000–3000 caratteri. Meccanica verificata (envelope, branch, pagina, JSON senza fence), estrazione inutilizzabile: il modello leggero restituisce l'array vuoto anche dove i dati esistono.

### Prova con Qwen 3.8, prompt v3 (2 ott 2026, caso 6)

Prima run Qwen 3.8: 7 pagine (2,3,4,5,8,13,14), zero righe estratte. Le sequenze 2, 4, 5, 8, 13 e 14 restituiscono il guscio placeholder `{"NAME": "SME", "DRIVERNAME": "modbusplc", "DRIVERCONFIG": ":", "ID": 1, "measures": [], "bitinfo": []}`; la sequenza 3 restituisce `[]`. Cinque risposte su sette sono in fence Markdown (`output_format: MARKDOWN_JSON`) nonostante l'istruzione JSON-only.

La run appena ricevuta conferma il pattern: 7 envelope `status: OK`, correttamente etichettati `MEASURES_BISON` e associati alle sequenze 2, 3, 4, 5, 8, 13 e 14. Le sequenze 2, 3, 4, 8, 13 e 14 contengono il guscio vuoto; la 5 contiene `[]`. Sei risposte su sette sono `MARKDOWN_JSON`, una `JSON`. Il tagger ha quindi funzionato; l'estrazione no. Fixture anonimizzata: [`../tests/case_6/outputs/observed_lv2_measurement_qwen38_measures_rerun_sanitized.json`](../tests/case_6/outputs/observed_lv2_measurement_qwen38_measures_rerun_sanitized.json). La gestione del vuoto varia rispetto alla prima run (le pagine 3 e 5 si scambiano `[]` e guscio), ma non cambia il risultato: zero righe estratte.

Il guscio è compatibile con i default del prompt (`NAME: "SME"` senza etichetta, `DRIVERCONFIG: ":"` senza IP/porta); questo mostra che il modello ha prodotto il formato previsto, ma non dimostra da solo che l'immagine sia arrivata correttamente al VLM. Nota di diagnosi: i default stessi fabbricano le stazioni vuote — una pagina senza IP produce un oggetto stazione sintetico invece di `[]`. Se la sonda mostra che il modello legge, il prompt di estrazione va riscritto senza avvolgimento stazione-per-IP (sole righe piatte, join con la stazione per via deterministica dopo). Le pagine IOL 2–4 contengono tabelle reali. Restano da distinguere la lettura/ricezione dell'immagine e la complessità del Powered identity, che supera 600 righe e combina estrazione tabellare, logiche BISON, default stazione e output aggregato. Prossimo test: una sola run del ramo con la [sonda di leggibilità tabella](../platforms/lv2/measurement/prompts/diagnostics/measure_table_readability_probe_v1.md), mantenendo `{edge.media}[2]` nel campo Prompt e sostituendo temporaneamente il Powered identity. La sonda restituisce intestazioni e al massimo cinque righe per ogni pagina iterata; confrontare in particolare le IOL 2–4. Se non trascrive, investigare il media ricevuto; se trascrive, semplificare e separare le istruzioni di estrazione. I rami BITINFO/STATES non sono inclusi nell'output condiviso.

Regola confermata: modello leggero solo per prove di plumbing; la qualità di estrazione si giudica solo con Qwen 3.8, e i confronti tra run valgono solo a parità di modello e di classificazione.

## Prima raccolta output condivisa

Il materiale incollato dall'utente contiene almeno cinque blocchi fenced `json` concatenati, senza indicazione del Naive/nodo sorgente accanto a ciascun blocco. Quattro blocchi completi sono JSON validi: tre restituiscono il placeholder legacy con `NAME: "SME"`, `DRIVERCONFIG: ":"`, `measures: []` e `bitinfo: []`; l'ultimo contiene 20 misure. Un blocco lungo è troncato nella copia allegata a metà di una proprietà (`"TYPE,`), quindi non è possibile stabilire se fosse troncato il payload originale o solo la copia. L'output fornito non consente di distinguere con certezza i rami né di concludere che i VLM abbiano unito le proprie risposte: manca l'etichetta di provenienza nella raccolta.

Le risposte sono inoltre racchiuse in fence Markdown ` ```json ` nonostante l'istruzione JSON-only. Non attribuire ancora questi blocchi ai tre VLM né usarli per scrivere l'assemblatore. Per la prossima run inserire un Pytool tra VLM e Naive per ramo, così ogni output sarà autonomamente identificabile e associato alla pagina. I placeholder vuoti derivano dalla forma legacy; dopo aver separato i rami, decidere se introdurre una nuova versione dei prompt che restituisca `[]` quando la pagina non contiene righe estraibili, evitando station vuote sintetiche.

### Formato diagnostico proposto

Ogni Pytool etichettatore dovrà produrre un envelope simile a questo, anche quando l'output VLM non si può interpretare come JSON:

```json
{
  "diagnostic": "LV2_MEASUREMENT_BRANCH",
  "branch": "MEASURES_BISON",
  "page": {
    "key": "<media key>",
    "sequence_index": 8,
    "document_role": "JOB",
    "label": "MEASUREMENT_TECHNICAL_DATA"
  },
  "output_format": "MARKDOWN_JSON",
  "vlm_output": [ ... ]
}
```

Usare valori distinti per `branch`: `MEASURES_BISON`, `BITINFO_NAMES`, `BITINFO_STATES`. Se la risposta non è JSON parsabile, l'envelope include `vlm_output_raw` e `parse_error`. In questo modo il collector può aggregare gli output senza perdere il ramo né la pagina. Gli edge #5, #6 e #7 sono quelli mostrati nello screenshot più recente. Questa diagnosi richiede una nuova esecuzione della LV2 per ottenere envelope etichettati.

## Ambito della run

Avviare la platform LV1 principale esegue anche i rami collegati che ricevono pagine. Nel caso 6, il filtro Station produce pagine, quindi viene attivata anche l'iniezione LV2 Station oltre a Measurement. Per una run di sola diagnosi Measurement, scollegare temporaneamente in LV1 il collegamento in ingresso alla sottopiattaforma Station (senza eliminare nodi o script), avviare la prova e ripristinare il collegamento dopo. Non si riporta un numero edge LV1 perché il canvas principale corrente non è visibile nello screenshot Measurement più recente.

## Forma obiettivo dell'output per pagina

Il Pytool di assemblaggio, da progettare dopo aver visto gli output VLM reali, dovrà produrre un record per pagina e preservare la provenienza. Forma concettuale:

```json
{
  "key": "<chiave media>",
  "sequence_index": 0,
  "document_role": "JOB",
  "label": "MEASUREMENT_TECHNICAL_DATA",
  "review_required": false,
  "review_warnings": [],
  "measurement_info": {
    "stations": [],
    "bitinfo": []
  }
}
```

Le `bitinfo` generali e gli stati `TEXTON/TEXTOFF` si associano all'interno della stessa pagina con `MEASUREID` e `BITNO`; non usare solo `DRIVERCONFIG` come chiave di join. Se un output manca o non si associa, conservare un errore/avviso con la pagina, senza scartare le estrazioni valide degli altri rami.

## Cosa migrare dal legacy

| Nodo legacy | Ruolo funzionale | Decisione per il nuovo flusso |
|---|---|---|
| Nodo 1 — Take the correct key | Estrae la chiave dalla finestra di pagina | Riutilizzare il Pytool chiave della LV2 Station. |
| Nodo 2 — Medex | Risolve la chiave in immagine | Riutilizzare `content2media` della LV2 Station. |
| Nodo 3 — VLM Measures * Bison | Estrae oggetti station e righe `measures`, compresi tipo, registro, unità, limiti/range, scale, divisione, `GROUP` e regole BISON | Adattare il prompt a una pagina; evitare merge cross-pagina e default inventati. |
| Nodo 4 — VLM Bitinfo General | Rileva righe digitali e `BITNAME` | Conservare le regole packed/standalone, carry-over REG, bit e skip delle righe vuote. |
| Nodo 5 — VLM Bitinfo TextON/OFF | Calcola i due stati logici | Associare allo stesso `MEASUREID`/`BITNO`; unire solo con il ramo Bitinfo General. |
| Nodi 6–9 — Pytool merge | Pulisce e combina misure, stati e bitinfo usando chiavi di stazione/IP | Non portare subito il merge per IP dentro la LV2 iterativa: assemblare prima i rami della stessa pagina. |
| Nodo 10 — Delete Null names | Rimuove nomi vuoti e voci non utili | Riesaminare i filtri legacy prima di applicarli; non eliminare segnali validi per corrispondenze generiche. |
| Nodo 11 — Check Group ingresso digitale | Applica `GROUP: Ingresso_digitale` in una condizione specifica | Mantenere come regola downstream da verificare, dopo aver confrontato misure e bitinfo. |

## Vincoli di migrazione

- Conservare ordine e valori delle righe; non deduplicare per `NAME+UNITS` finché non è confermato che righe omonime siano duplicati.
- Distinguere il registro Modbus dall'indirizzo PLC `INDIRIZZO`/DBX. Per colonne REG sparse, il carry-over è solo dall'alto verso il basso e solo nei layout documentati.
- Non inventare righe placeholder, nomi, unità, IP, porte, registri o range.
- Conservare i registri con zeri iniziali come stringhe e i registri Modbus numerici come numeri, secondo lo schema legacy.
- Rispettare le regole `CMD`/`SET`/`MV`/`XTM`, i casi `CALCOLATA`, le misure Raw, i flag `Int`/`Range`/`Division` e l'identificazione dei gruppi packed digitali.
- Non propagare ciecamente per pagina il default stazione `SME`, `DRIVERCONFIG` incompleto o `ID`: la normalizzazione/consolidamento successivo deve preservare ciò che la pagina dichiara davvero.
- Per la prima prova tenere indipendenti i VLM 4 e 5, come nel legacy. Decidere se il VLM 5 debba anche ricevere il risultato del VLM 4 solo dopo aver verificato gli output e i collegamenti consentiti da MyHydra.

## Fonti legacy

La proposta deriva da `legacy/double_pdf/LV2/Station Measurement Technical data (Condition node)/`, Nodi 1–11. Il legacy resta intatto. Prima di convertire i prompt lunghi in versioni per pagina, controllare gli schemi completi di Nodo 3, Nodo 4 e Nodo 5.

## Prossimo step sul canvas

Dentro l'iniezione `DOUBLE PDF MEASUREMENT DATA`, sostituire il Naive sonda temporaneo con i nodi 1–5 e collegare tre Naive di output ai tre VLM. Lasciare iterativa la sottopiattaforma, non i singoli Pytool. Dopo aver ricevuto i tre output del caso 6, definire il Pytool di assemblaggio per pagina.
