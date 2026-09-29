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
| [`outputs/observed_classifier.json`](outputs/observed_classifier.json) | Risposta reale del VLM, 27 etichette su 14 iterazioni |
| [`outputs/expected_unique_page_labels.json`](outputs/expected_unique_page_labels.json) | Etichette deduplicate per chiave, 14 elementi |
| [`outputs/expected_pytool_first_window.json`](outputs/expected_pytool_first_window.json) | Risultato atteso del Pytool sul primo giro |

## Convenzioni

- I file in `outputs/` con `observed` nel nome sono stati incollati dall'utente o mostrati nel canvas.
- I file con `expected` sono risultati **derivati** dai dati osservati e servono come confronto manuale del Pytool.
- Le chiavi `CASE6_PAGE_nn` sono sintetiche e identificano solo la posizione nella sequenza; non sono chiavi Medex reali e non codificano il PDF di origine.
- Il caso 6 contiene 14 chiavi uniche e 14 finestre sovrapposte: ogni finestra tranne l'ultima ha due chiavi, con overlap di una chiave.

Lo Pytool non elimina l'overlap tra finestre: la deduplicazione deve avvenire dopo il ciclo del Livello 1, usando la chiave media come identità tecnica.

## Stato

La suite non è stata eseguita contro il runtime MyHydra. I file sono fixture e documentazione per la verifica manuale sulla piattaforma. L'esecuzione reale del Pytool resta da verificare.
