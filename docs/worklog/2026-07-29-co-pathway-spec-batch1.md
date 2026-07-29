# Worklog: CO pathway exact specification batch 1

- Date: 2026-07-29
- Branch: `agent/bootstrap-project-foundation`
- Pull request: #1

## Objective

Convert the first group of CO-pathway inventory entries into a versioned, machine-readable, source-verified specification that can be loaded and tested without implying complete AERMOD support.

## Records completed

`STARTING`, `FINISHED`, `TITLEONE`, `TITLETWO`, `MODELOPT`, `AVERTIME`, `POLLUTID`, `RUNORNOT`, `ERRORFIL`, `EVENTFIL`, `SAVEFILE`, `INITFILE`, `MULTYEAR`, and repeatable `DEBUGOPT`.

## Evidence processed

- `coset.f` dispatch branches and handlers;
- `modules.f` field capacities and pollutant storage size;
- all 53 current official input decks;
- the current official regression findings for PM10 MULTYEAR state chaining;
- current v26135 source comments documenting repeatable `DEBUGOPT`.

## Outputs

- bundled CO pathway index and four batch-1 record fragments;
- typed loader and structural validator;
- tests for record order, mandatory records, MODELOPT/DEBUGOPT catalogs, MULTYEAR conflicts, and unsupported pathways;
- source/fixture evidence CSV;
- human-readable reference guide.

## Validation

A temporary package reconstruction loaded the bundled resource fragments and passed eight local pytest tests. Final Ruff, strict mypy, and cross-platform pytest validation is delegated to the repository CI after the commit.

## Key decisions

1. The schema is explicitly partial and versioned.
2. Record fragments are separate package resources so later batches can extend CO without creating one monolithic file.
3. Source-recognized options are not automatically labelled regulatory.
4. Official handler quirks and comment/code discrepancies are retained as evidence.
5. Unknown or extra syntax must be preserved before semantic validation.
6. No production runstream parser is started until the remaining exact specification and preservation fixtures are ready.

## Next work

Continue CO specification with decay, flagpole, urban, ozone/NOx background, chemistry, deposition, low-wind, RLINE, aircraft, and other option-dependent records. Add invalid official-behavior probes where the current fixture suite has no active record.
