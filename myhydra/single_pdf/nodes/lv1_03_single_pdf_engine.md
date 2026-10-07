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

Nel flusso ridisegnato (v14/v15) l'uscita del motore va al nodo LV1-04 CONSOLIDATORE, che unisce i 3 rami VLM per pagina e fonde le pagine; il pytool LV1-05 JSON CREATOR trasforma poi l'unificato in ADAS. È la modifica strutturale prevista dall'Opzione B di ADR-001, con il merge spostato fuori dal creator.

- **Da confermare:** l'indice `{edge}[4]` del creator (scheda LV1-05) è fragile, perché l'inserimento del consolidatore sposta gli indici a valle. Verificare sul canvas a ogni rewiring, con la checklist in [`../platforms/README.md`](../platforms/README.md).
- **Da confermare (invariati):** forma esatta del payload aggregato; comportamento su errore/timeout di una singola pagina (il creator non ha `try/except` globale); retry.
- **Riferimenti:** [`lv1_04_consolidatore.md`](lv1_04_consolidatore.md), [`lv1_05_json_creator.md`](lv1_05_json_creator.md), [ADR-001](../../../docs/architettura/ADR-001-merge-multi-page.md).
