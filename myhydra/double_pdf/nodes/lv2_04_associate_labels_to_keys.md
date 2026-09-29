# Nodo LV2-04 — Associazione etichette e chiavi

- **Tipo/nome:** Pytool.
- **Script:** [`../pytools/associate_page_labels_to_media_keys.py`](../pytools/associate_page_labels_to_media_keys.py).
- **Input `{question}`:** finestra originale ricevuta dal ciclo LV1, contenente le chiavi Medex.
- **Input edge #2:** output JSON del VLM.
- **Operazione:** decodifica `_medexkeys` anche se annidato/serializzato; associa ogni `index` locale alla chiave in ordine; controlla numero, indici duplicati/mancanti e classe ammessa.
- **Output MyHydra:** variabile `result` contenente JSON.
- **Diagnostica aggiornata:** `{question}` contiene JSON valido con `_medexkeys` in tutte le 14 iterazioni; edge #2 contiene JSON valido con `pages`. I primi 13 giri hanno due chiavi e l’ultimo una. `_medexkeys` è una stringa JSON serializzata dentro il JSON esterno.
- **Errore precedente:** edge #4 era vuoto in tutte le iterazioni; non è la sorgente corretta delle chiavi.
- **Correzione progettuale:** non usare l'output del Medex LV2 come sorgente delle chiavi: contiene le immagini risolte. Il Pytool deve leggere `{question}` (input originale LV1) e edge #2 (classificazione VLM). L'edge #4 vuoto e il nodo Naive non servono all'associazione e possono restare scollegati/non usati durante la verifica.
- **Vincoli di stile:** nessuna funzione/classe/lambda/any/all; cicli `while`; commenti italiani; placeholder `{edge}[N]`.
- **Limite:** non assegna numero pagina globale o nome PDF; non deduplica tra finestre diverse.
