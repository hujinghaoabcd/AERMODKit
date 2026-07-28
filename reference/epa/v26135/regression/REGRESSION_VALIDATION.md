# AERMOD v26135 official regression validation

## Scope

This report validates the unmodified EPA AERMOD v26135 Fortran source against the current official EPA test configuration `aermet26135_aermod26135`.

Evidence used:

- official source ZIP SHA256: `5092c1d68b77d9407c9f67d497b440a79d2ee746f9ed6515a63ad4a5b11cd8ed`;
- official test ZIP SHA256: `fc5ad71de5ba64a50ed72d4d19c45b32ad14447353b1216c3d1f420ce84beff8`;
- GNU Fortran 14.2.0;
- EPA-supplied GNU compile flags: `-fbounds-check -Wuninitialized -O2 -static`;
- EPA-supplied link flags: `-static -O2`;
- the exact 29-unit EPA compilation and link order.

The test fixtures contain 53 input decks, 18 meteorological/support files, and 189 official expected output files.

## Execution result

All **53 of 53** official input decks completed with return code 0 and the `AERMOD Finishes Successfully` marker.

The PM10 `MULTYEAR` decks for 1986–1990 are a dependency chain. The 1987–1990 decks fail when incorrectly run as independent tests because each consumes the previous year's `.sav` file. When run in EPA order in one isolated chain workspace, all five years complete successfully.

Total measured model execution time across the selected successful executions was approximately **216.9 seconds** in the working container.

## Main-output comparison

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
| Compiler-sensitive investigation | 1 | A material difference requires explicit investigation before numerical parity is claimed. |

### Representation-only findings

- `aermod-baldwin45`, `aermod-baldwinHoriz`, `aermod-baldwinVert`, `blp_urban`, `flatelev`, `lovett`, and `mcr` differ only as `0.0` versus `-0.0` in echoed meteorological values.
- `allsrcs` and `multurb` report the same concentration values but choose a different order among receptors tied at the same value.
- `Test3_Base_cart_3cond_SNC_bar` has matching numeric results but one diagnostic line differs in residual NUL-buffer text around `EVENT.TMP`.

### Small floating-point findings

The annual NO2 cases and SCIM show maximum extracted output-value relative differences around `4.0e-7` to `1.9e-6`. The PM10/PM2.5 family reaches approximately `2.21e-4` in the largest PM10 result difference.

These are recorded as compiler/platform drift, not silently rounded away. A future automated regression gate must define an evidence-based tolerance separately for each output family.

### Flagged case: `capped`

The `capped` case completes successfully but does not meet a tight numerical-parity criterion under GNU Fortran 14.2 with the EPA GNU flags:

- maximum extracted output-value absolute difference: **2.2248**;
- maximum extracted output-value relative difference: **5.26130%**.

Some remaining differences in this case are tied-receptor ordering, but real concentration differences are also present. The nearby `capped_nostd` case is canonical-exact, which narrows the investigation toward the capped/horizontal-stack downwash pathway and compiler/optimization behavior.

AERMODKit must not patch the EPA numerical source to force agreement. The next investigation should compare:

1. EPA's distributed Windows executable;
2. Intel oneAPI `ifx` with the supplied `/O2 /Qipo /Qprec-div` flags;
3. GNU builds across versions and optimization/precision flags;
4. the exact `capped` output sections and involved source routines.

## All expected output names produced

Across the isolated cases and the PM10 chain:

- official expected output filenames: **189**;
- filenames produced by at least one corresponding run: **189**;
- text outputs: **183**;
- text outputs with at least one canonical exact candidate: **131**;
- binary/state outputs: **6**.

Binary `.sav`/direct-access state files are not expected to be byte-portable across compiler and platform combinations. Their presence and workflow behavior are validated here; semantic binary validation requires a format-aware reader or downstream restart test.

## Reproducibility and limitations

- Each ordinary case ran in its own workspace with isolated `Outputs`, `postfiles`, and `plotfiles` directories.
- Meteorological files were shared read-only.
- The PM10 multiyear sequence used one isolated chain workspace.
- Official expected outputs remained separate from generated outputs.
- The report compares the main `.out` for every case and filename coverage for all 189 expected outputs.
- This report does not yet establish regulatory equivalence for every compiler/platform combination.
- Heavy official regression should run as a scheduled/manual workflow or release gate rather than on every small pull request.

Machine-readable details are in:

- `v26135-regression-results.csv`;
- `v26135-regression-summary.json`;
- `v26135-output-file-coverage.csv`.
