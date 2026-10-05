# Double PDF IOL+JOB — Documento integrale per presentazione

> Fonte per generatori di presentazioni (Gamma, Tome, Beautiful.ai e simili):
> incollare tutto il testo. Stato aggiornato al 5 ottobre 2026, casi 6 e 7.

---

## 1. Titolo e messaggio centrale

**Double PDF IOL+JOB: da mappatura PLC/SCADA e specifica JOB a JSON ADAS pronto all'import.**
Un VLM legge, Python calcola e non inventa mai, ogni dubbio finisce in revisione.

---

## 2. Il problema

Un impianto di monitoraggio emissioni (SME/SAE) si configura con due documenti:
una **mappatura IOL** con tabelle di registri PLC/SCADA (indirizzi, TAG,
descrizioni, REG, BIT, TIPO) e una **descrizione JOB** con specifica
(indirizzi IP, campi scala, limiti, logiche di validazione, formule).
I due PDF vengono caricati insieme in chat, in ordine casuale e senza metadati
di origine: la piattaforma non sa quale pagina appartiene a quale documento.
Casi di riferimento: coppia 6 (`JOB.0139.23`, impianto SO2, 5+9 pagine) e
coppia 7 (`JOB.0105.22`, cogenerazione Biogen, 4+7 pagine).

## 3. L'idea in tre pilastri

1. Il VLM classifica ogni pagina (ruolo IOL/JOB + etichetta) e trascrive le
   tabelle riga per riga, senza calcolare nulla.
2. Python filtra, deduplica, unisce con join deterministici e calcola tutti i
   campi derivati (DRIVERPRIVATE hex, DRIVERCONFIG XML, ID sequenziali).
3. Placeholder, conflitti tra rami e buchi di copertura finiscono in code di
   revisione esplicite, mai nei dati in silenzio.

## 4. Architettura: un livello smista, tre rami estraggono

Livello 1 (una sola esecuzione): Medex PDF→PNG, Medex finestre di pagina,
iniezione iterativa Page Classifier (un giro per pagina), Pytool
deduplicazione, Pytool preparazione array root, tre Pytool filtro
(STATION_INFORMATION, MEASUREMENT_TECHNICAL_DATA, DENSITY_MAP).
Livello 2 (iniezioni iterative, una pagina alla volta): Station Information
(6 pagine nel caso 6: IP, porta, scale), Measurement Data (7 pagine: tre VLM
paralleli + tre tagger + assemblatore per pagina), Density in forwarding.
Finale: Pytool CONSOLIDA PRE-JSON CREATOR, oggi rinominato PREPARAZIONE X JSON
(unisce i tre rami in una stazione con 69 variabili), Pytool JSON CREATOR
(trasforma in 22 misure + 60 bitinfo ADAS), Naive OUTPUT.

## 5. Livello 1 nodo per nodo

Nodo 1 CONVERTI PDF IN PNG (Medex): i PDF diventano immagini ingrandite per
leggibilità. Nodo 2 CREA FINESTRE DI PAGINE (Medex): 14 finestre sovrapposte
nel caso 6, ogni pagina compare due volte per non perderne i bordi. Nodo 3
DOUBLE PDF PAGE CLASSIFIER (iniezione VLM): per ogni finestra assegna ruolo
(IOL, JOB o UNKNOWN da evidenze visive) ed etichetta di contenuto. Nodo 4
DEDUPLICA PAGINE SOVRAPPOSTE (Pytool): collassa la stessa chiave media in 14
pagine uniche; i disaccordi si risolvono con priorità legacy e restano negli
avvisi. Nodo 5 PREPARA PAGINE PER I FILTRI (Pytool): un array root di record
pagina con review_required e review_warnings propagati. Nodi 6, 7, 8 FILTRI
(Pytool): partizionano le 14 pagine in 6 Station, 7 Measurement, 1 Density,
conservando il record intero. Nodi 10 e 9 INIEZIONI Station e Measurement:
estrazione iterativa. Nodo 11 PREPARAZIONE X JSON (Pytool non iterativo):
legge i tre array dagli edge 10, 11 e 12 e produce stazione 10.100.50.95 porta
511 con scale SO2 collegate e review ereditate. Nodo 12 JSON CREATOR (Pytool):
chunk in ingresso dall'edge 13, ADAS in uscita verso il Naive 13 OUTPUT.

## 6. Le tre sotto-piattaforme di Livello 2

Classifier: Medex content2media più VLM con prompt dedicato. Il routing usa la
label, il document_role resta metadato; mai dedurre il PDF dal prefisso chiave
Medex, instabile tra run. Station: Pytool estrai-chiave, Medex immagine, VLM
con prompt v5 (niente default SME inventato, array vuoto se pagina vuota),
associatore pagina-estrazione. Restituisce IP, porta e scale (SO2 0–300,
Temperatura fumi 0–100, con unità e limiti dalla v5). Measurement: Medex
immagine in testa, tre VLM paralleli (misure e BISON con prompt v4 che
trascrive anche DATA_TYPE dalla colonna TIPO; bitinfo e nomi; stati
TEXTON/TEXTOFF), tre Pytool etichettatori che aggiungono ramo e pagina e
gestiscono le fence Markdown, assemblatore per pagina che unisce i tre rami
con join sul nome, BIT dal ramo misure, scarto di nomi vuoti e numerici,
merge delle stazioni con stesso DRIVERCONFIG e coda di revisione.

## 7. Le cinque regole d'oro e perché fidarsi

Primo: join sul nome, mai su MEASUREID, che ha tre semantiche diverse
(gruppi posizionali, chunk da 16, registri veri) e come chiave corrompe tutto.
Secondo: il BIT vale sempre quello del ramo misure, verificato 6 su 6 da
coordinate colonna del PDF; il BITNO del ramo bitinfo non lo sovrascrive mai e
i disaccordi vanno in review (caso PM-302A/PM-302B). Terzo: righe bianche
uguale righe saltate — riserve 420–424 e 428–430, filler numerici e TAG vuoti
non generano mai misure fantasma (il sistema legacy inventava
"Comando riservato"). Quarto: TEXTON e TEXTOFF sono derivati dal nome, non
letti — nel PDF non esiste alcuna colonna di stato; convenzione valida ma dato
sintetico. Quinto: modello leggero 3.6 solo per prove di plumbing e Qwen 3.8
per la qualità; i confronti tra run valgono solo a parità di modello e di
classificazione.

## 8. Numeri verificati del caso 6 (run Qwen 3.8, confronto riga per riga col PDF)

Classificazione: 14 pagine uniche (6 Station, 7 Measurement, 1 Density).
Estrazione: 65 misure col leggero, 69 con Qwen 3.8. Assemblatore: 7 pagine OK,
pagina 4 completamente pulita. Consolidatore: stazione Sistema Analisi SO2 su
10.100.50.95 porta 511, 69 variabili, scale SO2 0–300 collegate. ADAS finale:
22 misure (5 gruppi packed registri 1/3/4/5/6, 9 analogiche, 8 singoli CMD in
scrittura) + 60 bitinfo, validazione Pydantic superata. Dettagli dal PDF:
pagina 2 completa 30 su 30 con BIT da colonna; PM-310A a BIT 4 letto da
colonna; ventilatori a REG 6 per carry-over; SO2 Raw a REG 17 e Temperatura
fumi Raw a REG 33; QAL3 tempi a REG 9/10/11; nessun riempitivo sulle riserve.

## 9. Caso 7: generalizzazione riuscita (run Qwen 3.8)

Seconda coppia mai vista in progettazione (cogenerazione, IP 172.16.1.31 porta
511): 39 misure (4 packed + 18 analogiche INT + 9 singoli + 8 stimate) e 42
bitinfo, linkage intatto. Supera le trappole specifiche del documento: bit
wrap su REG 1 con 16 righe senza aprire registri spuri, righe bianche in mezzo
ai gruppi saltate senza rompere il carry-over, comandi e stimate completi.
Cinque variabili perse con warning esplicito (carry-over oltre il confine
pagina, non risolvibile in una LV2 per-pagina): gap noto e visibile, mai
silenzioso. Punto aperto: misure INT formattate col default in assenza di
data_type dichiarato.

## 10. Legacy contro nuovo, onestamente

Sopra al legacy con evidenza: righe fantasma mai inventate (il ground truth
legacy ha 12 bitinfo su righe bianche), BIT da colonna dove il PDF dà ragione
a noi contro il ground truth, niente default silenziosi, ADAS strutturalmente
valido con IP veri. Pari con riserve: TEXTON (nessuno li legge; il ground
truth ha tabella più ricca ma con errori propri), nomi stazione (la 3.8 li
trova, il leggero ripiega su SME). Sotto al legacy, da dichiarare al cliente:
linearizzazione BISON (il legacy la faceva, noi emettiamo il default in
attesa di specifiche), UNITS e limiti (recuperabili da Tabella JOB, lavoro
nostro), campione ancora di due coppie. Decisioni del cliente: zeri iniziali
degli indirizzi, specifiche BISON, regola sui nomi prefissati.

## 11. Glossario minimo

Edge numero N: filo tra nodi con numero locale al canvas, da ricontrollare
dopo ogni ricablaggio; può portare condizioni spurie che bloccano il filo in
silenzio. Question: record pagina dell'iterazione corrente. Edge con indice
tra parentesi: output testuale o immagine di un altro nodo. Envelope: output
dei tagger con ramo, pagina e payload, così ogni dato porta la provenienza.
Fixture observed: output runtime sanitizzato; expected: derivato. Un observed
con review_required a true non è un ground truth. Leggero 3.6: solo plumbing.
Qwen 3.8: qualità.

## 12. Punti aperti e prossimi passi

Scala TF non collegata (tag contro nome esteso), limiti JOB da collegare,
TEXTON parziali sul blocco REG 3 del caso 6, formato delle INT senza data_type,
carry-over oltre pagina, BISON e linearizzazione dal cliente. Prossimo: terza
coppia mai vista per provare la generalizzazione, poi collaudo e cliente.
