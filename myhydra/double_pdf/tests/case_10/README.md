# Caso di prova 10 — Essity (Collodi)

Quarta coppia: `IOL.0188.25` (9 pp) + `JOB.0188.25` (22 pp). Verità in
[`../test_adas_caso10_pdf_truth.py`](../test_adas_caso10_pdf_truth.py).

## Particolarità: due layout in un IOL

Pp2–5 mappa DB50 (colonne TAG|DESC|STRUCT|BIT|TIPO|DBX, **senza colonna REG**),
pp7–9 mappa DB100 classica (REG|BIT). Solo la DB100 è la mappa di scambio ADAS.

## Run1 (12/10): `outputs/observed_adas_case10_run1.json`

**23 misure, 24 bitinfo, 1 stazione, 2 warning.**

- **DB100 perfetta**: 20/20 misure e 24/24 bit riga per riga; stazione dichiarata
  + `192.168.1.1:511`; gateway/DCS/PC/MIR ignorati; limiti CO 300/375 ×3.
- **Difetto nuovo**: 3 misure AI-DB50 (CO, O2, TF) con registri 160/168/192
  **inventati dai DBD** — la mappa DB50 non ha colonna MODBUS (verificato sulle
  coordinate), quindi andavano scartate. Il controllo non le prende perché il
  registro è diverso da null/0. Fix nel prompt (REG solo da colonna REG).
- Le altre 18 righe DB50 senza REG sono scartate con warning: la guardia funziona.
- Pinnati: `FAILURE → ATTIVO` (sospetto), supero → `ALLARME` (terza variante,
  convenzione da cliente). `#RIF!` a pag 4 non ha sporcato.
