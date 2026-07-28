# Current State

- Updated: 2026-07-29
- Branch: `agent/bootstrap-project-foundation`
- Package version: `0.0.1.dev0`
- Development phase: Phase 0 bootstrap

## What exists

- a Python package using the `src/` layout;
- strict Ruff, mypy, and pytest configuration;
- a structured `Diagnostic` model designed for CLI, GIS, desktop, and web clients;
- a validated five-digit `ModelVersion` value object;
- a resource-backed version metadata registry;
- v26135 metadata, explicitly labelled metadata-only and incomplete;
- cross-platform CI for Python 3.11–3.13;
- architecture, policy decisions, roadmap, and session handover rules.

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
