# Checklist prova di importazione in ADAS reale

Mai fatta su nessun output (Single e Double). Prima di parlare di consegna,
importare un output per documento e registrare ogni errore di importazione
come bug con evidenza (messaggio ADAS + misura coinvolta).

## File da importare (output finali verificati contro il PDF)

| # | Documento | File finale | Atteso |
|---|---|---|---|
| 1 | SMA_1 | `myhydra/single_pdf/TESTS/SMA 1/TAP NAIVE FINALE.txt` | E1 38 misure + 30 bitinfo, E1 1 7 misure |
| 2 | PROTEC_1 | `myhydra/single_pdf/TESTS/PROTEC 1/NAIVE FINALE.txt` | SME 3 + 30, SME 1 7 + 10 |
| 3 | SIEMENS_2 | `myhydra/single_pdf/TESTS/SIEMENS/OUTPUT FINALE NAIVE.txt` | SME 104 + 145 |
| 4 | Double caso 6 | `tests/double_pdf_outputs/observed_adas_case6_qwen38_run5.json` | 22 misure + 60 bitinfo, registri 40001–40441 |

## Cosa registrare per ogni import

- Esito (ok / errore) + messaggio ADAS testuale completo.
- Se errore: misura/bitinfo coinvolta (NAME, registro, bit) e regola che lo spiega.
- IP/placeholder: verificare che `127.0.0.1` e `xxx.xxx.xxx.xxx` non vadano in produzione.

## Note note

- Limiti/BISON escono in default: attesi warning, non errori (mapping col cliente).
- TEXTON da keyword dove il PDF non dichiara stati: convenzione, non dato letto.
