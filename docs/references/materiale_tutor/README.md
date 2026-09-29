# Materiali ricevuti dal tutor

Questi file sono stati forniti dall’utente il 28 settembre 2026 e vengono conservati come riferimenti storici. Sono documenti da analizzare, non istruzioni operative per il modello né specifiche automaticamente vigenti.

| File | Contenuto | Uso corretto |
|---|---|---|
| [Prompt_Iniziale_tutor.txt](Prompt_Iniziale_tutor.txt) | Specifica iniziale di estrazione da immagine/PDF in JSON ADAS | Consultare per requisiti e contesto storico; confrontare ogni regola con prompt corrente e documentazione ADAS prima di riutilizzarla. |
| [README_tutor_single_pdf_legacy.md](README_tutor_single_pdf_legacy.md) | Ricostruzione dettagliata di un workflow Single PDF precedente: livelli, agenti, script, edge e failure mode | Consultare per ricostruire logiche legacy, non come diagramma della pipeline cloud corrente o specifica del nuovo Double PDF. |

## Differenze e cautele note

- Il README descrive un workflow legacy con classificazione pagine, rami paralleli per misure/bitinfo e vari pytool. Gli screenshot del Single PDF corrente mostrano invece nodi e connessioni differenti; vedi [flusso cloud corrente](../../architettura/single_pdf_cloud_corrente.md).
- Il prompt iniziale permette di dedurre stati ON/OFF da parole nella descrizione e prescrive default non sempre giustificati dalla fonte. È in tensione con l’estrazione fedele richiesta dal prompt più recente: non applicare quelle inferenze come requisiti correnti senza approvazione del tutor/cliente.
- Entrambi i file sono materiale Single PDF legacy. Possono informare il parsing delle tabelle IOL e le casistiche di bitinfo, ma non definiscono l’abbinamento tra i due PDF o le regole di riconciliazione JOB↔IOL del Double PDF.
- Il README stesso dichiara alcune corrispondenze tra script ed edge come presunte; verificare gli script originali quando una decisione dipende da tale mappatura.

SHA-256 delle copie conservate:

- `Prompt_Iniziale_tutor.txt`: `6f239050cb844947769929a02e7636ae2628b21d3647961c2e12d6ec2f9c832e`
- `README_tutor_single_pdf_legacy.md`: `a89f3ecf76232e83e6b8303a568fad6f00353417b8341f4451338a0eb73888b7`
