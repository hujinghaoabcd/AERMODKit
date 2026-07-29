# ADR 0003: Executable source dispatch defines the recognized syntax set

- Status: Accepted
- Date: 2026-07-29

## Context

The pre-existing inventory omitted `SO PLATFORM` and `SO VBARRIER`, and treated `SWPOINT` as unconfirmed, even though the non-comment v26135 executable source dispatches both keywords and accepts `SWPOINT` in `SOLOCA`/`SOPARM`. The current manual summary does not list `SWPOINT`.

## Decision

For a version-specific pathway completion claim, the exact set of recognized primary syntax is the non-comment executable dispatcher branches in the official EPA source. Manuals determine documented/regulatory status, field explanations, and user-facing evidence; they do not erase executable syntax. Source/manual differences are represented as status and probe records.

## Consequences

- SO completion contains 40 primary records, including `PLATFORM` and `VBARRIER`.
- `SWPOINT` is modeled as source-recognized ALPHA/development syntax with an explicit manual-list omission.
- Recognition never implies regulatory approval.
- Future parser layers preserve unknown/future syntax even when semantic support is unavailable.
