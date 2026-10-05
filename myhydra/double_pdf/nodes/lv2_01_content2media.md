# Nodo LV2-01 — CONTENT2MEDIA

- **Tipo/nome:** Medex.
- **Configurazione attiva:** `{"request":"content2media","nume":1,"content":{edge}[1]}` — il `content` riceve la chiave dal Pytool `ESTRAI CHIAVE PAGINA` a monte (edge #1 nella configurazione Station corrente). Ricontrollare l'indice edge sul canvas prima di incollare: è locale alla piattaforma.
- **Configurazione storica, non usare:** `{"request":"content2media","nume":1,"content":{question}}` leggeva dalla `{question}` iterativa, cioè l'intero record pagina e non la sola chiave. Abbandonata perché il record pagina non è un contenuto risolvibile in media; la chiave va estratta prima con il Pytool.
- **Input:** chiave pagina prodotta dal Pytool `ESTRAI CHIAVE PAGINA`.
- **Compito:** risolvere la chiave media in un media utilizzabile dal VLM.
- **Nota piattaforma:** i nodi Medex non hanno variabile di output impostabile (solo i Pytool ce l'hanno, valore `result`): l'output del Medex è sempre esposto. Se a valle arriva vuoto, il problema è nel `content` in ingresso, non in un'impostazione di output.
- **Edge:** output media verso il VLM; inserire `{edge.media}[n]` da solo nel campo **Prompt** del VLM, non nel **Context** né nel **Powered identity**. L'indice è locale al canvas e va letto dal collegamento Medex→VLM. Questi media non sostituiscono le chiavi originali: i Pytool di associazione leggono il record pagina dall'input iterativo `{question}`.
- **Verifica runtime:** il test Station ha mostrato le sei immagini filtrate per il ramo. Il numero di immagini per ciascuna iterazione del LV2 va confrontato con le pagine del ramo e riconfermato sul canvas definitivo.
