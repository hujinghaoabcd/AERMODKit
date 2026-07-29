# Current State

- Updated: 2026-07-29
- Branch: `agent/bootstrap-project-foundation`
- Pull request: #1 (draft, unmerged)
- Package version: `0.0.1.dev0`
- Development phase: Phase 0 complete record-level specifications for all primary pathways; full-spec acceptance and loss-aware syntax implementation pending

## Complete pathway specifications

- CO: 39/39 primary `COCARD` records.
- SO: 40/40 primary `SOCARD` records, 13 executable-recognized source types, and source-type-dependent `SRCPARAM` signatures.
- RE: 9/9 primary `RECARD` records; `GRIDCART` and `GRIDPOLR` secondary records are modeled as nested block state machines.
- ME: 23/23 primary `MECARD` records.
- EV: 5/5 primary `EVCARD` records.
- OU: 18/18 ordinary `OUCARD` records.
- Event output: 4/4 `EV_OUCARD` records represented as an explicit event-output submode.

## ME, EV, and OU coverage

The bundled specifications now cover meteorological files and station metadata, date selection, wind controls, SCIM and turbulence filters, event period/location pairing, include boundaries, ordinary report tables, all current external output families, `FILEFORM`, `NOHEADER`, daily/design-value controls, and event-mode `EVENTOUT`.

Ordinary `OUCARD` and event-mode `EV_OUCARD` remain separate because `EVENTOUT` is mandatory in event processing but is not accepted by the ordinary output dispatcher.

## Evidence boundaries

Complete pathway specification means record-level source/evidence coverage. It does not mean that every cataloged official-executable behavior probe has been run, that source-recognized development syntax is regulatory, or that a production parser or application layer exists.

## Not yet implemented

Production lexer/parser, immutable loss-aware concrete syntax tree, format-preserving writer, semantic project model, runner, output parser, and GIS layers remain pending.

## Validation baseline

- local focused ME/EV/OU baseline: 27 pytest tests passed;
- ME source/spec comparison: 23/23, missing 0, extra 0;
- EV source/spec comparison: 5/5, missing 0, extra 0;
- ordinary OU source/spec comparison: 18/18, missing 0, extra 0;
- event-output source/spec comparison: 4/4, missing 0, extra 0;
- SHA256-controlled reconstruction run `30429920125`: all nine Ubuntu/Windows/macOS × Python 3.11/3.12/3.13 jobs passed and the apply job committed the verified payload;
- verified ME/EV/OU payload commit: `2ff484789bbdecd468d8d22f1f9d93f597a3b0ad`;
- ordinary CI restored in commit `bf3b2a3c4c8e9145efdf6305690e6ec07a7d69fb`;
- clean-tree ordinary CI run `30430048717`: all nine jobs passed without reconstruction chunks or temporary apply logic;
- final documentation-state CI will be recorded after this handover update is committed.
