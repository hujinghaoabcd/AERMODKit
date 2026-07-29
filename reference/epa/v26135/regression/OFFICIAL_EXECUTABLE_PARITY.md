# AERMOD v26135 official executable parity

## Purpose

This evidence check determines whether the official EPA expected outputs for the `capped` family are internally consistent with EPA's distributed Windows executable, and separates that question from cross-compiler source-build parity.

## Official binary evidence

The canonical EPA archive was downloaded in GitHub Actions run `30411529300`.

- archive URL: `https://gaftp.epa.gov/Air/aqmg/SCRAM/models/preferred/aermod/aermod_exe.zip`;
- archive SHA256: `0ccf49702109637e665c8567891e365b4585a62a560faae35ce0194048683a24`;
- extracted executable: `aermod.exe`;
- executable size: `3,940,864` bytes;
- executable SHA256: `599b491b021c7ec254ba3a1062386f287e56e54a0d3bb9b67cfa72275d6916da`;
- binary format: PE32+ Windows console executable, x86-64;
- evidence artifact ID: `8708575372`;
- evidence artifact digest: `7ef4ce9d2a9b26f43b399c4dc62740d57544f38734b96c7fef4a449c66865ba1`.

Binary strings and linked-runtime evidence identify Intel Fortran runtime components. This supports an Intel build family, but does not prove the exact compiler frontend or version used for the distributed executable.

## Probe method

The probe:

1. reused the retained current `aermet26135_aermod26135` fixture artifact;
2. kept expected and generated outputs in separate directories;
3. ran each case in an isolated workspace;
4. removed only date/time fields, line-ending differences, trailing whitespace, and output-directory prefixes before text comparison;
5. did not round or alter model-result values;
6. localized any remaining numeric differences by source group and output table.

The workflow and probe are retained as:

- `.github/workflows/epa-official-executable-parity.yml`;
- `tools/probe_official_aermod_executable.py`.

The workflow is manual-only after this evidence run.

## Results

| Case | Return code | Success marker | Canonical diff lines | Numeric mismatches | Maximum relative difference |
|---|---:|---:|---:|---:|---:|
| `capped` | 0 | yes | 0 | 0 | 0 |
| `capped_nostd` | 0 | yes | 0 | 0 | 0 |

The official EPA executable reproduces both official expected outputs exactly after the limited neutralization of run metadata.

## GNU source-build localization

The unmodified GNU Fortran 14.2 source build also completes both cases successfully, but `capped` has localized numerical differences while `capped_nostd` is canonical-exact.

The earlier maximum extracted relative difference of approximately `5.2613%` is concentrated in:

- source group `STACK1C`;
- the `2ND HIGHEST 1-HR` table;
- selected near-field cells.

The `2ND HIGHEST 3-HR` table reaches about `5.2114%`. This value does not describe the overall period-high result: the first period-high values in `CAPPED.SUM` differ by only about `2.13e-5` for `STACK1C` and `1.05e-5` for `STACK1C0`, while the other seven source-group first period-high values are identical.

Recompiling `prime.f`, `calc1.f`, `calc2.f`, `prise.f`, or `sigmas.f` individually at `-O0`, with all other GNU objects retained at the official `-O2`, did not alter the result. A single-unit optimization change in those files therefore does not explain the difference.

## Decision

1. The EPA-distributed executable and official expected outputs define exact release-fixture parity.
2. Reproduced source builds are evaluated in a separate compiler/platform evidence tier.
3. Exact cross-compiler byte or numeric parity is not assumed.
4. Tolerances must be documented by compiler, platform, case, output family, and intended use.
5. AERMODKit will not modify EPA numerical source merely to force GNU agreement with the Intel-linked official executable.

Machine-readable evidence is in `official-executable-parity.json`.
