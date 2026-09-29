# Nodo backlog — MERGE PAGES

- **Stato:** `DA CONFERMARE` — non esiste come nodo separato. Il merge è incorporato nel pytool LV1-04.
- **Funzione attesa:** unire i risultati parziali delle singole pagine in un unico risultato completo.

## È già fatto, dentro il pytool

Il legacy aveva un nodo dedicato, il "Pages Merger", che si occupava solo di questo. L'Opzione B di ADR-001 lo ha assorbito in `json_creator.py`, che ora riceve tutte le pagine e le unisce prima di trasformarle: forward-fill di nome, IP, porta e slave, merge delle stazioni con stesso IP, dedup del bitinfo e unione dei digitali impacchettati che attraversano il confine fra due pagine.

Il vantaggio è che il merge avviene a livello semantico piccolo, prima della trasformazione tecnica pesante, e non dopo. Se il merge fosse rimasto un nodo separato a valle, si sarebbe dovuto rinumerare gli ID e rimappare il bitinfo su dati già trasformati.

Quindi non serve un nodo separato. Se in futuro il merge crescesse di complessità e meritasse una sua scheda, il posto naturale è dentro `json_creator.py`, non un nodo separato.

- **Riferimenti:** [legacy LV1 nodo 5, Pages Merger](../../../legacy/single_pdf/LV1/Node%205%20Pages%20Merger%20Pytool.txt), [`lv1_04_json_creator.md`](lv1_04_json_creator.md), [ADR-001](../../../docs/architettura/ADR-001-merge-multi-page.md), [`../../../TODO.md`](../../../TODO.md).
