# caso 3 protec 2 — PROTEC

Confronto fra `Mappatura_3_Cliente_PROTEC_2.pdf` e `OUTPUT PROTEC 2.txt`.

## Esito

| | |
|---|---|
| Righe estratte dal PDF | 79 |
| Righe del PDF presenti nell'output | 39 |
| Righe del PDF assenti per una regola del prompt | 40 |
| Righe del PDF assenti senza spiegazione | 0 |
| Righe del PDF senza indirizzo Modbus (grandezze derivate) | 0, di cui 0 trasformate in misure |
| Righe dell'output assenti dal PDF | 0 |

Le cinque categorie sommano a 79 contro 79 righe estratte.

### Natura degli scostamenti

| Classe | Righe |
|---|---|
| saltata da regola (comportamento richiesto) | 40 |
| corrispondenza corretta | 38 |
| correzione di refuso del documento | 1 |

Le scostamenti non sono tutti difetti. `correzione di refuso del documento` significa che il testo nel PDF e' sbagliato e l'output lo ha corretto; `scelta di progetto` significa che la pipeline ha fatto qualcosa di deliberato e diverso. Solo la classe `difetto` richiede una decisione.

### Motivi di scarto

Le righe scartate non sono un mucchio indistinto: ogni classe segue una regola diversa del prompt.

| Classe di scarto | Righe |
|---|---|
| nome generico da regola V2 del prompt | 32 |
| zona esclusa da regola V20 del prompt | 8 |

## Registri e indirizzi

- Registri distinti nel PDF: **19**, nell'output: **19**
- IP trovati nel documento: `10.127.126.99`, `10.127.126.114`, `10.127.126.113`
- IP usati dall'output: `127.0.0.1`, `10.127.126.99`
- **IP dichiarati e mai usati:** `10.127.126.114`, `10.127.126.113`
- Nomi stazione prodotti dall'output: `SME`, `SME 1`

### Dove si e' perduta la copertura

Il file di output registra nei suoi metadati quante variabili ha ricevuto: **39**, in un solo chunk.
Il PDF contiene 79 righe utilizzabili. Il pytool ne ha viste meno.

**La perdita e' avvenuta a monte del pytool, nell'estrazione VLM**, non nel pytool. Il pytool ha lavorato tutto quello che gli e' stato passato: non puo' produrre misure per righe che non ha mai ricevuto.

Su questo caso la spiegazione plausibile e' la modalita' di invio: **un solo chunk** per un documento di 29 pagine suggerisce che le pagine siano state accorpate in un'unica richiesta invece che una per iterazione. E' la stessa ipotesi del rischio n. 1 di ADR-001, e qui si vede concretamente.

### Copertura per pagina

| Pagina | Righe | Coperte | Saltate da regola |
|---|---|---|---|
| 1 | 55 | 20 | 35 |
| 2 | 24 | 19 | 5 |

## Scostamenti

| Registro | Bit | Stazione PDF | Esito | PDF | Output |
|---|---|---|---|---|---|
| 40001 | 1 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40001 | 2 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40001 | 3 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40001 | 4 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40001 | 5 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40001 | 6 | — | `saltata_da_regola_di_prompt` | Non Utilizzato | — |
| 40001 | 7 | — | `saltata_da_regola_di_prompt` | Non Utilizzato | — |
| 40001 | 13 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40002 | 0 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40002 | 1 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40002 | 2 | — | `saltata_da_regola_di_prompt` | Non Utilizzato | — |
| 40002 | 3 | — | `saltata_da_regola_di_prompt` | Non Utilizzato | — |
| 40002 | 4 | — | `saltata_da_regola_di_prompt` | Non Utilizzato | — |
| 40002 | 5 | — | `saltata_da_regola_di_prompt` | Non Utilizzato | — |
| 40002 | 6 | — | `saltata_da_regola_di_prompt` | Non Utilizzato | — |
| 40002 | 7 | — | `saltata_da_regola_di_prompt` | Non Utilizzato | — |
| 40002 | 10 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40002 | 11 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40002 | 12 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40002 | 13 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40002 | 14 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40002 | 15 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40003 | 0 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40003 | 1 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40003 | 2 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40003 | 3 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40003 | 4 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40003 | 5 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40003 | 6 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40003 | 7 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40003 | 11 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40003 | 12 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40004 | 4 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40004 | 5 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40004 | 6 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40004 | 7 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40004 | 10 | — | `nome_diverso` | RC Pressione Diferenziale | RC PRESSIONE DIFFERENZIALE |
| 40004 | 12 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40004 | 13 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40004 | 14 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40004 | 15 | — | `saltata_da_regola_di_prompt` | Disponibile | — |

