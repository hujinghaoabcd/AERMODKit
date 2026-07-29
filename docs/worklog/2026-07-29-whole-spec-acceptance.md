# Worklog: v26135 whole-spec acceptance

- Date: 2026-07-29
- Development branch: `agent/whole-spec-acceptance`
- Pull request: #5, merged
- Merge commit: `cbd721b80c5642d5fcc60ec2f77fe70095e9a79b`
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

## Validation and publication

- initial CI exposed two Ruff `SIM300` set-comparison findings and one import-spacing finding;
- all findings were corrected on the branch without weakening lint configuration;
- final CI run `30443993754` passed all nine Ubuntu/Windows/macOS × Python 3.11/3.12/3.13 jobs;
- every final job passed Ruff, strict mypy, pytest, and coverage;
- PR #5 was merged with the verified head `deb7f2bd8d02bae7142ae1bba7e2655f2fda4ecb`.

## Boundary

This batch does not claim production parsing, semantic mapping, executable orchestration, or final
behavioral coverage. It intentionally prevents a repeat of the earlier error where record inventory
completion was treated as permission to advance directly into semantic and runner layers.

## Next

Execute the high-priority parser-shaping behavior probes with the official v26135 Windows executable,
retain complete evidence bundles, and regenerate the acceptance report after each probe batch.
