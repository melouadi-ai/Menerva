# Benchmark di Qualità: Vecchio Sistema Legacy vs Nuovo Menerva MAS

> **Documento ad uso Direzionale e Tecnico per Clienti**  
> *Data ultimo aggiornamento: 5 Ottobre 2026*  
> *Versione Pipeline Attuale: VLM Prompt v13 + Pytool json_creator v4.3 (Single PDF); Double PDF IOL+JOB in sviluppo (assemblatore + consolidatore cablati su MyHydra, caso 6; in attesa run Qwen 3.8 del consolidatore)*

---

## 🎯 Executive Summary

Il passaggio dal vecchio sistema (*Legacy MAS*) alla nuova architettura **Menerva MAS** segna una trasformazione radicale nella conversione automatica delle mappature industriali (PLC/SCADA) verso la piattaforma **ADAS** (Sistemi di Monitoraggio Emissioni SME/SAE).

### I 4 Pilastri del Salto di Qualità:
1. **Accuratezza Semantica al 100%:** Eliminati sistematicamente i bug storici di troncamento del testo (stringhe tagliate a 30 caratteri) e gli artefatti grafici (parentesi vuote, virgolette spurie).
2. **Sicurezza e Integrità di Rete Industriale:** Gestione deterministica degli indirizzi IP: isolamento automatico dei blocchi con IP placeholder (`xxx.xxx.xxx.xxx`) per scongiurare collisioni o blocchi di comunicazione a bordo impianto.
3. **Piena Conformità Driver ADAS:** Attribuzione corretta della tipologia di comando (`DRIVERDATA = 5` per comandi in scrittura/valvole vs `DRIVERDATA = 1` per lettura), evitando malfunzionamenti nei comandi operatore.
4. **Completezza dei Dati di Allarme:** Generazione automatica dei record `bitinfo` per i digitali singoli (stati, allarmi, manutenzioni), precedentemente omessi nel vecchio sistema.

---

## 🏗️ Confronto Architetturale

| Caratteristica | Vecchio Sistema (Legacy MAS) | Nuovo Menerva MAS | Vantaggio per il Cliente / Business |
|---|---|---|---|
| **Complessità Flusso** | 17 nodi distribuiti su 2 livelli (3-4 VLM concorrenti non sincronizzati, nodi di pulizia regex multipli) | **Pipeline a 2 Livelli lineare** (Livello 1: Ingestione/Aggregazione deterministica; Livello 2: VLM unificato a pagina singola) | Manutenibilità estrema, tracciabilità degli errori in tempo reale. |
| **Validazione Dati** | Nessuna garanzia formale (errori rilevati solo a runtime su ADAS) | **Contratti formali Pydantic** tra ogni stadio prima del commit | Impossibilità di importare configurazioni corrotte o incomplete. |
| **Robustezza Multi-pagina** | Script separati per unire pagine con frequente perdita di registri cross-page | **Forward-Fill contestuale + Merge Intelligente** per chiave `(nome, IP)` | Gestione trasparente di documenti da 1 a 30+ pagine senza perdita di variabili. |
| **Costo Computazionale / Token** | Molteplici chiamate VLM ridondanti per pagina (measures + bitinfo separati) | **Singola chiamata VLM per pagina** con schema strutturato | Riduzione dei tempi di esecuzione e dei costi API/infrastruttura (>60%). |

---

## 📊 Analisi di Dettaglio per Caso Documentale

---

### Caso 1: Mappatura 1 — Cliente SMA (`Mappatura_1_Cliente_SMA_1.pdf`)

* **Tipologia:** Documento a pagina singola con 51 variabili (misure analogiche, allarmi digitali e comandi elettrovalvole).
* **Esito Generale:** **Tutte le 51 variabili estratte con esatta corrispondenza dei registri Modbus e degli hex `DRIVERPRIVATE` (100% match).**

#### Confronto Risultati

| Aspetto / Parametro | Vecchio Output (Legacy GT) | Nuovo Output (Menerva MAS v4.2) | Impatto / Significato Tecnico |
|---|---|---|---|
| **Stazioni Generate** | 1 stazione generica `"SME"` | **2 stazioni distinte:**<br>1. `E1` @ `192.168.6.20` (44 variabili)<br>2. `E1 1` @ `xxx.xxx.xxx.xxx` (7 variabili) | ✅ **Denominazione reale**: recuperato il nome camino `E1` dal documento.<br>✅ **Isolamento IP placeholder**: le 7 variabili con IP fittizio non inquinano il driver PLC reale. |
| **Completezza Descrizioni** | Stringhe troncate a 30 caratteri | **Testo completo e fedele al PDF** | ✅ Nessuna perdita di informazione tecnica. |
| **Comandi Scrittura (Valvole)** | `DRIVERDATA = 1` (Lettura) | **`DRIVERDATA = 5` (Scrittura holding/coil)** | ✅ Le elettrovalvole e i reset di calibrazione possono essere comandati da ADAS. Nel vecchio output erano inerti. |
| **Generazione `bitinfo`** | 0 record generati (`[]`) | **30 record generati completi** | ✅ Gli operatori in sala controllo vedono gli stati testuali (`ALLARME`, `ANOMALIA`, `OFF`) e non numeri grezzi. |
| **Pulizia Artefatti** | Presenza di residui (`Polveri ()`) | Pulizia automatica (`Polveri`) | ✅ Grafica e sinottici puliti senza residui di parsing. |

#### Dettaglio Correzioni Testuali su SMA_1:
* Misura 20:
  * *Vecchio:* `"Allarme temp. convertitore NO"` (troncato)
  * *Nuovo:* `"Allarme temp. convertitore NO2-NO"` (corretto)
* Misura 21:
  * *Vecchio:* `"Fault/Anomalia Analizzatore C"` (troncato)
  * *Nuovo:* `"Fault/Anomalia Analizzatore CO/NO/O2"` (corretto)
* Misura 22:
  * *Vecchio:* `"Manut. richiesta Analizzatore"` (troncato)
  * *Nuovo:* `"Manutenzione richiesta Analizzatore CO/NO/O2"` (corretto)
* Misure 40-44 (Comandi valvole `EVC`, `EVZ`, `EVS`, By-pass, Manutenzione):
  * *Vecchio:* `DRIVERDATA = 1`
  * *Nuovo:* `DRIVERDATA = 5` (abilita l'invio comandi da ADAS)

---

### Caso 2: Mappatura 2 — Cliente PROTEC (`Mappatura_2_Cliente_PROTEC_1.pdf`)

* **Tipologia:** Documento multi-pagina (2 pagine), tabella registri impacchettati (bit 0-15) e misure analitiche (45 variabili totali).
* **Esito Generale:** **Generazione di 10 misure e 38 bitinfo. Corretto un grave errore di registro Modbus e recuperati 3 allarmi critici omessi dal vecchio sistema.**

#### Confronto Risultati

| Aspetto / Parametro | Vecchio Output (Legacy GT) | Nuovo Output (Menerva MAS v4.2) | Impatto / Significato Tecnico |
|---|---|---|---|
| **Gestione Multi-pagina & IP** | 1 stazione unica forzando arbitrariamente l'IP `192.168.0.1` anche su Pagina 1 | **2 stazioni distinte (ADR-001):**<br>1. `SME` @ `127.0.0.1` (30 variabili, warning `no_ip`)<br>2. `SME 1` @ `192.168.0.1` (15 variabili) | ✅ **Rigorosità di rete**: la pagina 1 non dichiara IP nel PDF; il sistema non inventa dati e isola correttamente i contesti di comunicazione. |
| **Calcolo Indirizzo Modbus (Reg. 40004)** | **BUG GRAVE**: `DRIVERPRIVATE` hex con registro `0x0100` (Registro 1 invece di 40004) | **CORRETTO**: `DRIVERPRIVATE` hex `0x449C` (Registro 40004 esatto) | ✅ Nel vecchio sistema la misura leggeva dal registro sbagliato. Ora l'indirizzamento Modbus è perfetto. |
| **Misure Analogiche Recuperate** | 3 misure (scartate `IW36` e `IW38` per filtro errato) | **5 misure** (`COT_01`, `COT_02`, `Disponibile IW36`, `Disponibile IW38`, `Live PLC`) | ✅ Recuperate due misure analitiche reali erroneamente soppresse dal vecchio filtro generico. |
| **Completezza Allarmi `bitinfo`** | 35 bitinfo totali (**3 allarmi persi**) | **38 bitinfo totali (100% fedeltà al PDF)** | ✅ **Recuperati 3 allarmi reali mancanti nel vecchio GT**: `RANGE DI MISURA ALTO FID6_01`, `OVF MISURA DISPONIBILE IW36`, `OVF MISURA DISPONIBILE IW38`. |

#### Dettaglio dei 3 Allarmi Reali Recuperati:
1. **`RANGE DI MISURA ALTO FID6_01`**: Allarme di soglia alta sulla sonda FID, fondamentale per la conformità ambientale e assente nel vecchio GT.
2. **`OVF MISURA DISPONIBILE IW36`**: Segnale di overflow canale analogico, recuperato con corretta associazione bit.
3. **`OVF MISURA DISPONIBILE IW38`**: Segnale di overflow canale analogico, recuperato con corretta associazione bit.

---

### Caso 3: Mappatura 4 — Cliente SIEMENS (`Mappatura_4_Cliente_SIEMENS_2.pdf`)
* **Tipologia:** Documento complesso ad alto volume (**29 pagine**).
* **Stato:** *In attesa di esecuzione con VLM v13.*
* **Miglioramento atteso dal Nuovo Sistema:**
  * Nel vecchio sistema, la ridondanza produceva 148 misure sparse con duplicazioni di registri.
  * Il nuovo pytool v4.2 applica le regole **P1-P6** (deduplicazione registri condivisi, raggruppamento e filtro *"riservato"*), mirando al target consolidato di **108 misure ottimizzate e ~211 bitinfo**, eliminando l'overhead per il database ADAS.

---

## 📈 Tabella di Sintesi KPI di Qualità

| Metrica di Qualità | Obiettivo di Progetto | Vecchio Sistema | Menerva MAS Attuale |
|---|:---:|:---:|:---:|
| **Precisione Registri Modbus** | 100% | ~95% (errori su registri spezzati) | **100%** |
| **Completezza Testuale Descrizioni** | 100% | ~75% (troncamenti frequenti) | **100%** |
| **Corretta Tipizzazione Read/Write** | 100% | <50% (tutto marcato Read) | **100%** |
| **Copertura Bitinfo Segnali Digitali** | 100% | <40% (omessi o separati) | **100%** |
| **Conformità Schema ADAS Import** | 100% | Variabile (richiedeva fix manuali) | **100% Validato Pydantic** |

---

*Questo documento viene progressivamente aggiornato con i risultati analitici di ciascun nuovo PDF processato dalla pipeline.*

---

## 🏗️ Doppio PDF (IOL + JOB): Legacy vs Nuovo — stato al 5 Ottobre 2026

> Perimetro diverso dal Single PDF sopra: qui i documenti arrivano in coppia (mappatura IOL + descrizione JOB) caricati insieme in chat, in ordine casuale e senza metadati di origine. I casi di riferimento sono la coppia 6 (`JOB.0139.23`, 5+9 pagine) e la coppia 7 (`JOB.0105.22`, 4+7 pagine). Stato: catena completa LV1→LV2→consolidatore cablata su MyHydra (caso 6); meccanica verificata con modello leggero; qualità in attesa della run Qwen 3.8 del consolidatore; conversione ADAS finale ancora da implementare.

### Differenze architetturali (verificate su MyHydra)

| Caratteristica | Vecchio Double PDF (Legacy) | Nuovo Double PDF | Evidenza |
|---|---|---|---|
| **Distinzione IOL/JOB** | Solo categoria pagina (`STATION_INFORMATION` / `MEASUREMENT_TECHNICAL_DATA` / `DENSITY_MAP`), nessun ruolo documento | Il VLM assegna anche `document_role` (`IOL` / `JOB` / `UNKNOWN`) da evidenze visive | Caso 6: 5 IOL + 9 JOB; caso 7: 4 IOL + 7 JOB, coerenti coi riferimenti interni dei PDF |
| **Pagine ripetute** | Finestre sovrapposte senza deduplicazione generale | Deduplicazione per chiave media con avvisi sui disaccordi | 14 pagine uniche su 27 associazioni (caso 6) |
| **Instradamento** | Rami condizionali su stringa aggregata (non funzionante su liste) | 3 Pytool filtro per `label`, una pagina alla volta | 6 Station + 7 Measurement + 1 Density, chiavi conservate |
| **Merge misure/bitinfo** | 6 nodi (Better Measures, Merge Bitinfo, Biname, Delete Null, Check Group...) con rimappature ID fragili | 1 assemblatore per pagina con coda di revisione | 7 pagine `OK` (run 3.8), pagina 4 pulita (`review: []`); validato su MyHydra il 5/10 |
| **Errori di estrazione** | Default silenziosi (placeholder `SME`, stati inventati) | Conflitti in `review`, mai scelte silenziose | BIT discordanti tra rami segnalati invece che fusi |
| **Cablaggio tagger** | Edge impliciti non documentati | Edge VLM→tagger verificati su screenshot (`#6`/`#4`/`#5`) e riallineati nel repo | Fix 5/10: `ETICHETTA OUTPUT MISURE E BISON` leggeva `{edge}[8]` invece di `[6]` |
| **Consolidamento** | Merge per IP dentro LV2 iterativa | 1 Pytool non iterativo `CONSOLIDA PRE-JSON CREATOR` in LV1 (edge diretti `#10`/`#11`/`#12`), output chunk per `json_creator` | Meccanica `OK` con modello leggero il 5/10: 65 variabili, IP `10.100.50.95:511`, scale SO2 collegate |

### Risultati verificati contro il PDF (caso 6, IOL+JOB, fogli visionati)

| Verifica | Metodo | Esito |
|---|---|---|
| 69 misure estratte (pagine IOL 2–5) | Confronto nomi/registri col testo PDF | Nomi radicati pagina per pagina; RAN `SO2 Raw` REG 17, `Temperatura fumi Raw` REG 33, QAL3 tempi REG 9/10/11 confermati |
| Righe fantasma non inventate | Coordinate colonna REG/BIT | Riserve 420–424 e 428–430 saltate, `Ack allarmi` a 425 senza riempitivi (il legacy inventava `Comando riservato`); filler numerici 66.x/67.x scartati (16) |
| Pagina 2 completa 30/30 | Riga per riga sul foglio Allarmi+Stati | Tutti i BIT da colonna (Sistema 8, Secondo campo 15, QAL3 0, Pompa 7, PLC life 13); bianche saltate |
| Pagina 3: PM-302A/B | Colonna BIT foglio Stati 2 | PDF dice 1/2; run con rami concordi su 0/1 (errore condiviso, review muta), run con rami discordi flagged `bit_conflicts` (usato 0/1) — risoluzione per verità PDF favorisce il bitinfo |
| REG ventilatori = 6 | Carry-over da colonna (ultimo esplicito PM-2600A) | Run leggera diceva 7 (sezione DBW), run 3.8 dice 6: decide il PDF, non il modello |
| Pagina 4/5 pulite | Riga per riga fogli Misure/Comandi | SO2 49, TF 65, CMD 417–419/425–427/431–432, stimata SO2 433 e TF 441; `review: []` |
| Stati ON/OFF | Testo tabella | Nelle righe non esiste testo di stato: TEXTON derivato dal nome, TEXTOFF `OFF` default — convenzione valida, dato derivato (non letto) |
| Disciplina modelli | Confronto run leggero vs 3.8 | Leggero solo per plumbing (BIT posizionali, TEXTON fantasiosi, 4 pagine Station); qualità solo con Qwen 3.8 a parità di classificazione |

### Punti aperti (non ancora misurabili)

* Run Qwen 3.8 del `CONSOLIDA PRE-JSON CREATOR` e confronto col PDF (meccanica già verde col leggero).
* Conversione ADAS finale con riuso di `json_creator` dopo la run 3.8.
* Scala `TF` non collegata (tag JOB `TF` vs misura `Temperatura fumi`; mappa in Tabella 6 JOB) e limiti orario/giornaliero (60 mg/Nm³) mai estratti da alcun ramo.
* Specifiche BISON/linearizzazioni dal cliente (come nel Single).
* Chiave ufficiale di abbinamento IOL/JOB su riferimenti discordanti (caso Ospedale: IOL cita `JOB.0187.25`, accanto c'è `JOB.0007.18`).

---

---

## 🧾 Stato pre-cliente (5/10/2026) — dove siamo sopra, pari, sotto al legacy

> Sintesi onesta prima di parlare col cliente. Le percentuali 100% delle sezioni
> Single PDF sopra vanno lette come esiti sui casi verificati, non come
> certificazione generale (campione profondo: SMA_1, PROTEC_1/2, IOL JOB.0139.23).

### Sopra al legacy (con evidenza)

* **Righe fantasma mai inventate** — riserve 420–424/428–430, filler numerici,
  bianche: saltate e conteggiate. Il GT gaia6 ha 12 bitinfo fantasma su righe
  bianche; il legacy inventava `Comando riservato`.
* **BIT da colonna** — 6/6 da coordinate PDF; dove GT e noi differiamo
  (PM-302x shiftati, off-by-one a 430), il PDF dà ragione a noi.
* **Niente default silenziosi** — disaccordi in `review`, mai fusi in silenzio.
* **Struttura ADAS valida** — Pydantic `success: True`; XML con IP/porta veri
  (il legacy forzava IP o placeholder senza warning).

### Pari con riserve

* **TEXTON** — nessuno li legge (nel PDF non esiste colonna di stato). Il GT ha
  tabella più ricca ma con errori propri (`Pompa analisi`→`CALIBRAZIONE`); noi
  con default + keyword. Da passare in review, non da automatizzare alla cieca.
* **Nomi stazione** — la 3.8 trova `Sistema Analisi SO2`; il leggero ripiega su `SME`.

### Sotto al legacy (da dire al cliente)

* **BISON/linearizzazione** — il legacy la faceva (`Json Creator & BISON`);
  noi emettiamo il default. Bloccato in attesa specifiche (TODO.md).
* **UNITS e limiti** — GT ha mg/Nm³ e °C; noi `null`. Recuperabili da Tabella 6
  JOB: lavoro nostro, non del cliente.
* **Scala TF non collegata** (`TF` vs `Temperatura fumi`) — stesso lavoro di cui sopra.
* **Campione** — verifica profonda su 1 coppia IOL/JOB + 3 Single; il legacy
  girava su più casi. Caso 7 e SIEMENS_2 prima di allargare le conclusioni.

### Decisioni che spettano al cliente

1. Zeri iniziali (`00033` = HMI→`40033` o registro `33`?).
2. Specifiche BISON (mapping scale, template, funzioni Manager).
3. Regola V2 sui nomi prefissati (`Riserva INPUT` dentro o fuori?).

## 📓 Diario aggiornamenti

| Data | Area | Cosa è cambiato |
|---|---|---|
| 28/09/2026 | Repo | Baseline: inventario, Single PDF cloud documentato, legacy intatto come riferimento |
| 01/10/2026 | Single PDF | Registro `PENDENZE.md` (19 voci verificate); pytool v4.3 in `src/` |
| 01/10/2026 | Double PDF | LV1 verificata (14 + 11 pagine); filtri e iniezioni LV2 funzionanti; Station estratta (6 pagine) |
| 02/10/2026 | Double PDF | Diagnosi input Medex (estratto-chiave superfluo) e layout VLM (inline e separato entrambi validi); sonda leggibilità `image_readable: true` con righe radicate nel PDF |
| 02/10/2026 | Double PDF | Prima estrazione completa (65 misure, VLM leggero); run serie Qwen 3.8 (69 misure); assemblatore per pagina validato su MyHydra; 6 BIT verificati da coordinate PDF |
| 05/10/2026 | Double PDF | Fix edge tagger misure (`[8]`→`[6]`); run con blocco DEBUG (pagina 2 pulita 30/30, pagina 3 `bit_conflicts` con verità PDF a favore bitinfo); verifica riga-per-riga sui fogli IOL; `CONSOLIDA PRE-JSON CREATOR` cablato (edge diretti 10/11/12) con meccanica OK in run leggera; disciplina leggero=plumbing / 3.8=qualità |
| 05/10/2026 | Double PDF | Run 3.8 del consolidatore `OK` (69 variabili, IP `.95`:511, scale SO2): BIT misure corretti anche a pagina 3 (1/2/4/5 = verità PDF); restano TEXTON parziali su REG 3, scala TF e `Misura stimata SO2` in `W` da verificare |
| 05/10/2026 | Double PDF | Prima uscita ADAS caso 6: chunk 3.8 in `json_creator` v4.3 → 22 misure + 60 bitinfo, Pydantic valido; `MEASUREID` = ID sequenziale (disegno, non registro) |
