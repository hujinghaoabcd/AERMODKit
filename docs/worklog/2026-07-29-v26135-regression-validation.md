# Worklog — 2026-07-29 — v26135 official source and regression baseline

## Objective

Turn the Phase 0 inventory into an auditable source/build/test baseline using current EPA v26135 assets.

## Completed

- used GitHub-hosted runners to download the official source, sample-run, and test-case ZIPs because the local working container could not resolve `gaftp.epa.gov`;
- calculated and independently verified archive SHA256 values;
- indexed all archive entries without committing the large ZIP files;
- extracted and indexed the complete official AERMOD source;
- identified 566 Fortran program units and exact pathway dispatchers;
- mapped 120 primary records to source branches and candidate handler calls;
- reproduced the EPA GNU build with GNU Fortran 14.2.0, exact flags, and exact 29-unit order;
- retained all compiler warnings as evidence without changing EPA code;
- extracted the current `aermet26135_aermod26135` fixture set;
- created a 53-case feature and keyword registry;
- reran ordinary tests in independent sandboxes to prevent output cross-contamination;
- recognized and correctly executed the PM10 1986–1990 MULTYEAR dependency chain;
- completed all 53 official decks successfully;
- verified that all 189 official expected output filenames were generated;
- compared every main output using limited, documented canonicalization;
- classified parity outcomes and flagged `capped` for compiler-sensitive investigation;
- added a reusable validation tool and machine-readable reports;
- changed EPA asset and current-fixture snapshot workflows to manual-only triggers after identifying cumulative PR path matching that caused repeated large downloads.

## Important findings

1. All 53 model runs succeed. The earlier apparent failures for PM10 1987–1990 were caused by running dependency-chain decks independently.
2. Twenty-seven main outputs are canonical exact after neutralizing only run date/time, output path prefix, line endings, and trailing whitespace.
3. Ten additional cases have no extracted result-value difference; changes are signed zero, tied receptor ordering, or one diagnostic buffer representation.
4. Fifteen cases show small compiler/platform floating-point drift at or below `2.21241e-4` relative difference.
5. `capped` shows a materially larger extracted result-value relative difference of about 5.2613%; `capped_nostd` is canonical exact.
6. Binary MULTYEAR state files are workflow-valid but are not assumed byte-portable across compilers.

## Guardrails

- do not patch EPA numerical source merely to match a reference file;
- do not treat tied-receptor ordering as a concentration difference;
- do not run MULTYEAR decks as independent cases;
- do not mix official expected outputs and generated outputs in the same directory;
- do not establish a global regression tolerance from one output family.

## Next handoff

Investigate `capped` with EPA's distributed executable, Intel `ifx`, and controlled GNU compiler/flag variants. In parallel, continue the exact keyword argument/validation schema and clean-room PyAERMOD coverage audit. Parser work remains blocked until the remaining specification acceptance criteria are met.
