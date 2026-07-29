# AERMOD v26135 capability inventory

## Purpose

This directory is an evidence-tracked inventory, not a blanket implementation claim. It prevents AERMODKit from inheriting omissions, simplifications or stale version assumptions from other wrappers.

## Files

- `../epa/v26135/manifest.yaml` — official asset, component-version and parity-evidence manifest;
- `v26135-keywords.csv` — broad runstream inventory seed;
- `v26135-keyword-status-overrides.csv` — authoritative promotion layer for completed records;
- `v26135-co-batch1-evidence.csv` and `v26135-co-batch2-evidence.csv` — earlier CO evidence sets;
- `v26135-co-completion-evidence.csv` — evidence for the final 15 CO records;
- `v26135-co-source-exact-match.json` — machine-generated 39/39 COCARD exact-set result;
- `v26135-co-official-behavior-probes.json` — focused probe catalog for retained guide/source discrepancies;
- source-type, output and source-code mapping inventories;
- `../epa/v26135/regression/` — official fixture and compiler-tier parity evidence.

## Current state

Official source, executable, sample-run and test-case assets have been independently materialized and hashed through auditable workflows. Large binaries are indexed rather than committed.

The CO pathway now has complete primary-record specification coverage: all 39 records dispatched by `COCARD` in `coset.f` resolve to bundled source-verified records. This does not mean the production parser, semantic model or runner is implemented, and it does not convert ALPHA, legacy or non-regulatory options into regulatory options.

## Promotion rule

A record is promoted only after current authoritative/manual evidence, exact source handling, argument/default/validation rules, regulatory-status boundaries, fixture evidence or documented absence, bundled schema coverage, tests and loss-aware preservation behavior are recorded. The override file remains authoritative until a deterministic inventory generator consolidates the seed and promotions.
