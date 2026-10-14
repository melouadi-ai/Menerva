# Gate di accettazione output finale (Single PDF)

Ogni finale, prima di passare oltre, deve superare TUTTI i punti sotto.
Strumento: `myhydra/single_pdf/verifica_pdf/verdetto_finale.py FINALE caso`.
Nessuna eccezione silenziosa: ogni scarto ha regola, artefatto o decisione.

## G0 — Tap completi (bloccante)
Un verdetto = 3 file di UN SOLO run: `TAP_MERGE` + `TAP_CONSOLIDATORE` +
`FINALE`. Mai mescolare run diversi. Con prompt ≥ v19 il merge deve
contenere `checklist` (prova che i VLM hanno girato davvero).

## G1 — Copertura motivata al 100% (bloccante)
`contabile (coperte+motivate) == tot righe verità`. Le motivate sono solo:
V2 (vuote/spare/header), V20 (nota NO SME...), V21 (zona _HW),
verità troncata/normalizzata (underscore, 49 char, hyphen),
giudizio-spare documentato riga per riga. Righe `BUCO` vere: zero,
oppure lista nominale con causa (VLM/mismatch) e piano (re-run/fix).

## G2 — Stati esatti (bloccante dove il PDF ha la colonna)
`TEXTON == stato PDF` su OGNI riga con stato dichiarato. Fallback keyword
solo dove la cella stato è vuota/assente, mai dove è piena.

## G3 — Zero junk (bloccante)
Nessun TEXTON/TEXTOFF in `1`, `0`, `1 =`, `0=...`, `1=...`.

## G4 — Zero invenzioni (bloccante)
Ogni bitinfo/misura ha controparte nel PDF (stesso registro+bit / nome).
Nessuna stazione, IP o registro estraneo al documento (contaminazione
da cache = run da rifare dal nodo 1, mai da valle).

## G5 — Validità ADAS (bloccante)
BITNO 0-15, TEXTON/TEXTOFF non vuoti, MEASUREID collegati, DRIVERPRIVATE
sani, nomi ≤ 49 char. Unico import reale in ADAS resta il test finale.

## G6 — Nomi fedeli
Match normalizzato (hyphen/underscore/spazi/case); refusi del PDF
rispettati (`Ossiegno` resta `Ossiegno`); V19-cleanup solo bordi.

## G7 — Warning parlanti (bloccante)
Nessun fallback silenzioso: pagine senza stati → `sospetto_sottocampionamento`
o `blocco_rows_vuoto`; shift → `stati_riallineati`/`disallineati`;
junk scartato senza TEXTON sporchi.

## G8 — Suite verdi (bloccante)
`.venv/bin/python -m pytest -q` (root) +
`.venv/bin/python -m pytest myhydra/double_pdf/tests -q` +
pin recall `tests/test_single_texton_recall.py` mai in calo.

## G9 — Parità collega (dove esiste il suo output)
Stessa copertura; differenze TEXTON solo se motivate da PDF.

## Baseline attuali (non scendere)
| Doc | Righe | Stati | Note |
|---|---|---|---|
| SMA_1 | 48/50 (buchi: H2O, Polveri TQ) | n/a | 1 refuso fedele |
| PROTEC_1 | 45/45 | 36/36 | — |
| PROTEC_2 | 39/39 | 22/22 | — |
| ORI_5 | 58/58 | 45/45 | — |
| SUPERWATT_8 | 114/131 + 5 estranee DA TOGLIERE | 59/59 | re-run pulito atteso |
| SIEMENS_2 | 232/431 + 195 motivati | n/a | 4 buchi noti, HW al cliente |
| LEGNANO_6 | da verificare | n/a | — |
| LUXOTTICA_7 | da verificare | n/a | — |
