# Worklog: official-specification mainline recovery

- Date: 2026-07-29
- Recovery branch: `agent/recover-official-spec-mainline`
- Current-main parent: `83eed3e7a374f9e1b7a4ef30994b1854ec660e8b`
- Official-spec parent: `0739b9104b3784ab80aa980a00212404d24f29bc`

## Trigger

A review of the original conversation and the preserved SO/RE handover package showed that the
recent PR #2 work had been developed from the initial repository state rather than from the
60-commit official-specification branch in PR #1.

## Findings

- PR #1 contains complete source-verified record sets for CO, SO, RE, ME, EV, ordinary OU, and
  event-output mode, plus official assets, executable parity, fixtures, CI, ADRs, and handover.
- PR #2 contained a smaller manual-derived registry and moved into parser, semantic, and runner
  design before the accepted prerequisites were complete.
- The parallel registry omitted executable-recognized `VBARRIER` and misclassified `EVENTOUT`
  as an ordinary OU keyword rather than a distinct event-output dispatch mode.
- The new Progress 03 branch had no commits, so no additional work needed to be discarded.

## Recovery method

1. Preserved the PR #2 merge tree at `archive/pr2-parallel-prototype-20260729`.
2. Created `agent/recover-official-spec-mainline` from the current `main` head.
3. Built a two-parent merge commit whose tree is based on the complete PR #1 head.
4. Added ADR 0005 and this recovery record.
5. Restored the Phase 0 handover and next-step sequence.

## Validation required before merge

- ordinary cross-platform CI must pass on the recovery PR;
- the recovery diff must contain the PR #1 specification/reference/test tree and remove the
  parallel prototype modules from the active tree;
- `main` must remain recoverable through the archive branch;
- no force push is permitted.

## Next work after recovery

Run deterministic whole-spec acceptance, complete the remaining targeted official-executable
behavior probes, finish the clean-room third-party audit, and then implement the loss-aware
lexer/CST/format-preserving writer before any semantic model or runner expansion.
