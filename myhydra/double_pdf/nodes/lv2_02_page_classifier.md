# Nodo LV2-02 — Classificatore pagine

- **Tipo/nome:** Visiomaru/VLM.
- **Prompt:** [`../prompts/page_classifier_v1.md`](../prompts/page_classifier_v1.md).
- **Input:** immagini prodotte dal nodo LV2-01.
- **Output:** un JSON con un oggetto `pages` per ogni immagine ricevuta; indici zero-based locali al giro.
- **Classi ammesse:** `STATION_INFORMATION`, `MEASUREMENT_TECHNICAL_DATA`, `DENSITY_MAP`.
- **Non fa:** estrazione dei campi o generazione ADAS.
- **Test caso 6:** 14 iterazioni, 13 coppie e un giro finale a immagine singola; overlap classificati in modo coerente.
