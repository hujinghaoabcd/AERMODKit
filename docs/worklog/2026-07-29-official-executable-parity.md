# Worklog: EPA official executable parity and `capped` localization

- Date: 2026-07-29
- Branch: `agent/bootstrap-project-foundation`
- Pull request: #1

## Objective

Resolve whether the GNU Fortran 14.2 `capped` difference is caused by inconsistent EPA expected outputs, a source-code problem, or compiler/build behavior.

## Work completed

1. Added `tools/probe_official_aermod_executable.py` for isolated, cross-platform execution and section-aware numeric comparison.
2. Added a Windows GitHub Actions evidence workflow.
3. Reused retained current fixtures instead of redownloading the 466 MB test archive.
4. Downloaded and hashed the official EPA executable archive.
5. Ran `capped` and `capped_nostd` with EPA's official Windows executable.
6. Verified zero canonical and numerical differences for both cases.
7. Inspected the official PE executable and found Intel Fortran runtime evidence.
8. Localized the GNU maximum relative difference to `STACK1C` second-highest 1-hour and 3-hour tables.
9. Compared `CAPPED.SUM` period-high values and showed that the 5.2613% value is not an overall maximum-concentration error.
10. Recompiled `prime.f`, `calc1.f`, `calc2.f`, `prise.f`, and `sigmas.f` individually at `-O0`; none changed the result.
11. Converted the executable evidence workflow to manual-only after the successful evidence run.

## Evidence

- official executable archive SHA256: `0ccf49702109637e665c8567891e365b4585a62a560faae35ce0194048683a24`;
- official executable SHA256: `599b491b021c7ec254ba3a1062386f287e56e54a0d3bb9b67cfa72275d6916da`;
- GitHub Actions run: `30411529300`;
- evidence artifact: `8708575372`;
- artifact digest: `7ef4ce9d2a9b26f43b399c4dc62740d57544f38734b96c7fef4a449c66865ba1`;
- `capped`: 10,615 expected/generated lines, zero canonical differences;
- `capped_nostd`: 4,848 expected/generated lines, zero canonical differences.

## Decision

The EPA executable and expected outputs define exact official release-fixture parity. Reproduced source builds are evaluated as a separate compiler/platform tier with explicit tolerances. The source will not be altered merely to force GNU output to match the Intel-linked official executable.

## Important nuance

The official binary contains Intel Fortran runtime evidence, but the exact Intel compiler frontend and version have not been proven. The EPA source package's `intel_ifx_aermod.bat` is consistent with the likely build family but is not treated as definitive provenance for the distributed binary.

## Next task

Begin the exact CO-pathway keyword schema, starting with control framing, titles, `MODELOPT`, averaging periods, pollutant/run controls, error/event files, repeatable `DEBUGOPT`, and MULTYEAR save/restart records.
