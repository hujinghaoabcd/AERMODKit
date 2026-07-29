# Next Steps

## Immediate stage: remaining official-executable behavior probes

Eight retained questions remain pending.

### Batch 4 — SO and RE behavior

Prioritize:

- `SO-PLATFORM-01`: trailing-field acceptance, ignore, or rejection;
- `SO-BACKGRND-01`: duplicate global/sector profiles, precedence, and hourly/static conflicts;
- `RE-GRID-ID-01`: omitted NetID continuation and active-grid inheritance;
- `RE-DISC-EXTRA-01`: terrain/flag fields supplied under inactive options.

Every probe must retain positive controls, exact deck hashes, executable/source archive hashes,
stdout/stderr, main/error outputs, diagnostics, source contexts, and an interpretation boundary.

### Batch 5 — ME, EV, and OU behavior

Then resolve:

- `ME-FORMAT-LEGACY`;
- `ME-SCIM-6FIELD`;
- `EV-PAIRING`;
- `OU-FILE-CONFLICT`.

`ME-TURB-DUP` is already source-resolved and remains part of the final gate accounting.

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

### Batch 3

- `alpha_dependency_matrix`;
- `arcftopt_repeat_extra_fields`;
- `OU-MAXDCONT-FORMS`.

The normalized inventory is now 19 total, 10 executed, 1 source-resolved, and 8 pending.

## Parser-entry preparation after Batch 5

1. Complete the clean-room third-party capability audit without copying implementations or treating third-party APIs as authoritative.
2. Freeze representative official and synthetic fixtures for comments, blank lines, mixed case, tabs, quoting, LF/CRLF, unknown/future/development records, include boundaries, continuations, nested grids, malformed records, incomplete blocks, and event-output submode.
3. Add a preservation-safe ADR for any intentionally deferred behavior.
4. Freeze fixture hashes and expected diagnostics.
5. Regenerate whole-spec acceptance and require:

```text
record_set_gate_passed = true
behavior_probe_gate_passed = true
fixtures_frozen = true
clean_room_audit_complete = true
syntax_implementation_ready = true
```

## Loss-aware syntax stage

Only after the parser-entry gate opens:

1. implement tokens with exact byte/character spans and original text;
2. implement a lexer preserving comments, blank lines, whitespace, tabs, quoting, original case, numeric spelling, and line endings;
3. implement an immutable CST for pathway boundaries, known/unknown/malformed records, unknown fields, include boundaries, continuations, nested grids, and event-output blocks;
4. implement a format-preserving writer whose no-edit output is byte-identical;
5. keep canonical formatting separate from preservation writing;
6. require byte-exact and normalized round-trip tests across the frozen fixture set.

## Later stages

Only after syntax invariants are stable:

- typed semantic project models and cross-pathway validation;
- isolated executable runner and provenance;
- output parsers and result objects;
- GIS integrations and public API.
