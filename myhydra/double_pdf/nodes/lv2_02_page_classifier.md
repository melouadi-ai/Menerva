# Nodo LV2-02 — Classificatore pagine

- **Tipo/nome:** Visiomaru/VLM.
- **Prompt corrente:** [`../prompts/page_classifier_v2_role_and_type.md`](../prompts/page_classifier_v2_role_and_type.md). La v1 è conservata come baseline dei risultati precedenti.
- **Input:** immagini prodotte dal nodo LV2-01.
- **Output:** un JSON con un oggetto `pages` per ogni immagine ricevuta; ogni pagina ha indice zero-based locale, `document_role` e `label`.
- **Ruoli documento:** `IOL`, `JOB`, `UNKNOWN`; determinati dalle evidenze visive di quella pagina, mai dall'ordine casuale di upload.
- **Classi ammesse:** `STATION_INFORMATION`, `MEASUREMENT_TECHNICAL_DATA`, `DENSITY_MAP`.
- **Non fa:** estrazione dei campi o generazione ADAS.
- **Test caso 6:** 14 iterazioni, 13 coppie e un giro finale a immagine singola.
- **Run v2 su MyHydra:** il risultato deduplicato assegna 5 pagine a `IOL` e 9 a `JOB`, in accordo con i due PDF noti del caso 6. Alcune run hanno mostrato una o due categorie discordanti sulle finestre sovrapposte; il deduplicatore le risolve con la priorità legacy e le segnala per revisione.
