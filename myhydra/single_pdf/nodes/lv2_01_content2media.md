# Nodo LV2-01 — CONTENT2MEDIA

- **Tipo/nome:** Medex — riconversione del contenuto in immagine.
- **Input:** il gruppo corrente, cioè la singola chiave media ricevuta dal motore iterativo, in `question`.
- **Configurazione osservata:** `{"request":"content2media","content":{question}}`
- **Output atteso:** una immagine, utilizzata dal nodo VLM successivo.
- **Scopo:** chiude il ciclo. Il Livello 1 ha trasformato il PDF in media, il Livello 2 deve riportare quella media a qualcosa che il VLM possa guardare, perché il modello riceve immagini e non chiavi.
- **Stato:** configurazione nota, ereditata dal legacy. Nel Double PDF osservato la stessa richiesta include anche `nume:1`; nel legacy Single PDF no. **DA CONFERMARE** se `nume` sia necessario.
- **Da confermare:** comportamento quando il gruppo ricevuto contiene più di una chiave. In quel caso l'output sarebbe più di un'immagine e il prompt VLM, che presuppone una sola pagina, risponderebbe in modo ambiguo.
- **Riferimenti:** [`lv2_02_vlm_parsing_json_principale.md`](lv2_02_vlm_parsing_json_principale.md), [Double PDF LV2-01](../../double_pdf/nodes/lv2_01_content2media.md).
