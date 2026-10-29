# LV2 prompts — current

I 3 rami dello split, **stato al 28 ottobre 2026**: misure v18, nomi-bit v16,
stati v19. Da mettere in Powered identity (istruzioni) con `{edge.media}[N]`
nel campo Prompt e Context vuoto. Dettagli dei rami in
[`../README.md`](../README.md).

**Da incollare al rewiring**: il canvas attivo esegue ancora il prompt v13 a
ramo unico (vedi `history/`). I tre rami correnti non sono mai stati eseguiti
sul canvas.

```sh
sha256sum vlm_measures_v18.md vlm_bitnames_v16.md vlm_bitstates_v19.md
```

Hash attesi (byte-identici a `src/prompts/`, che resta la fonte autorevole):

- `vlm_measures_v18.md`: `dd55d4855131c0f53f2ca3e939f6a6b1acd152beb0bd3a6a4d7feed77e946763`
- `vlm_bitnames_v16.md`: `5baec7eb7074d985707f0e5a4fe1a70f28c3b27e5e2e7b906a6ef717a9705b2e`
- `vlm_bitstates_v19.md`: `2325a235ac6f6170431d9000d7bdcfe52e618758fa2487230477bf34be242652`

Lo specchio gemello di questa cartella è
[`../../../prompt/`](../../../prompt/), con lo stesso inventario e gli stessi
hash. Le due cartelle vanno ricopiate insieme: una sola delle due aggiornata è
la causa del disallineamento trovato il 28/10 (v14 citati come correnti per tre
settimane).

## Cosa NON è più corrente

`vlm_bitstates_v14.md` e `vlm_bitstates_v15.md` restano in questa cartella
perché `tests/test_single_prompts_v14.py` li confronta byte per byte con
`src/prompts/`, ma sono **storico**: non vanno incollati nei nodi. La tabella
delle versioni correnti è in [`../../../prompt/README.md`](../../../prompt/README.md).
