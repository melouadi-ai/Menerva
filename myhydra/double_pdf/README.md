# Double PDF — progetto MyHydra

Questa directory documenta e raccoglie l'implementazione nuova del workflow Double PDF. Il legacy rimane in [`../../legacy/double_pdf/`](../../legacy/double_pdf/) come riferimento e non viene modificato da questo progetto.

## Stato attuale

- **LV1, classificazione e deduplicazione:** verificata su MyHydra. Il caso 6 ha prodotto 14 pagine uniche; il caso 7 ne ha prodotte 11. I conflitti di classificazione restano visibili come avvisi.
- **LV1, instradamento per etichetta:** i tre Pytool filtrano i record completi usando `label`. `STATION_INFORMATION` e `MEASUREMENT_TECHNICAL_DATA` vanno alle rispettive LV2 iterative; `DENSITY_MAP` viene inoltrata con un Naive.
- **Passaggio LV1→LV2:** verificato in una run del caso 6. I rami hanno ricevuto rispettivamente 6 pagine Station, 7 Measurement e 1 Density; le chiavi e i metadati sono rimasti associati alle pagine.
- **LV2 Station Information:** nuova run con il Pytool associatore aggiornato: tutte e 6 le pagine sono associate senza errori; 3 hanno estrazioni e 3 restituiscono `[]`. Restano avvisi di classificazione sulle pagine 11 e 12 e una variazione tra run nell'estrazione della pagina 10.
- **LV2 Measurement Data:** collegata alla sua iniezione; al momento contiene un Naive di forwarding. È stata progettata la sequenza di estrazione per pagina, derivata dai nodi Measurement legacy; prompt VLM e Pytool di assemblaggio saranno definiti dopo aver raccolto gli output grezzi delle tre estrazioni.
- **Density Map:** forwarding come nel comportamento legacy osservato; non c'è ancora una specifica di estrazione richiesta.

Il vecchio `PAGE DISPATCHER` è parcheggiato e non fa parte del routing attuale. Non eliminarlo finché non viene concordato esplicitamente.

## Struttura

| Directory/file | Contenuto |
|---|---|
| [`WORKFLOW_DESIGN.md`](WORKFLOW_DESIGN.md) | Architettura corrente, collegamenti e decisioni ancora aperte |
| [`nodes/`](nodes/) | Schede di configurazione per nodi e sottopiattaforme |
| [`nodes/lv2_06_measurement_extraction_design.md`](nodes/lv2_06_measurement_extraction_design.md) | Proposta LV2 Measurement, mappatura legacy e sequenza canvas |
| [`prompts/`](prompts/) | Prompt VLM versionati |
| [`pytools/`](pytools/) | Script da incollare nei Pytool MyHydra e relativo inventario |
| [`tests/`](tests/) | Fixture anonimizzate, risultati osservati e test locali |
| [`../../legacy/double_pdf/`](../../legacy/double_pdf/) | Workflow precedente usato come riferimento; non modificare per il nuovo sviluppo |

## Canvas LV1 corrente

1. Medex `PDF TO PNG CONVERSION`.
2. Medex `MEDIA 2 CONTENT E DIVISIONE IN GRUPPI`.
3. Iniezione `DOUBLE PDF PAGE CLASSIFIER`, iterativa.
4. Pytool `DEDUPLICAZIONE`.
5. Pytool `DISPATCHER PREP`.
6. Pytool filtro `STATION_INFORMATION` → iniezione LV2 Station Information.
7. Pytool filtro `MEASUREMENT_TECHNICAL_DATA` → iniezione LV2 Measurement Data.
8. Pytool filtro `DENSITY_MAP` → Naive di forwarding.

I numeri dei nodi possono cambiare se il canvas viene riordinato; i nomi e i contratti sono il riferimento stabile. Per i placeholder e gli edge fare riferimento alle schede aggiornate e verificare l'indice sul canvas prima di incollare uno script.

## Prossimi passi

Considerare verificata la catena tecnica Station; mantenere i warning visibili e controllare i dati estratti rispetto alle pagine sorgente prima di consolidarli. Per Measurement, configurare tre estrazioni VLM parallele con tre Naive sonda, poi progettare l'assemblaggio per pagina dagli output effettivi.
