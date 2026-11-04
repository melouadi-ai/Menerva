# Single PDF — documenti di cablaggio canvas

Questa cartella non contiene più script: dal 4/11/2026 le copie da incollare
vivono in un solo posto, [`../pytools/`](../pytools/README.md), dove accanto a
ogni copia canvas c'è la versione documentata. Le vecchie cartelle
`lv1/scripts/updated_pending_validation/` e `lv2/scripts/...` contenevano
duplicati byte-identici e sono state eliminate.

Qui resta la **conoscenza del cablaggio**: com'è fatto il canvas, quali edge
esistono, cosa controllare prima e dopo un rewiring.

## Mappa

- [`lv1/README.md`](lv1/README.md): catena LV1 (nodi, edge, indici, budget di paste).
- [`lv2/README.md`](lv2/README.md): i due VLM del redesign v2 e il `PAGE ASSEMBLER`.
- [`../verifica_pdf/BENCHMARK_GATE.md`](../verifica_pdf/BENCHMARK_GATE.md): gate di verifica (§13-bis).

## Contratto I/O dei Pytool — chiarito una volta sola qui

Due meccanismi di emissione, entrambi intenzionali. Non uniformare senza motivo.

| Nodo | Emissione | Errore | Stato verifica |
|---|---|---|---|
| `CONSOLIDATORE` | `result = json.dumps(...)` | ERROR JSON in `result`, mai blank | eseguito sul canvas (run di collaudo) |
| `ORACLE_APPLY` | `result = json.dumps(...)` | ERROR JSON in `result`, mai blank | eseguito sul canvas |
| `PAGE ASSEMBLER` | `result = json.dumps(...)` | ERROR JSON in `result`, mai blank | eseguito sul canvas |
| `SLICE-A/B/C` | `result = json.dumps(...)` | ERROR JSON in `result`, mai blank | eseguito sul canvas |
| `MERGE_AB/ABC` | `result = json.dumps(...)` | ERROR JSON in `result`, mai blank | eseguito sul canvas |
| `JSON CREATOR` v15 | `print(output)` + variabile `output` | `try/except` globale: stampa ERROR JSON, mai blank | meccanismo legacy verificato dal Double (nodo 12) |

Regola per il futuro: i nuovi Pytool usano `result` + ERROR JSON. Il creator
v15 resta `print`-based perché è il meccanismo che ha già funzionato sul
canvas; cambiarlo significherebbe cambiare il contratto di uscita del flusso.

## Checklist edge (il punto in cui i wire muoiono in silenzio)

Per **ogni** edge del flusso:

1. **Nessuna match-condition spuria.** Un placeholder residuo (visto:
   `pippo` su un edge filtro→iniezione nel Double) blocca il wire senza
   errori: il nodo a valle muore di fame (blank, non ERROR JSON).
2. **Tipo di edge corretto.** Gli edge media (`{edge.media}[N]`) devono
   partire dal ramo `@MEDIA`; gli edge testo (`{edge}[N]`) dal ramo testo.
   Un media letto come testo porta `null` a valle.
3. **Conteggio edge in uscita.** `MEDIA2CONTENT` → 3 (uno per SLICE);
   `CONTENT2MEDIA` → 2 (UNIFIED + ORACOLO); `MERGE_ABC` → 2
   (CONSOLIDATORE + ORACLE_APPLY).
4. **Indice riletto.** Ogni `{edge}[N]` è locale al canvas e cambia quando
   si aggiungono o spostano nodi: va riletto a ogni rewiring.

## Budget di paste

Misura empirica: 34.365 byte = rosso, 33.520 = verde (6–28 ottobre 2026).
Guardia di progetto: **< 34.300 byte**.

| Copia | Byte |
|---|---|
| `consolidator_canvas.py` | 34.113 |
| `json_creator_v15_canvas.py` | 25.299 |
| `oracle_apply_canvas.py` | 6.949 |
| `page_assembler_canvas.py` | 3.108 |
| `merger_canvas.py` | 1.980 |
| `slicer_canvas.py` | 905 |

Se una copia supera il budget non si edita a mano: si rigenera con
[`../pytools/render_canvas.py`](../pytools/render_canvas.py), che toglie i
commenti e verifica che l'AST resti identico.
