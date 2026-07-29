# AERMOD v26135 capability inventory

## Purpose

This directory is an evidence-tracked inventory, not a blanket implementation claim. It prevents AERMODKit from inheriting omissions, simplifications or stale version assumptions from other wrappers.

## Files

- `../epa/v26135/manifest.yaml` — official asset, component-version and parity-evidence manifest;
- `v26135-keywords.csv` — broad runstream inventory seed;
- `v26135-keyword-status-overrides.csv` — authoritative promotion layer for completed schema batches;
- `v26135-co-batch1-evidence.csv` — evidence for 14 foundational CO records;
- `v26135-co-batch2-evidence.csv` — evidence for 10 decay, urban/receptor, ozone and NO2-ratio records;
- source-type, output and source-code mapping inventories;
- `../epa/v26135/regression/` — official fixture and compiler-tier parity evidence.

## Current state

Official source, executable, sample-run and test-case assets have been independently materialized and hashed through auditable workflows. Large binaries are indexed rather than committed. CO batches 1-2 currently promote 24 records; the remaining inventory is not implementation-ready.

The retained local October 2023 User's Guide is historical only. Current v26135 manuals, source, executable behavior and fixtures take precedence. AERMAP remains 24142 while AERMOD/AERMET are 26135.

## Promotion rule

A record is promoted only after current authoritative/manual evidence, exact source handling, argument/default/validation rules, regulatory-status boundaries, fixture evidence or documented absence, bundled schema coverage, tests and loss-aware preservation behavior are recorded. The override file remains authoritative until a deterministic inventory generator consolidates the seed and promotions.
