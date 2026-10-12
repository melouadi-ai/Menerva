# PDF di riferimento — caso 8 (Rivoli)

Le due fonti della verità per questo caso. **Il confronto output↔PDF si fa su
questi file**: per questo caso non esiste alcun ground truth legacy.

| File | Ruolo | Pagine | SHA-256 (primi 16) |
|---|---|---|---|
| `IOL.0177.25.pdf` | IOL: la mappa di scambio dati (DB100) | 4 | `2a177cf8d877ef27` |
| `JOB.0177.25.pdf` | JOB: la specifica di progetto | 23 | `331f8e982fbbb1cf` |

Copia byte-identica di `data/test_inputs/Mappature/Doppio PDF/CTM Rivoli/`.

## Dove si legge cosa

L'IOL ha colonne `DESCRIZIONE | REG | BIT | TIPO | STRUCT BIT | RANGE`, e la
`REG` è una cella unita. Per i registri servono le coordinate delle celle,
non il testo grezzo.

Verità per registro, dal foglio IOL:

| Registro | Contenuto | Bit |
|---|---|---|
| 1 | Allarmi | 8, 9, 10, 11, 12, 0, 1, 2, 3 (bianche 13–15, 4–7) |
| 2 | 16 righe tutte bianche | — (niente packed, niente bit) |
| 3 | Stati: Sistema in misura … Pompa analisi | 8, 9, 10, 11, 12, 13, 7 |
| 4 | Stati: EV cal zero … Impianto in manutenzione | 8–13, 0, 1, 2, 3, 5, 6 (bianche 14, 15, 4, 7) |
| 15–32 | Misure INT, con titolo solo 18 NOx, 25 TF, 31 QG, 32 PWR | — |
| 33–47 | Misure REAL dispari, con titolo solo 33 CO, 37 O2 Secco | — |
| 193–197 | Impostazioni INT (CO rif, NO2 rif, O2S, O2U, QFNs) | — |
| 209–222 | Comandi WORD (209, 211–214, 216, 217, 221, 222) | 1 bit ciascuno |
| 226–240 | Stimate WORD (226 NOx, 233 TF, 239 QG, 240 PWR) | — |

Totale **27 misure, 37 bitinfo**. Le righe senza TITOLO non generano nulla.

## Cosa dice il JOB e non dice l'IOL

| Capitolo | Contenuto | Stato |
|---|---|---|
| Tabella 7 (5.1) | Mask 192.168.1.xxx; PC SME .10, PLC **.1:511**, MIR9000e .2 | ✅ una sola stazione col PLC |
| Intestazione | `Oggetto: Sistema Analisi Emissioni` | ✅ nome dichiarato |
| Tabella 8 (5.4.1) | 6 scale: CO 0–240 (lim 120/150), NOx 0–20 (lim 8/10), O2S 0–25, TF 0–600, QG 0–600, PWR 0–2000 | ✅ 5/6 (NOx fuori: TAG `NO` vs `NOx`?) |
| 4.5.2 | CO e O2 già in ingegneristiche, resto 0…10000; nessun "dividere" | ✅ nessun warning DIVISIONE |
| Tabella 10 (5.6) | Matrice validazioni | ✅ input completi (nessun bit perso) |
| 5.3 | QAL2/QAL3 non richieste, ma l'IOL le porta | ✅ tenute coi nomi del PDF |
| Pag. 23 | Cliente finale "San Dalmazzo" | ⚠️ copia-incolla loro, irrilevante per l'output |
