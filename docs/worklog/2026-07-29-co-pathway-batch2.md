# Worklog: CO pathway exact specification batch 2

- Date: 2026-07-29
- Branch: `agent/bootstrap-project-foundation`
- Pull request: #1

## Objective

Extend the source-verified CO specification without prematurely implementing parser classes. The batch covers a coherent set of decay, receptor/urban, static ozone and NO2-ratio controls.

## Records completed

`HALFLIFE`, `DCAYCOEF`, `FLAGPOLE`, `URBANOPT`, `O3SECTOR`, `OZONEVAL`, `OZONEFIL`, `NO2EQUIL`, `NO2STACK`, `ARMRATIO`.

## Evidence processed

- current `coset.f`, plus `setup.f`, `calc2.f` and `aermod.f` supporting behavior;
- current EPA User's Guide sections 3.2.5, 3.2.8, 3.2.10 and 3.2.11;
- all 53 current official input decks;
- existing official-executable/source-build parity policy.

## Engineering changes

- aggregate batch 2 now composes batch 1 and batch 2 fragments;
- fragment validation accepts positive fragment batches no newer than the aggregate;
- three new machine-readable fragments and structural tests were added;
- evidence and promotion tables were updated;
- documentation now records source/manual discrepancies instead of flattening them;
- temporary connector staging files were removed from the final repository tree.

## Validation

- local reconstructed package: 13 tests passed and all 24 record keywords were unique;
- GitHub Actions run `30417130492`: success;
- Ubuntu, Windows and macOS with Python 3.11, 3.12 and 3.13 all passed Ruff, strict mypy and pytest.

## Deferred by design

`O3VALUES`, `OZONUNIT` and the NOX background family were deferred because their temporal flags, vector sizes, sector fallback and conflict rules need a dedicated batch.

## Next work

Implement CO batch 3 for temporal ozone and ambient NOx controls, then deposition, low-wind/direction-window and aircraft controls. Add focused executable probes for uncovered edge behavior.
