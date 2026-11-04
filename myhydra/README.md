# MyHydra — i workflow in sviluppo

Area di sviluppo dei workflow MyHydra **correnti**. Il materiale storico resta
in [`../legacy/`](../legacy/): è read-only e non va modificato.

```text
myhydra/
├── README.md
├── CHANGELOG.md
├── single_pdf/                      # un PDF → JSON ADAS
│   ├── README.md                    # stato, flusso, contratto di pagina, rischi
│   ├── PENDENZE.md                  # registro storico delle verifiche + voci aperte
│   ├── prompt/                      # SOLO i 2 prompt correnti (UNIFIED, ORACOLO)
│   ├── pytools/                     # 6 script correnti, ognuno documentato + canvas
│   ├── nodes/                       # una scheda per nodo, prefisso lv1_ o lv2_
│   ├── platforms/                   # documenti di cablaggio canvas (lv1, lv2)
│   ├── pdf_input/                   # gli 8 PDF di riferimento
│   ├── verifica_pdf/                # verità PDF per caso, gate, confronti
│   ├── archive/                     # versione precedente: solo riferimento
│   └── TESTS/                       # artefatti delle run (ignorata da git)
└── double_pdf/                      # coppia di PDF IOL + JOB
    ├── README.md
    ├── WORKFLOW_DESIGN.md
    ├── nodes/
    ├── platforms/                   # per subplatform: prompt e script
    └── tests/                       # fixture e risultati per caso
```

I due workflow sono rami paralleli: **non condividono nodi, prompt, script né
test**. Le schede dei nodi portano il prefisso `lv1_` o `lv2_` perché ciascun
workflow ha due livelli, e i due livelli non vanno confusi.

## La regola della struttura (dal 4 novembre 2026)

> Fuori da una cartella `archive/` c'è solo materiale che si incolla o si
> esegue **oggi**. Dentro `archive/` c'è materiale che **non si incolla e non
> si esegue**: serve solo come riferimento di qualità da superare.

Conseguenze pratiche:

- Un prompt corrente esiste in due posti soli: `src/prompts/` (autorevole) e
  `myhydra/single_pdf/prompt/` (copia di paste, byte-identica).
- Uno script corrente esiste nella coppia `pytools/<nome>.py` (documentato) +
  `pytools/<nome>_canvas.py` (copia da incollare). Nessun altro posto.
- Lo storico dei prompt vive solo in `src/prompts/archive/`; la copia che era
  nel ramo MyHydra è in `single_pdf/archive/prompts_v13_v19/`.

Il dettaglio della riorganizzazione è in
[`../docs/architettura/RIORGANIZZAZIONE_2026-11-04.md`](../docs/architettura/RIORGANIZZAZIONE_2026-11-04.md).

## Regole di documentazione

- Ogni nodo ha una scheda con scopo, input, output, configurazione, collegamenti, stato e punti da confermare.
- I prompt e gli script hanno versioni esplicite e riferimenti dalle schede dei nodi.
- Gli output di test distinguono i dati **osservati** (`observed_*`) dai risultati **attesi** derivati (`expected_*`, `ATTESI_*`).
- Le chiavi Medex copiate negli esempi vengono sostituite con chiavi sintetiche: quelle runtime sono temporanee. Si conserva la struttura, compresa la finestra sovrapposta e il cambio di prefisso al confine delle sorgenti.
- Ogni comportamento non ancora osservato viene marcato `DA CONFERMARE`, senza trasformarlo in un requisito.
- Quando un prompt o uno script è mantenuto anche in `src/`, la copia in `myhydra/` è byte-identica e il README riporta l'hash atteso, così il disallineamento è verificabile.
- Gli indici `{edge}[N]` sono **locali al canvas**: vanno riletti a ogni rewiring. Un indice sbagliato non produce errori, produce un nodo blank.

## Stato attuale

**Single PDF (redesign v2).** Due prompt (`UNIFIED`, `ORACOLO`), `PAGE ASSEMBLER`
e `ORACLE_APPLY`, creator v15 con audit dell'oracolo. Canvas cablato (LV1: 16
nodi, LV2: 5). Prima run di collaudo in corso su PROTEC_2. Suite verde: 251 test
root + 84 Double. Non ancora importato in ADAS reale. Decisioni cliente aperte:
BISON, zeri iniziali, regola V2, nome stazione. Dettagli in
[`single_pdf/README.md`](single_pdf/README.md) e
[`single_pdf/PENDENZE.md`](single_pdf/PENDENZE.md).

**Double PDF.** Catena LV1→LV2→consolidatore→ADAS verificata end-to-end sui
casi 6 e 7 con Qwen 3.8: caso 6 = 22 misure + 60 bitinfo, registri
40001–40441; caso 7 = 40 misure + 47 bitinfo, 47/47 bit del PDF. Restano i
fattori `Dividere x10`, le due scale O2 senza unità, il nome stazione variabile
e nessun output Double importato in ADAS reale. Stato in
[`double_pdf/WORKFLOW_DESIGN.md`](double_pdf/WORKFLOW_DESIGN.md).

**Avvertenza comune.** Le fixture di entrambi i workflow contengono dati di
produzione presi alla lettera: indirizzi IP e nomi di clienti. Vanno sanificate
prima di pubblicare il repository o di usarle in un prompt.

## Riferimenti

- [`../docs/architettura/ADR-001-merge-multi-page.md`](../docs/architettura/ADR-001-merge-multi-page.md) — la decisione che ha definito l'architettura del Single PDF
- [`../docs/architettura/RIORGANIZZAZIONE_2026-11-04.md`](../docs/architettura/RIORGANIZZAZIONE_2026-11-04.md) — la mappa della struttura corrente
- [`../docs/architettura/double_pdf_workflow_proposta.md`](../docs/architettura/double_pdf_workflow_proposta.md) — proposta del Double PDF
- [`../docs/architettura/single_pdf_cloud_corrente.md`](../docs/architettura/single_pdf_cloud_corrente.md) — il flusso cloud osservato
