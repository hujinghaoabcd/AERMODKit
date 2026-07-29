# AERMOD v26135 capability inventory

## Purpose

This directory is an evidence-tracked inventory, not a blanket implementation claim. It prevents AERMODKit from inheriting omissions, simplifications, or stale version assumptions from other wrappers.

## Files

- `../epa/v26135/manifest.yaml` — official asset, component-version, and parity-evidence manifest;
- `v26135-keyword-dispatch.csv` — deterministic primary dispatcher inventory for all pathways, including framing records;
- `v26135-keywords.csv` — broad runstream inventory with completed pathway promotions consolidated;
- `v26135-keyword-status-overrides.csv` — authoritative CO promotion history;
- `v26135-co-*-evidence.csv` and `v26135-co-source-exact-match.json` — complete CO evidence;
- `v26135-so-re-completion-evidence.csv` — source/manual/fixture evidence for all 49 SO+RE primary records;
- `v26135-so-source-exact-match.json` and `v26135-re-source-exact-match.json` — exact SO/RE dispatcher results;
- `v26135-so-re-keyword-dispatch.csv` and `v26135-so-re-official-behavior-probes.json` — SO/RE handler map and probe catalog;
- `v26135-me-ev-ou-completion-evidence.csv` — source/manual/fixture evidence for ME, EV, ordinary OU, and event-output records;
- `v26135-me-source-exact-match.json`, `v26135-ev-source-exact-match.json`, `v26135-ou-source-exact-match.json`, and `v26135-event-output-source-exact-match.json` — exact final-pathway dispatcher results;
- `v26135-me-ev-ou-keyword-dispatch.csv`, `v26135-me-ev-ou-status-overrides.csv`, and `v26135-me-ev-ou-official-behavior-probes.json` — final-pathway dispatch, promotion, and probe evidence;
- `v26135-source-types.csv` — 13 source-recognized `LOCATION` types and exact `SRCPARAM` summaries;
- `v26135-outputs.csv` — source-verified ordinary and event output-family inventory;
- `../epa/v26135/regression/` — official fixture and compiler-tier parity evidence.

## Current state

Official source, executable, sample-run, and test-case assets have been independently materialized and hashed through auditable workflows. Large binaries are indexed rather than committed.

Complete record-level dispatcher coverage now includes:

- CO: 39/39 primary `COCARD` records;
- SO: 40/40 primary `SOCARD` records;
- RE: 9/9 primary `RECARD` records;
- ME: 23/23 primary `MECARD` records;
- EV: 5/5 primary `EVCARD` records;
- OU: 18/18 ordinary `OUCARD` records;
- event output: 4/4 `EV_OUCARD` records.

The deterministic dispatcher inventory corrects earlier SO omissions for `PLATFORM` and `VBARRIER`. `SWPOINT` remains source-recognized ALPHA/development syntax with an explicit current-manual-list omission. Recognition does not imply regulatory approval.

Ordinary output and event output are modeled separately because `EVENTOUT` belongs to `EV_OUCARD`, not ordinary `OUCARD`.

This does not mean the production parser, semantic model, runner, output parser, or GIS layer is implemented.

## Promotion rule

A record is promoted only after current authoritative/manual evidence, exact source handling, argument/default/validation rules, regulatory-status boundaries, fixture evidence or documented absence, bundled schema coverage, tests, and loss-aware preservation behavior are recorded.
