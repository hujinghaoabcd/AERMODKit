# Worklog: official v26135 behavior probes batch 1

- Date: 2026-07-29
- Development branch: `agent/official-behavior-probes-batch1`
- Base: whole-spec-accepted `main`
- Phase: evidence collection before production loss-aware syntax

## Objective

Execute the first parser-shaping behavior probes with the EPA-distributed v26135 Windows executable
and retain enough evidence to distinguish accepted, rejected, and indeterminate behavior without
turning the probe harness into the application runner.

## Initial batch

The batch contains one infrastructure control and six targeted cases:

1. official Test3 RLINEXT/RBARRIER control;
2. SWPOINT with ALPHA;
3. SWPOINT without ALPHA;
4. one-barrier VBARRIER form;
5. two-barrier VBARRIER form;
6. repeated OZONEFIL in the same O3 sector;
7. repeated NOX_FILE in the same NOx sector.

## Evidence retained by the workflow

- official executable size and SHA-256;
- official source archive size and SHA-256;
- exact materialized input deck for each case;
- stdout and stderr;
- main output and error files;
- parsed E/W/I diagnostic rows;
- every workspace file size and SHA-256;
- selected official `soset.f` and `coset.f` handler ranges;
- one machine-readable batch summary.

## Boundary

No targeted case is declared accepted or rejected in advance. Only the official control has an
expected successful outcome. Workflow artifacts remain provisional until reviewed and committed as
final evidence. Production lexer/CST, semantic models, runner, output parser, and GIS remain out of
scope.
