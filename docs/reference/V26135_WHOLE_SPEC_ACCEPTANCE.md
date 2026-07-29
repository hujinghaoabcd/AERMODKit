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

- total: 18
- executed with retained evidence: 0
- source-resolved: 1
- official-executable pending: 17

Record-set acceptance therefore passes, but the project remains before the production
loss-aware syntax implementation gate until the retained executable
probes are resolved.
