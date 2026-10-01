# Nodo LV2-01 — CONTENT2MEDIA

- **Tipo/nome:** Medex.
- **Configurazione riportata:** `{"request":"content2media","nume":1,"content":{question}}`
- **Input:** chiave pagina prodotta dal Pytool `ESTRAI CHIAVE PAGINA` (edge #1 nella configurazione Station corrente).
- **Compito:** risolvere le chiavi media in media utilizzabili dal VLM.
- **Configurazione riportata:** `{"request":"content2media","nume":1,"content":{edge}[1]}`; usare l'indice edge esatto del canvas.
- **Edge:** output media verso il VLM. Questi media non sostituiscono le chiavi originali: il Pytool di associazione deve leggere il record pagina dall'input iterativo `{question}`.
- **Verifica runtime:** il test Station ha mostrato le sei immagini filtrate per il ramo. Il numero di immagini per ciascuna iterazione del LV2 va confrontato con le pagine del ramo e riconfermato sul canvas definitivo.
