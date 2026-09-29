# Nodo LV1-01 — PDF2PNG

- **Tipo/nome:** Medex — `PDF TO PNG CONVERSION`
- **Input:** `question`, contenente i PDF allegati alla chat.
- **Configurazione osservata:** `{"request":"pdf2png","nume":5}{question}`
- **Significato di `nume`:** ingrandimento per facilitare la lettura, secondo la conferma dell’utente.
- **Output atteso:** pagine PDF convertite in media; il nodo non classifica né estrae contenuti.
- **Test caso 6:** 14 anteprime per due documenti da 5 e 9 pagine.
- **Da confermare:** forma completa del payload e mantenimento dell’ordine per ciascun allegato.
