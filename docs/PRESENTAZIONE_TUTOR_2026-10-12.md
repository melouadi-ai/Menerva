# Menerva MAS — Presentazione al tutor (12/10/2026)

Conversione automatica di mappature PLC/SCADA (PDF) in configurazioni ADAS
per il monitoraggio emissioni (SME/SAE). Due flussi: Single PDF (mappatura
singola) e Double PDF (coppia IOL+JOB).

## 1. Problema

I documenti di mappatura (tabelle registri Modbus, liste I/O Siemens, stati
impianto) vanno tradotti a mano in JSON ADAS: misure analogiche/digitali,
bit di dettaglio (`bitinfo`), stati ON/OFF, scale, limiti. Il sistema legacy
(un solo VLM con un unico prompt) produceva output mai misurati contro i PDF:
registri sbagliati, righe inventate, allarmi persi — scoperti solo a runtime
su ADAS.

## 2. Approccio

- **VLM solo per lettura e trascrizione** (3 rami specializzati: misure,
  nomi-bit, stati), mai per conti, join o dedup.
- **Tutta l'assemblatura in codice deterministico** (pytool inline): join per
  chiave `riga`, carry-over registro esplicito, dedup per chiave, merge stazioni.
- **Ogni disaccordo diventa warning**, mai scelta silenziosa.
- **Verifica contro il PDF, non contro il legacy**: tabelle verità estratte
  dal layer testo del PDF (`verifica_pdf/per_caso/`), confronto meccanico
  `confronta.py` sul JSON finale. Un verdetto = una sola run (tap di run
  diverse non si incrociano: il VLM varia).

## 2bis. Perché non un VLM singolo (scelte contro il legacy)

- Il VLM non fa più i conti: join, carry-over e dedup avvenivano "in testa"
  al modello (bug storici: REG-contatore, wrap BIT 15→0, bitinfo fantasma sui
  registri adiacenti). Ora è codice deterministico su chiavi.
- Compiti stretti con self-check: 3 rami da un lavoro ciascuno. Un prompt solo
  degrada a fine blocco (TEXTON omessi, pagine a zero, 129 righe perse in
  silenzio su SIEMENS).
- Nessuna scelta silenziosa: V2/V20/V21 come codice con motivo; ogni
  disaccordo un warning. Il singolo VLM riempiva i buchi (default, conteggi).
- Difesa in profondità: ogni bug trovato è diventato guardia + test, non una
  preghiera nel prompt.
- Costo: 3-4 chiamate per pagina invece di 1, run lunghe (SIEMENS oltre un'ora).

## 3. Risultati Single PDF (finale vs PDF)

| Documento | Righe PDF | Copertura chiavi | Buchi | Inventate |
|---|---|---|---|---|
| SMA_1 (1 pag.) | 50 | 44 ok + 1 refuso | 0 | 0 |
| PROTEC_1 (2 pag.) | 89 | 45/45 | 0 | 0 |
| PROTEC_2 (2 pag.) | 79 | 39/39 | 0 | 0 |
| SIEMENS_2 (29 pag., 1116 righe) | 1116 | ~98% (228/230) | 5 motivati (3 varianza p9 + 2 regola) | 0 accertate |
| ORI_MARTIN_5 (3 pag.) | 119 | 58/58 | 0 | 0 |
| SUPERWATT_8 (4 pag.) | 181 | 131/131 | 0 | 0 |
| LUXOTTICA_7 (22 pag., 707 righe) | 707 | ~69% sostanziale | pagine HW 12+15 (regola) + singoli | 0 |
| LEGNANO_6 (29 pag., 1106 righe) | 1106 | ~65% chiavi | pagine HW 12-17 (regola) + sparsi | 0 accertate |

Spare e righe da scartare correttamente assenti (es. 222 V2 su SIEMENS, 44 su
PROTEC_1). TEXTON: letti dove il PDF li dichiara (maggioranza su PROTEC, quota
variabile per run), derivati da keyword con avviso dove mancano;
SMA/SIEMENS non hanno colonna stati (convenzione, come il legacy).

## 4. Risultati Double PDF (casi 6 e 7, Qwen 3.8)

- Caso 6: 22 misure + 60 bitinfo = **100% del PDF**. Il GT legacy ha 2
  registri errati, 18 bitinfo fantasma, TEXTON shiftati di una riga, QAL3
  `INT` scritti 250 invece di 150.
- Caso 7: 40 misure + 47 bitinfo, verificati contro PDF.

## 5. Difetti trovati e fix (tutti con test di regressione)

- **D1**: dedup packed ignorava il bit → chiave + bit.
- **F1b**: join posizionale applicava registri dei nomi sulle righe sbagliate
  → i nomi vincono solo a descrizioni concordi, altrimenti tengono le misure.
- **F13**: buste rows vuote assegnate ai nomi → ignorate.
- **F14**: righe placeholder duplicate sulla stazione reale → vince placeholder.
- **F15**: i 3 rami numeravano `riga` in modo diverso → indice fisico di riga
  ovunque + warning `stati_orfani`.
- **F17**: stati senza chiave di controllo → `description` check-key (V28),
  voto di maggioranza a registri uguali contro le correzioni di refusi.
- **F18/F19**: due regressioni introdotte dai fix e prese dai test/field
  (grouper che perdeva gli stati; maggioranza che scavalcava con bit diversi).
- **F16**: cluster pagina 9 SIEMENS sciolto come varianza (isolata: 32/32).
- **F20 (F1c)**: a descrizioni concordi ma registri diversi i nomi non si
  applicano più (riempiono solo registri nulli): niente righe fantasma
  adiacenti. I 4 finali congelati risultano invariati.
- **F21**: bit fuori 0-15 (N.Bit 1-based non rimappato) → rimappato se libero,
  altrimenti segnalato: l'output resta importabile.
- **F22**: pagine 12-17 perse su Luxottica/Legnano = zone HW con regola V21
  in tutti i rami (obbedienza, non guasto; provato via SLICE-A). Warning
  `pagina_vuota_sospetta` per pagine davvero mute.

## 6. Tuning VLM (evidenze, non sensazioni)

Standard: temperatura 0,01, Top P 0,4, storico OFF, thinker OFF.
Thinker ON: 6 buchi + V2 violate (vietato). Sotto 0,01: ritorni nulli.
Top P 0,2: TEXTON peggiori. I setting aiutano TEXTON/stabilità, non copertura.

## 7. Limiti onesti e lavoro futuro

- Mai importato un output in ADAS reale (checklist pronta).
- Limiti/BISON non applicati (manca specifica cliente).
- 6 decisioni cliente: HW dentro/fuori (la più grossa: ~200 righe),
  BISON, regola V2-composti, zeri iniziali, nome stazione, IP di default.
- Refusi corretti dal VLM contro le istruzioni (segnalati, mai auto-applicati).
- Nuovi documenti in coda: Essity (terza coppia Double), CTM Rivoli, Ospedale
  (caso-regola abbinamento), già inventariati con hash.
- Suite: 148 test root + 52 double, verdi; tutto committato e pushato.
