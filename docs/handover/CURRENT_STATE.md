# Current State

- Updated: 2026-07-29
- Branch: `agent/bootstrap-project-foundation`
- Pull request: #1 (draft)
- Package version: `0.0.1.dev0`
- Development phase: Phase 0 official specification and compiler-tier parity baseline
- Repository visibility: public

## What exists

- a Python package using the `src/` layout;
- structured diagnostics and AERMOD release identifiers;
- a resource-backed v26135 metadata registry explicitly labelled incomplete;
- an official v26135 asset manifest with independent component versions;
- SHA256 and archive indexes for the official source, executable, sample-run, and test-case assets;
- the complete 29-unit official Fortran build order and supplied GNU/Intel build flags;
- 566 declaration-level Fortran program-unit records;
- exact pathway dispatchers and a source branch map for 120 primary runstream records;
- a broad evidence-ranked keyword/pathway inventory and 12 confirmed LOCATION source types;
- an official test-fixture registry for 53 current input decks, 80 observed pathway/keyword combinations, and 12 source types;
- a 53-deck GNU source-build execution and output-coverage baseline;
- an EPA official Windows executable probe for `capped` and `capped_nostd`;
- reproducible tools for isolated regression and focused executable parity analysis;
- architecture, source-of-truth, clean-room, worklog, and handover records.

## Official asset state

- `aermod_source.zip`: 674,503 bytes; SHA256 `5092c1d68b77d9407c9f67d497b440a79d2ee746f9ed6515a63ad4a5b11cd8ed`;
- `aermod_exe.zip`: SHA256 `0ccf49702109637e665c8567891e365b4585a62a560faae35ce0194048683a24`;
- official `aermod.exe`: 3,940,864 bytes; SHA256 `599b491b021c7ec254ba3a1062386f287e56e54a0d3bb9b67cfa72275d6916da`;
- `AERMOD_Sample_Run.zip`: 95,949,615 bytes; SHA256 `3ee2180fd0ad9c954350bbbe3ca3567ce02df91a2869cec5f6c45178bff32da0`;
- `aermod_test_cases.zip`: 488,669,681 bytes; SHA256 `fc5ad71de5ba64a50ed72d4d19c45b32ad14447353b1216c3d1f420ce84beff8`;
- current test configuration: `aermet26135_aermod26135`;
- current regression fixture snapshot: 273 files, 72,473,324 bytes;
- large EPA ZIPs and executables are not committed to Git; metadata, hashes, indexes, and bounded evidence artifacts are retained.

## Build and parity state

The unmodified EPA source was compiled with GNU Fortran 14.2.0 using the EPA-supplied GNU flags and exact unit order:

```text
compile: -fbounds-check -Wuninitialized -O2 -static
link:    -static -O2
```

GNU results:

- all 29 Fortran source units compile and link;
- executable SHA256: `e8313b430047472ccf9a6cbd49b573c8e638aafaca25805e42c0f9c7a14341a5`;
- all 53 official input decks return zero and contain `AERMOD Finishes Successfully`;
- the PM10 1986–1990 decks are validated as an ordered MULTYEAR chain;
- all 189 official expected output filenames are produced by a corresponding run;
- main-output classifications: 27 canonical exact, 10 representation/tie equivalent, 9 minor floating-point drift, 6 moderate floating-point drift, and 1 compiler-specific localized difference.

Official executable result:

- the EPA executable is a PE32+ x86-64 binary containing Intel Fortran runtime evidence;
- `capped` and `capped_nostd` both reproduce official expected outputs with zero canonical or numerical differences;
- the official test fixture is internally consistent;
- the GNU `capped` difference is localized primarily to `STACK1C` second-highest 1-hour and 3-hour tables, not the overall period-high result;
- recompiling `prime.f`, `calc1.f`, `calc2.f`, `prise.f`, or `sigmas.f` individually at `-O0` did not change that result.

## Parity policy

1. The EPA-distributed executable and expected outputs define exact official release-fixture parity.
2. Reproduced source builds use a separate compiler/platform evidence tier.
3. Exact cross-compiler text/numeric parity is not assumed.
4. Tolerances must be explicit by compiler, platform, case, output family, and intended use.
5. EPA numerical source is not modified merely to force agreement.

## CI state

The latest ordinary GitHub Actions matrix remains green across Ubuntu, Windows, and macOS with Python 3.11, 3.12, and 3.13 for Ruff, strict mypy, and pytest with coverage.

EPA asset, fixture, and official-executable evidence workflows are manual-only (`workflow_dispatch`) after their first successful evidence runs.

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
