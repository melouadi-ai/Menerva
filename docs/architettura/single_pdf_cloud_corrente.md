# Single PDF cloud — flusso osservato

## Fonte e limiti

Questa pagina descrive i due screenshot forniti dall’utente il 28 settembre 2026. Rappresenta la configurazione visibile del Single PDF sulla piattaforma cloud alla data indicata. Gli screenshot mostrano nomi, descrizioni e connessioni dei nodi; non mostrano configurazioni, prompt, payload, regole interne o risultati di esecuzione.

Il diagramma va quindi trattato come una mappa osservata della piattaforma, non come prova che la corrispondente logica sia implementata in questo repository.

## Livello 1

```text
1. medex
   ├── #1 @MEDIA   → 2. medex
   └── #2 @NOMEDIA → 3. naive

2. medex → #3 → 4. SINGLE PDF ENGINE (iterativo)
                    │
                    └── #4 → 5. pytool
                              descrizione: “Pulizia JSON PRE-BISON”
                              │
                              └── #5 → 6. naive (nodo di uscita visibile)
```

La lettura del ramo è basata sulle etichette visibili: il primo Medex separa i percorsi `@MEDIA` e `@NOMEDIA`; il secondo Medex passa al motore iterativo; il risultato prosegue al pytool e poi al nodo Naive finale.

## Livello 2

```text
1. medex — “Conversione CONTENT a PNG”
   ├── #1 @MEDIA   → 3. visiomaru — “PARSING JSON PRINCIPALE”
   └── #2 @NOMEDIA → 2. naive (nodo di uscita visibile)
```

Il diagramma mostra dunque un ramo `MEDIA` che raggiunge Visiomaru e un ramo `NOMEDIA` che raggiunge Naive. Non mostra il contenuto né la destinazione successiva degli output dei due nodi.

## Cosa non si può dedurre dagli screenshot

- Se il nodo iniziale converte effettivamente il PDF o riceve contenuto già preparato: manca la configurazione Medex.
- Che cosa significhino esattamente i filtri `@MEDIA` e `@NOMEDIA` per i tipi e i valori dei payload.
- Come il nodo `SINGLE PDF ENGINE` itera, divide le pagine, raccoglie le risposte o gestisce errori e retry.
- Il modello e il prompt di Visiomaru, lo schema del JSON principale e la sua validazione.
- Le trasformazioni eseguite dal pytool oltre alla descrizione “Pulizia JSON PRE-BISON”.
- Se e dove avvengano generazione BISON, linearizzazione, validazione finale o consegna del JSON ADAS.
- Il collegamento runtime tra Livello 1 e Livello 2 oltre alle connessioni rappresentate nell’editor.

Per verificare questi punti servono le configurazioni esportate dei nodi, i loro prompt/script e almeno un input con gli output intermedi corrispondenti.

## Differenza rispetto ai file nel repository

I file `legacy/single_pdf/` sono esportazioni testuali di una versione precedente e hanno una struttura diversa. Il codice in `src/nodes/json_creator.py` è un artefatto locale distinto dai nodi cloud. Nessuno dei due va usato per riempire i dettagli mancanti del diagramma senza confronto con la configurazione cloud corrente.
