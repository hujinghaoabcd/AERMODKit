# Changelog

All notable project changes will be recorded here.

## Unreleased

### Added

- initial package metadata and CI;
- structured diagnostic model;
- AERMOD release identifier and version metadata registry;
- v26135 bootstrap metadata explicitly marked as incomplete;
- architecture, decision, worklog, and handover documentation;
- official v26135 asset/component manifest;
- evidence-ranked keyword, source-type, output, and source-code mapping inventories;
- clean-room PyAERMOD v26135 gap-audit seed;
- cryptographic hashes and archive indexes for the official v26135 source, sample-run, and test-case assets;
- declaration-level index for 566 Fortran program units;
- source-verified pathway dispatch and primary-record branch mapping;
- current 53-deck official fixture and feature registry;
- reproducible official-case validation tool with isolated workspaces and PM10 MULTYEAR chaining;
- machine-readable regression results and output-file coverage reports.

### Fixed

- corrected the Ruff `UP035` import location for `Mapping`;
- corrected strict-mypy narrowing in `ModelVersion.parse()`;
- restored a fully green GitHub Actions matrix after the repository became public and actionable CI logs became available;
- prevented official expected outputs from being overwritten during local numerical validation;
- corrected PM10 1987–1990 validation by preserving the required MULTYEAR state-file chain.

### Documentation

- recorded that AERMAP remains 24142 while the current AERMOD release is 26135;
- recorded official archive hashes, source structure, build flags, and reproducible GNU build results;
- recorded a 53/53 successful official-deck execution baseline;
- classified main-output parity into canonical, representation/tie, minor drift, moderate drift, and compiler-sensitive categories;
- documented the unresolved `capped` compiler-sensitive numerical finding;
- advanced handover instructions from asset materialization to parity investigation and exact keyword-schema completion.
