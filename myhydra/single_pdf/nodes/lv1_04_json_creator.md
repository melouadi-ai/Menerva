# Nodo LV1-04 — JSON CREATOR

- **Tipo/nome:** Pytool — merge delle pagine e trasformazione in formato ADAS.
- **Input:** JSON intermedi aggregati dal nodo LV1-03, letti da `raw = r'''{edge}[4]'''`.
- **Script:** [`../pytools/json_creator_v4_2.py`](../pytools/json_creator_v4_2.py).
- **Output:** lista di stazioni in formato ADAS, con `measures` e `bitinfo`.
- **Posizione nella catena:** primo nodo dopo il motore iterativo. È la modifica strutturale prevista dall'Opzione B di ADR-001.

## Cosa fa, in ordine

1. **Parse difensivo** dell'ingresso in quattro formati accettati: JSON concatenati senza separatore, JSONL, array esterno, oggetto Python già parsato. Rimuove i fence Markdown e, in caso di errore di parsing, si riposiziona sul prossimo `{` o `[`.
2. **Validazione Pydantic opzionale** delle singole stazioni. **Non blocca mai**: errori e warning finiscono in `_warnings`. Su MyHydra la validazione è saltata, perché lo script cerca `src/models/` salendo da `__file__` e sul runtime il pacchetto non esiste.
3. **Chunk in pagine**: ogni chunk diventa una pagina logica.
4. **Forward-fill** di `name`, `ip`, `port`, `modbus_id` da una pagina alla successiva. Una pagina con `variables` vuota non crea stazione ma non azzera i valori, quindi il fill prosegue oltre le pagine vuote.
5. **Merge delle stazioni** per chiave `nome_normalizzato|ip`. Gli IP placeholder ricevono una chiave univoca e **non vengono mai fusi**, né fra loro né con IP reali.
6. **Pipeline per variabile**: filtri sulle descrizioni, parsing robusto di registro e bit, guardie di tipo, dedup, scelta del formato analogico.
7. **Emissione** delle misure e del bitinfo.
8. **Pulizia dei nomi** e rinomina delle stazioni omonime.
9. **Metadati**: `_meta` e `_warnings` iniettati in ogni stazione.

## Formati in uscita a seconda del tipo di variabile

| Tipo | `DRIVERDATA` | `TYPE` | Bitinfo |
|---|---|---|---|
| `DIGITALE_IMPACCATO` | 2 | 1 | una riga per bit, `NAME` = `Ingressi digitali N` |
| `DIGITALE_SINGOLO` | 1 in lettura, 5 in scrittura | 6 | una riga con `BITNO` 0 |
| `ANALOGICA` | 0 | 0 | nessuna |

## DRIVERPRIVATE

Sei word da 32 bit little-endian, più il prefisso `0x`: **48 caratteri esadecimali**.

```text
word[0] registro Modbus   word[1] 0   word[2] 0
word[3] 0                 word[4] ID stazione (slave)   word[5] formato (150 o 250)
```

Il formato della parola 5 dipende da `data_type`: `INT16`, `UINT16` e `INT` danno 150, tutto il resto dà 250, `WORD` compreso.

## Difetti noti, verificati sul codice

- **Le guardie A e B testano il campo `bit` grezzo, non il bit già estratto.** Una riga con `modbus_register` uguale a `"40001.3"` e `kind` `DIGITALE_SINGOLO` ha `bit` a `None` ma bit effettivo 3: non viene riclassificata e produce un digitale singolo con `BITNO` 3.
- **Il fold P2 può collassare righe.** Se più digitali singoli condividono un registro e hanno tutti `bit` assente, si trovano tutti con `BITNO` 0 e il dedup ne tiene uno solo.
- **Il dedup P1 dei digitali singoli usa il solo registro** come chiave: due digitali singoli distinti sullo stesso registro, il secondo viene scartato con il suo bitinfo.
- **Nessun `try/except` globale.** Il legacy ne aveva uno che restituiva un JSON di errore; v4.2 lascia propagare le eccezioni, quindi un errore non gestito significa nessun output.
- **`NAME` non viene più troncato.** La colonna `NAME` è `nvarchar(50)` e il legacy tagliava a 49 caratteri.

I dettagli di confronto con il legacy e le divergenze riscontrate su dati reali sono in [`../test/caso_2_protec_1/README.md`](../test/caso_2_protec_1/README.md).

- **Da confermare:** l'indice `{edge}[4]` è fragile, perché cambia se il numero di nodi precedenti il pytool varia. Verificare sul canvas prima dell'incollaggio.
- **Riferimenti:** [`../pytools/README.md`](../pytools/README.md), [contratto ADAS](../../../docs/contracts/ADAS_FINAL.md) *(con riserve, vedi `pytools/README.md`)*.
