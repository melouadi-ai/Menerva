# Prompt — Double PDF

## Inventario

| File | Versione | Nodo | Stato |
|---|---|---|---|
| [`page_classifier_v1.md`](page_classifier_v1.md) | `v1` | LV2-02 — classificatore pagine | In uso. 14 giri classificati nel caso 6. |

## Scopo del prompt

Il classificatore è l'unico prompt del workflow Double PDF. Riceve una o più immagini di pagina e assegna a ciascuna una delle tre etichette: `STATION_INFORMATION`, `MEASUREMENT_TECHNICAL_DATA`, `DENSITY_MAP`.

Non estrae dati e non produce testo libero: restituisce un solo oggetto JSON con la chiave `pages`, una voce per immagine, con indice in base zero.

## Regole di versione

- Ogni modifica al prompt crea un file nuovo con suffisso `_vN`; i file precedenti non vengono modificati.
- Le schede dei nodi in [`../nodes/`](../nodes/) referenziano il prompt in uso tramite link, mai per numero di versione in testo.
- Una modifica al prompt invalida le fixture di `../tests/`: i risultati in `outputs/observed_*` vanno rigenerati e i `expected_*` ricalcolati.
