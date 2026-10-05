# data/ — provenienza mista, leggere prima di usare

Questa cartella contiene PDF reali, JSON ADAS storici e fixture intermedie
**senza qualifica uniforme di ruolo**: nessun file qui dentro è automaticamente
un ground truth. Regole prima di usare un file come riferimento:

1. Verificare il ruolo: input VLM? output ADAS storico? frammento Medex/config?
   (i file `*medex*.json` in `test_outputs/` sono stringhe di configurazione,
   non output).
2. Verificare lo SHA contro `docs/architettura/inventario_repository.md`:
   esistono omonimi pericolosi (es. `Mappatura_6_Cliente_SMI_1.pdf` da 0 byte
   qui contro l'IOL vero da 5 pagine in `docs/protocolli/mappature/`) e duplicati
   byte-identici in `docs/protocolli/`.
3. I JOB e diversi PDF contengono **credenziali operative e dati di produzione**:
   mai includerli in prompt, log o fixture non sanitizzate.
4. Contesto decisionale: `docs/architettura/analisi_progetto.md` (casi 6/7,
   caso negativo Ospedale, prescrizione del manifest con hash).

Convenzione fixture altrove: `observed_*` = output runtime sanitizzato,
`expected_*` = derivato. Un `observed_*` con `review_required: true` non è
un ground truth.
