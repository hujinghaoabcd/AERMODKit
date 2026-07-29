# Changelog

All notable project changes will be recorded here.

## Unreleased

### Recovery

- restored the 60-commit, source-verified official-specification line as the authoritative working tree through a non-destructive two-parent merge;
- preserved the merged PR #2 parallel prototype at `archive/pr2-parallel-prototype-20260729` for later clean-room salvage review;
- restored the accepted stage order: whole-spec acceptance, loss-aware CST, format-preserving writer, semantic model, runner/results, then GIS;
- added ADR 0005 and a durable mainline-recovery worklog.

### Added

- deterministic v26135 whole-spec acceptance models for dispatcher and retained behavior-probe gates;
- machine-readable and Markdown acceptance reports covering seven dispatch modes and 138 primary records;
- official v26135 behavior-probe harness with isolated workspaces, asset/deck/output hashes, parsed diagnostics and source-range evidence;
- manifest-driven batch-2 harness supporting preparation-generated downstream decks, regex mutations, required-file checks and reusable case fragments;
- exact official-source diagnostic context extraction for E261, E603, E371-E374, W375, W620 and W595;
- reviewed batch-1 evidence for SWPOINT, VBARRIER field forms, OZONEFIL sector repetition and NOX_FILE sector repetition;
- reviewed batch-2 evidence for temporal-vector completeness, VBARRIER ranges/same-side selection and event-output FILEFORM behavior;
- compact retained results, detailed reference reports, workflow artifact provenance, source pattern evidence and probe-manifest tests;
- CLI regeneration tool and repository integration tests for acceptance evidence;
- initial package metadata and CI;
- structured diagnostic model;
- AERMOD release identifier and version metadata registry;
- architecture, decision, worklog and handover documentation;
- official v26135 asset/component manifest;
- evidence-ranked keyword, source-type, output and source-code mapping inventories;
- clean-room PyAERMOD v26135 gap-audit seed;
- cryptographic hashes and archive indexes for official source, executable, sample-run and test-case assets;
- declaration-level index for 566 Fortran program units;
- source-verified pathway dispatch and primary-record branch mapping;
- current 53-deck official fixture and feature registry;
- reproducible official-case validation with isolated workspaces and PM10 MULTYEAR chaining;
- machine-readable regression results and output-file coverage;
- official-executable parity probe and focused Windows evidence workflow;
- explicit official-executable versus reproduced-source-build parity tiers;
- versioned pathway-specification loader with structural validation;
- complete source-verified record-level specifications for all primary pathways and event-output mode;
- exact source-type-dependent `LOCATION`/`SRCPARAM` signatures for 13 executable-recognized source types;
- nested state-machine schemas for `GRIDCART` and `GRIDPOLR`;
- exact-set reports, fixture occurrence evidence, behavior probes, validators, tests, ADRs, reference notes and handover records.

### Changed

- v26135 completeness is expressed as separate record-set and behavior-probe gates;
- the refined behavior inventory contains 19 questions: 7 executed, 1 source-resolved and 11 official-executable pending;
- SWPOINT has retained official evidence for its ALPHA dependency and six-parameter form;
- VBARRIER one/two forms, inclusive parameter ranges, E371-E374 mapping and same-side W375/W620 behavior are retained;
- incomplete O3VALUES and NOX_VALS vectors are tied to E261 and E603 across global/sector scopes with source-supported flag generalization;
- event-output FILEFORM EXP is retained outside DFAULT + criteria-pollutant use and resets to FIX with W595 inside that condition;
- OZONEFIL and NOX_FILE repeatability is scoped by sector: distinct-sector records are accepted and same-sector reassignment is rejected with `E501`;
- parser-entry readiness remains false while 11 official-executable probes are pending and fixture freeze is incomplete;
- v26135 metadata completeness reports complete source-verified record-level specifications for all primary pathways and event-output mode;
- pathway fragment loading composes positive older/equal batches into newer aggregate batches;
- EPA archive, fixture and executable evidence workflows are manual-only after initial successful evidence runs;
- keyword promotions are recorded in companion status-override/evidence layers until deterministic inventory regeneration.

### Fixed

- made behavior-probe unsuccessful-completion matching case-insensitive and included fatal diagnostics emitted only in the main output;
- replaced invalid exploratory VBARRIER values with source-valid LAI and LM inputs before retaining final evidence;
- added first/second barrier endpoint controls and equal-distance same-side evidence before closing the VBARRIER range probe;
- added global/sector temporal controls before generalizing temporal-vector completeness behavior;
- added distinct-sector controls and different filenames to isolate same-sector OZONEFIL/NOX_FILE duplicate behavior;
- corrected Ruff `UP035` import location and strict-mypy narrowing;
- restored a green cross-platform GitHub Actions matrix;
- prevented official expected outputs from being overwritten during local numerical validation;
- corrected PM10 1987–1990 MULTYEAR state-file chaining;
- separated ordinary `OUCARD` from event-mode `EV_OUCARD`;
- corrected SO inventory omissions for `PLATFORM` and `VBARRIER`;
- recovered the official-specification mainline after the parallel PR #2 implementation was mistakenly merged.

### Documentation

- recorded batch-1 official executable outcomes, diagnostic codes, asset hashes, artifact provenance and interpretation boundaries;
- recorded batch-2 executable/source outcomes, generated EVENT-deck provenance, debug evidence and representative-case generalization boundaries;
- recorded the explicit parser-entry criteria after whole-spec record-set acceptance;
- recorded AERMAP 24142 versus AERMOD 26135 component versioning;
- recorded official archive hashes, source structure, build flags and GNU build results;
- recorded 53/53 official-deck execution and parity evidence;
- documented preservation targets, source/manual discrepancies, development syntax boundaries and complete pathway specifications.
