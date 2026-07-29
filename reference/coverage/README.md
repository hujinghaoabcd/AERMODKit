# AERMOD v26135 capability inventory

## Purpose

This directory is an evidence-tracked inventory, not a blanket implementation claim. It prevents AERMODKit from inheriting omissions, simplifications, or stale version assumptions from other wrappers.

## Files

- `../epa/v26135/manifest.yaml` — official asset, component-version, and parity-evidence manifest;
- `v26135-keyword-dispatch.csv` — deterministic primary dispatcher inventory for all pathways, including framing records;
- `v26135-keywords.csv` — broad runstream inventory with completed SO/RE promotions consolidated;
- `v26135-keyword-status-overrides.csv` — authoritative CO promotion history;
- `v26135-co-*-evidence.csv` and `v26135-co-source-exact-match.json` — complete CO evidence;
- `v26135-so-re-completion-evidence.csv` — source/manual/fixture evidence for all 49 SO+RE primary records;
- `v26135-so-source-exact-match.json` and `v26135-re-source-exact-match.json` — exact dispatcher/specification results;
- `v26135-so-re-keyword-dispatch.csv` — handler-level SO/RE source map;
- `v26135-so-re-official-behavior-probes.json` — focused unresolved behavior probe catalog;
- `v26135-source-types.csv` — 13 source-recognized LOCATION types and exact SRCPARAM summaries;
- output and source-code mapping inventories;
- `../epa/v26135/regression/` — official fixture and compiler-tier parity evidence.

## Current state

Official source, executable, sample-run, and test-case assets have been independently materialized and hashed through auditable workflows. Large binaries are indexed rather than committed.

Complete record-level pathway coverage currently includes:

- CO: 39/39 primary `COCARD` records;
- SO: 40/40 primary `SOCARD` records;
- RE: 9/9 primary `RECARD` records.

The deterministic dispatcher inventory corrects the earlier omission of SO `PLATFORM` and `VBARRIER`. `SWPOINT` is recorded as source-recognized ALPHA/development syntax with an explicit current-manual-list omission. Recognition does not imply regulatory approval.

This does not mean the production parser, semantic model, runner, output parser, or GIS layer is implemented.

## Promotion rule

A record is promoted only after current authoritative/manual evidence, exact source handling, argument/default/validation rules, regulatory-status boundaries, fixture evidence or documented absence, bundled schema coverage, tests, and loss-aware preservation behavior are recorded.
