# Modelli Pydantic per Menerva MAS

Questo modulo contiene gli schemi Pydantic per validare gli output del VLM e del json_creator, fungendo da "cancello" tra i vari stadi della pipeline.

## 📁 Struttura

```
src/models/
├── __init__.py          # Esporta tutti i modelli e funzioni
├── vlm_schema.py        # Definizioni modelli (VLM intermedio + ADAS finale)
└── validators.py        # Funzioni di validazione sicura
```

## 🎯 Scopo

I modelli Pydantic servono per:

1. **Validazione automatica** degli output VLM prima del processing
2. **Documentazione eseguibile** del contratto tra stadi
3. **Rilevamento errori** strutturato con messaggi dettagliati
4. **Abilitare retry automatici** in caso di output VLM malformato

## 📊 Modelli disponibili

### Contratto VLM Intermedio

Questi modelli validano il JSON prodotto dal VLM (`vlm_extraction_v11.md`):

| Modello | Descrizione |
|---------|-------------|
| `Variable` | Singola variabile estratta (misura, digitale singolo o impacchettato) |
| `Station` | Stazione PLC con nome, IP, porta, lista di variabili |
| `VLMOutput` | Output completo del VLM per una pagina (lista di stazioni) |

### Contratto ADAS Finale

Questi modelli validano il JSON prodotto dal json_creator:

| Modello | Descrizione |
|---------|-------------|
| `MeasureADAS` | Singola misura in formato ADAS (con DRIVERPRIVATE hex, XML, VM_SOURCE_CODE) |
| `BitInfoADAS` | Riga di bitinfo (MEASUREID, BITNO, TEXTON, TEXTOFF) |
| `StationADAS` | Stazione ADAS completa con misure e bitinfo |
| `ADASOutput` | Output finale (lista di stazioni) |

## 🚀 Utilizzo

### Validazione sicura (consigliato)

Le funzioni `safe_validate_*` restituiscono un `ValidationResult` con errori strutturati:

```python
from src.models import safe_validate_vlm, safe_validate_adas, print_validation_summary

# Validazione output VLM
result = safe_validate_vlm(vlm_json_string_or_dict)
print_validation_summary(result, "Output VLM")

if result.success:
    vlm_output = result.data
    print(f"Estratte {vlm_output.total_variables()} variabili")
    print(f"Stazioni: {vlm_output.total_stations()}")
else:
    print(f"Errori: {result.errors}")

# Validazione output ADAS
result = safe_validate_adas(adas_json_string_or_list)
print_validation_summary(result, "Output ADAS")

if result.success:
    stations = result.data
    total_measures = sum(len(st.measures) for st in stations)
    print(f" Prodotte {total_measures} misure totali")
```

### Validazione diretta (lancia eccezioni)

Se preferisci gestire le eccezioni manualmente:

```python
from src.models import validate_vlm_output, validate_adas_output
from pydantic import ValidationError

try:
    vlm_output = validate_vlm_output(json_dict)
    print(f"OK: {vlm_output.total_variables()} variabili")
except ValidationError as e:
    print(f"Errore validazione: {e}")
```

## 🔍 Validatori integrati

I modelli includono validatori per:

### Variable
- `bit`: range 0-15
- `description`: non vuota
- `units`: converte "1"/"0" in null (regola V3)

### Station
- `port`: range 1-65535
- `modbus_id`: range 1-247
- `ip`: accetta null, IP validi e placeholder (xxx.xxx.xxx.xxx)

### MeasureADAS
- `DRIVERDATA`: deve essere 0, 1, 2 o 5
- `TYPE`: deve essere 0, 1 o 6
- `DRIVERPRIVATE`: formato hex valido (0x + 48 caratteri)

### BitInfoADAS
- `BITNO`: range 0-15
- `BITNAME`: convertito in maiuscolo

### StationADAS
- `DRIVERCONFIG`: XML valido con tag `<configuration>` e `ipaddress`

## 📋 Esempio completo

```python
import json
from src.models import safe_validate_vlm, print_validation_summary

# JSON di esempio (output VLM per PROTEC_1 pagina 1)
vlm_json = {
    "stations": [
        {
            "name": None,
            "protocol": "ModBus TCP",
            "ip": None,
            "port": None,
            "modbus_id": None,
            "variables": [
                {
                    "description": "Allarme Generatore H2",
                    "units": None,
                    "modbus_register": 40001,
                    "bit": 0,
                    "kind": "DIGITALE_IMPACCATO",
                    "read_write": "R",
                    "state_on": "Da Definire",
                    "state_off": None,
                    "scale_elec_start": None,
                    "scale_elec_end": None,
                    "scale_eng_start": None,
                    "scale_eng_end": None,
                    "limit_hour": None,
                    "limit_day": None
                }
            ]
        }
    ]
}

# Validazione
result = safe_validate_vlm(vlm_json)
print_validation_summary(result, "Test PROTEC_1 pagina 1")

# Output:
# ==============================================================
# Test PROTEC_1 pagina 1
# ==============================================================
# ✅ Validazione PASSATA
# 
# 📊 Statistiche:
#   - Stazioni: 1
#   - Variabili totali: 1
#   - Stazione 1: (default SME) @ (default 127.0.0.1) (1 variabili)
# 
# ⚠️  Warning (2):
#   - 1 stazione/i senza IP (verrà usato default 127.0.0.1)
#   - 1 stazione/i senza nome (verrà usato default 'SME')
# ==============================================================
```

## 🧪 Test

Per eseguire i test di validazione:

```bash
cd /home/next/Desktop/Menerva_MAS
python3 tests/test_pydantic_models.py
```

I test verificano:
- ✅ Validazione output VLM corretti (PROTEC_1, SMA_1)
- ✅ Validazione output ADAS corretti
- ✅ Rifiuto di dati non validi (JSON malformato, campi mancanti, bit fuori range)
- ✅ Gestione casi limite (pagina vuota, IP placeholder, units numeriche)

## 🔗 Integrazione con MyHydra

### Nel Livello 2 (validazione opzionale VLM)

Puoi aggiungere un nodo pytool dopo il VLM per validare l'output:

```python
# Nodo: Validatore VLM (opzionale)
from src.models import safe_validate_vlm

raw = r'''{edge}[3]'''  # Output del VLM
result = safe_validate_vlm(raw)

if result.success:
    print(json.dumps({"status": "ok", "variables": result.data.total_variables()}))
else:
    print(json.dumps({"status": "error", "errors": result.errors}))
```

### Nel Livello 1 (dopo il json_creator)

Puoi validare l'output finale prima dell'export:

```python
# Nodo: Validatore ADAS (opzionale)
from src.models import safe_validate_adas

raw = r'''{edge}[3]'''  # Output del json_creator
result = safe_validate_adas(raw)

if result.success:
    stations = result.data
    total = sum(len(st.measures) for st in stations)
    print(f"ADAS valido: {len(stations)} stazioni, {total} misure")
else:
    print(f"Errore ADAS: {result.errors}")
```

## 📝 Note

- I modelli sono basati su `docs/contracts/VLM_INTERMEDIATE.md` e `ADAS_FINAL.md`
- Il prompt corrente è `src/prompts/vlm_extraction_v11.md`
- I modelli sono progettati per essere **permissivi ma corretti**: accettano tutti i casi legittimi (IP placeholder, nome null, units null) ma rifiutano errori strutturali

## 🚀 Prossimi passi

- [ ] Integrare la validazione nel json_creator per abortire su errori VLM
- [ ] Aggiungere retry automatico nel Livello 2 se validazione fallisce
- [ ] Creare fixture di test per ogni PDF del corpus
- [ ] Aggiungere validazione nel nodo di merge multi-pagina
