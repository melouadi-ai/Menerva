# LV2 — indice sottopiattaforme

- [`page_classifier/`](page_classifier/README.md): classifica ruolo documento e tipo pagina. Powered identity corrente non ancora riverificata dopo la separazione dei campi VLM.
- [`station_information/`](station_information/README.md): estrae i dati visibili per pagina. La nuova configurazione del VLM non è ancora stata riverificata.
- [`measurement/`](measurement/README.md): tre estrazioni parallele per pagina. Prompt e Pytool etichettatori sono pronti, da verificare insieme su MyHydra.
- [`shared/`](shared/README.md): estrazione comune della chiave dalla pagina iterativa.
