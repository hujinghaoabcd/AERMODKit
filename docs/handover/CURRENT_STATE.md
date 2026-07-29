# Current State

- Updated: 2026-07-29
- Branch: `agent/bootstrap-project-foundation`
- Pull request: #1 (draft)
- Package version: `0.0.1.dev0`
- Development phase: Phase 0 source-verified specification and compiler-tier parity baseline
- Repository visibility: public

## What exists

- a Python package using the `src/` layout;
- structured diagnostics and AERMOD release identifiers;
- a versioned v26135 metadata registry now labelled **partial source-verified**, not metadata-only;
- a typed pathway-specification loader with structural validation and loud failure for unavailable pathways;
- CO pathway batch 1 covering 14 framing and foundational control records;
- four bundled CO record fragments plus a stable index, allowing later batches to extend the pathway without one monolithic file;
- 40 current source-recognized `MODELOPT` tokens and their high-level conflicts/default behavior;
- 23 current `DEBUGOPT` tokens, v26135 card repeatability, individual-option nonrepeatability, case-preserved filenames, and observed default filenames;
- source/fixture evidence for required fields, defaults, diagnostics, handler ranges, and current official examples;
- SHA256 and archive indexes for the official source, executable, sample-run, and test-case assets;
- the complete 29-unit official Fortran build order and supplied GNU/Intel build flags;
- 566 declaration-level Fortran program-unit records;
- exact pathway dispatchers and a source branch map for 120 primary runstream records;
- an official test-fixture registry for 53 current input decks;
- a 53-deck GNU source-build execution and output-coverage baseline;
- an EPA official Windows executable probe for `capped` and `capped_nostd`;
- architecture, source-of-truth, clean-room, worklog, and handover records.

## CO batch 1 scope

Completed records:

```text
STARTING  FINISHED  TITLEONE  TITLETWO  MODELOPT  AVERTIME  POLLUTID
RUNORNOT  ERRORFIL  EVENTFIL  SAVEFILE  INITFILE  MULTYEAR  DEBUGOPT
```

The schema explicitly records that:

- pathway continuation records commonly omit the `CO` prefix;
- extra/unknown syntax must be retained by the future syntax layer even when the official handler ignores it;
- `SAVEFILE` and `INITFILE` conflict with `MULTYEAR`;
- PM10 MULTYEAR fixtures are an ordered state chain;
- `DEBUGOPT` records are repeatable in v26135 while each individual option is not;
- source recognition does not by itself establish regulatory status;
- the `EVENTFIL` invalid-detail comment/implementation discrepancy remains visible for behavioral testing.

## Validation state

- a temporary reconstructed package loaded all four schema fragments successfully;
- eight local pytest tests passed for metadata, record order, required records, option catalogs, conflicts, and missing-pathway behavior;
- repository CI remains the final Ruff, strict-mypy, and cross-platform pytest authority for the committed implementation.

## Official asset and parity state

- official source ZIP SHA256: `5092c1d68b77d9407c9f67d497b440a79d2ee746f9ed6515a63ad4a5b11cd8ed`;
- official executable ZIP SHA256: `0ccf49702109637e665c8567891e365b4585a62a560faae35ce0194048683a24`;
- official `aermod.exe` SHA256: `599b491b021c7ec254ba3a1062386f287e56e54a0d3bb9b67cfa72275d6916da`;
- sample ZIP SHA256: `3ee2180fd0ad9c954350bbbe3ca3567ce02df91a2869cec5f6c45178bff32da0`;
- test ZIP SHA256: `fc5ad71de5ba64a50ed72d4d19c45b32ad14447353b1216c3d1f420ce84beff8`;
- GNU Fortran 14.2 source build completes all 53 current official decks;
- the EPA executable exactly reproduces the probed `capped` and `capped_nostd` expected outputs;
- cross-compiler parity remains a separate evidence tier with explicit tolerances.

## What does not exist yet

- no exact schema for the remaining CO records;
- no exact schema for SO, RE, ME, EV, and OU pathways;
- no completed official-versus-PyAERMOD capability audit;
- no AERMOD input lexer, parser, AST, writer, or semantic project model;
- no production runner or output parser;
- no GIS code;
- no claim of complete AERMOD support or universal compiler parity;
- no final open-source licence decision.

## Non-negotiable constraints

1. Official EPA material is authoritative.
2. Third-party projects are comparison references only.
3. Unsupported or future official syntax must not be silently discarded.
4. EPA numerical source is not modified merely to force expected-output agreement.
5. Source-recognized options are not automatically described as regulatory.
6. Every material session ends with updated handover and worklog records.
7. CI and parity failures must be traced to concrete evidence before behavior changes.
