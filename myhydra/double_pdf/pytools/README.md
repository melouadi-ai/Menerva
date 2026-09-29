# Pytools — Double PDF

## Inventario

| File | Nodo | Stato |
|---|---|---|
| [`associate_page_labels_to_media_keys.py`](associate_page_labels_to_media_keys.py) | LV2-04 | Generato per questo workflow; esecuzione su MyHydra da verificare. |

## Contratto del runtime Pytool

Lo script è scritto per essere incollato direttamente nel corpo di un nodo Pytool MyHydra, non per essere importato. Questo comporta tre vincoli:

- I dati arrivano tramite placeholder `{edge}[N]`, risolti dalla piattaforma al momento dell'esecuzione. Gli indici sono quelli letti sul canvas e vanno ricontrollati prima dell'incollaggio.
- Il risultato deve essere nella variabile `result`, serializzato come stringa JSON, che la piattaforma legge per popolare l'edge successivo. In caso di errore lo script restituisce comunque un JSON con `status: ERROR` invece di propagare l'eccezione.
- Le variabili `media_raw` e `vlm_raw` alla riga 5-6 devono restare invariate. Gli indici `[4]` e `[2]` corrispondono agli edge del nodo Naive e del nodo Visiomaru descritti nel README.

## Stile

Lo script usa cicli `while` con indice esplicito, `try/except` e nessuna funzione o classe. È una scelta deliberata per adattarsi al runtime limitato del nodo Pytool.

## Storico

Lo script è stato separato in questa cartella il 29/09/2026 durante la baseline del caso 6. Prima viveva insieme alla specifica del nodo.
