# Next Steps

## Immediate next task: CO batch 3 temporal ozone and ambient NOx controls

Complete the records deliberately deferred from batch 2:

1. `O3VALUES` and `OZONUNIT`, including temporal flags and exact vector cardinalities;
2. `NOXSECTR`, `NOX_FILE`, `NOXVALUE`, `NOX_VALS`, `NOX_UNIT`;
3. fallback precedence among constant, temporal and hourly-file background inputs;
4. sector-specific conflicts and FINISHED checks;
5. GRSM-only applicability for ambient NOx records.

## Then: remaining CO controls

- `GASDEPDF`, `GASDEPVD`, `GDLANUSE`, `GDSEASON`;
- `LOW_WIND`, `AWMADWNW`, `ORD_DWNW`;
- `ARCFTOPT`;
- remaining dispatch-map records and per-option regulatory/development status for all MODELOPT tokens.

## Focused official-executable probes

Add small, manual evidence workflows for:

- zero/negative `HALFLIFE` and `DCAYCOEF`;
- same-sector repeated `OZONEVAL` and `OZONEFIL`;
- OZONEFIL source/manual repeatability behavior;
- invalid `URBANOPT` roughness under DFAULT/non-DFAULT;
- trailing fields on `ARMRATIO`;
- previously listed `EVENTFIL`, restart and repeated DEBUGOPT edge cases.

## Inventory and schema engineering

- add a deterministic inventory generator that merges seed rows with status overrides;
- add consistency checks so every promoted keyword resolves to exactly one bundled record;
- keep older completed fragment batches immutable and permit composition only into equal/newer aggregate batches;
- do not start production parser classes yet.

## Parser acceptance remains pending

Before parser work: complete CO and representative other pathways, select EV/unknown/development preservation fixtures, finish the clean-room PyAERMOD audit and test preservation policy.
