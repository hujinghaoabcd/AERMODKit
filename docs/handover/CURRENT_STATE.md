# Current State

- Updated: 2026-07-30
- Active development branch: `agent/official-behavior-probes-batch4`
- Active pull request: #13, pending final-head validation and merge
- Official behavior-probe batch 3 PR: #11, merged
- Batch 3 merge commit: `cab11308b022fe648dcb3bd5ba00bc7e758bc19a`
- Official behavior-probe batch 2 PR: #9, merged
- Batch 2 merge commit: `279b61160412a8073632d31156f897cd6edcee4a`
- Official behavior-probe batch 1 PR: #7, merged
- Batch 1 merge commit: `4e6e92ddd86420144438a4e6d2eb0b77b3db33ab`
- Package version: `0.0.1.dev0`
- Development phase: Phase 0 record-level specification accepted; official behavior-probe gate partially complete

## Authoritative mainline

The source-verified official-specification line remains authoritative. The former PR #2 parallel prototype is retained only at `archive/pr2-parallel-prototype-20260729` and must not be used as a development base.

## Whole-spec record-set acceptance

All seven dispatch modes and all 138 source-dispatched primary records remain accepted:

- CO 39/39;
- SO 40/40;
- RE 9/9;
- ME 23/23;
- EV 5/5;
- ordinary OU 18/18;
- event-output OU 4/4.

## Official behavior probes

### Batches 1–3

Retained evidence covers SWPOINT, VBARRIER, sector O3/NOx file repetition, temporal vectors, event-output FILEFORM, the ALPHA/DFAULT matrix, ARCFTOPT/aircraft dependencies, and MAXDCONT forms.

### Batch 4

Reviewed evidence:

- workflow run: `30479954822`;
- reviewed head: `215764df489d623c3433e6baa0a6b301b0ab3f68`;
- artifact ID: `8735323902`;
- artifact digest: `sha256:cc3cb39b85bac2429e11deda087853e3a5a89852f0574a27968f1393012378f1`;
- artifact size: `338,627,341` bytes;
- cases: 40;
- accepted/rejected/indeterminate: 29/11/0;
- expectations met: 40/40.

Resolved outcomes:

- PLATFORM accepts the exact payload and trailing numeric fields; trailing numeric values are preservation-only;
- PLATFORM text extras, non-point use, duplicate source assignment, and PRIME conflict map to E208/E631/E632/E633;
- repeated static BACKGRND profiles map to E231 and a second HOURLY file to E168/E501;
- HOURLY and non-HOURLY BACKGRND coexist in either order, with HOURLY primary and static fallback;
- active GRIDCART/GRIDPOLR blocks accept implicit, NetID-only, and fully explicit secondary lines;
- a different active-block NetID produces E170;
- DISCCART/DISCPOLR inactive terrain/flag fields are accepted with W229 and ignored semantically;
- missing fields required by active options use W228.

Evidence is retained in:

- `reference/probes/v26135/batch4/result.json`;
- `reference/probes/v26135/batch4/case-evidence.csv`;
- `docs/reference/V26135_OFFICIAL_BEHAVIOR_PROBES_BATCH4.md`.

## Retained behavior-probe gate

The normalized inventory contains 19 questions:

- executed: 14;
- source-resolved: 1;
- official-executable pending: 4.

Remaining:

- `ME-FORMAT-LEGACY`;
- `ME-SCIM-6FIELD`;
- `EV-PAIRING`;
- `OU-FILE-CONFLICT`.

The behavior gate remains incomplete. Production lexer/CST work is still forbidden until Batch 5, clean-room audit, fixture freeze, and parser-entry ADR are complete.

## Not yet implemented

Production lexer/parser, immutable CST, format-preserving writer, semantic project model, runner, output parser, and GIS layers remain pending.

## Validation status

- reviewed Batch 4 run `30479954822` passed all 40 cases;
- reviewed-head CI `30479955343` passed all nine jobs;
- final PR head still requires full CI and Batch 4 official workflow before merge.
