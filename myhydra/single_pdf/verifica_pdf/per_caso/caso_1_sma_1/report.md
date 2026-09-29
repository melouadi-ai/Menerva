# caso 1 sma 1 — SMA

Confronto fra `Mappatura_1_Cliente_SMA_1.pdf` e `Output SMA_1.txt`.

## Esito

| | |
|---|---|
| Righe estratte dal PDF | 50 |
| Righe del PDF presenti nell'output | 45 |
| Righe del PDF assenti per una regola del prompt | 0 |
| Righe del PDF assenti senza spiegazione | 0 |
| Righe del PDF senza indirizzo Modbus (grandezze derivate) | 5, di cui 5 trasformate in misure |
| Righe dell'output assenti dal PDF | 0 |

Le cinque categorie sommano a 50 contro 50 righe estratte.

### Natura degli scostamenti

| Classe | Righe |
|---|---|
| corrispondenza corretta | 42 |
| difetto | 2 |
| correzione di refuso del documento | 1 |

Le scostamenti non sono tutti difetti. `correzione di refuso del documento` significa che il testo nel PDF e' sbagliato e l'output lo ha corretto; `scelta di progetto` significa che la pipeline ha fatto qualcosa di deliberato e diverso. Solo la classe `difetto` richiede una decisione.

## Righe del documento trasformate in misure senza indirizzo

Il documento contiene righe di grandezze derivate che **non hanno un indirizzo Modbus**: sono valori calcolati a partire da altri registri. L'output le ha comunque emesse come misure, e in particolare contro il registro 0, che non corrisponde a nulla nel documento.

Da solo il JSON non mostra il problema: `DRIVERPRIVATE` ha la lunghezza giusta ed esadecimale valido, solo che la prima parola e' zero.

| Riga nel PDF | Tipo | Misura emessa | Registro emesso |
|---|---|---|---|
| NOX | CALCOLATA | NOX | 0 |
| H2O | CALCOLATA | H2O | 0 |
| PORTATA FUMI umida | CALCOLATA | PORTATA FUMI umida | 0 |
| Polveri () | CALCOLATA | Polveri | 0 |
| Polveri TQ | CALCOLATA | Polveri TQ | 0 |

## Registri e indirizzi

- Registri distinti nel PDF: **43**, nell'output: **43**
- IP trovati nel documento: `192.168.6.20`, `IP xxx,xxx,xxx,xxx`
- IP usati dall'output: `192.168.6.20`, `xxx.xxx.xxx.xxx`
- **IP dichiarati e mai usati:** `IP xxx,xxx,xxx,xxx`
- **Il documento usa più di una convenzione di indirizzo:** `0-padded` (30 righe, es. 00033, 00034, 00035, 00036, 00037), `4xxxx` (15 righe, es. 40001, 40002, 40003, 40004, 40005)

  La normalizzazione del pytool applica la stessa regola a tutte. Gli indirizzi che nel documento avevano zeri iniziali arrivano nell'output come interi brevi, cioè puntano a un registro diverso da quello scritto. Il confronto riga per riga non può segnalarlo, perché dall'output l'informazione sulla convenzione originale è perduta.
- Nomi stazione prodotti dall'output: `E1`, `E1 1`
- Metadati nel PDF: cliente=Silve, punto_emissivo=E1

### Dove si e' perduta la copertura

Il file di output registra nei suoi metadati quante variabili ha ricevuto: **52**, in un solo chunk.
Il PDF contiene 50 righe utilizzabili. Il pytool ne ha viste altrettante.

## Scostamenti

| Registro | Bit | Esito | PDF | Output |
|---|---|---|---|---|
| 40001 | — | `nome_diverso` | Temperatura Fumi | CO |
| 40005 | — | `nome_diverso` | CO | Pressione |
| 45 | — | `nome_diverso` | Allarme 1 Ossiegno umido | ALLARME 1 OSSIGENO UMIDO |

