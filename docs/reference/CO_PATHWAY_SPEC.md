# CO pathway source-verified specification

## Status

The bundled AERMOD v26135 CO specification remains **partial**. Batch 1 covers 14 framing/control records. Batch 2 adds 10 decay, urban/receptor, static ozone and NO2-ratio records, for **24 records total**. All other CO records remain inventory-only.

```python
from aermodkit.spec import load_pathway_specification

co = load_pathway_specification("CO", "26135")
ozone_file = co.get_record("OZONEFIL")
```

## Batch 2 records

| Keyword | Purpose | Current fixtures | Handler |
|---|---|---:|---|
| `HALFLIFE` | exponential-decay half-life | 0 | `EDECAY` |
| `DCAYCOEF` | exponential-decay coefficient | 0 | `EDECAY` |
| `FLAGPOLE` | default receptor height | 5 | `FLAGDF` |
| `URBANOPT` | single/multiple urban areas | 7 | `URBOPT` |
| `O3SECTOR` | ozone wind sectors | 0 | `O3SECTOR` |
| `OZONEVAL` | constant/fallback ozone | 16 | `O3VAL` |
| `OZONEFIL` | hourly ozone file | 8 | `O3FILE` |
| `NO2EQUIL` | ambient equilibrium ratio | 7 | `NO2EQ` |
| `NO2STACK` | global in-stack ratio | 16 | `NO2STK` |
| `ARMRATIO` | ARM2 min/max ratios | 2 | `ARM2_Ratios` |

## Source-behavior boundaries

- `HALFLIFE` and `DCAYCOEF` are mutually exclusive and the first form wins. `EDECAY` does not explicitly reject zero or negative values; this is recorded rather than replaced by invented source validation.
- `FLAGPOLE` defaults to 0.0 m when the optional value is absent.
- `URBANOPT` has distinct single- and multiple-area forms. A non-1.0 roughness is forced to 1.0 under DFAULT and is non-default otherwise.
- `O3SECTOR` accepts two to six ascending circular sector starts. Widths below 30 degrees are errors; widths below 60 degrees generate warnings.
- `OZONEVAL` and `OZONEFIL` default to UG/M3. Sector forms depend on `O3SECTOR`. The source does not explicitly reject same-sector duplicate records, so focused executable probes remain required.
- The User's Guide labels `OZONEFIL` non-repeatable, while the source dispatcher/handler supports sector-indexed calls. Both pieces of evidence are retained rather than silently choosing one interpretation.
- `NO2STACK` has no current default of 0.1; setup uses a negative sentinel until a CO or source-level ratio is supplied.
- `ARMRATIO` applies 0.50/0.90 defaults when omitted. Its handler checks for too few fields but does not explicitly reject trailing extra fields, which must be preserved.

## Fragment composition

Aggregate CO batch 2 intentionally composes older batch 1 fragments with new batch 2 fragments. The loader accepts a fragment only when its batch is positive and no newer than the aggregate batch. This lets completed evidence remain immutable while later batches extend the same pathway.

## Still excluded

`O3VALUES`, `OZONUNIT`, all NOX background records, deposition, low-wind/direction-window controls, aircraft controls and remaining option-dependent records are not yet bundled. No production lexer/parser/AST/writer is claimed.
