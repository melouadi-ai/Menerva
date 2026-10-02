# Caso di prova 6

Caso `Mappatura_6_Cliente_SMI_1` della coppia IOL + JOB. Raccoglie le evidenze osservate sui due livelli e le fixture verificatesi.

## Input

- `Mappatura_6_Cliente_SMI_1.pdf` — 5 pagine.
- `Mappatura_6_Descrizione_Cliente_SMI_1.pdf` — 9 pagine.

## Evidenze osservate — Livello 1

- Il primo Medex visualizza 14 anteprime totali con `nume:5` (fattore di ingrandimento dichiarato dall'utente).
- Il secondo Medex produce 14 finestre/elementi con 14 chiavi media uniche e sovrapposizione di una chiave tra finestre adiacenti.
- Il motore iterativo esegue 14 giri nel test osservato.
- I prefissi opachi non identificano in modo stabile il confine dei PDF: catture diverse hanno mostrato cardinalità 9+5 e 12+2. Non usarli per attribuire pagine ai file.

Il payload completo di chiavi runtime è effimero e non viene archiviato. La forma sanitizzata delle finestre è in [`inputs/medex_windows_sanitized.json`](inputs/medex_windows_sanitized.json). Nell’ultima diagnostica, `{question}` e edge #2 risultano JSON validi in tutte le 14 iterazioni.

## Fixture

| File | Ruolo |
|---|---|
| [`inputs/medex_windows_sanitized.json`](inputs/medex_windows_sanitized.json) | Le 14 finestre sovrapposte, con chiavi sintetiche |
| [`inputs/pytool_first_window.json`](inputs/pytool_first_window.json) | Payload del primo giro, usato come input del Pytool |
| [`outputs/observed_classifier.json`](outputs/observed_classifier.json) | Risposta reale del VLM v1, 27 categorie su 14 iterazioni; non contiene il ruolo IOL/JOB |
| [`outputs/observed_pytool_sanitized.json`](outputs/observed_pytool_sanitized.json) | Output storico del Pytool v1, con chiavi runtime sostituite da ID sintetici |
| [`outputs/observed_dedup_sanitized.json`](outputs/observed_dedup_sanitized.json) | Output LV1 storico osservato nel nodo Naive; categoria conservata, ruolo non classificato |
| [`outputs/observed_role_v2_conflict_sanitized.json`](outputs/observed_role_v2_conflict_sanitized.json) | Errore reale della prova v2, sanitizzato: stesso ruolo ma categorie diverse per una chiave sovrapposta |
| [`outputs/observed_role_v2_dedup_sanitized.json`](outputs/observed_role_v2_dedup_sanitized.json) | Output runtime dopo la regola aggiornata: 14 pagine, ruoli IOL/JOB e due conflitti di categoria segnalati |
| [`outputs/observed_prepare_pages_clean_sanitized.json`](outputs/observed_prepare_pages_clean_sanitized.json) | Output osservato del nuovo Pytool preparatore: array root di 14 pagine, nessun avviso in questa esecuzione |
| [`outputs/observed_dispatch_injection_probe_sanitized.json`](outputs/observed_dispatch_injection_probe_sanitized.json) | Prova runtime dell'iniezione LV2: 14 input `SINGLE_PAGE`, ciascuno con una sola pagina |
| [`outputs/observed_lv1_filtered_branches_sanitized.json`](outputs/observed_lv1_filtered_branches_sanitized.json) | Output runtime dei filtri LV1: 6 Station, 7 Measurement, 1 Density, con chiavi sostituite da ID sintetici |
| [`outputs/observed_lv2_station_information_sanitized.json`](outputs/observed_lv2_station_information_sanitized.json) | Output runtime LV2 Station Information su 6 pagine, chiavi anonimizzate |
| [`outputs/observed_lv2_station_information_v2_sanitized.json`](outputs/observed_lv2_station_information_v2_sanitized.json) | Output runtime con prompt v2: un errore di formato e un oggetto senza campi, chiavi anonimizzate |
| [`outputs/observed_lv2_station_information_v2_associated_sanitized.json`](outputs/observed_lv2_station_information_v2_associated_sanitized.json) | Run successiva con associatore aggiornato: 6 record senza errori, chiavi anonimizzate |
| [`outputs/observed_lv2_measurement_light_model_measures_sanitized.json`](outputs/observed_lv2_measurement_light_model_measures_sanitized.json) | Run Measurement con VLM leggero (non Qwen 3.8): 9 record `OK` ma `vlm_output` sempre vuoto, anche sulle IOL con tabelle; i rami BITINFO/STATES non sono stati raccolti |
| [`outputs/observed_lv2_measurement_qwen38_measures_rerun_sanitized.json`](outputs/observed_lv2_measurement_qwen38_measures_rerun_sanitized.json) | Run Measurement con Qwen 3.8: 7 record, zero righe estratte (gusci placeholder SME, 6 con fence); pagina 5 `[]`; rami BITINFO/STATES non ancora acquisiti |
| [`outputs/expected_unique_page_labels.json`](outputs/expected_unique_page_labels.json) | Etichette deduplicate per chiave, 14 elementi |
| [`outputs/expected_pytool_first_window.json`](outputs/expected_pytool_first_window.json) | Risultato atteso del Pytool sul primo giro |

## Convenzioni

- I file in `outputs/` con `observed` nel nome sono stati incollati dall'utente o mostrati nel canvas.
- I file con `expected` sono risultati **derivati** dai dati osservati e servono come confronto manuale del Pytool.
- Le chiavi `CASE6_PAGE_nn` sono sintetiche e identificano solo la posizione nella sequenza; non sono chiavi Medex reali e non codificano il PDF di origine.
- Il caso 6 contiene 14 chiavi uniche e 14 finestre sovrapposte: ogni finestra tranne l'ultima ha due chiavi, con overlap di una chiave.

Il Pytool ha restituito `status: OK` in tutte le 14 finestre. Le prime 13 contengono due associazioni e l'ultima una (27 associazioni totali); le etichette ripetute delle chiavi di overlap concordano. Lo Pytool non elimina l'overlap: la deduplicazione deve avvenire dopo il ciclo LV1, usando la chiave media come identità tecnica.

La catena LV1 fino al nodo Naive è stata verificata su MyHydra: il suo output è `status: OK`, `page_count: 14`; la fixture sanitizzata è in `outputs/observed_dedup_sanitized.json`.

Quella verifica usava la classificazione v1. Nella successiva prova con il ruolo v2, la prima versione del deduplicatore ha fermato l'elaborazione perché la stessa chiave risultava `JOB/STATION_INFORMATION` in una finestra e `JOB/MEASUREMENT_TECHNICAL_DATA` nell'altra. I log intermedi permetterebbero di investigare la causa, ma recuperarli richiederebbe una nuova run.

Dato che ottenere i risultati intermedi richiederebbe una nuova run, la regola è stata aggiornata senza chiedere altri output: categoria discordante → priorità legacy con avviso; ruolo discordante → `UNKNOWN` con avviso. La nuova regola è verificata localmente; la fixture di errore sopra conserva la risposta della prima versione del deduplicatore.

Nella successiva run MyHydra, la regola aggiornata ha restituito `status: OK`, 14 pagine e `review_required: true`. Il classificatore ha assegnato le prime 5 pagine al ruolo `IOL` e le successive 9 a `JOB`, in accordo con le lunghezze dei due PDF del caso 6. Due chiavi hanno ricevuto categorie discordanti nelle finestre sovrapposte; entrambe sono state risolte come `STATION_INFORMATION` secondo la priorità legacy e incluse in `warnings`. L'output anonimizzato è in `outputs/observed_role_v2_dedup_sanitized.json`.

In una run successiva, il nuovo Pytool di preparazione ha prodotto direttamente un array root con 14 record, conservando chiavi, sequenza, ruolo e categoria. In questa esecuzione non sono comparsi conflitti: tutti i record hanno `review_required: false` e `review_warnings: []`. L'output anonimizzato è in `outputs/observed_prepare_pages_clean_sanitized.json`. Le due osservazioni vanno mantenute entrambe: la classificazione sui duplicati sovrapposti può variare tra run.

La prova dell'iniezione LV2 ha confermato 14 chiamate con `input_kind: SINGLE_PAGE`, indici 1–14 e una chiave distinta per chiamata. Il ruolo è stato assegnato a 5 pagine IOL e 9 JOB. In questa run le categorie sono 1 `DENSITY_MAP`, 8 `MEASUREMENT_TECHNICAL_DATA` e 5 `STATION_INFORMATION`. Rispetto alla precedente run pulita è cambiata l'etichetta alla posizione 11; altre acquisizioni avevano mostrato variazioni alle posizioni 11 e 12. Fixture anonimizzata: `outputs/observed_dispatch_injection_probe_sanitized.json`.

Nella run più recente dei filtri LV1 del caso 6, l'output osservato ha instradato 6 pagine Station (indici 6, 7, 9, 10, 11, 12), 7 Measurement (2, 3, 4, 5, 8, 13, 14) e 1 Density Map (1). Gli indici da 1 a 14 risultano coperti una sola volta. Le pagine Station 11 e 12 conservano i rispettivi avvisi di classificazione discordante. Fixture sanitizzata: `outputs/observed_lv1_filtered_branches_sanitized.json`. Questa verifica riguarda il routing e la conservazione dei metadati, non l'estrazione delle LV2.

La successiva run LV2 Station Information ha restituito 6 record associati alle pagine 6, 7, 9, 10, 11 e 12. La pagina 6 ha prodotto protocollo `ModBus TCP`, IP PLC `10.100.50.95` e porta `511`; la pagina 7 ha prodotto due campi scala (SO2 0–300 e Temperatura fumi 0–100). La pagina 10 ha restituito `station_info: []`. Le pagine 9, 11 e 12 hanno invece prodotto un oggetto con tutti i campi null e `campi_scala: []`; il prompt va reso più esplicito per evitare questi oggetti vuoti. Le pagine 11 e 12 mantengono gli avvisi di classificazione del LV1. Nel payload osservato `review_required` è numerico e `review_warnings` è una stringa JSON serializzata; non normalizzare silenziosamente questi tipi nella fixture. Output anonimizzato: `outputs/observed_lv2_station_information_sanitized.json`.

La successiva run con il prompt v2 ha prodotto dati parziali nelle sequenze 6, 7, 10 e 11. Sequenza 6: nome `Sistema Analisi SO2`, protocollo `ModBus TCP`, IP PLC `10.100.50.95`, porta `511`. Sequenza 7: due campi scala, SO2 0–300 e Temperatura fumi 0–100. Sequenza 10: nome `Sistema Analisi SO2`. Sequenza 11: protocollo `ModBus TCP`. Sequenza 9 è in errore perché il JSON decodificato dal VLM non era un array; il messaggio non rivela quale tipo sia stato restituito. Sequenza 12 ha ancora un oggetto con tutti i campi null e `campi_scala: []`, nonostante la regola v2. Solo la sequenza 12 ha un avviso di categoria in questa run. La variazione rispetto ai warning precedenti conferma che le classificazioni possono cambiare tra run. I tipi runtime dei metadati restano numerici/stringificati. Fixture anonimizzata: `outputs/observed_lv2_station_information_v2_sanitized.json`.

Nella run successiva, con il Pytool associatore aggiornato, tutte e sei le pagine hanno un output associato senza `ERROR`: le sequenze 6, 7 e 11 contengono dati; 9, 10 e 12 restituiscono `station_info: []`. La sequenza 6 contiene nome `Sistema Analisi SO2`, protocollo `ModBus TCP`, IP PLC `10.100.50.95` e porta `511`; la 7 contiene SO2 0–300 e Temperatura fumi 0–100; la 11 contiene protocollo `ModBus TCP`. La sequenza 10 aveva restituito il nome in una run precedente, quindi confrontare con l'immagine prima di considerarlo stabile. In questa run i conflitti di categoria sono sulle sequenze 11 e 12. Fixture anonimizzata: `outputs/observed_lv2_station_information_v2_associated_sanitized.json`.

Una run Measurement con VLM leggero (modello cambiato globalmente, non Qwen 3.8) ha prodotto 9 record `OK` nel ramo `MEASURES_BISON`, tutti con `vlm_output: []` — anche sulle pagine IOL 2–4, che contengono tabelle `DESCRIZIONE`/`REG`/`BIT` da 2000–3000 caratteri. Meccanica verificata (envelope, branch, pagina, JSON senza fence), estrazione inutilizzabile. In quella run le pagine Measurement erano 9 (2,3,4,5,8,11,12,13,14) perché anche il classifier girava sul modello leggero. Fixture anonimizzata (solo ramo misure; BITINFO/STATES non raccolti): `outputs/observed_lv2_measurement_light_model_measures_sanitized.json`. Regola: modello leggero solo per prove di plumbing, confronti solo a parità di modello.

## Stato

Il Pytool è stato eseguito nel runtime MyHydra con esito positivo per tutte le finestre e la nuova regola di deduplicazione ha completato la run. La fixture sanitizzata conserva il risultato senza memorizzare le chiavi runtime. I test locali verificano parsing e associazione senza invocare MyHydra o il VLM. L'output è utilizzabile, ma `review_required: true` segnala che le due pagine discordanti vanno controllate prima di affidarsi alle relative categorie.
