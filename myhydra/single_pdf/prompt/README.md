# Prompt — Single PDF (v2)

## Inventario (4 novembre 2026)

Il redesign v2 usa **due** prompt: un solo estrattore (`UNIFIED`) e un
verificatore (`ORACOLO`). In questa cartella c'è solo ciò che si incolla
oggi: i prompt dei 3 rami (v13–v19) sono in
[`../../../src/prompts/archive/`](../../../src/prompts/archive/) e nella
copia storica [`../archive/prompts_v13_v19/`](../archive/prompts_v13_v19/).

| File | Versione | Nodo | Stato |
|---|---|---|---|
| [`vlm_unified_v1.md`](vlm_unified_v1.md) | `v1` | LV2 `UNIFIED` — estrazione unica (misure + bit + stati + tecnici) | **Corrente.** Checklist prima delle variabili, schema unico, V1-V30. |
| [`vlm_oracle_v1.md`](vlm_oracle_v1.md) | `v1` | LV2 `ORACOLO` — verifica (5 categorie + `evidenza`) | **Corrente.** R0 Context gate: senza il JSON di UNIFIED nel Context risponde `errore_input`. |

## Sorgente e sincronizzazione

`src/prompts/` è autorevole; questa cartella è la **copia di paste**, byte per
byte identica. Non esistono altri specchi: la copia in
`platforms/lv2/prompts/` è stata eliminata il 4/11/2026 perché duplicava gli
stessi file (e si chiamava "current" pur contenendo solo versioni superate).

```sh
cd myhydra/single_pdf/prompt
sha256sum ../../../src/prompts/vlm_unified_v1.md vlm_unified_v1.md
sha256sum ../../../src/prompts/vlm_oracle_v1.md vlm_oracle_v1.md
```

Hash attesi (le due copie devono coincidere):

| File | sha256 |
|---|---|
| `vlm_unified_v1.md` | `d50edd72d17717a6e36ffd95afc1c25ff1a2f4bfb310dc4075fba57ac30cf820` |
| `vlm_oracle_v1.md` | `a1d8b5a4bd1fedcabad242c47e65e14d760bb44c3a4a918c7f820813d6d7668b` |

Pinnato da `tests/test_single_canvas_hygiene.py::test_prompt_correnti_una_copia_di_paste`,
`tests/test_single_unified.py` e `tests/test_single_oracle.py`.

## Storico (non si incolla)

Tutte le versioni del periodo a 3 rami, con il motivo per cui sono state
superate, sono in [`../archive/prompts_v13_v19/`](../archive/prompts_v13_v19/)
e in [`../../../src/prompts/archive/`](../../../src/prompts/archive/).
Le regole chiave restano pinnate da `tests/test_single_prompt_contracts.py`
(per non reintrodurre i difetti che avevano motivato ogni versione).

## Cronologia sintetica

| Versione | Novità | Esito |
|---|---|---|
| `v13` | parsing JSON a ramo unico | storico del canvas pre-redesign |
| `v14`–`v15` | 3 rami separati (misure / nomi bit / stati), `riga` assoluta | join fragile, sostituito |
| `v16` | checklist prima delle variabili, catalogo header | riduceva le invenzioni |
| `v17`–`v18` | anchored row scan, misure senza descrizione vietate | migliorava la fedeltà, non la struttura |
| `v19` | checklist prima degli stati | ultima versione dei 3 rami |
| `vlm_unified_v1` | **un solo estrattore** | struttura corrente |
| `vlm_oracle_v1` | **verificatore con evidenza** | struttura corrente |
