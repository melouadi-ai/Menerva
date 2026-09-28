"""
Modelli Pydantic per la validazione degli output del VLM (contratto intermedio).

Questi modelli servono come "cancello" tra il VLM e il json_creator:
- Rilevano output malformati prima del processing
- Documentano il contratto in modo eseguibile
- Abilitano retry automatici in caso di errore VLM

Schema basato su: docs/contracts/VLM_INTERMEDIATE.md
Versione prompt: vlm_extraction_v11.md
"""

from typing import Optional, Literal
from pydantic import BaseModel, Field, field_validator


class Variable(BaseModel):
    """
    Una singola variabile estratta dal PDF (misura, digitale singolo o impacchettato).
    
    Corrisponde a una riga della tabella Modbus.
    """
    
    description: str = Field(..., description="Nome della variabile (dalla colonna Description)")
    units: Optional[str] = Field(None, description="Unità di misura (es. mg/Nm³, %, °C)")
    modbus_register: Optional[int] = Field(None, description="Registro Modbus (es. 40001, 40002)")
    bit: Optional[int] = Field(None, description="Bit all'interno del registro (0-15)")
    data_type: Optional[str] = Field(
        None,
        description=(
            "DataType dichiarato nel documento (INT16/UINT16/INT/REAL32/REAL/DINT/FLOAT/WORD). "
            "Usato dal pytool v4.2 (regola V25) per il formato analogico nel DRIVERPRIVATE."
        ),
    )
    
    kind: Literal["ANALOGICA", "DIGITALE_SINGOLO", "DIGITALE_IMPACCATO"] = Field(
        ..., 
        description="Tipo di variabile"
    )
    
    read_write: Optional[Literal["R", "W"]] = Field(
        None, 
        description="Direzione: R=read, W=write, null=non specificato"
    )
    
    state_on: Optional[str] = Field(None, description="Stato ON (dalla colonna '1 =')")
    state_off: Optional[str] = Field(None, description="Stato OFF (dalla colonna '0 =')")
    
    # Scale elettriche (solo se unità V o mA)
    scale_elec_start: Optional[float] = Field(None, description="Inizio scala elettrica")
    scale_elec_end: Optional[float] = Field(None, description="Fine scala elettrica")
    
    # Scale ingegneristiche (solo se unità mg/Nm³, %, mBar, °C, Nm³/h)
    scale_eng_start: Optional[float] = Field(None, description="Inizio scala ingegneristica")
    scale_eng_end: Optional[float] = Field(None, description="Fine scala ingegneristica")
    
    # Limiti (solo se colonne esistono nel documento)
    limit_hour: Optional[float] = Field(None, description="Limite orario")
    limit_day: Optional[float] = Field(None, description="Limite giornaliero")
    
    @field_validator('bit')
    @classmethod
    def validate_bit_range(cls, v: Optional[int]) -> Optional[int]:
        """Il bit deve essere tra 0 e 15."""
        if v is not None and (v < 0 or v > 15):
            raise ValueError(f"Bit {v} fuori range (0-15)")
        return v
    
    @field_validator('description')
    @classmethod
    def validate_description_not_empty(cls, v: str) -> str:
        """La description non può essere vuota."""
        if not v or not v.strip():
            raise ValueError("Description non può essere vuota")
        return v.strip()
    
    @field_validator('units')
    @classmethod
    def validate_units_not_numeric(cls, v: Optional[str]) -> Optional[str]:
        """
        Le units non possono essere solo numeri (regola V3 del prompt).
        Se la cella contiene solo "1" o "0", deve essere null.
        """
        if v is None:
            return None
        v = v.strip()
        if v in ["", "1", "0"]:
            return None
        return v


class Station(BaseModel):
    """
    Una stazione PLC estratta dal PDF.
    
    Corrisponde a un singolo IP Modbus (reale o placeholder).
    """
    
    name: Optional[str] = Field(None, description="Nome della stazione (da NOME/Punto emissivo/SAE)")
    protocol: Optional[str] = Field(None, description="Protocollo (es. ModBus TCP)")
    ip: Optional[str] = Field(None, description="Indirizzo IP del PLC")
    port: Optional[int] = Field(None, description="Porta Modbus (default 502)")
    modbus_id: Optional[int] = Field(None, description="ID Modbus (default 1)")
    
    variables: list[Variable] = Field(..., description="Lista delle variabili di questa stazione")
    
    @field_validator('port')
    @classmethod
    def validate_port_range(cls, v: Optional[int]) -> Optional[int]:
        """La porta deve essere tra 1 e 65535."""
        if v is not None and (v < 1 or v > 65535):
            raise ValueError(f"Porta {v} fuori range (1-65535)")
        return v
    
    @field_validator('modbus_id')
    @classmethod
    def validate_modbus_id_range(cls, v: Optional[int]) -> Optional[int]:
        """L'ID Modbus deve essere tra 1 e 247."""
        if v is not None and (v < 1 or v > 247):
            raise ValueError(f"Modbus ID {v} fuori range (1-247)")
        return v
    
    @field_validator('ip')
    @classmethod
    def validate_ip_format(cls, v: Optional[str]) -> Optional[str]:
        """
        L'IP può essere:
        - null (non specificato)
        - Un IP valido (es. 192.168.0.1)
        - Un placeholder (xxx.xxx.xxx.xxx, xxx,xxx,xxx,xxx, :)
        """
        if v is None:
            return None
        v = v.strip()
        if not v:
            return None
        return v


class VLMOutput(BaseModel):
    """
    Output completo del VLM per una singola pagina.
    
    Questo è il "contratto intermedio" tra il VLM e il json_creator.
    """
    
    stations: list[Station] = Field(..., description="Lista delle stazioni estratte da questa pagina")
    
    @field_validator('stations')
    @classmethod
    def validate_stations_not_empty(cls, v: list[Station]) -> list[Station]:
        """
        Almeno una stazione deve essere presente (anche se vuota).
        Se la pagina è completamente vuota, il VLM dovrebbe restituire [] esplicitamente.
        """
        # Nota: permettiamo lista vuota per pagine senza contenuto
        return v
    
    def total_variables(self) -> int:
        """Restituisce il numero totale di variabili in tutte le stazioni."""
        return sum(len(st.variables) for st in self.stations)
    
    def total_stations(self) -> int:
        """Restituisce il numero di stazioni."""
        return len(self.stations)


# Modelli per validare l'output finale ADAS (dopo json_creator)

class MeasureADAS(BaseModel):
    """
    Una misura nel formato ADAS finale.
    
    Corrisponde a una riga nella tabella misure del DB.
    """
    
    STATIONID: int = Field(..., description="ID della stazione (1-based)")
    NAME: str = Field(..., description="Nome della misura")
    DISABLED: int = Field(0, description="0=attivo, 1=disabilitato")
    DIGITAL: Optional[int] = Field(None, description="Flag digitale")
    DOWNLOAD: int = Field(0, description="Flag download")
    SNAPSHOT: int = Field(1, description="Flag snapshot")
    IGNOREERRORS: int = Field(0, description="Flag ignora errori")
    
    # Valori limite (BIG = 3.40282e+38 per analogiche, null per digitali)
    LOWCRITICAL: Optional[float] = Field(None, description="Limite critico basso")
    HIGHCRITICAL: Optional[float] = Field(None, description="Limite critico alto")
    LOWRANGE: Optional[float] = Field(None, description="Range basso")
    HIGHRANGE: Optional[float] = Field(None, description="Range alto")
    LOWOFFSET: Optional[float] = Field(None, description="Offset basso")
    HIGHOFFSET: Optional[float] = Field(None, description="Offset alto")
    SQRAW: Optional[float] = Field(None, description="Valore raw")
    SQ1HOURMEAN: Optional[float] = Field(None, description="Media oraria")
    SQ3HOURMEAN: Optional[float] = Field(None, description="Media 3 ore")
    SQ8HOURMEAN: Optional[float] = Field(None, description="Media 8 ore")
    SQDAILYMEAN: Optional[float] = Field(None, description="Media giornaliera")
    
    UNITS: Optional[str] = Field(None, description="Unità di misura")
    STANDARDRANGEID: Optional[int] = Field(None, description="ID range standard")
    
    DRIVERDATA: int = Field(..., description="Tipo driver (0=analogica, 1=digitale, 2=impacchettato, 5=comando)")
    TYPE: int = Field(..., description="Tipo formato (0=analogica, 1=impacchettato, 6=digitale)")
    
    DRIVERPRIVATE: str = Field(..., description="Stringa hex little-endian 6×int32")
    ONLY_POSITIVES: Optional[int] = Field(None, description="Flag solo positivi")
    
    VM_SOURCE_CODE: str = Field(..., description="Codice BISON per linearizzazione")
    PERIOD: int = Field(5, description="Periodo di campionamento (secondi)")
    SNAPSIZE: int = Field(1000, description="Dimensione snapshot")
    DRIVERCONFIG: str = Field(..., description="XML configurazione driver")
    
    ID: int = Field(..., description="ID univoco della misura (1-based per stazione)")
    UNITS2: Optional[str] = Field(None, description="Unità di misura (duplicato)")
    
    @field_validator('DRIVERDATA')
    @classmethod
    def validate_driverdata(cls, v: int) -> int:
        """DRIVERDATA deve essere 0, 1, 2 o 5."""
        if v not in [0, 1, 2, 5]:
            raise ValueError(f"DRIVERDATA {v} non valido (atteso 0, 1, 2, 5)")
        return v
    
    @field_validator('TYPE')
    @classmethod
    def validate_type(cls, v: int) -> int:
        """TYPE deve essere 0, 1 o 6."""
        if v not in [0, 1, 6]:
            raise ValueError(f"TYPE {v} non valido (atteso 0, 1, 6)")
        return v
    
    @field_validator('DRIVERPRIVATE')
    @classmethod
    def validate_driverprivate_format(cls, v: str) -> str:
        """
        DRIVERPRIVATE deve essere una stringa hex che inizia con '0x'.
        Formato: 0x + 48 caratteri hex (6×int32 little-endian = 24 byte = 48 hex chars)
        """
        if not v.startswith("0x"):
            raise ValueError(f"DRIVERPRIVATE deve iniziare con '0x', ricevuto: {v[:10]}...")
        hex_part = v[2:]
        if len(hex_part) != 48:
            raise ValueError(f"DRIVERPRIVATE hex deve essere 48 caratteri, ricevuto: {len(hex_part)}")
        try:
            int(hex_part, 16)  # Verifica che sia hex valido
        except ValueError:
            raise ValueError(f"DRIVERPRIVATE contiene caratteri non hex: {v}")
        return v


class BitInfoADAS(BaseModel):
    """
    Una riga di bitinfo nel formato ADAS finale.
    
    Definisce il significato di un bit all'interno di una misura impacchettata o digitale.
    """
    
    MEASUREID: int = Field(..., description="ID della misura a cui si riferisce questo bit")
    BITNO: int = Field(..., description="Numero del bit (0-15)")
    BITNAME: str = Field(..., description="Nome del bit (maiuscolo)")
    TEXTON: str = Field(..., description="Testo quando il bit è 1")
    TEXTOFF: str = Field(..., description="Testo quando il bit è 0")
    
    @field_validator('BITNO')
    @classmethod
    def validate_bitno_range(cls, v: int) -> int:
        """BITNO deve essere tra 0 e 15."""
        if v < 0 or v > 15:
            raise ValueError(f"BITNO {v} fuori range (0-15)")
        return v
    
    @field_validator('BITNAME')
    @classmethod
    def validate_bitname_uppercase(cls, v: str) -> str:
        """BITNAME deve essere maiuscolo."""
        return v.upper()


class StationADAS(BaseModel):
    """
    Una stazione nel formato ADAS finale.
    
    Contiene tutte le misure e i bitinfo per quel PLC.
    """
    
    NAME: str = Field(..., description="Nome della stazione")
    DRIVERNAME: str = Field("modbusplc", description="Nome del driver")
    XPOSITION: int = Field(430, description="Posizione X nel sinottico")
    YPOSITION: int = Field(530, description="Posizione Y nel sinottico")
    DOWNLOADTYPE: int = Field(0, description="Tipo download")
    DOWNLOADPROGRAM: Optional[str] = Field(None, description="Programma download")
    IGNOREERRORS: int = Field(0, description="Flag ignora errori")
    SNAPSHOT: Optional[int] = Field(None, description="Flag snapshot")
    NORMALSNAPSHOT: int = Field(1, description="Snapshot normale")
    CRITICSNAPSHOT: int = Field(32767, description="Snapshot critico")
    ALARMSNAPSHOT: int = Field(32767, description="Snapshot allarme")
    SYNOBITMAP: Optional[str] = Field(None, description="Bitmap sinottico")
    LINENAME: Optional[str] = Field(None, description="Nome linea")
    AREACODE: Optional[str] = Field(None, description="Codice area")
    ADDRESS: Optional[str] = Field(None, description="Indirizzo")
    LINECONFIGURATION: Optional[str] = Field(None, description="Configurazione linea")
    TIMELASTCONFIGURATION: Optional[str] = Field(None, description="Ora ultima configurazione")
    TIMELASTDOWNLOAD: Optional[str] = Field(None, description="Ora ultimo download")
    EVENTTIME: Optional[str] = Field(None, description="Ora evento")
    EVENTCODE: int = Field(0, description="Codice evento")
    EVENTORIGIN: Optional[str] = Field(None, description="Origine evento")
    CODE: Optional[str] = Field(None, description="Codice")
    DRIVERPRIVATE: Optional[str] = Field(None, description="Driver privato stazione")
    OVERWRITEMEASURES: int = Field(1, description="Flag sovrascrivi misure")
    DRIVERCONFIG: str = Field(..., description="XML configurazione driver (con IP, porta, timeout)")
    
    ID: int = Field(..., description="ID univoco della stazione (1-based)")
    
    measures: list[MeasureADAS] = Field(..., description="Lista delle misure di questa stazione")
    bitinfo: list[BitInfoADAS] = Field(..., description="Lista dei bitinfo di questa stazione")
    
    @field_validator('DRIVERCONFIG')
    @classmethod
    def validate_driverconfig_xml(cls, v: str) -> str:
        """DRIVERCONFIG deve essere un XML valido con tag configuration."""
        if not v.startswith("<configuration>"):
            raise ValueError(f"DRIVERCONFIG deve iniziare con <configuration>, ricevuto: {v[:20]}...")
        if not v.endswith("</configuration>"):
            raise ValueError(f"DRIVERCONFIG deve finire con </configuration>")
        if "ipaddress" not in v:
            raise ValueError("DRIVERCONFIG deve contenere ipaddress")
        return v


class ADASOutput(BaseModel):
    """
    Output finale completo nel formato ADAS.
    
    Questo è ciò che il json_creator produce dopo aver processato tutte le pagine.
    """
    
    stations: list[StationADAS] = Field(..., description="Lista di tutte le stazioni")
    
    def total_measures(self) -> int:
        """Restituisce il numero totale di misure in tutte le stazioni."""
        return sum(len(st.measures) for st in self.stations)
    
    def total_bitinfo(self) -> int:
        """Restituisce il numero totale di bitinfo in tutte le stazioni."""
        return sum(len(st.bitinfo) for st in self.stations)
    
    def total_stations(self) -> int:
        """Restituisce il numero di stazioni."""
        return len(self.stations)


# Funzioni di utilità per validazione rapida

def validate_vlm_output(json_data: dict) -> VLMOutput:
    """
    Valida un JSON intermedio del VLM e restituisce l'oggetto VLMOutput.
    
    Args:
        json_data: Dizionario JSON da validare
        
    Returns:
        VLMOutput validato
        
    Raises:
        ValidationError: Se il JSON non è conforme allo schema
    """
    return VLMOutput(**json_data)


def validate_adas_output(json_data: list[dict]) -> list[StationADAS]:
    """
    Valida un JSON finale ADAS e restituisce la lista di StationADAS.
    
    Args:
        json_data: Lista di dizionari JSON (stazioni) da validare
        
    Returns:
        Lista di StationADAS validate
        
    Raises:
        ValidationError: Se il JSON non è conforme allo schema
    """
    return [StationADAS(**station) for station in json_data]
