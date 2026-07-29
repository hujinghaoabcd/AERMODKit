# CO pathway source-verified specification

## Status

The bundled AERMOD v26135 CO specification is **partial**. Batch 1 covers the 14 framing and foundational control records listed below. Remaining CO records stay at inventory status and must not be presented as fully specified or implemented.

The machine-readable index and record fragments are bundled below `src/aermodkit/spec/versions/v26135/` and loaded with:

```python
from aermodkit.spec import load_pathway_specification

co = load_pathway_specification("CO", "26135")
model_options = co.get_record("MODELOPT")
```

## Evidence hierarchy

1. EPA v26135 source code and observed official executable behavior;
2. current EPA v26135 manuals and release material;
3. current `aermet26135_aermod26135` official fixtures;
4. AERMODKit validation tests.

The specification stores source dispatch and handler ranges, diagnostics, fixture examples, and evidence status for each record.

## Batch 1 records

| Keyword | Required | Repeatability | Handler | Current fixtures |
|---|---:|---|---|---:|
| `STARTING` | yes | once | `COCARD` | 53 |
| `FINISHED` | yes | once | `COCARD` | 53 |
| `TITLEONE` | yes | once | `TITLES` | 53 |
| `TITLETWO` | no | once | `TITLES` | 38 |
| `MODELOPT` | yes | once | `MODOPT` | 53 |
| `AVERTIME` | yes | once | `AVETIM` | 53 |
| `POLLUTID` | yes | once | `POLLID` | 53 |
| `RUNORNOT` | yes | once | `RUNNOT` | 53 |
| `ERRORFIL` | no | once | `ERRFIL` | 52 |
| `EVENTFIL` | no | once | `EVNTFL` | 0 active |
| `SAVEFILE` | no | once | `SAVEFL` | 0 active |
| `INITFILE` | no | once | `INITFL` | 0 active |
| `MULTYEAR` | no | once | `MYEAR` | 5 |
| `DEBUGOPT` | no | record-repeatable | `DEBOPT` | 2 |

## Important behavioral findings

### Pathway continuation

Only the opening and closing records need the explicit `CO` pathway token in the current official decks. Records inside the block commonly omit the prefix:

```text
CO STARTING
   TITLEONE  Example
   MODELOPT  CONC FLAT
   AVERTIME  1 PERIOD
   POLLUTID  SO2
   RUNORNOT  RUN
CO FINISHED
```

A future lexer must track the active pathway rather than require a pathway prefix on every line.

### Preservation before semantics

The source handlers do not validate every possible extra token. For example, `STARTING` and `FINISHED` do not inspect payload fields. AERMODKit may diagnose extra fields at the semantic layer, but the syntax layer must retain them verbatim. Comments, blank lines, original case, spacing, unknown records, and future/development fields follow the same rule.

### `MODELOPT`

The current source recognizes 40 option tokens. `DEFAULT` aliases `DFAULT`. The source initializes current numerical defaults before processing options, defaults to `CONC` with warning `W205` when no output type is selected, and enforces option conflicts such as dry/wet depletion opposites and incompatible NO₂ techniques. Regulatory status is option-specific: source recognition alone is not a regulatory endorsement.

### `AVERTIME`

The source accepts integer-hour divisors of 24, plus `MONTH`, `PERIOD`, and `ANNUAL`. `PERIOD` and `ANNUAL` are mutually exclusive. Officially expected integer values are `1, 2, 3, 4, 6, 8, 12, 24`; duplicates are errors.

### `POLLUTID`

The pollutant identifier is stored in an eight-character field. The optional `H1H`, `H2H`, or `INC` modifier is restricted to `NO2`, `SO2`, and PM2.5 identifier variants and disables pollutant-specific special averaging behavior with warning `W276`.

### Restart and multiyear records

`SAVEFILE` and `INITFILE` conflict with `MULTYEAR`. A one-filename `MULTYEAR` record writes state; a two-filename record reads the previous state and writes the current state. The official PM10 1986–1990 fixtures prove that these records form an ordered state chain. Legacy `H6H` remains accepted but emits `W352`.

### `DEBUGOPT`

`DEBUGOPT` is repeatable in v26135. Each card contributes tokens to a combined stream processed after all `DEBUGOPT` cards have been read. Individual debug options remain nonrepeatable. Filenames preserve original case. `LINE` is deliberately present in the recognition array only to diagnose invalid use; `AREA` is the supported debug selector.

### Known source-comment discrepancy

`EVNTFL` comments say an invalid `SOCONT|DETAIL` parameter uses the default, but the current source emits `W203` without explicitly assigning `DETAIL` after the invalid value has already been stored. The specification records the implemented behavior and preserves this discrepancy for future executable tests rather than normalizing it away.

## Validation boundary

Loading the CO batch 1 specification proves only that these 14 records passed structural validation and are backed by current source evidence. It does not imply complete CO coverage, a production parser, semantic execution support, support for every `MODELOPT` combination, or regulatory approval of non-default options.

The next specification batch should extend CO records rather than start production parser classes prematurely.
