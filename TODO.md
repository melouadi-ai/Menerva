# TODO - In attesa di specifiche dal cliente

## BISON / VM_SOURCE_CODE - Linearizzazione scale
**Stato:** ⏳ BLOCCATO - In attesa di specifiche dal cliente

### Contesto
Attualmente il `json_creator.py` genera `VM_SOURCE_CODE` hardcodato al default:
```
if elapsed() then    storep(11);else store(8);fi;
```

### Cosa serve dal cliente
Per generare il codice BISON con linearizzazione (ZE/SE/ZI/SI), servono:
1. **Regole di linearizzazione**: Come mappare i valori elettrici (scala_elec) ai valori ingegneristici (scala_eng) in linguaggio Manager
2. **Template BISON**: Esempi reali di `VM_SOURCE_CODE` per misure con:
   - Scala lineare (es. 4-20mA → 0-300 mg/Nm³)
   - Condizioni di validazione (allarme sonda, frigo, manutenzione)
   - Gestione limiti orari/giornalieri
3. **Funzioni disponibili**: Elenco completo delle funzioni del linguaggio Manager (store, storep, elapsed, ecc.)

### Riferimenti
- Manuale: `docs/architettura/Manuale sviluppo linguaggio Manager rev03.pdf`
- Script attuale: `src/nodes/json_creator.py` (variabile `VM_DEFAULT`)
- Contratto VLM: `src/prompts/vlm_extraction_v11.md` (campi `scale_elec_*`, `scale_eng_*`, `limit_hour`, `limit_day`)
- Contratto ADAS: `docs/contracts/ADAS_FINAL.md`

### Azione quando arrivano le specifiche
1. Creare `src/core/bison_builder.py` con la logica deterministica di generazione
2. Aggiornare `json_creator.py` per chiamare il builder invece di usare `VM_DEFAULT`
3. Aggiornare il contratto `ADAS_FINAL.md` con esempi reali

---

## Altro
- [x] ✅ **Validazione Pydantic per il contratto intermedio VLM** — Completato in `src/models/`
- [x] ✅ **Test automatici con fixture dai PDF reali** — Completato in `tests/test_pydantic_models.py`
- [ ] Test automatici con fixture su PROTEC_2, SIEMENS, Curtiriso
- [ ] Nodi mancanti: pdf_splitter, page_classifier, merge_pages
- [ ] Configurazione MyHydra Livello 1 (orchestratore)
- [ ] Semplificazione MyHydra Livello 2 (rimozione pytool interno)
