# Nodo SLICE — fetta di gruppi-pagina per shard parallelo (nuovo)

- **Tipo/nome:** Pytool — ritaglia le pagine di uno shard da SIEMENS/protocolli lunghi.
- **Input:** array dei gruppi da LV1-02 MEDIA2CONTENT (oggetti `{_medexkeys}`, in ordine).
- **CONFIG:** costanti `START`/`END` (1-based, inclusi; topologia universale una sola volta: A 1-10, B 11-20, C 21-10000) e `N` di `raw = r'''{edge}[N]'''` (ricontrollare a ogni rewiring, togliere match-condition spurie).
- **Script:** [`../platforms/lv1/scripts/updated_pending_validation/slicer_canvas.py`](../platforms/lv1/scripts/updated_pending_validation/slicer_canvas.py) (copia canvas; documentata in [`../pytools/slicer.py`](../pytools/slicer.py)).
- **Output:** stessa forma dell'input (array) con le sole posizioni `[START:END]`, pronto per il motore iterativo dello shard. Range impossibile o input non lista → ERROR JSON con `tb`, mai blank.
- **Posizione nella catena:** tra MEDIA2CONTENT e il motore iterativo di ogni shard. Il motore sotto non vede differenze rispetto al flusso seriale.
- **Verifica senza tap/debug:** il Naive a valle mostra la fetta; la lunghezza deve essere `END-START+1`.
- **Riferimenti:** `tests/test_single_shard_merger.py`, scheda `lv1_03b_merger.md`.
