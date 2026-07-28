# Next Steps

## Immediate next task

Create the **AERMOD v26135 official capability inventory** before implementing runstream classes.

### Deliverables

1. `reference/epa/v26135/manifest.yaml` with official assets, versions, checksums where available, and distribution notes;
2. `reference/coverage/v26135-keywords.csv` covering pathway, keyword, arguments, repeatability, applicability, and official references;
3. `reference/coverage/v26135-source-types.csv` covering every official source type and associated keywords;
4. `reference/coverage/v26135-outputs.csv` covering output keywords and file formats;
5. a source-code map connecting parser routines and keyword handlers to Fortran files/subroutines;
6. a written gap report comparing official v26135 capabilities with `pyaermod`, without copying its implementation.

## Implementation after the inventory

Begin the loss-aware runstream layer in this order:

1. token and source-location model;
2. pathway/block splitter;
3. comment and unknown-line preservation;
4. AST nodes;
5. format-preserving writer;
6. golden round-trip tests using official sample decks;
7. semantic mapping only after syntax preservation is reliable.

## Known decisions still pending

- final licence;
- exact project persistence format;
- CLI framework;
- whether generated schema artifacts live in the wheel or are built at release time.
