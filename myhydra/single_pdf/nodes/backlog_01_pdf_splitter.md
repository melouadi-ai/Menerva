# Nodo backlog — PDF SPLITTER

- **Stato:** `DA CONFERMARE` — non esiste, non è stato progettato. Elencato in `TODO.md` fra i nodi mancanti.
- **Funzione attesa:** separare le pagine di un PDF in modo esplicito, producendo unità che verranno poi elaborate singolarmente.

## Perché è in backlog e non in catena

Sotto l'Opzione B di ADR-001 questo compito **è già svolto**,implicitamente, da due nodi: il Medex `pdf2png` produce una immagine per pagina, e il Medex `media2content` con `nkeysgrp: 1` le raggruppa una per gruppo. Il motore iterato poi tratta ogni gruppo come una pagina.

Un nodo splitter esplicito servirebbe se si volesse un controllo diretto sulla segmentazione, per esempio per classificare le pagine prima di elaborarle. Questo non è previsto dal flusso attuale.

- **Da confermare:** se il nodo serva al Double PDF, dove le pagine di due documenti diversi convivono e la segmentazione è più delicata.
- **Riferimenti:** [`../../../TODO.md`](../../../TODO.md), [legacy](../flusso_cloud_osservato.md).
