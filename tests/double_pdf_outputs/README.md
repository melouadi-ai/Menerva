# Double PDF Outputs tests

Cartella di raccolta per gli **output MyHydra** relativi al caso d'uso **DOUBLE PDF**
(coppia di file: `IOL.xxxx.xx.pdf` mappatura I/O + `JOB.xxxx.xx.pdf` descrizioni/lavori).

Stessa convenzione della cartella gemella [`../single_pdf_outputs/`](../single_pdf_outputs/):
- un file di output per run, `.json` o `.txt`;
- nome contenente il caso (`CTM_RIVOLI`, `SAN_MARCO_CATANIA`, `BIOGEN`, `ESSITY`, ...)
  oppure riga `_CASE: <CASO>` in testa al file.

## Stato
⏳ Pipeline Double PDF non ancora avviata. Prerequisiti:
1. LV1/LV2 del vecchio MAS Double PDF incollati in `legacy/double_pdf/LV1|LV2/`
   (vedi [legacy/README.md](../../legacy/README.md));
2. Nodi mancanti implementati: `pdf_splitter`, `page_classifier`, `merge_pages`.

## Prima uscita ADAS Double PDF (caso 6, 5/10/2026)

- `observed_adas_case6_qwen38.json`: chunk del `CONSOLIDA PRE-JSON CREATOR`
  (run Qwen 3.8) passato in `src/nodes/json_creator.py` v4.3 in locale —
  1 stazione `Sistema Analisi SO2` (`10.100.50.95:511`), 22 misure
  (5 packed + 9 analogiche + 8 singoli), 60 bitinfo, validazione Pydantic
  `success: True` senza errori né warning. `MEASUREID` nei bitinfo = ID
  sequenziale della misura (disegno v4.x, non registro: vedi confronto PROTEC_1).

## Ground truth di riferimento (legacy GAIA)
- `data/test_outputs/gaia_ctm_rivoli.json`
- `data/test_outputs/gaia_doublefile_result_6.json`, `gaia_doublefile_result_7.json`
- `data/test_outputs/output_multiple_files.json`, `outputvisiopiufiles.json`
