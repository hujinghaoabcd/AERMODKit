# Next Steps

## Immediate next task: resolve the `capped` parity finding

The source/build/test pipeline is now operational. The next evidence task is to determine why the official `capped` expected output differs materially from the GNU Fortran 14.2 reproduction while `capped_nostd` is canonical exact.

### Required investigation

1. obtain and hash the EPA-distributed Windows executable;
2. run `capped` and `capped_nostd` with that executable against the same official fixtures;
3. build with Intel oneAPI `ifx` using EPA's `/O2 /Qipo /Qprec-div` flags when an appropriate runner is available;
4. compare GNU compiler versions and controlled optimization/precision variants without changing EPA source;
5. isolate the first divergent output section and trace it to capped/horizontal-stack downwash routines;
6. document whether the EPA expected output is compiler-specific and define the correct parity rule.

## Complete the source-verified keyword specification

1. expand every keyword row with exact syntax and positional arguments;
2. record argument types, units, required/optional status, repeatability, defaults, ranges, dependencies, conflicts, and regulatory/development status;
3. attach exact Fortran branch and called-handler locations;
4. map each keyword and feature to official sample/test fixtures;
5. capture associated fatal, warning, and informational diagnostics;
6. complete the official-versus-PyAERMOD clean-room coverage audit;
7. decide how generated schemas are validated and bundled.

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

- [x] official source, sample, and test archives materialized and hashed;
- [x] exact official build order and flags recorded;
- [x] pathway dispatch and all currently inventoried primary records mapped to source branches;
- [x] current 53-deck official fixture set indexed;
- [x] reproduced executable completes all 53 official decks;
- [x] expected and generated outputs kept separate during validation;
- [ ] `capped` compiler-sensitive difference resolved or governed by an explicit parity policy;
- [ ] every keyword has an exact argument and validation schema;
- [ ] representative EV-pathway and unknown/development-option preservation fixtures selected;
- [ ] clean-room third-party coverage audit completed;
- [ ] parser preservation policy covered by tests.

## CI and regression maintenance

- keep Ruff, strict mypy, and pytest green on every PR;
- retain EPA asset and current-fixture snapshot workflows as manual-only jobs;
- add heavy official regression as a manual, scheduled, or release-gate workflow rather than every small commit;
- store expected tolerances by compiler, platform, case, and output family;
- monitor Node runtime deprecation warnings for GitHub Actions dependencies;
- do not reduce checks merely to hide platform-specific failures.

## Known decisions still pending

- final licence;
- exact project persistence format;
- CLI framework;
- generated-schema distribution policy;
- policy for distributing/downloading EPA executables and official test assets;
- supported compiler/platform parity tiers.
