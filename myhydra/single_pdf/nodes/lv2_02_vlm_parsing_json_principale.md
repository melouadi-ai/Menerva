# Nodo LV2-02 — VLM, estrazione unificata + oracolo (redesign v2)

- **Tipo/nome:** Visiomaru — modello vision-language, unica sorgente di
  estrazione dati. Nel sottomotore LV2 ci sono **due** istanze:
  - **UNIFIED** (estrazione, prompt `vlm_unified_v1.md`);
  - **ORACOLO** (verifica, prompt `vlm_oracle_v1.md`).
- **Input:** l'immagine prodotta da LV2-01 (una pagina) **in entrambe** le
  istanze.
- **Configurazione dei campi (identica nelle due istanze):** `{edge.media}[N]`
  **da solo** nel campo **Prompt**; istruzioni in **Powered identity**;
  **Context** vuoto. `N` è locale al canvas.
- **Prompt correnti:**
  - [`../prompt/vlm_unified_v1.md`](../prompt/vlm_unified_v1.md) (copia canvas:
    [`../platforms/lv2/prompts/current/vlm_unified_v1.md`](../platforms/lv2/prompts/current/vlm_unified_v1.md));
  - [`../prompt/vlm_oracle_v1.md`](../prompt/vlm_oracle_v1.md) (copia canvas:
    [`../platforms/lv2/prompts/current/vlm_oracle_v1.md`](../platforms/lv2/prompts/current/vlm_oracle_v1.md)).
- **Stato:** copie byte-identiche a `src/prompts/`; il canvas attivo esegue
  già UNIFIED (nodo etichettato `UNIFIED`), l'ORACOLO resta da incollare.

## Perché due istanze e non tre rami

Il redesign v14 divideva la pagina in **tre estrazioni indipendenti** della
stessa immagine (misure, nomi bit, stati) unite a valle sulla chiave `riga`.
Il join posizionale è fragile: ogni discordanza di scarto produce
`riga_mismatch`, `descrizione_mismatch`, `stati_riallineati` — 62 warning su
una run SIEMENS.

Dal redesign v2 **una sola estrazione** legge la riga intera e la scrive
completa (misure + bit + stati + campi tecnici). Non c'è più join per `riga`:
non possono esistere disaccordi fra rami che non esistono.

La seconda istanza (ORACOLO) **non estrae**: riceve la stessa immagine e
l'output di UNIFIED, e restituisce solo **discrepanze** in un JSON a cinque
categorie (`mancanti`, `unita_inventate`, `junk_stati`, `refusi_corretti`,
`ip_dichiarati_non_usati`). Non riscrive nulla: segnala, con `evidenza`
obbligatoria.

## Contratto di uscita del LV2

L'assemblatore di pagina (naive a valle dei due VLM) produce **una pagina**:

```json
{"page_no": 1,
 "stations": [{"name", "protocol", "ip", "port", "modbus_id",
               "variables": [...]}],
 "verifica": {"page_no": 1, "mancanti": [], "unita_inventate": [],
              "junk_stati": [], "refusi_corretti": [],
              "ip_dichiarati_non_usati": []}}
```

`stations` è il contratto storico (v14), `verifica` è la novità v2. Il
consolidatore ignora `verifica`; il nodo `ORACLE_APPLY` (LV1-04b) la legge
dall'output grezzo del motore e applica le correzioni al consolidato.

## Confini del compito del VLM

- **Una immagine = una pagina.** Nessuna memoria di altre pagine.
- **`description` e stati sono copia esatta.** Refusi inclusi: la correzione
  è del cliente, non del modello (V13).
- **`data_type` va copiato dalla colonna, mai dedotto.**
- **Ogni bit dalla propria riga** (V30), mai da coil/DBX, mai rinumerato.
- **`riga` è l'indice fisico della riga**, buche comprese (contratto storico,
  resta valido per i tap a 3 rami).
- **L'oracolo non calcola e non corregge:** solo discrepanze con evidenza.

- **Riferimenti:** [`../prompt/README.md`](../prompt/README.md) (inventario e
  hash), [`../platforms/lv2/README.md`](../platforms/lv2/README.md),
  [`../verifica_pdf/BENCHMARK_GATE.md`](../verifica_pdf/BENCHMARK_GATE.md)
  (§13-bis), [contratto VLM](../../../docs/contracts/VLM_INTERMEDIATE.md).
