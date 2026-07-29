# Current State

- Updated: 2026-07-29
- Active branch: `main`
- Recovery PR: #3, merged
- Recovery-state PR: #4, merged
- Original foundation PR: #1, automatically marked merged because its full history is now reachable from `main`
- Package version: `0.0.1.dev0`
- Development phase: Phase 0 complete record-level specifications; whole-spec acceptance and loss-aware syntax implementation are next

## Mainline recovery completed

The source-verified official-specification line is again the authoritative project tree. Recovery
used a non-destructive two-parent merge and did not force-push or rewrite history.

- PR #1 head retained: `0739b9104b3784ab80aa980a00212404d24f29bc`
- two-parent recovery commit: `6959ecee34c0e9b69cecb56030018ca1ba53ac24`
- recovery PR #3 merge commit: `e9a4ebb453ab855512cd4c39be1b227df53689ea`
- recovery CI run `30441812294`: all nine Ubuntu/Windows/macOS × Python 3.11/3.12/3.13 jobs passed
- recovery-state CI run `30442044413`: all nine jobs passed
- PR #2 parallel prototype retained at `archive/pr2-parallel-prototype-20260729`
- stale branch `agent/0.1-typed-includes-runner` contains no work beyond the former PR #2 `main` state and must not be used as a development base

See ADR 0005 and `docs/worklog/2026-07-29-mainline-recovery.md`.

## Complete pathway specifications

- CO: 39/39 primary `COCARD` records.
- SO: 40/40 primary `SOCARD` records, 13 executable-recognized source types, and source-type-dependent `SRCPARAM` signatures.
- RE: 9/9 primary `RECARD` records; `GRIDCART` and `GRIDPOLR` secondary records are modeled as nested block state machines.
- ME: 23/23 primary `MECARD` records.
- EV: 5/5 primary `EVCARD` records.
- OU: 18/18 ordinary `OUCARD` records.
- Event output: 4/4 `EV_OUCARD` records represented as an explicit event-output submode.

## Evidence boundaries

Complete pathway specification means record-level source/evidence coverage. It does not mean that
every behavior probe has been run, that source-recognized development syntax is regulatory, or
that a production parser or application layer exists.

## Not yet implemented

Production lexer/parser, immutable loss-aware concrete syntax tree, format-preserving writer,
semantic project model, runner, output parser, and GIS layers remain pending.

## Validation baseline

- official assets, hashes, archive indexes, source declarations, fixtures, and parity evidence are recorded;
- 53/53 current official decks executed in the established evidence workflow;
- CO/SO/RE/ME/EV/ordinary-OU/event-output exact-set verification is complete;
- prior clean-tree and documentation CI matrices passed;
- recovery and recovery-state CI both passed all nine jobs, including Ruff, strict mypy, and pytest.
