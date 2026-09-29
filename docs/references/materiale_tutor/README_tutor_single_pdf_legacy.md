# Menerva — Pipeline di estrazione dati da documenti PLC/SCADA (SME/SAE)

## 1. Cos'è questo progetto

Menerva è una pipeline multi-agente per estrarre, da documenti tecnici di configurazione PLC/SCADA (mappe di registri Modbus TCP/IP, liste I/O Siemens), i dati necessari a configurare stazioni di monitoraggio emissioni ambientali (SME/SAE):

- anagrafica stazione (nome, IP/porta PLC, protocollo);
- misure analogiche e digitali (`measures`), con relativi registri Modbus;
- bit di dettaglio per i registri digitali "impacchettati" (`bitinfo`), con stati ON/OFF (`TEXTON`/`TEXTOFF`);
- campi di scala/range dei segnali (`campi_scala`), usati per la linearizzazione.

La pipeline è costruita come **workflow ad agenti** (canvas con nodi: LLM/VLM, tool Python, condizioni, iterazione) e lavora **una pagina di PDF alla volta**, per poi fondere i risultati di tutte le pagine in un unico JSON finale pronto per l'import a sistema.

Questo repository di documentazione descrive:
1. l'architettura a due livelli del workflow (§2);
2. i prompt degli agenti VLM (§3);
3. gli script Python di post-processing (§4);
4. le regole di dominio consolidate (§5);
5. i principali bug di hallucination già affrontati e le relative mitigazioni (§6).

> **Nota sulla precisione dei riferimenti ai nodi**: i nomi dei nodi citati (es. *"pytool - Merge Bitinfo"*) sono presi dai due diagrammi del canvas. Il numero di edge `{edge}[N]` presente in ogni script Python è invece un riferimento **certo**, incorporato direttamente nel codice, e viene usato qui come chiave primaria per ordinare gli script. Dove la corrispondenza esatta script↔nodo non è inequivocabile dal solo diagramma, è segnalata come "corrispondenza presunta".

---

## 2. Architettura a due livelli

### 2.1 Livello 1 — Flusso principale (Figura 1: "flusso_principale")

Il flusso principale gestisce l'intero documento PDF:

1. **Nodo `medex` (#1)** — converte il PDF in immagini, pagina per pagina.
2. **Branch `@MEDIA` / `@NOMEDIA`** — instrada la pagina a seconda che contenga o meno contenuti visivi rilevanti:
   - `@MEDIA` → nodo `medex` (#2), poi nodo `naive` (#14);
   - `@NOMEDIA` → nodo `naive` (#3) → nodo `naive` (#9).
3. **Nodo iterativo `MENERVA - 2 PDFs Modified Visio bison` (#13)** — è il cuore della pipeline: per ciascuna pagina rilevante esegue l'intero sotto-flusso descritto in §2.2 (Figura 2). L'icona "Iterative Node" evidenziata su questo nodo indica che il blocco viene ripetuto **una pagina alla volta, con offset +1** fino a esaurimento del documento.
4. **Catena di tool Python di consolidamento**, eseguita dopo (o in parallelo, per rami diversi) all'iterazione, sui risultati aggregati di tutte le pagine:
   - `pytool - Stations and Ports` (#4)
   - `pytool - Pages Merger` (#5) — corrisponde allo script `merge_pages.py` (§4.6);
   - `pytool - Json Creator` (#6) — corrisponde allo script di aggregazione per `nome_stazione` (§4.5);
   - `pytool - Remove: Quotes, Br...` (#7) — sanifica virgolette/parentesi nei JSON malformati generati dal templating;
   - `pytool - Station Informatio...` (#8);
   - `pytool - Check Empty BitInf...` (#10);
   - `pytool - Check if there are...` (#11) — filtra pagine vuote/non parsabili ("NOJSON");
   - nodi `naive` (#9, #12, #14) — punti di passaggio/risposta del workflow.

In sintesi: **Figura 1 = orchestrazione documento intero** (conversione PDF→immagini, iterazione pagina-per-pagina, merge finale multi-pagina, conversione al formato di output definitivo).

### 2.2 Livello 2 — Blocco iterativo per singola pagina (Figura 2: "loop_pagina")

Questo è il contenuto del nodo iterativo #13 di Figura 1, eseguito una volta per ciascuna pagina del PDF:

1. **`medex` (#1)** → passa l'immagine di pagina a **`visio2 - Split Files` (#6)**, un modello VLM che classifica la pagina assegnando un'etichetta (`label`) e un indice (`index`), tra:
   - `STATION_INFORMATION`
   - `MEASUREMENT_TECHNICAL_DATA`
   - `DENSITY_MAP`
   
   Se nessuna pagina rientra in queste categorie → **`naive` (#21)**, ramo di uscita "nessuna pagina utile".

2. **Filtraggio per etichetta** — due nodi Python identici a meno del `TARGET_LABEL` (§4.1):
   - **`pytool - Take the Correct K[ey]` (#15)** → filtra le pagine `STATION_INFORMATION`;
   - **`pytool - Take the Correct K[ey]` (#16)** → filtra le pagine `MEASUREMENT_TECHNICAL_DATA`.
   
   Entrambi ricevono in ingresso l'output di `Split Files` più la struttura `_medexkeys` (chiavi/percorsi immagine per pagina) e restituiscono la chiave immagine corrispondente alla pagina con l'etichetta target.

3. **Ramo `STATION_INFORMATION`** (nodi 18 → 2 → 13, sinistra del diagramma):
   - **`medex` (#18)** ricarica l'immagine tramite la chiave filtrata;
   - **`visio2 - Station Info` (#2)** — agente VLM che estrae IP/porta del PLC, protocollo e i **campi scala** (tabella "Campi scala", § 4.5.1: `segnale`/`tag`/`campo_da`/`campo_a`) — vedi prompt in §3.1;
   - **`pytool - Station Informatio...` (#13, secondo livello)** — script Python (§4.2) che, ispezionando il JSON prodotto, aggiunge un flag `CAMPI_SCALA: true` oppure `STATION_INFORMATIONS: true` a seconda che l'oggetto contenga o meno la lista `campi_scala`. Questo flag serve al merge finale per distinguere, tra le pagine classificate come "info stazione", quelle che hanno prodotto solo l'anagrafica da quelle che hanno anche prodotto i campi scala.

4. **Ramo `MEASUREMENT_TECHNICAL_DATA`** (nodi 19 → 3/4/5 → 11/7, centro-destra del diagramma):
   - **`medex` (#19)** ricarica l'immagine della pagina misure;
   - tre agenti VLM in parallelo leggono la stessa immagine con tre prompt distinti:
     - **`visio2 - Measures` (#3)** — estrae stazioni + misure (§3.2);
     - **`visio2 - Bitinfo General` (#5)** — estrae i bit "grezzi" (MEASUREID/BITNO/BITNAME) dei registri digitali impacchettati (§3.3);
     - **`visio2 - Bitinfo TextON/Tex...` (#4)** — estrae, per ciascun bit, gli stati logici `TEXTON`/`TEXTOFF` (§3.4);
   - **`pytool - Merge Bitinfo` (#7)** — fonde l'output "general" (edge #2) con l'output "TEXTON/TEXTOFF" (edge #3) per chiave `(DRIVERCONFIG, MEASUREID, BITNO)` (§4.4);
   - **`pytool - Better Measures JS...` (#11)** — ripulisce l'output misure: rimuove la sezione `bitinfo` (di competenza degli agenti dedicati), scarta misure con `NAME` puramente numerico, e deduplica per `(NAME, UNITS)` (§4.3);
   - **`pytool - Merge Multiple V...` (#8)** — combina measures ripulite (edge #7) e bitinfo fuso (edge #9, dopo "Delete NULL Names") in un unico oggetto stazione per IP (§4.4b);
   - **`pytool - Delete NULL Names` (#9)** — rimuove/ripulisce nomi non validi (spare, riserva, disponibile, ecc.) da `measures`/`bitinfo` e normalizza il testo con regex (§4.7);
   - **`pytool - BitName Number` (#12)** e **`pytool - Check Group Ingress...` (#10)** — passaggi ausiliari di normalizzazione e assegnazione del flag `GROUP: "Ingresso_digitale"` ai registri digitali condivisi all'interno della stessa stazione (§4.8).

5. **`pytool - Station Information...` (#13)**, **`pytool - Merge results Ins...` (#14)** e i nodi `naive` (#17, #20) chiudono il ramo `DENSITY_MAP`/uscita e assemblano l'oggetto finale della pagina, che viene restituito al nodo iterativo di Figura 1.

In sintesi: **Figura 2 = pipeline di estrazione per singola pagina**, con tre agenti VLM specializzati (Station Info, Measures, Bitinfo×2) più una decina di tool Python di pulizia/merge/deduplica il cui unico scopo è produrre, per ciascuna pagina, un oggetto stazione coerente con lo schema finale (`NAME`, `DRIVERNAME`, `DRIVERCONFIG`, `ID`, `measures`, `bitinfo`, `campi_scala`).

---

## 3. Prompt degli agenti VLM

### 3.1 Agente "Station Info" (IP, protocollo, campi scala)

File: prompt Station Information / Campi Scala.

- Estrae **solo** protocollo (da `SUPERVISOR`), IP/porta del PLC (da `IP ADDRESSES`, con regole esplicite per scegliere la riga ADAS vs DCS e PLC vs Gateway/HMI) e la tabella **Campi scala** (§4.5.1: `segnale`, `tag`, `campo_da`, `campo_a`, separando il range `low…high unit` e scartando l'unità di misura).
- Vincolo forte: nessuna inferenza, `nome_stazione` limitato a un set chiuso di etichette ammesse (mai nomi di azienda/impianto/città), con fallback `"SME"`.
- Output: array JSON con schema fisso, lingua italiana per i valori dei campi (non per le chiavi).

### 3.2 Agente "Measures" (stazioni e misure)

- Estrae metadati stazione (`NAME`, `DRIVERNAME`, `DRIVERCONFIG`, `ID`) e l'array `measures`, preservando l'ordine di riga del documento.
- Applica una fase di **pre-scan obbligatoria** in 4 passi (inventario IP, calcolo NAME, copia REG con carry-over, identificazione digitali impacchettati) prima di produrre qualunque JSON.
- Contiene un lungo insieme di regole anti-hallucination (v. §6), tra cui: divieto di inventare NAME/UNITS per righe con TAG e DESCRIZIONE vuoti; regole di carry-over del registro REG (mai guardare avanti, mai reset su BIT=0 o separatori grafici); classificazione digitale/analogico basata sul tag di ultima colonna (`CMD`/`SET`/`MV`/`XTM`) e non sulla sola colonna TIPO; gestione delle righe `CALCOLATA`; flag `Int`/`Range_low`/`Range_high`/`Division`/`Division_value` dalla colonna RANGE.

### 3.3 Agente "Bitinfo General"

- Estrae **solo** `MEASUREID`/`BITNO`/`BITNAME` per righe "Packed Digital" (notazione puntata `INTERO.BIT`) e "Single Digital (Standalone/CMD)" (registro non condiviso, es. `STRUCT = CMD`).
- Stessa disciplina di carry-over del REG e stessa proibizione di leggere valori dalla colonna INDIRIZZO (DBX/DBW/DBD) vista nell'agente Measures.
- Caso vuoto gestito esplicitamente (nessuna invenzione di entry se non c'è nulla da estrarre).

### 3.4 Agente "Bitinfo TEXTON/TEXTOFF"

- Stesso perimetro di righe (packed digital + standalone/CMD) dell'agente General, ma il focus è risolvere gli stati logici `TEXTON`/`TEXTOFF` a partire dalla colonna "Logic State/Range" (`STATE_VALUE`), con una cascata di regole (Case 1→4) e una **keyword table** di fallback quando la colonna è assente.
- Include numerosi self-check espliciti contro l'omissione di `TEXTON`/`TEXTOFF` su blocchi ripetitivi lunghi e sull'ultimo blocco del documento (failure mode ricorrente, v. §6).

---

## 4. Script Python di post-processing

Tutti gli script seguono le stesse convenzioni di stile (v. §7): niente funzioni/classi/lambda, cicli `while` con indice esplicito al posto di `any()`/`all()`, commenti in italiano, placeholder `{edge}[N]` sostituito a runtime con l'output del nodo collegato all'edge N.

### 4.1 Filtro pagine per etichetta (`TARGET_LABEL`)
Input: `{edge}[13]` (output di `Split Files` + `_medexkeys`). Gestisce parsing robusto (oggetti "nudi" non incapsulati, `_medexkeys` doppiamente serializzata) e restituisce solo la chiave immagine della prima pagina che combacia con `TARGET_LABEL` (`STATION_INFORMATION` o, in una seconda istanza del nodo, `MEASUREMENT_TECHNICAL_DATA`).

### 4.2 Flag Station Information vs Campi Scala
Input: `{edge}[10]`. Aggiunge `CAMPI_SCALA: true` se l'oggetto (dict o primo elemento di una lista) contiene `campi_scala` valorizzato, altrimenti `STATION_INFORMATIONS: true`.

### 4.3 Pulizia Measures ("Better Measures")
Input: `{edge}[6]`. Svuota `bitinfo` (di competenza degli agenti dedicati), rimuove misure con `NAME` puramente numerico, deduplica per `(NAME, UNITS)` mantenendo la prima occorrenza.

### 4.4 Merge Bitinfo General + TEXTON/TEXTOFF
Input: `base = {edge}[2]` (bitinfo general), `states = {edge}[3]` (bitinfo texton/off). Costruisce un indice per chiave `(DRIVERCONFIG, MEASUREID, BITNO)` e applica `TEXTON`/`TEXTOFF` all'oggetto base.

### 4.4b Merge Measures + Bitinfo per stazione
Input: `agent_a = {edge}[7]` (measures), `agent_b = {edge}[9]` (bitinfo). Indicizza il bitinfo per IP (senza porta) accumulando **tutti** i bitinfo della stessa IP tra le pagine, poi assembla un oggetto stazione unico con `measures` + `bitinfo`.

### 4.5 Aggregazione per `nome_stazione` (Json Creator)
Input: `{edge}[6]` (nome diverso in questa variante top-level). Appiattisce ricorsivamente liste annidate, ricava IP/porta per `nome_stazione` dagli oggetti `STATION_INFORMATIONS`, aggrega `measures`/`bitinfo`/`campi_scala` per nome stazione, normalizza `MODBUSREGISTRO` in notazione puntata (`"40001.3"` → `40001`), e assegna `GROUP: "Ingresso_digitale"` ai registri condivisi **all'interno della stessa stazione ma non cross-stazione** (calcolato tramite `reg_to_stations`).

### 4.6 `merge_pages.py` — Merge multi-pagina
Input: `PAGE_OUTPUTS = [{edge}[3]]`. Il più corposo dei tool: parsing tollerante di JSON eventualmente racchiusi in fence Markdown o annidati più volte; raggruppamento delle stazioni per chiave `(NAME, DRIVERCONFIG)` con **eccezione esplicita per IP placeholder** (`xxx.xxx.xxx.xxx`), mai fuse tra loro; deduplica misure per tipo (`DRIVERDATA` 0/1/2) con chiavi diverse (nome+registro per analogiche e digitali impacchettate, solo registro per digitali singole); deduplica bitinfo per `(MEASUREID, BITNO)`; **rinumerazione finale** di `ID` stazione e `ID`/`STATIONID` misura in ordine di prima apparizione. Scrive anche `localoutput28page1.json` su disco.

### 4.7 Rimozione nomi non validi + pulizia testo
Input: `{edge}[4]` (una variante) e `{edge}[5]` (un'altra variante, incentrata su parentesi/virgolette). Scarta misure/bitinfo il cui nome coincide esattamente con una lista di sezioni generiche (`"misure"`, `"comandi"`, `"impostazioni"`, ecc.) o **contiene** parole come `spare`, `riserva`, `disponibil*`, `non usato`; rimuove parole ricorrenti (`misura`, `analizzatore`, `parametro`, ecc.) dal testo restante; ripulisce parentesi tonde/quadre e virgolette da `NAME`/`BITNAME`/`TEXTON`/`TEXTOFF`, con logica diversa a seconda che il nome abbia o meno duplicati nella stessa stazione (mantiene le parentesi disambiguanti, rimuove quelle vuote).

### 4.8 Assegnazione `GROUP` cross/intra-stazione
Input: `{edge}[5]`. Ricalcola `reg_to_stations` per individuare registri condivisi **tra stazioni diverse** (da escludere) e assegna `GROUP: "Ingresso_digitale"` solo ai registri `TYPE == 6` condivisi **all'interno della stessa stazione**.

### 4.9 Merge finale Station Info + Tech Data + Density Map
Input: `{edge}[12]` (station info), `{edge}[11]` (tech data), `{edge}[23]` (density map). Gestisce input vuoti in modo sicuro (stringhe non parsate se vuote) e concatena gli oggetti disponibili in un'unica lista finale per la pagina.

### 4.10 Pulizia JSON malformati da templating
Input: `{edge}[12]` (variante top-level). Rimuove elementi vuoti generati dal sistema di templating (es. `[, {...}]`, `{...},, {...}`, `{...},]`) tramite sostituzioni regex ripetute fino a stabilizzazione, poi filtra le stazioni vuote/non valide restituendo `"NOJSON"` se non resta nulla di utile.

### 4.11 Assemblaggio Station + Measures + Campi Scala per IP
Input: `{edge}[8]`. Raccoglie IP/porta/nome/campi_scala dai gruppi con flag `STATION_INFORMATIONS`, poi fonde tutti gli altri gruppi (measures/bitinfo) in un'unica stazione base con `DRIVERCONFIG` ricostruito come `"ip:porta"`.

### 4.12 Default TEXTON/TEXTOFF
Input: `{edge}[7]`. Rete di sicurezza finale: se un bitinfo non ha sia `TEXTON` che `TEXTOFF` valorizzati, imposta `TEXTON: "ON"` / `TEXTOFF: "OFF"` come default, per evitare campi vuoti nell'output.

### 4.13 Conversione al formato finale di sistema
Input: `{edge}[4]` (documento a sé, top-level, post-merge multi-pagina). Il più complesso: costruisce `DRIVERCONFIG` in formato XML per il driver Modbus, deduplica/rinomina stazioni con lo stesso nome base aggiungendo un suffisso incrementale (`"Forno"`, `"Forno 1"`, `"Forno 2"`...), costruisce il blob binario `DRIVERPRIVATE` (registro, bit, device, formato little/big-endian) per ogni misura, applica la **linearizzazione** delle misure `Int` che hanno un `campo_scala` corrispondente (genera codice `VM_SOURCE_CODE` con dichiarazioni `ZE/SE/ZI/SI` e formula di scala), rinumera `ID` misure e `MEASUREID` bitinfo per stazione, e **scarta i bitinfo "fantasma"** che puntano a registri non risolti riutilizzando la firma `(BITNAME, TEXTON, TEXTOFF)` di un bit reale già presente nella stessa stazione (bug storico dei registri adiacenti inventati, v. §6). Scrive `testlocaljson.json` su disco.

---

## 5. Regole di dominio consolidate

- **Packed digital**: `DRIVERDATA=2, TYPE=1`.
- **Digitale singolo**: `DRIVERDATA=1, TYPE=6`.
- **Comando (CMD) sotto sezione OUTPUT**: `DRIVERDATA=5, TYPE=6`.
- **XTM / analogico**: `DRIVERDATA=0, TYPE=0`.
- Il tag dell'ultima colonna (`CMD`/`SET`/`MV`/`XTM`) è **sempre prevalente** sulla colonna TIPO e sull'assenza di unità di misura per decidere se una riga è analogica o digitale.
- `GROUP: "Ingresso_digitale"` va assegnato **solo** quando `MODBUSREGISTRO` compare più volte nella stessa stazione con `TYPE==6`, mai cross-stazione.
- Le IP placeholder (`":"`, `xxx.xxx.xxx.xxx`, `xxx,xxx,xxx,xxx`) individuano sempre una stazione separata e non vengono mai fuse con stazioni a IP reale.
- Il nome stazione non usa mai nomi di azienda/impianto/città; è limitato a un set chiuso di etichette (`Punto emissivo`, `camino`, `Emissione`, `SAE`, ecc.), con fallback `"SME"`.
- Notazione puntata dei registri (`"40001.3"`) → parte intera come `MODBUSREGISTRO`, parte decimale come `BITNO`.
- Indirizzi in coil/input space (`"00033"`) restano stringhe per preservare gli zeri iniziali; i registri holding (`40001`) sono interi.

---

## 6. Bug di hallucination noti e mitigazioni

| Bug | Sintomo | Mitigazione |
|---|---|---|
| MODBUSREGISTRO come contatore | Il modello incrementa il registro per ogni gruppo invece di leggere la cifra REG | Regola esplicita "mai contare i gruppi", esempio con REG non consecutivi (1, 3, 4 — senza 2) |
| Wrap BIT 15→0 | Il modello interpreta il ritorno a BIT 0 come nuovo registro | Regola esplicita: solo un nuovo intero esplicito in REG apre un nuovo registro, mai un pattern di BIT |
| Omissione TEXTON/TEXTOFF a fine blocco/documento | Il modello "si stanca" su blocchi ripetitivi lunghi o sull'ultimo gruppo | Self-check esplicito con scansione a ritroso dell'ultimo blocco, regola "ogni riga è un task indipendente" |
| DRIVERDATA=5 assegnato ad analogici sotto OUTPUT | Confusione tra colonna TIPO (WORD/INT) e tag di ultima colonna | Il tag di ultima colonna (CMD/SET/MV/XTM) è reso l'unica fonte valida, con esempi wrong/correct |
| Bitinfo fantasma su registri adiacenti inesistenti | Duplicazione di un bit reale su un registro vicino non presente nel documento | Script di conversione finale scarta le entry non risolte la cui firma `(BITNAME, TEXTON, TEXTOFF)` coincide con un bit reale già presente |
| MEASUREID incrementato ad ogni reset di BITNO | Confuso con un contatore di blocco | Regola esplicita + esempio "NOT 4 — nessuna nuova cifra REG è apparsa" |
| Lettura di valori dalla colonna INDIRIZZO (DBX/DBW/DBD) | Il valore numerico dell'indirizzo PLC viene scambiato per il registro Modbus | Colonna dichiarata "read-only reference", con esempi wrong espliciti (parte intera e decimale dell'indirizzo) |

---

## 7. Convenzioni di stile del codice Python

- Nessuna `def`, nessuna `class`, nessuna `lambda`, nessun `any()`/`all()`.
- Cicli `while` con variabile indice esplicita al posto di iterazioni implicite.
- Commenti inline in italiano.
- Il placeholder `{edge}[N]` nel codice non è un errore di parsing: viene sostituito dal motore del workflow con l'output del nodo collegato all'edge `N` prima dell'esecuzione.
- `null` sempre in minuscolo nei JSON di output, mai `"NULL"`/`"Null"`.
- Deduplica sempre basata su chiavi composite esplicite (es. `(MEASUREID, BITNO)`, `(NAME, UNITS)`) piuttosto che su uguaglianza dell'intero oggetto.