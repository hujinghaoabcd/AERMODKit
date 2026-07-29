# Worklog: official v26135 behavior probes batch 2

- Date: 2026-07-29
- Development branch: `agent/official-behavior-probes-batch2`
- Pull request: #9, draft during evidence review
- Base: behavior-batch-1-complete `main`
- Phase: official behavior evidence before production loss-aware syntax

## Objective

Resolve the next high-priority parser-shaping questions without starting a production parser:

- incomplete O3/NOx temporal vectors;
- VBARRIER range and same-side behavior;
- event-output FILEFORM under DFAULT.

## Harness changes

Batch 2 introduced a manifest-driven harness capable of:

- retained fixture bases;
- preparation-generated downstream decks;
- literal and regex-based deterministic mutations;
- required generated-file checks;
- isolated workspaces and full file hashing;
- manifest-defined source ranges;
- exact diagnostic-call pattern extraction from the official source tree.

The harness is evidence infrastructure only and is not the application runner.

## Exploratory run and expansion

The first 20-case run succeeded but was not promoted directly because review identified three useful
coverage additions:

- global MONTH temporal cases needed sector-scoped controls;
- first-barrier range endpoints needed second-barrier endpoint controls;
- unequal same-side selection needed an equal-distance tie case.

The manifest was extended through a separate case fragment rather than by duplicating the original
manifest. The final reviewed batch contains one preparation and 27 cases.

## Final reviewed evidence

- workflow run: `30452705724`;
- reviewed head: `aaf683d4d0fa089a6d4159b9ea17b66e959cf1e3`;
- artifact ID: `8724254777`;
- artifact digest: `sha256:a7a27eb5c09ccb13a00f2d7a9bf9aa0c60e5cc6297e23765144b354a1c519d2e`;
- artifact size: `220,514,839` bytes;
- preparation: 1 accepted;
- cases: 15 accepted, 12 rejected, 0 indeterminate;
- all 28 expectations met.

The same head passed the full nine-job CI run `30452701635` and the retained batch-1 workflow
`30452701321`.

## Findings

### Temporal vectors

- complete global and sector MONTH vectors were accepted for O3VALUES and NOX_VALS;
- 11-of-12 O3VALUES vectors were rejected with E261;
- 11-of-12 NOX_VALS vectors were rejected with E603;
- sector messages name O3SECT1 or NOXSCT1;
- source evidence shows one count-versus-required-maximum rule across supported flags and scopes.

### VBARRIER

- HT 2.0..10.0, WT 2.5..13.0, LAI 4.0..10.92 and LM 0.55..3.75 are inclusive for both positions;
- below/above cases map to E371, E372, E373 and E374;
- unequal same-side DCL values produce W375 and zero the farther barrier;
- equal same-side DCL values retain both input records, produce no W375, then emit W620 at runtime;
- the v26135 equality tie uses barrier 2 because the source changes the default only for strict barrier-1 closeness.

### Event-output FILEFORM

- EXP remains EXP outside the DFAULT + criteria-pollutant combination;
- FIX is accepted for DFAULT/SO2;
- EXP under DFAULT/SO2 emits W595 and is reset to fixed output notation;
- source evidence expresses the general condition through the PollCrit flag.

## Gate update

The three completed catalog entries are:

- `temporal_vector_incomplete`;
- `SO-VBARRIER-RANGE-01`;
- `OU-EVENT-FILEFORM`.

The whole-spec behavior inventory is now 19 total, 7 executed, 1 source-resolved and 11 pending.
The syntax implementation gate remains closed.

## Boundary

The MONTH and SO2 executable cases are representative. Broader flag/criteria behavior is promoted only
because the exact official source branches are retained alongside the executable evidence. No semantic
model, production parser, formatter, runner, output parser or GIS layer was introduced.
