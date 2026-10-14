# Gate di accettazione output finale — Single PDF (v2 estensivo)

Ogni `FINALE` passa di qui prima di avanzare. Niente passa con silenzi:
ogni riga del PDF è dentro l'ADAS oppure ha una motivazione scritta.
Strumento: `myhydra/single_pdf/verifica_pdf/verdetto_finale.py FINALE caso`.

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
  con `stati_riallineati` + `xfound` + `desc_ok = (nb_desc is not None`.
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
| SMA_1 | 48/50 | n/a (0 stati) | H2O, Polveri TQ; refuso fedele |
| PROTEC_1 | 45/45 | 36/36 | — |
| PROTEC_2 | 39/39 | 22/22 | — |
| ORI_5 | 58/58 | 45/45 | — |
| SUPERWATT_8 | 114/131 + pagina 4 + decontaminare SME 1 | 59/59 | re-run pulito |
| SIEMENS_2 | 232/431 + 195 motivati | n/a | 40011.6/7, 40017.15, MMC?, Riserva; HW al cliente |
| LEGNANO_6 | da verificare | n/a | — |
| LUXOTTICA_7 | da verificare | n/a | — |
