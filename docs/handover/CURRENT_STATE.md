# Current State

- Updated: 2026-07-29
- Branch: `agent/bootstrap-project-foundation`
- Pull request: #1 (draft)
- Package version: `0.0.1.dev0`
- Development phase: Phase 0 official capability inventory

## What exists

- a Python package using the `src/` layout;
- structured diagnostics and AERMOD release identifiers;
- a resource-backed v26135 metadata registry explicitly labelled incomplete;
- an official v26135 asset manifest with independent component versions;
- a broad evidence-ranked keyword/pathway inventory;
- an official source-type inventory including 12 confirmed LOCATION types;
- an output-control inventory and parser-priority seed;
- a provisional/confirmed Fortran source-map seed;
- a clean-room PyAERMOD gap-audit seed;
- architecture, source-of-truth, clean-room, worklog, and handover records.

## Verified locally

- editable setuptools installation succeeds;
- 7 pytest tests pass;
- `src/` and `tests/` compile to bytecode;
- generated CSV files parse successfully and contain evidence-status fields.

## CI state

The first GitHub Actions matrix run failed before useful step/log information was returned by the connector. The exact cause remains unresolved. Ruff and mypy have not yet been observed passing in GitHub Actions and were unavailable locally.

## Reference-material state

- current EPA web metadata and parsed current PDF text were inspected;
- current v26135 binaries/source/sample/test archives are not materialized locally;
- SHA256 values are therefore not available;
- the retained local User Guide PDF is the October 2023 edition and is historical only;
- AERMAP remains 24142 while AERMOD, AERMET, AERMINUTE, AERSURFACE, and AERPLOT are recorded as 26135.

## What does not exist yet

- no line-level, source-verified complete keyword schema;
- no exact argument/range/default/dependency matrix for every keyword;
- no AERMOD input lexer, parser, AST, writer, or semantic project model;
- no executable runner;
- no output parser;
- no GIS code;
- no claim of complete AERMOD support;
- no final open-source licence decision.

## Non-negotiable constraints

1. Official EPA material is authoritative.
2. Third-party projects are comparison references only.
3. Unsupported official content must not be silently discarded.
4. Every material session ends with updated handover and worklog records.
5. Unknown CI failures must remain explicitly unknown until supported by logs.
6. Inventory evidence levels must not be promoted without official support.
