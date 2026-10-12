# Verità pre-run — Ospedale San Marco Catania (12/10/2026)

Coppia `IOL.0007.18.02` (7 pp) + `JOB.0007.18` (21 pp). Scheda scritta **prima**
della run: al suo arrivo, confronto immediato.

## ⚠️ Mismatch di numerazione (non bloccante)

Il file si chiama `IOL.0007.18.02` ma dentro dichiara `IOL.0187.25`
(14 occorrenze contro 0). Il JOB richiama `.01` e `.02`: la coppia è giusta
per riferimento, l'intestazione è stale/rinumerata. Qui **abbiamo solo la .02**;
la .01 (caldaie) manca. Fogli GV2 (pp2–4) + GV3 (pp5–7) in un'unica DB100.

## Attesi (corretti dopo la run1: due errori di lettura nella scheda pre-run)

- **35 misure**: packed 1/3/4/81 (150/1/2) · REAL 17 CO, 19 NO, 21 O2 Secco,
  33 Temp. fumi + 97 CO, 99 NO, 101 O2 Secco, 113 Temp. fumi, 125 Portata gas (250) ·
  SET 401, 402, 409–412 + 457–460 (medie/tempi, 150) · CMD 417, 418, 419, 424, 425, 429, 430, 431, 432
  + 478, 479, 480 (150/6/5). **Zero stimate** (XTM 481–496 tutte bianche).
  (Pre-run: dimenticati SET 401/402 con titolo nel conteggio.)
- **50 bitinfo**: GV2 REG 1 bit 8–15 (8) · REG 3 bit 8, 9, 10, 11, 0, 1, 2, 3, 6, 7 (10:
  anche Scansione 0–3, non viste in pre-run) ·
  REG 4 bit 8, 10, 11, 12, 13, 14, 0, 1, 2, 3, 5, 6 (12) · GV3 REG 81 bit 8–15 (8) ·
  12 comandi a bit 0. REG 2/82/83/84 tutti bianchi. (DBX 70.1 senza descrizione: esclusa.)
- **Stazioni: AMBIGUO** — uscita 1 stazione `.11` (caldaie) ma il JOB assegna
  questo IOL (`.02`) ai motori (`.21/.22`). Da sciogliere col cliente.
- **Scale JOB Tab 13 (motori)**: CO 0–600 (lim 200/250), NO 0–500 (100/125),
  O2S 0–25%, TF 0–600 °C. Warning attesi: CO + NO. Nessuna divisione
  (misure già in float ingegneristici, §5.5.3). O2 di riferimento 5%.
- **Nota join**: qui c'è `NO` (non `NOx`) e il TAG è identico — il join deve prenderlo.
