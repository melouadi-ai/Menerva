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
| **Tabella 9**: 19 righe di campi scala con unità e limiti | ❌ applicate 4 unità su 18 segnali, 0 limiti |
| **4.7 Tabella 12 (validazioni)**: colonne `STATI IMPIANTO` = Fermo, Manutenzione, Fuori servizio, Lavaggio | ❌ Sono **esattamente i 5 bit persi**. La matrice di invalidazione delle misure non ha più input |
| **4.5.2**: misure non asteriscate con campo 0…10000 da riscalare; le 9 asteriscate già in unità ingegneristiche, "dividere 10" | ❌ L'istruzione è anche scritta nella colonna `RANGE` dell'IOL (`Dividere x10` sui registri 33-39, 41-42). Non la raccogliamo da nessuna delle due fonti |

### Difetti aperti

1. **Cinque stati d'impianto persi — carry-over del registro attraverso il confine di pagina.** La cella `REG 4` è unita e copre `DBX 70.0` (pagina 2) fino a `DBX 71.7` (pagina 3). A pagina 3 la colonna `REG` è visivamente vuota, il VLM restituisce `modbus_register: null` e `json_creator` scarta la riga come "variabile senza indirizzo". Persi: `Impianto in spegnimento` (bit 3), `Impianto in lavaggio` (4), `SME in manutenzione` (5), `Impianto in manutenzione` (6), `Impianto fuori servizio per guasto` (7). Il warning li elenca, ma il dato in ADAS non c'è. Nel caso 6 non si è manifestato perché lì la copertura `REG` non attraversa la pagina. **Gravità elevata**: sono le colonne `STATI IMPIANTO` della Tabella 12 del JOB.
2. **Unità: 4 su 18. Il join è il colpevole, non il VLM.** Il JOB identifica i segnali con i **tag** (`CO`, `O2S`, `TF`, `P_MTR`…), l'IOL li descrive a parole (`CO`, `O2 Secco`, `Temperatura fumi`, `Potenza motore`). Il join del consolidatore è esatto: `description == tag` oppure `description == tag + " Raw"`. Le 4 unità applicate sono **esattamente** i 4 tag che coincidono col testo della descrizione; le altre 14 righe di Tabella 9 vengono scartate dal join. Il campo su cui agganciare è il **tag dell'IOL**, che il consolidatore non porta nel chunk.
3. **Limiti giornalieri e orari mai applicati.** Il JOB li dichiara (CO 40/50 mg/Nm3, NO 30/37.5, NH3 2/2.5, COT 10, PLV 10) e il consolidatore li mette nel chunk (`limit_day`, `limit_hour`), ma `json_creator` non li legge: scrive costanti sentinella.
4. **I fattori "Dividere x10" delle 9 misure asteriscate non sono raccolti**, né dall'IOL (colonna RANGE) né dal JOB (4.5.2).
5. **Lo script del nodo 12 non è quello del repo**, vedi [`../../nodes/lv1_07_json_creator_adas.md`](../../nodes/lv1_07_json_creator_adas.md).

## Lettura

Il caso 7 supporta la distinzione dei ruoli su una seconda coppia e con conteggi diversi dal caso 6. Resta un singolo avviso di categoria sulle finestre sovrapposte: la pagina corrispondente va verificata visivamente prima di considerare definitiva l'etichetta. Il risultato non dimostra da solo il comportamento su tutte le possibili coppie o layout.
