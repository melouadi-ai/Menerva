# PDF di riferimento — caso 6

Le due fonti della verità per questo caso. **Il confronto output↔PDF si fa su
questi file, non sul ground truth legacy**: il legacy sbaglia (vedi
[`../test_adas_caso6_pdf_truth.py`](../test_adas_caso6_pdf_truth.py)).

| File | Ruolo | Pagine | SHA-256 (primi 16) |
|---|---|---|---|
| `Mappatura_6_Cliente_SMI_1.pdf` | IOL: la mappa di scambio dati, 22 misure e 47 righe di bit | 5 | `f389830a3a56a339` |
| `Mappatura_6_Descrizione_Cliente_SMI_1.pdf` | JOB: la specifica di progetto | 9 | `99d80f331026e8b5` |

Copia byte-identica di `~/Downloads/Menerva/menervaPdf (Caricato)/6_7 DOCPLU/`.
Se gli hash non coincidono, la cartella locale ha la precedenza per la
verifica: il resto del repo non deve dipendere da un percorso fuori dal progetto.

## Dove si legge cosa

L'IOL ha colonne `DESCRIZIONE | REG | BIT | TIPO` e la `REG` è una cella unita:
il valore compare una volta e vale per tutte le righe sotto, fino al prossimo
numero. Leggere solo il testo grezzo (`get_text()`) fa perdere questa
struttura: per la verità dei registri servono le coordinate delle celle.

Verità per registro, dal foglio IOL:

| Registro | Contenuto | Bit |
|---|---|---|
| 1 | Allarmi | 8–13 |
| 2 | (riempitivo, senza titolo) | 8–15, 0–7 |
| 3 | Stati: Sistema in misura … Pompa analisi | 8–11, 15, 0–3, 5–7 |
| 4 | Stati: Stato elettrovalvola cal zero … Impianto fuori servizio | 8–11, 13, 0–3, 5–7 |
| 5 | Stati 2 (DCS) | 8–15, 1, 2, 4, 5 |
| 6 | Stati 2 (DCS) | 8–13, 0–3 |
| 9, 10, 11 | QAL3 tempo trascorso apertura elettrovalvola N2/ARIA/SO2 | — (`TIPO=INT`) |
| 17, 33 | SO2 Raw, Temperatura fumi Raw | — (`TIPO=REAL`) |
| 49, 65 | SO2, Temperatura fumi | — (`TIPO=REAL`) |
| 417–419, 425–427, 431, 432 | Comandi | — (`TIPO=WORD`) |
| 433, 441 | Misura stimata SO2, Misura stimata Temperatura fumi | — (`TIPO=WORD`) |

Totale **60 bitinfo**: 52 impaccati più 8 comandi. Le righe senza TITOLO non
generano bit. Il GT legacy ne ha 78, perché riempie le righe bianche e
duplica `PM-2601A/B` e i quattro ventilatori.

Il JOB di questo caso **non contiene la colonna unità**: `mg/Nm3` e `°C` nel GT
legacy sono inferenze, non dati del documento. Qui l'output emette `mg/Nm3` su
SO2 e SO2 Raw perché la scala SO2 è dichiarata, e `null` altrove.

## Attenzione alle copie in `docs/protocolli/mappature/`

`docs/protocolli/mappature/` contiene questi stessi documenti più **spezzoni per
pagina** (suffissi `-1`, `-1-2`, `-2-4`, `-15-29_second_split`, ecc.). Sono
derivati, non sorgenti. Per la verifica usare i due file qui sopra.