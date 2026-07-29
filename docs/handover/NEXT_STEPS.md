# Next Steps

## Next major stage: whole-spec acceptance

1. Generate one deterministic whole-spec acceptance report covering CO, SO, RE, ME, EV, ordinary OU, and event-output mode.
2. Run the remaining targeted official-executable behavior probes for retained source/manual ambiguities.
3. Finish the clean-room third-party capability audit without copying implementations or treating third-party APIs as authoritative.
4. Freeze representative official and synthetic fixtures for unknown, future, development, include, continuation, nested-grid, line-ending, and malformed syntax.
5. Record the acceptance result, uncovered ambiguities, and explicit parser-entry criteria in the worklog and handover.

## After whole-spec acceptance: loss-aware syntax

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
