# caso 4 siemens 2 — SIEMENS

Confronto fra `Mappatura_4_Cliente_SIEMENS_2.pdf` e `OUTPUT SIEMENS 2.txt`.

## Esito

> **Estrazione parziale.** Confronto **parzialmente validato**. L'estrazione copre 28 pagine su 29 e i registri e i nomi che produce sono coerenti. La perdita di copertura e' stata pero' localizzata a monte: i metadati dell'output indicano che il pytool ha ricevuto 274 variabili in un solo chunk, mentre il documento ne contiene 1116 righe. Il pytool non puo' aver perso righe che non ha ricevuto, quindi la perdita e' nell'estrazione VLM. Resta non verificato in locale il modo in cui le 29 pagine sono state inviate, quindi l'attribuzione al VLM e' dedotta, non osservata.

| | |
|---|---|
| Righe estratte dal PDF | 1116 |
| Righe del PDF presenti nell'output | 236 |
| Righe del PDF assenti per una regola del prompt | 751 |
| Righe del PDF assenti senza spiegazione | 129 |
| Righe del PDF senza indirizzo Modbus (grandezze derivate) | 0, di cui 0 trasformate in misure |
| Righe dell'output assenti dal PDF | 0 |

Le cinque categorie sommano a 1116 contro 1116 righe estratte.

### Natura degli scostamenti

| Classe | Righe |
|---|---|
| saltata da regola (comportamento richiesto) | 751 |
| corrispondenza corretta | 157 |
| difetto | 157 |
| correzione di refuso del documento | 51 |

Le scostamenti non sono tutti difetti. `correzione di refuso del documento` significa che il testo nel PDF e' sbagliato e l'output lo ha corretto; `scelta di progetto` significa che la pipeline ha fatto qualcosa di deliberato e diverso. Solo la classe `difetto` richiede una decisione.

## Registri e indirizzi

- Registri distinti nel PDF: **591**, nell'output: **104**
- **Solo nel PDF, nessuna misura corrispondente:** 40030, 40033, 40034, 40035, 40036, 40043, 40044, 40045, 40046
- IP trovati nel documento: `192.168.2.11`, `255.255.255.0`, `192.168.2.15`, `192.168.2.101`, `192.168.2.10`
- IP usati dall'output: `192.168.2.11`
- **IP dichiarati e mai usati:** `255.255.255.0`, `192.168.2.15`, `192.168.2.101`, `192.168.2.10`
- Nomi stazione prodotti dall'output: `SME`

### Dove si e' perduta la copertura

Il file di output registra nei suoi metadati quante variabili ha ricevuto: **274**, in un solo chunk.
Il PDF contiene 638 righe utilizzabili. Il pytool ne ha viste meno.

**La perdita e' avvenuta a monte del pytool, nell'estrazione VLM**, non nel pytool. Il pytool ha lavorato tutto quello che gli e' stato passato: non puo' produrre misure per righe che non ha mai ricevuto.

Su questo caso la spiegazione plausibile e' la modalita' di invio: **un solo chunk** per un documento di 29 pagine suggerisce che le pagine siano state accorpate in un'unica richiesta invece che una per iterazione. E' la stessa ipotesi del rischio n. 1 di ADR-001, e qui si vede concretamente.

### Copertura per pagina

Le pagine 12, 13, 14, 15, 16, 17, 20, 24, 26, 27, 28, 29 non hanno **nessuna** riga coperta dall'output.

Il documento è completo e l'input del run era l'intero PDF, quindi queste pagine sono state lette ma non riportate nell'estrazione. La perdita è a monte del pytool, come indicato sopra.

| Pagina | Righe | Coperte | Saltate da regola |
|---|---|---|---|
| 2 | 32 | 14 | 18 |
| 3 | 49 | 6 | 43 |
| 4 | 36 | 16 | 17 |
| 5 | 32 | 17 | 13 |
| 6 | 32 | 16 | 14 |
| 7 | 49 | 1 | 47 |
| 8 | 32 | 20 | 11 |
| 9 | 32 | 24 | 7 |
| 10 | 32 | 10 | 20 |
| 11 | 49 | 14 | 34 |
| 12 | 32 | 0 | 32 |
| 13 | 32 | 0 | 0 |
| 14 | 36 | 0 | 4 |
| 15 | 32 | 0 | 32 |
| 16 | 32 | 0 | 0 |
| 17 | 36 | 0 | 4 |
| 18 | 40 | 16 | 24 |
| 19 | 25 | 4 | 21 |
| 20 | 35 | 0 | 35 |
| 21 | 50 | 12 | 36 |
| 22 | 55 | 14 | 41 |
| 23 | 45 | 12 | 25 |
| 24 | 40 | 0 | 40 |
| 25 | 55 | 12 | 37 |
| 26 | 55 | 0 | 55 |
| 27 | 55 | 0 | 55 |
| 28 | 55 | 0 | 55 |
| 29 | 31 | 0 | 31 |

## Righe mancanti con nome generico prefissato

**129 righe** assenti dall'output hanno un nome che comincia per uno dei nomi generici che la regola V2 impone di saltare, senza però coincidere con essi. Il prompt chiede il confronto esatto, quindi per queste righe la regola non si applica e la pipeline non dovrebbe scartarle: l'output però le ha scartate.

| Prefisso | Righe mancanti | Nomi esempi |
|---|---|---|
| `riserva` | 129 | Riserva INPUT, Riserva OUTPUT DIRETTI, Riserva STATI LOGICI |

Non è possibile attribuire queste mancanze a un difetto senza decidere quale comportamento sia atteso. Se la regola deve essere esatta come è scritta, l'output ne scarta troppe; se deve coprire i prefissi, il prompt va corretto. È una domanda per il cliente.

## Scostamenti

| Registro | Bit | Esito | PDF | Output |
|---|---|---|---|---|
| 40001 | 12 | `saltata_da_regola_di_prompt` |  | — |
| 40001 | 13 | `nome_diverso` | COG2: COMANDO Autocal ULTRAMAT 23 | COG2: COMANDO AUTOCAL ULTRAMAT 23 NO+CO+ |
| 40001 | 14 | `nome_diverso` | COG3: COMANDO Autocal ULTRAMAT 23 | COG3: COMANDO AUTOCAL ULTRAMAT 23 NO+CO+ |
| 40001 | 15 | `saltata_da_regola_di_prompt` |  | — |
| 40001 | 0 | `nome_diverso` | COG2: COMANDO START VERIFICA QAL 3 | COG2: COMANDO START VERIFICA QAL 3 CO+NO |
| 40001 | 1 | `nome_diverso` | COG2: COMANDO STOP VERIFICA QAL 3 | COG2: COMANDO STOP VERIFICA QAL 3 CO+NO+ |
| 40001 | 2 | `nome_diverso` | COG2: COMANDO SET BYPASS CONVERTITORE | COG2: COMANDO SET BYPASS CONVERTITORE NO |
| 40001 | 3 | `nome_diverso` | COG2: COMANDO RESET BYPASS CONVERTITORE | COG2: COMANDO RESET BYPASS CONVERTITORE  |
| 40001 | 4 | `nome_diverso` | COG3: COMANDO START VERIFICA QAL 3 | COG3: COMANDO START VERIFICA QAL 3 CO+NO |
| 40001 | 5 | `nome_diverso` | COG3: COMANDO STOP VERIFICA QAL 3 | COG3: COMANDO STOP VERIFICA QAL 3 CO+NO+ |
| 40001 | 6 | `nome_diverso` | COG3: COMANDO SET BYPASS CONVERTITORE | COG3: COMANDO SET BYPASS CONVERTITORE NO |
| 40001 | 7 | `nome_diverso` | COG3: COMANDO RESET BYPASS CONVERTITORE | COG3: COMANDO RESET BYPASS CONVERTITORE  |
| 40002 | 8 | `saltata_da_regola_di_prompt` |  | — |
| 40002 | 9 | `saltata_da_regola_di_prompt` |  | — |
| 40002 | 10 | `saltata_da_regola_di_prompt` |  | — |
| 40002 | 11 | `saltata_da_regola_di_prompt` |  | — |
| 40002 | 12 | `saltata_da_regola_di_prompt` |  | — |
| 40002 | 13 | `saltata_da_regola_di_prompt` |  | — |
| 40002 | 14 | `saltata_da_regola_di_prompt` |  | — |
| 40002 | 15 | `saltata_da_regola_di_prompt` |  | — |
| 40002 | 0 | `saltata_da_regola_di_prompt` |  | — |
| 40002 | 1 | `saltata_da_regola_di_prompt` |  | — |
| 40002 | 2 | `saltata_da_regola_di_prompt` |  | — |
| 40002 | 3 | `saltata_da_regola_di_prompt` |  | — |
| 40002 | 4 | `saltata_da_regola_di_prompt` |  | — |
| 40002 | 5 | `saltata_da_regola_di_prompt` |  | — |
| 40002 | 6 | `saltata_da_regola_di_prompt` |  | — |
| 40002 | 7 | `saltata_da_regola_di_prompt` |  | — |
| 40003 | 11 | `saltata_da_regola_di_prompt` |  | — |
| 40003 | 12 | `saltata_da_regola_di_prompt` |  | — |
| 40003 | 13 | `saltata_da_regola_di_prompt` |  | — |
| 40003 | 14 | `saltata_da_regola_di_prompt` |  | — |
| 40003 | 15 | `saltata_da_regola_di_prompt` |  | — |
| 40003 | 3 | `saltata_da_regola_di_prompt` |  | — |
| 40003 | 4 | `saltata_da_regola_di_prompt` |  | — |
| 40003 | 5 | `saltata_da_regola_di_prompt` |  | — |
| 40003 | 6 | `saltata_da_regola_di_prompt` |  | — |
| 40003 | 7 | `saltata_da_regola_di_prompt` |  | — |
| 40004 | 8 | `saltata_da_regola_di_prompt` |  | — |
| 40004 | 9 | `saltata_da_regola_di_prompt` |  | — |
| 40004 | 10 | `saltata_da_regola_di_prompt` |  | — |
| 40004 | 11 | `saltata_da_regola_di_prompt` |  | — |
| 40004 | 12 | `saltata_da_regola_di_prompt` |  | — |
| 40004 | 13 | `saltata_da_regola_di_prompt` |  | — |
| 40004 | 14 | `saltata_da_regola_di_prompt` |  | — |
| 40004 | 15 | `saltata_da_regola_di_prompt` |  | — |
| 40004 | 0 | `saltata_da_regola_di_prompt` |  | — |
| 40004 | 1 | `saltata_da_regola_di_prompt` |  | — |
| 40004 | 2 | `saltata_da_regola_di_prompt` |  | — |
| 40004 | 3 | `saltata_da_regola_di_prompt` |  | — |
| 40004 | 4 | `saltata_da_regola_di_prompt` |  | — |
| 40004 | 5 | `saltata_da_regola_di_prompt` |  | — |
| 40004 | 6 | `saltata_da_regola_di_prompt` |  | — |
| 40004 | 7 | `saltata_da_regola_di_prompt` |  | — |
| 40005 | — | `saltata_da_regola_di_prompt` | Libero | — |
| 40006 | 8 | `saltata_da_regola_di_prompt` |  | — |
| 40006 | 9 | `saltata_da_regola_di_prompt` |  | — |
| 40006 | 10 | `saltata_da_regola_di_prompt` |  | — |
| 40006 | 11 | `saltata_da_regola_di_prompt` |  | — |
| 40006 | 12 | `saltata_da_regola_di_prompt` |  | — |

_Mostrate le prime 60 righe su 959._

