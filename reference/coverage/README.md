# AERMOD v26135 capability inventory

## Purpose

This directory is an evidence-tracked inventory, not an implementation claim. It exists to prevent AERMODKit from inheriting the omissions, simplifications, or version assumptions of commercial or third-party wrappers.

## Files

- `../epa/v26135/manifest.yaml` — official asset and component-version manifest;
- `v26135-keywords.csv` — current top-level and selected secondary runstream records;
- `v26135-source-types.csv` — official source-type vocabulary plus separately marked special/option-applied cases;
- `v26135-outputs.csv` — output control and parser-priority seed;
- `v26135-source-code-map.csv` — evidence-ranked source mapping seed.

## Evidence statuses

- `confirmed-current`: observed in the current EPA v26135 release pages or quick reference;
- `confirmed-release-note`: explicitly described in the v26135 transmittal memorandum or Model Change Bulletin 19;
- `provisional-file-level`: inferred only at a Fortran file/module level and must be verified against the source archive;
- `needs-source-verification`: potentially special or ambiguous behavior that must not yet become a public domain class.

## Important limitations

1. The v26135 source ZIP and official sample/test ZIPs were not materialized in the current runtime, so no SHA256 values or line-level Fortran mappings are available.
2. The current inventory is a broad official quick-reference seed. Every argument signature, repeatability rule, default, range, dependency, regulatory status, and error behavior still requires detailed User Guide and source-code verification.
3. The locally retained `aermod_userguide.pdf` is the October 2023 guide. It is useful as historical material only and is not the current v26135 specification.
4. AERMAP remains version 24142 even though AERMOD/AERMET and several support programs are 26135.
5. Unknown or unsupported records must be preserved by the future syntax layer rather than discarded.

## Completion rule

A row may be promoted to implementation-ready only after it has:

- a current official manual reference;
- a source-code handler or observed executable-behavior reference;
- argument and repeatability rules;
- at least one official sample/test fixture or a documented reason none exists;
- a planned or implemented regression test.
