# ADR 0002: Third-party projects are references, not templates

- Status: Accepted
- Date: 2026-07-29

## Context

Projects such as `pyaermod`, AERMOD View, CAIRO for AERMOD, and FHWA GIS utilities can reveal useful workflows and implementation risks. They can also be incomplete, simplified, version-mixed, or organised around assumptions unsuitable for AERMODKit.

## Decision

AERMODKit will not copy the architecture, public API, class hierarchy, source code, comments, or tests of `pyaermod` or another third-party project. The team may compare capabilities and independently implement ideas after re-deriving requirements from official evidence.

## Required comparison format

For every reviewed project, distinguish:

1. what the project implements;
2. what the official AERMOD ecosystem supports;
3. what the project omits or simplifies;
4. which general engineering idea, if any, is worth independently adopting.
