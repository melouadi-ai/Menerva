# Verità pre-run — Essity (12/10/2026)

Coppia `IOL.0188.25` (9 pp) + `JOB.0188.25` (22 pp), cartiera Essity Collodi (PT).
Scheda scritta **prima** della run: al suo arrivo, confronto immediato.

## Attesi

- **20 misure**: packed 1/3/4 (150/1/2) · REAL 17 CO, 21 O2 Secco, 33 Temp. fumi +
  INT 49 CO, 53 O2 Secco, 65 Temp. fumi · SET 409–414 (medie CO/NOx/NH3) ·
  CMD 417, 418, 425, 431, 432. **Zero stimate** (XTM non dettagliate nel doc).
- **24 bitinfo**: REG 1 bit 8–13 · REG 3 bit 8, 10, 11, 7 · REG 4 bit 8, 10, 13,
  0, 1, 2, 3, 5, 6 · 5 comandi a bit 0. REG 2 tutto bianco (niente packed).
- **Stazione**: `Sistema Analisi Emissioni`, `192.168.1.1:511`. Il gateway
  `192.168.10.250` NON deve generare nulla (trappola B2).
- **Scale JOB Tab 6**: CO 0–150 mg/Nm3 (lim 300/375!), O2S 0–25%, TF 0–200 °C.
  Warning atteso: solo LIMITI CO. Nessuna divisione (4–20 mA da riscalare).

## Rischi previsti (da verificare in `_warnings`/`review`)

1. **Pagine DB50 senza colonna REG** (pp2–5: TAG|DESC|STRUCT|BIT|TIPO|DBX,
   struct SB/ST2/HW4/HW20/AI/AO mai viste): se vanno a Measurement, il VLM
   deriva il registro da DBX o sporca. HW4/HW20 e XTM-DB50 sono tutte bianche.
2. **`#RIF!`** a pag 4 (riferimento Excel rotto): rumore VLM noto in anticipo.
3. **TEXTON nuovi**: `Failure`/`Fault analizzatore` — pinnare alla run.
4. Niente QAL nei comandi (solo `Start autocal`): coerente col JOB (non richieste).
