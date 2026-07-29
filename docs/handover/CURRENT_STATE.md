# Current State

- Updated: 2026-07-29
- Branch: `agent/bootstrap-project-foundation`
- Pull request: #1 (draft, open, not merged)
- Package version: `0.0.1.dev0`
- Development phase: Phase 0 source-verified specification
- Repository visibility: public

## Specification state

- The versioned pathway loader composes immutable fragments from multiple completed batches.
- CO aggregate batch: **2**.
- Source-verified CO records: **24**.
- Batch 1: 14 framing/control/restart/debug records.
- Batch 2: 10 decay, receptor/urban, static ozone and NO2-ratio records.
- Remaining CO records and every SO/RE/ME/EV/OU record are not yet complete exact specifications.

## Batch 2 records

`HALFLIFE`, `DCAYCOEF`, `FLAGPOLE`, `URBANOPT`, `O3SECTOR`, `OZONEVAL`, `OZONEFIL`, `NO2EQUIL`, `NO2STACK`, `ARMRATIO`.

## Important findings

1. `EDECAY` does not explicitly reject zero/negative values; source behavior is retained and semantic-policy diagnostics must remain separate.
2. `URBANOPT` supports single and multiple urban-area forms; non-default roughness status is mode-dependent.
3. `OZONEFIL` manual repeatability wording and source sector-indexed handling differ; both are recorded.
4. Same-sector duplicate `OZONEVAL/OZONEFIL` behavior still needs official-executable probes.
5. `NO2STACK` has no 0.1 default; a sentinel is initialized until CO/SO ratio input is supplied.
6. `ARMRATIO` does not explicitly reject trailing extra fields; the loss-aware syntax layer must preserve them.

## Existing official baseline

- Official source/executable/sample/test archives are hashed and indexed.
- GNU Fortran 14.2 source build completes 53/53 official decks and produces all 189 expected filenames.
- EPA's official executable exactly reproduces focused `capped` expected outputs.
- Heavy asset, fixture and executable workflows remain manual-only.

## CI

Batch 2 must not be considered finished until Ruff, strict mypy and pytest pass on Ubuntu, Windows and macOS with Python 3.11, 3.12 and 3.13.

## Non-negotiable constraints

- Official EPA evidence is authoritative.
- Source recognition does not imply regulatory approval.
- Unknown, extra, future and development syntax must be preserved.
- Do not modify EPA numerical source merely to force parity.
- Do not begin production parser work before specification and preservation acceptance criteria are met.
