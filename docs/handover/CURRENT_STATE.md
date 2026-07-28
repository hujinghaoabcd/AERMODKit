# Current State

- Updated: 2026-07-29
- Branch: `agent/bootstrap-project-foundation`
- Pull request: #1 (draft)
- Package version: `0.0.1.dev0`
- Development phase: Phase 0 official specification and parity baseline
- Repository visibility: public

## What exists

- a Python package using the `src/` layout;
- structured diagnostics and AERMOD release identifiers;
- a resource-backed v26135 metadata registry explicitly labelled incomplete;
- an official v26135 asset manifest with independent component versions;
- SHA256 and archive indexes for the official source, sample-run, and test-case ZIPs;
- the complete 29-unit official Fortran build order and supplied GNU/Intel build flags;
- 566 declaration-level Fortran program-unit records;
- exact pathway dispatchers and a source branch map for 120 primary runstream records;
- a broad evidence-ranked keyword/pathway inventory and 12 confirmed LOCATION source types;
- an official test-fixture registry for 53 current input decks, 80 observed pathway/keyword combinations, and 12 source types;
- an official regression baseline comparing a reproduced GNU build with EPA expected outputs;
- a reproducible regression-validation tool that isolates ordinary cases and preserves the PM10 MULTYEAR dependency chain;
- architecture, source-of-truth, clean-room, worklog, and handover records.

## Official asset state

- `aermod_source.zip`: 674,503 bytes; SHA256 `5092c1d68b77d9407c9f67d497b440a79d2ee746f9ed6515a63ad4a5b11cd8ed`;
- `AERMOD_Sample_Run.zip`: 95,949,615 bytes; SHA256 `3ee2180fd0ad9c954350bbbe3ca3567ce02df91a2869cec5f6c45178bff32da0`;
- `aermod_test_cases.zip`: 488,669,681 bytes; SHA256 `fc5ad71de5ba64a50ed72d4d19c45b32ad14447353b1216c3d1f420ce84beff8`;
- current test configuration: `aermet26135_aermod26135`;
- current regression fixture snapshot: 273 files, 72,473,324 bytes;
- large EPA ZIPs are not committed to Git; metadata, hashes, indexes, and bounded artifacts are retained.

## Build and regression state

The unmodified EPA source was compiled with GNU Fortran 14.2.0 using the EPA-supplied GNU flags and exact unit order:

```text
compile: -fbounds-check -Wuninitialized -O2 -static
link:    -static -O2
```

Results:

- all 29 Fortran source units compile and link;
- the generated executable is a statically linked x86-64 ELF;
- executable SHA256: `e8313b430047472ccf9a6cbd49b573c8e638aafaca25805e42c0f9c7a14341a5`;
- all 53 official input decks return zero and contain `AERMOD Finishes Successfully`;
- the PM10 1986–1990 decks are validated as an ordered MULTYEAR chain;
- all 189 official expected output filenames are produced by at least one corresponding run;
- main-output classifications: 27 canonical exact, 10 representation/tie equivalent, 9 minor floating-point drift, 6 moderate floating-point drift, and 1 compiler-sensitive investigation.

The only materially flagged case is `capped`. It completes successfully, but the extracted result values reach a maximum relative difference of approximately 5.2613% under GNU Fortran 14.2 and the EPA GNU flags. This is an open compiler/optimization parity investigation, not a model-run failure. `capped_nostd` is canonical exact.

## CI state

The latest ordinary GitHub Actions matrix is green across:

- Ubuntu, Windows, and macOS;
- Python 3.11, 3.12, and 3.13;
- Ruff, strict mypy, and pytest with coverage.

The EPA asset and current-fixture snapshot workflows have completed successfully and are now manual-only (`workflow_dispatch`) to avoid redownloading large official archives on every PR synchronization. Heavy numerical regression is not yet a permanent PR check.

## What does not exist yet

- no complete argument/type/unit/default/range/dependency/error schema for every keyword;
- no completed official-versus-PyAERMOD capability audit;
- no AERMOD input lexer, parser, AST, writer, or semantic project model;
- no production runner abstraction;
- no production output parser;
- no GIS code;
- no claim of complete AERMOD support or universal compiler parity;
- no final open-source licence decision.

## Non-negotiable constraints

1. Official EPA material is authoritative.
2. Third-party projects are comparison references only.
3. Unsupported official content must not be silently discarded.
4. EPA numerical source is not modified merely to force expected-output agreement.
5. Every material session ends with updated handover and worklog records.
6. CI and parity failures must be traced to concrete evidence before behavior changes.
7. Heavy regression tolerances must be documented by output family and compiler/platform.
