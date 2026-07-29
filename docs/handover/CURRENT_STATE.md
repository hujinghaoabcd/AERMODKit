# Current State

- Updated: 2026-07-29
- Branch: `agent/recover-official-spec-mainline`
- Package version: `0.0.1.dev0`
- Development phase: Phase 0 complete record-level specifications for all primary pathways; mainline recovery and whole-spec acceptance pending

## Mainline recovery

The official-specification tree from PR #1 is being restored through a non-destructive two-parent
merge. The former PR #2 tree is preserved at `archive/pr2-parallel-prototype-20260729` and is not
an active implementation baseline. See ADR 0005 and the mainline-recovery worklog.

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

- local focused ME/EV/OU baseline: 27 pytest tests passed;
- ME source/spec comparison: 23/23, missing 0, extra 0;
- EV source/spec comparison: 5/5, missing 0, extra 0;
- ordinary OU source/spec comparison: 18/18, missing 0, extra 0;
- event-output source/spec comparison: 4/4, missing 0, extra 0;
- SHA256-controlled reconstruction run `30429920125`: all nine Ubuntu/Windows/macOS × Python 3.11/3.12/3.13 jobs passed;
- clean-tree ordinary CI run `30430048717`: all nine jobs passed;
- documentation-state CI run `30430392577`: all nine jobs passed;
- final validation-record run `30430643785`: all nine jobs passed.
