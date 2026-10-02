# Double PDF — progetto MyHydra

Questa directory documenta e raccoglie l'implementazione nuova del workflow Double PDF. Il legacy rimane in [`../../legacy/double_pdf/`](../../legacy/double_pdf/) come riferimento e non viene modificato da questo progetto.

## Stato attuale

- **LV1, classificazione e deduplicazione:** verificata su MyHydra. Il caso 6 ha prodotto 14 pagine uniche; il caso 7 ne ha prodotte 11. I conflitti di classificazione restano visibili come avvisi.
- **LV1, instradamento per etichetta:** i tre Pytool filtrano i record completi usando `label`. `STATION_INFORMATION` e `MEASUREMENT_TECHNICAL_DATA` vanno alle rispettive LV2 iterative; `DENSITY_MAP` viene inoltrata con un Naive.
- **Passaggio LV1→LV2:** verificato in una run del caso 6. I rami hanno ricevuto rispettivamente 6 pagine Station, 7 Measurement e 1 Density; le chiavi e i metadati sono rimasti associati alle pagine.
- **Campi dei VLM:** l'immagine `{edge.media}[n]` va nel campo **Prompt**; **Context** resta vuoto; le istruzioni di estrazione vanno in **Powered identity**. Le nuove versioni dei prompt documentano esplicitamente questa separazione.
- **LV2 Station Information:** una run precedente con il Pytool associatore aggiornato ha associato tutte e 6 le pagine senza errori; 3 hanno estrazioni e 3 restituiscono `[]`. Le istruzioni Powered identity v4 sono pronte per Prompt `{edge.media}[2]`; non ancora riverificate dopo la separazione dei campi.
- **LV2 Measurement Data:** la run Qwen 3.8 del ramo misure associa correttamente 7 output alle pagine, ma non estrae righe. Prima di progettare l'assemblaggio, verificare la lettura dell'immagine con una prova breve di trascrizione.
- **Density Map:** forwarding come nel comportamento legacy osservato; non c'è ancora una specifica di estrazione richiesta.

Il vecchio `PAGE DISPATCHER` è parcheggiato e non fa parte del routing attuale. Non eliminarlo finché non viene concordato esplicitamente.

## Struttura

| Directory/file | Contenuto |
|---|---|
| [`WORKFLOW_DESIGN.md`](WORKFLOW_DESIGN.md) | Architettura corrente, collegamenti e decisioni ancora aperte |
| [`nodes/`](nodes/) | Schede di configurazione per nodi e sottopiattaforme |
| [`platforms/`](platforms/) | Materiali organizzati per platform e sottopiattaforma |
| [`platforms/lv1/`](platforms/lv1/) | Script LV1 divisi tra in uso, parcheggiati e diagnostici |
| [`platforms/lv2/`](platforms/lv2/) | Prompt e script organizzati dentro ciascuna sottopiattaforma |
| [`nodes/lv2_06_measurement_extraction_design.md`](nodes/lv2_06_measurement_extraction_design.md) | Progettazione LV2 Measurement, collegamenti e mappatura dei payload |
| [`tests/`](tests/) | Fixture anonimizzate, risultati osservati e test locali |
| [`../../legacy/double_pdf/`](../../legacy/double_pdf/) | Workflow precedente usato come riferimento; non modificare per il nuovo sviluppo |

Per trovare subito cosa copiare in MyHydra, entra nella cartella della sottopiattaforma e usa `prompts/current/` oppure `scripts/in_use/`. Gli script non ancora verificati sono in `scripts/updated_pending_validation/`; le versioni precedenti sono in `prompts/history/` o `scripts/history/`. Ogni cartella platform contiene un README con lo stato e l'elenco dei file.

## Canvas LV1 corrente

1. Medex `PDF TO PNG CONVERSION`.
2. Medex `MEDIA 2 CONTENT E DIVISIONE IN GRUPPI`.
3. Iniezione `DOUBLE PDF PAGE CLASSIFIER`, iterativa.
4. Pytool `DEDUPLICAZIONE`.
5. Pytool `DISPATCHER PREP`.
6. Pytool filtro `STATION_INFORMATION` → iniezione LV2 Station Information.
7. Pytool filtro `MEASUREMENT_TECHNICAL_DATA` → iniezione LV2 Measurement Data.
8. Pytool filtro `DENSITY_MAP` → Naive di forwarding.

I numeri dei nodi possono cambiare se il canvas viene riordinato; i nomi e i contratti sono il riferimento stabile. Per i placeholder e gli edge fare riferimento alle schede aggiornate e verificare l'indice sul canvas prima di incollare uno script. I codici media VLM vanno nel campo **Prompt**; le istruzioni vanno in **Powered identity**.

## Prossimi passi

Per Station, mantenere i warning visibili e controllare i valori estratti rispetto alle pagine sorgente prima di consolidarli. Per Measurement, usare prima la sonda breve di leggibilità della tabella; procedere alla semplificazione dell'estrazione solo dopo aver visto che il VLM trascrive correttamente il contenuto immagine.
