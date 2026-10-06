# PDF di riferimento — caso 7

Le due fonti della verità per questo caso. **Il confronto output↔PDF si fa su
questi file, non sul ground truth legacy**: il legacy sbaglia, e il confronto
va fatto sulla coppia IOL+JOB perché metà della verità sta nel JOB.

| File | Ruolo | Pagine | SHA-256 (primi 16) |
|---|---|---|---|
| `Mappatura_7_Cliente_SMI_2.pdf` | IOL: la mappa di scambio dati | 4 | `8cbd851e3e8266cb` |
| `Mappatura_7_Descrizione_Cliente_SMI_2.pdf` | JOB: la specifica di progetto | 7 | `90d4d0b587981c72` |

Copia byte-identica di `~/Downloads/Menerva/menervaPdf (Caricato)/6_7 DOCPLU/`.
Se gli hash non coincidono, la cartella locale ha la precedenza per la
verifica: il resto del repo non deve dipendere da un percorso fuori dal progetto.

## Dove si legge cosa

L'IOL ha colonne `DESCRIZIONE | REG | BIT | TIPO | STRUCT BIT | RANGE`, e la
`REG` è una cella unita. Per la verità dei registri servono le coordinate delle
celle (`get_text("words")`), non il testo grezzo.

Verità per registro, dal foglio IOL:

| Registro | Contenuto | Bit |
|---|---|---|
| 1 | Allarmi | 8–15, 0–7 (16 righe: è il bit wrap) |
| 2 | Allarme Box + linea riscaldata COT | 8 |
| 3 | Stati: Sistema in misura … Pompa analisi | 8, 10–15, 7 |
| 4 | Stati: Stato elettrovalvola cal zero … Fuori servizio per guasto | 8, 10–13, 0–7 |
| 17–42 | Misure, con i buchi 21, 24, 26, 29–32, 40 bianchi | — (`TIPO=INT`) |
| 145–158 | Comandi, con i buchi 146, 151, 154–156, 159–160 bianchi | — (`TIPO=WORD`) |
| 161–172 | Dati stimati, con i buchi 165, 166, 168, 170, 173–176 bianchi | — (`TIPO=WORD`) |

Totale **47 bitinfo**: 37 impaccati più 9 comandi più 1 riga per ciascuno degli
8 stimati. Le righe senza TITOLO non generano bit.

**Il punto delicato è REG 4.** La cella unita parte da `DBX 70.0` a pagina 2 e
arriva a `DBX 71.7` a pagina 3: **attraversa il confine di pagina**. A pagina 3
la colonna `REG` è visivamente vuota, il VLM restituisce `modbus_register: null`
e il pytool scarta la riga. I bit 3–7 (`Impianto in spegnimento`,
`Impianto in lavaggio`, `SME in manutenzione`, `Impianto in manutenzione`,
`Impianto fuori servizio per guasto`) sono quindi i cinque che mancano.

## Cosa dice il JOB e non dice l'IOL

| Capitolo | Contenuto | Stato |
|---|---|---|
| Tabella 8 (4.2) | `PC SME` due schede 192.168.70.103 e 172.16.1.10; `PLC` **172.16.1.31:511** | ✅ l'output ha la combinazione giusta e una sola stazione |
| Intestazione | `Oggetto: Sistema Analisi Emissioni` | ✅ il nome stazione è **dichiarato**, non dedotto |
| Tabella 9 (4.5.1) | 19 righe di campi scala con unità e limiti | ❌ 4 unità su 18, 0 limiti: il join scala↔misura è per uguaglianza esatta di stringa |
| 4.5.2 | Le 9 misure asteriscate sono già in unità ingegneristiche, "dividere 10" | ❌ non raccolto, anche dall'IOL che lo scrive in `RANGE` |
| Tabella 12 (4.7) | Validazioni: colonne `STATI IMPIANTO` = Fermo, Manutenzione, Fuori servizio, Lavaggio | ❌ sono **esattamente i 5 bit persi** |

Il JOB identifica i segnali con i **tag** (`CO`, `O2S`, `TF`, `P_MTR`), l'IOL li
descrive a parole (`CO`, `O2 Secco`, `Temperatura fumi`, `Potenza motore`).
Il join del consolidatore richiede `description == tag`: le 4 unità applicate
sono esattamente i 4 tag che coincidono, le altre 14 muoiono nel join.

## Attenzione alle copie in `docs/protocolli/`

`docs/protocolli/mappature/` e `docs/protocolli/clienti_extra/Biogen/` contengono
questi stessi documenti più **spezzoni per pagina** (suffissi `-3`, ecc.). Sono
derivati, non sorgenti. Per la verifica usare i due file qui sopra.