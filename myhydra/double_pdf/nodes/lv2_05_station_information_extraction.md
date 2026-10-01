# LV2 Station Information — estrazione per pagina

## Sequenza canvas attuale

La sottopiattaforma è iterativa: riceve una pagina del gruppo `STATION_INFORMATION` per iterazione.

| Nodo | Tipo | Nome descrittivo | Funzione |
|---:|---|---|---|
| 1 | Pytool | `ESTRAI CHIAVE PAGINA` | Legge il record dalla `{question}` corrente e restituisce la chiave media semplice. Script: [`../pytools/extract_page_key.py`](../pytools/extract_page_key.py). |
| 2 | Medex | `RECUPERA IMMAGINE DA CHIAVE` | `content2media` sulla chiave ricevuta dal nodo 1; configurazione in [LV2-01](lv2_01_content2media.md). |
| 4 | Visiomaru/VLM | `ESTRAI INFO STAZIONE DA IMMAGINE` | Estrae solo dati visibili nella pagina. Prompt eseguito: [v1](../prompts/station_information_extraction_v1.md). Revisione proposta: [v2](../prompts/station_information_extraction_v2.md). |
| 5 | Pytool | `ASSOCIA ESTRAZIONE ALLA PAGINA` | Associa il risultato VLM alla pagina della `{question}` corrente. Script aggiornato: [`../pytools/associate_station_extraction_to_page.py`](../pytools/associate_station_extraction_to_page.py); output VLM dall'edge #3. Accetta array, oggetto singolo o `null` e rimuove record privi di valori estratti. Revisione ancora da validare su MyHydra. |
| 3 | Naive | `OUTPUT JSON STAZIONE` | Output/sonda della sottopiattaforma; inoltra il risultato del nodo 5 (edge #4). |

I numeri sono quelli del canvas mostrato e non rappresentano l'ordine visuale dei nodi. Se cambiano collegamenti o numerazione, aggiornare edge e scheda.

## Risultato MyHydra osservato

Nella run dopo l'aggiornamento dell'associatore, le sei sequenze sono tutte associate senza `ERROR`. Sequenze 6 e 11: protocollo `ModBus TCP`; sequenza 6 inoltre nome `Sistema Analisi SO2`, IP `10.100.50.95`, porta `511`. Sequenza 7: campi scala SO2 0–300 e Temperatura fumi 0–100. Sequenze 9, 10 e 12: `station_info: []`. La sequenza 10 aveva restituito il nome stazione in una run precedente; la variabilità va verificata sull'immagine prima di consolidare il valore. Gli avvisi di classificazione in questa run restano sulle sequenze 11 e 12.

L'associazione chiave/metadati è presente nell'output. `review_required` arriva come `0`/`1`, `review_warnings` come stringa JSON serializzata. Non confondere questi campi con l'estrazione VLM; una fase successiva dovrà normalizzarli.

Fixture anonimizzata: [`../tests/case_6/outputs/observed_lv2_station_information_sanitized.json`](../tests/case_6/outputs/observed_lv2_station_information_sanitized.json).

## Stato

La catena tecnica è stata verificata su MyHydra con il Pytool aggiornato: accetta array, oggetto singolo o `null` e converte in `[]` i record senza valori. La qualità semantica resta da confrontare con le immagini e gli avvisi; non fondere dati fra pagine in questa fase.
