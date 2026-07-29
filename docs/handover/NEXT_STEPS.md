# Next Steps

## Immediate stage: targeted official-executable behavior probes

1. Continue using the retained official v26135 fixture snapshot and EPA Windows executable workflow for the 14 pending questions.
2. The next parser-shaping batch should prioritize:
   - incomplete `O3VALUES` and `NOX_VALS` temporal vectors;
   - event-output `FILEFORM` behavior under `DFAULT`;
   - `SO-VBARRIER-RANGE-01` boundary inclusivity and same-side `W375` behavior;
   - the remaining ALPHA/DFAULT dependency matrix where source evidence alone is insufficient.
3. For every probe, retain the exact materialized deck hash, executable/archive SHA-256, stdout/stderr, main output, error file, diagnostic codes, return code, positive control where needed, and an interpretation boundary.
4. Update the originating probe catalog entry to an explicit final state; do not infer general behavior beyond the tested form.
5. Regenerate `v26135-whole-spec-acceptance.json` after each reviewed probe batch.
6. Keep paired positive controls for scoped repeatability, fallback behavior, and option-dependent forms.
7. Finish the clean-room third-party capability audit without copying implementations or treating third-party APIs as authoritative.
8. Freeze representative official and synthetic fixtures for unknown, future, development, include, continuation, nested-grid, line-ending, and malformed syntax.

## Completed in official batch 1

- `SO-SWPOINT-01`;
- valid one- and two-barrier forms from `SO-VBARRIER-01`;
- same-sector versus distinct-sector `OZONEFIL` behavior;
- same-sector versus distinct-sector `NOX_FILE` behavior.

The refined gate contains 19 questions: 4 executed, 1 source-resolved, and 14 pending.

## Parser-entry gate

Loss-aware syntax implementation may begin only when:

- the record-set gate remains 7/7 and 138/138;
- all high-priority parser-shaping executable probes have final retained evidence;
- unresolved medium-priority probes have explicit preservation-safe handling and documented deferral;
- fixture hashes and expected diagnostics are frozen;
- no semantic model or canonical formatter is allowed to define the concrete syntax representation.

## After the probe gate: loss-aware syntax

1. Implement tokens with exact source spans and original text.
2. Implement a loss-aware lexer that preserves comments, blank lines, original case, whitespace, tabs, quoting, and original line endings.
3. Implement an immutable concrete syntax tree for pathway boundaries, known records, unknown records, unknown fields, include boundaries, continuations, and nested grid blocks.
4. Add a format-preserving writer whose default output reproduces original bytes when no edits are made.
5. Add byte-exact and normalized round-trip tests across the frozen fixture set.
6. Keep any canonical formatter separate from the format-preserving writer.

## Only after syntax round-trip invariants are stable

- implement typed semantic project models and cross-pathway validation;
- review the archived PR #2 prototype only for independently useful requirements or tests;
- add runner/executable management and isolated workspaces;
- add output parsing and provenance-aware result objects;
- add GIS integrations only after the syntax, semantic, and execution layers are stable.
