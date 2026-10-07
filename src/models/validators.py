"""
Utilità per la validazione degli output VLM e ADAS.

Questo modulo fornisce funzioni per:
- Validare JSON con Pydantic
- Gestire errori di validazione in modo strutturato
- Fornire feedback dettagliato su cosa non va
"""

import json
from typing import Any, Union
from pydantic import ValidationError

from .vlm_schema import (
    VLMOutput, 
    StationADAS, 
    validate_vlm_output, 
    validate_adas_output
)


class ValidationResult:
    """
    Risultato di una validazione.
    
    Contiene:
    - success: bool (True se validazione passata)
    - data: oggetto validato (se success=True)
    - errors: lista di errori (se success=False)
    - warnings: lista di warning (sempre presente)
    """
    
    def __init__(
        self, 
        success: bool, 
        data: Any = None, 
        errors: list[str] = None,
        warnings: list[str] = None
    ):
        self.success = success
        self.data = data
        self.errors = errors or []
        self.warnings = warnings or []
    
    def __repr__(self) -> str:
        status = "✅ PASS" if self.success else "❌ FAIL"
        return f"ValidationResult({status}, errors={len(self.errors)}, warnings={len(self.warnings)})"


def safe_validate_vlm(json_input: Union[str, dict]) -> ValidationResult:
    """
    Valida un JSON intermedio VLM in modo sicuro.
    
    Args:
        json_input: Stringa JSON o dizionario già parsato
        
    Returns:
        ValidationResult con:
        - success=True e data=VLMOutput se tutto OK
        - success=False e errors=[...] se validazione fallita
        
    Example:
        result = safe_validate_vlm('{"stations": [...]}')
        if result.success:
            print(f"Estratte {result.data.total_variables()} variabili")
        else:
            print(f"Errori: {result.errors}")
    """
    warnings = []
    
    # Step 1: Parsing JSON (se stringa)
    if isinstance(json_input, str):
        try:
            json_data = json.loads(json_input)
        except json.JSONDecodeError as e:
            return ValidationResult(
                success=False,
                errors=[f"JSON non valido: {str(e)}"]
            )
    else:
        json_data = json_input
    
    # Step 2: Validazione struttura base
    if not isinstance(json_data, dict):
        return ValidationResult(
            success=False,
            errors=[f"Atteso oggetto JSON, ricevuto: {type(json_data).__name__}"]
        )
    
    if "stations" not in json_data:
        return ValidationResult(
            success=False,
            errors=["Campo 'stations' mancante nel JSON"]
        )

    # Step 2b (v14): description nulla o vuota è errore esplicito.
    # Il controllo è qui (non solo in Pydantic) per un messaggio chiaro
    # indipendente dal dettaglio dell'errore di tipo.
    desc_errors = []
    stations_raw = json_data["stations"]
    if isinstance(stations_raw, list):
        for si, st in enumerate(stations_raw):
            if not isinstance(st, dict):
                continue
            variables_raw = st.get("variables")
            if not isinstance(variables_raw, list):
                continue
            for vi, var in enumerate(variables_raw):
                if not isinstance(var, dict):
                    continue
                desc = var.get("description")
                if desc is None or (isinstance(desc, str) and not desc.strip()):
                    desc_errors.append(
                        f"Campo 'stations -> {si} -> variables -> {vi} -> description': "
                        f"description nulla o vuota non ammessa"
                    )
    if desc_errors:
        return ValidationResult(
            success=False,
            errors=desc_errors,
            warnings=warnings
        )
    
    # Step 3: Validazione Pydantic
    try:
        vlm_output = validate_vlm_output(json_data)
        
        # Step 4: Warning e controlli aggiuntivi
        if len(vlm_output.stations) == 0:
            warnings.append("Nessuna stazione estratta (PDF vuoto o illeggibile?)")
        
        # Controlla stazioni senza IP
        stations_without_ip = [
            st for st in vlm_output.stations if st.ip is None
        ]
        if stations_without_ip:
            warnings.append(
                f"{len(stations_without_ip)} stazione/i senza IP "
                f"(verrà usato default 127.0.0.1)"
            )
        
        # Controlla stazioni senza nome
        stations_without_name = [
            st for st in vlm_output.stations if st.name is None
        ]
        if stations_without_name:
            warnings.append(
                f"{len(stations_without_name)} stazione/i senza nome "
                f"(verrà usato default 'SME')"
            )
        
        return ValidationResult(
            success=True,
            data=vlm_output,
            warnings=warnings
        )
        
    except ValidationError as e:
        # Formatta errori Pydantic in modo leggibile
        error_messages = []
        for error in e.errors():
            field = " -> ".join(str(loc) for loc in error["loc"])
            msg = error["msg"]
            error_messages.append(f"Campo '{field}': {msg}")
        
        return ValidationResult(
            success=False,
            errors=error_messages,
            warnings=warnings
        )


def safe_validate_adas(json_input: Union[str, list]) -> ValidationResult:
    """
    Valida un JSON finale ADAS in modo sicuro.
    
    Args:
        json_input: Stringa JSON o lista già parsata (lista di stazioni)
        
    Returns:
        ValidationResult con:
        - success=True e data=list[StationADAS] se tutto OK
        - success=False e errors=[...] se validazione fallita
        
    Example:
        result = safe_validate_adas('[{"NAME": "E1", ...}, ...]')
        if result.success:
            total_measures = sum(len(st.measures) for st in result.data)
            print(f" Prodotte {total_measures} misure totali")
        else:
            print(f"Errori: {result.errors}")
    """
    warnings = []
    
    # Step 1: Parsing JSON (se stringa)
    if isinstance(json_input, str):
        try:
            json_data = json.loads(json_input)
        except json.JSONDecodeError as e:
            return ValidationResult(
                success=False,
                errors=[f"JSON non valido: {str(e)}"]
            )
    else:
        json_data = json_input
    
    # Step 2: Validazione struttura base
    if not isinstance(json_data, list):
        return ValidationResult(
            success=False,
            errors=[f"Attesa lista JSON (array di stazioni), ricevuto: {type(json_data).__name__}"]
        )
    
    if len(json_data) == 0:
        warnings.append("Nessuna stazione prodotta (input vuoto?)")
    
    # Step 3: Validazione Pydantic per ogni stazione
    stations = []
    errors = []
    
    for i, station_data in enumerate(json_data):
        try:
            station = StationADAS(**station_data)
            stations.append(station)
        except ValidationError as e:
            # Formatta errori per questa stazione
            for error in e.errors():
                field = " -> ".join(str(loc) for loc in error["loc"])
                msg = error["msg"]
                errors.append(f"Stazione {i+1}, campo '{field}': {msg}")
    
    if errors:
        return ValidationResult(
            success=False,
            errors=errors,
            warnings=warnings
        )
    
    # Step 4: Controlli aggiuntivi
    if len(stations) > 0:
        # Verifica che gli ID stazione siano sequenziali
        station_ids = [st.ID for st in stations]
        if station_ids != list(range(1, len(stations) + 1)):
            warnings.append(
                f"ID stazioni non sequenziali: {station_ids} "
                f"(atteso 1..{len(stations)})"
            )
        
        # Verifica coerenza STATIONID nelle misure
        for st in stations:
            wrong_station_ids = [
                m for m in st.measures if m.STATIONID != st.ID
            ]
            if wrong_station_ids:
                warnings.append(
                    f"Stazione '{st.NAME}' (ID={st.ID}): "
                    f"{len(wrong_station_ids)} misura/e con STATIONID errato"
                )
    
    return ValidationResult(
        success=True,
        data=stations,
        warnings=warnings
    )


def print_validation_summary(result: ValidationResult, title: str = "Validazione"):
    """
    Stampa un riassunto formattato del risultato di validazione.
    
    Args:
        result: ValidationResult da stampare
        title: Titolo del report
    """
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    
    if result.success:
        print(f"✅ Validazione PASSATA")
        print()
        
        # Statistiche
        if hasattr(result.data, 'total_variables'):
            # VLMOutput
            print(f"📊 Statistiche:")
            print(f"  - Stazioni: {result.data.total_stations()}")
            print(f"  - Variabili totali: {result.data.total_variables()}")
            
            for i, st in enumerate(result.data.stations, 1):
                ip_display = st.ip or "(default 127.0.0.1)"
                name_display = st.name or "(default SME)"
                print(f"  - Stazione {i}: {name_display} @ {ip_display} ({len(st.variables)} variabili)")
        
        elif isinstance(result.data, list):
            # Lista di StationADAS
            total_measures = sum(len(st.measures) for st in result.data)
            total_bitinfo = sum(len(st.bitinfo) for st in result.data)
            
            print(f"📊 Statistiche:")
            print(f"  - Stazioni: {len(result.data)}")
            print(f"  - Misure totali: {total_measures}")
            print(f"  - Bitinfo totali: {total_bitinfo}")
            
            for st in result.data:
                print(f"  - {st.NAME}: {len(st.measures)} misure, {len(st.bitinfo)} bitinfo")
    
    else:
        print(f"❌ Validazione FALLITA")
        print()
        print(f"🔴 Errori ({len(result.errors)}):")
        for error in result.errors:
            print(f"  - {error}")
    
    if result.warnings:
        print()
        print(f"⚠️  Warning ({len(result.warnings)}):")
        for warning in result.warnings:
            print(f"  - {warning}")
    
    print(f"{'='*60}\n")
