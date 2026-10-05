# Nodo LV1-06 — CONSOLIDA INTERMEDIO VLM

- **Tipo/nome canvas:** Pytool `CONSOLIDA PRE-JSON CREATOR` (nodo da creare dopo le iniezioni LV2).
- **Posizione:** dopo le iniezioni Station e Measurement e il Naive Density; non iterativo (riceve array aggregati).
- **Input:** tre array dalle tre destinazioni, con numeri edge scritti diretti nello script (verificato 05-10-2026: `#10` Station, `#11` Measurement, `#12` Density). Dopo ogni ricablaggio aggiornare i tre `{edge}[N]` in testa allo script.
- **Script:** [`../platforms/lv1/scripts/updated_pending_validation/consolidate_to_intermediate.py`](../platforms/lv1/scripts/updated_pending_validation/consolidate_to_intermediate.py).
- **Output:** `{"diagnostic": "LV1_CONSOLIDATOR", "status", "stations": [...], "density_pages": [...], "unmatched_scales": [...], "review": [...], "counters": {...}}`.
- **Contratto:** unisce per pagina le misure in ordine di sequenza; mappa `(DRIVERDATA, TYPE)` in `kind` (`(0,0)`→`ANALOGICA`, `(1,6)`→`DIGITALE_SINGOLO`, `(5,6)`→`DIGITALE_SINGOLO`, `(2,1)`→`DIGITALE_IMPACCATO`); `DRIVERDATA 5`→`read_write "W"`, resto `"R"`; `TEXTON`/`TEXTOFF`→`state_on`/`state_off`; `BIT` e registri passati come sono; `data_type` sempre `null` (il ramo misure non lo estrae: vale il default V25 di `json_creator`).
- **Stazioni:** primo valore non nullo per campo dai record `station_info`; un IP reale → tutte le misure lì; più IP → misure al primo + voce `multi_plc_unresolved` (caso multi-PLC mai visto nei dati di prova); solo placeholder/assenti → stazione con null (il default `SME` lo mette `json_creator`).
- **Scale:** tag uguale a `NAME` oppure a `NAME` senza suffisso `" Raw"` → `scale_eng_start`/`scale_eng_end`; resto in `unmatched_scales` + voce review.
- **Duplicati:** stesse coppie `(NAME, registro)` tenute entrambe + voce `duplicate_measures_kept`.
- **Uso finale:** l'array `stations` è un chunk valido per `src/nodes/json_creator.py` (accetta `{"stations": [...]}`).
