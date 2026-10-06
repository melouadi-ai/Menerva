# Pytools — Single PDF

## Inventario

| File | Versione | Nodo | Stato |
|---|---|---|---|
| [`json_creator_v4_5.py`](json_creator_v4_5.py) | `v4.5` | LV1-04 | In uso. |
| [`json_creator_v4_4.py`](json_creator_v4_4.py) | `v4.4` | — | Storico, superato. |
| [`json_creator_v4_2.py`](json_creator_v4_2.py) | `v4.2` | — | Storico, superato. |

## Sorgente e sincronizzazione

Lo script è mantenuto in `src/nodes/json_creator.py` e copiato qui. La copia è byte-identica; verificarla con:

```sh
sha256sum ../../../src/nodes/json_creator.py json_creator_v4_5.py
```

Hash atteso: `0f52c52896504abb70e3a58b2f21213a7df91c46747099ffe9bd5b8abc83caa2`

**Se i due hash divergono, la fonte autorevole è `src/nodes/`.**

Questo file ha `{edge}[4]` ed è del solo Single PDF. Il Double PDF ha una copia
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

- **Nessun `try/except` globale.** Il legacy restituiva un JSON di errore; qui le eccezioni si propagano e un errore non gestito significa nessun output.
- **`NAME` non viene troncato.** La colonna è `nvarchar(50)`; il legacy tagliava a 49 caratteri. Nomi più lunghi verranno rifiutati dal database.
- **`_meta` e `_warnings` sono iniettati in ogni stazione**, quindi duplicati N volte nell'output. È una scelta pragmatica per non aggiungere un involucro che romperebbe l'import in ADAS, ma appesantisce il payload.
- **`_meta.raw_sample` e `raw_head` contengono estratti grezzi dell'ingresso**, che possono includere indirizzi IP e nomi di stazione dei clienti. `docs/architettura/analisi_progetto.md` avverte che i documenti caricati contengono anche credenziali operative: se l'output deve girare su dati reali, questi campi vanno filtrati.
- **Tre difetti logici** documentati in [`../nodes/lv1_04_json_creator.md`](../nodes/lv1_04_json_creator.md): le guardie A e B che testano `bit` grezzo invece del bit estratto, il collasso del fold P2 e il dedup P1 dei digitali singoli.

## Non implementato

`VM_SOURCE_CODE` resta hardcoded a un valore di default e i campi `scale_elec_start`, `scale_elec_end`, `scale_eng_start`, `scale_eng_end`, `limit_hour` e `limit_day` sono raccolti dal VLM ma **non vengono mai usati** dallo script. La linearizzazione BISON è bloccata in attesa di specifiche del cliente.
