# Prompt — Double PDF

## Inventario

| File | Versione | Nodo | Stato |
|---|---|---|---|
| [`page_classifier_v1.md`](page_classifier_v1.md) | `v1` | LV2-02 — classificatore pagine | Baseline storica senza classificazione del ruolo IOL/JOB. |
| [`page_classifier_v2_role_and_type.md`](page_classifier_v2_role_and_type.md) | `v2` | LV2-02 — ruolo documento e categoria pagina | In uso; eseguito su MyHydra nei casi 6 e 7. Alcune pagine di confine hanno avvisi di categoria. |
| [`station_information_extraction_v1.md`](station_information_extraction_v1.md) | `v1` | LV2 Station Information — estrazione singola pagina | Eseguito su MyHydra; ha prodotto dati parziali, ma tre oggetti vuoti hanno evidenziato una regola da chiarire. |
| [`station_information_extraction_v2.md`](station_information_extraction_v2.md) | `v2` | LV2 Station Information — estrazione singola pagina | Eseguito su MyHydra. Con associatore aggiornato, una run ha 3 pagine con dati e 3 `[]`; pagina 10 variabile fra run. |

## Prompt Measurement in preparazione

La progettazione della LV2 Measurement prevede tre VLM indipendenti che ricevono la stessa immagine della pagina: misure/BISON, nomi/bitinfo digitali e stati `TEXTON/TEXTOFF`. I prompt saranno scritti in file versionati dopo aver confermato la sequenza dei nodi sul canvas; per la prima run ogni uscita sarà inoltrata a un Naive distinto, così gli schemi reali precedono il Pytool di assemblaggio. La scheda è [`../nodes/lv2_06_measurement_extraction_design.md`](../nodes/lv2_06_measurement_extraction_design.md).

## Scopo del prompt

Il classificatore riceve una o più immagini di pagina e assegna a ciascuna un ruolo documento (`IOL`, `JOB`, `UNKNOWN`) e una categoria (`STATION_INFORMATION`, `MEASUREMENT_TECHNICAL_DATA`, `DENSITY_MAP`). I due campi sono indipendenti. La v2 è stata eseguita nel runtime sui casi 6 e 7; le discrepanze sulle pagine sovrapposte sono risolte dal deduplicatore con avvisi.

Non estrae dati e non produce testo libero: restituisce un solo oggetto JSON con la chiave `pages`, una voce per immagine, con indice locale in base zero, ruolo e categoria. La v1 rimane la baseline storica.

Il prompt Station Information è distinto dal classificatore: viene eseguito nella LV2 dedicata e deve restituire un array JSON per la singola pagina. Non applicare il default legacy `SME` pagina per pagina; il prompt lo lascia alla fase di consolidamento. La v2 e il Pytool di associazione sono stati provati nel runtime; controllare la pagina 10 rispetto all'immagine perché il suo output varia tra run.

## Regole di versione

- Ogni modifica al prompt crea un file nuovo con suffisso `_vN`; i file precedenti non vengono modificati.
- Le schede dei nodi in [`../nodes/`](../nodes/) referenziano il prompt in uso tramite link, mai per numero di versione in testo.
- Una modifica al prompt invalida le fixture di `../tests/`: i risultati in `outputs/observed_*` vanno rigenerati e i `expected_*` ricalcolati.
