# Current State

- Updated: 2026-07-30
- Active branch: `main`
- Official behavior-probe batch 4 PR: #13, merged
- Batch 4 merge commit: `4887bef7629922b076ddb0adcf5ca7e30aaea62a`
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

- reviewed workflow run: `30479954822`;
- reviewed head: `215764df489d623c3433e6baa0a6b301b0ab3f68`;
- reviewed artifact ID: `8735323902`;
- reviewed artifact digest: `sha256:cc3cb39b85bac2429e11deda087853e3a5a89852f0574a27968f1393012378f1`;
- cases: 40;
- accepted/rejected/indeterminate: 29/11/0;
- expectations met: 40/40.

Final PR head `68e0ed8dc52d666cdc1b0f7db1e59b905fb7d7ac` independently passed:

- full nine-job CI: `30483264010`;
- official Batch 4 workflow: `30483264020`.

Final-head artifact:

- artifact ID: `8736670776`;
- digest: `sha256:2db8897f2e01520cd7f81d17dc1e4429e0862b6d7000f05443f00f84f073a898`;
- size: `338,627,401` bytes;
- expiration: `2026-08-28T19:14:15Z`.

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

## Workflow hygiene

The Batch 4 workflow trigger is restricted to Batch 4-specific manifests, source searches, tests, and its own workflow file. Later batches may reuse the generic harness without rerunning Batch 4 solely because shared tools changed.

## Not yet implemented

Production lexer/parser, immutable CST, format-preserving writer, semantic project model, runner, output parser, and GIS layers remain pending.

## Validation status

- 53/53 official decks executed in the established evidence workflow;
- all seven dispatcher exact-set reports pass;
- final PR #13 head passed CI `30483264010` and official workflow `30483264020`;
- PR #13 merged to `main` as `4887bef7629922b076ddb0adcf5ca7e30aaea62a`.
