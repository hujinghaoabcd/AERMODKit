# AERMOD v26135 official behavior probes — batch 3

## Scope

This batch resolves three parser-shaping questions before production loss-aware syntax begins:

- the ALPHA/DFAULT dependency matrix for `GDSEASON`, `GASDEPDF`, `GDLANUSE`, `GASDEPVD`, `LOW_WIND`, `AWMADWNW`, `ORD_DWNW`, and aircraft processing;
- repeated and extra-field `ARCFTOPT` behavior, separated from actual `ARCFTSRC` dependencies;
- the two executable `MAXDCONT` signatures, with and without an explicit trailing file unit.

The harness is evidence infrastructure only. It is not the future AERMODKit application runner.

## Reviewed official evidence

- workflow run: `30461120811`;
- reviewed head: `7433a58adb1c2cd7d8304d2af76bf30919345fb6`;
- artifact ID: `8727721661`;
- artifact digest: `sha256:c301bfc8ec367569da40923e214431a34bd7266999ba028d3a7cba9e0293e3f0`;
- artifact size: `284,393,626` bytes;
- official executable SHA-256: `599b491b021c7ec254ba3a1062386f287e56e54a0d3bb9b67cfa72275d6916da`;
- official source archive SHA-256: `5092c1d68b77d9407c9f67d497b440a79d2ee746f9ed6515a63ad4a5b11cd8ed`;
- cases: 35;
- accepted: 16;
- rejected: 19;
- indeterminate: 0;
- expectations met: 35/35.

Compact evidence is retained in `reference/probes/v26135/batch3/result.json`; per-case deck/output hashes are in `reference/probes/v26135/batch3/case-evidence.csv`.

## ALPHA/DFAULT matrix

Seven dedicated ALPHA controls completed:

- `GDSEASON`;
- `GASDEPDF`;
- `GDLANUSE`;
- `GASDEPVD`;
- `LOW_WIND`;
- `AWMADWNW`;
- `ORD_DWNW`.

The retained source and executable evidence establish:

- `GDSEASON`, `GASDEPDF`, `GDLANUSE`, and `GASDEPVD` use `E196` for DFAULT conflicts and `E198` when ALPHA is absent;
- `LOW_WIND` has an immediate `E133` branch without ALPHA; the broad no-ALPHA executable fixture also contains RLINEXT, so target-specific attribution relies on the exact retained source branch;
- DFAULT plus ALPHA produces target diagnostics `E133`, `E122`, and `E123` for `LOW_WIND`, `AWMADWNW`, and `ORD_DWNW` respectively;
- complete aircraft-source processing produces `E198` without ALPHA and `E198` plus `E204` under DFAULT plus ALPHA.

The matrix records actual v26135 diagnostics. It does not reinterpret development options as ordinary stable syntax.

## ARCFTOPT and aircraft dependencies

The following forms completed:

- complete aircraft control;
- `ARCFTOPT` with no payload;
- repeated `ARCFTOPT` with the same airport ID;
- repeated `ARCFTOPT` with different airport IDs;
- `ARCFTOPT` with more than one payload field.

The official dispatcher assigns `AFTID(1)` only when `IFC == 3`. Therefore:

- a one-payload repeated card is accepted and the later assignment wins in internal state;
- a no-payload card is accepted but does not assign `AFTID(1)`;
- a card with extra payload fields is accepted and preserved but does not assign `AFTID(1)`.

Last-assignment-wins is a source-state conclusion because the ordinary output does not expose `AFTID(1)` directly.

Aircraft-source dependency cases establish:

- no ALPHA: `E198`;
- DFAULT plus ALPHA: `E198` and `E204`;
- `ARCFTOPT` without a matching `ARCFTSRC`: `E822` in the retained fixture;
- `ARCFTSRC` without `ARCFTOPT`: `E821`;
- `ARCFTSRC` without preceding `HOUREMIS`: `E823`.

The positive fixture uses `POLLUTID OTHER` and a deterministic six-hour aircraft hourly-emissions file to avoid unrelated annual criteria-pollutant completeness checks.

## MAXDCONT forms

All four forms completed and generated the requested output file:

1. primary rank plus secondary rank, dynamic file unit;
2. primary rank plus secondary rank, explicit trailing file unit;
3. primary rank plus `THRESH` and threshold, dynamic file unit;
4. primary rank plus `THRESH` and threshold, explicit trailing file unit.

The THRESH cases emitted `W273` and `W415` in the selected annual NO2 context but were not rejected. Short output filenames were used after exploratory `E500` file-open failures; this is fixture hygiene and not a promoted general filename-length rule.

## Cross-platform evidence integrity

`case-evidence.csv` is byte-hashed. A Windows checkout initially converted LF to CRLF and caused a test-only SHA mismatch while all official executable workflows passed. `.gitattributes` now pins retained probe evidence files to LF without imposing a global newline policy. Future syntax fixtures remain free to preserve intentional CRLF inputs.

## Gate update

The normalized inventory remains 19 questions:

- executed with retained official evidence: 10;
- source-resolved: 1;
- official-executable pending: 8.

The record-set gate remains 7/7 dispatchers and 138/138 primary records. The behavior gate and production syntax gate remain closed.

## Interpretation boundary

The official executable results are limited to the exact materialized decks and support files retained by the workflow. Broader statements are made only where the exact official source branch is also retained. No production parser, CST, format-preserving writer, semantic model, runner, output parser, or GIS layer is introduced by this batch.
