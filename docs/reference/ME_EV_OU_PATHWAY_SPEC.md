# AERMOD v26135 ME, EV, and OU pathway specification

This stage completes record-level source-verified coverage for meteorology, event, ordinary output, and event-output dispatch.

## Exact coverage

- ME: 23/23 `MECARD` records.
- EV: 5/5 `EVCARD` records.
- OU: 18/18 ordinary `OUCARD` records.
- event output: 4/4 `EV_OUCARD` records (`STARTING`, `EVENTOUT`, `FILEFORM`, `FINISHED`).

## Major semantics

ME covers meteorological files/stations, date selection, wind rotation/categories, SCIM controls, year allocation, and nine mutually exclusive turbulence filters. EV covers period/location pairing, event date envelopes, includes, and event completeness. OU covers report tables, every external output family, FIX/EXP control, header suppression, daily/design-value outputs, file-unit/name collision QA, and event-output selection.

## Evidence boundary

Complete specification means every executable dispatcher record has a machine-readable source/evidence record. It does not mean that the loss-aware parser, semantic project model, runner, output reader, or GIS layer has been implemented. Cataloged official-executable probes remain separate from executed evidence.
