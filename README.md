# AERMODKit

AERMODKit is an independent, GIS-first Python toolkit for building, validating, running, and analysing projects across the U.S. EPA AERMOD modelling ecosystem.

> **Early development:** the U.S. EPA manuals, source code, release notes, and official test cases are the source of truth. Third-party projects, including `pyaermod`, are comparison references only.

## Initial scope

The project is being built in layers:

1. versioned official specification and traceability;
2. loss-aware AERMOD input/output handling;
3. deterministic validation and execution;
4. GIS-native source, receptor, terrain, building, and result workflows;
5. shared APIs for Python, CLI, QGIS, desktop, and web applications.

The first implementation milestone establishes a small tested core for version metadata and structured diagnostics. It intentionally does **not** claim full AERMOD feature coverage yet.

## Current status

Read these files before changing the project:

- [`docs/handover/CURRENT_STATE.md`](docs/handover/CURRENT_STATE.md)
- [`docs/handover/NEXT_STEPS.md`](docs/handover/NEXT_STEPS.md)
- [`docs/design/INITIAL_ARCHITECTURE_v0.1.md`](docs/design/INITIAL_ARCHITECTURE_v0.1.md)
- [`docs/decisions/0001-official-source-of-truth.md`](docs/decisions/0001-official-source-of-truth.md)
- [`docs/decisions/0002-third-party-clean-room-policy.md`](docs/decisions/0002-third-party-clean-room-policy.md)

## Development

```bash
python -m pip install -e ".[dev]"
pytest
ruff check .
mypy src
```

## Independence notice

AERMODKit is not affiliated with or endorsed by the U.S. EPA. It does not replace official executables, documentation, regulatory guidance, or professional judgement.
