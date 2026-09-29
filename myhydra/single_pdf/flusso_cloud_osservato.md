# Flusso cloud osservato — Single PDF

Questa pagina raccoglie la topologia vista sugli screenshot della piattaforma cloud del 28/09/2026. **Non è il flusso documentato in [`README.md`](README.md)** e non è implementato in questo repository. Serve a tenere traccia di una configurazione diversa, che va chiarita prima di decidere quale sia quella da usare.

La fonte primaria è [`../../docs/architettura/single_pdf_cloud_corrente.md`](../../docs/architettura/single_pdf_cloud_corrente.md).

## Limiti dell'osservazione

Gli screenshot mostrano nomi, descrizioni e connessioni dei nodi. **Non mostrano** configurazioni, prompt, payload, regole interne né risultati di esecuzione. Tutto ciò che segue è lettura delle etichette visibili, non prova di comportamento.

## Livello 1 osservato

```text
1. medex
   ├── #1 @MEDIA   → 2. medex
   └── #2 @NOMEDIA → 3. naive

2. medex → #3 → 4. SINGLE PDF ENGINE (iterativo)
                    │
                    └── #4 → 5. pytool
                              descrizione: "Pulizia JSON PRE-BISON"
                              │
                              └── #5 → 6. naive (nodo di uscita visibile)
```

## Livello 2 osservato

```text
1. medex — "Conversione CONTENT a PNG"
   ├── #1 @MEDIA   → 3. visiomaru — "PARSING JSON PRINCIPALE"
   └── #2 @NOMEDIA → 2. naive (nodo di uscita visibile)
```

## Differenze rispetto al flusso documentato

| Aspetto | Flusso documentato (ADR-001) | Flusso osservato |
|---|---|---|
| Nodi Livello 1 | 4 | 6 |
| Nodi Naive | nessuno | 3 (`#2` e `#3` di uscita, più il nodo finale `#6`) |
| Rami `@MEDIA` / `@NOMEDIA` | assenti | presenti su entrambi i Medex iniziali |
| Pytool | `json_creator.py` v4.2, genera l'output ADAS | descritto come "Pulizia JSON PRE-BISON" |
| Punto in cui nasce l'ADAS | nel pytool | **non visibile** |

Le due differenze che contano di più sono la descrizione del pytool e la presenza di BISON. Nel flusso documentato la generazione dell'output ADAS **è** il compito del pytool, e BISON è una fase successiva e ancora bloccata. Nel flusso osservato il pytool è etichettato come pulizia *pre*-BISON, il che suggerirebbe che l'ADAS venga generato altrove, in un nodo non visibile nello screenshot.

Non è possibile stabilire se siano due versioni dello stesso nodo o due nodi distinti.

## Cosa non si può dedurre

- Se il nodo iniziale converte il PDF o riceve contenuto già preparato: manca la configurazione Medex.
- Che cosa significhino `@MEDIA` e `@NOMEDIA` per tipi e valori dei payload.
- Come `SINGLE PDF ENGINE` itera, raccoglie le risposte, gestisce errori e retry.
- Modello e prompt di Visiomaru, schema del JSON principale e validazione.
- Le trasformazioni del pytool oltre l'etichetta "Pulizia JSON PRE-BISON".
- Se e dove avvengano generazione BISON, linearizzazione e consegna finale.
- Il collegamento runtime fra Livello 1 e Livello 2 oltre alle connessioni dell'editor.

## Perché questa pagina esiste

Il Double PDF ha una baseline documentata in un albero parallelo, e il Single PDF storico ha le sue esportazioni in `legacy/single_pdf/`. Il flusso cloud osservato non ha nessuna delle due cose: è un terzo riferimento, tratto da una sola osservazione. Senza una pagina che lo raccolga, si rischia di confonderlo con il flusso implementato.

## Cosa serve per chiuderla

Le configurazioni esportate dei nodi dei due livelli, i loro prompt e script, e almeno un input con gli output intermedi corrispondenti. Con questi tre elementi si può stabilire se il flusso osservato sia una versione più recente dello stesso, o un ramo diverso da mantenere separato.
