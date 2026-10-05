# Progettazione LV2 Measurement Technical Data

**Stato:** cablaggio confermato e output del ramo `MEASURES_BISON` raccolto in due run Qwen 3.8. Il Pytool associa tutte e 7 le risposte alla pagina e al ramo corretti, ma l'estrazione non produce righe: sei risposte sono gusci stazione vuoti e una è `[]`. Non progettare ancora il merge; prima verificare la lettura di una tabella con una prova VLM breve.

## Obiettivo della sottopiattaforma

Ricevere una pagina `MEASUREMENT_TECHNICAL_DATA` per iterazione e ricavarne misure analogiche/digitali e informazioni `bitinfo`, mantenendo la provenienza della pagina (`key`, `sequence_index`, `document_role`, `label`, avvisi). La LV2 non deve unire pagine diverse solo perché riportano lo stesso IP.

## Sequenza proposta sul canvas

| Ordine logico | Tipo | Nome proposto | Funzione |
|---:|---|---|---|
| 1 | Pytool | `ESTRAI CHIAVE PAGINA` | Riusa [`../platforms/lv2/shared/scripts/in_use/extract_page_key.py`](../platforms/lv2/shared/scripts/in_use/extract_page_key.py): estrae la chiave dal record iterativo `{question}`. |
| 2 | Medex | `RECUPERA IMMAGINE PAGINA` | `content2media` sulla chiave del nodo 1. |
| 3 | Visiomaru/VLM | `ESTRAI MISURE E BISON` | Parte dal legacy Nodo 3; estrae le righe di misura e i campi BISON richiesti, con ordine sorgente conservato. |
| 4 | Visiomaru/VLM | `ESTRAI BITINFO E NOMI` | Parte dal legacy Nodo 4; identifica i digitali packed e standalone/CMD e restituisce `MEASUREID`, `BITNO`, `BITNAME`. |
| 5 | Visiomaru/VLM | `ESTRAI STATI TEXTON TEXTOFF` | Parte dal legacy Nodo 5; restituisce `MEASUREID`, `BITNO`, `TEXTON`, `TEXTOFF` per gli stessi bitinfo. |
| 6 | Naive | `OUTPUT TEST MISURE` | Nella prima prova inoltra il risultato grezzo del VLM 3. |
| 7 | Naive | `OUTPUT TEST BITINFO` | Nella prima prova inoltra il risultato grezzo del VLM 4. |
| 8 | Naive | `OUTPUT TEST STATI DIGITALI` | Nella prima prova inoltra il risultato grezzo del VLM 5. |
| 10 | Pytool | `ETICHETTA OUTPUT MISURE` | Etichetta il ramo del VLM 1 e aggiunge la pagina iterativa; edge VLM #8 (canvas attuale). |
| 6 | Pytool | `ETICHETTA OUTPUT BITINFO` | Etichetta il ramo del VLM 2 e aggiunge la pagina iterativa; edge VLM #4 (canvas attuale). |
| 7 | Pytool | `ETICHETTA OUTPUT STATI` | Etichetta il ramo del VLM 3 e aggiunge la pagina iterativa; edge VLM #5 (canvas attuale). |

I nodi 3–5 ricevono la stessa immagine prodotta dal nodo 2 e lavorano in parallelo. I nodi 9–11 si inseriscono tra ciascun VLM e il Naive corrispondente. Aggiungono ramo e record pagina letto dalla `{question}` iterativa; trasformano le fence JSON in dati JSON quando possibile, mantenendo la risposta grezza se il parsing fallisce. Non sono il Pytool finale di merge.

### Cablaggio osservato sul canvas

Gli screenshot inviati dall'utente confermano la catena nodo 1 → nodo 2, il fan-out dell'immagine Medex ai tre VLM, i tre Pytool etichettatori e un Naive distinto a valle di ciascun Pytool. Nel canvas aggiornato i collegamenti VLM→Pytool sono #5, #6, #7 e quelli Pytool→Naive sono #8, #9, #10. La verifica riguarda la topologia visibile; gli script etichettatori devono ancora essere eseguiti su MyHydra.

## Contenuto da configurare nei nodi

### Nodo 1 — Pytool `ESTRAI CHIAVE PAGINA`

Incollare il contenuto completo di [`../platforms/lv2/shared/scripts/in_use/extract_page_key.py`](../platforms/lv2/shared/scripts/in_use/extract_page_key.py). Legge la `{question}` della singola iterazione e restituisce la chiave media come stringa semplice.

### Nodo 2 — Medex `RECUPERA IMMAGINE PAGINA`

Usare la chiave passata dall'edge #1:

```text
{"request":"content2media","nume":1,"content":{edge}[1]}
```

L'indice `[1]` corrisponde al collegamento Pytool→Medex #1 mostrato nello screenshot. Se MyHydra rinumera l'edge dopo modifiche al canvas, aggiornare l'indice.

### Nodi 3–5 — prompt VLM

Incollare il contenuto completo del file corrispondente:

| Nodo | Prompt |
|---:|---|
| 3 — `ESTRAI MISURE E BISON` | Powered identity [`measurement_measures_bison_v3.md`](../platforms/lv2/measurement/prompts/current/measurement_measures_bison_v3.md); campo Prompt `{edge.media}[2]` |
| 4 — `ESTRAI BITINFO E NOMI` | Powered identity [`measurement_bitinfo_names_v3.md`](../platforms/lv2/measurement/prompts/current/measurement_bitinfo_names_v3.md); campo Prompt `{edge.media}[3]` |
| 5 — `ESTRAI STATI TEXTON TEXTOFF` | Powered identity [`measurement_bitinfo_states_v3.md`](../platforms/lv2/measurement/prompts/current/measurement_bitinfo_states_v3.md); campo Prompt `{edge.media}[4]` |

Per tutti e tre i VLM lasciare **Context** vuoto e incollare nei rispettivi campi **Powered identity** il contenuto dei file indicati. Gli indici media #2, #3 e #4 sono locali ai collegamenti Medex→VLM di questo canvas. Le versioni v2 sono storiche: avevano messo il riferimento media dentro il testo di istruzioni invece che nel campo Prompt.

### Nodi 9–11 — Pytool etichettatori

Incollare gli script indicati, rispettando gli edge VLM in ingresso osservati nello screenshot aggiornato:

| Nodo | Script | Edge VLM in ingresso |
|---:|---|---:|
| 10 — `ETICHETTA OUTPUT MISURE` | [`../platforms/lv2/measurement/scripts/updated_pending_validation/tag_measurement_measures_output.py`](../platforms/lv2/measurement/scripts/updated_pending_validation/tag_measurement_measures_output.py) | #8 |
| 6 — `ETICHETTA OUTPUT BITINFO` | [`../platforms/lv2/measurement/scripts/updated_pending_validation/tag_measurement_bitinfo_names_output.py`](../platforms/lv2/measurement/scripts/updated_pending_validation/tag_measurement_bitinfo_names_output.py) | #4 |
| 7 — `ETICHETTA OUTPUT STATI` | [`../platforms/lv2/measurement/scripts/updated_pending_validation/tag_measurement_bitinfo_states_output.py`](../platforms/lv2/measurement/scripts/updated_pending_validation/tag_measurement_bitinfo_states_output.py) | #5 |

Ogni script legge anche `{question}` come record pagina dell'iterazione. Se il VLM restituisce JSON in fence Markdown, prova a decodificarlo; in caso di testo non parsabile, conserva risposta grezza ed errore insieme ai metadati della pagina.

### Nodi 6–8 — Naive di prova

Non inserire prompt o codice: lasciare il nodo Naive come forwarding dell'output del rispettivo VLM. Conservare i tre rami separati per poter controllare i payload grezzi.

| Naive | Ingresso |
|---|---|
| Nodo 6 — `OUTPUT TEST MISURE` | Edge #8 dal nodo 9 |
| Nodo 7 — `OUTPUT TEST BITINFO` | Edge #9 dal nodo 10 |
| Nodo 8 — `OUTPUT TEST STATI DIGITALI` | Edge #10 dal nodo 11 |

## Impostazioni e modello VLM osservati

Screenshot condiviso durante la prima elaborazione, per un nodo Visiomaru:

Modelli mostrati nel selettore `Core`:

- `mary - Qwen 3 Next 80B Q4`
- `marycoder - Qwen 3.5 35B Q8.0` (selezionato nello screenshot precedente)
- `marygpt - GPT OSS 120B Q4`
- `maryvl - Qwen 3.5 35B Q8.0 - Vision Language`

Correzione fornita dall'utente dopo aver consultato il tutor: il core attualmente selezionato (`marycoder - Qwen 3.5 35B Q8.0` nell'etichetta UI) corrisponde in realtà al modello Qwen 3.8; il nome mostrato non è stato aggiornato. Perciò mantenere il core già selezionato per questa prova, senza passare a `maryvl`. Applicare lo stesso core nei tre VLM e valutare l'output della run.

| Impostazione | Valore osservato | Indicazione per la prova |
|---|---|---|
| Core da usare nei VLM (confermato da screenshot il 2 ott 2026) | `marycoder - Qwen 3.8 Flash Next 180B 4 bit` | Etichetta UI precedente (`Qwen 3.5 35B Q8.0`) non aggiornata: secondo il tutor il modello effettivo è Qwen 3.8. Applicare lo stesso core nei tre VLM Measurement e nel classifier. |
| Message type | `Text` | Lasciare com'è per ora: il VLM riceve l'immagine dal collegamento Medex; verificare il comportamento dall'output. |
| Temperature | `0,1` | Mantenere bassa per contenere variazioni nell'estrazione. |
| Top P | `0,6` | Mantenere per la run comparativa iniziale. |
| Add current time | Attivo | Disattivare: l'ora corrente non è un dato richiesto dal documento. |
| Use history | Disattivo | Mantenere disattivo perché ogni iterazione tratta una pagina autonoma. |
| Thinker Mode | `0` | Lasciare invariato per questa prova; non è ancora stato confrontato con altre impostazioni. |

La schermata non conferma se i tre VLM hanno identiche impostazioni: controllare nei rispettivi nodi. La qualità di estrazione e l'effettiva ricezione dell'immagine saranno valutate dagli output della run.

### Prova con modello leggero (2 ott 2026, caso 6)

Per corse più veloci è stato provato un VLM più leggero in via globale (quindi anche sul classifier). Esito ramo `MEASURES_BISON`: 9 record `OK`, tutti con `vlm_output: []` e `output_format: JSON`, incluse le pagine IOL 2–4 che contengono tabelle `DESCRIZIONE`/`REG`/`BIT` da 2000–3000 caratteri. Meccanica verificata (envelope, branch, pagina, JSON senza fence), estrazione inutilizzabile: il modello leggero restituisce l'array vuoto anche dove i dati esistono.

### Prova con Qwen 3.8, prompt v3 (2 ott 2026, caso 6)

Prima run Qwen 3.8: 7 pagine (2,3,4,5,8,13,14), zero righe estratte. Le sequenze 2, 4, 5, 8, 13 e 14 restituiscono il guscio placeholder `{"NAME": "SME", "DRIVERNAME": "modbusplc", "DRIVERCONFIG": ":", "ID": 1, "measures": [], "bitinfo": []}`; la sequenza 3 restituisce `[]`. Cinque risposte su sette sono in fence Markdown (`output_format: MARKDOWN_JSON`) nonostante l'istruzione JSON-only.

La run appena ricevuta conferma il pattern: 7 envelope `status: OK`, correttamente etichettati `MEASURES_BISON` e associati alle sequenze 2, 3, 4, 5, 8, 13 e 14. Le sequenze 2, 3, 4, 8, 13 e 14 contengono il guscio vuoto; la 5 contiene `[]`. Sei risposte su sette sono `MARKDOWN_JSON`, una `JSON`. Il tagger ha quindi funzionato; l'estrazione no. Fixture anonimizzata: [`../tests/case_6/outputs/observed_lv2_measurement_qwen38_measures_rerun_sanitized.json`](../tests/case_6/outputs/observed_lv2_measurement_qwen38_measures_rerun_sanitized.json). La gestione del vuoto varia rispetto alla prima run (le pagine 3 e 5 si scambiano `[]` e guscio), ma non cambia il risultato: zero righe estratte.

Il guscio è compatibile con i default del prompt (`NAME: "SME"` senza etichetta, `DRIVERCONFIG: ":"` senza IP/porta); questo mostra che il modello ha prodotto il formato previsto, ma non dimostra da solo che l'immagine sia arrivata correttamente al VLM. Nota di diagnosi: i default stessi fabbricano le stazioni vuote — una pagina senza IP produce un oggetto stazione sintetico invece di `[]`. Se la sonda mostra che il modello legge, il prompt di estrazione va riscritto senza avvolgimento stazione-per-IP (sole righe piatte, join con la stazione per via deterministica dopo). Le pagine IOL 2–4 contengono tabelle reali. Restano da distinguere la lettura/ricezione dell'immagine e la complessità del Powered identity, che supera 600 righe e combina estrazione tabellare, logiche BISON, default stazione e output aggregato. Prossimo test: una sola run del ramo con la [sonda di leggibilità tabella](../platforms/lv2/measurement/prompts/diagnostics/measure_table_readability_probe_v1.md), mantenendo `{edge.media}[2]` nel campo Prompt e sostituendo temporaneamente il Powered identity. La sonda restituisce intestazioni e al massimo cinque righe per ogni pagina iterata; confrontare in particolare le IOL 2–4. Se non trascrive, investigare il media ricevuto; se trascrive, semplificare e separare le istruzioni di estrazione. I rami BITINFO/STATES non sono inclusi nell'output condiviso.

### Evidenza legacy sul layout (2 ott 2026)

Screenshot dei VLM legacy (visio2: `Station Info`, `Measures`, `BitInfo General`, `BitInfo TextON/TextOFF`): il campo **Prompt** conteneva istruzioni e token media insieme, con il token dentro il testo (`{edge.media}[23]`, `[19]`, `[20]`, `[21]` — indici locali a quel canvas). Nessun campo separato, e quella configurazione leggeva. Il layout separato non ha mai prodotto una lettura riuscita su nessun VLM. Ipotesi aggiornata: il token si risolve solo dentro il Prompt insieme alle istruzioni; da verificare con la sonda in layout legacy (token + istruzioni nello stesso campo Prompt).

### Verità PDF pagina 3 IOL (2 ott 2026, coordinate testo)

Ricostruzione righe per coordinate x (REG x=354, BIT x=379) su `Mappatura_6_Cliente_SMI_1.pdf` pagina 3 (DB100: impianto 1). Verdetti: (1) VN-400/2504 e 514K1/514K2 hanno REG vuoto ed ereditano il 6 (ultimo esplicito a PM-2600A; il 7 appartiene alla sezione DBW sotto) — run 3.8 corretta (REG 6), run leggera errata (REG 7); (2) PM-302A BIT=1 e PM-310A BIT=4 da colonna — ramo misure corretto, ramo bitinfo errato (BITNO 0 e 2); (3) righe RAW sparse senza TAG/DESC (REG 19,21,23...) correttamente saltate da entrambi; (4) SO2 Raw REG 17, TF Raw REG 33, QAL3 tempi 9/10/11 confermati; (5) nelle righe NON esiste testo di stato: TEXTON/TEXTOFF sono sintetizzati dal VLM dal nome (Marcia/Allarme/...) con default OFF — dato derivato, non letto. Regole assemblaggio: join su nome con BIT dal ramo misure; scartare BITNAME vuoti/numerici e stati delle righe scartate; TEXTOFF OFF valido come default legacy ma marcato derivato.

### Assemblatore validato su MyHydra (2 ott 2026, caso 6, VLM leggero)

9 pagine `OK`, zero ERROR, zero fence. BIT/TEXTON attaccati dove i rami li danno; review popolate su pagine 2–3 (duplicati, BIT non verificati), pagina 4 completamente pulita (`review: []`, 8 vuoti + 8 stati riserva scartati), JOB vuote silenti. Fixture verdetto: `outputs/observed_lv2_measurement_assembly_light_sanitized.json`. Nota: in questa run il ramo misure non emetteva coppie (NAME,BIT), quindi tutti i packed hanno BIT solo-da-bitinfo marcati non verificati — comportamento previsto dal disegno. Struttura pronta per la serie 3.8.

### Assemblatore per pagina pronto e testato (2 ott 2026)

Script [`assemble_page_measurements.py`](../platforms/lv2/measurement/scripts/updated_pending_validation/assemble_page_measurements.py): legge `{question}` + 3 envelope tagger e unisce per pagina. Regole implementate dalle evidenze: join su nome con BIT dal ramo misure (6/6 PDF); `MEASUREID` mai come chiave; scarto nomi vuoti/numerici; stati delle righe scartate scartati; merge stazioni stesso `DRIVERCONFIG`; `BIT`/`TEXTON`/`TEXTOFF` nulli dove assenti; code revisione (`bit_conflicts`, `unverified_bits` solo packed, `orphan_bitinfo`, duplicati, `missing_bitinfo`, `station_name_mismatch`). Test locali: `tests/test_assemble_page_measurements.py`, 5 casi su fixture serie (pagine 2–4 + vuoti + errori). Nodo canvas esistente: pytool non iterativo `ASSEMBLA MISURE PAGINA` (nodo 8) dentro la sottopiattaforma dopo i tagger (edge tagger→assemblatore `#7`/`#8`/`#9`, uscita `#10` al Naive 9), con tagger misure riallineato a `{edge}[6]` (filo VLM 1→nodo 7 = `#6`).

### Run con blocco DEBUG: diagnosi TEXTON pagina 2 + conflitto pagina 3 chiusi (5 ott 2026)

Blocco `DEBUG` temporaneo nell'assemblatore (chiavi `(MEASUREID,BITNO)` stati, triple bitinfo, coppie misure; rimosso dopo la diagnosi, script finale pulito e 33 test verdi). Esiti run fresca, 7 pagine `OK`:
- Pagina 2: tutti i 30 `TEXTON` attaccati (`Misura/Calibrazione/Zero/Span/Attivo/Avviamento/Aperto/Lavaggio/OK/Errore/Marcia/Anomalia/Spegnimento/Manutenzione/Guasto`), `review: []`, `review_required: false`. I `null` della run precedente erano variabilità del ramo stati tra run (riserve scartate 8 vs 20), non bug assemblatore: stati di questa run chiaveati su REG veri (1,3,4; il 2 è il blocco filler numerico, correttamente assente).
- Pagina 3: stavolta i rami DISACCORDANO e la review scatta come da disegno — `bit_conflicts: PM-302A misure=0 bitinfo=1 (usato 0); PM-302B misure=1 bitinfo=2 (usato 1)`. Il `debug` mostra bitinfo a colonna (1,2,4,5 = verità PDF) contro misure posizionali (0,1). Regola invariata (BIT misure usato + conflitto in review, mai scelta silenziosa); risoluzione per verità PDF favorisce il bitinfo su queste due righe, da applicare in sede review/consolidatore, non cambiando la regola sul singolo caso.
- Pagine 4/5/JOB pulite e confermate (`debug` pagina 4: stati 417–432 con riserve, bitinfo solo su righe nominate).

### BIT dal ramo misure: 6/6 verificati (2 ott 2026)

Coordinate colonna su IOL pagina 2: Sistema in misura BIT 8, Secondo campo SO2 BIT 15, QAL3 in corso BIT 0, Pompa analisi BIT 7 (in aggiunta a PM-302A BIT 1 e PM-310A BIT 4 su pagina 3). In tutti i casi il BIT del ramo misure è corretto e il BITNO del ramo bitinfo è errato. REGOLA ASSEMBLATORE: il BIT della misura vale sempre quello del ramo misure; il BITNO bitinfo non lo sovrascrive mai; discordanza in coda revisione con valore usato. Il BITNO resta utile solo dove il ramo misure non dà BIT (righe singole CMD con BITNO 0, singola riga corrispondente).

### Contraddizione chiusa + errore condiviso tra rami (2 ott 2026, run fresca stesso script)

Re-run con script verificato identico al repo: output auto-coerente, contraddizione sparita — era codice stantio, la review torna credibile. Ma la run fresca rivela un caso peggiore: pagina 3 con BIT posizionali (PM-302A 0, PM-302B 1, PM-310A 2, PM-310B 3...) invece che letti da colonna (PDF: 1, ?, 4, ?). Coppie e bitinfo CONCORDANO sul valore errato → nessuna voce review. Lezione: la review cattura il disaccordo, non l'errore condiviso; solo la verità PDF lo prende. Nota anche: split multi-station assente in questa run (un oggetto solo), `duplicate_states` su p2, 16 nomi numerici scartati, prefissi chiave diversi su 13-14 senza effetti sul join (assemblatore per iterazione, non per chiave).

### Contraddizione review-vs-BIT su pagina 3: spiegazione e chiusura (2 ott 2026)

Output 3.8 p3: TUTTI i 22 BIT uguali ai BITNO bitinfo (PM-302A 0, PM-302B 1, ...), ma review con conflitti `misure=1/2 (usato 1/2)`. Col codice repo è impossibile in un singolo passaggio (conflitto registrato implica output=pair). Spiegazione coerente: output e review prodotti da versioni diverse dello script (run eseguita prima di un ritocco al nodo 8) oppure paste mescolate. Chiusura: re-run con script noto (= versione incollata e verificata identica al repo) e confronto fresco. Se PM-302A esce 1, era codice stantio: chiuso. Se esce 0 con conflitto, si riproduce con gli input.

### Run assemblatore 3.8: struttura perfetta, una contraddizione da sciogliere (2 ott 2026)

7 pagine (2,3,4,5,8,13,14: 11 e 12 a Station in questa run), tutte `OK`. Pagina 4 e 5 e JOB pulite. Pagina 3 senza split multi-station (un oggetto solo). VN-x a REG 6 coerente col PDF. Prefissi chiave diversi tra pagine (DLUEE5GG8D vs DLUG0JIDW2 su 13-14): possibile batch di upload diverso, join resta per chiave intera. Texton nulli su p2-REG4 = copertura stati parziale (documentato, non bug).

ANOMALIA APERTA su pagina 3: review dice `PM-302A in marcia: misure=1 bitinfo=0 (usato 1)` ma il campo BIT in output vale 0 (stesso per PM-302B: detto 2, vale 1... verificare). Impossibile col codice repo (conflitto registrato implica pair-hit implica output=pair). Ipotesi: script su canvas diverso dal repo, oppure envelope con input inattesi. Servono i 3 envelope tagger di pagina 3 per riprodurre in locale. NON usare la review di queste due righe finché non si scioglie.

### Run serie Qwen 3.8: riferimento misure + conflitti BIT (2 ott 2026, caso 6)

27 envelope `OK`, stesse chiavi nei tre rami, zero fence. Fixture misure: `outputs/observed_lv2_measurement_qwen38_serie_measures_sanitized.json` (69 misure, pagina 4 come oggetto singolo, split ID 1/2/3 a pagina 3, mappe `NAME:BIT`). Trovati per l'assemblaggio: (1) conflitto BIT tra rami sulle stesse coppie pagina-nome (PM-302A: BIT 1 nel ramo misure vs BITNO 0 nel bitinfo; PM-310A: 4 vs 2) — join su nome, BIT in coda di revisione; (2) `(MEASUREID,BITNO)` non unico (duplicati nello stesso MID) — chiave di join `(pagina, nome, bit)`; (3) pagina 3 multi-station da fondere (stesso `DRIVERCONFIG`); (4) pagina 4 oggetto singolo da normalizzare a lista; (5) VN-x a REG 6 qui contro REG 7 nella run leggera — conflitto tra run, serve verità PDF; (6) `SME `-prefix incoerente tra rami/pagine — normalizzare contro il ramo Station; (7) stati su righe vuote e `TEXTOFF` sempre `OFF` (un `Attivo` dimostra lettura parziale) — da verificare. Bitinfo/stati serie: conteggi e anomalie in chat, trascrizione completa solo su repaste mirati.

### Run 3 rami stessa run: struttura OK, via alla serie 3.8 (2 ott 2026, caso 6, VLM leggero)

27 envelope `OK` (9 pagine × 3 rami), stesse chiavi nei tre rami, tutti JSON senza fence. Fixture strutturale: `outputs/observed_lv2_measurement_3branch_joinable_sanitized.json` (conteggi + 7 avvisi assemblaggio; contenuto completo nei fixture per-ramo). Struttura validata → via libera alla run serie Qwen 3.8. Note contenuto (da riverificare in serie): `MEASUREID` con tre semantiche (posizionale-gruppi p2, chunk da 16 righe p3, registri veri p4); bitinfo a strategia variabile (righe nominate vs enumerazione bit con filler numerici, duplicati tipo PM-2604A a BITNO 8 e 14); stati su righe riservate da scartare; `TEXTOFF` sempre `OFF` (default prompt?); split multi-station a pagina 3 da fondere; vuoti `[]` vs gusci da normalizzare.

### Ramo bitinfo acquisito (2 ott 2026, caso 6, VLM leggero)

Ramo `BITINFO_NAMES`, 9 pagine: 82 bitinfo su IOL 2–4 (36+30+16), `[]` altrove. Fixture: `outputs/observed_lv2_measurement_bitinfo_names_sanitized.json`. Run diversa dal ramo misure (chiavi `DLUEE5GG8D` vs `DLUDS63GS2`): il join per chiave vale solo dentro la stessa run. Osservazioni per l'assemblaggio: (1) `MEASUREID` con semantica variabile — piccoli id di gruppo su pagine packed (1–6) contro registri veri (417–432) a pagina 4; il join va normalizzato (se `MEASUREID` coincide con un `MODBUSREGISTRO` della pagina, join per registro); (2) 4 nomi bitinfo a pagina 2 senza misura corrispondente (`Sistema in misura`, `Calibrazione automatica in corso`, `Analizzatore SO2 in calibrazione di zero/span`); (3) righe riservate emesse con `BITNAME` vuoto (16 casi: pagina 3 MID6 bit 0–7, pagina 4 reg 420–424/428–430) — da scartare in assemblaggio come faceva `Delete Null names`. Manca il ramo stati per chiudere il join bit→stati.

### Prima estrazione completa (2 ott 2026, caso 6, VLM leggero)

Ramo `MEASURES_BISON`, 9 pagine: 65 misure su IOL 2–5 (26+27+11+1), `[]` su JOB 8,11–14. Fixture: `outputs/observed_lv2_measurement_light_full_sanitized.json`. Nomi radicati nel PDF pagina per pagina. Regole osservate nell'output: carry-over REG, skip righe fantasma (420–424 assenti prima di Ack allarmi 425), suffisso ` Raw`, CMD→`(5,6)`, prefisso `SME ` solo a pagina 5. Correzione di rotta: i vuoti precedenti del leggero erano plumbing (immagine assente), non incapacità del modello — con immagini e prompt v3 estrae anche lui. Resta da acquisire i rami BITINFO/STATES e la run 3.8 di confronto.

### Filtro Measurement vuoto (2 ott 2026)

Colpo di scena: tap sul dedup della stessa run (stesso prefisso chiavi `DLUDD429CY`): 14 pagine sane, 9 Measurement (2,3,4,5,8,11,12,13,14), 4 Station, 1 Density, zero warning. Il classificatore funziona; tap sul prep: array completo di 14 record. Il buco è nel filtro 7 o nel suo output: da controllare variabile di output (`result`) ed edge in ingresso. Precedente identico già visto (variabile persa incollando): spiegherebbe tap vuoto + iniezione affamata + `{question}` vuota in un colpo solo.

Run Station con VLM leggero, ramo Measurement scollegato, nodi Station intoccati: 4 record (sequenze 6,7,9,10) con attribuzione pagina intatta e dati veri (IP `10.100.50.95`, porta 511, scale SO2/TF). Fixture: `outputs/observed_lv2_station_information_light_run_sanitized.json`. Il classificatore leggero ha assegnato 4 pagine Station (11 e 12 finite altrove: variabilità nota). Conclusione aggiornata: il tagger ricostruito da zero mostra ancora `{question}` vuota, quindi non era il nodo. Ipotesi corrente: per la run Station si era scollegato l'ingresso dell'iniezione Measurement — se non ricollegato, l'iniezione gira a vuoto (`{question}` vuota in Medex e tagger, VLM senza immagine) pur con fili `{edge}` funzionanti. Da verificare il filo `FILTER_MEASUREMENT_TECHNICAL_DATA` → iniezione in LV1 prima di qualsiasi altra diagnosi. Cura proposta precedente (ricostruzione nodi) superata e archiviata.

Run con modello leggero, tre envelope `ERROR` (uno per ramo): output VLM presenti (`[]`, guscio SME, `[]`) ma `page_raw: ""` in tutti i tagger. Stesso errore con Qwen 3.8 (gusci con e senza fence). Sistematico su tutti i rami e su entrambi i modelli = contesto di iterazione assente, non bug di script né di modello. Ipotesi interruttore (`Aggiungi la domanda al prompt`) scartata: inserisce solo il placeholder, non abilita nulla; script del nodo 7 verificato corretto (`{question}` + `{edge}[4]`). Ipotesi corrente: i nodi modificati dopo la sonda riuscita (tagger riallineati, Medex con `content` cambiato più volte, VLM con prompt sostituiti) hanno perso il legame col contesto di iterazione, mentre i fili `{edge}` funzionano. Test dirimente eseguito (vedi sopra): Station funziona, quindi il problema è locale ai nodi Measurement modificati.

### Sonda di leggibilità riuscita (2 ott 2026, caso 6)

Medex con `content` dal record `{question}`, senza Pytool estrai-chiave (idea del tutor, confermata dal precedente classifier). Canvas ristrutturato: Medex è il nodo 10 in testa, i VLM sono i nodi 1/2/3 con edge `#1`/`#2`/`#3`, etichettatori 7/8/9, Naive 4/5/6. Sonda su pagina singola (sequenza 2): `image_readable: true`, heading `I/O List`, 5 righe trascritte alla lettera e radicate nel PDF (`AL_SONDA` a pagina 2 IOL, colonne `DESCRIZIONE`/`REG`/`BIT`). Fixture: `outputs/observed_lv2_measurement_probe_readable_sanitized.json`. Il modello legge; le regole di estrazione non sono mai state il blocco. La storia completa dei tentativi falliti resta nei paragrafi sotto (sonda Medex, verifiche canvas).

**Attenzione edge rinumerati**: i Prompt dei tre VLM vanno ricontrollati (`[1]`/`[2]`/`[3]` sui fili nuovi) — i vecchi indici `[2]`/`[3]`/`[4]` puntano ad altri fili.

Naive tappato sull'output Medex senza media abilitato: risponde con il token letterale `[{edge.media}[7]]` non risolto. Re-test con Medex diretto come output della sottopiattaforma: `[]`, nessuna immagine risolta. Sonda sul nodo 1 con Naive su `#6`: emette la chiave corretta, quindi `ESTRAI CHIAVE PAGINA` funziona e l'iniezione gli passa la pagina. Fix applicato (`{edge}[1]`, filo di sonda rimosso) ma il Medex emette ancora `[]`. Nota del tutor: il Pytool `ESTRAI CHIAVE PAGINA` (nodo 1) potrebbe essere superfluo — il Medex leggerebbe da solo la chiave dal record in arrivo da LV1. Precedente a favore: nel Page Classifier non esiste estrai-chiave e il Medex consuma direttamente le finestre. Test proposto: `content` ← `{question}` (record pagina intero) bypassando il nodo 1. Attenzione: togliendo il nodo 1 gli edge si rinumerano — ricontrollare gli `{edge.media}[N]` nei Prompt dei VLM dopo la modifica.

Filtro debug a pagina singola (prima IOL + Measurement: sequenza 2) + sonda al posto della Powered identity v3. Esito: 1 record `OK`, schema della sonda rispettato alla lettera (JSON valido, niente fence), ma `image_readable: false` con tutto il resto nullo/vuoto. Fixture: `outputs/observed_lv2_measurement_probe_sanitized.json`.

Verifiche sul canvas (da screenshot): campo Prompt di `ESTRAI MISURE E BISON` contiene esattamente `{edge.media}[2]`; core selezionato `marycoder - Qwen 3.8 Flash Next 180B 4 bit`; `Tipo messaggio: Testo`. Configurazione apparentemente corretta, ma il VLM dichiara immagine assente. Ipotesi rimaste: token media non risolto in questo nodo nonostante la sintassi giusta (la separazione dei campi non è mai stata verificata con successo su nessun VLM: anche le classificazioni post-separazione vanno ricontrollate), oppure Medex del ramo che non emette. Prossimo passo: confrontare campo per campo con un VLM che legge (classifier/Station) e, se identici, sonda Naive diretta sull'output Medex del ramo.

Regola confermata: modello leggero 3.6 solo per prove di plumbing; la qualità di estrazione si giudica solo con Qwen 3.8, e i confronti tra run valgono solo a parità di modello e di classificazione.

## Prima raccolta output condivisa

Il materiale incollato dall'utente contiene almeno cinque blocchi fenced `json` concatenati, senza indicazione del Naive/nodo sorgente accanto a ciascun blocco. Quattro blocchi completi sono JSON validi: tre restituiscono il placeholder legacy con `NAME: "SME"`, `DRIVERCONFIG: ":"`, `measures: []` e `bitinfo: []`; l'ultimo contiene 20 misure. Un blocco lungo è troncato nella copia allegata a metà di una proprietà (`"TYPE,`), quindi non è possibile stabilire se fosse troncato il payload originale o solo la copia. L'output fornito non consente di distinguere con certezza i rami né di concludere che i VLM abbiano unito le proprie risposte: manca l'etichetta di provenienza nella raccolta.

Le risposte sono inoltre racchiuse in fence Markdown ` ```json ` nonostante l'istruzione JSON-only. Non attribuire ancora questi blocchi ai tre VLM né usarli per scrivere l'assemblatore. Per la prossima run inserire un Pytool tra VLM e Naive per ramo, così ogni output sarà autonomamente identificabile e associato alla pagina. I placeholder vuoti derivano dalla forma legacy; dopo aver separato i rami, decidere se introdurre una nuova versione dei prompt che restituisca `[]` quando la pagina non contiene righe estraibili, evitando station vuote sintetiche.

### Formato diagnostico proposto

Ogni Pytool etichettatore dovrà produrre un envelope simile a questo, anche quando l'output VLM non si può interpretare come JSON:

```json
{
  "diagnostic": "LV2_MEASUREMENT_BRANCH",
  "branch": "MEASURES_BISON",
  "page": {
    "key": "<media key>",
    "sequence_index": 8,
    "document_role": "JOB",
    "label": "MEASUREMENT_TECHNICAL_DATA"
  },
  "output_format": "MARKDOWN_JSON",
  "vlm_output": [ ... ]
}
```

Usare valori distinti per `branch`: `MEASURES_BISON`, `BITINFO_NAMES`, `BITINFO_STATES`. Se la risposta non è JSON parsabile, l'envelope include `vlm_output_raw` e `parse_error`. In questo modo il collector può aggregare gli output senza perdere il ramo né la pagina. Dopo la ristrutturazione con Medex come nodo 10, gli edge VLM→tagger sono `#4`, `#6` e `#7` (verificare sul canvas: gli script leggono `{edge}[4]`, `[6]`, `[7]`).

## Ambito della run

Avviare la platform LV1 principale esegue anche i rami collegati che ricevono pagine. Nel caso 6, il filtro Station produce pagine, quindi viene attivata anche l'iniezione LV2 Station oltre a Measurement. Per una run di sola diagnosi Measurement, scollegare temporaneamente in LV1 il collegamento in ingresso alla sottopiattaforma Station (senza eliminare nodi o script), avviare la prova e ripristinare il collegamento dopo. Non si riporta un numero edge LV1 perché il canvas principale corrente non è visibile nello screenshot Measurement più recente.

## Forma obiettivo dell'output per pagina

Il Pytool di assemblaggio, da progettare dopo aver visto gli output VLM reali, dovrà produrre un record per pagina e preservare la provenienza. Forma concettuale:

```json
{
  "key": "<chiave media>",
  "sequence_index": 0,
  "document_role": "JOB",
  "label": "MEASUREMENT_TECHNICAL_DATA",
  "review_required": false,
  "review_warnings": [],
  "measurement_info": {
    "stations": [],
    "bitinfo": []
  }
}
```

Le `bitinfo` generali e gli stati `TEXTON/TEXTOFF` si associano all'interno della stessa pagina con `MEASUREID` e `BITNO`; non usare solo `DRIVERCONFIG` come chiave di join. Se un output manca o non si associa, conservare un errore/avviso con la pagina, senza scartare le estrazioni valide degli altri rami.

## Cosa migrare dal legacy

| Nodo legacy | Ruolo funzionale | Decisione per il nuovo flusso |
|---|---|---|
| Nodo 1 — Take the correct key | Estrae la chiave dalla finestra di pagina | Riutilizzare il Pytool chiave della LV2 Station. |
| Nodo 2 — Medex | Risolve la chiave in immagine | Riutilizzare `content2media` della LV2 Station. |
| Nodo 3 — VLM Measures * Bison | Estrae oggetti station e righe `measures`, compresi tipo, registro, unità, limiti/range, scale, divisione, `GROUP` e regole BISON | Adattare il prompt a una pagina; evitare merge cross-pagina e default inventati. |
| Nodo 4 — VLM Bitinfo General | Rileva righe digitali e `BITNAME` | Conservare le regole packed/standalone, carry-over REG, bit e skip delle righe vuote. |
| Nodo 5 — VLM Bitinfo TextON/OFF | Calcola i due stati logici | Associare allo stesso `MEASUREID`/`BITNO`; unire solo con il ramo Bitinfo General. |
| Nodi 6–9 — Pytool merge | Pulisce e combina misure, stati e bitinfo usando chiavi di stazione/IP | Non portare subito il merge per IP dentro la LV2 iterativa: assemblare prima i rami della stessa pagina. |
| Nodo 10 — Delete Null names | Rimuove nomi vuoti e voci non utili | Riesaminare i filtri legacy prima di applicarli; non eliminare segnali validi per corrispondenze generiche. |
| Nodo 11 — Check Group ingresso digitale | Applica `GROUP: Ingresso_digitale` in una condizione specifica | Mantenere come regola downstream da verificare, dopo aver confrontato misure e bitinfo. |

## Vincoli di migrazione

- Conservare ordine e valori delle righe; non deduplicare per `NAME+UNITS` finché non è confermato che righe omonime siano duplicati.
- Distinguere il registro Modbus dall'indirizzo PLC `INDIRIZZO`/DBX. Per colonne REG sparse, il carry-over è solo dall'alto verso il basso e solo nei layout documentati.
- Non inventare righe placeholder, nomi, unità, IP, porte, registri o range.
- Conservare i registri con zeri iniziali come stringhe e i registri Modbus numerici come numeri, secondo lo schema legacy.
- Rispettare le regole `CMD`/`SET`/`MV`/`XTM`, i casi `CALCOLATA`, le misure Raw, i flag `Int`/`Range`/`Division` e l'identificazione dei gruppi packed digitali.
- Non propagare ciecamente per pagina il default stazione `SME`, `DRIVERCONFIG` incompleto o `ID`: la normalizzazione/consolidamento successivo deve preservare ciò che la pagina dichiara davvero.
- Per la prima prova tenere indipendenti i VLM 4 e 5, come nel legacy. Decidere se il VLM 5 debba anche ricevere il risultato del VLM 4 solo dopo aver verificato gli output e i collegamenti consentiti da MyHydra.

## Fonti legacy

La proposta deriva da `legacy/double_pdf/LV2/Station Measurement Technical data (Condition node)/`, Nodi 1–11. Il legacy resta intatto. Prima di convertire i prompt lunghi in versioni per pagina, controllare gli schemi completi di Nodo 3, Nodo 4 e Nodo 5.

## Prossimo step sul canvas

Dentro l'iniezione `DOUBLE PDF MEASUREMENT DATA`, sostituire il Naive sonda temporaneo con i nodi 1–5 e collegare tre Naive di output ai tre VLM. Lasciare iterativa la sottopiattaforma, non i singoli Pytool. Dopo aver ricevuto i tre output del caso 6, definire il Pytool di assemblaggio per pagina.
