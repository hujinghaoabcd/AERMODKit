# Worklog: official v26135 behavior probes batch 1

- Date: 2026-07-29
- Development branch: `agent/official-behavior-probes-batch1`
- Pull request: #7, merged
- Merge commit: `4e6e92ddd86420144438a4e6d2eb0b77b3db33ab`
- Base: whole-spec-accepted `main`
- Phase: evidence collection before production loss-aware syntax

## Objective

Execute the first parser-shaping behavior probes with the EPA-distributed v26135 Windows executable
and retain enough evidence to distinguish accepted, rejected, and indeterminate behavior without
turning the probe harness into the application runner.

## Final batch

The reviewed batch contains three positive controls and six targeted observations:

1. official Test3 RLINEXT/RBARRIER control;
2. SWPOINT with ALPHA;
3. SWPOINT without ALPHA;
4. one-barrier VBARRIER form;
5. two-barrier VBARRIER form;
6. distinct-sector OZONEFIL control;
7. same-sector OZONEFIL duplicate;
8. distinct-sector NOX_FILE control;
9. same-sector NOX_FILE duplicate.

## Evidence retained by the workflow

- official executable size and SHA-256;
- official source archive size and SHA-256;
- exact materialized input deck for each case;
- stdout and stderr;
- main output and error files;
- parsed E/W/I diagnostic rows;
- every workspace file size and SHA-256;
- selected official `soset.f` and `coset.f` handler ranges;
- one machine-readable batch summary.

The full workspace artifact is run `30447131971`, artifact `8721942233`, digest
`sha256:4cfa463e9d2eb8f56e5d31d4df750c53ea4cadaa2d22b0bdf28a209a34f171d1`.
The reviewed compact result is committed at `reference/probes/v26135/batch1/result.json`.

## Corrections made during execution

The first exploratory run was not promoted as final evidence because it exposed two probe-harness
issues and one test-design issue:

- unsuccessful completion matching was case-sensitive and did not parse fatal diagnostics printed
  only in the main output;
- the initial VBARRIER LAI and LM values were outside the source-enforced valid ranges;
- the first OZONEFIL duplicate repeated the same path and therefore did not isolate sector identity.

The final run corrected all three issues, added distinct-sector positive controls, used different
filenames for same-sector duplicate cases, and produced zero indeterminate outcomes.

## Reviewed result

| Case | Outcome | Key diagnostic |
|---|---|---|
| official Test3 control | accepted | none fatal |
| SWPOINT with ALPHA | accepted | none fatal |
| SWPOINT without ALPHA | rejected | `SO E198` |
| one VBARRIER | accepted | none fatal |
| two VBARRIERs | accepted | none fatal |
| distinct-sector OZONEFIL | accepted | none fatal |
| same-sector OZONEFIL | rejected | `CO E501` |
| distinct-sector NOX_FILE | accepted | none fatal |
| same-sector NOX_FILE | rejected | `CO E501` |

Totals: 9 cases, 6 accepted, 3 rejected, 0 indeterminate.

## Acceptance-gate update

Four retained questions now have final official-executable evidence:

- `SO-SWPOINT-01`;
- `SO-VBARRIER-01` for valid one- and two-barrier forms;
- `ozonefil_same_sector_duplicate`;
- `nox_file_same_sector_duplicate`.

The combined VBARRIER question was split so that range boundaries and same-side `W375` behavior
remain pending as `SO-VBARRIER-RANGE-01`. The normalized probe inventory is now 19 total, 4 executed,
1 source-resolved, and 14 pending.

## Validation and publication

- reviewed evidence workflow `30447131971` completed successfully;
- evidence harness/manifest CI `30447131982` passed all nine jobs;
- final PR #7 head `3331327ac4ab3cb40db6b81ffad9955907316dd7` passed all nine jobs in CI `30448106914`;
- the same final head passed official behavior workflow `30448106897`;
- PR #7 was merged to `main` as `4e6e92ddd86420144438a4e6d2eb0b77b3db33ab`.

## Boundary

Production lexer/CST, semantic models, runner, output parser, and GIS remain out of scope. The
remaining parser-shaping behavior probes must be completed or explicitly deferred through a
preservation-safe ADR before syntax implementation begins.
