# Contratto JSON — ADAS Finale

> **Versione**: 1.0  
> **Stadio**: Output dello Stadio 6/7 (Trasformazione Python)  
> **Consumatore**: Piattaforma ADAS (import diretto)

## Scopo

Questo documento definisce lo schema JSON finale prodotto dalla pipeline dopo la trasformazione dal formato VLM intermedio. Questo formato è **conforme al database ADAS** e contiene tutti i campi necessari per l'import nella piattaforma, inclusi valori calcolati deterministicamente (DRIVERPRIVATE hex, XML DRIVERCONFIG, VM_SOURCE_CODE).

## Schema

```json
{
  "NAME": "SME",
  "DRIVERNAME": "modbusplc",
  "XPOSITION": 430,
  "YPOSITION": 530,
  "DRIVERCONFIG": "<configuration>...</configuration>",
  "ID": 1,
  "measures": [ ... ],
  "bitinfo": [ ... ]
}
```

L'output è un **oggetto stazione singolo** (dopo merge di stazioni con stesso IP).

---

## Stazione (oggetto principale)

| Campo | Tipo | Descrizione |
|---|---|---|
| `NAME` | string | Nome finale della stazione (dopo merge). |
| `DRIVERNAME` | string | `"modbusplc"`. |
| `XPOSITION`, `YPOSITION` | integer | Coordinate sinottico. Default: `430`, `530`. |
| `DOWNLOADTYPE` | integer | `0`. |
| `DOWNLOADPROGRAM` | null | `null`. |
| `IGNOREERRORS` | integer | `0`. |
| `SNAPSHOT` | null | `null`. |
| `NORMALSNAPSHOT` | integer | `1`. |
| `CRITICSNAPSHOT` | integer | `32767`. |
| `ALARMSNAPSHOT` | integer | `32767`. |
| `SYNOBITMAP` | null | `null`. |
| `LINENAME`, `AREACODE`, `ADDRESS` | null | `null`. |
| `LINECONFIGURATION`, `TIMELASTCONFIGURATION`, `TIMELASTDOWNLOAD` | null | `null`. |
| `EVENTTIME`, `EVENTORIGIN`, `CODE` | null | `null`. |
| `EVENTCODE` | integer | `0`. |
| `DRIVERPRIVATE` | null | `null` a livello stazione. |
| `OVERWRITEMEASURES` | integer | `1`. |
| `DRIVERCONFIG` | string | **XML completo** con configurazione protocollo. Vedi sotto. |
| `ID` | integer | ID stazione (sequenziale partendo da 1). |
| `measures` | array | Lista di misure ADAS-complete. |
| `bitinfo` | array | Lista di bit digitali. |

### DRIVERCONFIG — XML

```xml
<configuration>
  <commProto>
    <p0 class="Protocollo MODBUS (master) via TCP/IP"
        name="Protocollo MODBUS (master) via TCP/IP"
        ipaddress="192.168.0.1"
        tcpport="502"
        timeout="5000"
        retries="3"
        write4XXXX="6"/>
  </commProto>
  <recoveryProto/>
</configuration>
```

**Regole di generazione**:
- `ipaddress`: IP reale dalla stazione primaria (non placeholder).
- `tcpport`: porta dal DRIVERCONFIG VLM (default `502`).
- `timeout`, `retries`, `write4XXXX`: valori fissi come sopra.

---

## Misura (ADAS)

| Campo | Tipo | Descrizione |
|---|---|---|
| `STATIONID` | integer | Riferimento alla stazione contenitore. |
| `NAME` | string | Nome della misura. |
| `DISABLED` | integer | `0`. |
| `DIGITAL` | null | `null`. |
| `DOWNLOAD` | integer | `0`. |
| `SNAPSHOT` | integer | `1`. |
| `IGNOREERRORS` | integer | `0`. |
| `LOWCRITICAL`, `HIGHCRITICAL` | number | Default: `-3.40282e+38`, `3.40282e+38` (float min/max). |
| `LOWRANGE`, `HIGHRANGE` | number | Da scale VLM o default float min/max. |
| `LOWOFFSET`, `HIGHOFFSET` | number | Default float min/max. |
| `SQRAW`, `SQ1HOURMEAN`, `SQ3HOURMEAN`, `SQ8HOURMEAN`, `SQDAILYMEAN` | number | Default float min/max per analogici. `null` per digitali. |
| `UNITS` | string\|null | Unità ingegneristica. |
| `STANDARDRANGEID` | null | `null`. |
| `DRIVERDATA` | integer | Dal VLM intermedio. |
| `TYPE` | integer | Dal VLM intermedio. |
| `DRIVERPRIVATE` | string | **Hex calcolato deterministicamente**. Vedi sotto. |
| `ONLY_POSITIVES` | integer\|null | `0` per analogici, `null` per digitali. |
| `VM_SOURCE_CODE` | string | Codice Manager per la misura. Default: `"if elapsed() then storep(11); else store(8); fi;"`. |
| `PERIOD` | integer | `5`. |
| `SNAPSIZE` | integer | `1000`. |
| `DRIVERCONFIG` | string | XML misura: `<configuration SynopticAnalogicFormat="%7.2f"/>`. |
| `ID` | integer | **Rinumerato** in sequenza partendo da 1, dopo merge e ordinamento. |
| `UNITS2` | string\|null | Copia di `UNITS` per analogici, `null` per digitali. |

### DRIVERPRIVATE — Calcolo hex

Il DRIVERPRIVATE è una stringa hex di 52 caratteri calcolata deterministicamente:

```
0x [8 hex] 9C 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 [8 hex registro] [8 hex tipo]
```

**Regole**:
- Primi 8 hex: codifica del tipo di misura (analogico vs digitale) e dell'ID.
- `9C` per digitali impacchettati, `01` per digitali singoli.
- Ultime 16 cifre: registro MODBUS (in hex, little-endian) + tipo.

**Esempi**:
- `"0x419C00000000000000000000000000000100000096000000"` → digitale impaccato, registro 1
- `"0x010000000000000000000000000000000100000096000000"` → digitale singolo
- `"0x489C000000000000000000000000000001000000FA000000"` → analogico

---

## Bitinfo (ADAS)

| Campo | Tipo | Descrizione |
|---|---|---|
| `MEASUREID` | integer | ID della misura digitale contenitore (**ID rinumerato**). |
| `BITNO` | integer | Posizione bit (0–15). |
| `BITNAME` | string | Nome del bit. |
| `TEXTON` | string | Testo quando bit = 1. |
| `TEXTOFF` | string | Testo quando bit = 0. |

---

## Trasformazioni deterministiche (da VLM intermedio → ADAS)

Il nodo Python di trasformazione applica queste operazioni **senza** chiamare LLM:

1. **Merge stazioni con stesso IP**: stazioni multiple con IP reale identico vengono fuse in un'unica stazione. Le misure e bitinfo vengono concatenate.
2. **Selezione stazione primaria**: per gruppi con IP placeholder + IP reale, l'IP reale è primario.
3. **Calcolo DRIVERPRIVATE hex**: per ogni misura, genera la stringa hex basandosi su DRIVERDATA, TYPE, e MODBUSREGISTRO.
4. **Generazione XML DRIVERCONFIG**: costruisce l'XML con IP e porta dalla stazione.
5. **Rinumerazione ID misure**: dopo merge e ordinamento, riassegna ID da 1 in sequenza.
6. **Aggiornamento MEASUREID nei bitinfo**: allinea i riferimenti ai nuovi ID misure.
7. **Inserimento VM_SOURCE_CODE**: default `"if elapsed() then storep(11); else store(8); fi;"`.
8. **Popolamento campi fissi**: LOWCRITICAL, HIGHCRITICAL, PERIOD, SNAPSIZE, ecc.

---

## Merge delle stazioni — Regole

```
INPUT:   [Stazione A (IP 192.168.6.20, 5 misure),
          Stazione B (IP xxx.xxx.xxx.xxx, 3 misure),
          Stazione C (IP 192.168.6.20, 2 misure)]

OUTPUT:  Stazione "SME" (IP 192.168.6.20, 7 misure)
         → le 3 misure di Stazione B scartate (placeholder IP)
         → misure di A e C concatenate, poi rinumerate
```

**Eccezione**: se il documento ha solo stazioni con IP placeholder, usa la prima come primaria.

---

## Esempio minimo

Vedi `data/test_inputs/Mappatura_2_Cliente_PROTEC_1.json` per un esempio completo conforme a questo contratto.
