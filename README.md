# AERMODKit

AERMODKit is an independent, GIS-first Python toolkit for building, validating,
running, and analysing projects across the U.S. EPA AERMOD modelling ecosystem.

> **Current baseline:** EPA AERMOD v26135. EPA manuals, source code, release notes,
> and official test cases are the source of truth. Third-party projects are references
> only and are not treated as authoritative implementations.

## Current milestone

Version `0.1.0a2` provides:

- complete CO, SO, RE, ME, EV, and OU keyword registries for v26135;
- all v26135 MODELOPT tokens and all 13 source types;
- lossless reading and exact preserve-mode writing;
- deterministic canonical writing;
- GRIDCART/GRIDPOLR continuation validation;
- keyword, option, ordering, source, and cross-pathway diagnostics;
- a read-only semantic project view that always retains the original syntax tree.

```python
from aermodkit import (
    build_project_model,
    parse_aermod,
    validate_document,
    write_aermod,
)

text = open("aermod.inp", encoding="utf-8").read()
document = parse_aermod(text, version="26135")
issues = validate_document(document)
model = build_project_model(document)
clone = write_aermod(document, mode="preserve")
canonical = write_aermod(document, mode="canonical")
```

## Architecture rules

1. EPA executables remain the numerical truth source.
2. Every keyword and rule is versioned and evidence-backed.
3. Unknown input is never silently discarded.
4. The lossless AST is authoritative; semantic objects are projections.
5. GIS geometry is never reduced to a lossy first/last-point approximation by default.
6. The core package remains independent of GUI and web frameworks.
7. Each completed batch includes tests, a progress record, and a handover update.

## Development

```bash
python -m pip install -e ".[dev]"
pytest
```

See [`HANDOFF.md`](HANDOFF.md) and [`docs/progress/`](docs/progress/) for the
current implementation boundary and the next locked task.
