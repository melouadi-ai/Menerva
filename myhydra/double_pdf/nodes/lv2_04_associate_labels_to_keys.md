# Nodo LV2-04 — Associazione etichette e chiavi

> **Scheda storica.** Questo associatore apparteneva alla precedente classificazione VLM per finestre e non è nel percorso operativo corrente, dove il Page Classifier è un'iniezione LV2 e la deduplicazione avviene nel Pytool LV1-04. Tenerlo come traccia tecnica; non usarlo per modificare il canvas attuale senza prima riallineare il workflow.

- **Tipo/nome:** Pytool.
- **Script:** [`../pytools/associate_page_labels_to_media_keys.py`](../pytools/associate_page_labels_to_media_keys.py).
- **Input `{question}`:** finestra originale ricevuta dal ciclo LV1, contenente le chiavi Medex.
- **Input edge #2:** output JSON del VLM con `index`, `document_role` e `label`.
- **Operazione:** decodifica `_medexkeys` anche se annidato/serializzato; associa ogni `index` locale alla chiave in ordine; conserva sia ruolo documento sia categoria e controlla conteggi, indici e valori ammessi. Se riceve un risultato storico senza `document_role`, usa `UNKNOWN`.
- **Output MyHydra:** variabile `result` contenente JSON con `key`, `index`, `document_role` e `label` per pagina.
- **Diagnostica aggiornata:** `{question}` contiene JSON valido con `_medexkeys` in tutte le 14 iterazioni; edge #2 contiene JSON valido con `pages`. I primi 13 giri hanno due chiavi e l’ultimo una. `_medexkeys` è una stringa JSON serializzata dentro il JSON esterno.
- **Errore precedente:** edge #4 era vuoto in tutte le iterazioni; non è la sorgente corretta delle chiavi.
- **Prima prova dello script associatore:** output vuoto (`[,,,,,]`) per tutte le iterazioni nonostante gli ingressi siano validi. Lo script è stato semplificato per il formato osservato; questa revisione è stata poi incollata nel runtime MyHydra.
- **Verifica locale della revisione:** testato il sorgente effettivo con placeholder simulati, tutte le 14 finestre campione, una finestra singola, slash escapate e conteggio errato; 4 casi passano.
- **Revisione con ruolo documento:** il Pytool ora conserva `document_role`; i risultati storici senza questo campo ricevono `UNKNOWN`. Test locali complessivi aggiornati dopo la modifica: 10 casi superati tra associazione e deduplicazione.
- **Verifica runtime MyHydra:** 14 record `status: OK`; le prime 13 finestre associano due chiavi ciascuna e l'ultima una, per 27 associazioni sulle 14 chiavi uniche. Le etichette ripetute delle chiavi di overlap concordano.
- **Fixture runtime storica sanitizzata:** [`../tests/case_6/outputs/observed_pytool_sanitized.json`](../tests/case_6/outputs/observed_pytool_sanitized.json). È stata prodotta con la prompt v1 e non contiene il ruolo; le chiavi runtime sono sostituite con ID sintetici.
- **Correzione progettuale:** non usare l'output del Medex LV2 come sorgente delle chiavi: contiene le immagini risolte. Il Pytool deve leggere `{question}` (input originale LV1) e edge #2 (classificazione VLM). L'edge #4 vuoto e il nodo Naive non servono all'associazione e possono restare scollegati/non usati durante la verifica.
- **Vincoli di stile:** nessuna funzione/classe/lambda/any/all; cicli `while`; commenti italiani; placeholder `{edge}[N]`.
- **Limite:** non assegna numero pagina globale o nome PDF; non deduplica tra finestre diverse.
