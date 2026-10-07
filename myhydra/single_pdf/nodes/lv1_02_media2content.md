# Nodo LV1-02 — MEDIA2CONTENT

- **Tipo/nome:** Medex — raggruppamento delle chiavi media in gruppi.
- **Input:** output del nodo LV1-01, edge #1.
- **Configurazione osservata:** `{"request":"media2content","nume":0, "nkeysgrp": 1}{edge.media}[1]`
- **Significato dei parametri:** `nkeysgrp: 1` è il punto architetturale dell'intero workflow. Raggruppando **una immagine per gruppo**, ogni gruppo corrisponde a **una pagina**, e quindi ogni gruppo è **una iterazione** del motore. È questo che rende il Livello 2 stateless per pagina.
- `nume: 0` non è stato interpretato; nel Double PDF il nodo equivalente produce finestre di due chiavi con overlap di una. **DA CONFERMARE** se `0` è un valore neutro o se ha un effetto.
- **Output atteso:** una sequenza di gruppi, ciascuno contenente una chiave media.
- **Stato:** configurazione nota, ereditata dal legacy. Non verificata sulla piattaforma corrente.
- **Da confermare:** numero di chiavi per gruppo e comportamento con PDF a una sola pagina.
- **Checklist edge-settings al rewiring:** `nkeysgrp: 1` (un gruppo = una pagina = un giro del motore); `{edge.media}[1]` ricontrollato; ispezionare le impostazioni di ogni edge e rimuovere match-condition spurie (checklist completa in [`../platforms/README.md`](../platforms/README.md)).
- **Riferimenti:** [`lv1_03_single_pdf_engine.md`](lv1_03_single_pdf_engine.md) per l'uso dei gruppi; [Double PDF LV1-02](../../double_pdf/nodes/lv1_02_media2content.md) per il nodo equivalente con output a finestre.
