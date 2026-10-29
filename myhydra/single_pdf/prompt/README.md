# Prompt — Single PDF

## Inventario (stato al 28 ottobre 2026)

I tre rami del redesign sono i prompt **correnti**. Le versioni precedenti
restano come storia in [`history/`](history/) e in `src/prompts/`: non si
modificano e non si incollano.

| File | Versione | Nodo | Stato |
|---|---|---|---|
| [`vlm_measures_v18.md`](vlm_measures_v18.md) | `v18` | LV2 ramo 1 di 3 — misure + dati tecnici | **Corrente.** Vieta le variabili senza cella descrizione. |
| [`vlm_bitnames_v16.md`](vlm_bitnames_v16.md) | `v16` | LV2 ramo 2 di 3 — nomi bit | **Corrente.** BIT solo da suffisso/N.Bit, mai da coil (V30). |
| [`vlm_bitstates_v19.md`](vlm_bitstates_v19.md) | `v19` | LV2 ramo 3 di 3 — stati TEXTON/TEXTOFF | **Corrente.** Checklist prima degli stati, join tollerante. |
| [`history/vlm_extraction_v13.md`](history/vlm_extraction_v13.md) | `v13` | LV2-02 — parsing JSON a ramo unico | Storico: è il prompt del canvas pre-redesign. |
| [`history/vlm_bitstates_v14.md`](history/vlm_bitstates_v14.md) | `v14` | ramo stati | Storico, superato da v15→v19. |
| [`history/vlm_bitstates_v15.md`](history/vlm_bitstates_v15.md) | `v15` | ramo stati | Storico, superato da v16→v19. |

I file `v14`/`v15`/`v17` di misure, nomi e stati esistono in `src/prompts/` e
sono referenziati dai test che pinnano le singole regole, ma **la versione da
incollare nei nodi è quella della tabella qui sopra**.

## Sorgente e sincronizzazione

I prompt sono mantenuti in `src/prompts/` e copiati in due specchi
byte-identici: questa cartella e
[`../platforms/lv2/prompts/current/`](../platforms/lv2/prompts/current/).
Verifica:

```sh
cd myhydra/single_pdf/prompt
sha256sum ../../../src/prompts/vlm_measures_v18.md vlm_measures_v18.md \
          ../platforms/lv2/prompts/current/vlm_measures_v18.md
sha256sum ../../../src/prompts/vlm_bitnames_v16.md vlm_bitnames_v16.md \
          ../platforms/lv2/prompts/current/vlm_bitnames_v16.md
sha256sum ../../../src/prompts/vlm_bitstates_v19.md vlm_bitstates_v19.md \
          ../platforms/lv2/prompts/current/vlm_bitstates_v19.md
```

Hash attesi (le tre copie devono coincidere):

| File | sha256 |
|---|---|
| `vlm_measures_v18.md` | `dd55d4855131c0f53f2ca3e939f6a6b1acd152beb0bd3a6a4d7feed77e946763` |
| `vlm_bitnames_v16.md` | `5baec7eb7074d985707f0e5a4fe1a70f28c3b27e5e2e7b906a6ef717a9705b2e` |
| `vlm_bitstates_v19.md` | `2325a235ac6f6170431d9000d7bdcfe52e618758fa2487230477bf34be242652` |
| `history/vlm_extraction_v13.md` | `7fe80cd5ea7bcfcfeb751647dbfc7b1ad96f057efb653cf87f9c29259e851fb3` |

**Se i tre hash divergono, la fonte autorevole è `src/prompts/`.** Quando il
prompt cambia lì, va ricopiato nei due specchi e questo file aggiornato.
Pinnato da `tests/test_single_canvas_hygiene.py::test_prompts_current_byte_identical_to_src`
e `tests/test_single_prompt_contracts.py`.

## Cronologia delle versioni

### Ramo misure + dati tecnici

| Regola | v13 | v14 | v15 | v16 | v17 | v18 |
|---|---|---|---|---|---|---|
| `data_type` copia esatta (V25) | sì | sì | sì | sì | sì | sì |
| Split in 3 rami, niente stati | — | **novità** | — | — | — | — |
| `zona` / `tag` / `pagina` / `riga` | — | **novità** | — | — | — | — |
| V3 senza `"Unità"` fra gli esempi | bug | **corretto** | — | — | — | — |
| `checklist` + `righe_viste` prima delle variabili | — | — | — | **novità** | — | — |
| BIT solo da suffisso/N.Bit, mai da coil | — | — | — | — | **novità** | — |
| Vietate le variabili senza cella descrizione | — | — | — | — | — | **novità** |

### Ramo nomi bit

| Regola | v14 | v15 | v16 |
|---|---|---|---|
| Solo registro/bit/descrizione + `riga` | **novità** | — | — |
| `riga` = indice fisico, buche incluse | **novità** | — | — |
| Check-key normalizzata | — | **novità** | — |
| BIT solo da suffisso/N.Bit (V30) | — | — | **novità** |

### Ramo stati TEXTON/TEXTOFF

| Regola | v14 | v15 | v16 | v17 | v18 | v19 |
|---|---|---|---|---|---|---|
| `state_on`/`state_off` copie esatte (V7/V8) | **novità** | — | — | — | — | — |
| Stati sparsi solo su righe valorizzate (V27/D7) | — | **novità** | — | — | — | — |
| Catalogo header + `digitali_visti` | — | — | **novità** | — | — | — |
| Scansione ancorata riga per riga (V29) | — | — | — | **novità** | — | — |
| Scansione in cima, corta e imperativa | — | — | — | — | **novità** | — |
| `checklist` prima degli stati, join tollerante | — | — | — | — | — | **novità** |

## Disallineamento con la documentazione (chiuso 2026-10-28)

`docs/contracts/VLM_INTERMEDIATE.md` dichiarava i prompt **v14** come
riferimento mentre la produzione è ferma a misure v18 / nomi v16 / stati v19.
Allineato il 28/10/2026 insieme a questo file e a
[`../platforms/lv2/README.md`](../platforms/lv2/README.md). Se torna a citare
una versione diversa da quella della tabella qui sopra, è il contratto a
essere sbagliato, non i prompt.

## Regole di versione

- Ogni modifica crea un file nuovo con suffisso `_vN`; i precedenti non vengono modificati.
- Le schede dei nodi in [`../nodes/`](../nodes/) referenziano il prompt tramite link, mai per numero di versione in testo.
- Una modifica al prompt invalida le fixture di [`../test/`](../test/): i `observed_*` vanno rigenerati e i derivati ricalcolati.
- Un prompt nuovo entra in questa tabella **lo stesso giorno** in cui è stato validato, e i due specchi vengono ricopiati prima del commit: è così che il v14 è rimasto "corrente" per tre settimane dopo essere stato superato.
