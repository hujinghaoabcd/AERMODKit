# Current State

- Updated: 2026-07-29
- Active development branch: `agent/whole-spec-acceptance`
- Recovery PR: #3, merged
- Recovery-state PR: #4, merged
- Original foundation PR: #1, automatically marked merged because its full history is now reachable from `main`
- Package version: `0.0.1.dev0`
- Development phase: Phase 0 record-level specification accepted; retained behavior-probe gate remains incomplete

## Mainline recovery completed

The source-verified official-specification line is the authoritative project tree. Recovery used a
non-destructive two-parent merge and did not force-push or rewrite history.

- PR #1 head retained: `0739b9104b3784ab80aa980a00212404d24f29bc`
- two-parent recovery commit: `6959ecee34c0e9b69cecb56030018ca1ba53ac24`
- recovery PR #3 merge commit: `e9a4ebb453ab855512cd4c39be1b227df53689ea`
- recovery CI run `30441812294`: all nine Ubuntu/Windows/macOS × Python 3.11/3.12/3.13 jobs passed
- recovery-state CI run `30442044413`: all nine jobs passed
- PR #2 parallel prototype retained at `archive/pr2-parallel-prototype-20260729`
- stale branch `agent/0.1-typed-includes-runner` must not be used as a development base

See ADR 0005 and `docs/worklog/2026-07-29-mainline-recovery.md`.

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
The evaluator also checks framing uniqueness, non-empty syntax forms, required preservation-policy
flags, source/bundled counts, and exact source-report correspondence.

Machine-readable evidence is in
`reference/coverage/v26135-whole-spec-acceptance.json`; the human report is
`docs/reference/V26135_WHOLE_SPEC_ACCEPTANCE.md`.

## Retained behavior-probe gate

The three existing probe catalogs normalize to 18 retained questions:

- executed with retained final evidence: 0;
- source-resolved: 1;
- official-executable pending: 17.

The record-set gate therefore passes, but the behavior-probe gate remains incomplete. Production
loss-aware lexer/CST work must not begin until the targeted executable probes required by the parser
entry criteria are resolved or explicitly deferred through an ADR with preservation-safe behavior.

## Evidence boundaries

Record-set acceptance means source/evidence-backed dispatcher coverage. It does not mean that every
behavior probe has been run, that source-recognized development syntax is regulatory, or that a
production parser or application layer exists.

## Not yet implemented

Production lexer/parser, immutable loss-aware concrete syntax tree, format-preserving writer,
semantic project model, runner, output parser, and GIS layers remain pending.

## Validation baseline

- official assets, hashes, archive indexes, source declarations, fixtures, and parity evidence are recorded;
- 53/53 current official decks executed in the established evidence workflow;
- all seven dispatcher exact-set reports pass;
- deterministic whole-spec acceptance code, CLI generation, reports, and tests are present;
- recovery and recovery-state CI both passed all nine jobs, including Ruff, strict mypy, and pytest.
