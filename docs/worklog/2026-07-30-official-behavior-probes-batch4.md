# Worklog: official v26135 behavior probes Batch 4

- Date: 2026-07-30
- Development branch: `agent/official-behavior-probes-batch4`
- Pull request: #13
- Phase: official behavior evidence before production loss-aware syntax

## Objective

Resolve the four remaining SO/RE questions:

- PLATFORM trailing fields and source conflicts;
- BACKGRND duplicate and HOURLY/static behavior;
- active GRIDCART/GRIDPOLR continuation IDs;
- inactive DISCCART/DISCPOLR conditional fields.

## Probe design

The reviewed manifest contains 40 cases:

- 7 PLATFORM cases;
- 11 BACKGRND cases;
- 8 GRIDCART/GRIDPOLR continuation cases;
- 8 DISCCART conditional-field cases;
- 6 DISCPOLR conditional-field cases.

Each group includes positive controls. The evidence bundle retains materialized decks, output hashes, stdout/stderr, diagnostics, official executable/source hashes, and source-pattern contexts.

## Exploratory corrections

The first 30-case run identified one control-design issue: the PLATFORM control used `STACKDW`, which already had PRIME building data, and correctly produced `E633`.

The expanded run identified two additional fixture issues:

- PLATFORM cards were inserted after the first `SRCGROUP`, producing ordering diagnostic `E140`;
- the DISCPOLR ELEV control named a source not present in `flatelev.inp`, producing `E300`.

The final run moved PLATFORM before source-group processing and used `ELEV_STK`, the active source in the ELEV fixture. No behavior conclusion was promoted from a failed positive control.

## Reviewed evidence

- workflow: `30479954822`;
- reviewed head: `215764df489d623c3433e6baa0a6b301b0ab3f68`;
- artifact: `8735323902`;
- digest: `sha256:cc3cb39b85bac2429e11deda087853e3a5a89852f0574a27968f1393012378f1`;
- cases: 40;
- accepted/rejected/indeterminate: 29/11/0;
- expectations met: 40/40;
- nine-job CI at the reviewed head: `30479955343`.

## Findings

### PLATFORM

The exact form and one/two trailing numeric fields completed. Extra numeric fields are converted but not assigned to semantic PLATFORM state. Text extras produce E208; duplicate source, non-point use, and PRIME conflict produce E632, E631, and E633.

### BACKGRND

Repeated static vectors produce E231; a second HOURLY file for one scope produces E168/E501. HOURLY and non-HOURLY coexist in either order. HOURLY data are primary and static profiles substitute missing hours.

### Grid continuation

GRIDCART and GRIDPOLR accept implicit, NetID-only, and fully explicit secondary lines inside active blocks. A different NetID produces E170 plus expected incomplete-block diagnostics.

### Discrete receptor conditional fields

DISCCART and DISCPOLR accept fields supplied under inactive ELEV/FLAGPOLE options with W229 and ignore them semantically. Missing active fields use W228.

## Gate update

Completed:

- `SO-PLATFORM-01`;
- `SO-BACKGRND-01`;
- `RE-GRID-ID-01`;
- `RE-DISC-EXTRA-01`.

The inventory becomes 19 total, 14 executed, 1 source-resolved, and 4 pending. Production syntax remains closed.

## Boundary

No production lexer, CST, preservation writer, semantic model, runner, output parser, or GIS layer was introduced.
