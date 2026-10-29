# Gate di accettazione output finale — Single PDF (v3 completo)

Ogni `FINALE` passa di qui prima di avanzare. Niente passa con silenzi:
ogni riga del PDF è dentro l'ADAS oppure ha una motivazione scritta.
Strumento: `myhydra/single_pdf/verifica_pdf/verdetto_finale.py FINALE caso`.
Changelog in fondo: ogni regola ha una data e un motivo.

---

## 0. Protocollo run (precondizioni, bloccanti)

- **P0. Run intero dal nodo 1.** Mai ripartire dai nodi a valle: la cache
  della piattaforma riusa immagini e output VLM vecchi (due incidenti:
  documento compressori dentro PROTEC_2 e SUPERWATT). Sospetto cache se due
  finali di run diversi sono byte-identici nonostante paste/temperature
  cambiati.
- **P1. Un verdetto = 3 file di UN SOLO run**: `TAP_MERGE` (o `ABC.txt`) +
  `TAP_CONSOLIDATORE` (o `CONSOLIDATOR.txt`) + `FINALE`. Mai mescolare run.
- **P2. Prompt attesi nel run**: stati ≥ v19 (`checklist` presente nel tap),
  misure ≥ v16 (`checklist`/`righe_viste`), nomi ≥ v16 (V30), consolidatore
  con `stati_riallineati` + `xfound` + `desc_ok = (nb_desc is not None`
  + `xdigits` (veto cifre) + filtro nomi senza descrizione.
  Senza queste stringhe il run è vecchio: rifarlo.
- **P3. Taps salvati** in `myhydra/single_pdf/TESTS/<DOC> NUOVO/` (nuovo run =
  nuova cartella o conferma esplicita di sovrascrittura).

## 1. Copertura — ogni riga ha un destino (bloccante)

Per ogni riga della tabella verità (`per_caso/*/tabella_pdf.json`):
- **Coperta**: stesso registro (+bit per le digitali) e nome compatibile
  (normalizzazione: hyphen/underscore/spazi/case; troncamento 49 ammesso
  se il nostro è prefisso/suffisso fedele; refusi rispettati).
- **Scarto motivato** (solo queste voci, con prova):
  - V2: descrizione vuota/`/` o match esatto spare/header (lista in prompt).
  - V20: annotazione con `NO PC SME`/`NO SME`/`NOT USED`/`NON UTILIZZATO`.
  - V21: zona `INPUT_HW`/`OUTPUT_HW`/`*_HW` — SOLO con decisione cliente
    (questione F22 aperta: default = escluso).
  - `Riserva*`/`‐`-dash/backtick-spare: giudizio-spare documentato riga per riga.
  - Tabella verità troncata/normalizzata (underscore, 30 char, hyphen):
    noi abbiamo il testo intero e fedele.
- **Buco vero**: nient'altro. Ognuno con causa (VLM/mismatch) e piano
  (re-run/fix). Tolleranza: zero, salvo lista nominale approvata.

## 2. Stati — trascrizione esatta (bloccante dove la colonna esiste)

- `TEXTON`/`TEXTOFF` == cella PDF su OGNI riga con stato dichiarato.
- Fallback keyword SOLO a cella vuota/assente. Mai su cella piena.
- Documenti senza colonna stati (SMA/SIEMENS/LEGNANO/LUX): fallback
  intatto + zero righe stato emesse dal ramo (`STATE == 0` nel tap).

## 3. Igiene valori (bloccante)

- Zero junk: nessun TEXTON/TEXTOFF in `1`, `0`, `1 =`, `0=...`, `1=...`.
- Zero invenzioni: ogni bitinfo/misura ha controparte PDF (stesso
  registro+bit/nome). Zero stazioni/IP/registri estranei (spia cache).
- Bit solo da suffisso/N.Bit (V30): mai da coil/DBX. Verificare i bit
  dei gemelli COG2/COG3 (stesso pattern, esiti indipendenti).
- Nomi BITNAME/MEASURE interi: code troncate dal VLM (es. `Terminata`
  senza `CON ERRORI`) sono buchi, non stile.

## 4. Validità ADAS (bloccante)

BITNO 0-15 intero; TEXTON/TEXTOFF non vuoti; MEASUREID collegati a misure
esistenti; DRIVERPRIVATE con registro decodificabile; nomi ≤ 49 char
(limite ADAS, troncamento a valle ammesso solo qui); nessuna misura senza
registro salvo CALCOLATA/V15 (ANALOGICA, reg null dichiarato).

## 5. Warning parlanti (bloccante)

Il tap consolidatore DEVE mostrare, dove ricorrono i casi:
`stati_riallineati` (shift compensati), `stati_disallineati` (scarti con
dettaglio), `stati_orfani_utili` (orfani con valori, riga per riga),
`blocco_rows_vuoto` (rami silenti, con conteggio),
`sospetto_sottocampionamento` (pagine a zero stati),
`pagina_vuota_sospetta` (solo per pagine davvero vuote/note),
`bit_fuori_range`, `riga_disallineata`, `copia_reale_da_placeholder`.
 vietato: fallback senza warning corrispondente.

## 6. Regressioni automatiche (bloccante)

```sh
.venv/bin/python -m pytest -q                              # root
.venv/bin/python -m pytest myhydra/double_pdf/tests -q     # double
.venv/bin/python -m pytest tests/test_single_texton_recall.py -q  # pin
```
Pin mai in calo (ORI 33/45, PROTEC_1 29/36, PROTEC_2 22/22, SUPERWATT 47/59).
Nuovo pin replay quando un run porta tap nuovi.

## 7. Confronto pari (dove esiste l'output collega)

Stessa copertura; TEXTON diversi solo se motivati dal PDF
(es. nostro refuso fedele `Ossiegno` vs sua correzione `Ossigeno`: vinciamo
noi per V13). Mai peggiorare su una voce dove lui è pari al PDF.

## 8. Deviazioni note (non bloccano, restano scritte)

- HW dentro/fuori, BISON/limiti, V2-composti, zeri iniziali, nome stazione,
  IP default `127.0.0.1`: decisi col cliente, non dal verdetto.
- `NAME_MAX` 49 char: troncamento a valle documentato, non errore VLM.
- Legacy GT non è riferimento di qualità (ha errori propri): il PDF decide.

## 9. Scheda verdetto (obbligatoria per documento)

```
Doc:            Run del:      Tap: MERGE/CONS/FINALE (singolo run)
Righe: cop/___  Stati: ok/___  HW-spare motivati: ___
Buchi veri: __ (lista nominale + causa + piano)
Invenzioni: __  ADAS-invalidi: __  Junk: __
Suite: root __/ double __/ pin __/
Gate: PASS/FAIL   Verificatore: data
```

## Baseline (non scendere mai)

| Doc | Righe | Stati | Residuo noto |
|---|---|---|---|
| SMA_1 | 49/50 | n/a (0 stati) | buco H2O; 1 refuso corretto; 0 inv |
| PROTEC_1 | 45/45 | 36/36 | perfetto, 0 inv |
| PROTEC_2 | 39/39 | 22/22 | 1 refuso corretto; 0 inv |
| ORI_5 | 58/58 | 45/45 | 2 refusi corretti; 0 inv |
| SUPERWATT_8 | 114/131 (17 pag.4 + Diverter) | 59/59 | re-run pulito + decontaminare SME 1 |
| SIEMENS_2 | 233/431 + 195 motivati (3 buchi + 1 refuso) | n/a | HW al cliente; 0 inv |
| LEGNANO_6 | da verificare | n/a | — |
| LUXOTTICA_7 | da verificare | n/a | — |

---

## 10. Matrice per-campo (quanto la verità permette)

La verità è ricca su SMA/PROTEC/ORI/SUPERWATT, scarna su
SIEMENS/LEGNANO/LUXOTTICA (solo registro/bit/descrizione/pagina).
Si verifica solo dove la verità copre:

| Campo ADAS | Verità ricca | Come si verifica | Tolleranza |
|---|---|---|---|
| NAME/BITNAME | tutte | match §11 | — |
| DRIVERPRIVATE (reg) | tutte | registro esatto (V4/V22) | nessuna |
| BITNO | dove `bit` c'è | esatto dopo V23/V30 | nessuna |
| TEXTON/OFF | dove `stato` c'è | esatto (case-insens.) | nessuna |
| UNITS | SMA/ORI/SUP (13/110/142) | cella non-numerica as-is | `Unità`-header→null |
| scale eng | SMA/ORI/SUPERWATT | coppie ingegneristiche | null se assenti |
| DATA_TYPE | SMA/PROTEC/ORI/SUP | copia esatta colonna | mai dedotto |
| READ_WRITE | PROTEC/ORI/SUPERWATT/SMA | R/W da colonna | null se assente |
| TAG/ZONA | dove ci sono | verbatim, mai usati come nomi | null se assenti |
| limiti/BISON | aperti (cliente) | trascritti dove dichiarati | sentinelle documentate |

Mai verificare un campo contro verità vuota: assenza tabella ≠ errore nostro.

## 11. Normalizzazione nomi (spec esatta)

Nell'ordine: maiuscole; `‐`/`–`→`-`; `_`→spazio; `\xa0`→spazio;
collapse spazi; strip. Poi match se uguali, prefisso/suffisso (troncamento
49 ADAS), o contenimento con verità-alnum ≥ 12 char. Refusi PDF intoccabili.
Underscore reali del PDF restano underscore nel confronto contro verità
che li normalizza (PROTEC_1 `FID6_01`: vinciamo noi).

## 12. Stazioni e IP

Un IP vero per stazione; placeholder (`xxx`, `:`) mai fusi coi veri;
carry-over solo dentro stessa tabella; `127.0.0.1` ammesso solo come
default dichiarato (questione cliente aperta); nome stazione solo da
etichette S1, mai da Cliente/Impianto/città. Split `E1`/`E1 1`-style
accettato dove il PDF separa tabelle con/senza IP.

## 13. Catalogo warning (devono esserci quando ricorre il caso)

`stati_riallineati` (shift compensati, con `40->41`), `stati_disallineati`
(scarti, con descrizioni), `stati_orfani_utili` (orfani con valori),
`stati_orfani` (orfani nulli), `blocco_rows_vuoto` (conteggio),
`sospetto_sottocampionamento` (pagine a zero stati),
`pagina_vuota_sospetta` (solo pagine davvero vuote/note),
`riga_mismatch`, `riga_disallineata`, `descrizione_mismatch`,
`bit_register_mismatch`, `refuso_sospetto/maggioranza`, `registro_applicato`,
`copia_reale_da_placeholder`, `bit_fuori_range`, `scarto_V2/V20/V21`
(con motivazione letterale), `pagina_senza_numero`, `sequenza_buchi`,
`bit_offset_pagina` (pagina con N.Bit contato 1-based: una volta per
registro con `reg N: nomi-bit 1-based, bit riportati a 0`, e per il bit in
cima con `reg N: bit 16->15`; se compare e i bit emessi sono quelli del
PDF, la regola ha fatto il suo lavoro).
 vietato: TEXTON da fallback senza warning che lo dichiara.

## 14. Contaminazione e verità sospette (procedure)

- **Sospetto cache** (finale con descrizioni/IP fuori documento, o due run
  diversi byte-identici): run nullo, ripartire dal nodo 1, riverificare.
- **Verità sospetta** (underscore normalizzati, troncamenti 30 char,
  `OK` vs `EXT+TIME INTERLOCK`, registri legacy shiftati): NON allineare
  l'output alla tabella — vince il PDF, la tabella si annota in
  `PANORAMICA` (precedente: GT legacy con 18 bitinfo fantasma caso 6).
- **Confronto col GT legacy**: differenze mai colmate senza verifica sul PDF.

## 15. Changelog gate

- 2026-10-13 v1: G0–G9, scheda verdetto, baseline.
- 2026-10-14 v2: protocollo anti-cache P0, voci spare, deviazioni cliente.
- 2026-10-14 v3: matrice per-campo §10, normalizzazione §11, stazioni §12,
  catalogo warning §13, procedure §14.
- 2026-10-28 v4: P2 riconosce il consolidatore col veto cifre (`xdigits`)
  e l'invisibilità dei nomi senza descrizione.
- 2026-10-29 v5: §13 aggiunge `bit_offset_pagina` (pagina 1-based nel ramo
  nomi-bit, bit 16→15); la regola deve stare anche nella copia canvas, non
  solo in `src/` (divergenza scoperta il 29/10, ora pinnata da
  `render_canvas.py` e dal confronto dei cataloghi di regole).
