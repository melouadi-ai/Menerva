# PROTEC 2 — attesi per la run v2 (redesign UNIFIED+ORACOLO)

Documento: `Mappatura_3_Cliente_PROTEC_2.pdf` — **2 pagine**, 79 righe. Verità PDF:
`verifica_pdf/per_caso/caso_3_protec_2/tabella_pdf.json`.

## Numeri attesi

| Voce | Atteso |
|---|---|
| Pagine | 2 |
| Righe del PDF | 79 |
| Misure (righe senza bit) | **15** |
| Bitinfo (righe con bit) | **24** (20 a pagina 1, 4 a pagina 2) |
| Righe saltate da regola | 40 (32 `Disponibile` V2, 8 `Non Utilizzato` V2/V20) |
| Registri distinti | 19 (40001–40004 + 40005…40033 dispari) |
| Variabili attese nel consolidato | 39 |

## Shard

Con 2 pagine tutto cade in `SLICE A` (1-10): `SLICE B` e `SLICE C` devono restituire `[]`
e i due merger devono concatenare senza errore. È il test del percorso seriale automatico.

## Misure attese (15)

| Pagina | Registro | Descrizione |
|---|---|---|
| 2 | 40005 | Misura CO |
| 2 | 40007 | Misura NO |
| 2 | 40009 | Misura NO2 |
| 2 | 40011 | Misura SO2 |
| 2 | 40013 | Misura NH3 |
| 2 | 40015 | Misura H2O |
| 2 | 40017 | Misura CO2 |
| 2 | 40019 | Miura O2 |
| 2 | 40021 | Misura CH4 |
| 2 | 40023 | Misura TOC |
| 2 | 40025 | Misura Polveri |
| 2 | 40027 | Misura Temperatura |
| 2 | 40029 | Misura Pressione Differenziale |
| 2 | 40031 | Misura Pressione Assoluta |
| 2 | 40033 | Live PLC |

## Bit attesi (24)

| Pagina | Registro | Bit | Descrizione PDF | TEXTON nel PDF |
|---|---|---|---|---|
| 1 | 40001 | 0 | Check Cycle Polverimetro | Check Cycle Attivo |
| 1 | 40001 | 8 | Selettore Misura / Manutenzione | Manutenzione |
| 1 | 40001 | 9 | Allarme Temperatura Cabina | OK |
| 1 | 40001 | 10 | Condizionatore 1 OFF | OK |
| 1 | 40001 | 11 | Condizionatore 2 OFF | OK |
| 1 | 40001 | 12 | Allarme Essiccatore | OK |
| 1 | 40001 | 14 | Allarme 24 VDC | OK |
| 1 | 40001 | 15 | Allarme Polverimetro | OK |
| 1 | 40002 | 8 | Lampada OR Allarmi |  |
| 1 | 40002 | 9 | Lampada Allarme Alta Temperatura Cabina |  |
| 1 | 40003 | 8 | MCA10 Errore | Errore |
| 1 | 40003 | 9 | Maintenance MCA10 | Manutenzione |
| 1 | 40003 | 10 | Maintenance Request MCA10 | Richiesta Manutenzione |
| 1 | 40003 | 13 | Error FID | Errore |
| 1 | 40003 | 14 | Maintenance FID | Manutenzione |
| 1 | 40003 | 15 | Maintenance Request FID | Richiesta Manutenzione |
| 1 | 40004 | 0 | OVF Polveri | Errore |
| 1 | 40004 | 1 | OVF Temperatura | Errore |
| 1 | 40004 | 2 | OVF Pressione Differenziale | Errore |
| 1 | 40004 | 3 | OVF Pressione Assoluta | Errore |
| 2 | 40004 | 8 | RC Polveri | Errore |
| 2 | 40004 | 9 | RC Temperatura | Errore |
| 2 | 40004 | 10 | RC Pressione Diferenziale | Errore |
| 2 | 40004 | 11 | RC Pressione Assoluta | Errore |

## Trappole note di questo documento

1. **IP fabbricato**: il PDF dichiara 3 IP (`10.127.126.99`, `.114`, `.113`) e ne usa 1.
   Pagina 1 non ha IP nella tabella: il creator emette il default `127.0.0.1` su `SME`.
   Atteso il warning `oracolo_ip` con i due IP non usati.
2. **Refuso nel PDF**: `RC Pressione Diferenziale` (pagina 2) → il VLM tende a
   correggerlo in `DIFFERENZIALE`. Atteso `oracolo_refuso`, nessuna correzione automatica.
3. **`Disponibile` / `Non Utilizzato`**: 40 righe da saltare. Se compaiono in output,
   V2/V20 non sono state applicate.
4. **Nessuna stazione nel PDF**: `name` è nullo; il naming (`SME`, `SME 1`) resta quello
   del creator, non è un errore di estrazione.
