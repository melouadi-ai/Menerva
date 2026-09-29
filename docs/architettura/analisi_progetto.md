# Analisi del progetto Menerva MAS

## Obiettivo

Convertire documenti tecnici PLC/SCADA in dati strutturati e in una configurazione JSON ADAS, riducendo la trascrizione manuale. Le entità principali visibili nei contratti e nei modelli locali sono stazioni, misure e bitinfo; la trasformazione finale può inoltre generare configurazioni driver e codice VM.

## Stato delle evidenze

| Area | Evidenza nel repository | Stato dichiarato dall’utente |
|---|---|---|
| Single PDF | Prompt, script, modelli, output di esempio e documentazione storica | Parte 1 completata sulla piattaforma cloud; il diagramma corrente è descritto in [single_pdf_cloud_corrente.md](single_pdf_cloud_corrente.md) |
| Double PDF | Prompt e script testuali legacy nei rami `legacy/double_pdf/LV1` e `LV2`; campioni IOL/JOB | Prossima parte da progettare come flusso nuovo e migliorato |
| BISON e linearizzazione | Valore predefinito nello script locale e TODO che cita specifiche cliente mancanti | Requisiti effettivi della piattaforma corrente da verificare |

Il repository non contiene l’intera configurazione della piattaforma cloud. README e note storiche riportano versioni e stati diversi; non sono una fonte affidabile dello stato cloud odierno.

Il censimento file-per-file, i conteggi, gli hash, i duplicati e i limiti della revisione sono documentati in [inventario_repository.md](inventario_repository.md). Il censimento non equivale a una verifica umana semantica di tutti i record PDF/JSON o di ogni ramo dei grandi script legacy.

Il tutor ha fornito un prompt iniziale e una ricostruzione ampia del vecchio Single PDF. Le copie sono conservate in [`docs/references/materiale_tutor/`](../references/materiale_tutor/), con provenienza e checksum. Il README legacy è utile per esaminare script, agenti e failure mode su misure e bitinfo; il prompt iniziale include anche inferenze ON/OFF che non vanno considerate attive senza conferma. Questi materiali non definiscono l’abbinamento IOL/JOB del Double PDF.

## Ruolo del flusso Double PDF legacy

Il materiale legacy descrive classificazione delle pagine (informazioni stazione, dati tecnici di misura, density map), estrazione tramite rami distinti, merge dei risultati e conversione ADAS. È un riferimento sulle casistiche affrontate, non un contratto completo e verificato per abbinare due documenti.

Nei campioni, l’IOL contiene tipicamente indirizzi, registri, bit, tipi e segnali; il JOB può contenere metadati del sistema, comunicazione, campi scala, limiti e logiche applicative. La presenza di un campo nel JOB non prova che debba finire in ADAS: va definita la regola di collegamento alla misura IOL e la destinazione del dato.

## Coppie mostrate dal tutor

I quattro PDF caricati dall’utente costituiscono due input Double PDF distinti: ogni esecuzione prevista deve ricevere entrambi i file della relativa coppia.

| Gruppo | File IOL | File JOB (“Descrizione”) | Riferimento interno osservato | Evidenza |
|---|---|---|---|---|
| 6 | `Mappatura_6_Cliente_SMI_1.pdf` (5 pagine) | `Mappatura_6_Descrizione_Cliente_SMI_1.pdf` (9 pagine, estratto delle pagine 7–15 di JOB da 20 pagine) | Entrambi riportano `JOB.0139.23`; l’IOL riporta anche `IOL.0139.23` | Corrispondenza interna coerente. Il JOB include supervisore, campi scala, limiti e modifiche del 2026; l’IOL contiene mappe/registri e misure. |
| 7 | `Mappatura_7_Cliente_SMI_2.pdf` (4 pagine) | `Mappatura_7_Descrizione_Cliente_SMI_2.pdf` (7 pagine, estratto delle pagine 9–15 di JOB da 21 pagine) | Entrambi riportano `JOB.0105.22`; l’IOL riporta anche `IOL.0105.22` | Corrispondenza interna coerente. Il JOB include IP/porta PLC e campi scala/limiti; l’IOL contiene mappa, registri, bit e segnali. |

Questi sono i casi iniziali da usare per definire il Double PDF. I file caricati non sono tutti presenti come copie identiche nel repository: in particolare, l’IOL del gruppo 6 caricato non ha corrispondenza SHA-256 nel repository; il file omonimo sotto `data/test_inputs/` è vuoto e non è quel documento. Non sostituire o confondere le due copie.

I JOB caricati contengono anche credenziali operative. Non includerle in prompt, log, fixture o output dimostrativi; per condividere o versionare questi PDF serve una copia redatta e autorizzata.

Conferma dell’utente sul flusso d’ingresso: IOL e JOB vengono allegati insieme in un’unica chat AI; non ci sono slot separati per ruolo. Il VLM deve classificare il ruolo del documento e il tipo di pagina. Resta da verificare se il runtime passa al workflow il nome/ID del file e il numero di pagina per ogni immagine.

Una precedente anomalia osservata nel campione Ospedale San Marco (riferimento JOB interno discordante rispetto al nome del file) resta un utile caso negativo separato; non è uno dei due esempi mostrati dal tutor.

## Rischi documentali da conservare nel progetto

- I nomi dei PDF e delle cartelle non sono sufficienti a provare una coppia. Nei due esempi del tutor, i riferimenti interni IOL/JOB concordano (`0139.23` e `0105.22`); nel distinto campione Ospedale San Marco l’IOL riporta invece un riferimento JOB discordante rispetto al file fornito. L’associazione richiede quindi verifica, non correzione automatica.
- Alcuni PDF sono duplicati byte per byte con nomi o collocazioni differenti; è necessario registrare provenienza e hash prima di definirli benchmark.
- È presente un PDF vuoto: `data/test_inputs/Mappatura_6_Cliente_SMI_1.pdf`.
- I JSON sotto `data/test_inputs/` e `data/test_outputs/` hanno ruoli misti: alcuni sono output ADAS, intermedi, frammenti o dati storici. Non considerarli tutti ground truth senza provenienza e revisione confermate.
- I confronti automatici esistenti individuano discrepanze ma non stabiliscono quale file sia corretto quando il riferimento non è qualificato.
- Le note legacy descrivono merge e deduplicazioni basati su nomi, IP, registri o ID intermedi. La nuova soluzione deve preservare riferimenti stabili tra misure e bitinfo dopo ogni merge e rinumerazione.

## Impostazione consigliata per il nuovo Double PDF

1. Acquisire i documenti come entità separate e conservare hash, nome, tipo, revisione e pagine.
2. Proporre l’abbinamento IOL/JOB usando identificativi esterni e riferimenti interni; rendere espliciti conflitti e associazioni incerte.
3. Estrarre ciascun documento separatamente e registrare per ogni campo documento, pagina e posizione d’origine.
4. Normalizzare gli oggetti in uno schema intermedio comune senza confondere indirizzo PLC, registro Modbus, bit e identificativo di misura.
5. Collegare campi JOB e segnali IOL con chiavi esplicite e regole verificabili; mantenere i conflitti non risolti nel risultato di revisione.
6. Validare riferimenti e vincoli, quindi generare deterministicamente il JSON ADAS.
7. Produrre un riepilogo di riconciliazione con elementi associati, non trovati, duplicati o ambigui e relative fonti.

## Decisioni ancora da fissare

- Identificativo canonico e regola di associazione tra IOL e JOB, incluse revisioni discordanti.
- Quali campi JOB alimentano quali campi ADAS e con quale criterio di corrispondenza.
- Comportamento richiesto quando un documento manca, una tabella è illeggibile o i riferimenti non concordano.
- Dataset di riferimento approvati, con provenienza, revisione e verifica umana.
- Specifiche necessarie per BISON e per l’uso delle scale e dei limiti.
- Regole per distinguere le revisioni: il JOB del gruppo 6 include una sezione “Adeguamento marzo 2026” e l’IOL presenta date/versioni in copertina. Va deciso quale fonte o revisione prevale quando le informazioni cambiano.
- Come il runtime rappresenta più allegati della stessa chat dopo Medex e se preserva nome/ID del PDF e numero di pagina; il riconoscimento semantico IOL/JOB e del tipo pagina spetta al VLM.

Prima di automatizzare le decisioni ambigue, fissare queste regole su coppie campione e conservare le evidenze per pagina. Gli screenshot del Single PDF non forniscono informazioni su tali scelte del Double PDF.
