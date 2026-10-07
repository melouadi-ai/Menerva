# Prompt — Single PDF

## Inventario

| File | Versione | Nodo | Stato |
|---|---|---|---|
| [`vlm_extraction_v13.md`](vlm_extraction_v13.md) | `v13` | LV2-02 — parsing JSON principale | Storico. Copia byte-identica di `src/prompts/vlm_extraction_v13.md`. |
| [`vlm_measures_v14.md`](vlm_measures_v14.md) | `v14` | LV2 misure+dati tecnici (ramo 1 di 3) | In uso. Copia byte-identica di `src/prompts/vlm_measures_v14.md`. |
| [`vlm_bitnames_v14.md`](vlm_bitnames_v14.md) | `v14` | LV2 nomi-bit (ramo 2 di 3) | In uso. Copia byte-identica di `src/prompts/vlm_bitnames_v14.md`. |
| [`vlm_bitstates_v14.md`](vlm_bitstates_v14.md) | `v14` | LV2 stati (ramo 3 di 3) | In uso. Copia byte-identica di `src/prompts/vlm_bitstates_v14.md`. |

## Sorgente e sincronizzazione

I prompt sono mantenuti in `src/prompts/` e copiati qui. Le copie sono byte-identiche; verificarle con:

```sh
sha256sum ../../../src/prompts/vlm_extraction_v13.md vlm_extraction_v13.md
sha256sum ../../../src/prompts/vlm_measures_v14.md vlm_measures_v14.md
sha256sum ../../../src/prompts/vlm_bitnames_v14.md vlm_bitnames_v14.md
sha256sum ../../../src/prompts/vlm_bitstates_v14.md vlm_bitstates_v14.md
```

Hash attesi:

| File | sha256 |
|---|---|
| `vlm_extraction_v13.md` | `7fe80cd5ea7bcfcfeb751647dbfc7b1ad96f057efb653cf87f9c29259e851fb3` |
| `vlm_measures_v14.md` | `783982679817d94e0e774496a536d3325d7009de1f59435eb97a1797b75dc16d` |
| `vlm_bitnames_v14.md` | `b134800c1d7d1ec7146ecb5236549ff87813a32daff9323d651088867ea7529a` |
| `vlm_bitstates_v14.md` | `fb96b76f0f4c86aa05e89d6e6ef3182a8069f8a28499fc2308c7b882b8ccf42b` |

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

## v14 — split in 3 rami (redesign Single, 2026-10-07)

`vlm_extraction_v13.md` resta storico e immutato. I 3 rami v14 ne sono lo
split senza nuove regole di scarto (solo V2/V20/V21 in tutti i rami):

- ramo misure: tutto v13 tranne gli stati (contratto di ramo: gli stati li
  emette il ramo stati, join su `riga`); aggiunge `zona`/`tag`/`pagina`/`riga`
  e il self-check BIT "point-to-cell". V3 senza `"Unità"` fra gli esempi
  (era un esempio che insegnava l'errore su `Polveri (GR)`).
- ramo nomi-bit: solo registro/bit/descrizione + `riga`; V23/V26 fedeltà bit.
- ramo stati: solo `state_on`/`state_off` + `riga`; V7/V8 copie esatte,
  stati da keyword restano compito dichiarato del pytool.

## Disallineamento con la documentazione

`docs/contracts/VLM_INTERMEDIATE.md` dichiara ancora **v11** come prompt di riferimento, pur includendo già il campo `data_type` introdotto da v12. Il contratto non è stato aggiornato.

## Regole di versione

- Ogni modifica crea un file nuovo con suffisso `_vN`; i precedenti non vengono modificati.
- Le schede dei nodi in [`../nodes/`](../nodes/) referenziano il prompt tramite link, mai per numero di versione in testo.
- Una modifica al prompt invalida le fixture di [`../test/`](../test/): i `observed_*` vanno rigenerati e i derivati ricalcolati.
