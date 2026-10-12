# Caso di prova 9 — Ospedale San Marco Catania

Coppia `IOL.0007.18.02` (7 pp) + `JOB.0007.18` (21 pp). Fogli GV2 (pp2–4) +
GV3 (pp5–7) in un'unica DB100. Verità pre-run in
[`../../PDF per il confronto/Ospedale San Marco Catania/VERITA_PRE_RUN.md`](../../PDF per il confronto/Ospedale San Marco Catania/VERITA_PRE_RUN.md).

## Attesi (dalla scheda pre-run del 12/10)

- **33 misure, 45 bitinfo, 0 stimate** (XTM 481–496 tutte bianche).
- Packed 1/3/4/81 · REAL 17/19/21/33 + 97/99/101/113/125 · SET 409–412 + 457–460 ·
  CMD 417/418/419/424/425/429/430/431/432 + 478/479/480.
- Scale JOB Tab 13: CO 0–600 (200/250), NO 0–500 (100/125), O2S, TF.
- **Aperti**: n. stazioni (JOB: 2 PLC) · mismatch numerazione `0007.18`/`0187.25`.

## Output

In attesa della run: fixture in `outputs/`, test di verità in
`../test_adas_caso9_pdf_truth.py` (da scrivere all'arrivo).
