# Materiali per platform

Ogni cartella raccoglie gli artefatti MyHydra di una platform o sottopiattaforma. I nomi delle cartelle esprimono lo stato operativo:

- `scripts/in_use/`: script già usati nel canvas attivo.
- `scripts/updated_pending_validation/`: revisione pronta, ma da confermare con una run MyHydra.
- `scripts/parked/` e `scripts/diagnostics/`: materiale non collegato al flusso attivo.
- `scripts/history/` e `prompts/history/`: versioni precedenti, conservate per confronto.
- `prompts/current/`: prompt Powered identity da usare nella configurazione corrente. Se non sono ancora stati eseguiti dopo una modifica, il README della sottopiattaforma lo indica.

Nel VLM, `{edge.media}[n]` va nel campo **Prompt**, **Context** resta vuoto e le istruzioni vanno nel **Powered identity**. Gli edge `{edge}[n]` dei Pytool restano riferimenti ai payload testuali.

## Indice

- [`lv1/`](lv1/README.md): deduplicazione e routing dei record pagina.
- [`lv2/page_classifier/`](lv2/page_classifier/README.md): ruolo documento e categoria pagina.
- [`lv2/station_information/`](lv2/station_information/README.md): estrazione dati stazione.
- [`lv2/measurement/`](lv2/measurement/README.md): misure e dati bitinfo.
- [`lv2/shared/`](lv2/shared/README.md): utility comuni alle LV2 iterative.
