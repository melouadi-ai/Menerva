# Nodo LV1-07 — JSON CREATOR ADAS

- **Tipo/nome canvas:** Pytool `JSON CREATOR` (nodo 12, non iterativo, ultimo della catena).
- **Posizione:** dopo il nodo 11 `PREPARAZIONE X JSON`; uscita verso il Naive 13 `OUTPUT` (edge `#14`).
- **Input:** chunk intermedio dal nodo 11 via edge `#13` (verificato 05-10-2026).
  Riga da impostare nello script: `raw = r'''{edge}[13]'''.strip()`.
  Dopo ogni ricablaggio aggiornare il numero con quello reale del filo 11→12.
- **Script:** **NON è** `src/nodes/json_creator.py`. La copia incollata nel nodo 12
  è una variante ridotta: sulle misure analogiche emette `LOWCRITICAL/HIGHCRITICAL/
  LOWRANGE/HIGHRANGE/LOWOFFSET/HIGHOFFSET/SQ* = null`, mentre il repo e tutti e
  quattro i ground truth legacy emettono il sentinel `-3.40282e38` / `+3.40282e38`.
  Una versione ancora più vecchia (`observed_adas_case6_qwen38_serie.json`) non
  aveva addirittura le chiavi. Verificato il 05-10-2026 confrontando tutte le
  fixture Double con le quattro Single e con i GT.
  **Da fare:** riallineare il nodo 12 a `src/nodes/json_creator.py` v4.4
  (stessa versione del Single PDF: i due flussi condividono solo questo
  trasformatore finale, mai prompt né estrazioni) e rifare una run.
  Finché non è fatto, ogni output Double è un formato non validato: nessun
  Double PDF è mai stato importato in un ADAS reale.
- **Output atteso (caso 6, run 3.8):** lista con 1 stazione `Sistema Analisi SO2`
  (`10.100.50.95:511`), 22 misure (5 packed + 9 analogiche + 8 singoli),
  60 bitinfo; fixture in `tests/double_pdf_outputs/observed_adas_case6_qwen38.json`.
- **Serie canvas 3.8 (5/10):** `tests/double_pdf_outputs/observed_adas_case6_qwen38_serie.json`
  (22 misure + 60 bitinfo, linkage intatto, self-check silenzioso; stazione
  `SME` di default in questa run; PM-302A/B posizionali 0/1 da risolvere in review).
- **Verdetto caso 6 (5/10):** 22/22 registri e 60/60 bit conformi al PDF IOL,
  `DATA_TYPE` applicato (QAL3 `INT` → formato 150 contro 250 del legacy).
  Verità PDF e test in `tests/test_adas_caso6_pdf_truth.py`.
- **Verdetto caso 7 (5/10):** 39 misure e 47 bit attesi dal PDF IOL, output
  39 + **42**. Le 5 righe mancanti sono i bit 3–7 di REG 4, la cui cella `REG`
  è unita e **attraversa il confine di pagina**: a pagina 3 la colonna è
  visivamente vuota, il VLM restituisce `modbus_register: null` e il pytool
  scarta la riga (`VARIABILI SENZA INDIRIZZO`). Verità e test in
  `tests/test_adas_caso7_pdf_truth.py`.
- **Note:** `MEASUREID` nei bitinfo = ID sequenziale della misura (disegno v4.x,
  link relazionale intatto; il legacy usava il registro). `TEXTON` nulli in
  ingresso diventano `ATTIVO/OFF` per convenzione documentata.
- **Anomalia nota (run leggera 5/10, CHIUSA):** 6 ID packed-range nei bitinfo contro
  5 misure packed → 14 righe riattribuite. Causa: paste non identica al repo nel
  nodo 12, non il codice (il linkage è strutturalmente garantito: gli ID
  nascono insieme). Re-paste byte-identica verificata con nuova run leggera:
  6 packed (reg 1,3,4,5,6,7) + linkage intatto, nessun warning. Il self-check
  `BITINFO NON COLLEGATI` in `_warnings` sorveglia d'ora in poi. Estratto
  verificato in `tests/double_pdf_outputs/observed_adas_case6_light.json`.
