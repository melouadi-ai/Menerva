# Double PDF IOL+JOB — resoconto per il tutor (6 ottobre 2026)

Conversione automatica delle coppie di documenti (mappatura IOL + descrizione JOB) in configurazioni ADAS per sistemi di monitoraggio emissioni. Piattaforma: MyHydra (canvas cloud). Metodo di verifica: ogni output è confrontato **riga per riga con i PDF**, mai con i ground truth storici (che risultano peggiori: vedi sezione 3).

I PDF di riferimento stanno nelle cartelle dei casi (`myhydra/double_pdf/tests/case_6/` e `case_7/`, sottocartella `PDF di riferimento/`), byte-identici ai sorgenti. Il confronto va fatto su **coppia IOL+JOB**, perché metà della verità (unità, limiti, validazioni, IP) sta nel JOB.

## 1. Fatto finora

- **Catena LV1→LV2→ADAS cablata e funzionante su MyHydra**, verificata end-to-end con Qwen 3.8 sui casi 6 (`JOB.0139.23`, 5+9 pagine) e 7 (`JOB.0105.22`, 4+7 pagine).
- **LV1**: classificazione pagine, deduplicazione finestre sovrapposte (14 pagine caso 6, 11 caso 7), filtri per ramo (6 Station / 7 Measurement / 1 Density nel caso 6), iniezioni LV2.
- **LV2 Measurement a 3 rami** (misure, nomi bitinfo, stati) + assemblatore per pagina con coda di revisione (i disaccordi tra rami finiscono in `review`, mai fusi in silenzio).
- **Consolidatore LV1** (`PREPARAZIONE X JSON`, nodo 11): unisce LV2 Station + Measurement + Density in un chunk con `registro_suggerito` (suggerisce, non applica mai) e collegamento scale.
- **JSON CREATOR finale** (nodo 12): produce misure + bitinfo ADAS. Dopo aver scoperto che la copia sul canvas era divergente dal repo (campi limite a `null` invece del sentinel), il nodo è riallineato. I due flussi hanno **copie separate** dello stesso trasformatore (Single `{edge}[4]`, Double `{edge}[13]`), perché l'indice edge è diverso.
- **Limite dimensionale del canvas scoperto e gestito**: un paste da 34.365 byte manda il nodo in rosso, uno da 32.766 passa. La copia da incollare è senza commenti (26.731 byte, AST identico al file documentato), con test di parità che la bloccano.
- **Prompt misure v5**: `DATA_TYPE` trascritto da TIPO + self-check di copia letterale del BIT (dopo una regressione PM-302A/B shiftati di uno).
- **TEXTON da keyword** (decisione 6/10): l'IOL non ha colonna di stato, quindi ogni `state_on` è inferenza del VLM; in una run aveva scritto ALLARME su heartbeat ed elettrovalvole.
- **Fixture e test di verità**: ogni run è salvata e confrontata col PDF in test automatici (27 root + 50 double verdi).

## 2. Funzionante e verificato

### Caso 6 — 100% del PDF

Run4 (riferimento): **22 misure e 60 bitinfo, tutti conformi** al foglio IOL (registri 1,3,4,5,6,9,10,11,17,33,49,65,417–419,425–427,431,432,433,441; `INT`→formato 150, `REAL`→250; `mg/Nm3` su SO2/SO2 Raw; PM-302A/B ai bit 1/2; stazione `Sistema Analisi SO2`, `10.100.50.95:511`; nessun warning).

### Caso 7 — quasi tutto

Run3: **39 registri su 39 conformi** (`INT`→150 sulle 18 analogiche, `WORD`→250 sulle stimate; stazione `Sistema Analisi Emissioni`, `172.16.1.31:511` da Tabella 8 JOB; sentinel e `UNITS2` corretti), ma **42 bitinfo contro 47** e una misura col nome sbagliato (vedi sotto). Run4 chiude entrambi i punti.

### Caso 7 — quasi tutto (run5: 47/47 bit, 17/18 unità, range reali)

Run5 (riferimento): **40 misure e 47 bitinfo**. I 5 stati recuperati, 17 unità collegate per TAG (resta fuori solo `Consumo combustibile orario`, la cui riga scala non porta l'unità), fondi scala in `LOWRANGE`/`HIGHRANGE`, warning con nomi per i 5 limiti e le 9 divisioni (mapping in fase BISON). REG 166 col nome che oscilla per run (CO/COT), stazione `SME` (ramo Station null).

### Il ground truth storico non è un riferimento

`gaia_doublefile_result_6.json` sbaglia: 2 registri (430/431 invece di 431/432), 18 bitinfo inventate (78 contro 60, di cui 12 su righe bianche), TEXTON spostati di una riga, QAL3 `INT` scritti come REAL, un bitinfo orfano. Le differenze output-vs-legacy non vanno colmate senza verifica sul PDF. Fissato in `test_legacy_ha_errori_noti_il_nostro_no`.

## Aggiornamento 12/10 — terzo caso: Rivoli (verificato)

Coppia `IOL/JOB.0177.25` (Rivoli, mai vista prima): run archiviata come
`myhydra/double_pdf/tests/case_8/`, verità in `test_adas_caso8_pdf_truth.py`.

- **27 misure e 37 bitinfo, 100% delle righe con titolo.** REG 2 (16 righe
  bianche) non genera nemmeno la packed; REG 4 tutto a pagina 2, nessun bit
  perso; stazione dichiarata + IP PLC `192.168.1.1:511`; 1 solo warning (CO).
- **Unico difetto: NOx senza scala** (probabile TAG `NO` vs `NOx`, stessa
  classe di fragilità del join). Pinnati: TEXTON `COMANDO` sui superamento,
  refuso `rferito` corretto, `ppm` da descrizione.

## Aggiornamento 12/10 — quarto caso: Essity (run sotto cartella San Marco!)

La run incollata in `TESTS/OSPEDALE SAN MARCO CATANIA/` era di Essity
(registri 160/168/192, limiti 300/375): spostata in `TESTS/ESSITY/`,
archiviata come `tests/case_10/` con `test_adas_caso10_pdf_truth.py`.

- **DB100 perfetta**: 20/20 misure, 24/24 bit, stazione + IP giusti, gateway ignorato.
- **Difetto nuovo**: 3 misure AI-DB50 con registri inventati dai DBD (la mappa
  DB50 non ha colonna MODBUS: andavano scartate). Le altre 18 righe DB50
  scartate con warning: la guardia funziona, il buco è il fallback VLM.
- Pinnati: `FAILURE → ATTIVO`, supero → `ALLARME` (terza variante).

## Aggiornamento 12/10 — quinto caso: San Marco (35/50 al 100%, 1 IP ambiguo)

Run in `tests/case_9/` con `test_adas_caso9_pdf_truth.py`: **35 misure e 50
bitinfo, 100% delle righe con titolo** (la scheda pre-run ne contava 33/45 per
due errori di lettura: SET 401/402 e Scansione 0–3). NO collegato, QG sentinel
corretto, 4 limiti, niente scarti né divisioni.

- **IP ambiguo (da cliente)**: uscita `.11` (caldaie) ma il JOB assegna questo
  IOL (`.02`) ai motori (`.21/.22`).
- **DRIVERDATA=1** su 5 comandi (inferenza R/W incoerente), **TEXTON supero
  divisi** ALLARME/eco-nome nella stessa run: regole da fissare.

## 3. Mancante, in ordine di priorità

1. **5 stati d'impianto persi sul caso 7** (unico buco grave). La cella `REG 4` è unita e attraversa il confine di pagina (DBX 70.0 a p2 → DBX 71.7 a p3): a p3 la colonna è vuota, il VLM restituisce `null`, il pytool scarta. Sono le colonne `STATI IMPIANTO` della Tabella 12 del JOB (validazioni): senza questi la matrice di invalidazione delle misure perde l'input. Serve il carry-over oltre il confine di pagina nel consolidatore.
2. **Unità 4/18 e limiti 0/5 sul caso 7.** Il JOB li dichiara tutti (Tabella 9), ma il join scala↔misura è per uguaglianza esatta di stringa mentre il JOB usa i tag (`TF`, `O2S`) e l'IOL descrive a parole: le 4 applicate sono i 4 tag che coincidono. Serve portare il `tag` IOL nel chunk e agganciare su quello.
3. **Fattori `Dividere x10`** delle 9 misure asteriscate (JOB 4.5.2, colonna RANGE IOL): non raccolti.
4. **Misura 166 col nome sbagliato** (caso 7 run3): TAG `COT_XTM` con descrizione vuota emessa come seconda `Misura stimata CO`.
5. **Prova di importazione in ADAS reale**: mai fatta. Validazione solo contro PDF e schema.
6. Terza coppia mai vista; decisioni cliente (BISON, zeri iniziali, regola V2, nome stazione, unità inferite).

## 4. Guida alla verifica: dal JSON al punto esatto del PDF

Ogni campo dell'output ADAS ha una fonte precisa nella coppia. Metodo generale: aprire l'IOL, cercare la DESCRIZIONE (testo), leggere sulla **stessa riga** le colonne REG/BIT/TIPO; aprire il JOB per scale, unità, limiti e validazioni. Attenzione: la colonna REG è a celle unite (il valore compare una volta e vale fino al prossimo numero) e il testo grezzo estratto perde questa struttura: per i registri servono le coordinate delle celle.

### 4.1 Mappa campo → fonte

| Campo JSON | Dove si verifica | Come |
|---|---|---|
| `NAME` stazione | JOB, intestazione (Oggetto/Titolo) | Caso 7: `Sistema Analisi Emissioni` è dichiarato. Caso 6: dedotto (`Sistema Analisi SO2`; nel PDF: `Impianto lavorazione SO2`) |
| `DRIVERCONFIG` IP/porta | JOB Tabella 8 (indirizzi) | Caso 6: `10.100.50.95:511`. Caso 7: PLC `172.16.1.31:511` (i due IP del PC SME non fanno stazione) |
| `NAME` misura | IOL, colonna DESCRIZIONE | Testo letterale della riga (mai dal TAG) |
| Registro (`DRIVERPRIVATE` primo blocco, little-endian) | IOL, colonna REG | Cella unita: vale per tutte le righe sotto fino al prossimo numero. Convertire: `struct "<I"` dei primi 8 hex |
| `BITNO` | IOL, colonna BIT | Copia letterale della riga (0–15). Le righe bianche (senza TITOLO) non generano bit |
| Formato (ultimo blocco: 150/250) | IOL, colonna TIPO | `INT`→150, `REAL`/`WORD`→250. Verificare contro TIPO, non contro il nome |
| `UNITS` | JOB Tabella 9 (caso 7); scala dichiarata (caso 6) | Caso 6: il PDF non ha colonna unità, `mg/Nm3` solo dove la scala SO2 è dichiarata. Caso 7: 18 unità dichiarate, 4 applicate |
| `TEXTON`/`TEXTOFF` | Nessuna colonna: derivati da keyword | Convenzione documentata, non lettura. Nel PDF non esiste testo di stato |
| Limiti | JOB Tabella 9 (giornaliero/orario) | Dichiarati (es. CO 40/50), mai applicati: in ADAS resta il sentinel `∓3.40282e38` |
| `MEASUREID` | Relazionale, non documentale | ID sequenziale della misura (il legacy usava il registro: non confrontarli) |
| `_warnings` | Diagnostica di pipeline | `VARIABILI SENZA INDIRIZZO` elenca le righe scartate (nel caso 7 sono i 5 stati persi) |

### 4.2 Tabelle verità per caso

**Caso 6** (`Mappatura_6_Cliente_SMI_1.pdf`, 5 pagine): REG 1 bit 8–13; REG 3 bit 8–11/15/0–3/5–7; REG 4 bit 8–11/13/0–3/5–7; REG 5 bit 8–15/1/2/4/5 (PM-302A=1, PM-302B=2, PM-310A=4, PM-310B=5); REG 6 bit 8–13/0–3 (ventilatori 0–3); REG 9/10/11 QAL3 `INT`; REG 17 SO2 Raw, 33 TF Raw, 49 SO2, 65 TF (`REAL`); comandi 417–419/425–427/431/432; stimate 433/441. Totale 60 bitinfo.

**Caso 7** (`Mappatura_7_Cliente_SMI_2.pdf`, 4 pagine): REG 1 16 bit con wrap 8→15 poi 0–7; REG 2 un bit (8); REG 3 bit 8/10–15/7; REG 4 bit 8/10–13/0–7 (di cui 3–7 a pagina 3: i 5 persi); Misure 17–42 `INT` (buchi bianchi 21/24/26/29–32/40); Comandi 145–158 (buchi 146/151/154–156/159–160); Stimate 161–172 (buchi 165/168/170/173–176). Totale atteso 47 bitinfo.

### 4.3 Trappole note (errori già commessi e chiusi)

- Confrontare col legacy invece che col PDF (il legacy ha 18 bit fantasma nel caso 6).
- Leggere il registro dalla colonna INDIRIZZO (`DBX 73.1` non è il registro 73).
- Trattare il passaggio BIT 15→0 come nuovo registro (è il wrap dello stesso).
- Contare le righe bianche come misure (DBW 902–910, 420–424, 428–430).
- Cercare le unità nell'IOL del caso 6 (non esistono: sono inferenze del legacy).
- Confrontare `MEASUREID` col registro (è un ID sequenziale, per disegno).
