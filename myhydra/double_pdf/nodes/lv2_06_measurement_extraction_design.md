# Progettazione LV2 Measurement Technical Data

**Stato:** cablaggio iniziale confermato dallo screenshot del canvas; ancora da verificare con una run. La proposta deriva dal legacy ed è adattata al passaggio iterativo di una pagina per volta. I prompt e il Pytool finale non sono ancora stati preparati.

## Obiettivo della sottopiattaforma

Ricevere una pagina `MEASUREMENT_TECHNICAL_DATA` per iterazione e ricavarne misure analogiche/digitali e informazioni `bitinfo`, mantenendo la provenienza della pagina (`key`, `sequence_index`, `document_role`, `label`, avvisi). La LV2 non deve unire pagine diverse solo perché riportano lo stesso IP.

## Sequenza proposta sul canvas

| Ordine logico | Tipo | Nome proposto | Funzione |
|---:|---|---|---|
| 1 | Pytool | `ESTRAI CHIAVE PAGINA` | Riusa [`../pytools/extract_page_key.py`](../pytools/extract_page_key.py): estrae la chiave dal record iterativo `{question}`. |
| 2 | Medex | `RECUPERA IMMAGINE PAGINA` | `content2media` sulla chiave del nodo 1. |
| 3 | Visiomaru/VLM | `ESTRAI MISURE E BISON` | Parte dal legacy Nodo 3; estrae le righe di misura e i campi BISON richiesti, con ordine sorgente conservato. |
| 4 | Visiomaru/VLM | `ESTRAI BITINFO E NOMI` | Parte dal legacy Nodo 4; identifica i digitali packed e standalone/CMD e restituisce `MEASUREID`, `BITNO`, `BITNAME`. |
| 5 | Visiomaru/VLM | `ESTRAI STATI TEXTON TEXTOFF` | Parte dal legacy Nodo 5; restituisce `MEASUREID`, `BITNO`, `TEXTON`, `TEXTOFF` per gli stessi bitinfo. |
| 6 | Naive | `OUTPUT TEST MISURE` | Nella prima prova inoltra il risultato grezzo del VLM 3. |
| 7 | Naive | `OUTPUT TEST BITINFO` | Nella prima prova inoltra il risultato grezzo del VLM 4. |
| 8 | Naive | `OUTPUT TEST STATI DIGITALI` | Nella prima prova inoltra il risultato grezzo del VLM 5. |

I nodi 3–5 ricevono la stessa immagine prodotta dal nodo 2 e lavorano in parallelo. Per la prima prova non aggiungere ancora il Pytool di merge: raccogliere i tre output separati permette di verificare gli schemi prima di scrivere il parser/associatore. Poi i tre Naive di test saranno sostituiti da un Pytool di assemblaggio per pagina e da un Naive finale.

### Cablaggio osservato sul canvas

Lo screenshot inviato dall'utente conferma la catena nodo 1 → nodo 2, il fan-out dell'immagine Medex ai tre VLM e un Naive distinto collegato a ciascun VLM. Nel canvas mostrato i collegamenti in uscita dai nodi 2–5 sono numerati rispettivamente #2, #3, #4, #5, #6 e #7. La verifica riguarda la topologia visibile, non ancora i payload effettivamente ricevuti dai VLM.

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
