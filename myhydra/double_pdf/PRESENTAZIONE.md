# Double PDF IOL+JOB — Presentazione del progetto

> Documento divulgativo e di onboarding. Dettagli tecnici nelle schede
> `nodes/` e in `WORKFLOW_DESIGN.md`; numeri aggiornati al 5/10/2026 (caso 6).

## 1. Il problema

Un impianto di monitoraggio emissioni si configura con **due documenti**:
una **mappatura IOL** (tabelle registri PLC/SCADA) e una **descrizione JOB
(hour)** (specifica: IP, scale, limiti, logiche). I due PDF vengono caricati
insieme in chat, **in ordine casuale e senza metadati di origine**: la
piattaforma non sa quale pagina appartiene a quale documento. Il progetto
Double PDF li trasforma in **un JSON ADAS pronto all'import**, con ogni
scelta tracciabile.

## 2. L'idea in una frase

Un VLM **legge** (classifica pagine, trascrive tabelle); Python **calcola**
(filtra, unisce, verifica) e **non inventa mai**: ogni dubbio finisce in una
coda di revisione invece di diventare un dato silenzioso.

## 3. Architettura: un livello smista, tre livelli estraggono

```text
LV1 (smistamento, 1 sola esecuzione)
  Medex PDF→PNG → Medex finestre → CLASSIFIER (iterativo, 1 giro/pagina)
  → DEDUPLICA → PREPARA → 3 FILTRI (Station / Measurement / Density)
       |                    |                    |
LV2-STATION            LV2-MEASUREMENT        (forwarding)
 (6 pagine)            (7 pagine)
       |                    |
       └────── CONSOLIDATORE (unisce tutto in 1 stazione + variabili)
                    |
              JSON CREATOR (22 misure + 60 bitinfo ADAS) → OUTPUT
```

## 4. LV1 nodo per nodo (nomi canvas)

| Nodo | Tipo | Cosa fa |
|---|---|---|
| `CONVERTI PDF IN PNG` (1, Medex) | conversione | I PDF diventano immagini (`nume=5` per leggibilità) |
| `CREA FINESTRE DI PAGINE` (2, Medex) | finestre | 14 finestre sovrapposte (caso 6): ogni pagina compare 2 volte per non perderne i bordi |
| `DOUBLE PDF PAGE CLASSIFIER` (3, iniezione) | VLM iterativo | Per ogni finestra assegna **ruolo** (`IOL`/`JOB`/`UNKNOWN` da evidenze visive) + **etichetta** (`STATION_INFORMATION` / `MEASUREMENT_TECHNICAL_DATA` / `DENSITY_MAP`) |
| `DEDUPLICA PAGINE SOVRAPPOSTE` (4, Pytool) | dedup | Collassa la stessa chiave media (14 uniche su 27); i disaccordi si risolvono con priorità legacy e restano negli avvisi |
| `PREPARA PAGINE PER I FILTRI` (5, Pytool) | array root | Un array di record pagina con `review_required`/`review_warnings` propagati |
| `FILTER STATION INFORMATION` (6) / `FILTER MEASUREMENT TECHNICAL DATA` (7) / `FILTER DENSITY MAP` (8, Pytool) | filtri | Partizionano le 14 pagine (6 / 7 / 1) conservando il record intero |
| `DOUBLE PDF STATION INFORMATION` (10, iniezione) | LV2 | Estrae IP/porta/scale dalle 6 pagine Station |
| `DOUBLE PDF MEASUREMENT DATA` (9, iniezione) | LV2 | Estrae le misure dalle 7 pagine Measurement (3 rami paralleli) |
| `INOLTRA DENSITY MAP` (9→Naive) | forwarding | La pagina densità passa invariata |
| `PREPARAZIONE X JSON` (11, Pytool) | consolidatore | Unisce i 3 rami in **1 stazione + 69 variabili** (tipi, scale SO2, review ereditate) |
| `JSON CREATOR` (12, Pytool) | trasformatore | Chunk → ADAS: `DRIVERPRIVATE` hex, `DRIVERCONFIG` XML, rinumerazione ID |
| `OUTPUT` (13, Naive) | uscita | Il JSON finale |

## 5. Le tre sotto-piattaforme LV2

**Classifier** — Medex `content2media` + VLM con prompt dedicato. Regola chiave:
il routing usa la `label`, il `document_role` resta metadato; mai dedurre il
PDF dal prefisso chiave (instabile tra run).

**Station** — `ESTRAI CHIAVE PAGINA` → Medex immagine → VLM (prompt v4, niente
default `SME` inventato, `[]` se vuota) → associatore pagina+estrazione.
Dà IP `10.100.50.95:511` e le scale (SO2 0…300, TF 0…100).

**Measurement** — Medex immagine → **3 VLM paralleli** (misure+BISON,
bitinfo+nomi, stati TEXTON/TEXTOFF) → **3 tagger** (etichettano ramo+pagina,
gestiscono le fence Markdown) → **assemblatore per pagina** (join su nome,
BIT dal ramo misure, scarti vuoti/numerici, review mai silenziosa) → Naive.

## 6. Le regole d'oro (perché fidarsi)

1. **Join su nome, mai su ID**: il `MEASUREID` ha tre semantiche diverse (gruppi, chunk, registri veri) — usarlo come chiave corrompe il join.
2. **BIT dal ramo misure** (verificato 6/6 da coordinate PDF); il BITNO bitinfo non lo sovrascrive mai; i disaccordi vanno in `review` (es. PM-302A/B).
3. **Righe bianche = righe saltate**: riserve 420–424, filler numerici, TAG vuoti non generano mai misure fantasma (il legacy inventava `Comando riservato`).
4. **TEXTON/TEXTOFF derivati, non letti**: nel PDF non esiste colonna di stato — convenzione valida, ma dato sintetico.
5. **Leggero = plumbing, 3.8 = qualità**: i confronti valgono solo a parità di modello e classificazione.

## 7. Stato e numeri (caso 6, `JOB.0139.23`)

Classificazione 14 pagine → 6 Station + 7 Measurement + 1 Density; 65 misure
leggero / 69 misure 3.8; assemblatore 7 pagine `OK`; consolidatore `OK`
(stazione `Sistema Analisi SO2`, 69 variabili, scale SO2); ADAS locale
22 misure + 60 bitinfo, Pydantic valido. Aperti: scala `TF`, limiti JOB,
TEXTON parziali su REG 3, BISON/cliente.

## 8. Glossario minimo

- **Edge `#N`** = filo tra nodi, numero locale al canvas (ricontrollare dopo ogni ricablaggio; può portare condizioni spurie che bloccano il filo in silenzio).
- **`{question}`** = record pagina dell'iterazione corrente; **`{edge}[N]`** = output testuale di un altro nodo; **`{edge.media}[N]`** = immagine.
- **Envelope** = output tagger (`branch` + `page` + `vlm_output`): ogni dato porta la sua provenienza.
- **`observed_*`** = output runtime sanitizzato; **`expected_*`** = derivato. Con `review_required: true` non è ground truth.
