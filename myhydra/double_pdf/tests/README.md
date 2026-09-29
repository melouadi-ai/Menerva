# Convenzioni per i test LV2

- Gli output marcati `observed` sono stati incollati dall’utente o mostrati nel canvas.
- Gli output `expected` sono risultati derivati dai dati osservati e servono come confronto manuale del Pytool.
- Le chiavi `CASE6_PAGE_nn` sono sintetiche e identificano solo la posizione nella sequenza; non sono chiavi Medex reali e non codificano il PDF di origine.
- Il caso 6 contiene 14 chiavi uniche e 14 finestre sovrapposte: ogni finestra tranne l’ultima ha due chiavi, con overlap di una chiave.
- Il contenuto di `outputs/observed_classifier.json` conserva tutte le 27 etichette osservate, una risposta per iterazione.
- `outputs/expected_unique_page_labels.json` deduplica le etichette per chiave e deve contenere 14 elementi.
- La suite non è stata eseguita qui; i file sono fixture/documentazione per la verifica sul runtime MyHydra.
