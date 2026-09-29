# Nodo LV1-01 — PDF2PNG

- **Tipo/nome:** Medex — conversione PDF in immagini.
- **Input:** `question`, contenente il PDF allegato alla chat. Nel legacy la variabile usata era `question.media`.
- **Configurazione osservata:** `{"request":"pdf2png","nume":3}{question}`
- **Significato di `nume`:** fattore di ingrandimento della conversione, dichiarato dall'utente. Il legacy usava `3`, il flusso Double PDF osservato usa `5`. **DA CONFERMARE** quale valore usare per il Single PDF sulla piattaforma corrente.
- **Output atteso:** una immagine per pagina del PDF.
- **Vincoli:** il nodo non classifica e non estrae nulla. Non deve interpretare il contenuto delle pagine.
- **Stato:** configurazione nota, ereditata dal legacy. Non è stato osservato un canvas Single PDF aggiornato con questo nodo.
- **Da confermare:** forma completa del payload di output e mantenimento dell'ordine delle pagine.
- **Riferimenti:** [`../test/`](../test/) per i casi; [ADR-001](../../../docs/architettura/ADR-001-merge-multi-page.md) per la posizione del nodo nella catena.
