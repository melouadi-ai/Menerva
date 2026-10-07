# caso 2 protec 1 — PROTEC

Confronto fra `Mappatura_2_Cliente_PROTEC_1.pdf` e `Output PROTEC 1.txt`.

## Esito

| | |
|---|---|
| Righe estratte dal PDF | 89 |
| Righe del PDF presenti nell'output | 45 |
| Righe del PDF assenti per una regola del prompt | 44 |
| Righe del PDF assenti senza spiegazione | 0 |
| Righe del PDF senza indirizzo Modbus (grandezze derivate) | 0, di cui 0 trasformate in misure |
| Righe dell'output assenti dal PDF | 0 |

Le cinque categorie sommano a 89 contro 89 righe estratte.

### Natura degli scostamenti

| Classe | Righe |
|---|---|
| saltata da regola (comportamento richiesto) | 44 |
| corrispondenza corretta | 43 |
| scelta_di_progetto | 2 |

Le scostamenti non sono tutti difetti. `correzione di refuso del documento` significa che il testo nel PDF e' sbagliato e l'output lo ha corretto; `scelta di progetto` significa che la pipeline ha fatto qualcosa di deliberato e diverso. Solo la classe `difetto` richiede una decisione.

### Motivi di scarto

Le righe scartate non sono un mucchio indistinto: ogni classe segue una regola diversa del prompt.

| Classe di scarto | Righe |
|---|---|
| nome generico da regola V2 del prompt | 44 |

## Registri e indirizzi

- Registri distinti nel PDF: **14**, nell'output: **10**
- IP trovati nel documento: `192.168.0.1`, `192.168.0.2`
- IP usati dall'output: `127.0.0.1`, `192.168.0.1`
- **IP dichiarati e mai usati:** `192.168.0.2`
- Nomi stazione prodotti dall'output: `SME`, `SME 1`

### Dove si e' perduta la copertura

Il file di output registra nei suoi metadati quante variabili ha ricevuto: **45**, in un solo chunk.
Il PDF contiene 85 righe utilizzabili. Il pytool ne ha viste meno.

**La perdita e' avvenuta a monte del pytool, nell'estrazione VLM**, non nel pytool. Il pytool ha lavorato tutto quello che gli e' stato passato: non puo' produrre misure per righe che non ha mai ricevuto.

Su questo caso la spiegazione plausibile e' la modalita' di invio: **un solo chunk** per un documento di 29 pagine suggerisce che le pagine siano state accorpate in un'unica richiesta invece che una per iterazione. E' la stessa ipotesi del rischio n. 1 di ADR-001, e qui si vede concretamente.

### Copertura per pagina

| Pagina | Righe | Coperte | Saltate da regola |
|---|---|---|---|
| 1 | 57 | 30 | 27 |
| 2 | 32 | 15 | 17 |

## Scostamenti

| Registro | Bit | Stazione PDF | Esito | PDF | Output |
|---|---|---|---|---|---|
| 40002 | 0 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40002 | 1 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40002 | 2 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40002 | 3 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40002 | 4 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40002 | 5 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40002 | 6 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40002 | 7 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40002 | 12 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40002 | 13 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40002 | 14 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40002 | 15 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40003 | 2 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40003 | 3 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40003 | 4 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40003 | 5 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40003 | 6 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40003 | 7 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40004 | 0 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40004 | 1 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40004 | 2 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40004 | 3 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40004 | 4 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40004 | 5 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40004 | 6 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40004 | 7 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40004 | 8 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40004 | 9 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40004 | 12 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40004 | 13 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40004 | 14 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40004 | 15 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40005 | — | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40006 | — | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40007 | 4 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40007 | 5 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40007 | 6 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40007 | 7 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40007 | 10 | — | `riclassificata_dal_pytool` | OVF Misura Disponibile IW36 | — |
| 40007 | 11 | — | `riclassificata_dal_pytool` | OVF Misura Disponibile IW38 | — |
| 40007 | 12 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40007 | 13 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40007 | 14 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40007 | 15 | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40024 | — | — | `saltata_da_regola_di_prompt` | Disponibile | — |
| 40028 | — | — | `saltata_da_regola_di_prompt` | Disponibile | — |

