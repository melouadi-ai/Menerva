# Panoramica Single PDF — 8 ott 2026 (run 3.6/3.8, seriale + shard)

Riferimento: SIEMENS 29 pagine (`../PDFs per il confronto/Mappatura_4_Cliente_SMI..._SIEMENS_2.pdf`,
tabella verità `per_caso/caso_4_siemens_2/tabella_pdf.json`, 1116 righe).

## Metodo (vincolante da qui in poi)

- Un verdetto = tap di **una sola run** (merger + consolidatore + finale insieme,
  senza rilanci in mezzo). I tap riletti rieseguono a monte con varianza VLM:
  incrociare run diverse produce fantasmi (Q1 sciolto così).
- Copertura = **FINALE vs PDF** (artefatti stabili). Tap = solo meccanismo.
- 3.6 = idraulica e robustezza. 3.8 = qualità vincolante. Mai giudicare bit/stati
  da una 3.6 né la tenuta da una run sola.

## Verdetti

| Documento | Run | Contabilità | Verdetto |
|---|---|---|---|
| SMA_1 3.6 seriale | 51 vars → 45 misure + 6 scarti motivati + 30 bitinfo | VERDE | |
| PROTEC 1 3.8 seriale | 45/45 nel PDF su 89 righe (44 `Disponibile` = V2), 0 inventate | VERDE con riserva D1 | |
| SMA_1 3.8 seriale | 46 vars → 45 misure + 30 bitinfo, limiti/placeholder visibili | VERDE con riserve F1, F2 | |
| SMA_1 3.8 post-fix (seriale, F1b+D1+v15, `TESTS/SMA 1/`) | E1 45 misure + 30 bitinfo, E1 1 7 misure | VERDE con riserve: 44 ok + 1 refuso su chiavi, 0 buchi; REGRESSIONE F2: 3 misure placeholder duplicate su E1 (O2, Stato impianto, Temperatura Fumi); 37 `riga_disallineata` (F1b tiene misure, corretto); stati assenti (keyword) |
| SMA_1 3.8 post-fix2 (F14, `TESTS/SMA 1/` agg.) | E1 38 misure + 30 bitinfo, E1 1 7 misure | VERDE: 44 ok + 1 refuso, 0 buchi, 0 fantasma; leak F14 assente sul campo (O2/Stato/TempFumi solo su E1 1) |
| PROTEC 2 3.8 seriale | 39 vars → 20+4 bitinfo e 16+4, tutto coperto | VERDE | |
| PROTEC 2 3.8 post-fix (F15, `TESTS/PROTEC 2/`) | 4 + 16 misure, 20 + 4 bitinfo | VERDE con riserva: 39/39 chiavi (27 ok + 12 stato), 0 buchi, 0 fantasma, 40 scarti regola; 12 TEXTON da fallback (ramo stati emette poco su p2: recall VLM, non join); 13 `riga_disallineata` tenute-misure |
| PROTEC 2 shard (pilota) | identico al seriale (varianza VLM a parte) | VERDE meccanismo | |
| SIEMENS shard-A 3.6 | 9/10 pagine (manca p9 in quel tap), cover assorbita | PARZIALE (F6) | |
| SIEMENS shard-B 3.6+v15 | 10/10 giri, 35 vars, 0 scarti | VERDE meccanismo (F11, F12, F13) | |
| SIEMENS completa 3.8 pre-fix (shard, codice senza fix) | 91 misure + 144 bitinfo, 1 stazione (`JSON SIEMENS NUOVO.txt`) | VERDE con riserve: copertura nomi 215/224 (96%), 0 inventate, 9 buchi veri, ~15 shift (F1), 5 spare da verificare |
| SIEMENS completa 3.8 post-fix2 (F15, `TESTS/SIEMENS/`) | 104 misure + 145 bitinfo, 1 stazione, 29/29 pagine | VERDE: 232/237 chiavi nominate (97,9%), 5 buchi veri (3 p9 + 2 Riservato), 1 inventata F12 (40030/0), 0 spare emesse, 182 V2 assenti; TEXTON da keyword (il PDF non ha colonna stati, come il legacy); 33 `riga_disallineata` tenute-misure |
| PROTEC 1 3.8 post-fix (F14/F15, `TESTS/PROTEC 1/`) | 3 + 7 misure, 30 + 10 bitinfo | VERDE: 45/45 chiavi, 0 buchi, 0 inventate, 44 spare ok; numerazione fisica concorde fra rami (1-48/47/46); TEXTON 16→7 diversi; 14 `riga_disallineata` tenute-misure | |

## Ritrovamenti

- **D1 (bloccante, test parcheggiato).** Creator: dedup packed per `(desc, reg)`
  senza bit (`src/nodes/json_creator.py:566`) — PROTEC 1 perde i bit 10/11 di
  40007 pur presenti nel PDF. Fix: chiave + bit. Tocca src + tripla v15 +
  coppia edge13 + hash. IMPLEMENTATO (fd623fe).
- **F1 (bloccante).** Rami in disaccordo d'ordine/conta → join per `riga`
  applica registri/bit dei nomi sulle righe sbagliate a cascata. Casi puliti:
  SIEMENS p4 (measures salta 40007+40010, shifta tutto), Server 02 inghiottita
  (nome misure + reg nomi). Fix (F1b): applicare reg/bit dai nomi **solo se le
  descrizioni coincidono** (o desc nomi nulla); altrimenti tenere misure +
  warning forte. Tocca src + 3 copie consolidatore + test. IMPLEMENTATO (2f5db24).
- **F2.** Placeholder con variabili promosso a stazione ADAS (`E1 1` + IP finto
  nel DRIVERCONFIG). Merge o scarto: da disegnare.
- **F3.** 3.8 non emette le CALCOLATA (NOX/H2O/...). ADAS netto invariato,
  composizione diversa. Solo nota.
- **F4 = difetto noto n.1.** `limit_day` ora estratto (CO=50) e creator lo
  segnala come non applicato. Resta da implementare (mapping BISON, cliente).
- **F5.** Bit tutti null sui digitali SMA_1 → BITNO 0; singolo-vs-impaccato
  aperto. Da sciogliere col PDF.
- **F6.** Pagina 9 SIEMENS assente in un tap merger. Flakiness di run (altra run
  ce l'ha parziale). Metodo: fidarsi del contatore `pagine`, non del conteggio
  a occhio.
- **F7.** Cover con 14 nomi fantasma (= tabella p2). Disallineamento o
  allucinazione. Assorbito (0 misure → 0 output), ma da sciogliere.
- **F8.** Righe senza descrizione → scarti V2 (51 su shard-A). Col PDF: spare
  o nomi mancati? Solo la tabella lo dice.
- **F9 (dettaglio).** `_meta` off-by-one (135 vs 136). Bassa priorità.
- **F10 (prima sospetto, poi ridimensionato).** Giri motore persi in silenzio:
  shard-B dà 10/10 (`pagine: 10`), quindi il motore emette scheletri per i giri
  vuoti. Resta il caso giro-caduto-senza-scheletro (mai osservato finora).
  Azione: verificare se il motore espone un contatore giri.
- **F11.** Errore nomi applicato per precedenza (40117 vs 40119). Coperto da F1b.
- **F12.** `Riserva STATI LOGICI` → misura 40030. V2 match-esatto lascia passare
  i composti ("Riserva X"). Domanda di regola (cliente? o contains?).
- **F13 (fragilità).** Busta rows vuota → assegnata a bitnames per l'`else`
  (solo l'ordine fisso dei rami evita danni). Fix: ignorare le buste vuote.
  Piccolo, sicuro. IMPLEMENTATO (bc0ec7d). ATTENZIONE: il CONSOLIDATORE sul canvas è fermo a d5dfbfd: re-incollare prima delle prossime run.
- **Q1 sciolto.** Warning-vs-finale incoerenti = tap di run diverse.
- **F14 (nuovo, fixato).** Leak cross-stazione: il ramo measures emette le righe placeholder anche sotto la stazione reale (SMA_1: 7 copie); il consolidatore le teneva entrambe, il finale duplicava O2/Stato/TempFumi su E1. Fix: vince placeholder (`copia_reale_da_placeholder`), verificato 44 ok + 1 refuso, 0 buchi, 0 fantasma sul tap reale.
- **F15 (nuovo, fixato).** Contratto `riga` contraddittorio fra prompt (measures: sole emesse; stati v15: sopravvissute incluse omesse) + stati vincitori senza guardia. Fix: `riga` fisica in tutti e 3 i prompt + `stati_orfani` + copy-as-is rafforzato (refusi). Test `tests/test_single_prompt_contracts.py`.

## Note di disegno confermate sul campo

- Forward-fill IP nel creator (`last_ip`): spiega tutte le run (default
  127.0.0.1 senza seme, ereditato con seme). Fragile con teste stantie (F2).
- Stati sparsi v15: il VLM obbedisce (`rows: []`, niente padding). Da
  estendere ai bitstates di LV2-A/C (solo B ce l'ha).
- Warning `riga_mismatch` sugli stati scatterà di routine con v15
  (sottoinsieme): atteso, non difetto.
- VLM nondeterministico tra run: mai confrontare tap di run diverse.

## Prossimi passi proposti (ordine)

1. D1, F1b, F13 (P0, tutto testato in repo + repaste).
2. Indagine contatore giri motore (F6/F10).
3. v15 su LV2-A/C + run shard-A/C complete.
4. SIEMENS completa 3 shard + `confronta.py` vs tabella 1116 righe (verdetto).
5. Poi: F12/F2/B2 con cliente, F4 BISON, F5/F8 da PDF, F9.
