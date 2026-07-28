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
- clean-room PyAERMOD v26135 gap-audit seed.

### Fixed

- corrected the Ruff `UP035` import location for `Mapping`;
- corrected strict-mypy narrowing in `ModelVersion.parse()`;
- restored a fully green GitHub Actions matrix after the repository became public and actionable CI logs became available.

### Documentation

- recorded that AERMAP remains 24142 while the current AERMOD release is 26135;
- recorded current materialization, checksum, PDF screenshot, and reference limitations;
- recorded the CI failure chain, concrete fixes, and successful 9-job matrix;
- advanced handover instructions from inventory creation to source-verified specification work.
