# Inventario tecnico del repository Menerva MAS

> Censimento generato il 28 settembre 2026. È una mappa verificabile dei file e delle loro strutture, non una certificazione semantica di ogni record o di ogni pagina. I conteggi e gli hash descrivono la copia locale al momento della scansione.

## Copertura e conteggi

- File tracciati da Git: **364**; file fisici nella scansione (esclusi `.git`, `.venv`, cache e bytecode): **369**.
- La scansione copre file Python (AST/struttura), JSON (parsing/schema di massima), PDF (pagine/testo estraibile/hash), TXT/Markdown (lunghezza e intestazioni), XLSX (fogli e dimensioni), archivi (indice), e gli altri binari (tipo file).
- La lettura automatica del testo PDF non controlla visivamente ogni tabella; righe d’immagine/scansioni richiedono verifica a vista. Nessuno screenshot dà accesso alla configurazione interna cloud.

## Albero funzionale sintetico

- `src/`: implementazione locale attuale, modelli, prompt VLM attuali e versioni legacy.
- `legacy/`: esportazioni di flussi MyHydra, prompt e script Python storici, spesso duplicati o varianti sperimentali.
- `data/test_inputs/`: PDF di prova e JSON di ruoli misti (ADAS, intermedi, esempi legacy); un PDF con nome Mappatura 6 è vuoto.
- `data/test_outputs/`: output storici GAIA/MyHydra, frammenti e riferimenti di confronto; 7 file `.json` non sono JSON standard valido.
- `docs/architettura/`: documenti architetturali, questa mappa, schermate/diagrammi e manuale Manager.
- `docs/contracts/`: schema intermedio VLM e schema finale ADAS, da riallineare a script e cloud.
- `docs/protocolli/`: schemi DB, mappature PDF/Excel, documenti cliente e pacchetti di database.
- `docs/ricerca/`: prompt GAIA/Visio e note/attività storiche.
- `tests/`: test locali, harness, output single PDF e directory output Double PDF senza fixture effettive.
- `reports/`: confronto qualità legacy/attuale; affermazioni del report vanno confrontate con dati grezzi qualificati.
- `docs/references/materiale_tutor/`: due fonti del tutor copiate e annotate come riferimenti storici.

## File Python (80)

Ogni file è stato analizzato strutturalmente con AST. Le descrizioni di file legacy sono indicative dal nome/percorso e non sostituiscono una revisione semantica linea per linea.

- `legacy/gaia_scripts/Python-BetterMeasuresJson.py` — 39 righe; AST OK; trasformazione/aggregazione JSON. Top-level: var input_json. SHA-256 `ab5490fd7875`.
- `legacy/gaia_scripts/Python-BitNameNumber.py` — 23 righe; AST OK; gestione bitinfo digitali. Top-level: var input_json. SHA-256 `23273d6d3f23`.
- `legacy/gaia_scripts/Python-Check-Empty-BitInfo.py` — 24 righe; AST OK; gestione bitinfo digitali. Top-level: var json_input, var json_input. SHA-256 `28c714733b7f`.
- `legacy/gaia_scripts/Python-Check-Group-IngressoDigitale.py` — 57 righe; AST OK; raggruppamento ingressi digitali. Top-level: var input_json, var final_result_json, var reg_to_stations, var cross_station_regs. SHA-256 `301bc2c02c13`.
- `legacy/gaia_scripts/Python-Check-Only-StationInfos-Stations.py` — 41 righe; AST OK; estrazione/gestione stazioni. Top-level: var input_json, var input_json. SHA-256 `15b39b8ad1b2`.
- `legacy/gaia_scripts/Python-Delete-NULL-Names.py` — 85 righe; AST OK; script legacy/utility: ruolo da verificare nel sorgente. Top-level: var json_input, var json_output. SHA-256 `5c079e5068ed`.
- `legacy/gaia_scripts/Python-JSON-Creator.py` — 325 righe; AST OK; trasformazione/aggregazione JSON. Top-level: var input_json, var output_json, var input_json, var VM_SOURCE_CODE_DEFAULT, var DRIVERCONFIG_MEASURE. SHA-256 `c8a1538f4d17`.
- `legacy/gaia_scripts/Python-Merge-BitInfo.py` — 26 righe; AST OK; merge di dati. Top-level: codice inline. SHA-256 `54a64257090f`.
- `legacy/gaia_scripts/Python-Merge-Multiple-Gaia.py` — 43 righe; AST OK; merge di dati. Top-level: codice inline. SHA-256 `b14bb4ad500e`.
- `legacy/gaia_scripts/Python-Merge-Result-Iterative-Node.py` — 37 righe; AST OK; merge di dati. Top-level: var input_station_info, var input_tech_data, var input_density_map. SHA-256 `57cd74420ddd`.
- `legacy/gaia_scripts/Python-Merge-Visio.py` — 142 righe; AST OK; merge di dati. Top-level: var agent1_output, var agent2_output, var agent3_output, def safe_parse, var bitinfo_lookup, var bitinfo_blocks, var final_output. SHA-256 `ec1dc3cfb976`.
- `legacy/gaia_scripts/Python-Merge-and-Tag.py` — 271 righe; AST OK; merge di dati. Top-level: var VM_SOURCE_CODE_DEFAULT, var DRIVERCONFIG_MEASURE, var input_json, def safe_parse. SHA-256 `b2757abc4ae3`.
- `legacy/gaia_scripts/Python-MergeMultipleVisioAgents.py` — 43 righe; AST OK; merge di dati. Top-level: codice inline. SHA-256 `ca14a6237fdd`.
- `legacy/gaia_scripts/Python-Pages-Merger.py` — 259 righe; AST OK; merge_pages.py. Top-level: var PAGE_OUTPUTS, var output_json_final. SHA-256 `fdf3e0f8b894`.
- `legacy/gaia_scripts/Python-Remove-BitInfo.py` — 16 righe; AST OK; gestione bitinfo digitali. Top-level: var input_json. SHA-256 `2a10e2d2ae44`.
- `legacy/gaia_scripts/Python-Remove-Quotes-Brackets-units.py` — 104 righe; AST OK; script legacy/utility: ruolo da verificare nel sorgente. Top-level: var input_json, var input_json, var output_json. SHA-256 `dadb7ba11ac2`.
- `legacy/gaia_scripts/Python-Remove-Quotes-Brackets.py` — 106 righe; AST OK; script legacy/utility: ruolo da verificare nel sorgente. Top-level: var input_json, var input_json, var output_json. SHA-256 `6c0329131f8a`.
- `legacy/gaia_scripts/Python-Station-Name.py` — 19 righe; AST OK; estrazione/gestione stazioni. Top-level: var input_str, var output_str. SHA-256 `3832d5510dc9`.
- `legacy/gaia_scripts/Python-StationInformation-TakeIP.py` — 75 righe; AST OK; estrazione/gestione stazioni. Top-level: var input_json, var input_json, var driver_config, var merged_bitinfo, var bitinfo_id_offset, var output. SHA-256 `fb14ecf71f8b`.
- `legacy/gaia_scripts/Python-StationInformationFlag.py` — 19 righe; AST OK; estrazione/gestione stazioni. Top-level: var input_json, var input_json. SHA-256 `df95e858ed54`.
- `legacy/gaia_scripts/Python-Stations-AND-Ports.py` — 113 righe; AST OK; estrazione/gestione stazioni. Top-level: var input_json, var reg_to_stations, var cross_station_regs, var output_json. SHA-256 `85d320161432`.
- `legacy/gaia_scripts/Python-Take-The-Correct-IP.py` — 47 righe; AST OK; script legacy/utility: ruolo da verificare nel sorgente. Top-level: var input_json. SHA-256 `264b1f849f4e`.
- `legacy/gaia_scripts/Python-Take-The-Correct-Key.py` — 50 righe; AST OK; script legacy/utility: ruolo da verificare nel sorgente. Top-level: var input_json. SHA-256 `f4c573c62885`.
- `legacy/gaia_scripts/testpython.py` — 805 righe; AST OK; test legacy. Top-level: var input_json, var output_json, var input_json, var VM_SOURCE_CODE_DEFAULT, var DRIVERCONFIG_MEASURE. SHA-256 `8f05094357e9`.
- `legacy/main_old.py` — 6 righe; AST OK; script legacy/utility: ruolo da verificare nel sorgente. Top-level: def main. SHA-256 `fe74ef1708ea`.
- `legacy/python_codes/Python-Check-Group-IngressoDigitale.py` — 39 righe; AST OK; raggruppamento ingressi digitali. Top-level: var input_json, var final_result_json. SHA-256 `b1500898feec`.
- `legacy/python_codes/Python-Delete-NULL-Names.py` — 54 righe; AST OK; script legacy/utility: ruolo da verificare nel sorgente. Top-level: var json_input, var json_output. SHA-256 `8d35dd07063b`.
- `legacy/python_codes/Python-JSON-Creator.py` — 328 righe; AST OK; trasformazione/aggregazione JSON. Top-level: var input_json, var output_json, var input_json, var VM_SOURCE_CODE_DEFAULT, var DRIVERCONFIG_MEASURE. SHA-256 `001af8ac0238`.
- `legacy/python_codes/Python-Merge-BitInfo.py` — 36 righe; AST OK; merge di dati. Top-level: codice inline. SHA-256 `822d1faa0072`.
- `legacy/python_codes/Python-Merge-Multiple-Gaia.py` — 41 righe; AST OK; merge di dati. Top-level: codice inline. SHA-256 `e8b7c60fabfc`.
- `legacy/python_codes/Python-Pages-Merger.py` — 254 righe; AST OK; merge_pages.py. Top-level: var PAGE_OUTPUTS, var output_json_final. SHA-256 `4d6a680e858c`.
- `legacy/python_codes/Python-Stations-AND-Ports.py` — 51 righe; AST OK; estrazione/gestione stazioni. Top-level: var input_json, var output_json. SHA-256 `d3f5ba62ba5f`.
- `legacy/python_codes/deletenullnames.py` — 69 righe; AST OK; script legacy/utility: ruolo da verificare nel sorgente. Top-level: var json_input, var json_input, var json_output. SHA-256 `2168c146a350`.
- `legacy/python_codes/impaccato.py` — 913 righe; AST OK; script legacy/utility: ruolo da verificare nel sorgente. Top-level: var input_json, var VM_SOURCE_CODE_DEFAULT, var DRIVERCONFIG_MEASURE. SHA-256 `51be054dfc8b`.
- `legacy/python_codes/impaccatomyhydra.py` — 241 righe; AST OK; script legacy/utility: ruolo da verificare nel sorgente. Top-level: var input_json, var output_json, var VM_SOURCE_CODE_DEFAULT, var DRIVERCONFIG_MEASURE. SHA-256 `da9c7f4bc815`.
- `legacy/python_codes/impaccatomyhydraconpiufiles.py` — 1867 righe; AST OK; script legacy/utility: ruolo da verificare nel sorgente. Top-level: var VM_SOURCE_CODE_DEFAULT, var DRIVERCONFIG_MEASURE, var input_json. SHA-256 `eeb2c8a82719`.
- `legacy/python_codes/impaccatomyhydrapiufileerimozionesenzanome.py` — 4761 righe; AST OK; script legacy/utility: ruolo da verificare nel sorgente. Top-level: var input_json, var output_json, var input_json, var VM_SOURCE_CODE_DEFAULT, var DRIVERCONFIG_MEASURE. SHA-256 `0c2c37bc0d43`.
- `legacy/python_codes/main.py` — 6 righe; AST OK; script legacy/utility: ruolo da verificare nel sorgente. Top-level: def main. SHA-256 `a27ca8a38642`.
- `legacy/python_codes/mergemultipleevas.py` — 8205 righe; AST OK; plc_merger_strings.py. Top-level: var _total_bits, var output_json_final. SHA-256 `6f548ce70399`.
- `legacy/python_codes/n2.py` — 230 righe; AST OK; script legacy/utility: ruolo da verificare nel sorgente. Top-level: var input_json, var output_json, var VM_SOURCE_CODE_DEFAULT, var DRIVERCONFIG_MEASURE. SHA-256 `cb9c89f5d85d`.
- `legacy/python_codes/ordinapermodbus.py` — 41 righe; AST OK; script legacy/utility: ruolo da verificare nel sorgente. Top-level: var input_string. SHA-256 `d1942d4880f3`.
- `legacy/python_codes/original_pytool.py` — 923 righe; AST OK; script legacy/utility: ruolo da verificare nel sorgente. Top-level: var input_json, var output_json, var VM_SOURCE_CODE_DEFAULT, var DRIVERCONFIG_MEASURE. SHA-256 `84d003af9316`.
- `legacy/python_codes/pythoncheckgroupkey.py` — 34 righe; AST OK; raggruppamento ingressi digitali. Top-level: var input_json, var final_result_json. SHA-256 `ea823877e55e`.
- `legacy/python_codes/pythoncreatejson.py` — 330 righe; AST OK; trasformazione/aggregazione JSON. Top-level: var input_json, var output_json, var input_json, var VM_SOURCE_CODE_DEFAULT, var DRIVERCONFIG_MEASURE. SHA-256 `4af65b9dbfba`.
- `legacy/python_codes/pythonmergepages.py` — 254 righe; AST OK; merge_pages.py. Top-level: var PAGE_OUTPUTS, var output_json_final. SHA-256 `3eba12e52253`.
- `legacy/python_codes/pythonmultiplefiles.py` — 1647 righe; AST OK; script legacy/utility: ruolo da verificare nel sorgente. Top-level: var VM_SOURCE_CODE_DEFAULT, var DRIVERCONFIG_MEASURE, var input_json. SHA-256 `7cb50c330265`.
- `legacy/python_codes/pythonsorter.py` — 52 righe; AST OK; script legacy/utility: ruolo da verificare nel sorgente. Top-level: var input_string. SHA-256 `b8db137f1d41`.
- `legacy/python_codes/pythonstationsandports.py` — 56 righe; AST OK; estrazione/gestione stazioni. Top-level: var input_json, var output_json. SHA-256 `84618d6ee544`.
- `legacy/python_codes/pythonunionbigfiles.py` — 4478 righe; AST OK; script legacy/utility: ruolo da verificare nel sorgente. Top-level: var input_string. SHA-256 `49c874ea119b`.
- `legacy/python_codes/pythonunionevas.py` — 500 righe; AST OK; plc_merger_strings.py. Top-level: var _total_bits, var output_json_final. SHA-256 `ae7ec1c02d9d`.
- `legacy/python_codes/temp.py` — 328 righe; AST OK; script legacy/utility: ruolo da verificare nel sorgente. Top-level: var input_json, var output_json, var input_json, var VM_SOURCE_CODE_DEFAULT, var DRIVERCONFIG_MEASURE. SHA-256 `f3a21204b0ff`.
- `legacy/python_codes/unionepagine.py` — 702 righe; AST OK; merge_pages.py. Top-level: var PAGE_OUTPUTS, var output_json_final. SHA-256 `0f71bd29339c`.
- `src/__init__.py` — 0 righe; AST OK; script legacy/utility: ruolo da verificare nel sorgente. Top-level: codice inline. SHA-256 `e3b0c44298fc`.
- `src/agents/__init__.py` — 0 righe; AST OK; script legacy/utility: ruolo da verificare nel sorgente. Top-level: codice inline. SHA-256 `e3b0c44298fc`.
- `src/core/__init__.py` — 0 righe; AST OK; script legacy/utility: ruolo da verificare nel sorgente. Top-level: codice inline. SHA-256 `e3b0c44298fc`.
- `src/models/__init__.py` — 57 righe; AST OK; Modelli Pydantic per la validazione degli output del progetto Menerva MAS.. Top-level: codice inline. SHA-256 `9d1ede8ea77f`.
- `src/models/validators.py` — 293 righe; AST OK; Utilità per la validazione degli output VLM e ADAS.. Top-level: class ValidationResult, def safe_validate_vlm, def safe_validate_adas, def print_validation_summary. SHA-256 `b553c064554f`.
- `src/models/vlm_schema.py` — 382 righe; AST OK; Modelli Pydantic per la validazione degli output del VLM (contratto intermedio).. Top-level: class Variable, class Station, class VLMOutput, class MeasureADAS, class BitInfoADAS, class StationADAS, class ADASOutput, def validate_vlm_output. SHA-256 `1c8fe1bd43e0`.
- `src/nodes/__init__.py` — 1 righe; AST OK; script legacy/utility: ruolo da verificare nel sorgente. Top-level: codice inline. SHA-256 `6a0fc0aa30c7`.
- `src/nodes/json_creator.py` — 667 righe; AST OK; trasformazione/aggregazione JSON. Top-level: var VM_DEFAULT. SHA-256 `152ff3001428`.
- `src/nodes/legacy/json_creator_v3.py` — 708 righe; AST OK; trasformazione/aggregazione JSON. Top-level: var VM_DEFAULT. SHA-256 `a116f87907c0`.
- `src/nodes/legacy/json_creator_v4_1.py` — 582 righe; AST OK; trasformazione/aggregazione JSON. Top-level: var VM_DEFAULT. SHA-256 `359f797d40d9`.
- `tests/compare_with_gt.py` — 132 righe; AST OK; compare_with_gt.py - Confronta output MyHydra/pytool (JSON o DOCX) con i ground truth.. Top-level: def extract_text, def parse_json_objects, def reg_from_priv, def fmt_from_priv, def norm_name, def collect, def main. SHA-256 `16dad1470eac`.
- `tests/gaia_legacy/test1-stationinfoip.py` — 1135 righe; AST OK; estrazione/gestione stazioni. Top-level: var input_json, var input_json, var driver_config, var merged_bitinfo, var bitinfo_id_offset, var output. SHA-256 `dc6a9edcf82b`.
- `tests/gaia_legacy/test1_check_bitinfo.py` — 27 righe; AST OK; gestione bitinfo digitali. Top-level: var json_input, var json_input. SHA-256 `57d690fcbe20`.
- `tests/gaia_legacy/test1_check_if_there_are.py` — 952 righe; AST OK; test legacy. Top-level: var input_json, var input_json. SHA-256 `c88c6155c025`.
- `tests/gaia_legacy/test1_check_only_station_infos.py` — 90 righe; AST OK; estrazione/gestione stazioni. Top-level: var input_json, var input_json. SHA-256 `ca7207e74625`.
- `tests/gaia_legacy/test1_filtro_iterativo.py` — 56 righe; AST OK; test legacy. Top-level: var input_json. SHA-256 `4885b967f298`.
- `tests/gaia_legacy/test1_ipconfigs.py` — 594 righe; AST OK; test legacy. Top-level: var input_json, var input_json, var output. SHA-256 `6104060d823a`.
- `tests/gaia_legacy/test1_json_bitinfo.py` — 20 righe; AST OK; trasformazione/aggregazione JSON. Top-level: var input_json. SHA-256 `20b4252a2e94`.
- `tests/gaia_legacy/test1_json_creator.py` — 1200 righe; AST OK; trasformazione/aggregazione JSON. Top-level: var input_json, var output_json, var input_json, var VM_SOURCE_CODE_DEFAULT, var DRIVERCONFIG_MEASURE. SHA-256 `ff3c18dea16c`.
- `tests/gaia_legacy/test1_json_remove_bitinfo_num.py` — 23 righe; AST OK; trasformazione/aggregazione JSON. Top-level: var input_json. SHA-256 `b5d08bdce5bb`.
- `tests/gaia_legacy/test1_last_python.py` — 1242 righe; AST OK; test legacy. Top-level: codice inline. SHA-256 `a2a40c603df6`.
- `tests/gaia_legacy/test1_recoverybitname.py` — 436 righe; AST OK; gestione bitinfo digitali. Top-level: var json_input, var json_input. SHA-256 `71ec767d5ba5`.
- `tests/gaia_legacy/test1_remove_tech_info.py` — 26 righe; AST OK; test legacy. Top-level: def pulisci_e_carica_json. SHA-256 `8fcbc8275e37`.
- `tests/gaia_legacy/test1_stationinfo_json_key.py` — 1542 righe; AST OK; trasformazione/aggregazione JSON. Top-level: var input_json, var input_json, var driver_config, var merged_bitinfo, var bitinfo_id_offset, var output. SHA-256 `a6f173d79fc8`.
- `tests/run_fixture.py` — 94 righe; AST OK; Runner per testare json_creator.py contro una fixture VLM reale.. Top-level: codice inline. SHA-256 `a8b1e1f074dc`.
- `tests/run_json_creator.py` — 29 righe; AST OK; Runner per testare src/nodes/json_creator.py con un fixture realistico.. Top-level: codice inline. SHA-256 `0625e48045e3`.
- `tests/test_multipage.py` — 334 righe; AST OK; Test multi-pagina per src/nodes/json_creator.py (v3).. Top-level: def run_script, def check, def make_vlm_chunk, def ana, def digit_single, def digit_packed, var bitnos, var raw_jsonl. SHA-256 `bf15c9a3f8cc`.
- `tests/test_pydantic_models.py` — 416 righe; AST OK; Test di validazione per i modelli Pydantic.. Top-level: var VLM_OUTPUT_PROTEC_1, var ADAS_OUTPUT_PROTEC_1, def test_vlm_validation, def test_adas_validation, def test_invalid_data, def test_edge_cases. SHA-256 `98e96cc70c0f`.

Duplicati binari Python:
- `e3b0c44298fc`: `src/__init__.py`, `src/agents/__init__.py`, `src/core/__init__.py`

## JSON (49 file)

Parsing, forma esterna e conteggi dei campi standard eseguiti su tutti i file. Un conteggio non certifica che il contenuto sia corretto rispetto al PDF sorgente.

- `data/test_inputs/Mappatura_1_Cliente_SMA_1.json` — JSON valido, top-level `dict`, voci 1, stazioni ADAS 1, measures 51, bitinfo 0, variables VLM 0; chiavi esterne: ADDRESS, ALARMSNAPSHOT, AREACODE, CODE, CRITICSNAPSHOT, DOWNLOADPROGRAM, DOWNLOADTYPE, DRIVERCONFIG, DRIVERNAME, DRIVERPRIVATE, EVENTCODE, EVENTORIGIN, EVENTTIME, ID; 48454 byte; SHA-256 `68b363686131`.
- `data/test_inputs/Mappatura_2_Cliente_PROTECT_1.json` — JSON valido, top-level `dict`, voci 1, stazioni ADAS 1, measures 8, bitinfo 36, variables VLM 0; chiavi esterne: ADDRESS, ALARMSNAPSHOT, AREACODE, CODE, CRITICSNAPSHOT, DOWNLOADPROGRAM, DOWNLOADTYPE, DRIVERCONFIG, DRIVERNAME, DRIVERPRIVATE, EVENTCODE, EVENTORIGIN, EVENTTIME, ID; 13633 byte; SHA-256 `98e65ea1481f`.
- `data/test_inputs/Mappatura_2_Cliente_PROTEC_1.json` — JSON valido, top-level `dict`, voci 1, stazioni ADAS 1, measures 8, bitinfo 35, variables VLM 0; chiavi esterne: ADDRESS, ALARMSNAPSHOT, AREACODE, CODE, CRITICSNAPSHOT, DOWNLOADPROGRAM, DOWNLOADTYPE, DRIVERCONFIG, DRIVERNAME, DRIVERPRIVATE, EVENTCODE, EVENTORIGIN, EVENTTIME, ID; 13452 byte; SHA-256 `e7b4cb994231`.
- `data/test_inputs/Mappatura_3_Cliente_PROTEC_2.json` — JSON valido, top-level `dict`, voci 1, stazioni ADAS 1, measures 19, bitinfo 24, variables VLM 0; chiavi esterne: ADDRESS, ALARMSNAPSHOT, AREACODE, CODE, CRITICSNAPSHOT, DOWNLOADPROGRAM, DOWNLOADTYPE, DRIVERCONFIG, DRIVERNAME, DRIVERPRIVATE, EVENTCODE, EVENTORIGIN, EVENTTIME, ID; 22636 byte; SHA-256 `1eef4737e6db`.
- `data/test_inputs/Mappatura_4_Cliente_SIEMENS_2-1-15_splitted.json` — JSON valido, top-level `dict`, voci 1, stazioni ADAS 1, measures 29, bitinfo 300, variables VLM 0; chiavi esterne: ADDRESS, ALARMSNAPSHOT, AREACODE, CODE, CRITICSNAPSHOT, DOWNLOADPROGRAM, DOWNLOADTYPE, DRIVERCONFIG, DRIVERNAME, DRIVERPRIVATE, EVENTCODE, EVENTORIGIN, EVENTTIME, ID; 73791 byte; SHA-256 `c047f7e41a8a`.
- `data/test_inputs/Mappatura_4_Cliente_SIEMENS_2.json` — JSON valido, top-level `dict`, voci 1, stazioni ADAS 1, measures 148, bitinfo 211, variables VLM 0; chiavi esterne: ADDRESS, ALARMSNAPSHOT, AREACODE, CODE, CRITICSNAPSHOT, DOWNLOADPROGRAM, DOWNLOADTYPE, DRIVERCONFIG, DRIVERNAME, DRIVERPRIVATE, EVENTCODE, EVENTORIGIN, EVENTTIME, ID; 179701 byte; SHA-256 `fc899b6d70fa`.
- `data/test_inputs/Mappatura_4_Cliente_SIEMENS_2_NUM2.json` — JSON valido, top-level `dict`, voci 1, stazioni ADAS 1, measures 108, bitinfo 211, variables VLM 0; chiavi esterne: ADDRESS, ALARMSNAPSHOT, AREACODE, CODE, CRITICSNAPSHOT, DOWNLOADPROGRAM, DOWNLOADTYPE, DRIVERCONFIG, DRIVERNAME, DRIVERPRIVATE, EVENTCODE, EVENTORIGIN, EVENTTIME, ID; 141059 byte; SHA-256 `44f636f3696a`.
- `data/test_inputs/Mappatura_6_Cliente_SMI_1.json` — JSON valido, top-level `dict`, voci 1, stazioni ADAS 1, measures 23, bitinfo 51, variables VLM 0; chiavi esterne: ADDRESS, ALARMSNAPSHOT, AREACODE, CODE, CRITICSNAPSHOT, DOWNLOADPROGRAM, DOWNLOADTYPE, DRIVERCONFIG, DRIVERNAME, DRIVERPRIVATE, EVENTCODE, EVENTORIGIN, EVENTTIME, ID; 31300 byte; SHA-256 `d0a04d61b390`.
- `data/test_inputs/Mappatura_7_Cliente_SMI_2.json` — JSON valido, top-level `dict`, voci 1, stazioni ADAS 1, measures 39, bitinfo 71, variables VLM 0; chiavi esterne: ADDRESS, ALARMSNAPSHOT, AREACODE, CODE, CRITICSNAPSHOT, DOWNLOADPROGRAM, DOWNLOADTYPE, DRIVERCONFIG, DRIVERNAME, DRIVERPRIVATE, EVENTCODE, EVENTORIGIN, EVENTTIME, ID; 50919 byte; SHA-256 `b38d547b44be`.
- `data/test_inputs/legacy_examplejson.json` — JSON valido, top-level `list`, voci 1, stazioni ADAS 1, measures 10, bitinfo 39, variables VLM 0; chiavi esterne: ADDRESS, ALARMSNAPSHOT, AREACODE, CODE, CRITICSNAPSHOT, DOWNLOADPROGRAM, DOWNLOADTYPE, DRIVERCONFIG, DRIVERNAME, DRIVERPRIVATE, EVENTCODE, EVENTORIGIN, EVENTTIME, ID; 21765 byte; SHA-256 `345d1a3baa05`.
- `data/test_inputs/vlm_raw/PROTEC_1_2pages.json` — JSON valido, top-level `list`, voci 2, stazioni ADAS 0, measures 0, bitinfo 0, variables VLM 45; chiavi esterne: stations; 15321 byte; SHA-256 `089626c30ae1`.
- `data/test_outputs/Json_2_Cliente_PROTEC_1.json` — JSON valido, top-level `dict`, voci 1, stazioni ADAS 1, measures 10, bitinfo 40, variables VLM 0; chiavi esterne: ADDRESS, ALARMSNAPSHOT, AREACODE, CODE, CRITICSNAPSHOT, DOWNLOADPROGRAM, DOWNLOADTYPE, DRIVERCONFIG, DRIVERNAME, DRIVERPRIVATE, EVENTCODE, EVENTORIGIN, EVENTTIME, ID; 19733 byte; SHA-256 `088195b8e2bd`.
- `data/test_outputs/Json_4_Cliente_SIEMENS_2.json` — JSON valido, top-level `dict`, voci 1, stazioni ADAS 1, measures 108, bitinfo 206, variables VLM 0; chiavi esterne: ADDRESS, ALARMSNAPSHOT, AREACODE, CODE, CRITICSNAPSHOT, DOWNLOADPROGRAM, DOWNLOADTYPE, DRIVERCONFIG, DRIVERNAME, DRIVERPRIVATE, EVENTCODE, EVENTORIGIN, EVENTTIME, ID; 170186 byte; SHA-256 `9d8d2ef770ba`.
- `data/test_outputs/gaia_ctm_rivoli.json` — JSON valido, top-level `list`, voci 1, stazioni ADAS 1, measures 27, bitinfo 37, variables VLM 0; chiavi esterne: ADDRESS, ALARMSNAPSHOT, AREACODE, CODE, CRITICSNAPSHOT, DOWNLOADPROGRAM, DOWNLOADTYPE, DRIVERCONFIG, DRIVERNAME, DRIVERPRIVATE, EVENTCODE, EVENTORIGIN, EVENTTIME, ID; 43039 byte; SHA-256 `00f036be3a14`.
- `data/test_outputs/gaia_doublefile_result_6.json` — JSON valido, top-level `list`, voci 1, stazioni ADAS 1, measures 22, bitinfo 78, variables VLM 0; chiavi esterne: ADDRESS, ALARMSNAPSHOT, AREACODE, CODE, CRITICSNAPSHOT, DOWNLOADPROGRAM, DOWNLOADTYPE, DRIVERCONFIG, DRIVERNAME, DRIVERPRIVATE, EVENTCODE, EVENTORIGIN, EVENTTIME, ID; 45198 byte; SHA-256 `6b90a91bbedb`.
- `data/test_outputs/gaia_doublefile_result_7.json` — JSON valido, top-level `list`, voci 1, stazioni ADAS 1, measures 44, bitinfo 47, variables VLM 0; chiavi esterne: ADDRESS, ALARMSNAPSHOT, AREACODE, CODE, CRITICSNAPSHOT, DOWNLOADPROGRAM, DOWNLOADTYPE, DRIVERCONFIG, DRIVERNAME, DRIVERPRIVATE, EVENTCODE, EVENTORIGIN, EVENTTIME, ID; 68985 byte; SHA-256 `16a7211dab63`.
- `data/test_outputs/gaia_intermedio_6.json` — JSON valido, top-level `list`, voci 1, stazioni ADAS 1, measures 22, bitinfo 68, variables VLM 0; chiavi esterne: ADDRESS, ALARMSNAPSHOT, AREACODE, CODE, CRITICSNAPSHOT, DOWNLOADPROGRAM, DOWNLOADTYPE, DRIVERCONFIG, DRIVERNAME, DRIVERPRIVATE, EVENTCODE, EVENTORIGIN, EVENTTIME, ID; 43208 byte; SHA-256 `8c63af780906`.
- `data/test_outputs/gaia_mede1_iterative_node.json` — NON valido come JSON standard: JSONDecodeError (Expecting property name enclosed in double quotes: line 1 column 49 (char 48)); 59 byte; SHA-256 `7066bff26649`.
- `data/test_outputs/gaia_mede2_iterative_nove.json` — NON valido come JSON standard: JSONDecodeError (Expecting property name enclosed in double quotes: line 1 column 49 (char 48)); 59 byte; SHA-256 `eaad92250004`.
- `data/test_outputs/gaia_medex1.json` — NON valido come JSON standard: JSONDecodeError (Extra data: line 1 column 31 (char 30)); 40 byte; SHA-256 `bc78e4f955e0`.
- `data/test_outputs/gaia_medex2.json` — NON valido come JSON standard: JSONDecodeError (Extra data: line 1 column 53 (char 52)); 67 byte; SHA-256 `fca97b81de4f`.
- `data/test_outputs/gaia_result_1.json` — JSON valido, top-level `list`, voci 2, stazioni ADAS 2, measures 50, bitinfo 30, variables VLM 0; chiavi esterne: ADDRESS, ALARMSNAPSHOT, AREACODE, CODE, CRITICSNAPSHOT, DOWNLOADPROGRAM, DOWNLOADTYPE, DRIVERCONFIG, DRIVERNAME, DRIVERPRIVATE, EVENTCODE, EVENTORIGIN, EVENTTIME, ID; 56582 byte; SHA-256 `5f0cb4984b27`.
- `data/test_outputs/gaia_result_2.json` — JSON valido, top-level `list`, voci 1, stazioni ADAS 1, measures 8, bitinfo 36, variables VLM 0; chiavi esterne: ADDRESS, ALARMSNAPSHOT, AREACODE, CODE, CRITICSNAPSHOT, DOWNLOADPROGRAM, DOWNLOADTYPE, DRIVERCONFIG, DRIVERNAME, DRIVERPRIVATE, EVENTCODE, EVENTORIGIN, EVENTTIME, ID; 14766 byte; SHA-256 `54664e19e5bc`.
- `data/test_outputs/gaia_result_3.json` — JSON valido, top-level `list`, voci 1, stazioni ADAS 1, measures 19, bitinfo 24, variables VLM 0; chiavi esterne: ADDRESS, ALARMSNAPSHOT, AREACODE, CODE, CRITICSNAPSHOT, DOWNLOADPROGRAM, DOWNLOADTYPE, DRIVERCONFIG, DRIVERNAME, DRIVERPRIVATE, EVENTCODE, EVENTORIGIN, EVENTTIME, ID; 24199 byte; SHA-256 `398717c64a37`.
- `data/test_outputs/gaia_result_4.json` — JSON valido, top-level `list`, voci 1, stazioni ADAS 1, measures 339, bitinfo 209, variables VLM 0; chiavi esterne: ADDRESS, ALARMSNAPSHOT, AREACODE, CODE, CRITICSNAPSHOT, DOWNLOADPROGRAM, DOWNLOADTYPE, DRIVERCONFIG, DRIVERNAME, DRIVERPRIVATE, EVENTCODE, EVENTORIGIN, EVENTTIME, ID; 390479 byte; SHA-256 `80044124656e`.
- `data/test_outputs/gaia_result_4_1-15.json` — JSON valido, top-level `list`, voci 1, stazioni ADAS 1, measures 22, bitinfo 209, variables VLM 0; chiavi esterne: ADDRESS, ALARMSNAPSHOT, AREACODE, CODE, CRITICSNAPSHOT, DOWNLOADPROGRAM, DOWNLOADTYPE, DRIVERCONFIG, DRIVERNAME, DRIVERPRIVATE, EVENTCODE, EVENTORIGIN, EVENTTIME, ID; 58896 byte; SHA-256 `4f487fabe7b8`.
- `data/test_outputs/gaia_result_4_1-3.json` — JSON valido, top-level `list`, voci 1, stazioni ADAS 1, measures 2, bitinfo 18, variables VLM 0; chiavi esterne: ADDRESS, ALARMSNAPSHOT, AREACODE, CODE, CRITICSNAPSHOT, DOWNLOADPROGRAM, DOWNLOADTYPE, DRIVERCONFIG, DRIVERNAME, DRIVERPRIVATE, EVENTCODE, EVENTORIGIN, EVENTTIME, ID; 6091 byte; SHA-256 `58a5bc0771da`.
- `data/test_outputs/legacy_6pagesaftervision.json` — JSON valido, top-level `list`, voci 1, stazioni ADAS 0, measures 0, bitinfo 0, variables VLM 0; chiavi esterne: nessuna rilevata; 8983 byte; SHA-256 `afc40c393104`.
- `data/test_outputs/legacy_merged_sme.json` — JSON valido, top-level `list`, voci 1, stazioni ADAS 0, measures 0, bitinfo 0, variables VLM 0; chiavi esterne: nessuna rilevata; 74806 byte; SHA-256 `d365212e842c`.
- `data/test_outputs/legacy_multifilesvisio.json` — JSON valido, top-level `list`, voci 2, stazioni ADAS 0, measures 0, bitinfo 0, variables VLM 0; chiavi esterne: _params, _subkey; 57745 byte; SHA-256 `e92a204668ce`.
- `data/test_outputs/legacy_postbitnotest.json` — JSON valido, top-level `dict`, voci 1, stazioni ADAS 1, measures 34, bitinfo 52, variables VLM 0; chiavi esterne: ADDRESS, ALARMSNAPSHOT, AREACODE, CODE, CRITICSNAPSHOT, DOWNLOADPROGRAM, DOWNLOADTYPE, DRIVERCONFIG, DRIVERNAME, DRIVERPRIVATE, EVENTCODE, EVENTORIGIN, EVENTTIME, ID; 42370 byte; SHA-256 `84591c5e8a03`.
- `data/test_outputs/legacy_sortedwithmodbus.json` — JSON valido, top-level `list`, voci 2, stazioni ADAS 2, measures 41, bitinfo 575, variables VLM 0; chiavi esterne: DRIVERCONFIG, DRIVERNAME, ID, NAME, bitinfo, measures; 135663 byte; SHA-256 `f789f7a569f8`.
- `data/test_outputs/localoutput28page.json` — JSON valido, top-level `list`, voci 29, stazioni ADAS 29, measures 617, bitinfo 330, variables VLM 0; chiavi esterne: DRIVERCONFIG, DRIVERNAME, ID, NAME, bitinfo, measures; 255918 byte; SHA-256 `f7b07cacd314`.
- `data/test_outputs/localoutput28page1.json` — JSON valido, top-level `list`, voci 1, stazioni ADAS 1, measures 370, bitinfo 330, variables VLM 0; chiavi esterne: DRIVERCONFIG, DRIVERNAME, ID, NAME, bitinfo, measures; 182980 byte; SHA-256 `64afa8f9a49a`.
- `data/test_outputs/localoutput28page2.json` — JSON valido, top-level `dict`, voci 1, stazioni ADAS 1, measures 309, bitinfo 330, variables VLM 0; chiavi esterne: ADDRESS, ALARMSNAPSHOT, AREACODE, CODE, CRITICSNAPSHOT, DOWNLOADPROGRAM, DOWNLOADTYPE, DRIVERCONFIG, DRIVERNAME, DRIVERPRIVATE, EVENTCODE, EVENTORIGIN, EVENTTIME, ID; 422387 byte; SHA-256 `1363b5264072`.
- `data/test_outputs/menerva_outputs.json` — NON valido come JSON standard: JSONDecodeError (Expecting ',' delimiter: line 6 column 41 (char 128)); 23038 byte; SHA-256 `6cadc465e1b2`.
- `data/test_outputs/multipleevasoutput.json` — JSON valido, top-level `list`, voci 2, stazioni ADAS 2, measures 41, bitinfo 575, variables VLM 0; chiavi esterne: DRIVERCONFIG, DRIVERNAME, ID, NAME, bitinfo, measures; 135663 byte; SHA-256 `de39f92441f9`.
- `data/test_outputs/output_multiple_files.json` — JSON valido, top-level `dict`, voci 1, stazioni ADAS 1, measures 22, bitinfo 52, variables VLM 0; chiavi esterne: ADDRESS, ALARMSNAPSHOT, AREACODE, CODE, CRITICSNAPSHOT, DOWNLOADPROGRAM, DOWNLOADTYPE, DRIVERCONFIG, DRIVERNAME, DRIVERPRIVATE, EVENTCODE, EVENTORIGIN, EVENTTIME, ID; 36647 byte; SHA-256 `649ca5485c78`.
- `data/test_outputs/output_new_format.json` — JSON valido, top-level `dict`, voci 1, stazioni ADAS 1, measures 28, bitinfo 55, variables VLM 0; chiavi esterne: ADDRESS, ALARMSNAPSHOT, AREACODE, CODE, CRITICSNAPSHOT, DOWNLOADPROGRAM, DOWNLOADTYPE, DRIVERCONFIG, DRIVERNAME, DRIVERPRIVATE, EVENTCODE, EVENTORIGIN, EVENTTIME, ID; 42783 byte; SHA-256 `1f9edfdafc10`.
- `data/test_outputs/outputljsonmultiplefiles.json` — JSON valido, top-level `list`, voci 5, stazioni ADAS 0, measures 0, bitinfo 0, variables VLM 0; chiavi esterne: nessuna rilevata; 59453 byte; SHA-256 `50aaff677d99`.
- `data/test_outputs/outputlocaljson.json` — JSON valido, top-level `dict`, voci 1, stazioni ADAS 1, measures 41, bitinfo 575, variables VLM 0; chiavi esterne: ADDRESS, ALARMSNAPSHOT, AREACODE, CODE, CRITICSNAPSHOT, DOWNLOADPROGRAM, DOWNLOADTYPE, DRIVERCONFIG, DRIVERNAME, DRIVERPRIVATE, EVENTCODE, EVENTORIGIN, EVENTTIME, ID; 153499 byte; SHA-256 `db2fbb0dd7cb`.
- `data/test_outputs/outputmodelloantonello.json` — JSON valido, top-level `list`, voci 2, stazioni ADAS 0, measures 0, bitinfo 0, variables VLM 0; chiavi esterne: _params, _subkey; 44082 byte; SHA-256 `8d928e23ecec`.
- `data/test_outputs/outputmultipleevamyhydra.json` — JSON valido, top-level `list`, voci 499, stazioni ADAS 0, measures 0, bitinfo 0, variables VLM 0; chiavi esterne: BITNAME, BITNO, MEASUREID, TEXTOFF, TEXTON; 67431 byte; SHA-256 `4fa91e2f68ad`.
- `data/test_outputs/outputmyhydra.json` — JSON valido, top-level `list`, voci 3, stazioni ADAS 0, measures 0, bitinfo 0, variables VLM 0; chiavi esterne: nessuna rilevata; 62817 byte; SHA-256 `cb6570c182b3`.
- `data/test_outputs/outputvisio.json` — NON valido come JSON standard: JSONDecodeError (Expecting ',' delimiter: line 6 column 41 (char 145)); 34142 byte; SHA-256 `a0930179b8e2`.
- `data/test_outputs/outputvisiopiufiles.json` — JSON valido, top-level `list`, voci 4, stazioni ADAS 0, measures 0, bitinfo 0, variables VLM 0; chiavi esterne: nessuna rilevata; 47304 byte; SHA-256 `eac8c8ff9926`.
- `data/test_outputs/python_output.json` — NON valido come JSON standard: JSONDecodeError (Expecting ',' delimiter: line 27 column 37 (char 739)); 21632 byte; SHA-256 `a53b65e76dba`.
- `legacy/python_codes/outputpython.json` — JSON valido, top-level `dict`, voci 1, stazioni ADAS 1, measures 297, bitinfo 290, variables VLM 0; chiavi esterne: ADDRESS, ALARMSNAPSHOT, AREACODE, CODE, CRITICSNAPSHOT, DOWNLOADPROGRAM, DOWNLOADTYPE, DRIVERCONFIG, DRIVERNAME, DRIVERPRIVATE, EVENTCODE, EVENTORIGIN, EVENTTIME, ID; 337776 byte; SHA-256 `47a9497e6675`.
- `tests/gaia_legacy/testlocaljsoninput.json` — JSON valido, top-level `list`, voci 1, stazioni ADAS 1, measures 52, bitinfo 40, variables VLM 0; chiavi esterne: DRIVERCONFIG, DRIVERNAME, ID, NAME, bitinfo, measures; 18905 byte; SHA-256 `349ade0c7e89`.

JSON da trattare come frammento/non standard: `data/test_outputs/gaia_mede1_iterative_node.json`, `data/test_outputs/gaia_mede2_iterative_nove.json`, `data/test_outputs/gaia_medex1.json`, `data/test_outputs/gaia_medex2.json`, `data/test_outputs/menerva_outputs.json`, `data/test_outputs/outputvisio.json`, `data/test_outputs/python_output.json`.

## PDF (88 file)

Per ogni file sono verificati apertura, pagine, quantità di testo estraibile e SHA-256. I frammenti numerici delle pagine Siemens/SMI sono estratti/ritagli alternativi, non nuovi documenti sorgente. PDF senza testo estraibile richiedono revisione visiva/OCR.

- `data/test_inputs/Mappatura_1_Cliente_SMA_1.pdf` — 1 pagine; 4292 caratteri estraibili; 289478 byte; SHA-256 `28e1d3faf3b5`.
- `data/test_inputs/Mappatura_2_Cliente_PROTEC_1.pdf` — 2 pagine; 4576 caratteri estraibili; 267590 byte; SHA-256 `6fb0abec991e`.
- `data/test_inputs/Mappatura_3_Cliente_PROTEC_2.pdf` — 2 pagine; 4263 caratteri estraibili; 175240 byte; SHA-256 `b72049e7703c`.
- `data/test_inputs/Mappatura_6_Cliente_SMI_1.pdf` — non leggibile: Cannot open empty file: filename='data/test_inputs/Mappatura_6_Cliente_SMI_1.pdf'.; 0 byte; SHA-256 `e3b0c44298fc`.
- `data/test_inputs/Mappature/Doppio PDF/CTM Rivoli/IOL.0177.25.pdf` — 4 pagine; 7173 caratteri estraibili; JOB ref: JOB.0177.25; IOL ref: IOL.0177.25; 366734 byte; SHA-256 `2a177cf8d877`.
- `data/test_inputs/Mappature/Doppio PDF/CTM Rivoli/JOB.0177.25.pdf` — 23 pagine; 29673 caratteri estraibili; JOB ref: JOB.0148.24/JOB.0177.25/JOB.0177.25.; IOL ref: IOL.0177.25.; 2388451 byte; SHA-256 `331f8e982fbb`.
- `data/test_inputs/Mappature/Doppio PDF/Ospedale San Marco Catania/IOL.0007.18.02.pdf` — 7 pagine; 12593 caratteri estraibili; JOB ref: JOB.0187.25; IOL ref: IOL.0187.25; 674082 byte; SHA-256 `1ad17e5b284f`.
- `data/test_inputs/Mappature/Doppio PDF/Ospedale San Marco Catania/JOB.0007.18.pdf` — 21 pagine; 28099 caratteri estraibili; JOB ref: JOB.0007.18/JOB.0007.18.; IOL ref: IOL.0007.18..01/IOL.0007.18.02/IOL.0007.18.02.; 2679392 byte; SHA-256 `0546ce14d69b`.
- `data/test_inputs/Mappature/Singolo/Cliente_PROTEC.pdf` — 3 pagine; 5772 caratteri estraibili; 203643 byte; SHA-256 `de18fb9fb6db`.
- `data/test_inputs/Mappature/Singolo/Cliente_SIEMENS.pdf` — 29 pagine; 79817 caratteri estraibili; 180592 byte; SHA-256 `d57a8b58ad2a`.
- `data/test_outputs/Mappatura_2_Cliente_PROTEC_1.pdf` — 2 pagine; 4576 caratteri estraibili; 267590 byte; SHA-256 `6fb0abec991e`.
- `data/test_outputs/Mappatura_4_Cliente_SIEMENS_2.pdf` — 29 pagine; 70297 caratteri estraibili; 202472 byte; SHA-256 `354c2b28ac79`.
- `docs/architettura/Manuale sviluppo linguaggio Manager rev03.pdf` — 37 pagine; 49328 caratteri estraibili; 1576810 byte; SHA-256 `7517ff6232df`.
- `docs/protocolli/clienti_extra/Biogen/IOL.0105.22.pdf` — 4 pagine; 7611 caratteri estraibili; JOB ref: JOB.0105.22; IOL ref: IOL.0105.22; 318388 byte; SHA-256 `8cbd851e3e82`.
- `docs/protocolli/clienti_extra/Biogen/JOB.0105.22.pdf` — 7 pagine; 14016 caratteri estraibili; JOB ref: JOB.0105.22/JOB.0105.22.; IOL ref: IOL.0105.22.; 558093 byte; SHA-256 `90d4d0b58798`.
- `docs/protocolli/clienti_extra/CTM Rivoli/IOL.0177.25-1-2.pdf` — 2 pagine; 4026 caratteri estraibili; JOB ref: JOB.0177.25; IOL ref: IOL.0177.25; 291633 byte; SHA-256 `abf492cd8b10`.
- `docs/protocolli/clienti_extra/CTM Rivoli/IOL.0177.25-2-4.pdf` — 3 pagine; 6172 caratteri estraibili; JOB ref: JOB.0177.25; IOL ref: IOL.0177.25; 271580 byte; SHA-256 `6df4f32e2eaf`.
- `docs/protocolli/clienti_extra/CTM Rivoli/IOL.0177.25-2.pdf` — 1 pagine; 3025 caratteri estraibili; JOB ref: JOB.0177.25; IOL ref: IOL.0177.25; 198231 byte; SHA-256 `faddc7dd76ae`.
- `docs/protocolli/clienti_extra/CTM Rivoli/IOL.0177.25-3-4.pdf` — 2 pagine; 3147 caratteri estraibili; JOB ref: JOB.0177.25; IOL ref: IOL.0177.25; 194114 byte; SHA-256 `841f836cab9d`.
- `docs/protocolli/clienti_extra/CTM Rivoli/IOL.0177.25.pdf` — 4 pagine; 7173 caratteri estraibili; JOB ref: JOB.0177.25; IOL ref: IOL.0177.25; 366734 byte; SHA-256 `2a177cf8d877`.
- `docs/protocolli/clienti_extra/CTM Rivoli/JOB.0177.25-2-5.pdf` — 4 pagine; 6134 caratteri estraibili; JOB ref: JOB.0148.24/JOB.0177.25/JOB.0177.25.; 529838 byte; SHA-256 `22fa38b22e5c`.
- `docs/protocolli/clienti_extra/CTM Rivoli/JOB.0177.25-9.pdf` — 1 pagine; 1792 caratteri estraibili; JOB ref: JOB.0177.25/JOB.0177.25.; IOL ref: IOL.0177.25.; 253644 byte; SHA-256 `eaa572dbdd33`.
- `docs/protocolli/clienti_extra/CTM Rivoli/JOB.0177.25.pdf` — 23 pagine; 29673 caratteri estraibili; JOB ref: JOB.0148.24/JOB.0177.25/JOB.0177.25.; IOL ref: IOL.0177.25.; 2388451 byte; SHA-256 `331f8e982fbb`.
- `docs/protocolli/clienti_extra/Ospedale San Marco Catania/IOL.0007.18.02.pdf` — 7 pagine; 12593 caratteri estraibili; JOB ref: JOB.0187.25; IOL ref: IOL.0187.25; 674082 byte; SHA-256 `1ad17e5b284f`.
- `docs/protocolli/clienti_extra/Ospedale San Marco Catania/JOB.0007.18.pdf` — 21 pagine; 28099 caratteri estraibili; JOB ref: JOB.0007.18/JOB.0007.18.; IOL ref: IOL.0007.18..01/IOL.0007.18.02/IOL.0007.18.02.; 2679392 byte; SHA-256 `0546ce14d69b`.
- `docs/protocolli/clienti_extra/essity/IOL.0188.25.pdf` — 9 pagine; 16322 caratteri estraibili; JOB ref: JOB.0188.25; IOL ref: IOL.0188.25; 801371 byte; SHA-256 `b332ee9a1ebf`.
- `docs/protocolli/clienti_extra/essity/JOB.0188.25.pdf` — 22 pagine; 24873 caratteri estraibili; JOB ref: JOB.0188.25/JOB.0188.25.; IOL ref: IOL.0188.25.; 1870173 byte; SHA-256 `7ab5686e5cd1`.
- `docs/protocolli/clienti_extra/luxottica/LUXOTTICA_AGORDO_25_SETTEMBRE_2024.pdf` — 22 pagine; 48287 caratteri estraibili; 195387 byte; SHA-256 `9ec4c6999022`.
- `docs/protocolli/clienti_extra/ori martin/Scambio Modbus_ DB10_V1.pdf` — 3 pagine; 5772 caratteri estraibili; 203643 byte; SHA-256 `de18fb9fb6db`.
- `docs/protocolli/clienti_extra/superwatt/Mappatura DB10 Scambio ADAS.pdf` — 4 pagine; 9094 caratteri estraibili; 266896 byte; SHA-256 `1b71b53390a8`.
- `docs/protocolli/mappature/Mappatura_1_Cliente_SMA_1.pdf` — 1 pagine; 4292 caratteri estraibili; 289478 byte; SHA-256 `28e1d3faf3b5`.
- `docs/protocolli/mappature/Mappatura_2_Cliente_PROTEC_1.pdf` — 2 pagine; 4576 caratteri estraibili; 267590 byte; SHA-256 `6fb0abec991e`.
- `docs/protocolli/mappature/Mappatura_3_Cliente_PROTEC_2.pdf` — 2 pagine; 4263 caratteri estraibili; 175240 byte; SHA-256 `b72049e7703c`.
- `docs/protocolli/mappature/Mappatura_4_Cliente_SIEMENS_2-1-15_splitted-1-3.pdf` — 3 pagine; 6532 caratteri estraibili; 142494 byte; SHA-256 `2a904c5c2f45`.
- `docs/protocolli/mappature/Mappatura_4_Cliente_SIEMENS_2-1-15_splitted-1-4.pdf` — 4 pagine; 8932 caratteri estraibili; 145195 byte; SHA-256 `62cd404ff4f9`.
- `docs/protocolli/mappature/Mappatura_4_Cliente_SIEMENS_2-1-15_splitted.pdf` — 15 pagine; 34048 caratteri estraibili; 169042 byte; SHA-256 `fbea6086d4d9`.
- `docs/protocolli/mappature/Mappatura_4_Cliente_SIEMENS_2-13-14.pdf` — 2 pagine; 3802 caratteri estraibili; 83644 byte; SHA-256 `4732b8fe4161`.
- `docs/protocolli/mappature/Mappatura_4_Cliente_SIEMENS_2-13.pdf` — 1 pagine; 1811 caratteri estraibili; 82290 byte; SHA-256 `7ec465f5798d`.
- `docs/protocolli/mappature/Mappatura_4_Cliente_SIEMENS_2-15-29_second_split-5-8-2.pdf` — 1 pagine; 1679 caratteri estraibili; 82191 byte; SHA-256 `408617194673`.
- `docs/protocolli/mappature/Mappatura_4_Cliente_SIEMENS_2-15-29_second_split-5-8.pdf` — 4 pagine; 10963 caratteri estraibili; 88341 byte; SHA-256 `c7ab7410fcd6`.
- `docs/protocolli/mappature/Mappatura_4_Cliente_SIEMENS_2-15-29_second_split.pdf` — 15 pagine; 39880 caratteri estraibili; 107932 byte; SHA-256 `f716928fe3f0`.
- `docs/protocolli/mappature/Mappatura_4_Cliente_SIEMENS_2-7-29.pdf` — 23 pagine; 57265 caratteri estraibili; 123690 byte; SHA-256 `aa51faacff66`.
- `docs/protocolli/mappature/Mappatura_4_Cliente_SIEMENS_2.pdf` — 29 pagine; 70297 caratteri estraibili; 202472 byte; SHA-256 `354c2b28ac79`.
- `docs/protocolli/mappature/Mappatura_4_pagina-12.pdf` — 1 pagine; 3062 caratteri estraibili; 83804 byte; SHA-256 `cadbf6ebc5ea`.
- `docs/protocolli/mappature/Mappatura_5_Cliente_SIEMENS_1.pdf` — 36 pagine; 24096 caratteri estraibili; 66821 byte; SHA-256 `1073b622f9b0`.
- `docs/protocolli/mappature/Mappatura_6_Cliente_SMI_1-1-3.pdf` — 3 pagine; 7299 caratteri estraibili; JOB ref: JOB.0139.23; IOL ref: IOL.0139.23; 538966 byte; SHA-256 `b5f44af14aef`.
- `docs/protocolli/mappature/Mappatura_6_Cliente_SMI_1-1.pdf` — 1 pagine; 1758 caratteri estraibili; JOB ref: JOB.0139.23; IOL ref: IOL.0139.23; 357482 byte; SHA-256 `d61d27152ae7`.
- `docs/protocolli/mappature/Mappatura_6_Cliente_SMI_1-2-3.pdf` — 2 pagine; 5541 caratteri estraibili; JOB ref: JOB.0139.23; IOL ref: IOL.0139.23; 269323 byte; SHA-256 `b5d52a276f83`.
- `docs/protocolli/mappature/Mappatura_6_Cliente_SMI_1-2-4-2.pdf` — 1 pagine; 2542 caratteri estraibili; JOB ref: JOB.0139.23; IOL ref: IOL.0139.23; 191056 byte; SHA-256 `22fc79c669d3`.
- `docs/protocolli/mappature/Mappatura_6_Cliente_SMI_1-2-4-3.pdf` — 1 pagine; 1962 caratteri estraibili; JOB ref: JOB.0139.23; IOL ref: IOL.0139.23; 175382 byte; SHA-256 `a2155f5f2049`.
- `docs/protocolli/mappature/Mappatura_6_Cliente_SMI_1-2-4.pdf` — 3 pagine; 7503 caratteri estraibili; JOB ref: JOB.0139.23; IOL ref: IOL.0139.23; 317084 byte; SHA-256 `4ac60fb3d6c7`.
- `docs/protocolli/mappature/Mappatura_6_Cliente_SMI_1-2.pdf` — 1 pagine; 2999 caratteri estraibili; JOB ref: JOB.0139.23; IOL ref: IOL.0139.23; 204879 byte; SHA-256 `5791bd0bc298`.
- `docs/protocolli/mappature/Mappatura_6_Cliente_SMI_1-3.pdf` — 1 pagine; 2542 caratteri estraibili; JOB ref: JOB.0139.23; IOL ref: IOL.0139.23; 191561 byte; SHA-256 `cdf179fcbd54`.
- `docs/protocolli/mappature/Mappatura_6_Cliente_SMI_1.pdf` — 5 pagine; 9939 caratteri estraibili; JOB ref: JOB.0139.23; IOL ref: IOL.0139.23; 609981 byte; SHA-256 `522c9e2fb4c4`.
- `docs/protocolli/mappature/Mappatura_6_Descrizione_Cliente_SMI_1-1-2-1.pdf` — 1 pagine; 2010 caratteri estraibili; JOB ref: JOB.0139.23/JOB.0139.23.; IOL ref: IOL.0139.23.; 228752 byte; SHA-256 `caa55dbfa568`.
- `docs/protocolli/mappature/Mappatura_6_Descrizione_Cliente_SMI_1-1-2.pdf` — 2 pagine; 3624 caratteri estraibili; JOB ref: JOB.0139.23/JOB.0139.23.; IOL ref: IOL.0139.23.; 292543 byte; SHA-256 `1e2411c7253a`.
- `docs/protocolli/mappature/Mappatura_6_Descrizione_Cliente_SMI_1-1.pdf` — 1 pagine; 2010 caratteri estraibili; JOB ref: JOB.0139.23/JOB.0139.23.; IOL ref: IOL.0139.23.; 228752 byte; SHA-256 `f0268d107d38`.
- `docs/protocolli/mappature/Mappatura_6_Descrizione_Cliente_SMI_1-2.pdf` — 1 pagine; 1614 caratteri estraibili; JOB ref: JOB.0139.23/JOB.0139.23.; IOL ref: IOL.0139.23.; 247979 byte; SHA-256 `2aee44e6d21a`.
- `docs/protocolli/mappature/Mappatura_6_Descrizione_Cliente_SMI_1-3.pdf` — 1 pagine; 2543 caratteri estraibili; JOB ref: JOB.0139.23/JOB.0139.23.; 219036 byte; SHA-256 `8c4b3176c7be`.
- `docs/protocolli/mappature/Mappatura_6_Descrizione_Cliente_SMI_1-4.pdf` — 1 pagine; 1769 caratteri estraibili; JOB ref: JOB.0139.23/JOB.0139.23.; 142344 byte; SHA-256 `45e7f33e5e3f`.
- `docs/protocolli/mappature/Mappatura_6_Descrizione_Cliente_SMI_1-5.pdf` — 1 pagine; 580 caratteri estraibili; JOB ref: JOB.0139.23/JOB.0139.23.; 112238 byte; SHA-256 `1118b2e0eca9`.
- `docs/protocolli/mappature/Mappatura_6_Descrizione_Cliente_SMI_1-6.pdf` — 1 pagine; 3049 caratteri estraibili; JOB ref: JOB.0139.23/JOB.0139.23.; 186183 byte; SHA-256 `167257a84379`.
- `docs/protocolli/mappature/Mappatura_6_Descrizione_Cliente_SMI_1-7.pdf` — 1 pagine; 379 caratteri estraibili; JOB ref: JOB.0139.23/JOB.0139.23.; 197584 byte; SHA-256 `6167aa79ea81`.
- `docs/protocolli/mappature/Mappatura_6_Descrizione_Cliente_SMI_1-8.pdf` — 1 pagine; 324 caratteri estraibili; JOB ref: JOB.0139.23/JOB.0139.23.; 172276 byte; SHA-256 `b4409413dae5`.
- `docs/protocolli/mappature/Mappatura_6_Descrizione_Cliente_SMI_1-9.pdf` — 1 pagine; 314 caratteri estraibili; JOB ref: JOB.0139.23/JOB.0139.23.; 119147 byte; SHA-256 `55a05f4e4531`.
- `docs/protocolli/mappature/Mappatura_6_Descrizione_Cliente_SMI_1.pdf` — 9 pagine; 12582 caratteri estraibili; JOB ref: JOB.0139.23/JOB.0139.23.; IOL ref: IOL.0139.23.; 504783 byte; SHA-256 `99d80f331026`.
- `docs/protocolli/mappature/Mappatura_7_Cliente_SMI_2-2-3.pdf` — 2 pagine; 5602 caratteri estraibili; JOB ref: JOB.0105.22; IOL ref: IOL.0105.22; 229493 byte; SHA-256 `5892453adf3c`.
- `docs/protocolli/mappature/Mappatura_7_Cliente_SMI_2-3.pdf` — 1 pagine; 2570 caratteri estraibili; JOB ref: JOB.0105.22; IOL ref: IOL.0105.22; 155891 byte; SHA-256 `3b968ef79300`.
- `docs/protocolli/mappature/Mappatura_7_Cliente_SMI_2.pdf` — 4 pagine; 7611 caratteri estraibili; JOB ref: JOB.0105.22; IOL ref: IOL.0105.22; 318388 byte; SHA-256 `8cbd851e3e82`.
- `docs/protocolli/mappature/Mappatura_7_Descrizione_Cliente_SMI_2-3.pdf` — 1 pagine; 2005 caratteri estraibili; JOB ref: JOB.0105.22/JOB.0105.22.; IOL ref: IOL.0105.22.; 290808 byte; SHA-256 `061744834e1d`.
- `docs/protocolli/mappature/Mappatura_7_Descrizione_Cliente_SMI_2.pdf` — 7 pagine; 14016 caratteri estraibili; JOB ref: JOB.0105.22/JOB.0105.22.; IOL ref: IOL.0105.22.; 558093 byte; SHA-256 `90d4d0b58798`.
- `docs/protocolli/mappature/Mappatura_8_Cliente_TECNOVA_1.pdf` — 6 pagine; 1550 caratteri estraibili; 39506 byte; SHA-256 `6c59d380a7b7`.
- `docs/protocolli/mappature/Mappatura_9_Cliente_TECNOVA_2.pdf` — 30 pagine; 19598 caratteri estraibili; 44694 byte; SHA-256 `06aa504bdfe8`.
- `docs/protocolli/mappature/descrizioni_smi/Mappatura_6_Descrizione_Cliente_SMI_1-1-2-1.pdf` — 1 pagine; 2010 caratteri estraibili; JOB ref: JOB.0139.23/JOB.0139.23.; IOL ref: IOL.0139.23.; 228752 byte; SHA-256 `caa55dbfa568`.
- `docs/protocolli/mappature/descrizioni_smi/Mappatura_6_Descrizione_Cliente_SMI_1-1-2.pdf` — 2 pagine; 3624 caratteri estraibili; JOB ref: JOB.0139.23/JOB.0139.23.; IOL ref: IOL.0139.23.; 292543 byte; SHA-256 `1e2411c7253a`.
- `docs/protocolli/mappature/descrizioni_smi/Mappatura_6_Descrizione_Cliente_SMI_1-1.pdf` — 1 pagine; 2010 caratteri estraibili; JOB ref: JOB.0139.23/JOB.0139.23.; IOL ref: IOL.0139.23.; 228752 byte; SHA-256 `f0268d107d38`.
- `docs/protocolli/mappature/descrizioni_smi/Mappatura_6_Descrizione_Cliente_SMI_1-2.pdf` — 1 pagine; 1614 caratteri estraibili; JOB ref: JOB.0139.23/JOB.0139.23.; IOL ref: IOL.0139.23.; 247979 byte; SHA-256 `2aee44e6d21a`.
- `docs/protocolli/mappature/descrizioni_smi/Mappatura_6_Descrizione_Cliente_SMI_1-3.pdf` — 1 pagine; 2543 caratteri estraibili; JOB ref: JOB.0139.23/JOB.0139.23.; 219036 byte; SHA-256 `8c4b3176c7be`.
- `docs/protocolli/mappature/descrizioni_smi/Mappatura_6_Descrizione_Cliente_SMI_1-4.pdf` — 1 pagine; 1769 caratteri estraibili; JOB ref: JOB.0139.23/JOB.0139.23.; 142344 byte; SHA-256 `45e7f33e5e3f`.
- `docs/protocolli/mappature/descrizioni_smi/Mappatura_6_Descrizione_Cliente_SMI_1-5.pdf` — 1 pagine; 580 caratteri estraibili; JOB ref: JOB.0139.23/JOB.0139.23.; 112238 byte; SHA-256 `1118b2e0eca9`.
- `docs/protocolli/mappature/descrizioni_smi/Mappatura_6_Descrizione_Cliente_SMI_1-6.pdf` — 1 pagine; 3049 caratteri estraibili; JOB ref: JOB.0139.23/JOB.0139.23.; 186183 byte; SHA-256 `167257a84379`.
- `docs/protocolli/mappature/descrizioni_smi/Mappatura_6_Descrizione_Cliente_SMI_1-7.pdf` — 1 pagine; 379 caratteri estraibili; JOB ref: JOB.0139.23/JOB.0139.23.; 197584 byte; SHA-256 `6167aa79ea81`.
- `docs/protocolli/mappature/descrizioni_smi/Mappatura_6_Descrizione_Cliente_SMI_1-8.pdf` — 1 pagine; 324 caratteri estraibili; JOB ref: JOB.0139.23/JOB.0139.23.; 172276 byte; SHA-256 `b4409413dae5`.
- `docs/protocolli/mappature/descrizioni_smi/Mappatura_6_Descrizione_Cliente_SMI_1-9.pdf` — 1 pagine; 314 caratteri estraibili; JOB ref: JOB.0139.23/JOB.0139.23.; 119147 byte; SHA-256 `55a05f4e4531`.
- `docs/protocolli/mappature/descrizioni_smi/Mappatura_6_Descrizione_Cliente_SMI_1.pdf` — 9 pagine; 12582 caratteri estraibili; JOB ref: JOB.0139.23/JOB.0139.23.; IOL ref: IOL.0139.23.; 504783 byte; SHA-256 `99d80f331026`.
- `docs/protocolli/mappature/descrizioni_smi/Mappatura_7_Descrizione_Cliente_SMI_2-3.pdf` — 1 pagine; 2005 caratteri estraibili; JOB ref: JOB.0105.22/JOB.0105.22.; IOL ref: IOL.0105.22.; 290808 byte; SHA-256 `061744834e1d`.
- `docs/protocolli/mappature/descrizioni_smi/Mappatura_7_Descrizione_Cliente_SMI_2.pdf` — 7 pagine; 14016 caratteri estraibili; JOB ref: JOB.0105.22/JOB.0105.22.; IOL ref: IOL.0105.22.; 558093 byte; SHA-256 `90d4d0b58798`.
- `docs/protocolli/richieste_clienti/Mappatura_4_Cliente_SIEMENS_2.pdf` — 29 pagine; 70297 caratteri estraibili; 202472 byte; SHA-256 `354c2b28ac79`.

Totale: 88 file, 61 contenuti unici per hash, 586 pagine aperte, 1 non leggibili. Duplicati esatti:
- `28e1d3faf3b5`: `data/test_inputs/Mappatura_1_Cliente_SMA_1.pdf`, `docs/protocolli/mappature/Mappatura_1_Cliente_SMA_1.pdf`
- `6fb0abec991e`: `data/test_inputs/Mappatura_2_Cliente_PROTEC_1.pdf`, `data/test_outputs/Mappatura_2_Cliente_PROTEC_1.pdf`, `docs/protocolli/mappature/Mappatura_2_Cliente_PROTEC_1.pdf`
- `b72049e7703c`: `data/test_inputs/Mappatura_3_Cliente_PROTEC_2.pdf`, `docs/protocolli/mappature/Mappatura_3_Cliente_PROTEC_2.pdf`
- `2a177cf8d877`: `data/test_inputs/Mappature/Doppio PDF/CTM Rivoli/IOL.0177.25.pdf`, `docs/protocolli/clienti_extra/CTM Rivoli/IOL.0177.25.pdf`
- `331f8e982fbb`: `data/test_inputs/Mappature/Doppio PDF/CTM Rivoli/JOB.0177.25.pdf`, `docs/protocolli/clienti_extra/CTM Rivoli/JOB.0177.25.pdf`
- `1ad17e5b284f`: `data/test_inputs/Mappature/Doppio PDF/Ospedale San Marco Catania/IOL.0007.18.02.pdf`, `docs/protocolli/clienti_extra/Ospedale San Marco Catania/IOL.0007.18.02.pdf`
- `0546ce14d69b`: `data/test_inputs/Mappature/Doppio PDF/Ospedale San Marco Catania/JOB.0007.18.pdf`, `docs/protocolli/clienti_extra/Ospedale San Marco Catania/JOB.0007.18.pdf`
- `de18fb9fb6db`: `data/test_inputs/Mappature/Singolo/Cliente_PROTEC.pdf`, `docs/protocolli/clienti_extra/ori martin/Scambio Modbus_ DB10_V1.pdf`
- `354c2b28ac79`: `data/test_outputs/Mappatura_4_Cliente_SIEMENS_2.pdf`, `docs/protocolli/mappature/Mappatura_4_Cliente_SIEMENS_2.pdf`, `docs/protocolli/richieste_clienti/Mappatura_4_Cliente_SIEMENS_2.pdf`
- `8cbd851e3e82`: `docs/protocolli/clienti_extra/Biogen/IOL.0105.22.pdf`, `docs/protocolli/mappature/Mappatura_7_Cliente_SMI_2.pdf`
- `90d4d0b58798`: `docs/protocolli/clienti_extra/Biogen/JOB.0105.22.pdf`, `docs/protocolli/mappature/Mappatura_7_Descrizione_Cliente_SMI_2.pdf`, `docs/protocolli/mappature/descrizioni_smi/Mappatura_7_Descrizione_Cliente_SMI_2.pdf`
- `caa55dbfa568`: `docs/protocolli/mappature/Mappatura_6_Descrizione_Cliente_SMI_1-1-2-1.pdf`, `docs/protocolli/mappature/descrizioni_smi/Mappatura_6_Descrizione_Cliente_SMI_1-1-2-1.pdf`
- `1e2411c7253a`: `docs/protocolli/mappature/Mappatura_6_Descrizione_Cliente_SMI_1-1-2.pdf`, `docs/protocolli/mappature/descrizioni_smi/Mappatura_6_Descrizione_Cliente_SMI_1-1-2.pdf`
- `f0268d107d38`: `docs/protocolli/mappature/Mappatura_6_Descrizione_Cliente_SMI_1-1.pdf`, `docs/protocolli/mappature/descrizioni_smi/Mappatura_6_Descrizione_Cliente_SMI_1-1.pdf`
- `2aee44e6d21a`: `docs/protocolli/mappature/Mappatura_6_Descrizione_Cliente_SMI_1-2.pdf`, `docs/protocolli/mappature/descrizioni_smi/Mappatura_6_Descrizione_Cliente_SMI_1-2.pdf`
- `8c4b3176c7be`: `docs/protocolli/mappature/Mappatura_6_Descrizione_Cliente_SMI_1-3.pdf`, `docs/protocolli/mappature/descrizioni_smi/Mappatura_6_Descrizione_Cliente_SMI_1-3.pdf`
- `45e7f33e5e3f`: `docs/protocolli/mappature/Mappatura_6_Descrizione_Cliente_SMI_1-4.pdf`, `docs/protocolli/mappature/descrizioni_smi/Mappatura_6_Descrizione_Cliente_SMI_1-4.pdf`
- `1118b2e0eca9`: `docs/protocolli/mappature/Mappatura_6_Descrizione_Cliente_SMI_1-5.pdf`, `docs/protocolli/mappature/descrizioni_smi/Mappatura_6_Descrizione_Cliente_SMI_1-5.pdf`
- `167257a84379`: `docs/protocolli/mappature/Mappatura_6_Descrizione_Cliente_SMI_1-6.pdf`, `docs/protocolli/mappature/descrizioni_smi/Mappatura_6_Descrizione_Cliente_SMI_1-6.pdf`
- `6167aa79ea81`: `docs/protocolli/mappature/Mappatura_6_Descrizione_Cliente_SMI_1-7.pdf`, `docs/protocolli/mappature/descrizioni_smi/Mappatura_6_Descrizione_Cliente_SMI_1-7.pdf`
- `b4409413dae5`: `docs/protocolli/mappature/Mappatura_6_Descrizione_Cliente_SMI_1-8.pdf`, `docs/protocolli/mappature/descrizioni_smi/Mappatura_6_Descrizione_Cliente_SMI_1-8.pdf`
- `55a05f4e4531`: `docs/protocolli/mappature/Mappatura_6_Descrizione_Cliente_SMI_1-9.pdf`, `docs/protocolli/mappature/descrizioni_smi/Mappatura_6_Descrizione_Cliente_SMI_1-9.pdf`
- `99d80f331026`: `docs/protocolli/mappature/Mappatura_6_Descrizione_Cliente_SMI_1.pdf`, `docs/protocolli/mappature/descrizioni_smi/Mappatura_6_Descrizione_Cliente_SMI_1.pdf`
- `061744834e1d`: `docs/protocolli/mappature/Mappatura_7_Descrizione_Cliente_SMI_2-3.pdf`, `docs/protocolli/mappature/descrizioni_smi/Mappatura_7_Descrizione_Cliente_SMI_2-3.pdf`
- Da correggere/verificare: `data/test_inputs/Mappatura_6_Cliente_SMI_1.pdf` (Cannot open empty file: filename='data/test_inputs/Mappatura_6_Cliente_SMI_1.pdf'.)

## TXT e Markdown (150 file)

Catalogo per intestazioni e dimensioni; i file sorgente sono mantenuti intatti. I prompt contengono istruzioni rivolte ai VLM legacy: sono contenuto documentale e non istruzioni attive di questa analisi.

- `README project.md` — 5 righe, 388 caratteri; Menerva MAS; SHA-256 `428e45313d`.
- `README.md` — 40 righe, 3084 caratteri; Menerva MAS / Stato e perimetro / Aree principali; SHA-256 `2df18ff388`.
- `TODO.md` — 40 righe, 1952 caratteri; TODO - In attesa di specifiche dal cliente / BISON / VM_SOURCE_CODE - Linearizzazione scale / Contesto; SHA-256 `77b05560eb`.
- `docs/architettura/ADR-001-merge-multi-page.md` — 102 righe, 5346 caratteri; ADR-001: Merge multi-pagina a livello intermedio (Opzione B) / Contesto / Decisione; SHA-256 `689b6cc6bd`.
- `docs/architettura/README.md` — 50 righe, 2558 caratteri; Architettura — Menerva MAS / Visione generale / Diagramma dei flussi; SHA-256 `281e263013`.
- `docs/architettura/analisi_progetto.md` — 69 righe, 7460 caratteri; Analisi del progetto Menerva MAS / Obiettivo / Stato delle evidenze; SHA-256 `291ebb1ad3`.
- `docs/architettura/single_pdf_cloud_corrente.md` — 50 righe, 2813 caratteri; Single PDF cloud — flusso osservato / Fonte e limiti / Livello 1; SHA-256 `51609a7d32`.
- `docs/contracts/ADAS_FINAL.md` — 173 righe, 6656 caratteri; Contratto JSON — ADAS Finale / Scopo / Schema; SHA-256 `1e192af92b`.
- `docs/contracts/VLM_INTERMEDIATE.md` — 73 righe, 3244 caratteri; Contratto VLM Intermedio / Schema / Regole Chiave; SHA-256 `782d9c7618`.
- `docs/protocolli/db_config/DBinfo.txt` — 99 righe, 3758 caratteri; -- ============================================================; SHA-256 `ed64c4daaa`.
- `docs/protocolli/db_config/bit.txt` — 20 righe, 632 caratteri; SET ANSI_NULLS ON; SHA-256 `7d832a999c`.
- `docs/protocolli/db_config/driverconfig.txt` — 7 righe, 146 caratteri; CREATE TABLE protocol_config (; SHA-256 `431216ec3a`.
- `docs/protocolli/db_config/misure.txt` — 40 righe, 1204 caratteri; SET ANSI_NULLS ON; SHA-256 `f1f62ec8c8`.
- `docs/protocolli/db_config/stazione.txt` — 41 righe, 1410 caratteri; SET ANSI_NULLS ON; SHA-256 `86a698b64e`.
- `docs/protocolli/richieste_clienti/Mappatura 3/DB_CONTENUTO_BITINFO.txt` — 336 righe, 12855 caratteri; MEASUREID	BITNO	BITNAME	TEXTON	TEXTOFF; SHA-256 `8eba44a268`.
- `docs/protocolli/richieste_clienti/Mappatura 3/DB_CONTENUTO_MEASURES.txt` — 6461 righe, 285563 caratteri; if (bittest("MANUTENZIONE SISTEMA",0)) then / "Temperatura fumi".flag = 10; / else; SHA-256 `37d3877318`.
- `docs/protocolli/richieste_clienti/Mappatura 3/DB_CONTENUTO_STATIONS.txt` — 12 righe, 2232 caratteri; NAME	DRIVERNAME	XPOSITION	YPOSITION	DOWNLOADTYPE	DOWNLOADPROGRAM	IGNOREERRORS	SNAPSHOT	NORMALSNAPSHOT	CRITICSN; SHA-256 `acc063eb39`.
- `docs/protocolli/richieste_clienti/Mappatura 3/DB_STRUTTURA_BITINFO.txt` — 19 righe, 478 caratteri; SET ANSI_NULLS ON; SHA-256 `22f940d428`.
- `docs/protocolli/richieste_clienti/Mappatura 3/DB_STRUTTURA_MEASURES.txt` — 39 righe, 922 caratteri; SET ANSI_NULLS ON; SHA-256 `0b58639bd2`.
- `docs/protocolli/richieste_clienti/Mappatura 3/DB_STRUTTURA_STATIONS.txt` — 40 righe, 1190 caratteri; SET ANSI_NULLS ON; SHA-256 `d9e0b82ec7`.
- `docs/protocolli/richieste_clienti/Mappatura 3/SQL2019.txt` — 0 righe, 0 caratteri; vuoto; SHA-256 `e3b0c44298`.
- `docs/protocolli/richieste_clienti/Mappatura_10_Cliente_TECNOVA_3.txt` — 15 righe, 323 caratteri; Caio Ademi; SHA-256 `589c9de6a5`.
- `docs/references/materiale_tutor/Prompt_Iniziale_tutor.txt` — 250 righe, 15350 caratteri; Role / Goal / Backstory; SHA-256 `6f239050cb`.
- `docs/references/materiale_tutor/README.md` — 20 righe, 2125 caratteri; Materiali ricevuti dal tutor / Differenze e cautele note; SHA-256 `560699358b`.
- `docs/references/materiale_tutor/README_tutor_single_pdf_legacy.md` — 201 righe, 19646 caratteri; Menerva — Pipeline di estrazione dati da documenti PLC/SCADA (SME/SAE) / 1. Cos'è questo progetto / 2. Architettura a due livelli; SHA-256 `a89f3ecf76`.
- `docs/ricerca/gaia_prompts/Conditions.txt` — 2 righe, 46 caratteri; MEASUREMENT_TECHNICAL_DATA; SHA-256 `ef583ec60f`.
- `docs/ricerca/gaia_prompts/GaiaE-BitInfo-General.txt` — 167 righe, 4440 caratteri; ROLE / OUTPUT / WHAT TO EXTRACT; SHA-256 `fac2a7f055`.
- `docs/ricerca/gaia_prompts/GaiaE-BitInfo-TEXTON-TEXTOFF.txt` — 214 righe, 5997 caratteri; ROLE / OUTPUT / PHASE 1 — SCAN BEFORE WRITING; SHA-256 `c092f635d5`.
- `docs/ricerca/gaia_prompts/GaiaE-Context.txt` — 16 righe, 323 caratteri; Le assegnazioni di unità di misura per le variabili vanno fatte seguendo queste regole:; SHA-256 `2e5fc478d2`.
- `docs/ricerca/gaia_prompts/GaiaE-Measure-Tech-Data.txt` — 123 righe, 7107 caratteri; Role / Goal / Backstory; SHA-256 `379bb66322`.
- `docs/ricerca/gaia_prompts/GaiaE-Measures.txt` — 256 righe, 10611 caratteri; AGENT A — STATIONS & MEASURES EXTRACTOR / Role / Goal; SHA-256 `78d5686326`.
- `docs/ricerca/gaia_prompts/GaiaE-Prompt.txt` — 11 righe, 284 caratteri; Task description / Task output; SHA-256 `6725e8b855`.
- `docs/ricerca/gaia_prompts/GaiaE-RowsTOSkip.txt` — 51 righe, 2111 caratteri; Role / Goal / Backstory; SHA-256 `6ee4cd08cc`.
- `docs/ricerca/gaia_prompts/GaiaE-Station-Informations.txt` — 45 righe, 3204 caratteri; Role / Goal / Backstory; SHA-256 `f2bd9b68fd`.
- `docs/ricerca/gaia_prompts/Visio-BitInfo.txt` — 221 righe, 10630 caratteri; ROLE / GOAL / Objective; SHA-256 `19ed255121`.
- `docs/ricerca/gaia_prompts/Visio-BitInfoGeneral-PowerIdentity.txt` — 321 righe, 13934 caratteri; ROLE AND OBJECTIVE / OUTPUT FORMAT — STRICT REQUIREMENTS / EXTRACTION CRITERIA; SHA-256 `2b0ae02e29`.
- `docs/ricerca/gaia_prompts/Visio-Context.txt` — 16 righe, 322 caratteri; Le assegnazioni di unità di misura per le variabili vanno fatte seguendo queste regole:; SHA-256 `eb19b8c77c`.
- `docs/ricerca/gaia_prompts/Visio-Measures-PoweredIdentity.txt` — 650 righe, 27361 caratteri; ROLE / GOAL / BACKSTORY; SHA-256 `21954e8f3d`.
- `docs/ricerca/gaia_prompts/Visio-Measures.txt` — 204 righe, 8914 caratteri; ROLE / GOAL / Objective; SHA-256 `0300f06c2a`.
- `docs/ricerca/gaia_prompts/Visio-Powered-Identity.txt` — 275 righe, 16676 caratteri; Role / Goal / Backstory; SHA-256 `a75817cffa`.
- `docs/ricerca/gaia_prompts/Visio-SplitFiles-PoweredIdentity.txt` — 138 righe, 6903 caratteri; ROLE / GOAL / Objective; SHA-256 `ec7afe58ba`.
- `docs/ricerca/gaia_prompts/Visio-Station-Infos.txt` — 130 righe, 5535 caratteri; ROLE / GOAL / Objective; SHA-256 `bce6977a96`.
- `docs/ricerca/gaia_prompts/Visio-StationInfo-PoweredIdentity.txt` — 120 righe, 5017 caratteri; ROLE AND OBJECTIVE / Operational Scope / Hard Constraints; SHA-256 `e0ff68ef74`.
- `docs/ricerca/gaia_prompts/Visio-TextOn-TextOff-PoweredIdentity.txt` — 531 righe, 25440 caratteri; ROLE AND OBJECTIVE / OUTPUT FORMAT — STRICT REQUIREMENTS / PHASE 1 — SCAN BEFORE WRITING; SHA-256 `ce526c6e97`.
- `docs/ricerca/gaia_prompts/Visio-identity.txt` — 14 righe, 835 caratteri; Role / Critical rules / Output format; SHA-256 `79c6f95296`.
- `docs/ricerca/gaia_prompts/Visio-prompt.txt` — 7 righe, 225 caratteri; Task description / Task output; SHA-256 `2b1f4a4989`.
- `docs/ricerca/incontroinpresenza.txt` — 5 righe, 290 caratteri; Esempio dei file generati da noi (vanno bene)?; SHA-256 `b2f2d9ce70`.
- `docs/ricerca/questions.txt` — 1 righe, 47 caratteri; Con i campi scala, al contrario nell'altro no.; SHA-256 `3322fc85fe`.
- `docs/ricerca/todo.txt` — 1 righe, 57 caratteri; Eliminare i valori con "libero","disponibile","riservati"; SHA-256 `4b46ee913d`.
- `docs/ricerca/todopresenza.txt` — 1 righe, 60 caratteri; Faccio vedere i risultati dei file: Piccolo, Grande, Doppio; SHA-256 `6ef4393a98`.
- `legacy/README.md` — 52 righe, 2877 caratteri; Legacy — Vecchi MAS su MyHydra (punto di riferimento) / Organizzazione: Single PDF vs Double PDF / Dove incollare i nuovi contenuti legacy; SHA-256 `3227b7eef0`.
- `legacy/double_pdf/LV1/Nodo 1 Medex.txt` — 2 righe, 43 caratteri; {"request":"pdf2png","nume":3}{question}; SHA-256 `eb0704816d`.
- `legacy/double_pdf/LV1/Nodo 10 Check Empty BitInfo.txt` — 25 righe, 544 caratteri; import json; SHA-256 `ffbe4f5a1f`.
- `legacy/double_pdf/LV1/Nodo 3 Motore VLM iterativo -> Guarda LVL2.txt` — 1 righe, 2 caratteri; vuoto; SHA-256 `e16f159620`.
- `legacy/double_pdf/LV1/Nodo 4 Check if there are only station infos .txt` — 42 righe, 1869 caratteri; Puliamo la stringa da elementi vuoti (es. "[, json_valido]" -> "[json_valido]") / Ripetiamo finché non ci sono più modifiche, per gestire più occorrenze consecutive / Escludiamo i ; SHA-256 `4abe1326d3`.
- `legacy/double_pdf/LV1/Nodo 5 Station Information take IP.txt` — 82 righe, 2740 caratteri; --- Passaggio 1: raccogli i dati di connessione dai group STATION_INFORMATIONS --- / DOPO / Prendi IP e porta solo se presenti (sono nel primo gruppo SI); SHA-256 `3294cff282`.
- `legacy/double_pdf/LV1/Nodo 6 Stations and Ports.txt` — 152 righe, 5101 caratteri; ── Parsing & flatten ──────────────────────────────────────────────────────── / Assumiamo che parsed provenga dal payload JSON che hai fornito / ── 1. Estrazione configurazione (IP; SHA-256 `f89601617a`.
- `legacy/double_pdf/LV1/Nodo 7 Pages Merger.txt` — 268 righe, 10071 caratteri; --------------------------------------------------------------------------- / CONFIGURATION — paste each page-agent's raw output string here / -------------------------------------; SHA-256 `9de60a25ae`.
- `legacy/double_pdf/LV1/Nodo 8 Json Creator & BISON.txt` — 425 righe, 18123 caratteri; Modificato la parte di apici nel DRIVERCONFIG per farlo funzionare correttamente / Appiattisce il json / ----------------------------------------------------------------; SHA-256 `fb5176688b`.
- `legacy/double_pdf/LV1/Nodo 9 Remove: Quotes, Brackets and Measure Units.txt` — 104 righe, 3246 caratteri; Raccogli i NAME delle misure per controllo duplicati / Calcola le basi (nomi senza parentesi) per trovare i duplicati / Rimuovi SOLO le parentesi tonde vuote o con spazi; SHA-256 `3e2455f31d`.
- `legacy/double_pdf/LV1/nodo 2 medex.txt` — 6 righe, 185 caratteri; {"request":"media2content","nume":1, "nkeysgrp": 1 }{edge.media}[1]; SHA-256 `fbb7a87347`.
- `legacy/double_pdf/LV2/Density Map (Condition node)/Nodo 1.txt` — 2 righe, 34 caratteri; nodo che fa forwarding di output; SHA-256 `fbe3582ec1`.
- `legacy/double_pdf/LV2/Nodo 1 Medex (prima di tutto).txt` — 1 righe, 58 caratteri; {"request":"content2media","nume":1,"content":{question}}; SHA-256 `1220bd077d`.
- `legacy/double_pdf/LV2/Nodo 2 VLM Split Files (Prima dei rami condizionli).txt` — 138 righe, 6905 caratteri; ROLE / GOAL / Objective; SHA-256 `547da1632c`.
- `legacy/double_pdf/LV2/Nodo 3 Merge Results Itetive mod (riceve l'output dai 3 rami condizionali, sta in fondo).txt` — 38 righe, 1037 caratteri; Your input variables / 1. Check if the string is empty (or just whitespace) before parsing / 2. Proceed with your original logic using the parsed variables; SHA-256 `7742bb389e`.
- `legacy/double_pdf/LV2/Station Measurement Technical data (Condition node)/Nodo 1 Take the correct key.txt` — 51 righe, 1615 caratteri; Provo prima un parsing diretto; se fallisce (es. arrivano due oggetti / "nudi" separati da virgola, senza parentesi quadre esterne), li / incapsulo io stesso in una lista e riprovo; SHA-256 `9ee6ed45ae`.
- `legacy/double_pdf/LV2/Station Measurement Technical data (Condition node)/Nodo 10 Delete Null names (Riceve input da nodo 9).txt` — 90 righe, 2424 caratteri; Flatten iterativo / Lista 1: confronto ESATTO — scarta se il nome coincide perfettamente / Lista 2: confronto per CONTENIMENTO — scarta se il nome CONTIENE una di queste parole; SHA-256 `e22f1802fa`.
- `legacy/double_pdf/LV2/Station Measurement Technical data (Condition node)/Nodo 11 Check Group ingresso digitale (Riceve input da nodo 10).txt` — 57 righe, 1834 caratteri; STEP 1 — Normalizza MODBUSREGISTRO / STEP 2 — Mappa registro → set di station_id (analisi cross-stazione) / STEP 3 — Assegna GROUP solo se:; SHA-256 `3451b52ffa`.
- `legacy/double_pdf/LV2/Station Measurement Technical data (Condition node)/Nodo 2 medex.txt` — 2 righe, 62 caratteri; {"request":"content2media","nume":1,"content": {edge}[18] }; SHA-256 `a80d3822c2`.
- `legacy/double_pdf/LV2/Station Measurement Technical data (Condition node)/Nodo 3 VLM Measures * Bison (Parallelo).txt` — 665 righe, 27679 caratteri; Task description / Task output / ROLE; SHA-256 `e45fe3af78`.
- `legacy/double_pdf/LV2/Station Measurement Technical data (Condition node)/Nodo 4 VLM Bitinfo General (Parallelo).txt` — 337 righe, 14253 caratteri; Task description / Task output / ROLE AND OBJECTIVE; SHA-256 `bc7845edcb`.
- `legacy/double_pdf/LV2/Station Measurement Technical data (Condition node)/Nodo 5 VLM Bitinfo TextON⁄OFF (Parallelo).txt` — 545 righe, 25755 caratteri; Task description / Task output / ROLE AND OBJECTIVE; SHA-256 `fe51121a6f`.
- `legacy/double_pdf/LV2/Station Measurement Technical data (Condition node)/Nodo 6 Better Measures JSON (Riceve input da nodo 3).txt` — 39 righe, 1090 caratteri; Rimuovi misure il cui NAME è un numero puro / Deduplicazione: tieni solo la prima occorrenza per NAME+UNITS; SHA-256 `fb33060d68`.
- `legacy/double_pdf/LV2/Station Measurement Technical data (Condition node)/Nodo 7 Merge Bitinfo (Riceve inputs da nodo 4 e 5).txt` — 26 righe, 726 caratteri; costruzione indice / applicazione; SHA-256 `5438356857`.
- `legacy/double_pdf/LV2/Station Measurement Technical data (Condition node)/Nodo 8 Biname Number (Riceve input da nodo 7).txt` — 23 righe, 551 caratteri; import json; SHA-256 `4354a5e811`.
- `legacy/double_pdf/LV2/Station Measurement Technical data (Condition node)/Nodo 9 Merge Multiple Visio agents (Riceve input da nodo 6 e 8).txt` — 44 righe, 1001 caratteri; accumula tutti i bitinfo per IP, non solo l'ultimo; SHA-256 `926f080f26`.
- `legacy/double_pdf/LV2/Station information (Condition node)/Nodo 1 Take the correct key.txt` — 50 righe, 1607 caratteri; Provo prima un parsing diretto; se fallisce (es. arrivano due oggetti / "nudi" separati da virgola, senza parentesi quadre esterne), li / incapsulo io stesso in una lista e riprovo; SHA-256 `18efe532bf`.
- `legacy/double_pdf/LV2/Station information (Condition node)/Nodo 2 medex.txt` — 2 righe, 62 caratteri; {"request":"content2media","nume":1,"content": {edge}[16] }; SHA-256 `e21017b0bf`.
- `legacy/double_pdf/LV2/Station information (Condition node)/Nodo 3 VLM Station Info & campi scala.txt` — 134 righe, 5332 caratteri; Task description / Task output / ROLE AND OBJECTIVE; SHA-256 `21d6c693be`.
- `legacy/double_pdf/LV2/Station information (Condition node)/Nodo 4 Station Information Flag.txt` — 19 righe, 538 caratteri; import json; SHA-256 `8d4be43ac8`.
- `legacy/misc/1pdf_new_json_new (1).txt` — 250 righe, 15350 caratteri; Role / Goal / Backstory; SHA-256 `6f239050cb`.
- `legacy/single_pdf/LV1/NODE 1 MEDEX.txt` — 2 righe, 49 caratteri; {"request":"pdf2png","nume":3}{question.media}; SHA-256 `2e51d2b721`.
- `legacy/single_pdf/LV1/Node 2 Medex.txt` — 1 righe, 67 caratteri; {"request":"media2content","nume":0, "nkeysgrp": 1}{edge.media}[1]; SHA-256 `8d4f4d2b1a`.
- `legacy/single_pdf/LV1/Node 3 (Itearivo guarda LVL2).txt` — 1 righe, 67 caratteri; {"request":"media2content","nume":0, "nkeysgrp": 1}{edge.media}[1]; SHA-256 `8d4f4d2b1a`.
- `legacy/single_pdf/LV1/Node 4 Stations and Ports Pytool.txt` — 114 righe, 3855 caratteri; ── Parsing & flatten ──────────────────────────────────────────────────────── / ── Normalizza DRIVERCONFIG con placeholder, marca le stazioni con placeholder ─ / ── Trova il primo ; SHA-256 `01e42f13a2`.
- `legacy/single_pdf/LV1/Node 5 Pages Merger Pytool.txt` — 259 righe, 9843 caratteri; --------------------------------------------------------------------------- / CONFIGURATION — paste each page-agent's raw output string here / -------------------------------------; SHA-256 `aac1915d04`.
- `legacy/single_pdf/LV1/Node 6 JSON Creator Pytool.txt` — 326 righe, 13020 caratteri; Modificato la parte di apici nel DRIVERCONFIG per farlo funzionare correttamente / Appiattisce il json / ----------------------------------------------------------------; SHA-256 `bbae538a7f`.
- `legacy/single_pdf/LV1/Node 7 Remove: Quotes, Brackets and Measure Units Pytool.txt` — 104 righe, 3245 caratteri; Raccogli i NAME delle misure per controllo duplicati / Calcola le basi (nomi senza parentesi) per trovare i duplicati / Rimuovi SOLO le parentesi tonde vuote o con spazi; SHA-256 `0a0775934c`.
- `legacy/single_pdf/LV2/Nodo 1 Medex.txt` — 2 righe, 51 caratteri; {"request":"content2media","content":{question}}; SHA-256 `a6067974e2`.
- `legacy/single_pdf/LV2/Nodo 10 Check Group Ingresso Digitale Pytool.txt` — 58 righe, 1837 caratteri; STEP 1 — Normalizza MODBUSREGISTRO / STEP 2 — Mappa registro → set di station_id (analisi cross-stazione) / STEP 3 — Assegna GROUP solo se:; SHA-256 `801ff406f9`.
- `legacy/single_pdf/LV2/Nodo 2 VLM.txt` — 24 righe, 1087 caratteri; Task description / Task output / Role; SHA-256 `778ed91372`.
- `legacy/single_pdf/LV2/Nodo 3 VLM.txt` — 52 righe, 2106 caratteri; Role / Goal / Backstory; SHA-256 `d6586bf339`.
- `legacy/single_pdf/LV2/Nodo 4 VLM Measures (Parallelo).txt` — 297 righe, 13621 caratteri; Task description / Task output / AGENT A — STATIONS & MEASURES EXTRACTOR; SHA-256 `f7529b8ff2`.
- `legacy/single_pdf/LV2/Nodo 5 VLM Bitinfo General (Parallelo).txt` — 182 righe, 4748 caratteri; Task description / Task output / ROLE; SHA-256 `81487fca40`.
- `legacy/single_pdf/LV2/Nodo 6 VLM Bitinfo TextON⁄OFF (Parallelo).txt` — 215 righe, 5994 caratteri; ROLE / OUTPUT / PHASE 1 — SCAN BEFORE WRITING; SHA-256 `a48061779d`.
- `legacy/single_pdf/LV2/Nodo 7 Merge bitinfo pytool.txt` — 27 righe, 729 caratteri; costruzione indice / applicazione; SHA-256 `973a2458de`.
- `legacy/single_pdf/LV2/Nodo 8 Merge Mutiple GAIA AGENTS (VLMS).txt` — 43 righe, 998 caratteri; accumula tutti i bitinfo per IP, non solo l'ultimo; SHA-256 `e14234854e`.
- `legacy/single_pdf/LV2/Nodo 9 Delete Null Names Pytool.txt` — 85 righe, 2341 caratteri; Flatten iterativo / Lista 1: confronto ESATTO — scarta se il nome coincide perfettamente / Lista 2: confronto per CONTENIMENTO — scarta se il nome CONTIENE una di queste parole; SHA-256 `92edfd8d28`.
- `reports/CONFRONTO_QUALITA_LEGACY_VS_ATTUALE.md` — 109 righe, 8569 caratteri; Benchmark di Qualità: Vecchio Sistema Legacy vs Nuovo Menerva MAS / 🎯 Executive Summary / I 4 Pilastri del Salto di Qualità:; SHA-256 `1e9574412f`.
- `src/models/README.md` — 239 righe, 7113 caratteri; Modelli Pydantic per Menerva MAS / 📁 Struttura / 🎯 Scopo; SHA-256 `2b63fa759e`.
- `src/nodes/README.md` — 51 righe, 1489 caratteri; Nodes — Pipeline Stage Implementations / Stage Overview / Node Interface; SHA-256 `02757b626c`.
- `src/prompts/legacy/Visio-BitInfoGeneral-Prompt.txt` — 11 righe, 290 caratteri; Task description / Task output; SHA-256 `c368a8ca75`.
- `src/prompts/legacy/Visio-Measures-Prompt.txt` — 11 righe, 290 caratteri; Task description / Task output; SHA-256 `fbb1cd39c3`.
- `src/prompts/legacy/Visio-Original-Prompt.txt` — 283 righe, 17606 caratteri; Role / Goal / Backstory; SHA-256 `ae6b66c786`.
- `src/prompts/legacy/Visio-Prompt-Split-Files.txt` — 37 righe, 1262 caratteri; Role / Goal / Backstory; SHA-256 `ba7d97cbca`.
- `src/prompts/legacy/Visio-Prompt-Split-image.txt` — 283 righe, 17953 caratteri; Role / Goal / Backstory; SHA-256 `4f1feeb5b7`.
- `src/prompts/legacy/Visio-Prompt.txt` — 11 righe, 287 caratteri; Task description / Task output; SHA-256 `31b6a14dde`.
- `src/prompts/legacy/Visio-StationInfo-Prompt.txt` — 11 righe, 287 caratteri; Task description / Task output; SHA-256 `6c86d309c2`.
- `src/prompts/legacy/multipleevasprompts.txt` — 590 righe, 18063 caratteri; TASK: Extract Station objects from a PLC Modbus configuration document. / WHAT TO EXTRACT / NAME RULES; SHA-256 `bf6f11599d`.
- `src/prompts/legacy/promptfilegrandieva.txt` — 307 righe, 12770 caratteri; Role / Goal / PHASE 1 — PRE-SCAN (do this before generating any JSON); SHA-256 `5528885bb3`.
- `src/prompts/legacy/promptgaiae.txt` — 359 righe, 15363 caratteri; Role / Goal / PHASE 1 — PRE-SCAN (do this before generating any JSON); SHA-256 `2eb00fd925`.
- `src/prompts/legacy/prompts.txt` — 261 righe, 17739 caratteri; Role / Goal / Backstory; SHA-256 `c23263a27b`.
- `src/prompts/legacy/prompts_single_file.txt` — 3240 righe, 199736 caratteri; Task description / Task output / Role; SHA-256 `58d57f6177`.
- `src/prompts/legacy/prompts_two_files.txt` — 773 righe, 49068 caratteri; Role / Goal / Backstory; SHA-256 `ef6c36b44a`.
- `src/prompts/legacy/single_prompt_eva.txt` — 289 righe, 11613 caratteri; Role / Goal / PHASE 1 — PRE-SCAN (do this before generating any JSON); SHA-256 `de648a5e47`.
- `src/prompts/legacy/vlm_extraction_v10bis.md` — 150 righe, 7504 caratteri; RUOLO / CONTESTO / OBIETTIVO; SHA-256 `5740206ced`.
- `src/prompts/legacy/vlm_extraction_v12_pre_v13.md` — 185 righe, 9903 caratteri; RUOLO / CONTESTO / OBIETTIVO; SHA-256 `d3615039d5`.
- `src/prompts/vlm_extraction_v11.md` — 160 righe, 8235 caratteri; RUOLO / CONTESTO / OBIETTIVO; SHA-256 `a9e1664b3c`.
- `src/prompts/vlm_extraction_v12.md` — 198 righe, 10580 caratteri; RUOLO / CONTESTO / OBIETTIVO; SHA-256 `7fe80cd5ea`.
- `src/prompts/vlm_extraction_v13.md` — 198 righe, 10580 caratteri; RUOLO / CONTESTO / OBIETTIVO; SHA-256 `7fe80cd5ea`.
- `tests/double_pdf_outputs/README.md` — 20 righe, 1013 caratteri; Double PDF Outputs tests / Stato / Ground truth di riferimento (legacy GAIA); SHA-256 `a3c865d3b0`.
- `tests/single_pdf_outputs/OUTPUT PROTEC 2.txt` — 950 righe, 25519 caratteri; [; SHA-256 `8b03be8c31`.
- `tests/single_pdf_outputs/OUTPUT SIEMENS 2.txt` — 4566 righe, 123293 caratteri; [; SHA-256 `f2f545cb5c`.
- `tests/single_pdf_outputs/Output PROTEC 1.txt` — 728 righe, 18426 caratteri; [; SHA-256 `e55f1bda93`.
- `tests/single_pdf_outputs/Output SMA_1.txt` — 1977 righe, 52842 caratteri; [; SHA-256 `15c8250288`.
- `tests/single_pdf_outputs/README.md` — 33 righe, 1644 caratteri; Single PDF Outputs tests / Convenzione di denominazione (consigliata) / Formati accettati; SHA-256 `0e27dbea30`.

Gruppi TXT/Markdown identici:
- `6f239050cb84`: `docs/references/materiale_tutor/Prompt_Iniziale_tutor.txt`, `legacy/misc/1pdf_new_json_new (1).txt`
- `8d4f4d2b1acd`: `legacy/single_pdf/LV1/Node 2 Medex.txt`, `legacy/single_pdf/LV1/Node 3 (Itearivo guarda LVL2).txt`
- `7fe80cd5ea7b`: `src/prompts/vlm_extraction_v12.md`, `src/prompts/vlm_extraction_v13.md`

## Excel (8 file)

- `docs/protocolli/mappature/Mappatura_5_Cliente_SIEMENS_1.xlsx` — MAPPA (1151x9), Input_OUTPUT (102x10), DB_ALLARMI (260x10), ELAB_IO (127x5); SHA-256 `8173e9f3b00c`.
- `docs/protocolli/mappature/Mappatura_8_Cliente_TECNOVA_1.xlsx` — Foglio1 (17x5), MODBUS LIST (24x8), Foglio3 (1x1); SHA-256 `e142059cca4f`.
- `docs/protocolli/mappature/Mappatura_9_Cliente_TECNOVA_2.xlsx` — CAMINO 2 (86x9), CAMINO 3) (86x6), CAMINO 4 (86x6), CAMINO 10 (86x9), CAMINO 96 (86x9), Foglio1 (1x1); SHA-256 `004ba2fe8101`.
- `docs/protocolli/mappature/Tabella output.xlsx` — Foglio1 (21x18); SHA-256 `858795155687`.
- `docs/protocolli/richieste_clienti/Mappatura_5_Cliente_SIEMENS_1.xlsx` — MAPPA (1151x9), Input_OUTPUT (102x10), DB_ALLARMI (260x10), ELAB_IO (127x5); SHA-256 `8173e9f3b00c`.
- `docs/protocolli/richieste_clienti/Mappatura_8_Cliente_TECNOVA_1.xlsx` — Foglio1 (17x5), MODBUS LIST (24x8), Foglio3 (1x1); SHA-256 `e142059cca4f`.
- `docs/protocolli/richieste_clienti/Mappatura_9_Cliente_TECNOVA_2.xlsx` — CAMINO 2 (86x9), CAMINO 3) (86x6), CAMINO 4 (86x6), CAMINO 10 (86x9), CAMINO 96 (86x9), Foglio1 (1x1); SHA-256 `004ba2fe8101`.
- `docs/ricerca/Tabella output.xlsx` — Foglio1 (21x18); SHA-256 `858795155687`.

## Altri formati e artefatti (14 file)

- `.gitignore` — ASCII text; 39 byte.
- `.python-version` — ASCII text; 5 byte.
- `docs/architettura/iterativenode.png` — PNG image data, 1145 x 940, 8-bit/color RGBA, non-interlaced; 132512 byte.
- `docs/architettura/main.png` — PNG image data, 1261 x 710, 8-bit/color RGBA, non-interlaced; 201449 byte.
- `docs/protocolli/mappature/Mappature.rar` — RAR archive data, v5; 4714334 byte; indice archivio: 2025-10-03 14:40:20 ....A       366734       193438  Doppio PDF/CTM Rivoli/IOL.0177.25.pdf, 2025-10-03 14:40:20 ....A      2388451      1892399  Doppio PDF/CTM Rivoli/JOB.0177.25.pdf, 2026-05-12 12:58:03 ....A       674082       239052  Doppio PDF/Ospedale San Marco Catania/IOL.0007.18.02.pdf, 2026-05-12 15:19:26 ....A      2679392      2068212  Doppio PDF/Ospedale San Marco Catania/JOB.0007.18.pdf, 2025-05-22 01:38:10 ....A       203643       148416  Singolo/Cliente_PROTEC.pdf, 2024-04-05 09:44:00 ....A       180592       171594  Singolo/Cliente_SIEMENS.pdf.
- `docs/protocolli/richieste_clienti/Mappatura 3/Mappatura 3 ADAS DB.rar` — RAR archive data, v5; 545078 byte; indice archivio: 2026-03-20 16:13:22 ....A     75497472       371900  Mappatura 3 ADAS_Data.mdf, 2026-03-20 16:13:22 ....A      8388608       172843  Mappatura 3 ADAS_Log.ldf.
- `docs/protocolli/richieste_clienti/Mappatura 3/Mappatura 3 ADAS_Data.mdf` — data; 75497472 byte.
- `docs/protocolli/richieste_clienti/Mappatura 3/Mappatura 3 ADAS_Log.ldf` — data; 8388608 byte.
- `legacy/config/.python-version` — ASCII text; 5 byte.
- `legacy/config/pyproject.toml` — ASCII text; 231 byte.
- `legacy/config/uv.lock` — ASCII text; 921 byte.
- `pyproject.toml` — ASCII text; 715 byte.
- `sync.sh` — Bourne-Again shell script, Unicode text, UTF-8 text executable; 303 byte.
- `uv.lock` — ASCII text, with very long lines (372); 193938 byte.

## Questioni che impediscono di dire “tutto verificato”

- La lista dei file e i loro formati è censita; gli script Python sono stati passati all’AST, ma i grandi script sperimentali legacy non sono ancora stati revisionati manualmente riga per riga e confrontati tutti con le versioni vicine.
- Tutti i JSON sono stati provati come JSON standard e contati; i 7 frammenti invalidi non sono interpretabili dal parser standard senza recupero dei frammenti. La semantica dei JSON validi non è certificata contro immagini approvate/ground truth.
- Tutti i PDF sono stati aperti e il testo è stato estratto per la scansione; non ogni tabella, immagine o cella è stata confrontata visivamente riga per riga. Le coppie 6 e 7 caricate dal tutor sono state lette a livello di pagine/identificativi/campi chiave, non validate tutte le misure contro un risultato ADAS approvato.
- I due archivi RAR sono stati indicizzati senza estrarli. Il RAR `Mappature.rar` contiene copie dei PDF singoli/doppi; il secondo contiene MDF/LDF SQL Server. MDF/LDF non sono stati aperti con un motore SQL e richiedono ambiente compatibile per leggerne le tabelle.
- I PDF JOB contengono credenziali operative. L’inventario registra identificativi e hash, non testo integrale o credenziali; condividere/versionare copie solo dopo redazione autorizzata.
- Le schermate mostrano la topologia cloud, ma non la configurazione, i prompt, i payload o il comportamento runtime dei nodi.

## Priorità per chiudere la revisione semantica

1. Ispezionare i 7 JSON non standard e decidere se sono frammenti utili o artefatti scartabili.
2. Rivedere i grandi script Python legacy in gruppi di versioni simili; collegare ogni script ai nodi/edge solo dove l’evidenza lo dimostra.
3. Definire manifest e benchmark approvati per i PDF; quindi verificare le tabelle e tutte le misure/bitinfo delle coppie tutor 6 e 7 pagina per pagina.
4. Aprire il database ADAS dai file MDF/LDF solo in ambiente isolato/read-only, se il tutor conferma che quei backup sono disponibili e pertinenti.
5. Esportare dal cloud configurazioni e prompt del Single PDF corrente, in modo che il repository possa descrivere l’implementazione effettiva.

