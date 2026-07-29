# Roadmap

The roadmap is capability-driven. Dates are intentionally not promised before the official specification inventory is complete.

## Phase 0 — official specification foundation

- inventory AERMOD v26135 manuals, source files, release notes, errata, and official tests;
- build a keyword/pathway/source/output capability matrix;
- link each implemented rule to official documentation and, where relevant, Fortran routines;
- define loss-aware runstream parsing and project persistence contracts.

## Phase 1 — reliable minimum core

- loss-aware runstream lexer, parser, AST, and formatter;
- semantic project model for initial pathways;
- deterministic validation and diagnostics;
- local executable discovery and controlled runs;
- basic output parsing;
- EPA official-case numeric regression.

## Later phases

- complete AERMOD feature surface;
- AERMAP, AERMET, AERSURFACE, AERMINUTE, BPIP-PRIME, MMIF, and AERSCREEN;
- GIS-native workflows and QGIS plugin;
- desktop application;
- web platform and remote execution.
