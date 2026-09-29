# Nodo backlog — PAGE CLASSIFIER

- **Stato:** `DA CONFERMARE` — non esiste per il Single PDF. Esiste invece per il Double PDF, dove è un nodo attivo.
- **Funzione attesa:** assegnare a ogni pagina un'etichetta che ne descriva il tipo, così da instradare le pagine verso la trasformazione corretta.

## Non serve al Single PDF

Il classificatore nasce per il Double PDF, dove un documento contiene pagine di tipo diverso: informazioni di stazione, dati tecnici di misura e mappe di densità. Ogni tipo richiede un ramo di elaborazione diverso, quindi bisogna sapere di che tipo è la pagina prima di procedere.

Nel Single PDF non c'è questo problema: tutte le pagine di una mappatura sono trattate allo stesso modo e il pytool gestisce da solo le variabili mancanti. Le pagine di frontespizio, che potrebbero essere rumore, vengono gestite dal filtro sulle descrizioni vuote e dalla regola che una pagina senza variabili non crea stazione.

## Se un giorno servisse comunque

Le pagine problema sono già note. Sono le pagine di indice delle mappe registri, che contengono intestazioni come `Parametri`, `Impostazioni`, `Comandi digitali` e che non sono variabili reali. Il rischio è dichiarato in ADR-001 come numero 3, con la proposta di una regola di prompt, la V19.

La soluzione più economica resta **una regola del prompt**, non un nodo: il classificatore costerebbe un giro di VLM per pagina, mentre la regola costa un if.

- **Riferimenti:** [Double PDF LV2-02, classificatore attivo](../../double_pdf/nodes/lv2_02_page_classifier.md), [prompt del classificatore](../../double_pdf/prompts/page_classifier_v1.md), [ADR-001](../../../docs/architettura/ADR-001-merge-multi-page.md), [`../../../TODO.md`](../../../TODO.md).
