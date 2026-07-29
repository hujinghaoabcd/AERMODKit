# Current State

- Updated: 2026-07-29
- Active development branch: `agent/official-behavior-probes-batch1`
- Active pull request: #7, draft pending final branch CI and evidence review closure
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

The first reviewed official-executable batch used AERMOD v26135 executable SHA-256
`599b491b021c7ec254ba3a1062386f287e56e54a0d3bb9b67cfa72275d6916da`.

- workflow run: `30447131971`;
- artifact ID: `8721942233`;
- cases: 9;
- accepted: 6;
- rejected: 3;
- indeterminate: 0.

Resolved outcomes:

- six-parameter SWPOINT is accepted with ALPHA and rejected without ALPHA by `SO E198`;
- valid one- and two-barrier VBARRIER forms are accepted for ALPHA/FLAT RLINEXT;
- OZONEFIL is repeatable across distinct O3 sectors but same-sector reassignment is rejected by `CO E501`;
- NOX_FILE is repeatable across distinct NOx sectors but same-sector reassignment is rejected by `CO E501`.

Reviewed evidence is in `reference/probes/v26135/batch1/result.json` and
`docs/reference/V26135_OFFICIAL_BEHAVIOR_PROBES_BATCH1.md`.

## Retained behavior-probe gate

The refined catalogs now normalize to 19 questions:

- executed with retained official-executable evidence: 4;
- source-resolved: 1;
- official-executable pending: 14.

`SO-VBARRIER-RANGE-01` keeps range-boundary inclusivity and same-side `W375` behavior explicit rather
than incorrectly treating those untested details as complete.

The behavior-probe gate remains incomplete. Production loss-aware lexer/CST work must not begin until
the remaining parser-shaping probes are resolved or explicitly deferred through a preservation-safe ADR.

## Not yet implemented

Production lexer/parser, immutable loss-aware concrete syntax tree, format-preserving writer,
semantic project model, runner, output parser, and GIS layers remain pending.

## Validation baseline

- 53/53 current official decks executed in the established evidence workflow;
- all seven dispatcher exact-set reports pass;
- whole-spec acceptance CI run `30443993754` passed all nine jobs;
- behavior-probe harness/manifest head `1cd8e13dc2af2d0cc9fb88255ad7e96c190fade6` passed official workflow `30447131971`;
- the same head passed all nine Ubuntu/Windows/macOS × Python 3.11/3.12/3.13 jobs in CI `30447131982`;
- final documentation/catalog commits still require the branch's final CI before PR #7 can be marked ready.
