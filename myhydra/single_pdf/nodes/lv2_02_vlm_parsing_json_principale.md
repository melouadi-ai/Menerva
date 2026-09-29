# Nodo LV2-02 — VLM, PARSING JSON PRINCIPALE

- **Tipo/nome:** Visiomaru — modello vision-language, unica sorgente di estrazione dati.
- **Input:** l'immagine prodotta dal nodo LV2-01, che corrisponde a **una pagina**.
- **Prompt:** [`../prompt/vlm_extraction_v13.md`](../prompt/vlm_extraction_v13.md), versione `v13`.
- **Output:** un oggetto JSON intermedio con la chiave `stations`, una stazione per indirizzo IP, ciascuna con la propria lista di `variables`.
- **Stato:** prompt in uso. L'esecuzione non è stata osservata sulla piattaforma per questa versione.

## Il Livello 2 termina qui

Con l'Opzione B di ADR-001 il Livello 2 non contiene più nodi di merge. Nel legacy ne aveva tre, che univano i risultati dei tre agenti VLM paralleli. Oggi c'è un solo VLM che restituisce già un JSON unico, quindi il merge interno non serve più ed è stato rimosso.

## Confini del compito del VLM

Il prompt è costruito perché il modello **legga e trascriva, senza calcolare**. Le regole chiave sono:

- **Una immagine corrisponde a una pagina.** Non deve ricordare né completare righe di altre pagine.
- **`description` e gli stati sono copia esatta.** Se non sono leggibili, il valore è `null`. Vietato inferire da parole chiave o mettere valori predefiniti.
- **`data_type` va copiato dalla colonna, mai dedotto** dal nome o dal registro.
- **Ogni bit va copiato dalla propria riga**, senza rinumerare né interpolare. Righe consecutive possono avere bit non consecutivi.
- **Non calcolare** `DRIVERPRIVATE`, `ID`, `DRIVERDATA`, `TYPE` e l'XML. Non spettano al VLM.

I calcoli deterministici sono compito del pytool LV1-04. La divisione è il principio architetturale dell'intero progetto.

## Punti di frizione noti

**Gli stati ON/OFF.** Le regole V7 e V8 del prompt vietano al VLM di dedurre gli stati. Il pytool, però, contiene una tabella di parole chiave che li deduce comunque quando mancano. Non è un errore ma una delocalizzazione deliberata della regola dal prompt al codice, e va documentata come tale: il contratto scritto e l'implementazione non dicono la stessa cosa.

**Lo schema di validazione.** Nello schema Pydantic `description` è una stringa obbligatoria e non vuota, mentre nel prompt è dichiarata come `string|null` e la regola V2 dice di saltare la riga invece di emettere `null`. Se il VLM emette `null`, la validazione segnala un errore. La validazione non blocca, quindi il flusso prosegue e l'errore finisce fra i warning.

- **Riferimenti:** [`../prompt/README.md`](../prompt/README.md), [contratto VLM](../../../docs/contracts/VLM_INTERMEDIATE.md) *(dichiara ancora v11 come riferimento)*.
