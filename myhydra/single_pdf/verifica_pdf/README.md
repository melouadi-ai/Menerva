# Verifica output ↔ PDF

Confronta i JSON prodotti dal pytool con il PDF da cui dovrebbero derivare. Il PDF è la fonte di verità: gli output non lo contengono, lo riassumono, e un output può essere ben formato e sbagliato allo stesso tempo.

## Perché serve

Il JSON di output passa la validazione dello schema e sembra a posto: `DRIVERPRIVATE` ha la lunghezza giusta, i campi obbligatori ci sono, l'XML è ben formato. Nessuno di questi controlli dice se i numeri corrispondono a quelli del documento. Il confronto col PDF è l'unico controllo che lo dice.

## Uso

```sh
cd myhydra/single_pdf/verifica_pdf
../../../.venv/bin/python confronta.py                # tutti i casi
../../../.venv/bin/python confronta.py caso_2_protec_1  # un caso
../../../.venv/bin/python confronta.py --lista
```

Richiede `pymupdf`, presente nel `.venv` del repository. Lo script non scrive fuori da `per_caso/`.

## Cosa produce

Per ogni caso, tre file in `per_caso/<caso>/`:

| File | Contenuto |
|---|---|
| `tabella_pdf.json` | Le righe estratte dal PDF, con pagina, registro, bit e metadati. La base di confronto. |
| `verdetto.json` | Esito per ogni riga, più i controlli trasversali. Serve per le verifiche automatiche successive. |
| `report.md` | Lo stesso in forma leggibile, con le tabelle. |

## I quattro casi

| Caso | Cliente | Pagine | Estrattore | Esito |
|---|---|---|---|---|
| `caso_1_sma_1` | SMA | 1 | `sma` | 50 righe, 45 presenti, 0 assenti. Registro 0 su 5 righe derivate. |
| `caso_2_protec_1` | PROTEC | 2 | `protec` | 89 righe, 45 presenti, 44 saltate da regola, 0 assenti. |
| `caso_3_protec_2` | PROTEC | 2 | `protec` | 79 righe, 39 presenti, 40 saltate da regola, 0 assenti. |
| `caso_4_siemens_2` | SIEMENS | 29 | `siemens` | 1116 righe, 236 presenti, 726 assenti. Perdita a monte, vedi sotto. |

I PDF stanno in `../PDFs per il confronto/`, gli output in `../Outputs MYHYDRA/`. Gli output sono byte-identici a quelli in `tests/single_pdf_outputs/`: è lo stesso run, copiato per comodità.

## Le classi di scostamento

Il punto che conta di più: **non tutti gli scostamenti sono difetti**. Ogni riga riceve una classe.

| Classe | Significato |
|---|---|
| `ok` | Corrispondenza corretta. |
| `saltata_da_regola_di_prompt` | La riga manca perché una regola del prompt prescrive di scartarla. Comportamento richiesto, non un difetto. |
| `scelta_di_progetto` | La pipeline ha fatto qualcosa di deliberato e diverso dal documento. |
| `correzione_di_refuso_del_documento` | Il testo nel PDF è sbagliato e l'output lo ha corretto. |
| `difetto` | Serve una decisione. |

La distinzione è automatica: due nomi che differiscono per poco più di refusi si classificano come correzione, il resto come difetto.

## Un confronto che non può dare un verdetto

Un caso limite merita una nota, perché è quello da cui si rischierebbe di trarre la conclusione sbagliata.

**La regola V2 chiede il confronto esatto.** I nomi da scartare sono elencati come valori interi: `disponibile`, `riserva`, `non utilizzato`. I documenti però contengono varianti prefissate: `Riserva INPUT`, `Misura Disponibile IW36`. `Riserva INPUT` non coincide con `riserva`, quindi la regola, applicata alla lettera, non lo scarta. L'output però lo scarta.

Il report conta queste righe in una sezione a parte, `Righe mancanti con nome generico prefissato`, invece di registrarle come difetti. Non è una via di mezzo comoda: è il punto in cui la specifica non dice quale comportamento sia atteso, e la scelta spetta al cliente. Se la regola deve restare esatta, l'output ne scarta troppe; se deve coprire i prefissi, il prompt va corretto.

Lo stesso vale, in scala minore, per le righe che il pytool ha trasformate: `OVF Misura Disponibile IW36` non è andata persa, è finita dentro l'analogica `Misura Disponibile IW36` per effetto della guardia B. Il report le classifica `scelta_di_progetto` invece di contarle come mancanti.

## Il caso SIEMENS: la perdita è a monte, non nel pytool

Su SIEMENS_2 il confronto mostra 1116 righe nel documento e 236 presenti nell'output. La domanda ovvia è se il pytool abbia perso qualcosa. **No, e si può dimostrarlo dai metadati dell'output** senza ricostruire nulla.

Il campo `_meta.variables_total` del file di output vale **274**. Il pytool ha ricevuto 274 variabili e ne ha prodotte 251 misure e bitinfo: la differenza di 23 sta nel dedup e nelle righe doppie che il pytool collassa per progetto. Sulle 1116 righe del PDF il pytool non può aver perso niente, perché non le ha mai viste.

La perdita è quindi nell'estrazione VLM. Il dato che lo suggerisce è `chunks_parsed: 1`: **un solo chunk** per un documento di 29 pagine significa che le pagine sono state accorpate in un'unica richiesta invece che inviate una per iterazione. È il rischio n. 1 di ADR-001, concretizzato.

Resta un limite onesto: l'attribuzione al VLM è **dedotta** dai metadati, non osservata in locale. Non ho riprodotto l'invio delle 29 pagine, quindi non posso escludere che l'accorpamento sia avvenuto a valle del VLM, per esempio nel nodo iterativo che aggrega i risultati prima di passarli al pytool. Il report dichiara il caso come parzialmente validato per questa ragione.

L'estrattore SIEMENS, per parte sua, regge: 28 pagine su 29, registri e nomi coerenti. La pagina è ruotata di 90 gradi, `find_tables()` non la legge, e i registri a doppia occupazione (`40051/40052`, regola V22) cominciano dalla pagina 18.

## Limiti noti

- **Le fixture contengono dati di produzione**, presi alla lettera: IP reali e nomi di clienti. Prima di pubblicare il repository vanno sanitizzati.
- **L'abbinamento è per registro e bit**, non per nome. Quando due misure condividono un registro, l'abbinamento può assegnare la riga sbagliata; in quel caso l'esito è `nome_diverso` e la tabella lo mostra.
- **Il confronto non conosce l'input effettivo del run.** Se un output è stato prodotto da un PDF diverso o parziale, la copertura risulterà bassa senza che sia un difetto. Il report mostra la copertura per pagina proprio per rendere questo distinguibile.
- **Gli output non sono stati rigenerati.** Sono i file presenti in `Outputs MYHYDRA/`, prodotti dal pytool in un momento che non è stato registrato. Rifare il confronto dopo una modifica al prompt o al pytool richiede prima di rigenerarli.
- **Lo script contiene estrazioni specifiche per cliente.** I tre formati sono separati perché i documenti hanno strutture diverse; non c'è un parser unificato.

## Cosa non fa

Non modifica prompt, pytool né contratti, anche quando trova difetti. Produce le prove, la decisione è altrove. Non giudica il ground truth legacy: quello è confrontato a parte, in `../test/caso_2_protec_1/outputs/`.
