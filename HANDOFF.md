# AERMODKit handover

- Updated: 2026-07-29
- Current package version: 0.1.0a1
- EPA baseline: AERMOD v26135
- Current completed unit: 0.1 progress 01 — versioned schema and lossless syntax core

## Original task

Build an independent, GIS-first AERMOD Python ecosystem based on EPA official manuals,
Fortran source, release notes, and test cases. Do not copy or treat PyAERMOD as authoritative.
Do not rewrite the regulatory numerical core. The same UI-independent package must eventually
support Python, CLI, QGIS, desktop, and web applications.

## Non-negotiable principles

1. EPA official programs are the numerical source of truth.
2. GIS is a domain capability, not an optional plotting helper.
3. Every keyword/default/compatibility rule is tied to an AERMOD version and evidence.
4. Unknown keywords, comments, ordering, and raw text are retained.
5. Road geometries may not be collapsed to first/last points or first multipart members.
6. Large spatial assets stay outside small JSON/YAML project configuration files.
7. Each work unit updates progress and handover documents.

## Implemented files

- `src/aermodkit/schema/`: version models, registry, and v26135 data.
- `src/aermodkit/syntax/`: lossless AST, lexer, parser, and writers.
- `src/aermodkit/validation/`: schema-driven validation engine.
- `tests/`: registry, round-trip, and compatibility tests.
- `docs/progress/2026-07-29_0.1_schema_syntax_core.md`.

## Current behavioral guarantees

- `parse -> preserve write` does not discard unknown statements or comments.
- Canonical output is deterministic.
- v26135 MODELOPT tokens are registered once in a central schema.
- All 13 source types have explicit LOCATION and SRCPARAM contracts.
- `RLINEXT` and `SWPOINT` require ALPHA.
- Diagnostic records contain rule IDs, severity, pathway, keyword, line, source ID,
  and evidence slots.

## Known boundaries

- Only the first CO/SO keyword subset is semantically registered.
- Unknown keywords are preserved and warned about, but not interpreted.
- Continuation-card semantics and include-file expansion are not yet modeled.
- No EPA binary execution is part of this first unit.
- No GIS data model has been implemented yet.

## Next locked task

### 0.1 progress 02 — complete v26135 keyword registry and semantic mapping

1. Extract all CO and SO keywords from the July 2026 Quick Reference/User's Guide.
2. Add RE, ME, EV, and OU keyword schemas.
3. Model repeatable keywords and continuation-card families explicitly.
4. Add keyword dependencies, ordering rules, and version evidence.
5. Introduce semantic project mapping while retaining the AST as the lossless authority.
6. Add official sample/test-case fixtures and prepare real v26135 executable validation.

Do not start the QGIS plugin, web UI, output visualization, or roadway GIS conversion before
this schema/syntax foundation is complete.
