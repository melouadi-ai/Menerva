# Caso di prova 7

Coppia `Mappatura_7_Cliente_SMI_2` e `Mappatura_7_Descrizione_Cliente_SMI_2`, usata per verificare che il classificatore di ruolo generalizzi oltre il caso 6.

## Input e risultato

- `Mappatura_7_Cliente_SMI_2.pdf`: 4 pagine.
- `Mappatura_7_Descrizione_Cliente_SMI_2.pdf`: 7 pagine.
- L'output LV1 osservato contiene 11 pagine uniche: 4 classificate `IOL`, poi 7 `JOB`. I conteggi corrispondono alle lunghezze dei due PDF; le chiavi non conservano il nome del file, quindi l'attribuzione di ruolo è basata sulla classificazione visiva.
- Esito: `status: OK`, `review_required: true`, un conflitto di categoria all'indice 10, risolto come `STATION_INFORMATION` con la priorità legacy.

Output anonimizzato: [`outputs/observed_role_v2_dedup_sanitized.json`](outputs/observed_role_v2_dedup_sanitized.json). Le chiavi Medex effimere sono state sostituite con `CASE7_PAGE_nn`.

## Uscita ADAS 3.8 (5/10/2026)

Run canvas completa fino al nodo 12: [`outputs/observed_adas_case7_qwen38.json`](outputs/observed_adas_case7_qwen38.json) — stazione `172.16.1.31:511`, 39 misure (4 packed + 18 analogiche + 9 singoli + 8 stimate), 42 bitinfo, linkage intatto, 5 variabili scartate con warning (`Impianto in spegnimento/lavaggio/manutenzioni/fuori servizio`: REG nullo a inizio foglio, carry-over cross-pagina non risolvibile in LV2). Verifiche: bit wrap REG 1 (16 righe), bianche saltate, comandi/stimate tutti presenti; aperto il formato analogico delle misure INT senza `data_type` (250 = default, da decidere).

## Lettura

Il caso 7 supporta la distinzione dei ruoli su una seconda coppia e con conteggi diversi dal caso 6. Resta un singolo avviso di categoria sulle finestre sovrapposte: la pagina corrispondente va verificata visivamente prima di considerare definitiva l'etichetta. Il risultato non dimostra da solo il comportamento su tutte le possibili coppie o layout.
