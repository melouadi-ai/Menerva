# Single PDF — TEXTON esatti dal PDF (prompt v16 + patch script)

Data: 2026-10-13. Stato: design approvato (§1–§3), da implementare.
Obiettivo: TEXTON/TEXTOFF = esattamente gli stati dichiarati nel PDF.
Mai inventati (junk filtrato), mai persi in silenzio (ogni fallback dichiarato).

## Contesto e baseline misurata

- Flusso: SLICE-A/B/C → 3 ENGINE VLM (misure, nomi-bit, stati) → MERGE-AB/ABC
  (flat, nessun envelope) → CONSOLIDATORE → CREATOR → finale Naive.
- Recall stati (TEXTON == stato PDF): PROTEC_1 61%, PROTEC_2 27%,
  ORI_MARTIN_5 71%, SUPERWATT_8 80%. SMA/SIEMENS/LEGNANO/LUX non hanno
  colonna stati: fallback keyword corretto.
- Collega: pari su SMA (30/30), avanti 12-0 su run ORI vecchia, pareggio
  sul run ORI nuovo (12/12 recuperate con trascrizione).
- Vincoli canvas: pytool standalone (no def/class/lambda, output `result`;
  il creator legacy usa `print`, non toccare), budget paste 33.792 byte
  (consolidator_canvas a 33.327: ogni aggiunta va compensata), edge `{edge}[N]`
  locali, niente tap/debug (diagnosi via warning in output).
- Suite: 156 root + 81 double verdi. Specchi `myhydra/` byte-identici a `src/`.

## §1 — Prompt v16 (3 contratti VLM, approvati)

1. Catalogo header di stato: `1 =`, `STATO ON`, `Logic State(1)`, `STATO 1/0`,
   `ON/OFF TEXT`, `Testo On/Off`, `ON`/`OFF`, `1`/`0` come header mai come
   valori, singola colonna `STATO`/`ALLARME`/`TESTO`. Una sola colonna stato
   non-nulla → `state_on`.
2. Check-key: i rami copiano esatto (V13 intatta); il join confronta
   normalizzato (stesso V19). Virgolette/parentesi vuote non causano più
   `stati_disallineati` spuri.
3. `riga`: intestazione tabella = 0 (non contata); ogni riga corpo dall'alto,
   incluse skippate/vuote, numerazione continua su pagina multi-tabella.
4. Conteggi: risposte stati con `"digitali_visti": N`. Retrocompatibile
   (consolidatore ignora chiavi ignote).
5. Buco V2→stati: descrizione vuota/skippata ma cella stato piena → emessa
   comunque (`description: null` + `riga`); se orfana, warning dedicato
   (in ADAS non entra senza registro: dichiarato).
6. Anti-junk: stato solo da colonna a destra di descrizione/unità; pagina
   senza header di stato → tutti `null`. Filtri codice restano come rete.

## §2 — Patch script (4 interventi, approvati)

- P1 pairing normalizzato (esatto → V19 → typo-pair; vince misure).
- P2 duplicati `riga`: vince chi matcha la descrizione misure, else
  first-wins + warning.
- P3 `stati_orfani_utili`: orfani con stati non-nulli dichiarati riga per riga.
- P4 budget: sfoltire ~1 KB prima di P1–P3 (stringhe, rami morti). Non toccare
  `print` del creator. Fuori scopo: envelope/tagging merger, `127.0.0.1`.

## §3 — Test e rollout (approvati)

- T1 pin recall (soglie attuali, mai peggiorare in silenzio).
- T2 unit: pairing normalizzato, duplicati riga, orfani utili, `digitali_visti`,
  P6 `"1 ="` isolato.
- T3 suite verdi a ogni passo, TDD rosso→verde.
- Rollout: paste prompt v16 + consolidatore; re-run PROTEC_2 → ORI →
  SUPERWATT → PROTEC_1 con verdetto finale-vs-PDF. Se il budget non rientra,
  P3 slitta a warning aggregato (dichiarato prima del paste).
