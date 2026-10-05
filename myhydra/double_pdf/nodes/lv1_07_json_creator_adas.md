# Nodo LV1-07 — JSON CREATOR ADAS

- **Tipo/nome canvas:** Pytool `JSON CREATOR` (nodo 12, non iterativo, ultimo della catena).
- **Posizione:** dopo il nodo 11 `PREPARAZIONE X JSON`; uscita verso il Naive 13 `OUTPUT` (edge `#14`).
- **Input:** chunk intermedio dal nodo 11 via edge `#13` (verificato 05-10-2026).
  Riga da impostare nello script: `raw = r'''{edge}[13]'''.strip()`.
  Dopo ogni ricablaggio aggiornare il numero con quello reale del filo 11→12.
- **Script:** `src/nodes/json_creator.py` v4.3 canvas-safe (senza `def`/`lambda`,
  verificato con 13 test root). Stessa versione del Single PDF: i due flussi
  condividono solo questo trasformatore finale, mai prompt né estrazioni.
- **Output atteso (caso 6, run 3.8):** lista con 1 stazione `Sistema Analisi SO2`
  (`10.100.50.95:511`), 22 misure (5 packed + 9 analogiche + 8 singoli),
  60 bitinfo; fixture in `tests/double_pdf_outputs/observed_adas_case6_qwen38.json`.
- **Note:** `MEASUREID` nei bitinfo = ID sequenziale della misura (disegno v4.x,
  link relazionale intatto; il legacy usava il registro). `TEXTON` nulli in
  ingresso diventano `ATTIVO/OFF` per convenzione documentata.
