# Caso di prova 7

Coppia `Mappatura_7_Cliente_SMI_2` e `Mappatura_7_Descrizione_Cliente_SMI_2`, usata per verificare che il classificatore di ruolo generalizzi oltre il caso 6.

## Input e risultato

- `Mappatura_7_Cliente_SMI_2.pdf`: 4 pagine.
- `Mappatura_7_Descrizione_Cliente_SMI_2.pdf`: 7 pagine.
- L'output LV1 osservato contiene 11 pagine uniche: 4 classificate `IOL`, poi 7 `JOB`. I conteggi corrispondono alle lunghezze dei due PDF; le chiavi non conservano il nome del file, quindi l'attribuzione di ruolo è basata sulla classificazione visiva.
- Esito: `status: OK`, `review_required: true`, un conflitto di categoria all'indice 10, risolto come `STATION_INFORMATION` con la priorità legacy.

Output anonimizzato: [`outputs/observed_role_v2_dedup_sanitized.json`](outputs/observed_role_v2_dedup_sanitized.json). Le chiavi Medex effimere sono state sostituite con `CASE7_PAGE_nn`.

## Lettura

Il caso 7 supporta la distinzione dei ruoli su una seconda coppia e con conteggi diversi dal caso 6. Resta un singolo avviso di categoria sulle finestre sovrapposte: la pagina corrispondente va verificata visivamente prima di considerare definitiva l'etichetta. Il risultato non dimostra da solo il comportamento su tutte le possibili coppie o layout.
