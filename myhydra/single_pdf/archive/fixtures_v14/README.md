# Test — Single PDF

## Casi presenti

| Caso | Documento | Copertura |
|---|---|---|
| [`caso_2_protec_1/`](caso_2_protec_1/) | `Mappatura_2_Cliente_PROTEC_1` | 2 pagine, 45 variabili, 2 stazioni in output. Fixture VLM reale. |

## Perché un solo caso

È l'unico caso del repository con una fixture VLM intermedia reale, in `data/test_inputs/vlm_raw/PROTEC_1_2pages.json`, ed è quello indicato come rischio principale in ADR-001 per l'aggregazione multi-pagina. Gli altri casi (SMA_1, PROTEC_2, SIEMENS_2, SMI_1, SMI_2) hanno output del pytool in `tests/single_pdf_outputs/` ma nessuna fixture VLM intermedia, quindi non sono riproducibili a partire dal solo input.

Portarli qui richiede prima di recuperare le fixture VLM reali dai run cloud.

## Copertura del percorso multi-chunk

Nessuna fixture in questa cartella esercita il percorso di merge multi-chunk. Per i dettagli vedi [`caso_2_protec_1/README.md`](caso_2_protec_1/README.md), sezione "Come il fixture è stato realmente passato".

La copertura di quel percorso è affidata a `tests/test_multipage.py`, che usa fixture sintetiche costruite a mano e non dati reali. È la lacuna più importante da colmare.

## Avvertenza

Le fixture contengono dati di produzione, presi alla lettera: indirizzi IP reali e nomi di stazione dei clienti. Prima di pubblicare il repository o di usare questi file in un prompt vanno sanitizzati.

## Stato

Nessun test è stato eseguito contro il runtime MyHydra. Il confronto con il ground truth legacy è stato eseguito localmente ed è riportato in `caso_2_protec_1/`.
