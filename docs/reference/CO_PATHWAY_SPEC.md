# AERMOD v26135 complete CO pathway specification

## Status

The bundled CO pathway specification now covers all **39 primary records** dispatched by `COCARD` in EPA AERMOD v26135. The loader composes ten immutable JSON fragments and verifies that the aggregate record order contains no duplicates.

This is complete **record-specification coverage**, not a claim that a production parser, writer, runner, or regulatory-use workflow already exists.

## Coverage

- batches 1–2: 24 framing, model/run, restart, debug, decay, urban, static ozone, and NO2-ratio records;
- unified completion stage: 15 remaining records for temporal ozone, ambient NOx, gas deposition, low wind, PRIME research options, and aircraft plume rise;
- `MODELOPT`: all 40 source-recognized tokens now carry explicit guide/status classifications, including legacy source/guide discrepancies.

## Completion invariant

`tools/verify_complete_co_specification.py` extracts all `KEYWRD .EQ.` branches from `coset.f` and requires an exact set match with the bundled schema. Current expected result: 39 source records, 39 bundled records, no missing or extra records.

## Important retained evidence boundaries

1. `OZONEFIL` and `NOX_FILE`: current guide wording and source sector-index behavior are both retained; same-sector repeat behavior remains an official-executable probe.
2. `ARCFTOPT`: guide says non-repeatable, while the dispatcher does not issue the standard repeat error and only assigns the airport ID for exactly one payload field.
3. `ROMBERG` and `TOXICS`: source-recognized legacy tokens are preserved but are not advertised as current guide options.
4. v26135 includes a `BETA` family marker but no actual BETA options.
5. Source recognition never implies regulatory approval.

## Loss-aware boundary

Comments, blank lines, original case, spacing, repeat-value syntax, path quoting, unknown records, future tokens, and uninspected extra fields must survive syntax parsing. Semantic validation may diagnose them but must not silently discard them.
