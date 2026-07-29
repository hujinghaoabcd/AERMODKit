# AERMOD v26135 whole-spec acceptance

## Scope

This report accepts the source-dispatched primary record specification. It does not claim that the production lexer/CST/writer, semantic model, runner, output parser, or GIS layers exist. Behavior probes remain a separate prerequisite gate.

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
- executed with retained official-executable evidence: 14
- source-resolved: 1
- official-executable pending: 4

### Batch 1

- `SO-SWPOINT-01`;
- valid one/two-barrier forms from `SO-VBARRIER-01`;
- `ozonefil_same_sector_duplicate`;
- `nox_file_same_sector_duplicate`.

### Batch 2

- `temporal_vector_incomplete`;
- `SO-VBARRIER-RANGE-01`;
- `OU-EVENT-FILEFORM`.

### Batch 3

- `alpha_dependency_matrix`;
- `arcftopt_repeat_extra_fields`;
- `OU-MAXDCONT-FORMS`.

### Batch 4

- `SO-PLATFORM-01`;
- `SO-BACKGRND-01`;
- `RE-GRID-ID-01`;
- `RE-DISC-EXTRA-01`.

Record-set acceptance passes, but the project remains before the production loss-aware syntax gate until the four ME/EV/OU executable probes are resolved and the clean-room audit/fixture freeze are complete.
