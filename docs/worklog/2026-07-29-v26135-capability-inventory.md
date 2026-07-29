# Worklog: v26135 capability inventory seed

- Date: 2026-07-29
- Branch: `agent/bootstrap-project-foundation`
- Pull request: #1 (draft)

## Goal

Create the first official-evidence capability inventory before implementing AERMOD runstream classes.

## Completed

- re-verified the current EPA release as AERMOD 26135, released 2026-07-09;
- recorded component versions separately, including AERMAP 24142;
- created an official asset manifest with canonical URLs and materialization/checksum status;
- created a broad control/source/receptor/meteorology/event/output keyword inventory;
- created the current official source-type vocabulary and separated special/option-applied cases;
- created the output-control inventory and parser-priority seed;
- created an evidence-ranked Fortran source-map seed;
- created a clean-room PyAERMOD gap-audit seed;
- documented current release changes including repeatable DEBUGOPT, multiple HOUREMIS files, RLINEXT barrier enhancements, aircraft changes, and output fixes.

## Evidence inspected

- EPA current preferred-model release page and AERMOD product section;
- AERMOD v26135 Quick Reference Guide;
- AERMOD v26135 User Guide metadata and parsed text;
- AERMOD v26135 Transmittal Memorandum;
- AERMOD Model Change Bulletin 19;
- retained official-reference manifest and prior third-party audit notes.

## Validation and limitations

- CSV files were generated with a consistent schema and parsed back successfully;
- all keyword rows have an evidence status and official-reference field;
- the source archive, sample run, and test-case ZIPs could not be downloaded in the current runtime because DNS/name resolution failed;
- PDF screenshots failed with cache-miss errors, although parsed text was available;
- no SHA256 values or line-level source mappings are claimed;
- the retained local User Guide PDF is the 2023 edition and is explicitly excluded as a current-version authority.

## Next owner instructions

1. Materialize and hash the official v26135 source, sample, and test archives in a network-capable environment.
2. Extract exact argument signatures, repeatability, ranges, defaults, dependencies, and regulatory status from the current User Guide.
3. Map each keyword to exact Fortran files/subroutines and source lines.
4. Attach official sample/test fixtures to inventory rows.
5. Only then start the loss-aware token/source-location/pathway-block implementation.
