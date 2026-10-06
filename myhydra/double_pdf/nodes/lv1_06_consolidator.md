# Nodo LV1-06 — CONSOLIDA INTERMEDIO VLM

- **Tipo/nome canvas:** Pytool `PREPARAZIONE X JSON` (ex `CONSOLIDA PRE-JSON CREATOR`, nodo 11, dopo le iniezioni LV2).
- **Posizione:** dopo le iniezioni Station e Measurement e il Naive Density; non iterativo (riceve array aggregati).
- **Input:** tre array dalle tre destinazioni, con numeri edge scritti diretti nello script (verificato 05-10-2026: `#10` Station, `#11` Measurement, `#12` Density). Dopo ogni ricablaggio aggiornare i tre `{edge}[N]` in testa allo script.
- **Script:** [`../platforms/lv1/scripts/updated_pending_validation/consolidate_to_intermediate.py`](../platforms/lv1/scripts/updated_pending_validation/consolidate_to_intermediate.py).
- **Output:** `{"diagnostic": "LV1_CONSOLIDATOR", "status", "stations": [...], "density_pages": [...], "unmatched_scales": [...], "review": [...], "counters": {...}}`.
- **Contratto:** unisce per pagina le misure in ordine di sequenza; mappa `(DRIVERDATA, TYPE)` in `kind` (`(0,0)`→`ANALOGICA`, `(1,6)`→`DIGITALE_SINGOLO`, `(5,6)`→`DIGITALE_SINGOLO`, `(2,1)`→`DIGITALE_IMPACCATO`); `DRIVERDATA 5`→`read_write "W"`, resto `"R"`; `TEXTON`/`TEXTOFF`→`state_on`/`state_off`; `TAG`→`tag` (prompt v6, `null` se assente); `BIT` e registri passati come sono; `data_type` passato dal ramo misure (mai inferito: assente resta `null` per il default V25 di `json_creator`).
- **Stazioni:** primo valore non nullo per campo dai record `station_info`; un IP reale → tutte le misure lì; più IP → misure al primo + voce `multi_plc_unresolved` (caso multi-PLC mai visto nei dati di prova); solo placeholder/assenti → stazione con null (il default `SME` lo mette `json_creator`).
- **Scale:** `tag` variabile uguale al tag scala (prompt v6) oppure `NAME` uguale al tag o al tag + `" Raw"` → `scale_eng_start`/`scale_eng_end`; se la riga scala porta `unita`/`limite_orario`/`limite_giornaliero` li riversa senza sovrascrivere; resto in `unmatched_scales` + voce review.
- **Carry-over cross-pagina (decisione 6/10/2026, caso 7):** riga digitale con BIT ma senza REG eredita l'ultimo REG esplicito visto in ordine di sequenza (la LV2 gira una pagina alla volta: una cella REG a cavallo di due pagine non è recuperabile a monte) + voce `registro_applicato` con la pagina. Le analogiche senza REG restano `null`.
- **Duplicati:** stesse coppie `(NAME, registro)` tenute entrambe + voce `duplicate_measures_kept`.
- **Uso finale:** l'array `stations` è un chunk valido per `src/nodes/json_creator.py` (accetta `{"stations": [...]}`).
