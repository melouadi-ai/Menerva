# Double PDF — workflow proposto

## Vincolo d’ingresso

L’utente carica IOL e JOB insieme in un’unica chat AI, come allegati della stessa richiesta. Non sceglie slot o rami IOL/JOB. Il VLM deve riconoscere il ruolo del PDF e il tipo di contenuto della singola pagina.

La piattaforma deve tuttavia mantenere per ogni immagine la provenienza tecnica (file d’origine e numero di pagina), se disponibile nel payload Medex/orchestratore. Questi metadati non devono essere chiesti al VLM né ricostruiti per supposizione. Se il runtime non li espone, va verificata una strategia di tracciamento prima dell’implementazione.

I riferimenti interni osservati nei campioni del tutor concordano per il gruppo 6 (`JOB.0139.23`) e il gruppo 7 (`JOB.0105.22`). Questi riferimenti danno al Pair Validator un controllo in più dopo la classificazione, ma non sostituiscono il riconoscimento pagina per pagina.

## Livello 1 attualmente configurato

Dallo screenshot del canvas condiviso il 29 settembre 2026, il Livello 1 è:

```text
1. medex — PDF2PNG
    ↓ #1
2. medex — MEDIA2CONTENT
    ↓ #2
3. DOUBLE PDF ENGINE
```

Questa è una buona base lineare per l’ingresso in chat e il passaggio del contenuto al motore Double PDF. La schermata non mostra le configurazioni interne di Medex e non conferma se il secondo nodo consegni al motore una pagina per iterazione mantenendo il PDF d’origine.

**Aggiornamento:** l’utente ha confermato che il nodo iterativo è stato attivato dopo lo screenshot. Lo screenshot quindi non documenta lo stato corrente dell’interruttore. Resta da verificare il comportamento osservando il payload e il numero di invocazioni.

### Evidenze Medex del test con i PDF del caso 6

I file caricati sono `Mappatura_6_Cliente_SMI_1.pdf` e `Mappatura_6_Descrizione_Cliente_SMI_1.pdf`. L’utente chiarisce che nel primo nodo `{"request":"pdf2png","nume":5}{question}` il parametro `nume:5` è un ingrandimento per facilitare la lettura, non un numero di pagine o di file. Lo screenshot mostra 14 anteprime, coerenti col totale noto del caso 6 (5 + 9 pagine).

L’output condiviso del secondo Medex è una sequenza di 14 oggetti `_medexkeys`: i primi 13 contengono due chiavi adiacenti, con la seconda chiave di ciascun oggetto che ricompare come prima chiave del successivo; l’ultimo contiene una chiave sola. La sequenza contiene 14 chiavi media uniche, organizzate come finestre sovrapposte (27 occorrenze complessive), non come 14 oggetti che portano ciascuno una singola chiave. Questo suggerisce un buffer/finestra di media; non assumere che un oggetto equivalga a una pagina indipendente senza verificare il contratto di `nume`/`nkeysgrp` e il nodo iterativo.

Il nodo MEDIA2CONTENT LV1 è configurato come `{"request":"media2content","nume":1, "nkeysgrp": 1 }{edge.media}[1]`. I nomi file e i numeri pagina non sono esposti nelle chiavi. I prefissi osservati cambiano tra esecuzioni in posizioni diverse e non sono un identificatore affidabile del PDF sorgente. Nel legacy una nota associa `nume:1` a un buffer trasferito al VLM e `nkeysgrp:1` alle pagine per gruppo; il comportamento effettivo osservato qui è una finestra sovrapposta di due chiavi per iterazione (con una chiave nell’ultima).

### Prova del nodo iterativo con forwarding naive

Nella prova successiva il Double PDF Engine è iterativo e contiene soltanto un nodo `naive` che inoltra l’ingresso. L’output conferma 14 iterazioni/elementi. Ogni elemento contiene `_medexkeys` serializzato come stringa JSON; i primi 13 hanno due chiavi consecutive, con sovrapposizione di una chiave tra elementi adiacenti, e l’ultimo ne ha una. Quindi il forwarding conserva le finestre prodotte da Medex, non trasforma ciascun elemento in una singola pagina. In un VLM futuro, se ogni finestra è analizzata, le pagine interne alle finestre saranno viste in iterazioni adiacenti; il risultato va raccolto/deduplicato per chiave pagina, non semplicemente concatenato alla cieca.

In una cattura precedente si vedevano due prefissi con cardinalità 9+5; nella diagnostica più recente, sugli stessi 14 giri, i prefissi avevano cardinalità 12+2. Poiché la partizione non è stabile, i prefissi non vanno interpretati come confini dei PDF. La diagnostica conferma invece che `{question}` nel Pytool contiene il JSON esterno con `_medexkeys` (stringa JSON annidata) e che edge #2 contiene il JSON `pages` valido del VLM, in tutti i 14 giri.

**Valutazione:** il forwarding naïve non consegnava chiavi al Pytool (edge #4 vuoto). La sorgente corretta è `{question}`, l’input originale del ciclo LV1; il Medex LV2 converte quelle chiavi in immagini per il VLM. Il Pytool associatore ora legge `{question}` e edge #2. Il passo successivo è provare lo script aggiornato sul runtime; attesi 13 output a due record e uno a record singolo, tutti con `status: OK`.

### Esito del classificatore sul caso 6

Il VLM ha restituito 14 oggetti, uno per iterazione: 13 con due etichette locali (`index` 0 e 1) e l’ultimo con una (`index` 0). Le 27 etichette si ricompongono in 14 pagine uniche con questa sequenza:

| Pagina nella sequenza Medex (1-based) | Classe |
|---:|---|
| 1 | `DENSITY_MAP` |
| 2–5 | `MEASUREMENT_TECHNICAL_DATA` |
| 6–7 | `STATION_INFORMATION` |
| 8 | `MEASUREMENT_TECHNICAL_DATA` |
| 9–10 | `STATION_INFORMATION` |
| 11–14 | `MEASUREMENT_TECHNICAL_DATA` |

Tutte le 13 pagine che ricompaiono in due finestre hanno la stessa classe in entrambe le occorrenze. L’esito supporta la classificazione a finestre come prototipo. Gli indici `0` e `1` sono locali alla finestra, quindi per il passo successivo servono l’associazione con le chiavi della finestra e la deduplicazione per chiave, non un conteggio diretto delle 27 etichette come pagine.

## Cosa documenta davvero il Double PDF legacy

Il legacy non è un flusso che semplicemente divide i due PDF in ruoli IOL/JOB e poi li riconcilia. Nel Livello 2 il nodo `VLM Split Files` classifica ogni pagina in tre categorie: `STATION_INFORMATION`, `MEASUREMENT_TECHNICAL_DATA` e `DENSITY_MAP`; i rami condizionali elaborano le categorie separatamente. Il ramo station information estrae protocollo, IP/porta e `campi_scala`; il ramo measurement estrae stazioni/misure e, in parallelo, bitinfo/stati ON-OFF; il ramo density map è un forwarding. Un merge iterativo ricompone i risultati dei rami per pagina.

Nel Livello 1 legacy seguono controlli/aggregazioni delle informazioni di stazione, merge delle pagine, normalizzazione (incluse misure digitali impaccate) e il `Json Creator & BISON`, che produce l’output ADAS e applica la logica di scala quando trova corrispondenze. I file mostrano anche nodi successivi per pulizia/controllo BitInfo. Questo è il comportamento legacy visibile nei file, non una specifica cliente completa né una garanzia che ogni script fosse corretto o effettivamente collegato nella piattaforma.

**Distinzione delle evidenze:** la richiesta del tutor in `Prompt_Iniziale_tutor.txt` descrive in dettaglio l’estrazione Single PDF e il formato ADAS; non specifica una regola di matching generale tra IOL e JOB. Il classificatore legacy documenta le tre classi di pagina sopra, non le etichette IOL/JOB. La proposta di classificare esplicitamente il ruolo IOL/JOB, usare un Pair Validator/Reconciler e bloccare i conflitti è una possibile evoluzione progettuale, ma non va presentata come requisito già confermato dal legacy o dal cliente. Anche l’associazione per TAG richiede conferma su esempi e requisiti.

## Preflight per gruppi e pagine

Prima di aggiungere prompt o riconciliazione, verificare il percorso Medex con output reali. Il requisito logico è **un gruppo sorgente per PDF caricato e un elemento iterabile per pagina**, mantenendo l’associazione gruppo/file/pagina. I due file possono essere allegati alla stessa chat, ma il preflight non deve fonderne i confini.

### Verifica iniziale senza altri nodi

Eseguire prima una prova osservativa dei nodi 1 e 2 e ispezionare i loro output grezzi. Controllare che:

1. siano riconoscibili entrambi i PDF caricati come due sorgenti distinte;
2. ogni sorgente abbia il numero di pagine atteso, senza pagine vuote inattese;
3. ogni pagina abbia una chiave/media distinta e l’indice pagina;
4. sia possibile risalire dal media al PDF sorgente;
5. la lista che entra nell’iterativo contenga una unità per pagina, non una sola unità per PDF né un’unica immagine appiattita.

Nei campioni del tutor il gruppo 6 ha 5 pagine IOL + 9 JOB (**14 iterazioni attese**); il gruppo 7 ha 4 + 7 (**11 iterazioni attese**). Usare questi conteggi per la prova, non come costanti del workflow generale.

### Nodo di controllo da aggiungere se i metadati sono accessibili

Se l’output di `MEDIA2CONTENT` espone una struttura leggibile dal Pytool, inserire `Pytool Media Preflight` tra nodo 2 e nodo iterativo. Deve produrre un manifest di controllo e uno stato `READY` / `INPUT_ERROR`:

- `READY`: due PDF sorgente attesi; gruppi non vuoti; indici pagina univoci e consecutivi per sorgente; una unità iterabile per pagina; riferimenti sorgente preservati.
- `INPUT_ERROR`: allegato mancante/illeggibile, gruppo vuoto, indice duplicato o mancante, associazione file-pagina persa.

In caso di `INPUT_ERROR`, fermare l’iterativo e restituire la diagnosi. Se Pytool non può leggere i metadati Medex, non forzare un controllo fittizio: verificare se la condizione o l’iterativo possono farlo, altrimenti usare temporaneamente gli output grezzi e i conteggi per validare il comportamento.

Dopo il nodo iterativo, un controllo del collector dovrà verificare che il numero degli output pagina coincida con quello delle unità inviate, senza duplicati o pagine saltate. Solo dopo questo controllo conviene passare alla verifica semantica VLM (presenza di pagine IOL/JOB e riferimenti interni compatibili).

## Livello 1 — Orchestrazione della chat e della coppia

```text
Un messaggio chat con allegati IOL + JOB
    ↓
Medex: PDF allegati → immagini/pagine
    ↓
Iterativo: invia ogni pagina al Livello 2, conservando file origine + pagina
    ↓
Raccoglie output intermedi di tutte le pagine
    ↓
Pytool Pair Validator: controlla ruoli, riferimenti e copertura
    ↓
Condition: pairing_status
    ├── READY → Pytool Reconciler
    │              ↓
    │          Pytool ADAS Creator
    │              ↓
    │          Output JSON ADAS + rapporto di provenienza
    └── REVIEW_REQUIRED → Output di revisione con pagine/conflitti
```

### Nodi da inserire, in sequenza logica

| Ordine | Nodo | Compito |
|---|---|---|
| Ingresso | Input chat con entrambi gli allegati | È un solo avvio di workflow. La classificazione IOL/JOB avviene dopo, per pagina. |
| 1 | `Medex pdf2png` | Converte i PDF allegati in pagine/immagini. Deve mantenere associazione tra ogni pagina e il PDF da cui proviene. |
| 2 | Nodo iterativo | Invoca il Livello 2 una volta per pagina; non divide a monte gli allegati in canali IOL e JOB. |
| 3 | Merge/collector dei risultati iterativi | Ricompone tutti i JSON pagina mantenendo `source_file_id`, `page_number` e ordine d’origine. |
| 4 | `Pytool Pair Validator` | Verifica che il VLM abbia identificato i ruoli attesi, che ci siano contenuti utili da entrambi i documenti e che gli identificativi interni siano compatibili. Produce `READY` o `REVIEW_REQUIRED`; non corregge i conflitti. |
| 5 | `Condition` sullo stato | Consente la riconciliazione solo per coppie sufficientemente coerenti; manda i casi incerti al ramo di revisione. |
| 6 | `Pytool Reconciler` | Collega dati JOB e segnali IOL con chiavi documentate e conserva pagina e regola di match. Lascia irrisolti i match ambigui. |
| 7 | `Pytool ADAS Creator` | Converte il modello riconciliato nel formato ADAS, riusando le trasformazioni Single PDF soltanto dove la semantica coincide. |
| 8 | Output/`Naive` finale | Restituisce JSON ADAS e rapporto di provenienza oppure il rapporto di revisione. |

## Livello 2 — Comprensione ed estrazione di una pagina

```text
Medex content2media
    ↓
Visiomaru/VLM “Double PDF Page Analyzer”
    ├── riconosce il ruolo: IOL / JOB / UNKNOWN
    ├── riconosce il tipo pagina
    └── estrae i campi previsti per quel ruolo/tipo
    ↓
Pytool: parse, validazione e aggiunta metadati tecnici di fonte
    ↓
JSON intermedio della pagina
```

Nel primo prototipo userei **un’unica chiamata VLM per pagina** che classifica e poi estrae secondo il tipo riconosciuto. Evita un passaggio di classificazione separato e permette al VLM di leggere il contesto visivo della pagina. Se classifica `UNKNOWN` o non riesce a leggere la pagina, il record passa alla revisione invece di essere forzato in uno schema IOL o JOB.

Tipi pagina minimi da riconoscere:

- `IOL_REGISTER_MAP` / `IOL_SIGNAL_TABLE`: registri, bit, tag, descrizioni e dati tecnici dei segnali;
- `JOB_STATION_NETWORK`: protocollo, PLC, IP e porta;
- `JOB_SCALE_LIMITS`: campi scala, limiti orari/giornalieri e relativi segnali/tag;
- `JOB_OTHER`: testo di contesto non mappato nel risultato ADAS;
- `INDEX_OR_DENSITY_MAP`: indice o mappa grafica, da conservare/classificare ma senza inventare misure;
- `UNKNOWN`: pagina illeggibile, estranea o non classificabile con sufficiente evidenza.

Questi nomi sono etichette proposte: prima di fissarli bisogna controllare tutte le pagine campione, perché una stessa pagina può contenere più sezioni utili.

### Busta intermedia per pagina

Ogni risposta dovrebbe essere un oggetto con almeno:

```json
{
  "source_file_id": "fornito dal runtime, se disponibile",
  "source_filename": "nome file fornito dal runtime, se disponibile",
  "page_number": 1,
  "document_role": "IOL | JOB | UNKNOWN",
  "page_type": "IOL_SIGNAL_TABLE | JOB_SCALE_LIMITS | ...",
  "document_ref": "IOL/JOB identificato nella pagina, oppure null",
  "extracted_data": {},
  "warnings": []
}
```

Il VLM classifica ruolo e tipo pagina e trascrive evidenze; `source_file_id` e `page_number` devono provenire dall’orchestrazione se disponibili. Il VLM può estrarre la dicitura IOL/JOB stampata nel documento come `document_ref`, ma questa non va confusa con i metadati tecnici del file.

## Riconciliazione e condizioni di uscita

1. Verificare che siano stati identificati contenuti IOL e JOB nella stessa richiesta chat.
2. Confrontare riferimenti interni, nome file e contesto. Nei campioni 6 e 7 gli ID JOB sono coerenti; in altri campioni possono esserci conflitti.
3. Un identificativo mancante, un riferimento discordante o più candidati per la stessa coppia portano a `REVIEW_REQUIRED`.
4. Associare i dati JOB alle righe IOL solo tramite chiavi approvate. TAG esatti o riferimenti espliciti possono essere candidati; la somiglianza testuale da sola non deve fondere automaticamente.
5. Conservare per ogni valore finale file, pagina, dato sorgente e regola di collegamento.
6. Generare ADAS solo per i campi risolti e convalidati; non inventare IP, stato ON/OFF, unità, scale o limiti mancanti.

## Primo ordine di implementazione

1. Verificare che il runtime esponga identità dei PDF e numeri pagina quando più allegati entrano nella stessa chat; se non li espone, progettare un tracciamento alternativo.
2. Definire l’envelope JSON di pagina e il prompt del `Double PDF Page Analyzer`.
3. Provare classificazione ed estrazione su tutte le pagine delle coppie 6 e 7, controllando ruolo, tipo pagina e riferimenti interni.
4. Implementare il collector e il Pair Validator; provare un caso coerente e il campione separato con riferimento discordante.
5. Definire sul documento la chiave di match tra campi scala JOB e segnali IOL; contare match esatti, mancanti e ambigui.
6. Implementare il Reconciler e il rapporto di provenienza prima di collegare la conversione finale ADAS.

Non aggiungere rami BISON/linearizzazione finché le specifiche non sono confermate; conservare comunque scale e limiti nell’intermedio.
