# Nodo LV2-01 — CONTENT2MEDIA

- **Tipo/nome:** Medex.
- **Configurazione riportata:** `{"request":"content2media","nume":1,"content":{question}}`
- **Input:** la finestra corrente del nodo iterativo via `question`.
- **Compito:** risolvere le chiavi media in media utilizzabili dal VLM.
- **Edge:** output media verso Visiomaru e verso Naive nella configurazione corrente. Questi media non sostituiscono le chiavi originali: il Pytool le deve leggere dall'input iterativo `{question}`.
- **Da verificare:** numero di immagini materialmente presentate al VLM in ciascun giro (una o due nel caso osservato).
