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
- machine-readable regression results and output-file coverage reports;
- cross-platform official-executable parity probe and focused Windows evidence workflow;
- SHA256 and binary-format evidence for the EPA v26135 executable archive and `aermod.exe`;
- explicit official-executable versus reproduced-source-build parity tiers.

### Fixed

- corrected the Ruff `UP035` import location for `Mapping`;
- corrected strict-mypy narrowing in `ModelVersion.parse()`;
- restored a fully green GitHub Actions matrix after the repository became public and actionable CI logs became available;
- prevented official expected outputs from being overwritten during local numerical validation;
- changed EPA archive, fixture, and executable evidence workflows to manual-only triggers after their initial runs;
- corrected PM10 1987–1990 validation by preserving the required MULTYEAR state-file chain;
- corrected the interpretation of the `capped` 5.2613% maximum relative difference: it is localized to selected `STACK1C` second-highest table cells, not the overall model maximum.

### Documentation

- recorded that AERMAP remains 24142 while the current AERMOD release is 26135;
- recorded official archive hashes, source structure, build flags, and reproducible GNU build results;
- recorded a 53/53 successful official-deck execution baseline;
- classified main-output parity into canonical, representation/tie, minor drift, moderate drift, and compiler-specific categories;
- verified that the EPA executable reproduces `capped` and `capped_nostd` expected outputs exactly;
- documented Intel Fortran runtime evidence in the official Windows executable without overstating the exact compiler version;
- advanced handover instructions from parity investigation to exact CO-pathway keyword-schema completion.
