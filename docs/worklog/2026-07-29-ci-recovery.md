# Worklog: GitHub Actions recovery

- Date: 2026-07-29
- Branch: `agent/bootstrap-project-foundation`
- Pull request: #1
- Successful run: `30389503437`

## Goal

Determine why every GitHub Actions matrix job failed without steps, restore actionable CI, fix all reported code-quality failures, and leave a durable handover record.

## Investigation

1. The repository was initially private.
2. Nine matrix jobs were created, but every job had an empty step list and no retrievable log blob.
3. After the repository was made public and failed jobs were rerun, GitHub-hosted runners started normally.
4. This strongly indicates that the original failure was caused by private-repository Actions usage, billing, or policy constraints, but the exact GitHub billing-side message was not captured.
5. Once runners started, two concrete code issues became visible.

## Fixes

### Ruff

- Rule: `UP035`
- File: `src/aermodkit/diagnostics.py`
- Change: import `Mapping` from `collections.abc` instead of `typing`.

### strict mypy

- File: `src/aermodkit/spec/model_version.py`
- Error: the type checker did not narrow `str | ModelVersion` after `isinstance(value, cls)`.
- Change: use an explicit `isinstance(value, ModelVersion)` check before constructing from the remaining string value.

A transient indentation error was introduced while replacing `model_version.py`; it was immediately detected by remote inspection and corrected before the successful CI run.

## Final validation

GitHub Actions run `30389503437` passed all nine combinations:

| Operating system | Python 3.11 | Python 3.12 | Python 3.13 |
|---|---|---|---|
| Ubuntu | passed | passed | passed |
| Windows | passed | passed | passed |
| macOS | passed | passed | passed |

Every job passed:

- editable installation;
- Ruff;
- strict mypy;
- pytest with coverage.

## Remaining maintenance warning

GitHub emitted Node runtime deprecation warnings for `actions/checkout@v4` and `actions/setup-python@v5`. These warnings did not cause failure. Action-version maintenance should be handled separately after checking the current official action releases.

## Next owner instructions

Do not revisit the original zero-step failure unless it recurs. CI is now green. Continue with the source-verified v26135 specification tasks in `docs/handover/NEXT_STEPS.md`, and keep the full cross-platform matrix green.
