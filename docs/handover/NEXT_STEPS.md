# Next Steps

## Immediate major stage

Complete the remaining input pathways in two large stages rather than many small batches:

1. **SO + RE together** — all source definitions, source-type-dependent SRCPARAM signatures, downwash/barriers/roads/background/hourly emissions, Cartesian/polar/discrete receptor blocks, and include handling.
2. **ME + EV + OU together** — meteorology, event processing, output controls, output-family schemas, and file-format/header behavior.

## Parallel evidence work

Run the focused official-executable probes listed in `reference/coverage/v26135-co-official-behavior-probes.json` for the remaining guide/source discrepancies. These probes do not block moving to SO+RE because the ambiguity is explicit and loss-aware preservation is already required.

## After all pathways

- complete clean-room PyAERMOD coverage audit;
- run deterministic full-spec consistency generation;
- select unknown/development syntax fixtures;
- implement token/source-location model, pathway state machine, immutable loss-aware syntax tree, format-preserving writer, and round-trip tests;
- only then map to semantic project models and runner/output/GIS layers.
