# Pytool — Double PDF, nodo `JSON CREATOR` (nodo 12)

## File

[`scripts/in_use/json_creator_edge13.py`](scripts/in_use/json_creator_edge13.py) — v4.4, placeholder `{edge}[13]`.

È la stessa trasformazione finale che usa il Single PDF, con **due sole righe
diverse** dal sorgente:

| Riga | Single PDF | Double PDF |
|---|---|---|
| 2 (commento) | `edge 4 = JSON intermedio aggregato dal nodo iterativo` | `edge 13 = chunk JSON del nodo PREPARAZIONE X JSON (11)` |
| 45 | `raw = r'''{edge}[4]'''` | `raw = r'''{edge}[13]'''` |

Tutto il resto è identico a `src/nodes/json_creator.py` v4.4. Verificare con:

```sh
diff ../../../../src/nodes/json_creator.py scripts/in_use/json_creator_edge13.py
```

Le uniche differenze devono essere le righe 2 e 45. Hash atteso del file
Double: `e75c101395dcfaf9086edc393c4ea32ee8c0008333e88699b7869d471c629c91`.

**Se il `diff` mostra altro, la copia è divergente: non usarla.** È esattamente
come è successo il 5/10, quando la copia sul canvas aveva i campi limite a
`null` invece del sentinel `∓3.40282e38`.

## Perché due copie e non una

Il Double e il Single condividono il trasformatore finale, ma non l'indice
dell'edge: nel Single il chunk arriva dal motore iterativo sul filo #4, nel
Double dal nodo `PREPARAZIONE X JSON` sul filo #13. Un unico file con dentro
`{edge}[4]` costringerebbe a editare lo script a ogni switch di flusso, ed è
esattamente il modo in cui la divergenza è entrata.

Le copie stanno nelle rispettive cartelle, con l'indice dell'edge già corretto:
non vanno mescolate. Il Single PDF resta in
[`../../../single_pdf/pytools/json_creator_v4_4.py`](../../../single_pdf/pytools/json_creator_v4_4.py)
con `{edge}[4]` e hash `7d60929795a34fb3c8d70884335bb80bcc95004586e10c55b118694d525c0c6b`.

## Indice dell'edge

`{edge}[13]` è il filo 11→12. Se il canvas viene ricablato, l'indice va
ricontrollato: il numero è locale al canvas, non una proprietà dello script.
Se l'indice è sbagliato il nodo non produce output e non lascia warning, perché
non c'è nessun errore da cui difendersi.

## Limiti noti (ereditati dal Single, non risolti qui)

- `scale_elec_start`, `scale_elec_end`, `scale_eng_start`, `scale_eng_end`,
  `limit_hour`, `limit_day` sono raccolti dal chunk e **non vengono mai usati**.
  Sul caso 7 il JOB dichiara 18 unità e 5 limiti: ne applica 4.
- I campi limite delle misure analogiche escono al sentinel `±3.40282e38`, che
  è ciò che vanno in ADAS per "nessun limite". Se un output Double ha `null`
  in questi campi, lo script sul canvas non è questo.
- Nessun `try/except` globale: un'eccezione non gestita significa nessun output.
- `NAME` non viene troncato, mentre la colonna ADAS è `nvarchar(50)`.