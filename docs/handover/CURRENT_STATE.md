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
- explicit status classifications for all 40 source-recognized MODELOPT tokens.

## Evidence boundary

Complete CO specification means exact record-level syntax/evidence coverage. It does not mean the production parser, AST, writer, runner, output parser, GIS layer, or all regulatory workflows are implemented. Guide/source discrepancies are preserved for focused executable probes.

## Existing parity baseline

- all official assets hashed and indexed;
- official 29-unit source build order recorded;
- GNU Fortran 14.2 build completes all 53 official decks;
- official executable parity tier separated from source-build tiers;
- ordinary CI was green before this completion commit.
