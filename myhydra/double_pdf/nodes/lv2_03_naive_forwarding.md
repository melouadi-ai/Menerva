# Nodo LV2-03 — Naive forwarding

- **Tipo/nome:** Naive.
- **Input:** output del nodo LV2-01 Medex.
- **Compito:** inoltrare il payload Medex al Pytool senza trasformarlo.
- **Edge in ingresso:** #3 dal Medex.
- **Edge in uscita:** #4 verso Pytool.
- **Nota:** il nodo era stato inserito per trasportare le chiavi, ma l'edge #4 è risultato vuoto in tutte le 14 iterazioni. Inoltre l'output del Medex LV2 contiene media, non le chiavi originali necessarie al Pytool. La sorgente corretta delle chiavi è l'input iterativo `{question}`; il Naive non è necessario per l'associazione.
