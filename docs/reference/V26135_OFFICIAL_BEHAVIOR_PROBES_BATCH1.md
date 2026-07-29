# AERMOD v26135 official behavior probes — batch 1

## Purpose

This batch resolves parser-shaping source/manual ambiguities with the EPA-distributed AERMOD
v26135 Windows executable. It is an evidence exercise before loss-aware syntax implementation,
not an application runner.

## Official assets and workflow

- workflow run: `30447131971`;
- reviewed head: `1cd8e13dc2af2d0cc9fb88255ad7e96c190fade6`;
- artifact ID: `8721942233`;
- artifact digest: `sha256:4cfa463e9d2eb8f56e5d31d4df750c53ea4cadaa2d22b0bdf28a209a34f171d1`;
- official executable size: `3,940,864` bytes;
- official executable SHA-256: `599b491b021c7ec254ba3a1062386f287e56e54a0d3bb9b67cfa72275d6916da`;
- official source archive size: `674,503` bytes;
- official source archive SHA-256: `5092c1d68b77d9407c9f67d497b440a79d2ee746f9ed6515a63ad4a5b11cd8ed`.

The executable hash exactly matches the previously retained v26135 official-binary evidence.

## Method

1. Reuse retained official EPA fixture decks and meteorology.
2. Materialize deterministic mutations from `reference/probes/v26135/batch1/manifest.json`.
3. Execute every case in a separate workspace.
4. Require one unchanged official control to complete successfully.
5. Classify targeted forms from official completion markers and E/W/I diagnostics, not return code alone.
6. Retain input, output, diagnostic and source-snippet hashes in `result.json`.
7. Use distinct-sector positive controls to isolate supported sector repetition from same-sector duplicates.

## Results

| Case | Result | Key evidence |
|---|---|---|
| official Test3 RLINEXT/RBARRIER control | accepted | successful completion |
| SWPOINT, six parameters, ALPHA | accepted | successful completion; no fatal setup diagnostic |
| SWPOINT, same form, no ALPHA | rejected | `SO E198`, `SRCSIZ` |
| VBARRIER, one barrier, valid values | accepted | successful completion |
| VBARRIER, two barriers, opposite DCL signs, valid values | accepted | successful completion |
| OZONEFIL, two distinct sectors and files | accepted | confirms sector-indexed repetition |
| OZONEFIL, two different files in one sector | rejected | `CO E501`, `O3FILE` |
| NOX_FILE, two distinct sectors and files | accepted | confirms sector-indexed repetition |
| NOX_FILE, two different files in one sector | rejected | `CO E501`, `NOXFILE` |

Totals: 9 cases, 6 accepted, 3 rejected, 0 indeterminate.

## Specification consequences

### SWPOINT

The official executable accepts the source-recognized six-parameter `SRCPARAM` form when
`MODELOPT ALPHA` is active. The same exact source form without ALPHA is rejected by `SO E198`.
A future validator may therefore enforce the ALPHA dependency, while the loss-aware CST must still
preserve invalid input exactly.

### VBARRIER

Both executable field counts are confirmed for an `ALPHA` + `FLAT` `RLINEXT` source:

- one barrier: source ID plus five numeric fields;
- two barriers: source ID plus ten numeric fields.

The successful values were inside source-enforced ranges. Boundary inclusivity and same-side
barrier selection warning `W375` remain a separate pending probe, `SO-VBARRIER-RANGE-01`.

### OZONEFIL

The source/manual discrepancy is resolved more precisely than a single repeatable flag:

- repeated records are accepted across distinct `O3SECTOR` sectors;
- a second file assignment to the same sector is rejected with `E501`;
- the rejected case used two different filenames, so the result is not explained by repeating the
  same path string.

The future semantic rule is therefore uniqueness by ozone sector, not global non-repeatability.

### NOX_FILE

The same scoped pattern is confirmed:

- repeated records are accepted across distinct `NOXSECTR` sectors;
- a second file assignment to the same sector is rejected with `E501`;
- the rejected case used two different filenames.

The future semantic rule is uniqueness by ambient-NOx sector.

## Boundaries

- Results apply to the exact deck and executable hashes recorded in the machine-readable evidence.
- Successful setup does not make source-recognized development syntax regulatory.
- Warning `W650` observed during the SWPOINT numerical run is a model-computation warning and does
  not negate syntactic/semantic acceptance of the tested form.
- This batch does not resolve temporal vector cardinality, ARCFTOPT repetition, VBARRIER boundaries,
  receptor continuation omissions, event output formatting, or the remaining cataloged questions.
- Production lexer/CST work remains gated.

## Retained evidence

- manifest: `reference/probes/v26135/batch1/manifest.json`;
- reviewed machine result: `reference/probes/v26135/batch1/result.json`;
- evidence harness: `tools/run_v26135_official_behavior_probes.py`;
- workflow: `.github/workflows/epa-official-behavior-probes.yml`.
