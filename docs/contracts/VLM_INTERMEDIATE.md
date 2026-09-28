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
          "data_type": "string | null",
          "kind": "ANALOGICA | DIGITALE_SINGOLO | DIGITALE_IMPACCATO",
          "read_write": "R | W | null",
          "state_on": "string | null",
          "state_off": "string | null",
          "scale_elec_start": "number | null",
          "scale_elec_end": "number | null",
          "scale_eng_start": "number | null",
          "scale_eng_end": "number | null",
          "limit_hour": "number | null",
          "limit_day": "number | null"
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

### Divieti
- Mai calcolare DRIVERPRIVATE, ID, DRIVERDATA, TYPE, XML
- Mai usare colonna INDIRIZZO come registro
- Mai fondere stazioni IP reale + placeholder
- Rispondere SOLO con JSON valido

## Versione Prompt di Riferimento
`src/prompts/vlm_extraction_v11.md`
