# Nodo LV1-05 — JSON CREATOR

- **Tipo/nome:** Pytool — trasformazione dell'intermedio unificato in formato ADAS.
- **Input:** `{"stations": [...]}` dal nodo LV1-04 CONSOLIDATORE, letto da `raw = r'''{edge}[4]'''`.
- **CONFIG:** il `4` è locale al canvas — **ricontrollare N a ogni rewiring** (l'inserimento del consolidatore sposta gli indici a valle; ispezionare anche le match-condition dell'edge).
- **Script:** [`../platforms/lv1/scripts/updated_pending_validation/json_creator_v15_canvas.py`](../platforms/lv1/scripts/updated_pending_validation/json_creator_v15_canvas.py) (copia canvas, 26.857 byte; documentata byte-identica a `src/nodes/json_creator.py` in [`../pytools/json_creator_v15.py`](../pytools/json_creator_v15.py)).
- **Output:** lista di stazioni in formato ADAS, con `measures` e `bitinfo`. Emissione via `print(output)` (meccanismo legacy, verificato sul canvas dal Double, nodo 12).
- **Posizione nella catena:** ultimo nodo, dopo il consolidatore. Con l'Opzione B di ADR-001 il merge vive nel consolidatore: qui solo trasformazione deterministica.

## Cosa fa, in ordine (v15)

1. **Parse difensivo** dell'ingresso (stessi quattro formati del legacy).
2. **Pipeline per variabile**: filtri sulle descrizioni, parsing robusto di registro e bit, guardie di tipo, dedup, scelta del formato analogico da `data_type` (`INT16`/`UINT16`/`INT` → 150, resto/assente → 250).
3. **V19 vince su P5**: rimuove solo parentesi tonde vuote, virgolette esterne appaiate, spazi multipli. Parentesi con contenuto (`(GR)`), quadre, parole, refusi mai toccati.
4. **NAME misure troncato a 49 char** (ADAS nvarchar(50)); parola-intestazione `Unità`/`Unita` mai in UNITS (difesa in profondità su V3).
5. **Fondo scala dichiarato** → `LOWRANGE`/`HIGHRANGE`, sentinel se assente; limiti e divisori solo in review con i nomi (mapping BISON col cliente).
6. **Metadati**: `_meta` e `_warnings` iniettati in ogni stazione.

## Guardie attive (difesa in profondità, pinnate nella copia canvas)

- **Copertura A1**: più stazioni con lo stesso `page_no` e volume sopra soglia 100 → `COPERTURA SOSPETTA` (SIEMENS_2 sì, SMA_1 no).
- **Self-check linkage** bitinfo→misure; **avviso zeri iniziali** (`00033`); misure a registro 0 scartate (grandezze `CALCOLATA`).

## Limiti noti (ereditati, non risolti qui)

- **Nessun `try/except` globale**: un'eccezione = output blank senza ERROR JSON (il consolidatore a monte invece lo garantisce). In diagnosi, il blank del creator si riconosce così: edge e indice ok, ma nessun output.
- **`_meta` e `_warnings` duplicati** in ogni stazione (scelta pragmatica per non rompere l'import ADAS).
- **Il Double ha una copia separata** con `{edge}[13]` (`../../double_pdf/platforms/lv1/scripts/in_use/`): non mescolarle, l'indice è diverso perché diverso è il filo.

- **Riferimenti:** [`../platforms/README.md`](../platforms/README.md) (contratto I/O e checklist edge), [`lv1_04_consolidatore.md`](lv1_04_consolidatore.md), [`../pytools/README.md`](../pytools/README.md), [contratto ADAS](../../../docs/contracts/ADAS_FINAL.md) *(con riserve, vedi `pytools/README.md`)*.
