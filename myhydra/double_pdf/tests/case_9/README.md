# Caso di prova 9 — Ospedale San Marco Catania

Quinta coppia: `IOL.0007.18.02` (7 pp) + `JOB.0007.18` (21 pp). Verità in
[`../test_adas_caso9_pdf_truth.py`](../test_adas_caso9_pdf_truth.py).

## Run1 (12/10): `outputs/observed_adas_case9_run1.json`

**35 misure, 50 bitinfo, 1 stazione, 1 warning. 100% delle righe con titolo.**

- Packed 1/3/4/81 · REAL 17/19/21/33 + 97/99/101/113/125 · SET 401/402/409–412 +
  457–460 · CMD 417/418/419/424/425/429/430/431/432 + 478/479/480. Zero stimate.
- Unità+range su CO/NO/O2/TF in entrambi i blocchi (NO collegato!); QG sentinel
  (scala non dichiarata, corretto). Warning: 4 limiti (CO×2, NO×2).
- La scheda pre-run aveva due errori di lettura (SET 401/402 dimenticati, righe
  Scansione 0–3 non viste): ragione l'output, corretti in `VERITA_PRE_RUN.md`.

## Punti aperti (pinnati nei test, da sciogliere)

1. **IP stazione ambiguo**: uscita `.11` (PLC caldaie) ma il JOB assegna questo
   IOL (`.02`) ai motori (`.21/.22`). Foglie, intestazione e Station si
   contraddicono: decide il cliente/pianta, non il PDF.
2. **DRIVERDATA=1** su Ack/Scansioni/Superi GV2 (5 comandi): inferenza R/W del VLM,
   incoerente tra run. Regola `comandi = W` da valutare (prompt o BISON).
3. **TEXTON supero incoerenti nella stessa run**: ALLARME (GV2) vs eco del nome
   (GV3). Convenzione da cliente, con COMANDO (Rivoli).
4. Mismatch numerazione `.02`/`0187.25`, `.01` mancante.
