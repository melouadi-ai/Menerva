# Caso di prova 8 — Rivoli (CTM–Edison)

Terza coppia, mai vista prima del 12/10/2026: `IOL.0177.25` + `JOB.0177.25`
(centrale di cogenerazione di Rivoli TO). Verità nei PDF qui sotto, test in
[`../test_adas_caso8_pdf_truth.py`](../test_adas_caso8_pdf_truth.py).

## Input e risultato

- `IOL.0177.25.pdf`: 4 pagine (mappa DB100, impianto 1).
- `JOB.0177.25.pdf`: 23 pagine (specifica `Sistema Analisi Emissioni`).
- Run canvas fino al nodo 12: [`outputs/observed_adas_case8_run1.json`](outputs/observed_adas_case8_run1.json) —
  **27 misure, 37 bitinfo, 1 stazione, 1 warning**.

## Verdetto contro la coppia (12/10)

Tutto conforme al PDF riga per riga, tranne un punto:

- **Misure 27/27 e bit 37/37**: solo righe con titolo. REG 2 (16 righe tutte
  bianche) non produce nemmeno la packed — gli `Ingressi digitali` sono 1, 3, 4.
- **REG 4 tutto a pagina 2**: nessun carry-over oltre pagina, nessun bit perso
  (bit 4/7 assenti = righe bianche reali, non la perdita del caso 7).
- **Stazione dichiarata** `Sistema Analisi Emissioni`, IP PLC `192.168.1.1:511`;
  mask, PC SME e analizzatore correttamente ignorati.
- **Scale 5/6** (CO, O2, TF, QG, PWR con range reali); warning solo CO 120/150.
  Niente DIVISIONE — questo JOB non ne dichiara (§5.4.2).
- **Difetto noto**: NOx (reg 18) senza scala/unità/limiti — probabile TAG IOL
  `NO` contro `NOx` del JOB (join per TAG fallito). Stessa classe dei casi 6/7.
- **Pinnati**: TEXTON `COMANDO` sui due superamento (convenzione da fissare),
  `CO rferito` → `riferito` (politica refusi da decidere), stimata NOx con
  `ppm` dalla descrizione IOL.
