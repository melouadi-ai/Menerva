# Single PDF Outputs tests

Cartella di raccolta per gli **output MyHydra** (risultato del pytool `json_creator.py` v4.2)
relativi a test su **singolo PDF**. Incolla qui i file; il confronto con i ground truth
(`data/test_outputs/`) viene eseguito direttamente leggendo questa cartella.

## Convenzione di denominazione (consigliata)
```
<CASO>_<descrizione>.json      es.: PROTEC_1_run01.json
                               es.: SMA_1_vlm13_pytool42.json
                               es.: SIEMENS_2_page5-8.json
```
Casi noti: `SMA_1`, `PROTEC_1`, `PROTEC_2`, `SIEMENS_2`, `SMI_1`, `SMI_2`.
Se il nome non contiene il caso, aggiungi una riga `_CASE: <CASO>` in testa al file
o segnalalo nel messaggio.

## Formati accettati
- JSON lista di stazioni (output finale pytool) — preferito
- JSONL / JSON concatenati / repr Python / testo con recinti ``` : il parser del
  pytool li gestisce comunque, e anche il mio lettore è difensivo
- .txt va bene altrettanto

## Cosa faccio io quando trovi un file qui
1. Leggo l'output e lo normalizzo (appiattimento misure/bitinfo, drop `ID`,
   `STATIONID`, `_meta`, `_warnings`).
2. Confronto contro il GT ufficiale (`Json_2_Cliente_PROTEC_1.json`,
   `Json_4_Cliente_SIEMENS_2.json`) o contro gli output legacy GAIA.
3. Segnalo: misure mancanti/in più, DRIVERPRIVATE diversi (registro/formato 150/250),
   bitinfo con buchi (con mappa per registro), TEXTON/TEXTOFF, UNITÀ, DRIVERDATA.
4. Se serve dirimere un dubbio, verifico il PDF sorgente in `data/test_inputs/`.
