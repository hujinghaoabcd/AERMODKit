# Next Steps

## Immediate next task: complete the remaining CO-pathway specification

CO batch 1 is now source-verified, bundled, loadable, and covered by structural tests. The next primary task is to extend the same evidence standard to the remaining CO records rather than begin production parser classes prematurely.

### CO specification batch 2: chemistry, decay, urban and receptor controls

Prioritize:

1. `HALFLIFE` and `DCAYCOEF`, including mutual exclusivity and units;
2. `FLAGPOLE` and `URBANOPT`;
3. ozone records: `O3SECTOR`, `OZONEFIL`, `OZONEVAL`, `O3VALUES`, `OZONUNIT`;
4. ambient NOx records: `NOXSECTR`, `NOX_FILE`, `NOXVALUE`, `NOX_VALS`, `NOX_UNIT`;
5. NO2 technique controls: `NO2EQUIL`, `NO2STACK`, `ARMRATIO`;
6. exact technique dependencies for OLM, PVMRM, ARM2, GRSM, TTRM and TTRM2.

### CO specification batch 3: deposition and option-dependent processing

Then cover:

1. `GASDEPDF`, `GASDEPVD`, `GDLANUSE`, and `GDSEASON`;
2. `LOW_WIND`, `AWMADWNW`, and `ORD_DWNW`;
3. `ARCFTOPT`;
4. every remaining CO record in the source dispatch map;
5. per-option regulatory/development status for all 40 `MODELOPT` tokens.

For every record continue to capture:

- exact syntax, positional fields, types, units, defaults and ranges;
- repeatability and ordering;
- dependencies and conflicts;
- regulatory/development status without inferring approval from source recognition;
- fatal, warning and informational diagnostics;
- exact Fortran dispatcher, handler and source ranges;
- official valid fixtures and documented absence where none exists;
- loss-aware preservation behavior.

## Behavior fixtures missing from the current official suite

Create focused executable probes for records not active in the 53 current decks:

- `EVENTFIL` defaults and invalid `SOCONT|DETAIL` behavior;
- `SAVEFILE` forms and day increment handling;
- `INITFILE` default filename and conflicts;
- repeated `DEBUGOPT` cards versus repeated individual options;
- extra payload on `STARTING` and `FINISHED`;
- unknown/future option tokens and preservation expectations.

These probes must keep official behavior evidence separate from AERMODKit semantic-policy choices.

## Inventory consolidation

- use `v26135-keyword-status-overrides.csv` and the batch evidence CSV as the authoritative promotion layer for completed records;
- consolidate those promotions into a regenerated main keyword inventory once a deterministic inventory-generation script exists;
- do not manually claim that untouched inventory rows were rewritten;
- add schema consistency checks so every promoted keyword resolves to a bundled record.

## Secondary numerical compatibility track

The `capped` investigation no longer blocks specification work, but remains a parallel compatibility task:

1. reproduce with Intel oneAPI `ifx` and EPA's `/O2 /Qipo /Qprec-div` flags;
2. compare complete GNU builds across supported compiler versions;
3. trace the first differing `STACK1C` hour through capped-source/downwash routines;
4. define supported official-executable, Intel-source-build and GNU-source-build tiers;
5. define tolerances by output family and intended use;
6. retain focused numerical workflows as manual-only evidence jobs.

## Parser implementation after specification acceptance

Begin the loss-aware runstream layer only after the specification and preservation fixtures are sufficient:

1. token and source-location model;
2. pathway/block state machine;
3. blank-line, comment, include and unknown-record preservation;
4. immutable syntax nodes retaining spelling and spacing;
5. format-preserving writer;
6. byte and semantic round-trip tests using official decks;
7. semantic project mapping only after syntax preservation is reliable.

## Acceptance criteria before parser work

- [x] official source, executable, sample and test archives materialized or hashed;
- [x] official build order and flags recorded;
- [x] pathway dispatch and inventoried primary records mapped to source branches;
- [x] current 53-deck fixture set indexed and executed successfully by the GNU build;
- [x] official `capped` fixture consistency verified with EPA's executable;
- [x] compiler-tier parity policy established;
- [x] CO batch 1 includes 14 bundled source-verified records and structural tests;
- [ ] every remaining CO keyword has an exact schema;
- [ ] every SO, RE, ME, EV and OU keyword has an exact schema;
- [ ] invalid, unknown and development-option preservation fixtures are selected;
- [ ] clean-room third-party coverage audit is complete;
- [ ] parser preservation policy is covered by tests.

## CI and evidence maintenance

- keep Ruff, strict mypy and pytest green on every PR;
- keep EPA asset, fixture and executable workflows manual-only;
- run heavy regression as a manual, scheduled or release-gate workflow;
- replace expiring artifact IDs with a durable fixture-acquisition policy before long-term reliance;
- monitor GitHub Actions runtime deprecations;
- never reduce checks merely to hide platform-specific failures.

## Decisions still pending

- final licence;
- project persistence format;
- CLI framework;
- generated-schema distribution policy;
- policy for distributing/downloading EPA executables and test assets;
- supported compiler/platform tiers and regulatory-use wording.
