# Nodo LV2-02 — VLM, i 3 rami di estrazione

- **Tipo/nome:** Visiomaru — modello vision-language, unica sorgente di estrazione dati.
- **Input:** l'immagine prodotta dal nodo LV2-01, che corrisponde a **una pagina**, in tutti e tre i rami in parallelo.
- **Configurazione dei campi (identica nei 3 rami):** `{edge.media}[N]` **da solo** nel campo **Prompt**; istruzioni in **Powered identity**; **Context** vuoto. `N` è locale al canvas.
- **Prompt correnti:**
  - ramo 1, misure + dati tecnici: [`../prompt/vlm_measures_v18.md`](../prompt/vlm_measures_v18.md)
  - ramo 2, nomi bit: [`../prompt/vlm_bitnames_v16.md`](../prompt/vlm_bitnames_v16.md)
  - ramo 3, stati TEXTON/TEXTOFF: [`../prompt/vlm_bitstates_v19.md`](../prompt/vlm_bitstates_v19.md)
- **Stato:** copie byte-identiche a `src/prompts/`, mai eseguite sul canvas: il canvas attivo esegue ancora `vlm_extraction_v13.md` (ramo unico), conservato come storico in [`../prompt/history/`](../prompt/history/).

## Perché tre rami e non uno

Il ramo unico v13 chiedeva al VLM una pagina intera in una sola risposta: su
pagine dense l'estrazione si troncava e le unità di misura si perdevano. Il
redesign ha diviso il compito in tre estrazioni indipendenti della **stessa
immagine**, ognuna con un contratto minimo e un self-check proprio:

| Ramo | Emette | Non emette mai |
|---|---|---|
| misure (v18) | descrizione, unità, registro, bit, `kind`, `data_type`, `read_write`, scale, limiti, `zona`, `tag`, `pagina`, `riga` | `state_on`/`state_off` |
| nomi bit (v16) | descrizione, registro, bit, `riga` | unità, scale, stati, `kind`, `data_type`, campi stazione |
| stati (v19) | `state_on`, `state_off`, descrizione check-key, `riga` | registro, unità, scale |

Il **join** fra i tre avviene nel nodo LV1-04 CONSOLIDATORE, sulla chiave
`riga` (indice fisico della riga nella pagina, buche comprese). Ogni
disaccordo produce un warning: `riga_disallineata`, `riga_mismatch`,
`bit_register_mismatch`, `descrizione_mismatch`, `refuso_sospetto`,
`refuso_maggioranza`, `stati_disallineati`, `stati_orfani`.

## Il Livello 2 termina al VLM

Con l'Opzione B di ADR-001 il Livello 2 non contiene nodi di merge: ognuno dei
tre rami passa per un Pytool etichettatore e per l'assemblatore di pagina, e
torna al motore. Il merge vero è nel consolidatore, a valle.

## Confini del compito del VLM

Il prompt è costruito perché il modello **legga e trascriva, senza calcolare**. Le regole chiave sono:

- **Una immagine corrisponde a una pagina.** Non deve ricordare né completare righe di altre pagine.
- **`description` e gli stati sono copia esatta.** Se non sono leggibili, il valore è `null`. Vietato inferire da parole chiave o mettere valori predefiniti. **Anche un refuso del documento si trascrive**: la correzione è del cliente, non del modello.
- **`data_type` va copiato dalla colonna, mai dedotto** dal nome o dal registro.
- **Ogni bit va copiato dalla propria riga**, senza rinumerare né interpolare, e **mai calcolato da una colonna coil** (V30/`BIT SOURCE`). Righe consecutive possono avere bit non consecutivi.
- **`riga` è l'indice fisico della riga** nella pagina, contando anche le righe scartate (che lasciano buche). Senza questo contratto comune il join posizionale slitta (regressione PROTEC_1/PROTEC_2/SIEMENS).
- **Non calcolare** `DRIVERPRIVATE`, `ID`, `DRIVERDATA`, `TYPE` e l'XML. Non spettano al VLM.

I calcoli deterministici sono compito del pytool LV1-05 JSON CREATOR. La divisione è il principio architetturale dell'intero progetto.

## Punti di frizione noti

**Gli stati ON/OFF.** Le regole V7/V8 vietano al VLM di dedurre gli stati, e il ramo stati le rispetta. Il pytool, però, contiene una tabella di parole chiave che li deduce comunque quando mancano. Non è un errore ma una delocalizzazione deliberata della regola dal prompt al codice: la dipendenza `TEXTON da keyword` deve restare visibile nel warning, mai silenziosa.

**Lo schema di validazione.** Nello schema Pydantic `description` è una stringa obbligatoria e non vuota, mentre il prompt la dichiara come `string|null` e la regola V2 dice di saltare la riga invece di emettere `null`. Sul canvas la validazione Pydantic è saltata per disegno (`_pydantic_available = False`): l'errore non blocca il flusso, ma in locale il validatore lo segnala.

- **Riferimenti:** [`../prompt/README.md`](../prompt/README.md) (inventario e hash), [`../platforms/lv2/README.md`](../platforms/lv2/README.md) (rami e precedenze), [contratto VLM](../../../docs/contracts/VLM_INTERMEDIATE.md).
