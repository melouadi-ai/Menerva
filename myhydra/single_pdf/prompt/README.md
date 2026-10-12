# Prompt — Single PDF

## Inventario

| File | Versione | Nodo | Stato |
|---|---|---|---|
| [`vlm_extraction_v13.md`](vlm_extraction_v13.md) | `v13` | LV2-02 — parsing JSON principale | Storico. Copia byte-identica di `src/prompts/vlm_extraction_v13.md`. |
| [`vlm_measures_v14.md`](vlm_measures_v14.md) | `v14` | LV2 misure+dati tecnici (ramo 1 di 3) | Pronto da incollare al rewiring. Copia byte-identica di `src/prompts/vlm_measures_v14.md`. |
| [`vlm_bitnames_v14.md`](vlm_bitnames_v14.md) | `v14` | LV2 nomi-bit (ramo 2 di 3) | Pronto da incollare al rewiring. Copia byte-identica di `src/prompts/vlm_bitnames_v14.md`. |
| [`vlm_bitstates_v14.md`](vlm_bitstates_v14.md) | `v14` | LV2 stati (ramo 3 di 3) | Pronto da incollare al rewiring. Copia byte-identica di `src/prompts/vlm_bitstates_v14.md`. |

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
| `vlm_measures_v14.md` | `6b4fae9bf49bb8632972c961372a13a12c3be2cd107787d0bd1ba3c58c67a03a` |
| `vlm_bitnames_v14.md` | `f7c74b99ce6dd834db0e81deceb4f66531231aa8b0fc7c12db57d6c79b4a04d4` |
| `vlm_bitstates_v14.md` | `fb96b76f0f4c86aa05e89d6e6ef3182a8069f8a28499fc2308c7b882b8ccf42b` |
| `vlm_bitstates_v15.md` | `47914a264e1743cd8746a166a9b6fa210796e18c931a1ab6f47bb25b74228307` |

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

## Disallineamento con la documentazione (chiuso 2026-10-07)

`docs/contracts/VLM_INTERMEDIATE.md` dichiara ora i 3 prompt v14 come riferimento (prima: `vlm_extraction_v11.md`, pur includendo già il campo `data_type` introdotto da v12).

## Regole di versione

- Ogni modifica crea un file nuovo con suffisso `_vN`; i precedenti non vengono modificati.
- Le schede dei nodi in [`../nodes/`](../nodes/) referenziano il prompt tramite link, mai per numero di versione in testo.
- Una modifica al prompt invalida le fixture di [`../test/`](../test/): i `observed_*` vanno rigenerati e i derivati ricalcolati.
