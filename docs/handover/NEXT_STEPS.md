# Next Steps

## Immediate stage: targeted official-executable behavior probes

1. Continue using the retained official v26135 fixture snapshot and EPA Windows executable workflow for the 11 pending questions.
2. The next parser-shaping batch should prioritize:
   - the remaining ALPHA/DFAULT dependency matrix for `GDSEASON`, `GASDEPDF`, `GDLANUSE`, `GASDEPVD`, `LOW_WIND`, `AWMADWNW`, `ORD_DWNW` and `ARCFTOPT`;
   - repeated `ARCFTOPT` and extra-field behavior;
   - `OU-MAXDCONT-FORMS` with executable fixtures for THRESH, secondary-rank signatures and trailing units.
3. A following medium-priority batch should cover `SO-PLATFORM-01`, `SO-BACKGRND-01`, `RE-GRID-ID-01`, `RE-DISC-EXTRA-01`, `ME-FORMAT-LEGACY`, `ME-SCIM-6FIELD`, `EV-PAIRING` and `OU-FILE-CONFLICT`.
4. For every probe, retain exact deck hashes, executable/archive SHA-256, stdout/stderr, main/error outputs, diagnostic codes, positive controls, official source contexts and an interpretation boundary.
5. Update each originating probe catalog entry explicitly; do not infer general behavior beyond the executable cases and retained source branch.
6. Regenerate `v26135-whole-spec-acceptance.json` after each reviewed batch.
7. Finish the clean-room third-party capability audit without copying implementations or treating third-party APIs as authoritative.
8. Freeze representative official and synthetic fixtures for unknown, future, development, include, continuation, nested-grid, line-ending and malformed syntax.

## Completed official behavior evidence

### Batch 1

- `SO-SWPOINT-01`;
- valid one- and two-barrier forms from `SO-VBARRIER-01`;
- same-sector versus distinct-sector `OZONEFIL` behavior;
- same-sector versus distinct-sector `NOX_FILE` behavior.

### Batch 2

- `temporal_vector_incomplete`;
- `SO-VBARRIER-RANGE-01`;
- `OU-EVENT-FILEFORM`.

The refined gate contains 19 questions: 7 executed, 1 source-resolved and 11 pending.

## Parser-entry gate

Loss-aware syntax implementation may begin only when:

- the record-set gate remains 7/7 and 138/138;
- all high-priority parser-shaping executable probes have final retained evidence;
- unresolved medium-priority probes have explicit preservation-safe handling and documented deferral;
- fixture hashes and expected diagnostics are frozen;
- no semantic model or canonical formatter is allowed to define the concrete syntax representation.

## After the probe gate: loss-aware syntax

1. Implement tokens with exact source spans and original text.
2. Implement a loss-aware lexer that preserves comments, blank lines, original case, whitespace, tabs, quoting and original line endings.
3. Implement an immutable concrete syntax tree for pathway boundaries, known records, unknown records, unknown fields, include boundaries, continuations and nested grid blocks.
4. Add a format-preserving writer whose default output reproduces original bytes when no edits are made.
5. Add byte-exact and normalized round-trip tests across the frozen fixture set.
6. Keep any canonical formatter separate from the format-preserving writer.

## Only after syntax round-trip invariants are stable

- implement typed semantic project models and cross-pathway validation;
- review the archived PR #2 prototype only for independently useful requirements or tests;
- add runner/executable management and isolated workspaces;
- add output parsing and provenance-aware result objects;
- add GIS integrations only after the syntax, semantic and execution layers are stable.
