# PyAERMOD versus official AERMOD v26135: gap-audit seed

## Scope and policy

PyAERMOD is a useful comparison target, but it is not the AERMODKit specification, architecture template, or source-code base. This document records audit questions and previously observed risks; it does not copy PyAERMOD implementation code.

## Already observed

1. Previous repository inspection found parts of the input-generation documentation described against AERMOD 24142 while newer CI work targeted 26135. AERMODKit therefore requires an explicit versioned schema instead of an unversioned set of Python classes.
2. The examined GIS importer reduced a multi-vertex line to its first and last coordinate unless the user split it upstream. AERMODKit must preserve road geometry lineage and provide explicit segmentation strategies.
3. The examined GUI was primarily form-driven rather than GIS-first. AERMODKit will keep GUI code outside the model core and make spatial layers first-class.
4. A JSON-only project format is insufficient for large geospatial, temporal, and multidimensional data.

## v26135 feature areas requiring a fresh coverage audit

The following current official capabilities must be checked explicitly. Absence from this list does not imply PyAERMOD lacks or supports them.

- ALPHA and BETA development-option behavior;
- RLINE/RLINEXT barriers, depression, edge effects, `SBARRIER`, `BAREDGE`, and vegetative-barrier behavior;
- aircraft processing through `ARCFTOPT` and `ARCFTSRC`;
- multiple `HOUREMIS` files introduced or enabled in v26135;
- repeatable `DEBUGOPT` behavior;
- ozone/ambient-NOx sector and period inputs;
- GRSM source-group contributions in `MAXDCONT`;
- complete output vocabulary and exact file parsing;
- restart/MULTYEAR interactions affecting `MAXIFILE` and `POSTFILE`;
- all 12 current official LOCATION source types;
- loss-aware preservation of comments, includes, unknown records, record order, and unsupported development options;
- exact regulatory/development status for every option.

## Audit method

For each official capability:

1. identify the official v26135 manual record and source handler;
2. locate the corresponding public PyAERMOD API only after the official semantics are documented independently;
3. classify coverage as complete, partial, simplified, version-mismatched, absent, or unverified;
4. run official sample/test decks through the EPA executable;
5. compare generated runstreams and numerical outputs, not merely process exit status;
6. record licensing and provenance before reusing any nontrivial code.

## Current conclusion

No decision has been made to fork, depend on, or copy PyAERMOD. The current AERMODKit work remains an independent clean design based on official EPA evidence.
