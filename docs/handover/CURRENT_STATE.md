# Current State

- Updated: 2026-07-29
- Branch: `agent/bootstrap-project-foundation`
- Pull request: #1 (draft)
- Package version: `0.0.1.dev0`
- Development phase: Phase 0 bootstrap

## What exists

- a Python package using the `src/` layout;
- strict Ruff, mypy, and pytest configuration;
- a structured `Diagnostic` model designed for CLI, GIS, desktop, and web clients;
- a validated five-digit `ModelVersion` value object;
- a resource-backed version metadata registry;
- v26135 metadata, explicitly labelled metadata-only and incomplete;
- cross-platform CI definition for Python 3.11–3.13;
- architecture, policy decisions, roadmap, and mandatory session handover rules.

## Verified locally

- editable setuptools installation succeeds;
- 7 pytest tests pass;
- `src/` and `tests/` compile to bytecode;
- final code/configuration corrections were retested.

## CI state

The first GitHub Actions matrix run failed before useful step/log information was returned by the connector. The exact cause is unresolved. Ruff and mypy have not yet been observed passing in GitHub Actions and were unavailable locally.

## What does not exist yet

- no AERMOD input lexer, parser, AST, writer, or semantic project model;
- no keyword/pathway/source coverage matrix;
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
