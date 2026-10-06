# Caso di prova 7

Coppia `Mappatura_7_Cliente_SMI_2` e `Mappatura_7_Descrizione_Cliente_SMI_2`, usata per verificare che il classificatore di ruolo generalizzi oltre il caso 6.

## Input e risultato

- `Mappatura_7_Cliente_SMI_2.pdf`: 4 pagine.
- `Mappatura_7_Descrizione_Cliente_SMI_2.pdf`: 7 pagine.
- L'output LV1 osservato contiene 11 pagine uniche: 4 classificate `IOL`, poi 7 `JOB`. I conteggi corrispondono alle lunghezze dei due PDF; le chiavi non conservano il nome del file, quindi l'attribuzione di ruolo è basata sulla classificazione visiva.
- Esito: `status: OK`, `review_required: true`, un conflitto di categoria all'indice 10, risolto come `STATION_INFORMATION` con la priorità legacy.

Output anonimizzato: [`outputs/observed_role_v2_dedup_sanitized.json`](outputs/observed_role_v2_dedup_sanitized.json). Le chiavi Medex effimere sono state sostituite con `CASE7_PAGE_nn`.

## Uscita ADAS 3.8 (5/10/2026)

Run canvas completa fino al nodo 12: [`outputs/observed_adas_case7_qwen38_run2.json`](outputs/observed_adas_case7_qwen38_run2.json) — stazione `172.16.1.31:511`, 39 misure (4 packed + 18 analogiche + 9 singoli + 8 stimate), 42 bitinfo, linkage intatto. Fixture precedente: [`outputs/observed_adas_case7_qwen38.json`](outputs/observed_adas_case7_qwen38.json).

## Run5 con nodo 11 v4.5 e prompt v6 (6/10, riferimento attuale)

Fixture: [`outputs/observed_adas_case7_qwen38_run5.json`](outputs/observed_adas_case7_qwen38_run5.json) — **40 misure, 47 bitinfo**.

- **17 unità su 18** (anche le due O2 con `%` e range 0/25; resta fuori solo `Consumo combustibile orario`, la cui riga scala non porta l'unità).
- **Range reali ovunque dichiarati** (CO 0/200, TF 0/500, Q_OIL 0/110000...), sentinel solo sulle stimate.
- **Warning nuovi v4.5**: limiti (5 misure) e divisioni (9) elencati coi nomi, come da decisione.
- REG 166 tornato a `Misura stimata CO`: il nome oscilla per run (CO/COT), fissato in `test_misura_166_nome_variabile_per_run`.
- Stazione di nuovo `SME` (ramo Station null).

## Run4 con nodo 11 aggiornato + prompt v6 (6/10)

Fixture: [`outputs/observed_adas_case7_qwen38_run4.json`](outputs/observed_adas_case7_qwen38_run4.json) — **40 misure, 47 bitinfo: 100% del PDF**.

- **I 5 stati ci sono** (bit 3–7 di REG 4, TEXTON da keyword): il carry-over oltre il confine di pagina funziona, nessun warning, `review` con 5 voci `registro_applicato`. Fissato in `../test_adas_caso7_pdf_truth.py::test_stati_recuperati_con_carry_over`.
- **16 unità su 18** (join per TAG): restano fuori solo `O2 Secco` e `O2 Umido` (`%`), caso noto da investigare sul chunk.
- **REG 166 corretto**: esce come `Misura stimata COT` (era il duplicato sbagliato della run3).
- Sentinel e `UNITS2` confermati. Unità in apice (`mg/Nm³`) come run2: il VLM alterna ASCII e apice tra run, i test normalizzano.
- **Nome stazione `SME`**: il ramo Station ha restituito `null` in questa run e il merge è ripiegato sul default. IP/porta giusti, una sola stazione. Il nome resta una domanda per il cliente.

## Run3 con copia canvas + prompt v5 (6/10/2026)

Fixture: [`outputs/observed_adas_case7_qwen38_run3.json`](outputs/observed_adas_case7_qwen38_run3.json) — 40 misure, 42 bitinfo, sentinel `∓3.40282e38` sulle analogiche (la divergenza dal repo è chiusa), `UNITS2` popolato sulle 4 misure con unità, unità in ASCII (`mg/Nm3`, come JOB e GT legacy).

Rispetto alla run2 cambia poco ma in meglio sui TEXTON packed (ora da keyword): le due `STATO ELETTROVALVOLA` da `ATTIVO` ad `APERTO`, resto invariato. I 5 stati persi restano persi (stesso warning), le unità restano 4/18, i limiti 0/5.

Una misura in più, col nome sbagliato: al REG 166 esce una seconda `Misura stimata CO`. Nel PDF (pagina 4 IOL) la riga DBW 394 ha TAG `COT_XTM` e descrizione vuota: il registro esiste, il nome no (dovrebbe essere la stimata del COT). Fissato in `../test_adas_caso7_pdf_truth.py::test_difetto_conosciuto_misura_166_con_nome_sbagliato`.

### Verdetto contro il PDF IOL (5/10, `../test_adas_caso7_pdf_truth.py`)

Il PDF `Mappatura_7_Cliente_SMI_2.pdf` (4 pagine) dà **39 misure e 47 bitinfo**. L'output ha 39 misure corrette e **42** bitinfo: ne mancano 5.

Tutto il resto è conforme al PDF, riga per riga:

- **Registri**: 1, 2, 3, 4 (impaccati), 17–42 (`Misure`), 145–158 (`Comandi`), 161–172 (`Dati stimati`). Tutti corretti, nessuno spostato.
- **Bit**: REG 1 ha i 16 bit con wrap 8→15 poi 0→7; REG 2 un solo bit (8); REG 3 ha 8, 10–15, 7 saltando i bianchi 9 e 0–6; REG 4 ha 8, 10–13, 0–2 più i 5 perduti.
- **Formato**: `TIPO=INT` nel PDF sul blocco `Misure` → 150 sulle 18 analogiche; `TIPO=WORD` su `Dati stimati` → 250 sulle 8 stimate. `DATA_TYPE` letto correttamente, a differenza della run precedente che dava 250 ovunque.

### Cosa dice il JOB (7 pagine) e cosa ne facciamo

Il JOB.0105.22 è parte della verità quanto l'IOL, e su questo caso dice cose che l'IOL non dice:

| Contenuto JOB | Effetto sull'output |
|---|---|
| **Tabella 8**: `PC SME` due schede (192.168.70.103, 172.16.1.10), `PLC` **172.16.1.31:511** | ✅ Corretto: una sola stazione con l'IP del PLC e la porta giusta. I due IP del PC SME non generano stazioni |
| **Oggetto/Titolo**: `Sistema Analisi Emissioni` | ✅ Il nome stazione coincide col titolo: qui è **dichiarato**, non dedotto (nel caso 6 era dedotto) |
| **Tabella 9**: 19 righe di campi scala con unità e limiti | ✅ 16 unità e scale collegate in run4 (restano fuori O2 Secco/Umido); limiti dichiarati ma mai applicati in ADAS |
| **4.7 Tabella 12 (validazioni)**: colonne `STATI IMPIANTO` = Fermo, Manutenzione, Fuori servizio, Lavaggio | ✅ dal run4 sono i bit 3–7 di REG 4, presenti: la matrice ha di nuovo input |
| **4.5.2**: misure non asteriscate con campo 0…10000 da riscalare; le 9 asteriscate già in unità ingegneristiche, "dividere 10" | ❌ L'istruzione è anche scritta nella colonna `RANGE` dell'IOL (`Dividere x10` sui registri 33-39, 41-42). Non la raccogliamo da nessuna delle due fonti |

### Difetti aperti (run4)

1. ~~Cinque stati d'impianto persi~~ **chiuso in run4** (carry-over oltre pagina, `registro_applicato`; erano le colonne `STATI IMPIANTO` di Tabella 12).
2. ~~Join per uguaglianza esatta~~ **chiuso in run4** (TAG IOL nel chunk, 16/18 unità; restano fuori O2 Secco/Umido).
3. **Limiti giornalieri e orari mai applicati.** Il JOB li dichiara (CO 40/50 mg/Nm3, NO 30/37.5, NH3 2/2.5, COT 10, PLV 10) e il consolidatore li mette nel chunk (`limit_day`, `limit_hour`), ma `json_creator` non li legge: scrive costanti sentinella.
4. **I fattori "Dividere x10" delle 9 misure asteriscate non sono raccolti**, né dall'IOL (colonna RANGE) né dal JOB (4.5.2).
5. ~~Script del nodo 12 divergente~~ **chiuso il 6/10** (copia canvas AST-identica + test di parità).

## Lettura

Il caso 7 supporta la distinzione dei ruoli su una seconda coppia e con conteggi diversi dal caso 6. Resta un singolo avviso di categoria sulle finestre sovrapposte: la pagina corrispondente va verificata visivamente prima di considerare definitiva l'etichetta. Il risultato non dimostra da solo il comportamento su tutte le possibili coppie o layout.
