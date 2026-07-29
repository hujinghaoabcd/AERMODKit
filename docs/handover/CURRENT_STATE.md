# Current State

- Updated: 2026-07-29
- Branch: `agent/bootstrap-project-foundation`
- Pull request: #1 (draft, unmerged)
- Package version: `0.0.1.dev0`
- Development phase: Phase 0 complete CO specification, remaining pathway specification pending

## Complete CO specification

All 39 primary records dispatched by EPA AERMOD v26135 `COCARD` are bundled in a versioned, source-verified specification. The aggregate contains ten fragments and no duplicate or missing CO primary keyword.

The final combined stage added:

- `O3VALUES`, `OZONUNIT`;
- `NOXSECTR`, `NOXVALUE`, `NOX_VALS`, `NOX_UNIT`, `NOX_FILE`;
- `GDSEASON`, `GASDEPDF`, `GDLANUSE`, `GASDEPVD`;
- `LOW_WIND`, `AWMADWNW`, `ORD_DWNW`;
- `ARCFTOPT`;
- explicit current-status classifications for all 40 source-recognized `MODELOPT` tokens.

The source-dispatch exact-set check reports:

```text
source COCARD primary records: 39
bundled CO records:           39
missing records:              0
extra records:                0
```

## Validation state

The verified reconstruction workflow checked the compressed payload SHA256, every target-file SHA256, package installation, Ruff, strict mypy, and pytest with coverage. GitHub Actions run `30421642505` completed successfully across Ubuntu, Windows, and macOS with Python 3.11, 3.12, and 3.13; all nine matrix jobs and the final apply job passed.

The ordinary CI workflow has been restored after the one-time verified reconstruction. Temporary payload chunks and the one-time apply workflow are removed from the final tree.

## Evidence boundary

Complete CO specification means exact record-level syntax/evidence coverage. It does not mean the production parser, AST, writer, runner, output parser, GIS layer, or all regulatory workflows are implemented. Guide/source discrepancies are preserved for focused executable probes rather than normalized without evidence.

## Existing parity baseline

- all official assets hashed and indexed;
- official 29-unit source build order recorded;
- GNU Fortran 14.2 build completes all 53 official decks;
- official executable parity tier separated from reproduced source-build tiers;
- CO source/specification coverage is now exact at the primary-record dispatch level.
