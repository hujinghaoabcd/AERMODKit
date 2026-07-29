# ADR 0005: Recover the official-specification mainline

- Status: accepted
- Date: 2026-07-29

## Context

A parallel implementation was created from the repository's initial `main` commit while the
source-verified Phase 0 work remained in PR #1. That parallel branch introduced a simplified
keyword registry, parser, writer, semantic projection, and validation layer, then was merged as
PR #2. It did not include the official asset inventory, executable parity evidence, complete
source-dispatch specifications, event-output submode, cross-platform CI, or durable handover
history already present in PR #1.

The two lines diverged from the same initial commit. Continuing on the smaller parallel line
would invert the accepted development order by placing semantic models and runner work before
whole-spec acceptance and format-preserving syntax invariants.

## Decision

The official-specification branch at
`0739b9104b3784ab80aa980a00212404d24f29bc` is restored as the authoritative project tree.
The recovery commit has two parents: the current `main` commit produced by PR #2 and the complete
PR #1 head. This preserves both histories without force-pushing or deleting the parallel work.

The PR #2 tree is retained at `archive/pr2-parallel-prototype-20260729` for later clean-room
salvage review. No code from that prototype is automatically promoted.

Development order is restored to:

1. whole-spec acceptance and remaining official-executable probes;
2. clean-room third-party capability audit;
3. loss-aware lexer and concrete syntax tree;
4. format-preserving writer and byte/normalized round-trip invariants;
5. typed semantic project models and cross-pathway validation;
6. executable management, isolated workspaces, outputs, and provenance;
7. GIS integrations and application layers.

## Consequences

- `spec/` and its source/evidence-backed v26135 resources remain authoritative.
- The simplified `schema/`, `syntax/`, and `semantic/` implementation from PR #2 is not part of
  the restored working tree.
- Ideas from PR #2 may be migrated only after explicit comparison with official specifications
  and the accepted stage order.
- PR #1 history, official regression evidence, and green CI records remain reachable.
- No history rewrite or destructive force update is required.
