# AERMOD v26135 SO + RE pathway specification

## Completion

- SO: 40/40 primary `SOCARD` records bundled.
- RE: 9/9 primary `RECARD` records bundled.
- SO source types: 13 executable-recognized types, including ALPHA/development `SWPOINT`.
- RE grid secondary syntax is represented as nested state machines.

## Corrected inventory findings

The earlier dispatch inventory omitted executable `PLATFORM` and `VBARRIER` branches. The earlier source-type table marked `SWPOINT` unconfirmed; current source explicitly accepts it under ALPHA. These are corrected without treating recognition as regulatory status.

## SO architecture

The specification covers framing, source identity and source-type-dependent `SRCPARAM`, building/platform downwash, temporal emissions and hourly files, unit conversions, particulate/gas deposition, chemistry grouping, background concentration, roadway/solid/vegetative barriers, depressed roadways, buoyant lines, aircraft sources, HBP point-source selections, and final group ordering.

## RE architecture

`GRIDCART` and `GRIDPOLR` are block records with `STA`/`END` boundaries and exact coordinate-choice rules. Discrete Cartesian/polar and evaluation receptors encode terrain/flag conditional fields. `ELEVUNIT` must precede receptor definitions.

## Boundary

This is complete record-level specification, not a production parser, writer, semantic project model, runner, output parser, or GIS implementation.
