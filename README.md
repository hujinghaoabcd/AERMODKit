# AERMODKit

AERMODKit is an independent, GIS-first Python toolkit for building, validating,
running, and analysing projects across the U.S. EPA AERMOD modelling ecosystem.

> **Current baseline:** EPA AERMOD v26135. EPA manuals, source code, release notes,
> and official test cases are the source of truth. Third-party projects are references
> only and are not treated as authoritative implementations.

## Project purpose

AERMODKit does **not** replace the EPA Fortran numerical core. It builds a stable,
version-aware layer around the official programs:

- lossless reading and writing of AERMOD runstreams;
- machine-readable, versioned keyword and compatibility schemas;
- structured diagnostics tied to official evidence;
- GIS-first source, receptor, terrain, and result workflows;
- reproducible workspaces, execution ledgers, and official-binary regression tests;
- one UI-independent core for Python, CLI, QGIS, desktop, and web adapters.

## Current milestone: 0.1 schema and syntax core

The first implemented unit provides:

- an EPA v26135 registry for the initial CO/SO keyword set;
- all 36 MODELOPT tokens documented by the v26135 Quick Reference, including
  `BAREDGE` described in the option details;
- all 13 source types, including `POINTCAP`, `POINTHOR`, `RLINEXT`, and `SWPOINT`;
- schema-driven `DFAULT`/`ALPHA`/chemistry compatibility checks;
- a lossless AST that retains comments, spacing, quoted filenames, and unknown keywords;
- `preserve` and deterministic `canonical` writer modes.

```python
from aermodkit import parse_aermod, validate_document, write_aermod

text = open("aermod.inp", encoding="utf-8").read()
document = parse_aermod(text, version="26135")
issues = validate_document(document)
clone = write_aermod(document, mode="preserve")
canonical = write_aermod(document, mode="canonical")
```

## Non-negotiable engineering rules

1. EPA executables remain the numerical truth source.
2. Every keyword and rule is versioned and evidence-backed.
3. Unknown input is never silently discarded.
4. GIS geometry is never reduced to a lossy first/last-point approximation by default.
5. The core package remains independent of GUI and web frameworks.
6. Each completed batch includes tests, a progress record, and a handover update.

## Development

```bash
python -m pip install -e ".[dev]"
pytest
```

See [`HANDOFF.md`](HANDOFF.md) and [`docs/progress/`](docs/progress/) for the
current implementation boundary and the next locked task.
