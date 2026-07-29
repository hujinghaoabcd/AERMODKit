# Contributing

## Before changing code

Read `docs/handover/CURRENT_STATE.md`, `docs/handover/NEXT_STEPS.md`, and the relevant architecture decision records.

## Evidence rule

No AERMOD capability, default, restriction, or regulatory behaviour may be added solely because a third-party package implements it. Every model-facing rule must be traceable to official EPA documentation, source code, release material, or test behaviour.

## Required session close-out

Every material work session must update:

1. `docs/handover/CURRENT_STATE.md`;
2. `docs/handover/NEXT_STEPS.md`;
3. a dated file under `docs/worklog/`;
4. `CHANGELOG.md` when user-visible or architectural behaviour changes.

The worklog must state what changed, why, validation performed, unresolved risks, and the exact next task.

## Quality checks

```bash
ruff check .
mypy src
pytest
```
