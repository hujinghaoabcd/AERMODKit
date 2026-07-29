# Worklog: official-specification mainline recovery

- Date: 2026-07-29
- Recovery branch: `agent/recover-official-spec-mainline`
- Recovery PR: #3
- Current-main parent: `83eed3e7a374f9e1b7a4ef30994b1854ec660e8b`
- Official-spec parent: `0739b9104b3784ab80aa980a00212404d24f29bc`
- Two-parent recovery commit: `6959ecee34c0e9b69cecb56030018ca1ba53ac24`
- Final main merge: `e9a4ebb453ab855512cd4c39be1b227df53689ea`
- Recovery CI run: `30441812294`, 9/9 jobs passed

## Trigger

A review of the original conversation and the preserved SO/RE handover package showed that the
recent PR #2 work had been developed from the initial repository state rather than from the
60-commit official-specification branch in PR #1.

## Findings

- PR #1 contained complete source-verified record sets for CO, SO, RE, ME, EV, ordinary OU, and
  event-output mode, plus official assets, executable parity, fixtures, CI, ADRs, and handover.
- PR #2 contained a smaller manual-derived registry and moved into parser, semantic, and runner
  design before the accepted prerequisites were complete.
- The parallel registry omitted executable-recognized `VBARRIER` and misclassified `EVENTOUT`
  as an ordinary OU keyword rather than a distinct event-output dispatch mode.
- The new Progress 03 branch had no commits, so no additional work needed to be discarded.

## Recovery method

1. Preserved the PR #2 merge tree at `archive/pr2-parallel-prototype-20260729`.
2. Created `agent/recover-official-spec-mainline` from the former `main` head.
3. Built a two-parent merge commit whose working tree is based on the complete PR #1 head.
4. Added ADR 0005 and this recovery record.
5. Opened PR #3 and required the ordinary cross-platform CI matrix.
6. Confirmed all nine jobs passed Ruff, strict mypy, and pytest.
7. Merged PR #3 with the merge method, not squash or rebase, preserving the full PR #1 ancestry.
8. Confirmed GitHub automatically marked PR #1 merged because its head became reachable from `main`.

## Final state

- `main` now contains the complete official-specification and regression tree.
- PR #1's 60 commits remain in repository ancestry.
- PR #2 remains recoverable through the archive branch.
- no force push or history rewrite occurred.
- active development returns to Phase 0 acceptance and loss-aware syntax preparation.

## Next work

Run deterministic whole-spec acceptance, complete the remaining targeted official-executable
behavior probes, finish the clean-room third-party audit, and then implement the loss-aware
lexer/CST/format-preserving writer before any semantic model or runner expansion.
