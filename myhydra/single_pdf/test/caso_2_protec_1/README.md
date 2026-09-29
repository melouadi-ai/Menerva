# Caso di prova 2 — PROTEC 1

Caso `Mappatura_2_Cliente_PROTEC_1`, unico caso del repository con una fixture VLM intermedia reale. È il caso citato come rischio principale in ADR-001: l'aggregazione multi-pagina del nodo iterativo non è mai stata verificata su un PDF reale.

## Input

| File | Ruolo |
|---|---|
| [`inputs/vlm_raw_PROTEC_1_2pages.json`](inputs/vlm_raw_PROTEC_1_2pages.json) | Output VLM delle 2 pagine: 30 variabili `DIGITALE_IMPACCATO` nella pagina 1 (IP assente), 15 variabili nella pagina 2 (`ip=192.168.0.1`, `port=502`, `modbus_id=1`). |
| [`inputs/riferimento_legacy_adas_PROTEC_1.json`](inputs/riferimento_legacy_adas_PROTEC_1.json) | Payload ADAS prodotto dal vecchio MAS. Non è un formato atteso per v4.2: serve da riferimento per il confronto. |

## Output

| File | Ruolo |
|---|---|
| [`outputs/observed_json_creator_PROTEC_1.json`](outputs/observed_json_creator_PROTEC_1.json) | Esecuzione reale di `json_creator.py` v4.2 sul fixture. 2 stazioni (`SME` ID 1, `SME 1` ID 2), 3 + 7 misure, 30 + 8 bitinfo. |
| [`outputs/confronto_vs_legacy_PROTEC_1.txt`](outputs/confronto_vs_legacy_PROTEC_1.txt) | Report derivato, prodotto da `tests/compare_with_gt.py`. **Non è un output atteso**: è il risultato del confronto con il payload legacy. |

## Avvertenza sui dati

Queste fixture contengono dati di produzione presi alla lettera: indirizzi IP reali (`192.168.0.1`, `127.0.0.1`) e nomi di stazione dei clienti. Sono state copiate verbatim perché servono a riprodurre il comportamento reale. Se questi file finiscono in un repository pubblico o in un prompt, vanno sanitizzati.

## Come il fixture è stato realmente passato

Il run osservato ha ricevuto l'intero array JSON come **un unico chunk**:

```text
_meta.chunks_parsed    = 1
_meta.pages_processed  = 1
```

Questo significa che il percorso di **merge multi-chunk non è stato esercitato** da questa fixture. Lo script ha ricevuto `[{pagina1},{pagina2}]`, lo ha parsato come un array, e ha appiattito le due pagine in un'unica pagina logica con due stazioni.

Il percorso multi-chunk — forward-fill di `name`/`ip`/`port`/`modbus_id`, fusione delle stazioni con stesso IP, dedup del bitinfo, merge dei digitali impacchettati a cavallo di pagina — è coperto solo da `tests/test_multipage.py`, con fixture sintetiche, non da dati reali.

## Cosa mostra il confronto con il legacy

Il report contiene 40 righe di differenza. La maggior parte è **attesa**, essendo cambi di progetto deliberati, ma alcune richiedono attenzione.

### Divergenze attesse (modifiche di progetto)

**Nome delle misure impacchettate.** Nel GT legacy ogni misura packed prende il nome dell'ultima riga del registro; v4.2 usa `"Ingressi digitali N"`. Per questo lo strumento di confronto non riesce ad abbinare le misure e le riporta come 5 mancanti e 5 extra, pur essendo i registri gli stessi e in numero uguale (10 e 10).

**`TEXTOFF` di default.** Il legacy forzava `TEXTOFF = "OK"`; v4.2 usa `OFF` tramite la keyword table. Sono 38 righe su 40. La semantica cambia: `OK` significa "nessun problema", `OFF` significa "stato spento". **Da chiarire con il cliente quale sia il valore atteso.**

**`DRIVERPRIVATE` parola 4.** Il legacy vi scriveva l'ultimo bit elaborato, per esempio `0F000000` per il bit 15. È un artefato del loop legacy, che sovrascriveva il campo a ogni bit. v4.2 scrive sempre `00000000` e lascia il bit esclusivamente in `bitinfo.BITNO`, che è la scelta corretta.

**`ID` e `MEASUREID`.** Nel GT legacy `measures[].ID` e `bitinfo[].MEASUREID` valgono il numero di registro (40001, 40002…); in v4.2 sono sequenziali da 1 a N per stazione. Per questo `tests/compare_with_gt.py` ricostruisce il registro dal campo `DRIVERPRIVATE` invece di fidarsi dell'ID.

### Divergenze da esaminare

**`LIVE PLC` cambia tipo.** Nel GT è `DRIVERDATA=2`, `TYPE=1`, formato 150, cioè un digitale impacchettato. In v4.2 diventa `DRIVERDATA=0`, `TYPE=0`, formato 250, cioè un'analogica. La causa è la **guardia B** del pytool, che tratta `LIVE PLC` come keyword di stato e la forza ad analogica. Verificare se la misura vada letta come analogica o come digitale.

**2 bitinfo mancanti sul registro 40007, bit 10 e 11** (`OVF MISURA DISPONIBILE IW36`, `OVF MISURA DISPONIBILE IW38`). Non sono andati persi: nel v4.2 sono diventati le analoghe `MISURA DISPONIBILE IW36` e `MISURA DISPONIBILE IW38`, rispettivamente sui registri 40016 e 40020. È la stessa riclassificazione della guardia B.

**4 unità di misura mancanti.** Nel GT le misure `COT_01`, `COT_02`, `DISPONIBILE IW36`, `DISPONIBILE IW38` hanno `UNITS = "mg/Nm3"`; in v4.2 sono `null`. Verificato: il dato **manca già nel fixture VLM**, dove `units` è `null` su tutte e quattro. Non è il pytool a perderlo, è l'estrazione a non averlo colto. Se il GT è corretto, il prompt va rafforzato sulla cattura delle unità.

**Refuso in un `TEXTON`.** Lo stato di `RICHIESTA MANUTENZIONE FID6_01` compare come `RCHIESTA MNAUTENZIONE`, con due lettere spostate. Verificato nel fixture: il campo `state_on` della riga 40001 bit 2 contiene già `'Richiesta Mnautenzione'`, cioè il refuso è nella lettura del VLM e il pytool lo ha copiato fedelmente. Che sia un difetto di estrazione e non di post-processing è dimostrato dalla riga adiacente, 40001 bit 6, che contiene la stessa frase letta correttamente come `'Richiesta Manutenzione'`. È un limite dell'estrazione visiva, non dello script.

## Come rigenerare il confronto

Dalla radice del repository:

```sh
python3 tests/compare_with_gt.py \
  tests/single_pdf_outputs/"Output PROTEC 1.txt" \
  --gt data/test_outputs/Json_2_Cliente_PROTEC_1.json
```

## Stato

Il confronto è stato eseguito localmente il 29/09/2026 ed è riportato sopra. Nessun test è stato eseguito contro il runtime MyHydra: la verifica sulla piattaforma resta da fare.
