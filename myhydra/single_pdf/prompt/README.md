# Prompt — Single PDF

## Inventario (stato al 3 novembre 2026)

Il redesign v2 usa **due** prompt: un solo estrattore (UNIFIED) e un
verificatore (ORACOLO). I tre rami v14 restano come storia in
[`history/`](history/) e in `src/prompts/`: non si modificano e non si
incollano.

| File | Versione | Nodo | Stato |
|---|---|---|---|
| [`vlm_unified_v1.md`](vlm_unified_v1.md) | `v1` | LV2-02 UNIFIED — estrazione unica (misure + bit + stati + tecnici) | **Corrente.** Checklist prima delle variabili, schema unico, V1-V30. |
| [`vlm_oracle_v1.md`](vlm_oracle_v1.md) | `v1` | LV2-02 ORACOLO — verifica (5 categorie + `evidenza`) | **Corrente.** R0 Context gate: senza il JSON di UNIFIED nel Context risponde `errore_input`. |
| [`history/vlm_measures_v18.md`](history/vlm_measures_v18.md) | `v18` | LV2 ramo 1 di 3 — misure + dati tecnici | Storico (redesign v14). |
| [`history/vlm_bitnames_v16.md`](history/vlm_bitnames_v16.md) | `v16` | LV2 ramo 2 di 3 — nomi bit | Storico (redesign v14). |
| [`history/vlm_bitstates_v19.md`](history/vlm_bitstates_v19.md) | `v19` | LV2 ramo 3 di 3 — stati TEXTON/TEXTOFF | Storico (redesign v14). |
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
sha256sum ../../../src/prompts/vlm_unified_v1.md vlm_unified_v1.md \
          ../platforms/lv2/prompts/current/vlm_unified_v1.md
sha256sum ../../../src/prompts/vlm_oracle_v1.md vlm_oracle_v1.md \
          ../platforms/lv2/prompts/current/vlm_oracle_v1.md
```

Hash attesi (le tre copie devono coincidere):

| File | sha256 |
|---|---|
| `vlm_unified_v1.md` | `d50edd72d17717a6e36ffd95afc1c25ff1a2f4bfb310dc4075fba57ac30cf820` |
| `vlm_oracle_v1.md` | `a1d8b5a4bd1fedcabad242c47e65e14d760bb44c3a4a918c7f820813d6d7668b` |
| `history/vlm_extraction_v13.md` | `7fe80cd5ea7bcfcfeb751647dbfc7b1ad96f057efb653cf87f9c29259e851fb3` |

**Se gli hash divergono, la fonte autorevole è `src/prompts/`.** Quando il
prompt cambia lì, va ricopiato nei due specchi e questo file aggiornato.
Pinnato da `tests/test_single_canvas_hygiene.py::test_prompts_current_byte_identical_to_src`,
`tests/test_single_oracle.py` e `tests/test_single_unified.py`.

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
