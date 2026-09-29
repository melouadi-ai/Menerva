# Prompt — Single PDF

## Inventario

| File | Versione | Nodo | Stato |
|---|---|---|---|
| [`vlm_extraction_v13.md`](vlm_extraction_v13.md) | `v13` | LV2-02 — parsing JSON principale | In uso. Copia byte-identica di `src/prompts/vlm_extraction_v13.md`. |

## Sorgente e sincronizzazione

Il prompt è mantenuto in `src/prompts/` e copiato qui. La copia è byte-identica; verificarla con:

```sh
sha256sum ../../../src/prompts/vlm_extraction_v13.md vlm_extraction_v13.md
```

Hash atteso: `7fe80cd5ea7bcfcfeb751647dbfc7b1ad96f057efb653cf87f9c29259e851fb3`

**Se i due hash divergono, la fonte autorevole è `src/prompts/`.** Quando il prompt cambia lì, va ricopiato qui e questo file aggiornato con il nuovo hash.

## Cronologia delle versioni

| Regola | v11 | v12 | v13 |
|---|---|---|---|
| `data_type` nello schema | — | sì | sì |
| V20, skip su note `NO PC SME`, `NOT USED` | — | sì | riscritta, senza richiedere intestazione di colonna |
| V21, zona `INPUT_HW` / `_HW` | — | sì | sì |
| V22, registro doppio `40051/40052` | — | sì | sì |
| V23, rimappa bit da 1-16 | dentro V5 | separata | sì |
| V24, porta con testo `gate` | — | sì | sì |
| **V25, `data_type` copia esatta** | — | — | **novità** |
| **V26, fedeltà del bit** | — | — | **novità** |

Le due novità di v13 corrispondono alle due novità di `json_creator.py` v4.2: il formato analogico dedotto da `data_type` e il flag `CAMPO_SCALA_AS_MEASURES`. La coerenza è voluta, non casuale: il prompt raccoglie il dato, il pytool lo trasforma in modo deterministico.

## Disallineamento con la documentazione

`docs/contracts/VLM_INTERMEDIATE.md` dichiara ancora **v11** come prompt di riferimento, pur includendo già il campo `data_type` introdotto da v12. Il contratto non è stato aggiornato.

## Regole di versione

- Ogni modifica crea un file nuovo con suffisso `_vN`; i precedenti non vengono modificati.
- Le schede dei nodi in [`../nodes/`](../nodes/) referenziano il prompt tramite link, mai per numero di versione in testo.
- Una modifica al prompt invalida le fixture di [`../test/`](../test/): i `observed_*` vanno rigenerati e i derivati ricalcolati.
