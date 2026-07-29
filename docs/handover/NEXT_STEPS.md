# Next Steps

## Immediate next task: exact CO-pathway keyword specification

The official executable comparison has resolved the main uncertainty around `capped`: the EPA executable exactly reproduces the official fixture, while the GNU build has a localized compiler-specific difference. The next primary development task is therefore to turn the CO pathway inventory into a complete, machine-usable specification.

### CO specification batch 1

Start with the foundational control records:

1. `STARTING` / `FINISHED`;
2. `TITLEONE` / `TITLETWO`;
3. `MODELOPT` including regulatory, development, ALPHA, and BETA option interactions;
4. `AVERTIME`;
5. `POLLUTID`;
6. `RUNORNOT`;
7. `ERRORFIL`;
8. `EVENTFIL`;
9. `DEBUGOPT`, including v26135 repeatability;
10. `SAVEFILE` / `INITFILE` and MULTYEAR dependencies.

For each record capture:

- exact field syntax and position;
- argument type, unit, required/optional status, default and range;
- repeatability and ordering rules;
- dependencies, conflicts, regulatory/development status;
- fatal, warning and informational diagnostics;
- exact Fortran branch, called routines and source-line range;
- official sample/test fixtures exercising valid and invalid forms;
- preservation behavior for comments, unknown fields and future options.

### Required outputs

- a versioned CO schema source file;
- an evidence table linking each field to guide/source/test references;
- schema validation tests generated from official fixtures;
- a documented schema build/bundle policy;
- updates to keyword inventory evidence status.

## Secondary numerical compatibility track

The `capped` result no longer blocks keyword specification, but numerical compatibility remains an explicit parallel task:

1. reproduce with Intel oneAPI `ifx` and EPA's `/O2 /Qipo /Qprec-div` flags;
2. compare complete GNU builds across supported compiler versions;
3. trace the first differing `STACK1C` hour through cappd-source and downwash routines;
4. define official-executable, Intel-source-build and GNU-source-build parity tiers;
5. define tolerances by output family and intended use;
6. keep the focused parity workflow manual-only.

## Parser implementation after acceptance

Begin the loss-aware runstream layer in this order:

1. token and source-location model;
2. pathway/block splitter;
3. blank-line, comment, include, and unknown-record preservation;
4. immutable syntax-tree nodes retaining original spelling and spacing;
5. format-preserving writer;
6. golden byte/semantic round-trip tests using official decks;
7. semantic project mapping only after syntax preservation is reliable.

## Acceptance criteria before parser work

- [x] official source, executable, sample, and test archives materialized or hashed;
- [x] exact official build order and flags recorded;
- [x] pathway dispatch and all currently inventoried primary records mapped to source branches;
- [x] current 53-deck official fixture set indexed;
- [x] reproduced GNU executable completes all 53 official decks;
- [x] expected and generated outputs kept separate during validation;
- [x] official `capped` fixture consistency verified with EPA's executable;
- [x] compiler-tier parity policy established;
- [ ] every CO keyword has an exact argument and validation schema;
- [ ] every remaining pathway keyword has an exact schema;
- [ ] representative EV-pathway and unknown/development-option preservation fixtures selected;
- [ ] clean-room third-party coverage audit completed;
- [ ] parser preservation policy covered by tests.

## CI and regression maintenance

- keep Ruff, strict mypy, and pytest green on every PR;
- retain EPA asset, fixture, and executable workflows as manual-only jobs;
- run heavy official regression as a manual, scheduled, or release-gate workflow;
- store expected tolerances by compiler, platform, case, and output family;
- replace expiring cross-workflow artifact IDs with a durable fixture acquisition policy before relying on the official-executable probe long term;
- monitor Node runtime deprecation warnings for GitHub Actions dependencies;
- do not reduce checks merely to hide platform-specific failures.

## Known decisions still pending

- final licence;
- exact project persistence format;
- CLI framework;
- generated-schema distribution policy;
- policy for distributing/downloading EPA executables and official test assets;
- supported compiler/platform parity tiers and regulatory-use wording.
