# Nodo LV1-02 — MEDIA2CONTENT e divisione in gruppi

- **Tipo/nome:** Medex — `MEDIA2CONTENT E DIVISIONE IN GRUPPI`
- **Input:** output del nodo LV1-01, edge #1.
- **Output osservato:** 14 oggetti `_medexkeys`; primi 13 con due chiavi consecutive sovrapposte alla finestra seguente, ultimo con una chiave.
- **Configurazione LV1 fornita dall’utente:** `{"request":"media2content","nume":1, "nkeysgrp": 1 }{edge.media}[1]`
- **Chiavi uniche nel caso 6:** 14.
- **Output runtime inoltrato:** `_medexkeys` può essere serializzato come stringa JSON annidata.
- **Configurazione esatta:** `DA ACQUISIRE DAL CANVAS`; non copiare automaticamente la configurazione legacy.
- **Da confermare:** parametri di raggruppamento e comportamento generale oltre il caso 6.
