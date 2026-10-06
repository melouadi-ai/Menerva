# PDF da confrontare — Single PDF

Le fonti della verità per i quattro casi Single PDF. **Il confronto
output↔PDF si fa su questi file, non sul ground truth legacy.**

| Caso | File | Pagine | SHA-256 |
|---|---|---|---|
| `caso_1_sma_1` | `Mappatura_1_Cliente_SMA_1.pdf` | 1 | `28e1d3faf3b5842c3a1ef87b38083db4d33d35ca5ed9d6be18031b5e07e52906` |
| `caso_2_protec_1` | `Mappatura_2_Cliente_PROTEC_1.pdf` | 2 | `6fb0abec991ee0fdd8ec363102f6c11f4ee3799658c64b9f581ebdff6b6ab570` |
| `caso_3_protec_2` | `Mappatura_3_Cliente_PROTEC_2.pdf` | 2 | `b72049e7703cb65469d436e98f62c56a417635bbc90dde85e8704f2172b748a2` |
| `caso_4_siemens_2` | `Mappatura_4_Cliente_SIEMENS_2.pdf` | 29 | `354c2b28ac7999fafc320a6d7cdb2cb06121743d809cb583e4696ea8b845e3cc` |

Copia byte-identica di `docs/protocolli/mappature/`. Se gli hash divergono, la
cartella locale ha la precedenza per la verifica: il resto del repo non deve
dipendere da un percorso esterno.

Gli output corrispondenti sono in `../Outputs MYHYDRA/`, e il confronto
automatico gira in `../verifica_pdf/confronta.py`.

## Attenzione alle copie in `docs/protocolli/mappature/`

La stessa cartella contiene questi documenti più **spezzoni per pagina** e
ricalcoli di versioni diverse, con suffissi tipo `-1-15_splitted`,
`-7-29`, `-15-29_second_split`, `-13-14`, `-12`. Sono derivati, non sorgenti.
Per la verifica usare i quattro file qui sopra. Lo stesso vale per
`docs/protocolli/clienti_extra/`, che contiene altri clienti (Biogen, CTM
Rivoli, essity, luxottica, superwatt): utili come campione per la
generalizzazione, non per il confronto di questi quattro casi.

## Le tre cose che il confronto dei PDF ha già rivelato (5/10/2026)

1. **`UNITS: "Unità"`** sulla misura `Polveri (GR)` (registro 40008, caso SMA_1).
   Nel PDF la cella Unit di quella riga contiene `mg/Nm³`; la parola `Unità` è
   un'intestazione di sottocolonna, non un valore. Causa: la regola **V3** del
   prompt v13 elenca `"Unità"` fra gli esempi di unità valide, quindi insegna
   l'errore al modello. Il GT legacy ha lo stesso difetto, perciò l'abbiamo
   ereditato e non introdotto. Correzione: togliere `"Unità"` dagli esempi e
   dire esplicitamente che le intestazioni di colonna non sono unità.

2. **Refuso del documento corretto contro la regola V13.** In SMA_1 il PDF
   scrive `Allarme 1 Ossiegno umido` (refuso del cliente) e l'output emette
   `Allarme 1 Ossigeno umido`. V13 vieta la correzione dei refusi, e il GT
   legacy li ha trascritti fedelmente. La stessa regola, su PROTEC_1, è stata
   rispettata (`Rchiesta Mnautenzione` fedelmente, vedi D3 di `PENDENZE.md`).
   Quindi non è un bug di prompt: è affidabilità del VLM, e serve un test
   dedicato con fixture che contengano refusi noti.

3. **I due "difetto" di SMA_1 nel verdetto sono falsi positivi.**
   `verifica_pdf/confronta.py` confronta per registro ignorando la stazione, e
   il registro 40001 compare in due tabelle diverse del PDF: `CO` nella tabella
   `192.168.6.20` e `Temperatura Fumi` nella tabella `xxx.xxx.xxx.xxx`.
   L'output le separa correttamente in due stazioni; è lo strumento che non
   distingue. Correzione: abbinare su `(stazione, registro, bit)`.

## Da confrontare con cautela

**SIEMENS_2 non è validato.** 1116 righe nel documento, 236 presenti
nell'output, 129 righe non coperte. La perdita è a monte dell'estrazione
(`_meta.variables_total` = 274, `chunks_parsed` = 1 su 29 pagine), non del
pytool, che non ha mai visto le righe mancanti. Vedi
[`../verifica_pdf/README.md`](../verifica_pdf/README.md) e B3/C1 di
[`../PENDENZE.md`](../PENDENZE.md). Su questo caso non trarre conclusioni di
qualità.

**Copertura Bitinfo**: il report dichiara `100%` sui casi SMA_1 e PROTEC, ma su
SIEMENS_2 il nostro output ha 147 `bitinfo` contro 209 del legacy. Tutti i 29
bit in più sono confermati dal PDF; i 60 in più del legacy stanno tutti su
registri che noi non copriamo. La cifra `100%` non è sostenibile senza
qualificazione.