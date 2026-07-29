# AERMOD v26135 whole-spec acceptance

## Scope

This report accepts the source-dispatched primary record specification. It does not claim
that the production lexer/CST/writer, semantic model, runner, output parser,
or GIS layers exist. Behavior probes remain a separate prerequisite gate.

## Gate summary

- record-set gate: **PASS**
- behavior-probe gate: **INCOMPLETE**
- syntax implementation ready: **NO**
- accepted dispatchers: 7/7
- source-dispatched primary records: 138

## Dispatcher acceptance

| Dispatcher | Expected | Source | Bundled | Exact set | Framing | Syntax | Preservation | Result |
|---|---:|---:|---:|---|---|---|---|---|
| CO | 39 | 39 | 39 | yes | yes | yes | yes | PASS |
| SO | 40 | 40 | 40 | yes | yes | yes | yes | PASS |
| RE | 9 | 9 | 9 | yes | yes | yes | yes | PASS |
| ME | 23 | 23 | 23 | yes | yes | yes | yes | PASS |
| EV | 5 | 5 | 5 | yes | yes | yes | yes | PASS |
| OU | 18 | 18 | 18 | yes | yes | yes | yes | PASS |
| OU/EVENT | 4 | 4 | 4 | yes | yes | yes | yes | PASS |

## Retained behavior probes

- total: 19
- executed with retained official-executable evidence: 4
- source-resolved: 1
- official-executable pending: 14

The first official-executable batch resolved:

- `SO-SWPOINT-01`;
- `SO-VBARRIER-01` for valid one- and two-barrier field forms;
- `ozonefil_same_sector_duplicate`;
- `nox_file_same_sector_duplicate`.

The earlier combined VBARRIER question was split so that field-form acceptance is complete while
range-boundary and same-side `W375` behavior remains explicit as `SO-VBARRIER-RANGE-01`.

Record-set acceptance therefore passes, but the project remains before the production
loss-aware syntax implementation gate until the remaining parser-shaping executable
probes are resolved or explicitly deferred through a preservation-safe ADR.
