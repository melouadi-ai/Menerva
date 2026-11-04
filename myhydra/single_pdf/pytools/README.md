# Pytools — Single PDF (redesign v2)

Questa è **l'unica cartella** in cui vivono gli script del Single PDF. Accanto a
ogni versione documentata (con commenti) c'è la **copia canvas** senza commenti,
che è quella che si incolla nel nodo MyHydra. Dal 4/11/2026 non esistono più
copie in `platforms/*/scripts/`: erano duplicati byte-identici e duplicavano
anche la manutenzione.

## Inventario (6 coppie + 1 generatore)

| Documentato | Canvas (da incollare) | Nodo | Byte canvas |
|---|---|---|---|
| [`slicer.py`](slicer.py) | [`slicer_canvas.py`](slicer_canvas.py) | `SLICE-A/B/C` (LV1) | 905 |
| [`merger.py`](merger.py) | [`merger_canvas.py`](merger_canvas.py) | `MERGE_AB`, `MERGE_ABC` (LV1) | 1.980 |
| [`consolidator.py`](consolidator.py) | [`consolidator_canvas.py`](consolidator_canvas.py) | `CONSOLIDATORE` (LV1-04) | 34.113 |
| [`oracle_apply.py`](oracle_apply.py) | [`oracle_apply_canvas.py`](oracle_apply_canvas.py) | `ORACLE_APPLY` (LV1-04b) | 6.949 |
| [`json_creator_v15.py`](json_creator_v15.py) | [`json_creator_v15_canvas.py`](json_creator_v15_canvas.py) | `JSON CREATOR` (LV1-05) | 25.299 |
| [`page_assembler.py`](page_assembler.py) | [`page_assembler_canvas.py`](page_assembler_canvas.py) | `PAGE ASSEMBLER` (LV2-03) | 3.108 |

[`render_canvas.py`](render_canvas.py) non è un pytool da incollare: è il
generatore che produce ogni copia canvas dalla documentata (stesso AST,
1 spazio di indentazione per livello, commenti e righe vuote rimossi).

Le versioni del periodo precedente (`json_creator_v4_2`, `v4_4`, `v4_5`) sono in
[`../archive/pytools_v4/`](../archive/pytools_v4/): non si incollano.

## Sorgente autorevole

`src/` vince sempre.

| Script | Fonte autorevole | Rapporto |
|---|---|---|
| `json_creator_v15.py` | `src/nodes/json_creator.py` | **byte-identico** |
| `consolidator.py` | `src/nodes/single_consolidator.py` | stessa logica, versione inline adattata al canvas |
| gli altri | il file documentato **è** la fonte | nascono nel ramo MyHydra |

Hash correnti (verificabili con `sha256sum *.py`):

```text
429fb9bf871a0b18d5fff08897c32b11bd982f07bea289d0d87b0654a5900aaf  json_creator_v15.py   (= src/nodes/json_creator.py)
5c21f013b11d4886a65030f918feddc242487f3d3f32583e9f3806e252debc20  json_creator_v15_canvas.py
e9894934da6670a346bae9adc13fa5143bc1eb7b2c7578f8e967119b3a0f67dd  consolidator.py
8d3c7d67a9fca15a52be226526ee225cbc8f63f4e1b876c2edca9fd40d61e1cc  consolidator_canvas.py
ee61c0a7c075fed7e8c572d41d40c650889ca21d7eb9ad3473b47ff583a0bd82  oracle_apply.py
091718500bcc6a0c679de49fc09fd6e42c5f73bd236c6e618ab628d4eb298370  oracle_apply_canvas.py
822fe612d0958fc8b9c867259af9c26ad8e5a5b3f0857c6244f3314717a1f26c  page_assembler.py
7edd34825b1e8ef473077feeeafdddb037a87915bfb444761d54396e393e283b  page_assembler_canvas.py
6a0c7b7836fd35873a2e050005cdbfbccc88762b9d5e28705586657d8c92cbce  merger.py
50614896814d0f7c8d034d868235b9a9857e4973216d72017d14fe0609a2f347  merger_canvas.py
3b8faa4d4207179c3890b39b3872405c3232cc0c54a709dbfdf16be08a0baa4c  slicer.py
c008026276addcdc7cd06ca350647a44cfc29bc3930b82f1eb602bb5f19641a0  slicer_canvas.py
```

Se un hash diverge, il file autorevole è quello in `src/` (o il documentato):
si ricopia, non si edita la copia canvas a mano.

## Rigenerare le copie canvas

Mai modificare `*_canvas.py` a mano. Si modifica il documentato, poi:

```sh
.venv/bin/python myhydra/single_pdf/pytools/render_canvas.py           # verifica
.venv/bin/python myhydra/single_pdf/pytools/render_canvas.py --write   # riscrive
```

Il generatore verifica tutte le coppie e fallisce con codice 1 se una diverge.
La parità è pinnata anche da `tests/test_single_consolidator_canvas.py`,
`tests/test_single_shard_merger.py` e `tests/test_single_canvas_hygiene.py`.

## Budget di paste

Misura empirica: 34.365 byte = rosso, 33.520 = verde (6–28 ottobre 2026);
32.766 = verde. Guardia di progetto: **< 34.300 byte**, controllata da
`tests/test_single_canvas_hygiene.py`.

`consolidator_canvas.py` (34.113 B) è il più grande ed è già al limite: per
questo le regole dell'oracolo stanno in `oracle_apply_canvas.py` (6.949 B) e non
nel consolidatore. Se un domani una copia sfora, si spezza il nodo, non si
comprime il file.

## Contratto di emissione (non uniformare senza motivo)

| Nodo | Emissione | Errore |
|---|---|---|
| `SLICE-A/B/C`, `MERGE_AB/ABC`, `CONSOLIDATORE`, `ORACLE_APPLY`, `PAGE ASSEMBLER` | `result = json.dumps(...)` | ERROR JSON in `result`, mai blank |
| `JSON CREATOR` v15 | `print(output)` + variabile `output` | `try/except` globale: stampa ERROR JSON, mai blank |

Il creator resta `print`-based perché è il meccanismo già verificato sul canvas.
Cambiarlo significherebbe cambiare il contratto di uscita dell'intero flusso.

Tutti gli script sono **standalone**: niente `def`/`class`/`lambda`, nessun
import da `src.*`. Un `import src.models` fallisce sul canvas e la validazione
Pydantic viene saltata per progetto (`_pydantic_available = False`); la pipeline
prosegue identica. Non è un errore.

## Dettaglio dei singoli script

### `slicer.py` — SLICE-A/B/C

Divide l'array di pagine in tre shard (`START`/`END` in testa al file, una copia
per shard). Fuori portata restituisce `[]`: non è un guasto.

### `merger.py` — MERGE_AB / MERGE_ABC

Ricuce due array di pagine in uno. Due edge (`raw_a`, `raw_b`). In cascata:
`MERGE_AB` + `SLICE-C` → `MERGE_ABC`.

### `consolidator.py` — CONSOLIDATORE

Fonde le pagine e le stazioni in un unico consolidato, numerando gli ID.
Accetta anche l'output grezzo del motore. Ogni disaccordo e ogni scarto
V2/V20/V21 diventa un warning, mai silenzio. Config canvas: `{edge}[6]`.

### `oracle_apply.py` — ORACLE_APPLY

Applica le correzioni dell'oracolo al consolidato: **aggiunge** le variabili
mancanti, **annulla** unità inventate e stati junk. Refusi corretti e IP
dichiarati non usati restano **solo warning** (il PDF decide). Ogni variabile
toccata porta `_audit_oracolo {azione, campo, evidenza}`. Evidenza vuota → il
difetto non si applica. Due edge: `raw_c` (consolidato), `raw_v` (grezzo del
motore, che contiene `verifica` per pagina). Porta nel tap anche
`oracolo_assente` / `oracolo_input_assente`: un oracolo non collegato non può
restare in silenzio.

### `page_assembler.py` — PAGE ASSEMBLER

Vive nel **LV2**, dopo i due Visiomaru. Senza questo nodo l'output dell'oracolo
(le sole 5 categorie) non è né `stations` né `rows` e il consolidatore lo
rifiuta (`blocco senza stations ne rows`). Due edge: `raw_u` (UNIFIED),
`raw_o` (ORACOLO). Emette `{"page_no", "stations", "verifica"|null,
"assemble_warnings"}`.

### `json_creator_v15.py` — JSON CREATOR

Trasforma il consolidato nel JSON ADAS: `DRIVERPRIVATE`, `LOWRANGE`/`HIGHRANGE`,
limiti `limit_hour` → `SQ1HOURMEAN` e `limit_day` → `SQDAILYMEAN`, sentinel,
`XML`, `_meta`, `_warnings`, `_meta.audit_oracolo`.

## Contratto ADAS: divergenze dalla documentazione

`docs/contracts/ADAS_FINAL.md` descrive il formato `DRIVERPRIVATE` in modo che
non coincide col codice. Vale la pena conoscerle, perché chi legge solo il
contratto scriverà il prodotto sbagliato.

| Punto | Contratto | Codice |
|---|---|---|
| Lunghezza di `DRIVERPRIVATE` | 52 caratteri | **48** caratteri |
| Primo blocco di 8 hex | tipo di misura | **solo il registro**, little-endian |
| Posizione del registro | ultimo blocco | **primo** blocco |
| Quarta word | non descritta | sempre `00000000` |
| Misure con IP placeholder | scartate | **stazioni separate e mai scartate** |
| Forma dell'output | oggetto stazione singolo | **lista** di stazioni |

## Limiti noti

- **`try/except` globale**: le eccezioni emettono `{"status": "ERROR", ...}`, mai blank.
- **`NAME` non viene troncato**: la colonna ADAS è `nvarchar(50)`; nomi più lunghi vengono rifiutati dal database.
- **`_meta` e `_warnings` sono iniettati in ogni stazione**, quindi duplicati N volte.
- **`_meta.raw_sample` e `raw_head` contengono estratti grezzi** dell'ingresso, inclusi IP e nomi cliente: da filtrare prima di un uso su dati reali.
- **Linearizzazione BISON non implementata**: `scale_elec_*` e `scale_eng_*` sono raccolti dal VLM ma non usati; i `Dividere x10` (9 misure asteriscate) non sono raccolti.

## Double PDF: copia separata, non mescolare

Il Double PDF ha il suo trasformatore con `{edge}[13]` in
[`../../double_pdf/platforms/lv1/scripts/in_use/json_creator_edge13_canvas.py`](../../double_pdf/platforms/lv1/scripts/in_use/json_creator_edge13_canvas.py).
I due flussi condividono la logica ma non l'indice dell'edge: restano in
cartelle separate per non costringere a editare il file a ogni switch di flusso.
