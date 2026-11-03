# Pytools — Single PDF

## Inventario

| File | Versione | Nodo | Stato |
|---|---|---|---|
| [`json_creator_v15.py`](json_creator_v15.py) | `v15` | LV1-05 | Pronto da incollare al rewiring (redesign). |
| [`json_creator_v4_5.py`](json_creator_v4_5.py) | `v4.5` | — | Storico, superato. |
| [`json_creator_v4_4.py`](json_creator_v4_4.py) | `v4.4` | — | Storico, superato. |
| [`json_creator_v4_2.py`](json_creator_v4_2.py) | `v4.2` | — | Storico, superato. |
| [`consolidator.py`](consolidator.py) | `v14` | CONSOLIDATORE (LV1-04) | Documentato, da incollare dopo rewiring Task 8. |
| [`consolidator_canvas.py`](consolidator_canvas.py) | `v14` | CONSOLIDATORE (LV1-04) | Copia canvas senza commenti, stesso AST. |
| [`oracle_apply.py`](oracle_apply.py) | `v1` | ORACLE_APPLY (LV1-04b) | Documentato: applica le correzioni dell'oracolo al consolidato. |
| [`oracle_apply_canvas.py`](oracle_apply_canvas.py) | `v1` | ORACLE_APPLY (LV1-04b) | Copia canvas senza commenti, stesso AST. |
| [`page_assembler.py`](page_assembler.py) | `v1` | PAGE ASSEMBLER (LV2-03) | Documentato: unisce UNIFIED + ORACOLO in una pagina. |
| [`page_assembler_canvas.py`](page_assembler_canvas.py) | `v1` | PAGE ASSEMBLER (LV2-03) | Copia canvas senza commenti, stesso AST. |

## Sorgente e sincronizzazione

Lo script è mantenuto in `src/nodes/json_creator.py` (v15) e copiato qui. La copia è byte-identica; verificarla con:

```sh
sha256sum ../../../src/nodes/json_creator.py json_creator_v15.py
```

Hash atteso: `423e258860ff552532fe229e30174a3c66c18a4c45ecda84e6032f2e5271e799`

La copia canvas senza commenti (`json_creator_v15_canvas.py`, indentazione
compatta a 1 spazio/livello, stesso AST della documentata) vive in
`../platforms/lv1/scripts/updated_pending_validation/`; hash atteso:
`0768c752b5c18ac6852bed693619b21ff6ae91d052e3e67b815b3944e1bbe200`.

**Se gli hash divergono, la fonte autorevole è `src/nodes/`.**

## Consolidatore (redesign v14, Task 4)

Riferimento testabile: `src/nodes/single_consolidator.py`. Copia
documentata `consolidator.py` (stile inline, `{edge}[6]` da ricontrollare
dopo il rewiring Task 8) + copia canvas `consolidator_canvas.py` senza
commenti. La copia canvas **non si scrive a mano**: si genera dalla
documentata con `render_canvas.py` (stesso AST, 1 spazio per livello, righe
spezzate dentro parentesi unite), che è anche il controllo di parità in
`tests/test_single_consolidator_canvas.py`. La copia canvas resta sotto la
soglia di paste: 34.113 byte (guardia test 34.300; 34.365 = rosso certo).
Se gli hash divergono, vince `src/`.

```sh
sha256sum myhydra/single_pdf/pytools/consolidator.py myhydra/single_pdf/pytools/consolidator_canvas.py
```

Hash attesi:
- `consolidator.py`: `e9894934da6670a346bae9adc13fa5143bc1eb7b2c7578f8e967119b3a0f67dd`
- `consolidator_canvas.py`: `8d3c7d67a9fca15a52be226526ee225cbc8f63f4e1b876c2edca9fd40d61e1cc`

## ORACLE_APPLY (redesign v2)

Pytool separato perché il consolidatore canvas è già al limite di paste
(34.113 B): regole `oracolo_*` e audit trail vivono qui, non nel
consolidatore. Riceve **due edge**: il consolidato (nodo CONSOLIDATORE) e
l'output grezzo del motore, che contiene `verifica` per pagina. Applica solo
aggiungi/annulla (mai sovrascrive): refusi e IP non usati restano warning.

- `oracle_apply.py`: `ee61c0a7c075fed7e8c572d41d40c650889ca21d7eb9ad3473b47ff583a0bd82`
- `oracle_apply_canvas.py`: `091718500bcc6a0c679de49fc09fd6e42c5f73bd236c6e618ab628d4eb298370` (6.949 byte)

Legge anche `assemble_warnings` dalle pagine del motore e li porta nel tap
come `oracolo_assente` / `oracolo_input_assente`: un oracolo non collegato
non può restare in silenzio.

## PAGE_ASSEMBLER (redesign v2)

Vive nel **LV2**, subito dopo i due visiomaru. Senza questo nodo l'output
dell'oracolo (le sole 5 categorie) non è né `stations` né `rows` e il
consolidatore lo rifiuta (`blocco senza stations ne rows`). Due edge:
`raw_u = {edge}[2]` (UNIFIED) e `raw_o = {edge}[5]` (ORACOLO). Emette
`{"page_no", "stations", "verifica"|null, "assemble_warnings"}`.

- `page_assembler.py`: `822fe612d0958fc8b9c867259af9c26ad8e5a5b3f0857c6244f3314717a1f26c`
- `page_assembler_canvas.py`: `7edd34825b1e8ef473077feeeafdddb037a87915bfb444761d54396e393e283b` (3.108 byte)

Copia canvas in
`../platforms/lv2/scripts/updated_pending_validation/page_assembler_canvas.py`.

## Rigenerazione delle copie canvas

Dopo ogni modifica a una documentata:

```sh
python myhydra/single_pdf/pytools/render_canvas.py --write
cp myhydra/single_pdf/pytools/consolidator_canvas.py \
   myhydra/single_pdf/platforms/lv1/scripts/updated_pending_validation/
cp myhydra/single_pdf/pytools/oracle_apply_canvas.py \
   myhydra/single_pdf/platforms/lv1/scripts/updated_pending_validation/
cp myhydra/single_pdf/pytools/page_assembler_canvas.py \
   myhydra/single_pdf/platforms/lv2/scripts/updated_pending_validation/
```

`render_canvas.py` verifica tutte e quattro le coppie (`allineato`/`DIVERSO`)
e fallisce con codice 1 se una diverge.

Questo file ha `{edge}[2]` ed è del solo Single PDF. Il Double PDF ha una copia
separata con `{edge}[13}` in
[`../../double_pdf/platforms/lv1/scripts/in_use/json_creator_edge13_canvas.py`](../../double_pdf/platforms/lv1/scripts/in_use/json_creator_edge13_canvas.py)
(copia canvas senza commenti; il documentato è `json_creator_edge13.py`):
i due flussi condividono il trasformatore ma non l'indice dell'edge, quindi
restano in cartelle diverse.

La copia non ha header aggiuntivo per un motivo preciso: il file è un corpo Pytool pronto da incollare nel nodo, con il placeholder `{edge}[4]` alla riga 45. Aggiungere un header sposterebbe i numeri di riga e romperebbe i riferimenti incrociati fra questo README, le schede dei nodi e i contratti. La documentazione sta qui, il file resta incollabile.

## Storico delle versioni

| Versione | Sorgente | Edge | Note |
|---|---|---|---|
| v3 | `src/nodes/legacy/json_creator_v3.py` | `{edge}[3]` | Merge multi-pagina, parser difensivo. |
| v4.1 | `src/nodes/legacy/json_creator_v4_1.py` | `{edge}[4]` | Filtro sulle descrizioni contenenti `riservat`. |
| v4.2 | questo file (`json_creator_v4_2.py`) | `{edge}[4]` | Formato analogico da `data_type`, flag `CAMPO_SCALA_AS_MEASURES`. |
| v4.3 | `src/nodes/json_creator.py` (storico) | `{edge}[4]` | Scarto senza-registro, avvisi zeri iniziali e copertura (guardia morta). |
| v4.4 | `json_creator_v4_4.py` (storico) | `{edge}[4]` | Guardia copertura funzionante (stesso `page_no` + soglia 100), self-check linkage, validazione senza `def`. |
| v4.5 | questo file (`json_creator_v4_5.py`) | `{edge}[4]` | Fondo scala → `LOWRANGE`/`HIGHRANGE`; limiti e divisori solo in review (mapping BISON). |

Le variabili con prefisso `P` nella change-log dell'intestazione sono le correzioni portate dal v3 al v4: dedup delle misure, fold dei digitali singoli con registro condiviso, parsing robusto del registro, filtro dei nomi generici, pulizia delle parentesi e sanitizzazione degli stati.

## Contratto del runtime Pytool

- I dati arrivano tramite il placeholder `{edge}[4]`, risolto dalla piattaforma. L'indice è fragile: cambia se il numero di nodi precedenti varia. Verificare sul canvas.
- L'uscita è la variabile `output`, serializzata come JSON, stampata con `print`. La piattaforma la legge per popolare l'edge successivo.
- Lo stile è volutamente povero: `while` con indice esplicito, nessuna funzione, nessuna classe, nessuna f-string, commenti in italiano. È un adattamento al runtime limitato del nodo Pytool, ereditato dai nodi legacy.

## Note runtime

**La validazione Pydantic viene saltata su MyHydra.** Lo script prova a importare `src.models.validators`, risalendo da `__file__` fino a trovare una radice che contenga `src/models/`. Sulla piattaforma il pytool gira come script standalone e quel pacchetto non esiste, quindi l'import fallisce, l'eccezione viene catturata e `_pydantic_available` resta `False`. La pipeline prosegue identica, ma senza validazione. Non è un errore: è il comportamento previsto in entrambi gli ambienti.

**Il risultato è una lista di stazioni**, non un oggetto stazione singolo. `docs/contracts/ADAS_FINAL.md` dice il contrario.

## Contratto ADAS: divergenze dalla documentazione

`docs/contracts/ADAS_FINAL.md` descrive il formato `DRIVERPRIVATE` in modo che non coincide con il codice. Vale la pena conoscerle, perché chi legge solo il contratto scriverà il prodotto sbagliato.

| Punto | Contratto | Codice |
|---|---|---|
| Lunghezza di `DRIVERPRIVATE` | 52 caratteri | **48** caratteri |
| Primo blocco di 8 hex | tipo di misura | **solo il registro**, little-endian |
| Posizione del registro | ultimo blocco | **primo** blocco |
| Quarta word | non descritta | sempre `00000000`; il legacy vi metteva l'ultimo bit |
| Misure con IP placeholder | scartate, l'IP reale è primario | **sempre stazioni separate e mai scartate** |
| Forma dell'output | oggetto stazione singolo | **lista** di stazioni |

## Limiti noti

- **`try/except` globale di runtime** (fix Task 8 round 1/5): le eccezioni emettono `{"status": "ERROR", ...}` via `print(output)`, mai blank (modello: consolidatore v14).
- **`NAME` non viene troncato.** La colonna è `nvarchar(50)`; il legacy tagliava a 49 caratteri. Nomi più lunghi verranno rifiutati dal database.
- **`_meta` e `_warnings` sono iniettati in ogni stazione**, quindi duplicati N volte nell'output. È una scelta pragmatica per non aggiungere un involucro che romperebbe l'import in ADAS, ma appesantisce il payload.
- **`_meta.raw_sample` e `raw_head` contengono estratti grezzi dell'ingresso**, che possono includere indirizzi IP e nomi di stazione dei clienti. `docs/architettura/analisi_progetto.md` avverte che i documenti caricati contengono anche credenziali operative: se l'output deve girare su dati reali, questi campi vanno filtrati.
- **Tre difetti logici** documentati in [`../nodes/lv1_04_json_creator.md`](../nodes/lv1_04_json_creator.md): le guardie A e B che testano `bit` grezzo invece del bit estratto, il collasso del fold P2 e il dedup P1 dei digitali singoli.

## Non implementato

`VM_SOURCE_CODE` resta hardcoded a un valore di default e i campi `scale_elec_start`, `scale_elec_end`, `scale_eng_start`, `scale_eng_end`, `limit_hour` e `limit_day` sono raccolti dal VLM ma **non vengono mai usati** dallo script. La linearizzazione BISON è bloccata in attesa di specifiche del cliente.
