# ADR-001: Merge multi-pagina a livello intermedio (Opzione B)

**Stato:** ✅ Accettata
**Data:** 2026-09-24
**Decisore:** Utente + Qwen

## Contesto

Il workflow MyHydra è diviso in due livelli:
- **Livello 1** (orchestratore): spezzetta il PDF in immagini e orchestra il Livello 2
- **Livello 2** (sotto-piattaforma): processa una pagina alla volta

Problema: quando un PDF ha N pagine, il Livello 2 gira N volte e produce N JSON parziali.
Serve un merge finale per ottenere un unico JSON ADAS.

## Decisione

**Il merge avviene a livello INTERMEDIO** (dopo il VLM, prima del json_creator).

Flusso finale:

```
LIVELLO 1
├── N1: medex pdf2png          → PDF → N immagini
├── N2: medex media2content    → raggruppa 1 img per gruppo
├── N3: ITERATIVO              → invoca Livello 2 per ogni pagina
│     │
│     └── LIVELLO 2
│           ├── N1: medex content2media  → riconverte in immagine
│           └── N2: VLM                  → JSON intermedio della pagina
│                                         (output finale del Livello 2)
│
└── N4: pytool json_creator v3 → riceve N JSON intermedi aggregati
                                 │
                                 ├─ forward-fill name/ip/port cross-page
                                 ├─ merge stazioni per (name, ip)
                                 ├─ dedup bitinfo (MEASUREID, BITNO)
                                 ├─ merge digitali impacchettati cross-page
                                 ├─ trasformazione ADAS (hex, XML, IDs)
                                 └─ OUTPUT: JSON ADAS unico
```

## Motivazione (perché Opzione B e non Opzione A)

| Criterio | Opzione B (scelta) | Opzione A (merge a livello ADAS) |
|----------|-------------------|----------------------------------|
| **Semplicità del merge** | ✅ Semplice: concatena `variables[]`, forward-fill | ❌ Complesso: rinumera IDs, remap bitinfo, dedup DRIVERPRIVATE |
| **Digitali impacchettati cross-page** | ✅ Merge naturale (stesso registro = stessa measure) | ❌ Forensic: dedup per DRIVERPRIVATE hex |
| **Numerazione ID** | ✅ Unica passata, sequenziale | ❌ Rinumerazione + tabella mapping old→new |
| **Debugging** | ✅ Due sospetti: VLM o Python | ❌ Tre sospetti: VLM o pytool-pag o merger |
| **Forward-fill name/IP** | ✅ Banale (valore proprio vs ultimo valido) | ❌ Impossibile (già "bruciato" nell'XML) |
| **Impatto su Livello 2** | ⚠️ Rimuovere 1 nodo (pytool) | ✅ Nessuno |

**Principio guida:** *Merge early, transform late* — unire a livello semantico piccolo prima di trasformare a livello tecnico pesante.

## Modifiche richieste

1. **Livello 2**: RIMUOVERE il nodo pytool (il Livello 2 termina al VLM)
2. **Livello 1**: AGGIUNGERE un nodo pytool DOPO il nodo iterativo, contenente `json_creator.py` v3

## Riferimenti implementativi

- Script: `src/nodes/json_creator.py` (v3 multi-page)
- Contratto VLM: `src/prompts/vlm_extraction_v10bis.md`
- Contratto ADAS: `docs/contracts/ADAS_FINAL.md`
- Test: `tests/test_multipage.py` (15 test, tutti PASS)

## Regole ufficiali gestione stazioni (da README vecchio progetto §4.6, §5)

Il pytool v3 implementa le seguenti regole di dominio, verificate sui PDF reali:

| Situazione | Comportamento | Esempio reale |
|-----------|--------------|---------------|
| **Stazioni con STESSO IP reale** su pagine diverse | ✅ **FUSE** in una stazione unica (forward-fill + merge) | SMA_1 (se IP presente su tutte le pagine) |
| **Stazioni con IP placeholder** (`xxx.xxx.xxx.xxx`, `xxx,xxx,xxx,xxx`, `:`) | ⚠️ **MAI fuse** con stazioni IP reale, né tra loro → sempre separate | SMA_1 pagina 2 (stazione 2 separata) |
| **Stazioni con IP diversi** (reali distinti) | ❌ **Sempre separate** | Luxottica (se più PLC con IP diversi) |
| **Stazioni con IP null** (cella vuota nel PDF) | ❌ **Separate** con fallback `127.0.0.1` + warning nel payload | PROTEC_1 pagina 1 (30 variabili senza IP) |
| **Nome stazione mancante** (nessuna etichetta NOME/Punto emissivo/SAE/Camino/Emissione) | Fallback `"SME"` | Quasi tutti i PDF |
| **Più IP REALI sulla stessa pagina** | Una stazione per ciascun IP (regola S5 del prompt) | Clienti multi-sensore |

### Comportamento attuale su PROTEC_1 (2 pagine, 45 variabili totali)

```
Pagina 1: ip=null  → Stazione 1 "SME" @ 127.0.0.1 → 30 variabili (warning: no_ip)
Pagina 2: ip=192.168.0.1 → Stazione 2 "SME" @ 192.168.0.1 → 15 variabili
Output: 2 stazioni separate (COMPORTAMENTO CORRETTO per dominio)
```

## Rischi noti

1. **Aggregazione output iterativo**: MyHydra deve aggregare correttamente gli N output del Livello 2 in un unico payload per il pytool. Il parser v3 è difensivo (accetta concatenazione, JSONL, array, repr Python), ma il formato esatto va verificato su un PDF reale multi-pagina (es. PROTEC_1).

2. **Indice edge**: Il placeholder MyHydra `{edge}[3]` va verificato: l'indice `3` potrebbe cambiare a seconda di quanti nodi precedono il pytool nel Livello 1.

3. **Indice vs dati**: Alcuni PDF (es. SMI_1) hanno pagine "indice" della mappa registri (es. "Parametri/Impostazioni", "Comandi digitali") che non sono variabili reali. Richiede fix al prompt (V19 proposta).

## Prossimi passi

1. Verificare aggregazione iterativa su PROTEC_1 (3 pagine)
2. Configurare Livello 2 senza pytool
3. Configurare Livello 1 con pytool dopo nodo iterativo
4. Validare output su SMA (1 pagina, backward compat) e PROTEC (3+ pagine)
