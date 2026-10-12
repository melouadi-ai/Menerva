# Pytool — Double PDF, nodo `JSON CREATOR` (nodo 12)

## File: quale incollare

[`scripts/in_use/json_creator_edge13_canvas.py`](scripts/in_use/json_creator_edge13.py)
— è **questo** il file da incollare nel nodo (non quello documentato sotto).
Stessa logica del documentato (stesso AST, verificato da test), senza righe
di commento: 26.731 byte.

Il 6/10/2026 il file documentato (34.365 byte) ha mandato in rosso il nodo 12,
mentre la versione precedente (32.766 byte) passava. Evidenza: il paste oltre
una certa dimensione fallisce a parità di logica. Soglia di sicurezza nei
test: 32.000 byte (`test_json_creator_edge13_canvas.py`).

## File documentato (riferimento, NON da incollare)

[`scripts/in_use/json_creator_edge13.py`](scripts/in_use/json_creator_edge13.py)
— v4.4 + fix Double, placeholder `{edge}[13]`. Versione leggibile e commentata,
riferimento per ogni modifica futura.

È la stessa trasformazione finale che usa il Single PDF, con **divergenze
intenzionali e documentate** dal sorgente (decisione 6/10/2026, solo Double):

| Area | `src/nodes/json_creator.py` | Questa copia |
|---|---|---|
| Riga 2 (commento) | `edge 4 = JSON intermedio aggregato dal nodo iterativo` | `edge 13 = chunk JSON del nodo PREPARAZIONE X JSON (11)` |
| Riga raw | `raw = r'''{edge}[4]'''` | `raw = r'''{edge}[13]'''` |
| Tabella `KW` | 11 voci (VALVOLA, ALLARME, ZERO, SPAN...) | 31 voci: stesse + MARCIA, AVVIAMENTO, SPEGNIMENTO, MISURA, BLOCCO, OK/ERRORE, WARM-UP, STAND-BY, LIFE SIGNAL... |
| `TEXTON` packed | `state_on` se presente, altrimenti keyword | **sempre keyword** (l'IOL non ha colonna di stato) |
| `TEXTOFF` packed | `state_off` se presente, altrimenti keyword | invariato (resta dal chunk: `OFF`) |
| Singoli | `state_on` se presente, altrimenti keyword | invariato |
| `LOWRANGE`/`HIGHRANGE` analogiche | sempre sentinel | fondo scala dichiarato, sentinel se assente (v4.5, anche in `src/`) |
| Limiti/divisori | ignorati | solo in review con i nomi (v4.5, anche in `src/`) |
| Registro Modbus | dal PDF così com'è | **40000 + REG** (12/10/2026, sistema): gli IOL Double scrivono il REG corto (1→40001). Solo Double: il Single non somma perché i suoi PDF scrivono già 40001 |

Tutto il resto è identico a `src/nodes/json_creator.py` v4.5. Verificare con:

```sh
diff ../../../../src/nodes/json_creator.py scripts/in_use/json_creator_edge13.py
```

Il `diff` deve mostrare **solo** queste aree. Hash attesi:

- documentato (`json_creator_edge13.py`, NON da incollare): `f0c64b4413095fac23b76f849966ba2f3f6b7dfdd973029f20bd36ce683f2bec`
- copia canvas (`json_creator_edge13_canvas.py`, da incollare): `8f086a1ff0f11cfe7c3302fe54b2ad99a4145ef5fc530cd5a9ca89adbfdab01b`
  (28.427 byte, sotto la soglia 32 KB; offset 40000 del 12/10/2026)

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