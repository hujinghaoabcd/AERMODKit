# AERMODKit Initial Architecture v0.1

- Date: 2026-07-29
- Status: initial architecture; expected to evolve
- Project: **AERMODKit**
- Python distribution/import name: `aermodkit`
- Planned applications: AERMODKit for QGIS, AERMODKit Studio, AERMODKit Web

## 1. Mission

AERMODKit will be an independent, GIS-first Python toolkit for configuring, validating, executing, and analysing projects across the U.S. EPA AERMOD modelling ecosystem. It is not a rewrite of the AERMOD numerical core, is not affiliated with EPA, and must not imply regulatory approval.

The package must eventually support shared use by:

- Python scripts and notebooks;
- a command-line interface;
- a QGIS plugin;
- a standalone desktop application;
- a browser-based GIS application and remote execution service.

The shared Python core must remain independent from every user-interface framework.

## 2. Authority and evidence hierarchy

Implementation decisions use this order of authority:

1. official EPA source code and executable behaviour;
2. official user, formulation, implementation, evaluation, release, errata, and technical-support documents;
3. official EPA test cases and published reference outputs;
4. independently verified AERMODKit behaviour;
5. commercial software workflow observations;
6. third-party open-source projects.

`pyaermod` and other projects are comparison references only. Their architecture, class hierarchy, tests, comments, and code must not be copied. A third-party package may be simplified, incomplete, version-mixed, or wrong even when it successfully produces an input file.

## 3. Non-negotiable principles

1. **Version separation:** rules for different AERMOD releases must not be silently blended.
2. **Traceability:** model-facing schema and validation rules should link to official evidence.
3. **Loss awareness:** opening an input file must not silently discard unsupported keywords, comments, ordering, includes, or development options.
4. **GIS as a first-class capability:** geometry, CRS, topology, layers, selection, and attribute workflows are not post-processing decorations.
5. **Deterministic validation:** model rules are enforced by code, not generated or guessed by an AI interface.
6. **External official executables:** Python orchestration is separated from EPA binaries and records executable provenance.
7. **Reproducibility:** each run preserves inputs, outputs, executable identity, environment, logs, and checksums.
8. **Official numeric regression:** completion requires comparison with official test outputs, not merely a zero process exit code.
9. **Durable handover:** every material work session updates current state, next steps, changelog, and a dated worklog.

## 4. Layered system architecture

```text
Official EPA manuals + source + releases + tests
                       |
              Versioned specification
                       |
 Domain model -- Runstream I/O -- GIS -- Validation
                       |
      Processor wrappers -- Execution -- Results
                       |
                Stable public API
          /              |               \
       CLI          QGIS/Desktop          Web
```

No application layer may implement separate copies of AERMOD rules. QGIS, desktop, and web clients call the same core services and consume the same diagnostics.

## 5. Proposed repository structure

```text
AERMODKit/
├── src/aermodkit/
│   ├── domain/             # semantic AERMOD concepts
│   ├── spec/               # versioned official capability/schema layer
│   ├── io/                 # runstream, project and result formats
│   ├── geo/                # GIS-native geometry and layer operations
│   ├── processors/         # AERMOD-family program wrappers
│   ├── engine/             # execution, jobs, logs and provenance
│   ├── workflow/           # pipelines, batches and scenarios
│   ├── validation/         # field, cross-field, geometry and parity rules
│   ├── results/            # structured concentration/deposition outputs
│   ├── viz/                # optional visualisation adapters
│   ├── reporting/          # reports and audit summaries
│   ├── plugins/            # controlled extension points
│   ├── compat/             # historical and third-party import compatibility
│   └── cli/                # thin CLI over the public API
├── apps/
│   ├── qgis/
│   ├── desktop/
│   └── web/
├── services/
│   ├── api/
│   ├── worker/
│   └── scheduler/
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── roundtrip/
│   ├── regulatory/
│   ├── property/
│   ├── e2e/
│   └── performance/
├── reference/
│   ├── epa/
│   ├── coverage/
│   ├── aermod-view/
│   └── github-projects/
├── docs/
│   ├── design/
│   ├── decisions/
│   ├── handover/
│   └── worklog/
├── examples/
├── tools/
└── packaging/
```

Directories are added only when implementation begins. Empty directory theatre is discouraged.

## 6. Domain layer

The semantic model is expected to cover:

```text
domain/
├── project.py
├── scenario.py
├── control.py
├── meteorology.py
├── terrain.py
├── building.py
├── chemistry.py
├── deposition.py
├── emissions.py
├── temporal_profiles.py
├── background.py
├── source_groups.py
├── outputs.py
├── events.py
├── sources/
│   ├── point.py
│   ├── volume.py
│   ├── area.py
│   ├── area_circle.py
│   ├── area_polygon.py
│   ├── line.py
│   ├── rline.py
│   ├── rline_ext.py
│   ├── buoyant_line.py
│   └── open_pit.py
└── receptors/
    ├── discrete.py
    ├── cartesian.py
    ├── polar.py
    ├── evaluation.py
    └── collection.py
```

This list is provisional until the official v26135 capability inventory is complete. It must not be reduced to whatever a third-party wrapper currently exposes.

## 7. Versioned specification layer

The specification layer prevents model-version rules from being scattered across Python classes.

```text
spec/
├── model_version.py
├── registry.py
├── loader.py
├── capability.py
├── keyword.py
├── constraint.py
├── compatibility.py
├── traceability.py
├── diff.py
└── versions/
    ├── v24142/
    └── v26135/
```

Each version bundle should eventually record:

- pathways and keywords;
- argument order and types;
- units and defaults;
- requirement, repeatability, and applicability rules;
- mutually exclusive and dependent options;
- source-type relationships;
- regulatory versus development status;
- introduction, modification, and removal version;
- official manual/page references;
- source file, routine, and parser-handler references;
- official test-case coverage.

Generated schemas may later be produced from reviewed source data, but generated output must be reproducible and reviewable.

## 8. Runstream input architecture

AERMODKit requires two related representations:

```text
original text
    -> loss-aware tokens and source locations
    -> syntax tree preserving comments/order/unknown content
    <-> semantic project objects for supported concepts
    -> controlled formatting and output
```

The syntax layer comes before broad semantic classes. An unsupported line must remain available for round-trip output and diagnostics rather than disappearing.

Proposed modules:

```text
io/runstream/
├── token.py
├── location.py
├── lexer.py
├── block.py
├── ast.py
├── parser.py
├── formatter.py
├── comments.py
├── include.py
├── unknown.py
├── semantic_mapper.py
└── roundtrip.py
```

Round-trip testing has two levels:

- **loss-aware round trip:** preserve meaningful syntax, unsupported records, and comments;
- **semantic round trip:** parse supported concepts, write them, and recover equivalent objects.

Byte-identical output is not required where AERMOD itself normalises whitespace, but changes must be intentional and documented.

## 9. GIS architecture

GIS is a shared core, not GUI-specific code.

```text
geo/
├── crs.py
├── transform.py
├── precision.py
├── geometry.py
├── topology.py
├── spatial_index.py
├── layers.py
├── fields.py
├── importers/
├── exporters/
├── sources/
├── roads/
├── receptors/
├── buildings/
├── terrain/
├── landuse/
└── contours/
```

Road handling must never default to replacing a curved polyline by a single line between its first and last vertices. Segment generation should support vertex, maximum-length, curvature, and topology-node strategies. Derived AERMOD segments retain lineage:

```text
original_feature_id
parent_source_id
segment_id
segment_order
original_geometry
aermod_geometry
split_method
```

The future QGIS plugin should expose normal GIS behaviour: layer tree, map editing, snapping, selection, attribute tables, field mapping, spatial filtering, style control, processing algorithms, and error-to-feature navigation.

## 10. Processor and execution architecture

Processor wrappers are planned for:

- AERMOD;
- AERMAP;
- AERMET;
- AERSURFACE;
- AERMINUTE;
- BPIP-PRIME;
- MMIF;
- AERSCREEN;
- AERPLOT where appropriate.

A wrapper separates configuration, input generation, execution, output parsing, and QA. The execution engine should support local processes first and later Docker/Podman, SSH, schedulers, and remote APIs.

Each run records at least:

- model/version reported by the executable;
- executable path and SHA256;
- operating system and architecture;
- compiler/build information when known;
- command and environment;
- start/end timestamps and state transitions;
- input/output checksums;
- stdout, stderr, and model messages;
- cancellation, timeout, and failure reason.

A process return code of zero is not sufficient. Output files and fatal model messages must also be checked.

## 11. Validation and diagnostics

Diagnostics are shared objects for Python, CLI, QGIS, desktop, and web clients. The initial `Diagnostic` type includes code, severity, message, processor, pathway, object identity, field, evidence references, geometry reference, suggested fix, and context.

Future validation layers include:

- scalar field rules;
- cross-field rules;
- pathway completeness;
- source and receptor constraints;
- CRS and geometry QA;
- meteorological coverage;
- terrain/building consistency;
- chemistry and deposition rules;
- output compatibility;
- version compatibility;
- native model preflight;
- official numeric parity.

A GIS client should be able to click a diagnostic and select the offending feature and field.

## 12. Result architecture

Outputs should be parsed into explicit result objects, not only plots. Planned views include:

- run metadata and QA;
- receptor concentrations and deposition;
- maxima and ranked values;
- source-group and event results;
- spatial and temporal queries;
- background combinations;
- scenario comparison, exceedance, and uncertainty summaries.

Adapters may expose pandas, GeoPandas, xarray, GeoPackage, Parquet, NetCDF, Zarr, GeoTIFF, GeoJSON, and KMZ when appropriate. Optional dependencies must not burden the minimal package.

## 13. Project persistence

A working project is expected to be a directory rather than a single JSON file:

```text
example.amkproj/
├── manifest.yaml
├── project.json or project.sqlite
├── spatial/project.gpkg
├── tables/*.parquet
├── arrays/*.zarr
├── assets/
├── inputs/
├── runs/<run_id>/
│   ├── run.yaml
│   ├── environment.yaml
│   ├── checksums.yaml
│   ├── inputs/
│   ├── outputs/
│   ├── logs/
│   └── provenance/
├── styles/
├── cache/
├── temp/
└── locks/
```

This format is not frozen. The design requirement is separation of small configuration, vector layers, large tables, multidimensional arrays, immutable run records, and disposable cache/temp data.

## 14. Testing strategy

Required test families:

1. unit tests;
2. parser/writer golden tests;
3. loss-aware and semantic round-trip tests;
4. property-based parser and model tests;
5. processor integration tests;
6. official EPA test-case execution;
7. receptor-by-receptor numeric regression;
8. cross-version compatibility tests;
9. GIS geometry and CRS QA;
10. performance tests for large source/receptor sets;
11. end-to-end CLI, QGIS, desktop, and web tests as applications appear.

The CI baseline is Linux, Windows, and macOS with supported Python versions. Real EPA executable jobs may use separate workflows because of runtime, download reliability, and distribution constraints.

## 15. Development phases

### Phase 0 — official specification foundation

- inventory official v26135 assets;
- build keyword, source, output, and test-case matrices;
- map parser and computation routines in the Fortran source;
- define evidence and coverage reporting;
- define loss-aware runstream contracts.

### Phase 1 — reliable minimum core

- lexer, tokens, blocks, AST, and writer;
- initial semantic model;
- structured validation;
- local runner and basic output parsing;
- official-case numeric regression.

### Phase 2 — complete AERMOD feature surface

- all official source types and pathways;
- variable emissions, groups, background, chemistry, deposition, events, MULTYEAR, and output forms;
- explicit unsupported-feature reporting until each item is implemented.

### Phase 3 — preprocessor ecosystem

AERMAP, AERMET, AERSURFACE, AERMINUTE, BPIP-PRIME, MMIF, AERSCREEN, and related support workflows.

### Phase 4 — GIS core and QGIS plugin

Build stable GeoDataFrame/GeoPackage workflows first, then expose them through QGIS Processing algorithms and editing panels.

### Phase 5 and later

Standalone desktop and web applications after the core and GIS workflows are stable enough that applications do not force duplicate model logic.

## 16. Frozen and provisional decisions

### Frozen for the current phase

- EPA evidence hierarchy;
- third-party clean-room policy;
- versioned specification requirement;
- loss-aware parsing principle;
- UI-independent core;
- GIS-first model;
- structured diagnostics;
- reproducible run records;
- official numeric regression requirement;
- mandatory handover records.

### Provisional

- final licence;
- exact project extension and storage engines;
- CLI framework;
- GUI framework;
- web technology stack;
- plugin API;
- whether applications remain in one repository;
- whether EPA executables can be redistributed or must be discovered/downloaded separately;
- final project and package name pending publication checks.

## 17. Immediate handover

The next implementation must **not** begin by creating source classes from memory or copying `pyaermod`. It must create the v26135 official capability inventory listed in `docs/handover/NEXT_STEPS.md`. Runstream syntax work begins only after official sample decks and parser behaviour have been indexed.
