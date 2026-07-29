# Current State

- Updated: 2026-07-30
- Active branch: `main`
- Official behavior-probe batch 3 PR: #11, merged
- Batch 3 merge commit: `cab11308b022fe648dcb3bd5ba00bc7e758bc19a`
- Official behavior-probe batch 2 PR: #9, merged
- Batch 2 merge commit: `279b61160412a8073632d31156f897cd6edcee4a`
- Official behavior-probe batch 1 PR: #7, merged
- Batch 1 merge commit: `4e6e92ddd86420144438a4e6d2eb0b77b3db33ab`
- Whole-spec acceptance PR: #5, merged
- Package version: `0.0.1.dev0`
- Development phase: Phase 0 record-level specification accepted; official behavior-probe gate partially complete

## Authoritative mainline

The source-verified official-specification line remains authoritative. The former PR #2 parallel
prototype is retained only at `archive/pr2-parallel-prototype-20260729` and must not be used as a
development base. See ADR 0005 and `docs/worklog/2026-07-29-mainline-recovery.md`.

## Whole-spec record-set acceptance

The deterministic v26135 acceptance evaluator passes all seven dispatch modes and all 138 primary
source-dispatched records:

- CO: 39/39;
- SO: 40/40;
- RE: 9/9;
- ME: 23/23;
- EV: 5/5;
- ordinary OU: 18/18;
- event-output OU: 4/4.

Machine-readable evidence is in `reference/coverage/v26135-whole-spec-acceptance.json`.

## Official behavior probes — completed batches

### Batch 1

Resolved SWPOINT ALPHA dependency and six-field form, valid one/two VBARRIER forms, and sector-scoped
OZONEFIL/NOX_FILE repeatability.

### Batch 2

Resolved temporal-vector completeness, VBARRIER inclusive ranges and same-side selection, and
event-output FILEFORM behavior under DFAULT.

### Batch 3

Reviewed evidence contains 35 cases: 16 accepted, 19 rejected, 0 indeterminate, and 35/35 expectations met.

Resolved outcomes:

- seven ALPHA controls completed for gas-deposition, low-wind, and downwash cards;
- gas-deposition records use E196 for DFAULT conflicts and E198 when ALPHA is absent;
- LOW_WIND/AWMADWNW/ORD_DWNW expose E133/E122/E123 under DFAULT plus ALPHA;
- aircraft processing produces E198 without ALPHA and E198/E204 under DFAULT plus ALPHA;
- no-payload, repeated, and extra-field ARCFTOPT cards are accepted;
- exactly one ARCFTOPT payload assigns the airport ID, with later one-payload repeats winning in source state;
- aircraft dependencies retain E821, E822, and E823;
- both MAXDCONT signatures complete with dynamic or explicit trailing file units.

Reviewed evidence is in `reference/probes/v26135/batch3/result.json`,
`reference/probes/v26135/batch3/case-evidence.csv`, and
`docs/reference/V26135_OFFICIAL_BEHAVIOR_PROBES_BATCH3.md`.

Final PR #11 head `521bdb9c7c4857f3bc4507de4d742fa517e83d42` passed:

- full nine-job CI `30475925322`;
- batch-2 official regression `30475925186`;
- batch-3 official workflow `30475925233`.

Final-head artifact:

- artifact ID: `8733686581`;
- digest: `sha256:f7e7ffbb80f53de55db56e66a56d14c22731c061ce5fdd733a36fc1e258100c0`;
- size: `284,393,538` bytes.

## Retained behavior-probe gate

The normalized catalogs contain 19 questions:

- executed with retained official evidence: 10;
- source-resolved: 1;
- official-executable pending: 8.

The record-set gate remains passed, but the behavior gate remains incomplete. Production loss-aware
lexer/CST work must not begin until the remaining parser-shaping probes are resolved or explicitly
deferred through a preservation-safe ADR and the fixture freeze is complete.

## Cross-platform evidence policy

Byte-hashed retained probe evidence is pinned to LF through narrowly scoped `.gitattributes` rules.
This fixes Windows checkout hash drift without imposing a global newline policy on future CRLF syntax
fixtures.

## Not yet implemented

Production lexer/parser, immutable loss-aware CST, format-preserving writer, semantic project model,
runner, output parser, and GIS layers remain pending.

## Validation baseline

- 53/53 official decks executed in the established evidence workflow;
- all seven dispatcher exact-set reports pass;
- batch-1, batch-2, and batch-3 reviewed official workflows pass;
- final PR #11 head passed all nine CI jobs plus the batch-2 and batch-3 official workflows;
- PR #11 merged to `main` as `cab11308b022fe648dcb3bd5ba00bc7e758bc19a`.
