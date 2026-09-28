"""
Test di validazione per i modelli Pydantic.

Questo script testa i modelli su output reali (PROTEC_1, SMA_1)
per verificare che siano compatibili con i dati prodotti dal VLM e dal json_creator.
"""

import json
import sys
from pathlib import Path

# Aggiungi src/ al path per importare i modelli
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from models import (
    safe_validate_vlm,
    safe_validate_adas,
    print_validation_summary,
)


# ============================================================================
# TEST DATA: Output VLM per PROTEC_1 (2 pagine)
# ============================================================================

VLM_OUTPUT_PROTEC_1 = [
    {
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
                    },
                    {
                        "description": "Allarme FID6_01",
                        "units": None,
                        "modbus_register": 40001,
                        "bit": 1,
                        "kind": "DIGITALE_IMPACCATO",
                        "read_write": "R",
                        "state_on": "OK",
                        "state_off": None,
                        "scale_elec_start": None,
                        "scale_elec_end": None,
                        "scale_eng_start": None,
                        "scale_eng_end": None,
                        "limit_hour": None,
                        "limit_day": None
                    }
                    # ... (altre 28 variabili omesse per brevità)
                ]
            }
        ]
    },
    {
        "stations": [
            {
                "name": None,
                "protocol": "ModBus TCP",
                "ip": "192.168.0.1",
                "port": 502,
                "modbus_id": 1,
                "variables": [
                    {
                        "description": "FID6_01 In Protezione",
                        "units": None,
                        "modbus_register": 40004,
                        "bit": 10,
                        "kind": "DIGITALE_IMPACCATO",
                        "read_write": "R",
                        "state_on": "Protezione Attiva",
                        "state_off": None,
                        "scale_elec_start": None,
                        "scale_elec_end": None,
                        "scale_eng_start": None,
                        "scale_eng_end": None,
                        "limit_hour": None,
                        "limit_day": None
                    },
                    {
                        "description": "Misura COT_01",
                        "units": None,
                        "modbus_register": 40008,
                        "bit": None,
                        "kind": "ANALOGICA",
                        "read_write": "R",
                        "state_on": None,
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
]


# ============================================================================
# TEST DATA: Output ADAS per PROTEC_1 (stazione completa)
# ============================================================================

ADAS_OUTPUT_PROTEC_1 = [
    {
        "NAME": "SME",
        "DRIVERNAME": "modbusplc",
        "XPOSITION": 430,
        "YPOSITION": 530,
        "DOWNLOADTYPE": 0,
        "DOWNLOADPROGRAM": None,
        "IGNOREERRORS": 0,
        "SNAPSHOT": None,
        "NORMALSNAPSHOT": 1,
        "CRITICSNAPSHOT": 32767,
        "ALARMSNAPSHOT": 32767,
        "SYNOBITMAP": None,
        "LINENAME": None,
        "AREACODE": None,
        "ADDRESS": None,
        "LINECONFIGURATION": None,
        "TIMELASTCONFIGURATION": None,
        "TIMELASTDOWNLOAD": None,
        "EVENTTIME": None,
        "EVENTCODE": 0,
        "EVENTORIGIN": None,
        "CODE": None,
        "DRIVERPRIVATE": None,
        "OVERWRITEMEASURES": 1,
        "DRIVERCONFIG": '<configuration><commProto><p0 class="Protocollo MODBUS (master) via TCP/IP" name="Protocollo MODBUS (master) via TCP/IP" ipaddress="192.168.0.1" tcpport="502" timeout="5000" retries="3" write4XXXX="6"/></commProto><recoveryProto/></configuration>',
        "ID": 1,
        "measures": [
            {
                "STATIONID": 1,
                "NAME": "Allarme Generatore H2",
                "DISABLED": 0,
                "DIGITAL": None,
                "DOWNLOAD": 0,
                "SNAPSHOT": 1,
                "IGNOREERRORS": 0,
                "LOWCRITICAL": None,
                "HIGHCRITICAL": None,
                "LOWRANGE": None,
                "HIGHRANGE": None,
                "LOWOFFSET": None,
                "HIGHOFFSET": None,
                "SQRAW": None,
                "SQ1HOURMEAN": None,
                "SQ3HOURMEAN": None,
                "SQ8HOURMEAN": None,
                "SQDAILYMEAN": None,
                "UNITS": None,
                "STANDARDRANGEID": None,
                "DRIVERDATA": 1,
                "TYPE": 6,
                "DRIVERPRIVATE": "0x419C00000000000000000000000000000100000096000000",
                "ONLY_POSITIVES": None,
                "VM_SOURCE_CODE": "if elapsed() then    storep(11);else store(8);fi;",
                "PERIOD": 5,
                "SNAPSIZE": 1000,
                "DRIVERCONFIG": '<configuration SynopticAnalogicFormat="%7.2f"/>',
                "ID": 1,
                "UNITS2": None
            }
        ],
        "bitinfo": [
            {
                "MEASUREID": 1,
                "BITNO": 0,
                "BITNAME": "ALLARME GENERATORE H2",
                "TEXTON": "DA DEFINIRE",
                "TEXTOFF": "OFF"
            }
        ]
    }
]


# ============================================================================
# TEST FUNCTIONS
# ============================================================================

def test_vlm_validation():
    """Testa la validazione dell'output VLM."""
    print("\n" + "="*70)
    print("TEST 1: Validazione output VLM (PROTEC_1, 2 pagine)")
    print("="*70)
    
    # Test pagina 1
    print("\n--- Pagina 1 (IP null) ---")
    result_1 = safe_validate_vlm(VLM_OUTPUT_PROTEC_1[0])
    print_validation_summary(result_1, "Pagina 1")
    
    assert result_1.success, f"Validazione pagina 1 fallita: {result_1.errors}"
    assert result_1.data.total_stations() == 1, "Attesa 1 stazione in pagina 1"
    assert len(result_1.warnings) > 0, "Attesi warning per IP null"
    
    # Test pagina 2
    print("\n--- Pagina 2 (IP 192.168.0.1) ---")
    result_2 = safe_validate_vlm(VLM_OUTPUT_PROTEC_1[1])
    print_validation_summary(result_2, "Pagina 2")
    
    assert result_2.success, f"Validazione pagina 2 fallita: {result_2.errors}"
    assert result_2.data.total_stations() == 1, "Attesa 1 stazione in pagina 2"
    assert result_2.data.stations[0].ip == "192.168.0.1", "IP atteso 192.168.0.1"
    
    print("\n✅ TEST 1 PASSATO: Validazione VLM funziona correttamente")


def test_adas_validation():
    """Testa la validazione dell'output ADAS."""
    print("\n" + "="*70)
    print("TEST 2: Validazione output ADAS (PROTEC_1, stazione completa)")
    print("="*70)
    
    result = safe_validate_adas(ADAS_OUTPUT_PROTEC_1)
    print_validation_summary(result, "Output ADAS")
    
    assert result.success, f"Validazione ADAS fallita: {result.errors}"
    assert len(result.data) == 1, "Attesa 1 stazione"
    assert result.data[0].NAME == "SME", "Nome stazione atteso 'SME'"
    assert len(result.data[0].measures) == 1, "Attesa 1 misura"
    assert len(result.data[0].bitinfo) == 1, "Atteso 1 bitinfo"
    
    print("\n✅ TEST 2 PASSATO: Validazione ADAS funziona correttamente")


def test_invalid_data():
    """Testa che la validazione rifiuti dati non validi."""
    print("\n" + "="*70)
    print("TEST 3: Validazione dati non validi")
    print("="*70)
    
    # Test 3a: JSON malformato
    print("\n--- Test 3a: JSON malformato ---")
    result = safe_validate_vlm('{"stations": [invalid json}')
    print_validation_summary(result, "JSON malformato")
    assert not result.success, "Doveva fallire con JSON malformato"
    assert any("JSON non valido" in err for err in result.errors), "Errore JSON atteso"
    
    # Test 3b: Campo mancante
    print("\n--- Test 3b: Campo 'stations' mancante ---")
    result = safe_validate_vlm({"other_field": "value"})
    print_validation_summary(result, "Campo mancante")
    assert not result.success, "Doveva fallire con campo mancante"
    
    # Test 3c: Tipo errato
    print("\n--- Test 3c: Tipo errato (lista invece di oggetto) ---")
    result = safe_validate_vlm([1, 2, 3])
    print_validation_summary(result, "Tipo errato")
    assert not result.success, "Doveva fallire con tipo errato"
    
    # Test 3d: Bit fuori range
    print("\n--- Test 3d: Bit fuori range (16) ---")
    invalid_vlm = {
        "stations": [
            {
                "name": None,
                "protocol": None,
                "ip": None,
                "port": None,
                "modbus_id": None,
                "variables": [
                    {
                        "description": "Test",
                        "units": None,
                        "modbus_register": 40001,
                        "bit": 16,  # Invalido: deve essere 0-15
                        "kind": "DIGITALE_IMPACCATO",
                        "read_write": None,
                        "state_on": None,
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
    result = safe_validate_vlm(invalid_vlm)
    print_validation_summary(result, "Bit fuori range")
    assert not result.success, "Doveva fallire con bit=16"
    assert any("Bit 16" in err for err in result.errors), "Errore bit range atteso"
    
    print("\n✅ TEST 3 PASSATO: Validazione rifiuta correttamente dati non validi")


def test_edge_cases():
    """Testa casi limite (pagina vuota, stazioni multiple, ecc.)."""
    print("\n" + "="*70)
    print("TEST 4: Casi limite")
    print("="*70)
    
    # Test 4a: Pagina vuota
    print("\n--- Test 4a: Pagina vuota (stations=[]) ---")
    empty_page = {"stations": []}
    result = safe_validate_vlm(empty_page)
    print_validation_summary(result, "Pagina vuota")
    assert result.success, "Pagina vuota deve validare (con warning)"
    assert any("Nessuna stazione" in w for w in result.warnings), "Warning pagina vuota atteso"
    
    # Test 4b: IP placeholder
    print("\n--- Test 4b: IP placeholder (xxx.xxx.xxx.xxx) ---")
    placeholder_page = {
        "stations": [
            {
                "name": "Test",
                "protocol": "ModBus TCP",
                "ip": "xxx.xxx.xxx.xxx",
                "port": 502,
                "modbus_id": 1,
                "variables": []
            }
        ]
    }
    result = safe_validate_vlm(placeholder_page)
    print_validation_summary(result, "IP placeholder")
    assert result.success, "IP placeholder deve validare"
    assert result.data.stations[0].ip == "xxx.xxx.xxx.xxx", "IP placeholder preservato"
    
    # Test 4c: Units numeriche (devono essere null)
    print("\n--- Test 4c: Units numeriche ('1', '0' → null) ---")
    numeric_units = {
        "stations": [
            {
                "name": None,
                "protocol": None,
                "ip": None,
                "port": None,
                "modbus_id": None,
                "variables": [
                    {
                        "description": "Test",
                        "units": "1",  # Deve essere convertito in null
                        "modbus_register": 40001,
                        "bit": None,
                        "kind": "DIGITALE_SINGOLO",
                        "read_write": None,
                        "state_on": None,
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
    result = safe_validate_vlm(numeric_units)
    print_validation_summary(result, "Units numeriche")
    assert result.success, "Units numeriche devono validare"
    assert result.data.stations[0].variables[0].units is None, "Units '1' → null"
    
    print("\n✅ TEST 4 PASSATO: Casi limite gestiti correttamente")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("TEST SUITE: Modelli Pydantic per Menerva MAS")
    print("="*70)
    
    try:
        test_vlm_validation()
        test_adas_validation()
        test_invalid_data()
        test_edge_cases()
        
        print("\n" + "="*70)
        print("🎉 TUTTI I TEST SONO PASSATI!")
        print("="*70)
        print("\nI modelli Pydantic sono pronti per essere usati:")
        print("  - Nel json_creator per validare l'input VLM")
        print("  - In MyHydra per rilevare errori prima del processing")
        print("  - Nei test di regressione per verificare il contratto")
        print()
        
    except AssertionError as e:
        print(f"\n❌ TEST FALLITO: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERRORE IMPREVISTO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
