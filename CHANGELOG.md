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
- CO batch 2 evidence/promotions and tests for source-default, range and preservation boundaries.

### Changed

- v26135 metadata completeness now reports CO batches 1-2 with 24 source-verified records;
- pathway fragment loading now composes positive older/equal batches into a newer aggregate batch;
- EPA archive, fixture and executable evidence workflows are manual-only after their initial successful evidence runs;
- keyword promotions are recorded in a companion status-override/evidence layer until the main inventory is regenerated deterministically.

### Fixed

- corrected the Ruff `UP035` import location for `Mapping`;
- corrected strict-mypy narrowing in `ModelVersion.parse()`;
- restored a fully green GitHub Actions matrix after the repository became public and actionable logs became available;
- prevented official expected outputs from being overwritten during local numerical validation;
- corrected PM10 1987–1990 validation by preserving the MULTYEAR state-file chain;
- corrected interpretation of the `capped` maximum relative difference: it is localized to selected `STACK1C` second-highest table cells, not the overall maximum.

### Documentation

- recorded that AERMAP remains 24142 while current AERMOD is 26135;
- recorded official archive hashes, source structure, build flags and reproducible GNU build results;
- recorded a 53/53 successful official-deck execution baseline;
- classified official and reproduced-build parity evidence separately;
- verified that EPA's executable reproduces `capped` and `capped_nostd` exactly;
- documented Intel Fortran runtime evidence without overstating the exact compiler version;
- documented CO pathway continuation, loss-aware preservation, restart dependencies and repeatable `DEBUGOPT` behavior;
- preserved the `EVENTFIL` source-comment/implementation discrepancy for future executable tests;
- documented decay source-range boundaries, OZONEFIL manual/source repeatability evidence, NO2STACK sentinel behavior and ARMRATIO trailing-field preservation;
- advanced the handover from CO batch 2 to temporal ozone and ambient NOx controls.
