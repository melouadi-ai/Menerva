# Materiali per platform

Ogni cartella raccoglie gli artefatti MyHydra di una platform o sottopiattaforma. I nomi delle cartelle esprimono lo stato operativo:

- `scripts/in_use/`: script già usati nel canvas attivo.
- `scripts/updated_pending_validation/`: revisione pronta, ma da confermare con una run MyHydra.
- `scripts/parked/` e `scripts/diagnostics/`: materiale non collegato al flusso attivo.
- `scripts/history/` e `prompts/history/`: versioni precedenti, conservate per confronto.
- `prompts/current/`: prompt Powered identity da usare nella configurazione corrente. Se non sono ancora stati eseguiti dopo una modifica, il README della sottopiattaforma lo indica.

Nei VLM legacy che leggevano (screenshot visio2: Station Info, Measures, BitInfo General, BitInfo TextON/TextOFF) il campo **Prompt** conteneva istruzioni e token media insieme, con il token dentro il testo (`{edge.media}[23]`, `[19]`, `[20]`, `[21]` — indici locali a quel canvas). Nessun campo separato. Il layout separato (token solo in Prompt, istruzioni in Powered identity, Context vuoto) è verificato funzionante dal 2 ott 2026: la sonda con quel layout ha restituito `image_readable: true` con 5 righe radicate nel PDF. Entrambi i layout sono validi; il colpevole dei gusci vuoti era l'input del Medex, non i campi. Il layout legacy-inline è confermato funzionante il 2 ott 2026 dal prompt di trascrizione con token `{edge.media}[1]` dentro il testo (tabella TSV reale trascritta sul ramo misure). Gli edge `{edge}[n]` dei Pytool restano riferimenti ai payload testuali.

## Indice

- [`lv1/`](lv1/README.md): deduplicazione e routing dei record pagina.
- [`lv2/page_classifier/`](lv2/page_classifier/README.md): ruolo documento e categoria pagina.
- [`lv2/station_information/`](lv2/station_information/README.md): estrazione dati stazione.
- [`lv2/measurement/`](lv2/measurement/README.md): misure e dati bitinfo.
- [`lv2/shared/`](lv2/shared/README.md): utility comuni alle LV2 iterative.
