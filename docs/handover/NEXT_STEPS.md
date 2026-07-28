# Next Steps

## Immediate next task

Turn the **v26135 capability-inventory seed** into a source-verified specification.

### Required deliverables

1. download and hash the official `aermod_source.zip`, sample-run archive, and test-case archive;
2. record archive contents and exact compiler/build instructions;
3. expand every keyword row with exact syntax, argument types, units, required/optional status, repeatability, defaults, ranges, dependencies, conflicts, regulatory/development status, and error behavior;
4. map every keyword to exact Fortran file, subroutine/symbol, and source-line range;
5. link each capability to official sample/test fixtures and expected outputs;
6. complete the official-versus-PyAERMOD coverage audit without copying implementation code;
7. decide and document how generated schemas are built, validated, and bundled.

## Implementation after source verification

Begin the loss-aware runstream layer in this order:

1. token and source-location model;
2. pathway/block splitter;
3. blank-line, comment, include, and unknown-record preservation;
4. immutable syntax-tree nodes that retain original spelling and spacing;
5. format-preserving writer;
6. golden byte/semantic round-trip tests using official sample decks;
7. semantic project mapping only after syntax preservation is reliable.

## Acceptance criteria before parser work

- all official top-level keywords inventoried with current references;
- official source archive materialized and hashed;
- pathway dispatch and keyword handlers mapped at least to subroutine level;
- representative official sample decks available for CO, SO, RE, ME, EV, and OU;
- unknown/development-option preservation policy covered by tests;
- CI failure either fixed or documented with actionable platform evidence.

## Known decisions still pending

- final licence;
- exact project persistence format;
- CLI framework;
- whether generated schema artifacts live in the wheel or are built at release time;
- policy for distributing or downloading EPA executables and official test assets.
