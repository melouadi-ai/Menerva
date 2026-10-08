# Nodo MERGER — ricucitura chunk degli shard (nuovo)

- **Tipo/nome:** Pytool — concatena i chunk di 2 shard in ordine (A poi B).
- **Input:** due output grezzi di motore (`raw_a`, `raw_b`: stringhe con fence, array o dict; parser tollerante come il consolidatore).
- **CONFIG:** `N` dei due `{edge}` da ricontrollare a ogni rewiring, togliere match-condition spurie. Per 3 shard usare due merger in cascata (AB, poi ABC con l'output del primo in A).
- **Script:** [`../platforms/lv1/scripts/updated_pending_validation/merger_canvas.py`](../platforms/lv1/scripts/updated_pending_validation/merger_canvas.py) (copia canvas; documentata in [`../pytools/merger.py`](../pytools/merger.py)).
- **Output:** array unico dei blocchi (A+B), pronto per LV1-04 CONSOLIDATORE che li raggruppa in pagine in ordine di arrivo. Shard vuoto o illeggibile → ERROR JSON con `tb` e nome dello shard, mai silenzio.
- **Posizione nella catena:** tra i motori degli shard e il CONSOLIDATORE. Consolidatore e creator invariati.
- **Rischio residuo documentato:** una pagina persa *dentro* uno shard vivo non lascia buchi visibili; il merger conta solo shard vivi/morti. Mitigazione: confronto variabili per shard nel tap.
- **Riferimenti:** `tests/test_single_shard_merger.py`, scheda `lv1_02b_slicer.md`.
