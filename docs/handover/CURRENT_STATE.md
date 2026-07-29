# Current State

- Updated: 2026-07-29
- Active branch: `main`
- Official behavior-probe batch 2 PR: #9, merged
- Batch 2 merge commit: `279b61160412a8073632d31156f897cd6edcee4a`
- Official behavior-probe batch 1 PR: #7, merged
- Batch 1 merge commit: `4e6e92ddd86420144438a4e6d2eb0b77b3db33ab`
- Whole-spec acceptance PR: #5, merged
- Whole-spec acceptance merge commit: `cbd721b80c5642d5fcc60ec2f77fe70095e9a79b`
- Recovery PR: #3, merged
- Recovery-state PR: #4, merged
- Package version: `0.0.1.dev0`
- Development phase: Phase 0 record-level specification accepted; official behavior-probe gate partially complete

## Authoritative mainline

The source-verified official-specification line remains authoritative. The former PR #2 parallel
prototype is retained only at `archive/pr2-parallel-prototype-20260729` and must not be used as a
development base. See ADR 0005 and `docs/worklog/2026-07-29-mainline-recovery.md`.

## Whole-spec record-set acceptance

The deterministic v26135 acceptance evaluator covers seven executable dispatch modes:

- CO: 39/39 primary `COCARD` records;
- SO: 40/40 primary `SOCARD` records;
- RE: 9/9 primary `RECARD` records;
- ME: 23/23 primary `MECARD` records;
- EV: 5/5 primary `EVCARD` records;
- OU: 18/18 ordinary `OUCARD` records;
- event output: 4/4 `EV_OUCARD` records.

The record-set gate passes for all 7 dispatchers and all 138 source-dispatched primary records.
Machine-readable evidence is in `reference/coverage/v26135-whole-spec-acceptance.json`.

## Official behavior probes — batch 1

Batch 1 resolved:

- six-parameter SWPOINT with/without ALPHA;
- valid one- and two-barrier VBARRIER field forms;
- distinct-sector versus same-sector OZONEFIL behavior;
- distinct-sector versus same-sector NOX_FILE behavior.

Reviewed evidence is in `reference/probes/v26135/batch1/result.json` and
`docs/reference/V26135_OFFICIAL_BEHAVIOR_PROBES_BATCH1.md`.

## Official behavior probes — batch 2

The reviewed evidence used workflow `30452705724`, artifact `8724254777`, and official executable
SHA-256 `599b491b021c7ec254ba3a1062386f287e56e54a0d3bb9b67cfa72275d6916da`.
The final PR head `cad179c0aeadfd4a3c52040ae351f99eaa46622d` independently passed:

- full nine-job CI `30454599189`;
- batch-1 official regression `30454599319`;
- batch-2 official 27-case workflow `30454598843`.

The final-head batch-2 artifact is:

- artifact ID: `8725024839`;
- digest: `sha256:12e28236b5669156cf3acd2fb81db8ce9b88c2ad179346e0f0fa2d0c531d6cee`;
- size: `220,514,827` bytes.

Batch 2 results:

- preparation: 1 accepted;
- cases: 27 total, 15 accepted, 12 rejected, 0 indeterminate;
- expectations met: 28/28 including preparation.

Resolved outcomes:

- complete global/sector MONTH O3VALUES and NOX_VALS vectors are accepted;
- incomplete O3VALUES is rejected with E261 and incomplete NOX_VALS with E603;
- both VBARRIER positions use inclusive HT 2..10, WT 2.5..13, LAI 4..10.92 and LM 0.55..3.75 ranges;
- immediate outside-range values map to E371-E374;
- unequal same-side barriers produce W375 and retain the nearer barrier;
- equal-distance same-side barriers retain both input records, emit no W375, then emit runtime W620 and use barrier 2 on the v26135 equality tie;
- event-output EXP remains exponential outside DFAULT + criteria pollutant;
- DFAULT + SO2 + EXP emits W595 and resets output to fixed notation.

Reviewed evidence is in `reference/probes/v26135/batch2/result.json` and
`docs/reference/V26135_OFFICIAL_BEHAVIOR_PROBES_BATCH2.md`.

## Retained behavior-probe gate

The refined catalogs normalize to 19 questions:

- executed with retained official-executable evidence: 7;
- source-resolved: 1;
- official-executable pending: 11.

The record-set gate remains passed, but the behavior-probe gate remains incomplete. Production
loss-aware lexer/CST work must not begin until the remaining parser-shaping probes are resolved or
explicitly deferred through a preservation-safe ADR and the fixture freeze is complete.

## Workflow hygiene

The batch-1 workflow path filter is now restricted to `batch1/manifest.json`; later behavior batches
will no longer trigger an unnecessary batch-1 rerun solely because they add another manifest.

## Not yet implemented

Production lexer/parser, immutable loss-aware concrete syntax tree, format-preserving writer,
semantic project model, runner, output parser, and GIS layers remain pending.

## Validation baseline

- 53/53 current official decks executed in the established evidence workflow;
- all seven dispatcher exact-set reports pass;
- whole-spec acceptance CI run `30443993754` passed all nine jobs;
- batch-1 official evidence workflow `30447131971` passed;
- batch-2 reviewed evidence workflow `30452705724` passed;
- final PR #9 head passed CI `30454599189`, batch-1 regression `30454599319`, and batch-2 official workflow `30454598843`;
- PR #9 merged to `main` as `279b61160412a8073632d31156f897cd6edcee4a`.
