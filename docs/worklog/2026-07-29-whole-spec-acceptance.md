# Worklog: v26135 whole-spec acceptance

- Date: 2026-07-29
- Branch: `agent/whole-spec-acceptance`
- Base: recovered official-specification `main`

## Objective

Replace separate pathway-specific verification outputs with one deterministic acceptance model and
make the remaining executable-behavior gate explicit before production syntax work.

## Implemented

- added `aermodkit.spec.acceptance` with immutable dispatcher, probe, and whole-spec acceptance models;
- normalized the seven source-exact-match reports despite their historical field-name differences;
- verified source count, bundled count, exact-set correspondence, pathway framing uniqueness,
  non-empty syntax forms, and required preservation-policy flags;
- treated ordinary `OUCARD` and event `EV_OUCARD` as separate dispatch modes;
- combined the three retained behavior-probe catalogs without rewriting their source evidence;
- added deterministic JSON and Markdown generation through
  `tools/generate_v26135_whole_spec_acceptance.py`;
- added integration tests against the repository evidence set;
- generated the retained acceptance evidence and updated handover state.

## Acceptance result

- dispatcher record-set gate: PASS;
- accepted dispatchers: 7/7;
- source-dispatched primary records: 138/138;
- behavior probes cataloged: 18;
- source-resolved probes: 1;
- official-executable pending probes: 17;
- production loss-aware syntax gate: NOT YET OPEN.

## Boundary

This batch does not claim production parsing, semantic mapping, executable orchestration, or final
behavioral coverage. It intentionally prevents a repeat of the earlier error where record inventory
completion was treated as permission to advance directly into semantic and runner layers.

## Next

Execute the high-priority parser-shaping behavior probes with the official v26135 Windows executable,
retain complete evidence bundles, and regenerate the acceptance report after each probe batch.
