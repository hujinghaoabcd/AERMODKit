# AERMODKit handover

- Updated: 2026-07-29
- Current package version: 0.1.0a2
- EPA baseline: AERMOD v26135
- Current completed unit: 0.1 progress 02 — full registry and semantic mapping

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
7. The semantic project view never replaces the lossless AST as source of truth.
8. Each work unit updates tests, progress, and handover documents.

## Completed

- Versioned schema primitives and v26135 registry loading.
- All 36 v26135 MODELOPT tokens and all 13 source types.
- Full CO/SO/RE/ME/EV/OU statement-keyword registry.
- Lossless parser plus preserve/canonical writers.
- Explicit GRIDCART and GRIDPOLR continuation families.
- Keyword, option, source, ordering, continuation, and cross-pathway diagnostics.
- Read-only semantic projection for options, pollutant, periods, sources, met, outputs,
  and include references.
- Official-syntax multi-pathway fixture and expanded regression tests.

## Current guarantees

- `parse -> preserve write` retains every original line.
- Unknown future keywords remain in the AST and produce warnings rather than deletion.
- Every known keyword carries pathway-specific EPA v26135 evidence.
- The complete registered keyword surface is test-asserted.
- Semantic mapping retains `model.document is original_document`.

## Known boundaries

- Multi-form keywords still use conservative argument ranges rather than discriminated forms.
- Included files are referenced but are not recursively expanded.
- Values are not yet fully converted to typed fields with units/range validation.
- No EPA binary runner or numeric parity harness is included yet.
- GIS roadway conversion remains intentionally deferred.

## Next locked task

### 0.1 progress 03 — typed keyword forms, include graph, and official binary harness

1. Add discriminated forms for complex keywords and continuation records.
2. Implement safe include resolution, cycle detection, and dependency graph export.
3. Add typed fields, units, enum/range validation, and field-level diagnostics.
4. Add v26135 binary discovery/build provenance and execution metadata.
5. Import selected official EPA test cases and compare generated outputs.
6. Add a workspace manifest and immutable run ledger.

Do not start QGIS, desktop, or web UI work until the official binary harness and project
workspace are stable.
