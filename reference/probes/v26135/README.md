# AERMOD v26135 official behavior probes

This directory contains small, reviewable manifests for behavior questions that cannot be resolved
safely from a keyword inventory alone. The official EPA v26135 executable remains the behavioral
authority. The retained official fixture artifact supplies base decks and meteorology; manifests only
record deterministic mutations.

## Evidence rules

1. Every case runs in an isolated workspace.
2. A control case must reproduce successful execution before targeted outcomes are interpreted.
3. Targeted cases use `expected_outcome: observe`; acceptance or rejection is recorded, not assumed.
4. The executable, source archive, materialized input deck, stdout, stderr, output files, diagnostics,
   and SHA-256 values are retained in the workflow artifact.
5. Official source snippets are captured only for the exact handler ranges relevant to the batch.
6. A workflow artifact is not final repository evidence until reviewed and summarized in a committed
   result file and worklog.
7. These tools are an evidence harness, not the future AERMODKit application runner.

## Batch 1

`batch1/manifest.json` covers:

- the retained Test3 RLINEXT/RBARRIER control;
- SWPOINT with and without `MODELOPT ALPHA`;
- one- and two-barrier `VBARRIER` forms;
- repeated same-sector `OZONEFIL`;
- repeated same-sector `NOX_FILE`.
