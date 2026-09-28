"""
Modelli Pydantic per la validazione degli output del progetto Menerva MAS.

Questo pacchetto contiene gli schemi per:
- vlm_schema: Contratto intermedio VLM → json_creator
- (futuro) adas_schema: Contratto finale json_creator → ADAS

Usage:
    from src.models.vlm_schema import VLMOutput, validate_vlm_output
    
    # Validazione JSON intermedio
    vlm_data = validate_vlm_output(json_dict)
    print(f"Estratte {vlm_data.total_variables()} variabili")
"""

from .vlm_schema import (
    # Modelli VLM intermedio
    Variable,
    Station,
    VLMOutput,
    validate_vlm_output,
    
    # Modelli ADAS finale
    MeasureADAS,
    BitInfoADAS,
    StationADAS,
    ADASOutput,
    validate_adas_output,
)

from .validators import (
    ValidationResult,
    safe_validate_vlm,
    safe_validate_adas,
    print_validation_summary,
)

__all__ = [
    # VLM intermedio
    "Variable",
    "Station", 
    "VLMOutput",
    "validate_vlm_output",
    
    # ADAS finale
    "MeasureADAS",
    "BitInfoADAS",
    "StationADAS",
    "ADASOutput",
    "validate_adas_output",
    
    # Validatori
    "ValidationResult",
    "safe_validate_vlm",
    "safe_validate_adas",
    "print_validation_summary",
]
