# Nodo LV1-03 — SINGLE PDF ENGINE

- **Tipo/nome:** motore iterativo del Single PDF.
- **Input:** gruppi prodotti dal nodo LV1-02, edge #2.
- **Modalità:** Iterative Node attivo.
- **Comportamento:** un giro per gruppo, cioè un giro per pagina del PDF. Ogni giro invoca il Livello 2 passando il gruppo corrente e ne raccoglie il risultato.
- **Output:** i risultati del Livello 2 aggregati verso l'uscita LV1.

## Il punto critico

Il modo in cui il motore aggrega i risultati dei singoli giri **non è mai stato verificato su un PDF reale**. È il rischio numero 1 dichiarato in ADR-001.

Il pytool LV1-04 è stato scritto per essere difensivo proprio per questo: accetta quattro formati di ingresso diversi, elencati nella sua scheda. Se l'aggregazione producesse un formato diverso, il parser dovrebbe comunque reggere, ma la cosa va verificata e non dedotta.

## Differenza rispetto al legacy

Nel flusso legacy questo nodo non aggregava nulla: il merge era demandato a un pytool dedicato, il "Pages Merger". Con l'Opzione B di ADR-001 il merge si è spostato dentro `json_creator.py`, che ora riceve già i JSON intermedi di tutte le pagine e li unisce prima di trasformarli. Per questo il Livello 2 non ha più bisogno di nodi di merge interni.

- **Da confermare:** forma esatta del payload aggregato dal motore.
- **Da confermare:** comportamento in caso di errore o timeout su una singola pagina. Se il motore si ferma, si salta la pagina o fallisce l'intero flusso? Il pytool non ha un `try/except` globale, quindi un payload malformato non viene trattato.
- **Da confermare:** se e come avviene il retry.
- **Riferimenti:** [`lv1_04_json_creator.md`](lv1_04_json_creator.md), [ADR-001](../../../docs/architettura/ADR-001-merge-multi-page.md).
