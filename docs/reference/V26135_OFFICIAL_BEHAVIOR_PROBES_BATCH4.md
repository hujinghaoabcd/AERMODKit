# AERMOD v26135 official behavior probes — Batch 4

## Scope

Batch 4 resolves the remaining SO/RE parser-shaping questions before production loss-aware syntax work:

- `SO-PLATFORM-01`;
- `SO-BACKGRND-01`;
- `RE-GRID-ID-01`;
- `RE-DISC-EXTRA-01`.

The retained evidence uses the EPA-distributed AERMOD v26135 Windows executable and exact contexts from the v26135 source archive. The harness is evidence infrastructure, not the future application runner.

## Reviewed evidence

- workflow run: `30479954822`;
- reviewed head: `215764df489d623c3433e6baa0a6b301b0ab3f68`;
- artifact ID: `8735323902`;
- artifact name: `aermod-v26135-official-behavior-probes-batch4-215764df489d623c3433e6baa0a6b301b0ab3f68`;
- artifact digest: `sha256:cc3cb39b85bac2429e11deda087853e3a5a89852f0574a27968f1393012378f1`;
- artifact size: `338,627,341` bytes;
- official executable SHA-256: `599b491b021c7ec254ba3a1062386f287e56e54a0d3bb9b67cfa72275d6916da`;
- official source archive SHA-256: `5092c1d68b77d9407c9f67d497b440a79d2ee746f9ed6515a63ad4a5b11cd8ed`;
- cases: 40;
- accepted: 29;
- rejected: 11;
- indeterminate: 0;
- expectations met: 40/40.

Machine-readable evidence:

- `reference/probes/v26135/batch4/result.json`;
- `reference/probes/v26135/batch4/case-evidence.csv`;
- the full workflow artifact.

## PLATFORM

### Accepted forms

The exact semantic payload completed:

```text
SO PLATFORM <point_source_id> <base_elevation> <height> <width>
```

One and two additional numeric fields also completed.

The official `PLATFM` handler converts fields 4 through `IFC` to numeric temporary values but assigns only the first three values to the platform semantic state. Therefore trailing numeric fields are:

- accepted by v26135;
- semantically ignored after conversion;
- preservation-only for the future CST/writer;
- not additional PLATFORM parameters.

### Diagnostics

| Condition | Result |
|---|---|
| trailing nonnumeric field | `E208` |
| PLATFORM on a non-point source | `E631` |
| second PLATFORM for the same source | `E632` |
| PLATFORM and PRIME building inputs on the same source | `E633` |

The exploratory control initially used a source that already had PRIME inputs and correctly exposed `E633`. The final positive control uses a point source without PRIME building arrays.

## BACKGRND

### Static profile repetition

Both global and sector-scoped repeated `ANNUAL` records were rejected with `E231`, whether the second value matched or differed. This is a filled-slot conflict rather than last-assignment-wins.

### HOURLY repetition

A second HOURLY file for the same scope was rejected with `E168` and `E501`.

### HOURLY plus non-HOURLY

The following both completed:

```text
BACKGRND ANNUAL ... followed by BACKGRND HOURLY ...
BACKGRND HOURLY ... followed by BACKGRND ANNUAL ...
```

After normalizing only case-specific title, path, date, and time text, both outputs had SHA-256:

```text
2cea37d8b70122866e0b20c29b92aa937c2f550a2f909e6709e296f175c40468
```

The official source keeps separate `L_BGFile` and `L_BGValues` states. HOURLY observations are primary; non-HOURLY values substitute hours missing from the hourly file. Input order does not change that rule.

## GRIDCART and GRIDPOLR continuation forms

For an active grid block, the official executable accepted all three lexical forms:

```text
<secondary keyword> <fields...>
<NetID> <secondary keyword> <fields...>
<pathway keyword> <NetID> <secondary keyword> <fields...>
```

The first form omits both the pathway keyword and repeated NetID. The second omits only the pathway keyword. The third is fully explicit.

The source state rule is:

- if field 3 is a recognized secondary keyword, inherit active `PNETID`;
- if field 3 equals active `PNETID`, use field 4 as the secondary keyword;
- a different NetID inside the active block produces `E170`.

The wrong-ID cases also produce expected follow-on incomplete-grid diagnostics. The future CST must retain which lexical form appeared even though the semantic active grid ID is identical.

## DISCCART and DISCPOLR conditional fields

The executable accepted extra terrain and/or flagpole values when their governing option was inactive. It emitted `W229` and ignored those values semantically.

This behavior was confirmed for both Cartesian and polar discrete receptors across representative states:

- FLAT without FLAGPOLE;
- FLAT with FLAGPOLE;
- ELEV without FLAGPOLE;
- full DISCCART ELEV plus FLAGPOLE control.

The shared source branches use `W228` when a field required by an active option is missing.

`W229` does not make the input text discardable. The CST and preservation writer must retain every inactive-option field exactly, while the semantic projection may mark it inactive/ignored.

## Gate update

The normalized behavior inventory remains 19 questions:

```text
executed                     = 14
source_resolved              = 1
official_executable_pending  = 4
```

The remaining executable questions are:

- `ME-FORMAT-LEGACY`;
- `ME-SCIM-6FIELD`;
- `EV-PAIRING`;
- `OU-FILE-CONFLICT`.

The behavior gate and syntax implementation gate remain closed.
