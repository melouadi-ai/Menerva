# Contratto VLM Intermedio

Questo documento definisce lo schema JSON che il VLM deve produrre per ogni pagina di un documento di mappatura PLC/SCADA.

## Schema

```json
{
  "stations": [
    {
      "name": "string | null",
      "protocol": "string | null",
      "ip": "string | null",
      "port": "int | null",
      "modbus_id": "int | null",
      "variables": [
        {
          "description": "string | null",
          "units": "string | null",
          "modbus_register": "int | null",
          "bit": "int | null",
          "data_type": "string | null",   # V25: copia colonna DataType/Tipo, mai inferire
          "kind": "ANALOGICA | DIGITALE_SINGOLO | DIGITALE_IMPACCATO",
          "read_write": "R | W | null",
          "state_on": "string | null",
          "state_off": "string | null",
          "scale_elec_start": "number | null",
          "scale_elec_end": "number | null",
          "scale_eng_start": "number | null",
          "scale_eng_end": "number | null",
          "limit_hour": "number | null",
          "limit_day": "number | null",
          "zona": "string | null",
          "tag": "string | null",
          "pagina": "int | null",
          "riga": "int | null"
        }
      ]
    }
  ]
}
```

## Regole Chiave

### Stazione
- `name`: solo da etichette specifiche (NOME, Punto emissivo, Camino, Emissione, SAE)
- `ip`: carry-over dall'ultimo IP valido nella stessa tabella; placeholder separati
- `protocol`: "ModBus TCP" se presente, altrimenti null

### Variabili
- `description`: copia esatta dalla colonna, con **pulizia post-elaborazione (V19)**:
  - Rimozione di parentesi tonde vuote `()` (artefatti di formattazione)
  - Rimozione di virgolette semplici `'` e doppie `"` a inizio e fine stringa
  - Normalizzazione spazi multipli a uno singolo
  - **NON toccare**: parentesi con contenuto `(GR)`, parole, refusi, punteggiatura interna
  - Esempi: `"Polveri ()"` → `"Polveri"`, `"  SO2  "` → `"SO2"`, `"Stato (impianto)"` → `"Stato (impianto)"` (invariato)
- **Righe da saltare (V2)**:
  - Description completamente vuota
  - Match ESATTO (case-insensitive) con: "disponibile", "disponibile/", "disponible", "riserva", "spare", "reserve", "non utilizzato", "non utilizzata", "non usato", "libero", "---"
  - Intestazioni di sezione ESATTE (case-insensitive): "MISURE", "COMANDI", "IMPOSTAZIONI", "INPUT", "OUTPUT", "PARAMETRI", "REGISTRI", "SEGNALI", "VARIABILI", "ALLARMI", "STATI"
  - **NON saltare** se la description CONTIENE una di queste parole (es. "Misura Disponibile IW36" va tenuta)
- `kind`: ANALOGICA per stati/contatori/CALCOLATA senza registro; DIGITALE_SINGOLO per BOOL senza bit; DIGITALE_IMPACCATO per righe con suffisso bit o colonna bit
- `read_write`: copia esatta da colonna Read/Write ("R"/"W"), null se assente
- `state_on` / `state_off`: copia ESATTA dalla cella, mai inventare "1"/"0"
- `units`: null per digitali; copia testo non numerico per analogiche
- `scale_*`: null per digitali; elettrica solo se unità V/mA; ingegneristica da colonne scala
- `limit_hour` / `limit_day`: solo se le colonne esistono davvero nel documento
- `zona`: sezione/zona della tabella Modbus (es. ALLARMI, MISURE); stringhe vuote → null
- `tag`: TAG strumentale se presente nel documento, altrimenti null
- `pagina` / `riga`: tracciabilità riga-PDF (1-based, se presenti devono essere ≥ 1)
- `description`: nulla o vuota è **errore** di validazione (`safe_validate_vlm` fallisce)

### Divieti
- Mai calcolare DRIVERPRIVATE, ID, DRIVERDATA, TYPE, XML
- Mai usare colonna INDIRIZZO come registro
- Mai fondere stazioni IP reale + placeholder
- Rispondere SOLO con JSON valido

## Versione Prompt di Riferimento

Stato al 28/10/2026 — tre rami, un prompt corrente per ramo:

| Ramo | Prompt corrente |
|---|---|
| misure + dati tecnici | `src/prompts/vlm_measures_v18.md` |
| nomi bit | `src/prompts/vlm_bitnames_v16.md` |
| stati TEXTON/TEXTOFF | `src/prompts/vlm_bitstates_v19.md` |

Le versioni `v11`, `v12`, `v13` (ramo unico) e le intermedie `v14`–`v17`
restano in `src/prompts/` come storico e non vanno incollate nei nodi.
Inventario, cronologia delle regole e hash completi:
`myhydra/single_pdf/prompt/README.md`.

**Nota sul canvas:** il flusso Single attivo esegue ancora il ramo unico
`vlm_extraction_v13.md`; i tre rami correnti sono pronti ma mai eseguiti sulla
piattaforma. La migrazione è il rewiring descritto in
`myhydra/single_pdf/platforms/README.md`.

## v14 — decisioni config
- Campi extra sconosciuti: **ignorati** (default Pydantic, nessun `extra="forbid"`).
  Motivo: `json_creator` v4.5 legge campi extra dal chunk (`Division`,
  `Division_value`); rifiutarli romperebbe il flusso live
  (cfr. `tests/test_scale_range_limits.py::test_divisione_in_review`).
- `description` nulla/vuota: errore esplicito in `safe_validate_vlm`
  (controllo dedicato in `src/models/validators.py`, oltre al validatore Pydantic).
