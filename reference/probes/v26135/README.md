# AERMOD v26135 official behavior probes

This directory contains small, reviewable manifests for behavior questions that cannot be resolved safely from a keyword inventory alone. The official EPA v26135 executable remains the behavioral authority. The retained official fixture artifact supplies base decks and meteorology; manifests record deterministic mutations and exact evidence boundaries.

## Evidence rules

1. Every case runs in an isolated workspace.
2. Positive controls must reproduce successful execution before paired negative outcomes are interpreted.
3. Targeted cases use `expected_outcome: observe`; acceptance or rejection is recorded, not assumed.
4. The executable, source archive, materialized input deck, stdout, stderr, output files, diagnostics, and SHA-256 values are retained in the workflow artifact.
5. Official source ranges and exact diagnostic-call contexts are retained where executable cases need source-supported generalization.
6. A workflow artifact is not final repository evidence until reviewed and summarized in a committed result file and worklog.
7. These tools are an evidence harness, not the future AERMODKit application runner.

## Batch 1

`batch1/manifest.json` covers:

- the retained Test3 RLINEXT/RBARRIER control;
- SWPOINT with and without `MODELOPT ALPHA`;
- one- and two-barrier `VBARRIER` forms;
- distinct-sector and same-sector `OZONEFIL` pairs;
- distinct-sector and same-sector `NOX_FILE` pairs.

Reviewed evidence is in `batch1/result.json`. The final official run completed 9 cases: 6 accepted, 3 rejected, and 0 indeterminate. Detailed interpretation is in `docs/reference/V26135_OFFICIAL_BEHAVIOR_PROBES_BATCH1.md`.

## Batch 2

Batch 2 is composed from `batch2/manifest.json` and `batch2/additional-cases.json`. It covers:

- complete and incomplete global/sector MONTH vectors for `O3VALUES` and `NOX_VALS`;
- first- and second-barrier inclusive VBARRIER endpoints;
- all below/above directions for HT, WT, LAI and LM/LAD;
- unequal and equal same-side VBARRIER distance behavior;
- generated EVENT input followed by event-output `FILEFORM` EXP/FIX controls;
- exact official source contexts for E261, E603, E371-E374, W375, W620 and W595.

Reviewed evidence is in `batch2/result.json`. The final official run completed one accepted preparation and 27 cases: 15 accepted, 12 rejected, and 0 indeterminate. Detailed interpretation is in `docs/reference/V26135_OFFICIAL_BEHAVIOR_PROBES_BATCH2.md`.

## Batch 3

Batch 3 covers:

- seven ALPHA/DFAULT dependency groups;
- ARCFTOPT repeat, payload-count, and aircraft dependency behavior;
- deterministic aircraft hourly-emissions support;
- `MAXDCONT` secondary-rank and THRESH forms with dynamic/explicit units.

Reviewed evidence is in `batch3/result.json` and `batch3/case-evidence.csv`. The final official run completed 35 cases: 16 accepted, 19 rejected, and 0 indeterminate. Detailed interpretation is in `docs/reference/V26135_OFFICIAL_BEHAVIOR_PROBES_BATCH3.md`.

## Batch 4

Batch 4 is composed from the base manifest and PLATFORM, BACKGRND, GRID, DISCCART, and DISCPOLR case fragments. It covers:

- PLATFORM exact/trailing payload fields and source conflicts;
- global/sector BACKGRND repetition and HOURLY/static interaction;
- implicit, NetID-only, fully explicit, and wrong-ID GRIDCART/GRIDPOLR continuations;
- inactive ELEV/FLAGPOLE fields for DISCCART and DISCPOLR;
- exact source-state and diagnostic contexts for E208, E231, E631-E633, E168/E501, E170, W228, and W229.

Reviewed evidence is in `batch4/result.json` and `batch4/case-evidence.csv`. The final reviewed official run completed 40 cases: 29 accepted, 11 rejected, and 0 indeterminate. Detailed interpretation is in `docs/reference/V26135_OFFICIAL_BEHAVIOR_PROBES_BATCH4.md`.
