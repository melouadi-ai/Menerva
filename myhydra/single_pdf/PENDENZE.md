# Modifiche necessarie — Single PDF

Registro di lavoro compilato il 1 ottobre 2026 durante una sessione di validazione. **Non è una specifica**: raccoglie ciò che è stato verificato, ciò che è aperto e le scelte che spettano al cliente.

Ogni voce ha la sua evidenza e il comando per ricontrollarla. Ordinato per impatto.

---

## Dove siamo

Il Single PDF ha il prompt v13 e il pytool v4.3. La pipeline funziona ed è stata verificata contro i PDF reali, ma restano tre difetti aperti e un disallineamento fra le due copie del pytool.

Stato verificato oggi:

```sh
cd /home/next/Desktop/Menerva_MAS
.venv/bin/python tests/test_casi_reali.py
# RESULT: 13 passed, 2 failed

.venv/bin/python tests/test_multipage.py
# RESULT: 33 passed, 0 failed
```

I due fallimenti sono lo stesso difetto, trattato in A1.

---

## Blocco A — bloccanti

### A1. L'avviso di copertura non può scattare mai

**File:** `src/nodes/json_creator.py`, guardia della v4.3.

La condizione scritta è:

```python
if len(pages) > 1 and len(chunks) == 1:
```

Un array di pagine viene parsato come **un chunk solo** (la lista viene accodata come un unico elemento), quel chunk è una lista, e le stazioni vengono appiattite in **una pagina sola**. Quindi `len(pages) == 1` sempre: la condizione è falsa per costruzione, non per circostanza.

Conseguenza: la perdita di copertura più costosa del progetto (SIEMENS_2, 1116 righe nel documento contro 274 variabili ricevute dal pytool) resta invisibile in produzione. Oggi si vede solo perché esiste `verifica_pdf/confronta.py`.

**Il segnale giusto non è il numero di pagine**, perché un chunk unico non distingue "un PDF di una pagina" da "un PDF da 29 pagine accorpato". Il segnale è: **tutte le stazioni hanno lo stesso `page_no` e sono più di una**.

Da correggere la guardia su questa base, con tre condizioni, altrimenti si aggiunge rumore:

- più di una stazione in ingresso
- tutte con lo stesso `page_no`
- volume di variabili sopra una soglia, per non segnalare documenti legittimamente piccoli

**La soglia è una scelta, non un requisito.** Con `tv > 40` il documento SMA_1 (una pagina, 45 variabili) non scatta, che è il comportamento voluto. Ma se in futuro SMA_1 avrà più variabili su una pagina sola, scatterà su un documento legittimo. Una soglia più conservativa (100) produce meno falsi positivi e rischia di non segnalare nulla. Da scegliere conoscendo il volume tipico dei documenti.

Test da correggere insieme: `tests/test_casi_reali.py::test_warning_copertura` e `::test_nessun_avviso_su_documento_singola_pagina`.

### A2. La copia del pytool in `myhydra/` non è quella in `src/`

**Verificato oggi:**

```text
src/nodes/json_creator.py                      73f4c830...  (v4.3)
myhydra/single_pdf/pytools/json_creator_v4_2.py 152ff300...  (v4.2)
```

Il file in `myhydra/` è ancora la v4.2, e l'hash dichiarato in `pytools/README.md` è quello della v4.2, quindi l'hash è **corretto rispetto al file che c'è**, ma il file non è quello in uso.

Se qualcuno prende lo script da `myhydra/single_pdf/pytools/` per incollarlo sul canvas, usa la v4.2: le misure a registro 0 e gli avvisi di copertura non ci sono.

Da fare quando A1 è risolto: sincronizzare la copia, rinominarla in `json_creator_v4_3.py` e aggiornare hash e versione nel README. Non prima, altrimenti si sincronizza due volte.

### A3. Le fixture storiche contengono ancora il difetto che la v4.3 corregge

`Outputs MYHYDRA/Output SMA_1.txt` ha **6 misure con `DRIVERPRIVATE` a zero**:

| Stazione | Misura | Nel PDF |
|---|---|---|
| E1 | NOX | riga `CALCOLATA`, nessun indirizzo |
| E1 | H2O | `CALCOLATA`, nessun indirizzo |
| E1 | PORTATA FUMI umida | `CALCOLATA`, nessun indirizzo |
| E1 | Polveri | `CALCOLATA`, nessun indirizzo |
| E1 | Polveri TQ | `CALCOLATA`, nessun indirizzo |
| E1 | Anomalia Collegamento ADAM | tipo `Modbus`, colonna indirizzo vuota |

Sono grandezze derivate: il documento non ha loro un indirizzo Modbus. La v4.3 le scarta. Le fixture no, perché sono l'output della v4.2.

Non è un errore: sono la baseline del run storico. Ma `test_registro_zero_assente_negli_output_storici` le controlla e deve continuare a farlo, altrimenti il difetto non resta visibile.

**Da fare**: quando si rigenerano gli output, produrre una cartella separata e non sovrascrivere. Il confronto in `verifica_pdf/` usa gli storici come baseline; se cambiano, i report perdono il riferimento.

---

## Blocco B — difetti trovati col confronto, non ancora corretti

### B1. Indirizzi con zeri iniziali

`src/prompts/vlm_extraction_v13.md` e `src/nodes/json_creator.py` trattano due convenzioni diverse come se fossero una.

Nel PDF SMA_1:
- sezioni analogiche: `40001`
- sezioni digitali: `00033`

La normalizzazione del pytool produce `33` dal secondo, che come registro Modbus è diverso da `40033`. Nell'output l'informazione sulla convenzione originale è persa, quindi il confronto riga per riga non può segnalarlo.

La v4.3 aggiunge un **avviso** con l'elenco degli indirizzi a zeri iniziali, ma **non converte**: la conversione è una decisione di dominio.

**Da decidere con il cliente**: nel documento `00033` è un indirizzo HMI o un registro Modbus con zeri di formattazione? Se è HMI, la corrispondenza è `40000 + 33`. Se sono registri con zeri, il valore emesso è giusto e l'avviso basta.

Non decidere per convenienza: le due risposte portano a output diversi.

### B2. IP dichiarati e mai usati

| Caso | IP nel PDF | IP usati |
|---|---|---|
| PROTEC_1 | `192.168.0.1`, `192.168.0.2` | solo il primo |
| PROTEC_2 | `10.127.126.113`, `.114`, `.99` | solo `.99` |
| SIEMENS_2 | cinque, più una subnet mask | solo `192.168.2.11` |

La subnet mask `255.255.255.0` non è filtrata da nessuna regola: è un indirizzo valido per un matcher regex, non un indirizzo di PLC.

La causa non è il pytool, che prende il primo IP non nullo per stazione: è il prompt, che non ha una regola per "più IP reali sulla stessa pagina, anche quando uno non ha variabili". La regola S5 esiste ma dice "una stazione per IP", che il VLM può leggere come "solo dove ho trovato variabili".

**Da fare**: aggiungere al prompt v14 una regola esplicita. Verificabile col confronto: le stazioni attese aumentano.

### B3. La perdita di copertura su SIEMENS_2 è a monte, ma non è dimostrato

`_meta` dell'output storico dichiara:

```text
_meta.variables_total  = 274
_meta.chunks_parsed    = 1
_meta.pages_processed  = 1
```

Il pytool ha ricevuto 274 variabili e ne ha prodotte 251: la differenza sta nel dedup e nelle righe doppie che collassa per progetto. Sulle 1116 righe del PDF **non può aver perso niente, perché non le ha viste**.

Quindi la perdita è nell'estrazione VLM, e `chunks_parsed: 1` su 29 pagine suggerisce che le pagine siano state accorpate in una richiesta invece che inviate una per iterazione. È il rischio n. 1 di ADR-001, concretizzato.

**Ma l'attribuzione al VLM è dedotta, non osservata.** Non è stato riprodotto in locale l'invio delle 29 pagine, quindi non si può escludere che l'accorpamento sia avvenuto nel nodo iterativo, prima del VLM. `verifica_pdf/per_caso/caso_4_siemens_2/report.md` lo dichiara esplicitamente e il caso è marcato come parzialmente validato.

**Da fare**: guardare come il motore raggruppa le richieste. Non serve per A1, che è comunque da correggere, ma serve per chiudere la domanda.

---

## Blocco C — verifiche non riproducibili

### C1. Il caso SIEMENS_2 non è validato

Il confronto mostra 1116 righe e 236 presenti nell'output, con copertura discontinua: alcune pagine interamente scoperte, altre nessuna. Non è un troncamento pulito alle ultime pagine.

L'estrattore funziona (28 pagine su 29, registri e nomi coerenti) ma il confronto non distingue perdita della pipeline da perdita dell'estrattore.

**Da fare**: non tentare di correggerlo senza sapere come è stato generato l'output. Se l'input era un PDF parziale, il confronto va rifatto con l'input completo; se era completo, le 726 righe assenti sono un problema reale e la copertura discontinua ne è il sintomo.

### C2. La regola V2 non copre i nomi prefissati

La regola V2 chiede il confronto esatto: `riserva` va scartato, `Riserva INPUT` no. Ma l'output scarta anche `Riserva INPUT`, che sono 129 righe su SIEMENS_2.

Il report le conta in una sezione a parte invece di registrarle come difetti, perché non si può attribuire la mancanza a un difetto senza scegliere quale comportamento sia atteso.

**Da decidere con il cliente**: se la regola deve restare esatta, l'output scarta più di quanto dovesse. Se deve coprire i prefissi, il prompt va corretto. Sono due output diversi.

Non tarare la regola per farla combaciare con l'output: sarebbe circolare.

### C3. Le fixture senza il campo `data_type`

`test/caso_2_protec_1/inputs/vlm_raw_PROTEC_1_2pages.json` è anteriore alla regola V25 e non ha `data_type`. L'output corrispondente sì.

La conseguenza è che **la regola V25 non è esercitata da nessun test**: formato analogico 150 o 250 a seconda del `data_type` dichiarato è una delle due novità della v4.2 e non è mai stata provata su dati reali.

**Da fare**: rigenerare la fixture da una run col prompt v13, o costruirne una sintetica che copra `INT16` e `REAL32` con lo stesso registro.

---

## Blocco D — igiene

### D1. Il comando dei test non è quello di default

`pyproject.toml` ha `testpaths = ["tests"]`, quindi `pytest` dal root **non** raccoglie `tests/test_casi_reali.py` in posizione attesa e non vede gli altri.

Comandi verificati:

```sh
.venv/bin/python tests/test_casi_reali.py     # 13 passed, 2 failed
.venv/bin/python tests/test_multipage.py      # 33 passed, 0 failed
.venv/bin/python -m pytest myhydra/double_pdf/tests -q   # 23 passed
```

`pymupdf` è solo nel `.venv`, non nel `python3` di sistema: `verifica_pdf/confronta.py` va eseguito con `.venv/bin/python`.

### D2. Documentazione obsoleta da allineare

`docs/contracts/ADAS_FINAL.md` descrive il formato in modo che non coincide con il codice. Vale la pena conoscerlo, perché chi legge solo il contratto scrive il prodotto sbagliato:

| Punto | Contratto | Codice |
|---|---|---|
| Lunghezza di `DRIVERPRIVATE` | 52 caratteri | **48** |
| Primo blocco di 8 hex | tipo di misura | **solo il registro**, little-endian |
| Posizione del registro | ultimo blocco | **primo** blocco |
| Quarta word | non descritta | sempre `00000000`; il legacy vi metteva l'ultimo bit |
| Misure con IP placeholder | scartate, l'IP reale è primario | **sempre stazioni separate e mai scartate** |
| Forma dell'output | oggetto stazione singolo | **lista** di stazioni |

La tabella è già in `pytools/README.md`. Se il contratto non si aggiorna, resta una fonte in conflitto.

`docs/contracts/VLM_INTERMEDIATE.md` dichiara ancora v11 come prompt di riferimento.

### D3. Il refuso del documento, non del VLM

Correzione rispetto a una nota precedente: in PROTEC_1, alla riga `40001.2`, il campo stato contiene `Rchiesta Mnautenzione`. **Il refuso è nel PDF.** La riga adiacente `40001.6` ha la forma corretta `Richiesta Manutenzione`.

Quindi il VLM ha trascritto fedelmente e il ground truth legacy è stato quello che ha corretto di nascosto. Vale la pena saperlo prima di giudicare qualità dell'estrazione: è una divergenza di politica, non un errore.

`test/caso_2_protec_1/README.md` contiene ancora l'affermazione opposta. Da correggere quando si affronta D2.

---

## Riepilogo

| # | Voce | Tipo | Stato |
|---|---|---|---|
| A1 | Avviso di copertura mai attivabile | codice | ✅ risolto 5/10 (v4.4: stesso `page_no` + soglia 100; test dedicati) |
| A2 | Copia pytool in `myhydra/` ancora v4.2 | sincronizzazione | ✅ risolto 5/10 (`json_creator_v4_4.py` + hash, v4.2 conservata come storico) |
| A3 | Fixture storiche col difetto della v4.3 | informazione | da mantenere |
| B1 | Zeri iniziali negli indirizzi | decisione cliente | aperto |
| B2 | IP dichiarati e mai usati | prompt | da fare |
| B3 | Perdita SIEMENS attribuita ma non provata | verifica | da chiudere |
| C1 | Caso SIEMENS non validato | verifica | in attesa di B3 |
| C2 | Regola V2 e nomi prefissati | decisione cliente | aperto |
| C3 | `data_type` mai esercitato | test | da fare |
| D1 | Comandi di test non standard | informazione | da documentare |
| D2 | Contratti in conflitto col codice | documentazione | da allineare |
| D3 | Nota sul refuso da correggere | documentazione | da correggere |

**A1 e A2 sono gli unici due che si risolvono senza aspettare nessuno.** A2 dipende da A1, quindi nell'ordine. Gli altri tre (B1, C2, e in parte C1) aspettano il cliente.
