# Changelog

All notable project changes will be recorded here.

## Unreleased

### Added

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
- CO pathway batch 1 as four bundled specification fragments covering 14 records;
- source-verified catalogs for 40 `MODELOPT` tokens and 23 `DEBUGOPT` tokens;
- CO batch 1 evidence table, human-readable reference and structural tests;
- CO pathway batch 2 as three fragments covering 10 decay, receptor/urban, static ozone and NO2-ratio records;
- CO batch 2 evidence/promotions and tests for source-default, range and preservation boundaries;
- complete 39-record CO pathway specification, final 15-record evidence set, source exact-match verifier and official behavior-probe catalog;
- complete `MODELOPT` status audit for all 40 source-recognized tokens.

### Changed

- v26135 metadata completeness now reports complete source-verified record-level specifications for all primary pathways and the event-output submode;
- pathway fragment loading now composes positive older/equal batches into a newer aggregate batch;
- EPA archive, fixture and executable evidence workflows are manual-only after their initial successful evidence runs;
- keyword promotions are recorded in companion status-override/evidence layers until the main inventory is regenerated deterministically.

### Fixed

- corrected the Ruff `UP035` import location for `Mapping`;
- corrected strict-mypy narrowing in `ModelVersion.parse()`;
- restored a fully green GitHub Actions matrix after the repository became public and actionable logs became available;
- prevented official expected outputs from being overwritten during local numerical validation;
- corrected PM10 1987–1990 validation by preserving the MULTYEAR state-file chain;
- corrected interpretation of the `capped` maximum relative difference: it is localized to selected `STACK1C` second-highest table cells, not the overall maximum;
- corrected earlier SO inventory omissions for `PLATFORM` and `VBARRIER`;
- separated ordinary `OUCARD` from event-mode `EV_OUCARD` so `EVENTOUT` is not misclassified as an ordinary output record.

### Documentation

- recorded that AERMAP remains 24142 while current AERMOD is 26135;
- recorded official archive hashes, source structure, build flags and reproducible GNU build results;
- recorded a 53/53 successful official-deck execution baseline;
- classified official and reproduced-build parity evidence separately;
- verified that EPA's executable reproduces `capped` and `capped_nostd` exactly;
- documented Intel Fortran runtime evidence without overstating the exact compiler version;
- documented CO pathway continuation, loss-aware preservation, restart dependencies and repeatable `DEBUGOPT` behavior;
- preserved the `EVENTFIL` source-comment/implementation discrepancy for future executable tests;
- documented decay source-range boundaries, `OZONEFIL` manual/source repeatability evidence, `NO2STACK` sentinel behavior and `ARMRATIO` trailing-field preservation;
- completed record-level specifications for CO, SO, RE, ME, EV, ordinary OU, and event-output mode.

### Added — complete SO + RE specifications

- bundled all 40 v26135 SO primary records and all 9 RE primary records;
- added exact source-type-dependent `LOCATION`/`SRCPARAM` signatures, including source-recognized ALPHA `SWPOINT`;
- modeled `GRIDCART` and `GRIDPOLR` secondary records as nested loss-aware state machines;
- added SO/RE evidence tables, exact-set reports, official behavior probes, deterministic validator, tests, ADR, reference notes, and handover updates;
- validated the complete SO/RE payload through SHA256-controlled 9-platform reconstruction and a separate clean-tree 9-platform CI run.

### Added — complete ME + EV + OU specifications

- bundled all 23 v26135 ME primary records, all 5 EV primary records, and all 18 ordinary OU primary records;
- represented the 4-record `EV_OUCARD` event-output mode explicitly rather than merging it into ordinary `OUCARD`;
- added meteorological file/station/date/wind/SCIM/turbulence schemas and event period/location/include completeness rules;
- added ordinary and event output-family schemas, file-unit/name QA, `FILEFORM`, `NOHEADER`, daily/design-value, annual, multiyear, rank, evaluation, summary, and contribution controls;
- added exact-set reports, fixture occurrence evidence, output-family inventory, behavior probes, deterministic validator, tests, ADR, reference notes, worklog, and handover updates.
