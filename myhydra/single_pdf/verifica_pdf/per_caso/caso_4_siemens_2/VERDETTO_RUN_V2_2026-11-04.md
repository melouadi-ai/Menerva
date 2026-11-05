# Verdetto run v2 — SIEMENS_2 (29 pagine)

**Data run:** 4 nov 2026
**File:** `myhydra/single_pdf/TESTS/SIEMENS NUOVO/TAP_FINALE.txt`
**Riferimento legacy:** `FINALE LORENZO.txt` (29/10, stessa stazione)
**PDF sorgente:** `myhydra/single_pdf/pdf_input/Mappatura_4_Cliente_SIEMENS_2.pdf`

## Numeri

| | Noi (v2) | Legacy (Lorenzo) |
|---|---|---|
| Stazioni | 1 | 1 |
| Misure | 105 | 105 |
| Bitinfo | 145 | 145 |
| TYPE | 90 analogiche + 15 digitali | 90 + 15 |
| DRIVERDATA | 70/20/15 | 70/20/15 |
| Registri | 3486–61340 | 3486–61340 |
| IP | 192.168.2.11 | 192.168.2.11 |

**Numeri identici.** I 105 registri misure e i 145 bitinfo sono gli stessi.

## Difetti trovati

### 1. Nomi misure troncati a 49 char (39 su 105)

Tutti i 39 nomi troncati hanno esattamente **49 caratteri**. Il legacy ha nomi
completi fino a 83 char. Esempi:

| Noi (49) | Legacy (completo) |
|---|---|
| `COG2: CAMPO SCALA LOW 1 MISURA TEMPERATURA LINEA ` | `…LINEA PRELIEVO` (57) |
| `COG2: MISURA ULTIMA CALx CO ZERO (Calibrazione St` | `…(Calibrazione Strumentale)` (59) |
| `WATCH DOG COMUNICAZIONE PLC (se varia OK master+I` | `…(se varia OK master+I/O ok)` (55) |
| `COG2: PROGRESSIVO DATI CALIBRAZIONE COMPLETAM. OK` | `…OK CALx C1 (Variaz = read Data a PC)` (83) |

**Causa probabile:** il VLM UNIFIED tronca i nomi a ~49 char. Non c'è un
limite esplicito nel prompt `vlm_unified_v1.md`; è un comportamento del
modello. Il pytool `json_creator_v15.py` non tronca: usa `desc` così com'è.

**Gravità:** alta. I nomi troncati sono ambigui e non identificano la misura.

### 2. "Ingressi digitali N" numerati in ordine di apparizione, non di registro

I 15 registri sono gli stessi in noi e legacy, ma il numero nel nome è diverso:

| Registro | Noi | Legacy |
|---|---|---|
| 16796 | Ingressi digitali 1 | Ingressi digitali 1 |
| 17308 | Ingressi digitali 8 | Ingressi digitali 2 |
| 19356 | Ingressi digitali 2 | Ingressi digitali 3 |
| 19612 | Ingressi digitali 3 | Ingressi digitali 4 |
| 19868 | Ingressi digitali 9 | Ingressi digitali 5 |
| 20124 | Ingressi digitali 10 | Ingressi digitali 6 |
| 20380 | Ingressi digitali 11 | Ingressi digitali 7 |
| 20636 | Ingressi digitali 12 | Ingressi digitali 8 |
| 20892 | Ingressi digitali 13 | Ingressi digitali 9 |
| 21916 | Ingressi digitali 4 | Ingressi digitali 10 |
| 22172 | Ingressi digitali 5 | Ingressi digitali 11 |
| 22428 | Ingressi digitali 14 | Ingressi digitali 12 |
| 22684 | Ingressi digitali 15 | Ingressi digitali 13 |
| 22940 | Ingressi digitali 6 | Ingressi digitali 14 |
| 23708 | Ingressi digitali 7 | Ingressi digitali 15 |

**Causa:** `json_creator_v15.py` riga 608: `packed_count` incrementa in ordine
di apparizione delle righe nel consolidato. Il legacy numera in ordine di
registro crescente.

**Gravità:** media. I registri sono corretti; solo il numero nel nome è
sbagliato. Ma il nome è l'unico identificatore visibile in ADAS.

### 3. `(impulsivo)` perso dai BITNAME (12 su 145)

Nel PDF (pagina 2) le 12 righe del registro 40016 (16796) hanno `(impulsivo)`
in minuscolo alla fine della descrizione. Il legacy lo riporta come
`(IMPULSIVO)` nei BITNAME. Noi lo perdiamo: 0/12 bitinfo con `(IMPULSIVO)`.

**Causa:** il VLM UNIFIED non copia `(impulsivo)` nella descrizione. Il prompt
V13 dice "Copy texts AS THEY ARE: no removal of parentheses with content", ma
il modello lo rimuove comunque. Il pytool non lo rimuove: usa `desc` così com'è.

**Gravità:** bassa. È un'informazione secondaria, ma è nel PDF e il legacy la
riporta.

### 4. UNITS mancanti su 6 misure analizzatore

| Misura | Noi | Legacy |
|---|---|---|
| COG2: MISURA ANALIZZATORE CO (mg/m3) | None | mg/m3 |
| COG2: MISURA ANALIZZATORE NO (mg/m3) | None | mg/m3 |
| COG2: MISURA ANALIZZATORE O2 (%) | None | % |
| COG3: MISURA ANALIZZATORE CO (mg/m3) | None | mg/m3 |
| COG3: MISURA ANALIZZATORE NO (mg/m3) | None | mg/m3 |
| COG3: MISURA ANALIZZATORE O2 (%) | None | % |

**Causa probabile:** il VLM UNIFIED non legge la colonna unità per queste 6
righe. Il nome contiene già l'unità tra parentesi `(mg/m3)`, `(%)`, ma il
campo `units` resta null. Il legacy la riporta sia nel nome sia in UNITS.

**Gravità:** media. L'unità è deducibile dal nome, ma il campo UNITS è quello
che ADAS usa per la conversione.

### 5. TEXTON diversi su 5 bit

| (registro, BITNO) | Noi | Legacy |
|---|---|---|
| (21916, 10) MEMORIZZAZIONE DATA MMC ERRORE | ERRORE | ATTIVO |
| (22428, 11) COG2: COM. ELT YV3 (ZERO-SPANL) | ZERO | ATTIVO |
| (22428, 15) COG2: STATO VERIFICA QAL3…TERMINATA | ERRORE | ATTIVO |
| (22940, 11) COG3: COM. ELT YV4 (ZERO-SPANL) | ZERO | ATTIVO |
| (22940, 15) COG3: STATO VERIFICA QAL3…TERMINATA | ERRORE | ATTIVO |

**Causa:** il VLM UNIFIED legge il testo della cella stato-ON dal PDF. Il
legacy usa `ATTIVO` come default per tutti i bit. Nel PDF le celle stato-ON
sono vuote (non c'è una colonna stato in queste pagine), quindi il VLM
inventa un testo basandosi sulla descrizione. Il legacy usa un default
fisso.

**Gravità:** bassa. Il PDF non ha una colonna stato per queste righe; sia noi
sia il legacy inventiamo. Noi inventiamo qualcosa di più specifico, il legacy
usa un default generico.

### 6. Refusi nei nomi bitinfo

| (registro, BITNO) | Noi | Legacy | PDF |
|---|---|---|---|
| (19356, 6) | FORZATL | FORZATI | non estraibile |
| (20124, 13) | DA RESETTA RE | DA RESET TARE | non estraibile |
| (20636, 13) | DA RESETTA RE | DA RESET TARE | non estraibile |
| (22172, 1,2,9,10,13,14) | U23. O2 / U23.O2 | U23, O2 / U23,O2 | `U23. "CO"` (p8) |

**Causa:** il VLM UNIFIED legge i refusi dal PDF. Il legacy li corregge.
Per `U23.` vs `U23,`: nel PDF (pagina 8) il formato è `U23. "CO"` con punto,
quindi noi siamo fedeli al PDF e il legacy corregge. Per `FORZATL`/`FORZATI`
e `RESETTA RE`/`RESET TARE`: il testo non è estraibile dal PDF, non si può
verificare.

**Gravità:** bassa. La fedeltà al PDF è la regola V13; il legacy corregge i
refusi, noi no. Comportamento coerente col prompt.

## MERGE: oracolo assente su 29/29 pagine

Il warning `oracolo_input_assente: json UNIFIED assente o non interpretabile`
compare su **tutte e 29 le pagine** nel TAP_MERGE. Il ramo ORACOLO non ha mai
funzionato in questa run.

**Causa:** il nodo ORACOLO non riceve il JSON di UNIFIED nel campo Context.
Il prompt `vlm_oracle_v1.md` regola R0 dice: se il Context è vuoto, rispondere
con `errore_input`. Il `PAGE_ASSEMBLER` lo porta nel tap come
`oracolo_input_assente`.

**Da verificare sul canvas:**
1. Il nodo ORACOLO ha il campo Context con `{edge}[M]` (testo di UNIFIED)?
2. L'indice `M` è corretto dopo l'ultimo rewiring?
3. Il nodo ORACOLO è cablato (edge da UNIFIED a ORACOLO)?

**Gravità:** alta. Senza l'oracolo non c'è verifica: i difetti 1-6 non
sarebbero stati rilevati automaticamente.

## CONSOLIDATORE

- 2 stazioni: una con `name='Reekep OLIVETTI'` (0 variabili) e una con
  `name=None` (237 variabili).
- `counters`: pagine=29, variabili=237, scarti_V20=2, buchi_sequenza=1.
- Warning `pagina_senza_numero` su più pagine.

**Nota:** la stazione con `name=None` e 237 variabili è quella che contiene
tutte le misure. La stazione con nome e 0 variabili è un artefatto della
pagina 1 (che ha solo l'intestazione, nessuna riga dati).

## `_meta.audit_oracolo`

Vuoto (0 variabili toccate dall'oracolo), coerente con l'oracolo assente.

## Priorità fix

1. **ORACOLO non cablato** (alta): verificare il Context del nodo ORACOLO e
   l'indice edge. Senza oracolo non c'è verifica.
2. **Nomi troncati a 49 char** (alta): il VLM tronca. Serve una regola
   esplicita nel prompt UNIFIED: "NON troncare i nomi, copia la descrizione
   completa anche se lunga".
3. **UNITS mancanti su 6 misure** (media): il VLM non legge la colonna unità.
   Verificare se nel PDF la colonna unità è presente per quelle righe.
4. **Numerazione "Ingressi digitali"** (media): cambiare `packed_count` in
   ordine di registro crescente, non di apparizione.
5. **`(impulsivo)` perso** (bassa): il VLM rimuove le parentesi. Regola
   esplicita nel prompt: "NON rimuovere parentesi con contenuto".
6. **TEXTON inventati** (bassa): il VLM inventa stati dove il PDF non ce li
   ha. Accettabile: il legacy fa lo stesso con un default.
7. **Refusi** (bassa): comportamento coerente col prompt V13 (fedeltà al PDF).
