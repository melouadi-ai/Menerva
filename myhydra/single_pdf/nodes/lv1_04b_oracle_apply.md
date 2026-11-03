# Nodo LV1-04b — ORACLE_APPLY (nuovo, redesign v2)

- **Tipo/nome:** Pytool — applica le correzioni dell'oracolo al consolidato.
- **Input (due edge, ricontrollare N a ogni rewiring):**
  - `raw_c = r'''{edge}[6]'''` — il consolidato prodotto da `CONSOLIDATORE`
    (`{"stations", "warnings", "counters"}`);
  - `raw_v = r'''{edge}[7]'''` — l'output grezzo del motore (via `MERGE_ABC`
    o tap), che contiene una `verifica` per ogni pagina.
- **CONFIG:** ispezionare le impostazioni di **entrambi** gli edge a ogni
  rewiring (match-condition spurie = wire bloccato in silenzio).
- **Script:** [`../platforms/lv1/scripts/updated_pending_validation/oracle_apply_canvas.py`](../platforms/lv1/scripts/updated_pending_validation/oracle_apply_canvas.py)
  (copia canvas 6.410 byte; documentata in [`../pytools/oracle_apply.py`](../pytools/oracle_apply.py)).
  Riferimento della logica: `_oracle_apply` in `src/nodes/single_consolidator.py`.
- **Output:** stesso contratto del consolidatore (`{"stations", "warnings",
  "counters"}`) arricchito di `_audit_oracolo` sulle variabili toccate.
  Errori → ERROR JSON con `tb`, mai blank.
- **Posizione nella catena:** tra `CONSOLIDATORE` (LV1-04) e `JSON CREATOR`
  (LV1-05). Il creator non sa nulla dell'oracolo: riceve un consolidato
  già corretto.

## Cosa applica (e cosa no)

L'oracolo (`vlm_oracle_v1.md`) emette cinque categorie. Questo nodo ne
applica **solo due**, e solo nella forma "aggiungi" o "annulla":

| Categoria | Azione | `_audit_oracolo` |
|---|---|---|
| `mancanti` | aggiunge la variabile (descrizione verbatim, registro/bit dall'evidenza) | `{"azione": "aggiunta", "evidenza": ...}` |
| `unita_inventate` | `units = null` | `{"azione": "annullata", "campo": "units", "evidenza": ...}` |
| `junk_stati` | `state_on`/`state_off` → `null` | `{"azione": "annullata", "campo": "state_on", ...}` |
| `refusi_corretti` | **solo warning** (`oracolo_refuso`) | — |
| `ip_dichiarati_non_usati` | **solo warning** (`oracolo_ip`) | — |

**Mai sovrascrivere un valore esistente.** I refusi restano quelli del PDF
(V13: la fedeltà vince sulla correzione) e un IP dichiarato e non usato non
diventa mai una stazione inventata (B2).

Guardie:
- `evidenza` vuota → il difetto **non** si applica (`oracolo_evidenza_vuota`);
- descrizione già presente → nessun duplicato (`oracolo_duplicato`);
- nessuna `verifica` nell'input → il consolidato esce invariato;
- `assemble_warnings` delle pagine (da `PAGE ASSEMBLER`) entrano nel tap
  come `oracolo_assente` / `oracolo_input_assente`: un oracolo non
  collegato non può restare in silenzio.

## Perché è un nodo separato

La decisione iniziale era tenere l'apply dentro il consolidatore, ma la
copia canvas del consolidatore è a **34.113 byte** contro un limite di paste
di ~34.300 (34.365 = rosso certo). Aggiungere ~3 KB di logica avrebbe reso
il nodo rosso sul canvas. Il pytool separato tiene ogni script sotto
soglia e rende l'apply testabile da solo.

- **Riferimenti:** [`lv1_04_consolidatore.md`](lv1_04_consolidatore.md),
  [`lv1_05_json_creator.md`](lv1_05_json_creator.md),
  [`../verifica_pdf/BENCHMARK_GATE.md`](../verifica_pdf/BENCHMARK_GATE.md)
  (§13-bis, regole §16-18).
