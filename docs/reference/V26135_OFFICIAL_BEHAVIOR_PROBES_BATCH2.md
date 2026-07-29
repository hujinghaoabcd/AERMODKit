# AERMOD v26135 official behavior probes — batch 2

## Scope

This report records reviewed official-executable and official-source evidence for three retained
parser-shaping questions:

1. incomplete `O3VALUES` and `NOX_VALS` temporal vectors;
2. `VBARRIER` range boundaries and same-side selection;
3. event-output `FILEFORM` behavior under `DFAULT`.

The evidence harness is not the future AERMODKit runner. Production lexer/CST/writer, semantic
models, output parsing and GIS remain out of scope.

## Evidence identity

- official workflow run: `30452705724`;
- reviewed head: `aaf683d4d0fa089a6d4159b9ea17b66e959cf1e3`;
- artifact ID: `8724254777`;
- artifact digest: `sha256:a7a27eb5c09ccb13a00f2d7a9bf9aa0c60e5cc6297e23765144b354a1c519d2e`;
- artifact size: `220,514,839` bytes;
- official executable SHA-256: `599b491b021c7ec254ba3a1062386f287e56e54a0d3bb9b67cfa72275d6916da`;
- official source archive SHA-256: `5092c1d68b77d9407c9f67d497b440a79d2ee746f9ed6515a63ad4a5b11cd8ed`.

The official executable hash matches the retained v26135 evidence exactly.

## Method

The batch used one preparation and 27 isolated cases.

The preparation converted a short retained official Test1 deck to a POINT source and requested
`EVENTFIL`. The generated event deck was required to exist before any event-output case ran.

Each case retained:

- the exact materialized input deck and SHA-256;
- stdout and stderr;
- the main output and error file;
- parsed E/W/I diagnostics;
- all workspace file sizes and SHA-256 values;
- selected official source ranges;
- exact source-pattern contexts for E261, E603, E371-E374, W375, W620 and W595.

Return code zero was never treated as sufficient evidence of acceptance. Classification also required
the official success marker and absence of fatal diagnostics.

## Execution totals

| Group | Items | Accepted | Rejected | Indeterminate | Expectations met |
|---|---:|---:|---:|---:|---:|
| EVENT preparation | 1 | 1 | 0 | 0 | 1 |
| Probe cases | 27 | 15 | 12 | 0 | 27 |

## Temporal-vector completeness

### Executable cases

| Record and scope | Complete vector | Incomplete vector | Final diagnostic |
|---|---|---|---|
| global `O3VALUES MONTH` | accepted, 12 values | rejected, 11 values | `CO E261`, `NumVals=11` |
| sector `O3VALUES MONTH` | accepted, two complete sectors | rejected, SECT1 has 11 values | `CO E261`, `O3SECT1 N=11` |
| global `NOX_VALS MONTH` | accepted, 12 values | rejected, 11 values | `CO E603`, `NumVals 11` |
| sector `NOX_VALS MONTH` | accepted, two complete sectors | rejected, SECT1 has 11 values | `CO E603`, `NOXSCT1 N=11` |

### Source-supported general rule

The official source retains five E261 contexts and five E603 contexts covering global/sector forms
and hourly-file/no-file branches. Every completeness branch compares the accumulated value count
against the time-flag-derived required maximum.

Therefore:

- `O3VALUES` incomplete vectors are final CO input errors reported with E261;
- `NOX_VALS` incomplete vectors are final CO input errors reported with E603;
- sector diagnostics identify the affected sector;
- exact required counts remain determined by the existing time-flag cardinality table.

The executable cases use `MONTH` as a representative flag. Cross-flag behavior is supported by the
retained source branches, not by pretending that all twelve flags were executed separately.

## VBARRIER range boundaries

Both first- and second-barrier endpoint controls completed successfully.

| Parameter | Inclusive accepted range | Below/above result | Diagnostic |
|---|---:|---|---|
| height `HT` | 2.0–10.0 m | rejected | E371 |
| width `WT` | 2.5–13.0 m | rejected | E372 |
| leaf-area index `LAI` | 4.0–10.92 | rejected | E373 |
| leaf length `LM` / diagnostic LAD | 0.55–3.75 | rejected | E374 |

Official source uses strict `< minimum` and `> maximum` comparisons for both barrier positions,
confirming inclusive endpoints.

## VBARRIER same-side behavior

### Unequal absolute distances

When two barriers are on the same side and `|DCL1| < |DCL2|`:

- input processing emits W375 naming `VBARRIER 1`;
- the debug output retains barrier 1;
- barrier 2 is zeroed.

When `|DCL2| < |DCL1|`, the inverse occurs and W375 names `VBARRIER 2`.

### Equal absolute distances

When both barriers have the same-side and equal absolute DCL:

- input processing emits no W375;
- both barrier records remain populated in the debug output;
- runtime emits W620 repeatedly for affected hours/receptors;
- the v26135 runtime initializes the selected index to barrier 2 and changes it to barrier 1 only
  when barrier 1 is strictly closer.

The equality tie therefore selects barrier 2 in v26135. This is version-specific implementation
behavior, not a general physical recommendation.

## Event-output FILEFORM

A successful preparation generated a three-event processing deck. Four paired cases then established:

| Mode | Pollutant state | Requested form | Result |
|---|---|---|---|
| non-DFAULT | OTHER | EXP | accepted; exponential event values |
| DFAULT | OTHER | EXP | accepted; exponential event values |
| DFAULT | SO2 | FIX | accepted; fixed event values |
| DFAULT | SO2 | EXP | accepted with W595; output reset to fixed values |

The source condition is exact:

```text
EXP AND DFAULT AND PollCrit -> FILE_FORMAT = FIX and W595
EXP otherwise               -> FILE_FORMAT = EXP
```

SO2 is the executable criteria-pollutant case. Generalization to other criteria pollutants is based on
the retained `PollCrit` source branch.

## Acceptance-gate effect

Three retained questions are now classified as executed:

- `temporal_vector_incomplete`;
- `SO-VBARRIER-RANGE-01`;
- `OU-EVENT-FILEFORM`.

The normalized retained probe inventory becomes:

- total: 19;
- executed: 7;
- source-resolved: 1;
- official-executable pending: 11.

The behavior-probe gate remains incomplete and production loss-aware syntax remains closed.

## Evidence locations

- compact reviewed result: `reference/probes/v26135/batch2/result.json`;
- base manifest: `reference/probes/v26135/batch2/manifest.json`;
- additional case fragment: `reference/probes/v26135/batch2/additional-cases.json`;
- source diagnostic searches: `reference/probes/v26135/batch2/source-searches.json`;
- complete workspaces and source contexts: workflow artifact `8724254777`.
