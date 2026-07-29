# Next Steps

## Immediate stage: Batch 5 official behavior probes

Four executable questions remain:

1. `ME-FORMAT-LEGACY`
   - non-FREE `SURFFILE` and `PROFFILE` formats;
   - executable warnings/errors;
   - preservation of legacy format fields.
2. `ME-SCIM-6FIELD`
   - six-field `SCIMBYHR`;
   - numeric wet-scimming pair versus filename disambiguation.
3. `EV-PAIRING`
   - multiple `EVENTLOC` records per event;
   - EVENTPER/EVENTLOC count and FINISHED checks.
4. `OU-FILE-CONFLICT`
   - same filename or unit across output families;
   - path normalization and conflict diagnostics.

`ME-TURB-DUP` is already source-resolved.

Each probe must retain positive controls, materialized deck hashes, executable/source hashes, stdout/stderr, main/error outputs, diagnostics, exact source contexts, and an interpretation boundary.

## Completed official behavior evidence

### Batch 1

- `SO-SWPOINT-01`;
- valid forms from `SO-VBARRIER-01`;
- sector-scoped OZONEFIL and NOX_FILE repetition.

### Batch 2

- `temporal_vector_incomplete`;
- `SO-VBARRIER-RANGE-01`;
- `OU-EVENT-FILEFORM`.

### Batch 3

- `alpha_dependency_matrix`;
- `arcftopt_repeat_extra_fields`;
- `OU-MAXDCONT-FORMS`.

### Batch 4

- `SO-PLATFORM-01`;
- `SO-BACKGRND-01`;
- `RE-GRID-ID-01`;
- `RE-DISC-EXTRA-01`.

Current inventory:

```text
total                        = 19
executed                     = 14
source_resolved              = 1
official_executable_pending  = 4
```

## Parser-entry preparation after Batch 5

1. Complete the clean-room third-party capability audit without copying implementation details or treating third-party APIs as authoritative.
2. Freeze official and synthetic syntax fixtures for:
   - comments and blank lines;
   - mixed case;
   - tabs and irregular spaces;
   - quoted paths;
   - LF and CRLF;
   - unknown, future, and development records;
   - `INCLUDED` boundaries;
   - continuations;
   - nested GRIDCART/GRIDPOLR;
   - malformed records and incomplete blocks;
   - event-output submode.
3. Add the preservation-safe parser-entry ADR.
4. Freeze fixture hashes and expected diagnostics.
5. Regenerate whole-spec acceptance and require all parser-entry gates to pass.

## Loss-aware syntax stage

Only after the gate opens:

1. exact-span tokens;
2. a lexer preserving all source text and line endings;
3. immutable CST nodes for known, unknown, malformed, included, continued, and nested structures;
4. byte-exact no-edit writer;
5. separately opt-in canonical formatter;
6. round-trip tests across the frozen fixture set.

## Later stages

After syntax invariants are stable:

- typed semantic project model and cross-pathway validation;
- isolated executable runner and provenance;
- output parsers and result objects;
- GIS integration and public API.
