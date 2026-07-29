# Next Steps

## Immediate major stage: full-spec acceptance and loss-aware syntax implementation

1. Run the remaining official-executable behavior probes for retained source/manual ambiguities across all pathways.
2. Finish the clean-room third-party capability audit without copying implementation.
3. Generate a deterministic whole-spec acceptance report covering CO, SO, RE, ME, EV, ordinary OU, and event-output mode.
4. Select representative fixtures for unknown, future, development, include, continuation, and nested-grid syntax.
5. Implement the loss-aware lexer and concrete syntax tree while preserving comments, blank lines, original case, spacing, unknown records and fields, include boundaries, and nested grid blocks.
6. Add a format-preserving writer and byte/normalized round-trip tests before introducing semantic project models.

## After syntax round-trip invariants are stable

- implement typed semantic project models and cross-pathway validation;
- add runner/executable management and isolated workspaces;
- add output parsing and provenance-aware result objects;
- add GIS integrations only after the syntax, semantic, and execution layers are stable.
