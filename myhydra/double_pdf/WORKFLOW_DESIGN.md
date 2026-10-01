# Workflow Double PDF — stato della progettazione

**Ambito:** nuova implementazione MyHydra in `myhydra/double_pdf/`. Il workflow legacy in `legacy/double_pdf/` resta intatto e viene usato come riferimento funzionale.

## Architettura attuale

MyHydra non espone il nome del PDF di origine e i file caricati possono arrivare in ordine casuale. Il classificatore VLM assegna quindi a ogni pagina sia `document_role` (`IOL`, `JOB` o `UNKNOWN`) sia `label` (tipo pagina). Il routing usa la `label`; il ruolo resta nei metadati per l'elaborazione successiva.

```mermaid
flowchart TD
  A[Medex PDF to PNG] --> B[Medex media2content e finestre]
  B --> C[Iniezione LV2 iterativa Page Classifier]
  C --> D[Pytool deduplicazione LV1]
  D --> E[Naive output LV1]
  D --> F[Pytool Dispatcher Prep]
  F --> G[Pytool filtro STATION_INFORMATION]
  F --> H[Pytool filtro MEASUREMENT_TECHNICAL_DATA]
  F --> I[Pytool filtro DENSITY_MAP]
  G --> J[Iniezione LV2 Station Information]
  H --> K[Iniezione LV2 Measurement Data]
  I --> L[Naive forwarding Density Map]
  subgraph S[LV2 Station Information — iterativa]
    J --> S1[Pytool estrae la chiave pagina]
    S1 --> S2[Medex content2media]
    S2 --> S3[VLM estrae dati stazione]
    S3 --> S4[Pytool associa estrazione e pagina]
    S4 --> S5[Naive output/debug]
  end
```

Il diagramma riporta i nodi verificati; lo screenshot conferma il cablaggio della LV2 Measurement con un Pytool, un Medex, tre VLM paralleli, tre Pytool etichettatori e tre Naive distinti. Le Powered identity attuali e gli script aggiornati sono raccolti in [`platforms/lv2/measurement/`](platforms/lv2/measurement/); la nuova configurazione dei campi VLM e i relativi payload sono ancora da verificare a runtime. La sottopiattaforma `PAGE DISPATCHER`, progettata in precedenza per restituire stringhe e attivare rami condizionali, è parcheggiata: i filtri Pytool per etichetta l'hanno resa superflua per la configurazione corrente.

## Stato delle verifiche

| Fase | Evidenza | Stato |
|---|---|---|
| Classificazione e associazione chiave/ruolo/categoria | Run MyHydra dei casi 6 e 7 | Verificata, con avvisi di revisione su alcune categorie |
| Deduplicazione delle finestre sovrapposte | 14 pagine caso 6, 11 pagine caso 7 | Verificata; i conflitti di categoria vengono risolti con priorità legacy e restano negli avvisi |
| Preparazione dell'array root e iterazione LV2 | 14 input `SINGLE_PAGE` nel caso 6 | Verificata in una run diagnostica |
| Filtri e inoltro alle tre destinazioni | Output MyHydra: 6 Station, 7 Measurement, 1 Density nel caso 6 | Verificata in una run; gli indici 1–14 risultano partizionati una sola volta |
| Recupero immagine da chiave nel ramo Station | Medex ha mostrato le sei immagini Station | Verificata per il ramo osservato |
| Estrazione Station e associazione ai metadati | Dopo l'aggiornamento dell'associatore, tutte le 6 pagine terminano senza errori. Dati nelle pagine 6, 7 e 11; `[]` nelle 9, 10 e 12. | Catena tecnica verificata; classificazione e valori da revisionare |
| Estrazione Measurement | Cablaggio a tre VLM paralleli e tre Pytool etichettatori confermato da screenshot; prompt Powered identity v3 preparati | Prompt immagine `{edge.media}[2]`, `[3]`, `[4]`; nuova configurazione da riverificare |
| Aggregazione e JSON finale | Non implementati nel nuovo workflow | Da progettare dopo le estrazioni |

Le esecuzioni MyHydra possono restituire classificazioni diverse tra run sulle pagine di confine. I fixture anonimizzati conservano risultati distinti; un risultato osservato non va trattato come ground truth se ha `review_required: true`.

## Contratti dei passaggi LV1

1. Il classificatore produce record con chiave media, `sequence_index`, `document_role` e `label`.
2. Il deduplicatore LV1 collassa solo la stessa chiave media ripetuta dalle finestre sovrapposte. Non unisce pagine o dati semanticamente simili.
3. Il preparatore restituisce l'array root di record pagina, propagando `review_required` e `review_warnings`.
4. I filtri sono Pytool non iterativi e conservano il record intero. Leggono rispettivamente gli edge di input #5 (Station), #7 (Measurement) e #6 (Density), secondo la configurazione documentata al momento dell'ultima prova. Gli indici edge sono locali al canvas: ricontrollarli se si modificano i collegamenti.
5. Le due iniezioni LV2 classificazione/estrazione iterano sulle pagine del rispettivo filtro. Il forwarding Density Map non trasforma il record.

Gli script e i prompt sono organizzati per sottopiattaforma in [`platforms/`](platforms/); i collegamenti e le impostazioni dei nodi sono raccolti in [`nodes/`](nodes/).

## Contratto corrente LV2 Station Information

Il contesto iterativo `{question}` porta il record pagina originale e la sua chiave. Il Pytool estrae la chiave; Medex `content2media` la risolve in immagine. Nel VLM inserire `{edge.media}[n]` da solo nel campo **Prompt** (indice dell'edge Medex→VLM), lasciare **Context** vuoto e mettere le istruzioni nel **Powered identity**. Non incorporare il token media nelle istruzioni. Il Pytool finale associa l'array JSON VLM al record pagina e preserva ruolo, etichetta, sequenza e avvisi.

Il VLM lavora sulla singola immagine della pagina corrente. Il token media va nel campo **Prompt**, le istruzioni nel **Powered identity**, e **Context** resta vuoto. Se la pagina non contiene informazioni Station, il prompt richiede `[]`; se un campo non è presente, non va inventato. Il valore predefinito legacy `SME` non deve essere sintetizzato in ogni singola pagina: eventuale normalizzazione si decide nel consolidamento. La scheda completa è in [`nodes/lv2_05_station_information_extraction.md`](nodes/lv2_05_station_information_extraction.md). La v2 è stata eseguita prima di separare i campi; configurazione e prompt correnti sono in [`platforms/lv2/station_information/`](platforms/lv2/station_information/), ancora da riverificare.

**Esito della v2:** nel primo output, pagina 9 aveva un payload non-array e pagina 12 un oggetto vuoto. L'associatore aggiornato gestisce array, oggetto singolo o `null` e scarta oggetti senza valori. Nella run successiva tutte le sei iterazioni hanno prodotto un record associato senza `ERROR`: dati nelle pagine 6, 7 e 11; `station_info: []` nelle pagine 9, 10 e 12. Il risultato della pagina 10 varia tra run (prima conteneva il nome, poi `[]`), perciò controllare l'immagine prima di consolidare quel campo. In questa run gli avvisi di classificazione sono alle pagine 11 e 12; mantenerli separati dai dati VLM. Fixture prima run: `tests/case_6/outputs/observed_lv2_station_information_v2_sanitized.json`; run successiva: `tests/case_6/outputs/observed_lv2_station_information_v2_associated_sanitized.json`.

I campi recuperati sono distribuiti tra pagine: pagina 6 contiene protocollo, IP e porta PLC; pagina 7 contiene due intervalli `campi_scala` (SO2 e Temperatura fumi). L'assenza degli altri campi in quei record non va completata con inferenze locali: l'associazione/aggregazione fra pagine va progettata in seguito.

Nell'output MyHydra `review_required` appare come numero (`0`/`1`) e `review_warnings` come stringa JSON (`"[ ]"` o array serializzato), mentre `station_info` è un array JSON. Registrare questa differenza di tipo e normalizzare i metadati in un Pytool deterministico prima dell'aggregazione/final output.

## Prossime fasi

1. Confrontare i campi estratti Station con le pagine sorgente e mantenere i warning sulle pagine 11 e 12.
2. Normalizzare `review_required` e `review_warnings` in modo esplicito prima dell'aggregazione.
3. Configurare la LV2 Measurement secondo la scheda dedicata: per ogni VLM mettere `{edge.media}[n]` nel campo Prompt, lasciare Context vuoto e incollare la Powered identity indicata; poi raccogliere gli output grezzi per progettare l'assemblaggio per pagina.
4. Definire come associare estrazioni Station e Measurement usando evidenze dei documenti, senza dedurre il PDF dal prefisso della chiave.
5. Implementare aggregazione, revisione degli avvisi, normalizzazione e output finale solo dopo aver stabilizzato le estrazioni per pagina.

## Elementi parcheggiati

- La piattaforma `PAGE DISPATCHER` e gli script `dispatch_classified_pages.py` e `diagnose_dispatch_injection.py` sono rimasti nel progetto come materiale diagnostico/storico. Non fanno parte del percorso LV1 corrente.
- Non eliminare la piattaforma MyHydra `PAGE DISPATCHER` finché non è completata la verifica dei rami attuali e l'utente non dà l'indicazione concordata.
- Non modificare il legacy durante gli aggiornamenti del progetto nuovo.
