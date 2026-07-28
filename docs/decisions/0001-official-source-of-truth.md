# ADR 0001: EPA material is the source of truth

- Status: Accepted
- Date: 2026-07-29

## Decision

AERMODKit derives model behaviour from U.S. EPA manuals, official source code, release notes, errata, technical support documents, and official test cases. When these sources appear inconsistent, the discrepancy must be documented and resolved explicitly rather than hidden behind a guessed rule.

## Consequences

- Every model-facing schema item will eventually carry traceability metadata.
- A passing third-party test is not sufficient evidence of correctness.
- The project may support multiple AERMOD releases without blending their rules.
- Unsupported or not-yet-mapped official features must remain visible in coverage reports.
