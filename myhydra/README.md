# Nuovo progetto MyHydra

Questa è l'area di sviluppo per i workflow MyHydra correnti e nuovi. Il materiale storico resta in `../legacy/` e non va modificato.

## Struttura

```text
myhydra/
├── README.md
├── CHANGELOG.md
├── single_pdf/                      # un PDF → JSON ADAS
│   ├── README.md                    # scopo, flusso, nodi, regole di stazione, rischi
│   ├── flusso_cloud_osservato.md    # topologia osservata il 28/09, non implementata
│   ├── nodes/                       # una scheda per nodo, prefisso lv1_ o lv2_
│   ├── prompt/                      # prompt VLM versionati
│   ├── pytools/                     # script Pytool versionati
│   └── test/                        # fixture e risultati per caso
└── double_pdf/                      # coppia di PDF IOL + JOB
    ├── README.md                    # Livello 1 e Livello 2 in un documento unico
    ├── nodes/                       # una scheda per nodo, prefisso lv1_ o lv2_
    ├── prompts/                     # prompt VLM versionati
    ├── pytools/                     # script Pytool versionati
    └── tests/                       # fixture e risultati per caso, casi 6
```

I due workflow sono rami paralleli: non condividono nodi, prompt, script né test. Le schede dei nodi portano il prefisso `lv1_` o `lv2_` perché ciascun workflow ha due livelli e i due non vanno confusi.

La distinzione fra i due livelli è nella struttura logica e nel nome dei file, non in directory separate: ogni workflow è autosufficiente in una cartella.

## Regole di documentazione

- Ogni nodo ha una scheda con scopo, input, output, configurazione, collegamenti, stato e punti da confermare.
- I prompt e gli script hanno file propri, versioni esplicite e riferimenti dalle schede dei nodi.
- Gli output di test distinguono i dati osservati dai risultati attesi derivati.
- Le chiavi Medex copiate negli esempi vengono sostituite con chiavi sintetiche: quelle runtime sono temporanee. Si conserva la struttura, compresa la finestra sovrapposta e il cambio di prefisso al confine delle sorgenti.
- Ogni comportamento non ancora osservato viene marcato `DA CONFERMARE`, senza trasformarlo in un requisito.
- Le schede dei nodi che non fanno parte della catella attiva sono marcate `backlog` nel nome del file e spiegano perché non servono.
- Quando prompt e script sono mantenuti anche in `src/`, la copia in `myhydra/` è byte-identica e il relativo README riporta l'hash atteso, così il disallineamento è verificabile.

## Stato attuale

**Single PDF.** Prompt v13 e pytool `json_creator.py` v4.3 in `src/`; la copia in `single_pdf/pytools/` è ferma a v4.2 (bloccante A2 in [`single_pdf/PENDENZE.md`](single_pdf/PENDENZE.md), da sincronizzare dopo A1). Stato verificato e registro in [`single_pdf/PENDENZE.md`](single_pdf/PENDENZE.md). Il flusso è completo su carta ma non è mai stato eseguito sulla piattaforma con il prompt v13. La lacuna principale è l'aggregazione multi-pagina del motore iterativo, mai verificata su dati reali. BISON e linearizzazione sono bloccate in attesa di specifiche del cliente. Dettagli in [`single_pdf/README.md`](single_pdf/README.md).

**Double PDF.** Caso 6: catena completa LV1→LV2→consolidatore cablata su canvas (filtri, 3 VLM Measurement + tagger, assemblatore per pagina, `CONSOLIDA PRE-JSON CREATOR`); meccanica verificata, qualità in attesa della run Qwen 3.8 del consolidatore. Stato di progettazione in [`double_pdf/WORKFLOW_DESIGN.md`](double_pdf/WORKFLOW_DESIGN.md), fixture in [`double_pdf/tests/case_6/outputs/`](double_pdf/tests/case_6/outputs/).

**Avvertenza comune.** Le fixture di entrambi i workflow contengono dati di produzione presi alla lettera, indirizzi IP e nomi di clienti. Vanno sanitizzate prima di pubblicare il repository o di usarle in un prompt.

## Riferimenti

Per la panoramica architetturale e le decisioni aperte:

- [`../docs/architettura/ADR-001-merge-multi-page.md`](../docs/architettura/ADR-001-merge-multi-page.md) — la decisione che ha definito l'architettura del Single PDF
- [`../docs/architettura/double_pdf_workflow_proposta.md`](../docs/architettura/double_pdf_workflow_proposta.md) — proposta del Double PDF
- [`../docs/architettura/single_pdf_cloud_corrente.md`](../docs/architettura/single_pdf_cloud_corrente.md) — il flusso cloud osservato, riassunto in [`single_pdf/flusso_cloud_osservato.md`](single_pdf/flusso_cloud_osservato.md)
