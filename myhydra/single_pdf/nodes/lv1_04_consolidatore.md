# Nodo LV1-04 — CONSOLIDATORE (nuovo, redesign v14)

- **Tipo/nome:** Pytool — unisce i 3 rami VLM per pagina e fonde le pagine.
- **Input:** array dei chunk per pagina accumulati dal nodo LV1-03, letto da `raw = r'''{edge}[6]'''`.
- **CONFIG:** il `6` è locale al canvas — **ricontrollare N a ogni rewiring** e ispezionare le impostazioni dell'edge (rimuovere match-condition spurie: un placeholder residuo blocca il wire in silenzio).
- **Script:** [`../platforms/lv1/scripts/updated_pending_validation/consolidator_canvas.py`](../platforms/lv1/scripts/updated_pending_validation/consolidator_canvas.py) (copia canvas, 34.058 byte, generata da `../pytools/render_canvas.py`; documentata in [`../pytools/consolidator.py`](../pytools/consolidator.py), riferimento testabile `src/nodes/single_consolidator.py`).
- **Output:** `{"stations": [...], "warnings": [...], "counters": {...}}` via `result`. Mai blank: in caso di errore `result` è un ERROR JSON `{"status": "ERROR", ...}`.
- **Posizione nella catena:** dopo il motore iterativo, prima del JSON CREATOR. È il nodo che rende il creator un trasformatore puro: il merge non è più dentro `json_creator.py`.

## Cosa fa, in ordine

1. **Join dei 3 rami per pagina** sulla chiave `riga` (misure + nomi-bit + stati). Righe orfane scartate con warning.
2. **Precedenza su disaccordo** (fissata qui, mai silenzio): nomi-bit vince bit/registro **solo a descrizioni concordi** (F1b), altrimenti tengono le misure + `riga_disallineata`; due rami contro uno ripristinano la versione fedele (`refuso_maggioranza`); misure tutto il resto, stati vince state_on/off **solo a descrizione concorde** (`stati_disallineati` altrimenti, mai applicati alla cieca). `riga_mismatch` emesso sempre quando gli insiemi `riga` dei rami divergono; righe stati senza measures → `stati_orfani` (mai ignorate in silenzio). Righe placeholder duplicate sulla reale → scartate dalla reale, tenute solo placeholder (`copia_reale_da_placeholder`, F2).
3. **Join scale per `tag`** (stesso tag, fallback `description == tag/tag+" Raw"`): solo riempimento dei null, mai sovrascrittura.
4. **Carry-over registro** per stazione in ordine di pagina (voce `registro_applicato`; solo digitali con bit; analogiche senza REG restano null).
5. **Fold packed** (singoli con registro condiviso → IMPACCATO) e scarti `classify_row` conteggiati per regola (vedi sotto).
6. **Buchi `page_no`** in `sequenza_buchi`; `pagina` riempita dal contatore motore se null; stazioni anonime fuse sotto chiave `("anon",)`, reali per IP esatto.
7. **Pagina 1-based nel ramo nomi-bit** (`bit_offset_pagina`): se tutte le righe confrontabili hanno nome = misura +1 e almeno un bit supera 15, la pagina è contata 1..16 mentre le misure scrivono 0..15. Valgono i bit delle misure, i nomi non decidono bit né descrizione, il 16 viene riportato a 15. Sui registri di quella pagina il gate di ancoraggio tace (altrimenti rimetterebbe lo shift appena tolto). Il flag interno non esce nel JSON.

## Filtri V2/V20/V21 (vivono qui, non in un nodo separato)

Non esiste un nodo filtri sul canvas: le regole di scarto sono codice inline in questo script (logica copiata alla lettera dai prompt v14, identica nei 3 rami; riferimento testabile `src/nodes/single_filters.py`):

- **V2**: match esatto case-insensitive dopo strip contro spare/placeholder e intestazioni di sezione (`Riserva INPUT` resta keep: è CONTAINS, non esatto).
- **V21**: `zona` con `INPUT_HW`/`OUTPUT_HW` o suffisso `_HW`.
- **V20**: annotazione (`note` + stessi alias dei filtri) contenente `NO PC SME`/`NOT USED`/ecc.

Ogni scarto è un warning con `reason` letterale e un contatore (`scarti_V2/V20/V21`), mai silenzio.

## Handoff a valle

Il creator (LV1-05) legge `stations` con `variables` in formato v14 (`description`, `units`, `modbus_register`, `bit`, `kind`, `data_type`, `zona`, `tag`, `pagina`, `riga`, scale, limiti, stati). Pipeline verificata localmente sui casi 40014/SMA/PROTEC/SIEMENS (`tests/test_single_regressions.py`, `tests/test_single_truth_siemens.py`).

- **Da confermare alla prima run:** che il nodo esponga `result` (convenzione corrente, mai eseguita sul canvas in questo flusso).
- **Riferimenti:** [`../platforms/README.md`](../platforms/README.md) (contratto I/O e checklist edge), [`lv1_05_json_creator.md`](lv1_05_json_creator.md), [`lv1_03_single_pdf_engine.md`](lv1_03_single_pdf_engine.md).
