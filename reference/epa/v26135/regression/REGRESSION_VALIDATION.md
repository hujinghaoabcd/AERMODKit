# AERMOD v26135 official regression validation

## Scope

This report validates the unmodified EPA AERMOD v26135 Fortran source against the current official EPA test configuration `aermet26135_aermod26135`, and distinguishes the EPA-distributed executable baseline from a reproduced GNU source build.

Evidence used:

- official source ZIP SHA256: `5092c1d68b77d9407c9f67d497b440a79d2ee746f9ed6515a63ad4a5b11cd8ed`;
- official test ZIP SHA256: `fc5ad71de5ba64a50ed72d4d19c45b32ad14447353b1216c3d1f420ce84beff8`;
- official executable ZIP SHA256: `0ccf49702109637e665c8567891e365b4585a62a560faae35ce0194048683a24`;
- official `aermod.exe` SHA256: `599b491b021c7ec254ba3a1062386f287e56e54a0d3bb9b67cfa72275d6916da`;
- GNU Fortran 14.2.0;
- EPA-supplied GNU compile flags: `-fbounds-check -Wuninitialized -O2 -static`;
- EPA-supplied link flags: `-static -O2`;
- the exact 29-unit EPA compilation and link order.

The test fixtures contain 53 input decks, 18 meteorological/support files, and 189 official expected output files.

## Execution result

All **53 of 53** official input decks completed with return code 0 and the `AERMOD Finishes Successfully` marker under the reproduced GNU build.

The PM10 `MULTYEAR` decks for 1986–1990 are a dependency chain. The 1987–1990 decks fail when incorrectly run as independent tests because each consumes the previous year's `.sav` file. When run in EPA order in one isolated chain workspace, all five years complete successfully.

Total measured model execution time across the selected successful GNU executions was approximately **216.9 seconds** in the working container.

## Main-output comparison for the GNU build

Comparison canonicalization removes only:

- CRLF versus LF line endings and trailing whitespace;
- run date and time fields;
- the directory prefix on the main output filename.

It does **not** change model-result values.

| Classification | Cases | Interpretation |
|---|---:|---|
| Canonical exact | 27 | Main output becomes text-identical after the limited canonicalization above. |
| Representation/tie equivalent | 10 | Values match; differences are signed zero, equal-value receptor ordering, or one residual diagnostic buffer string. |
| Minor floating-point drift | 9 | Maximum extracted output-value relative difference is at most `1e-5`. |
| Moderate floating-point drift | 6 | Maximum extracted output-value relative difference is above `1e-5` and at most `1e-3`. |
| Compiler-specific localized difference | 1 | `capped` differs locally from the Intel-linked EPA executable while still completing successfully. |

### Representation-only findings

- `aermod-baldwin45`, `aermod-baldwinHoriz`, `aermod-baldwinVert`, `blp_urban`, `flatelev`, `lovett`, and `mcr` differ only as `0.0` versus `-0.0` in echoed meteorological values.
- `allsrcs` and `multurb` report the same concentration values but choose a different order among receptors tied at the same value.
- `Test3_Base_cart_3cond_SNC_bar` has matching numeric results but one diagnostic line differs in residual NUL-buffer text around `EVENT.TMP`.

### Small floating-point findings

The annual NO2 cases and SCIM show maximum extracted output-value relative differences around `4.0e-7` to `1.9e-6`. The PM10/PM2.5 family reaches approximately `2.21e-4` in the largest PM10 result difference.

These are recorded as compiler/platform drift, not silently rounded away. An automated regression gate must define an evidence-based tolerance separately for each output family.

## Resolved context for `capped`

The GNU build's maximum extracted relative difference is approximately **5.26130%**, but this does not describe a 5.26% error in the overall maximum or period-high result.

The largest differences are localized to:

- source group `STACK1C`, representing `POINTCAP` with standard building downwash;
- the `2ND HIGHEST 1-HR` table, with the largest differences in near-field cells;
- the `2ND HIGHEST 3-HR` table, with a maximum relative difference of about 5.2114%.

The `CAPPED.SUM` first period-high values show only about `2.13e-5` relative difference for `STACK1C` and `1.05e-5` for `STACK1C0`; the other seven source-group first period-high values are identical.

The EPA-distributed Windows executable was then run against the same fixtures in GitHub Actions run `30411529300`:

| Case | Canonical diff lines | Numeric mismatches | Maximum relative difference |
|---|---:|---:|---:|
| `capped` | 0 | 0 | 0 |
| `capped_nostd` | 0 | 0 | 0 |

This proves that the official expected outputs are consistent with the official executable. Binary inspection identifies an Intel Fortran runtime in the EPA executable, although the exact Intel compiler frontend/version remains unproven.

Recompiling only `prime.f`, `calc1.f`, `calc2.f`, `prise.f`, or `sigmas.f` at `-O0` while retaining the other GNU objects at the official `-O2` did not change the `capped` output. The difference is therefore not explained by a simple optimization change in any one of those units.

Detailed evidence is in `OFFICIAL_EXECUTABLE_PARITY.md` and `official-executable-parity.json`.

## Parity policy

- The EPA-distributed executable and current expected outputs define exact official release-fixture parity.
- Unmodified source builds define a separate compiler/platform parity tier.
- Source-build validation requires successful execution, structural/output coverage, and documented numerical tolerances; byte-exact output is not assumed across compilers.
- AERMODKit must not modify EPA numerical source merely to force GNU agreement with the Intel-linked official executable.

## All expected output names produced

Across the isolated cases and the PM10 chain:

- official expected output filenames: **189**;
- filenames produced by at least one corresponding GNU run: **189**;
- text outputs: **183**;
- text outputs with at least one canonical exact candidate: **131**;
- binary/state outputs: **6**.

Binary `.sav`/direct-access state files are not expected to be byte-portable across compiler and platform combinations. Their presence and workflow behavior are validated here; semantic binary validation requires a format-aware reader or downstream restart test.

## Reproducibility and limitations

- Each ordinary case ran in its own workspace with isolated `Outputs`, `postfiles`, and `plotfiles` directories.
- Meteorological files were shared read-only or hard-linked into isolated probe workspaces.
- The PM10 multiyear sequence used one isolated chain workspace.
- Official expected outputs remained separate from generated outputs.
- The report compares the main `.out` for every GNU case and filename coverage for all 189 expected outputs.
- The official executable probe currently covers `capped` and `capped_nostd`, not all 53 cases.
- The evidence establishes official fixture consistency and compiler-specific behavior; it does not establish universal regulatory equivalence for every source build.
- Heavy official regression and official-executable probes are manual/release evidence workflows rather than ordinary PR checks.

Machine-readable details are in:

- `v26135-regression-results.csv`;
- `v26135-regression-summary.json`;
- `v26135-output-file-coverage.csv`;
- `official-executable-parity.json`.
