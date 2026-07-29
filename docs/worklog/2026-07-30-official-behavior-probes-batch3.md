# Worklog: official v26135 behavior probes batch 3

- Date: 2026-07-30
- Development branch: `agent/official-behavior-probes-batch3`
- Pull request: #11, merged
- Merge commit: `cab11308b022fe648dcb3bd5ba00bc7e758bc19a`
- Base: behavior-batch-2-complete `main`
- Phase: official behavior evidence before production loss-aware syntax

## Objective

Resolve the remaining high-priority CO and OU parser-shaping questions:

- ALPHA/DFAULT dependencies;
- `ARCFTOPT` repeatability and extra fields;
- actual aircraft-source dependencies;
- `MAXDCONT` THRESH and secondary-rank forms.

## Probe design

The final manifest contains 35 cases:

- 21 dependency-matrix cases: seven ALPHA controls, seven no-ALPHA observations, and seven DFAULT-plus-ALPHA observations;
- 10 aircraft cases separating `ARCFTOPT` card behavior from `ARCFTSRC` and `HOUREMIS` requirements;
- 4 `MAXDCONT` cases covering two signatures with dynamic and explicit file units.

A deterministic six-hour aircraft hourly-emissions support file is frozen in the repository. Official source searches retain the exact branches for `E133`, `E196`, `E198`, `E204`, `E821`, `E823`, the `ARCFTOPT` dispatcher, and `OUMAXD_CONT`.

## Reviewed evidence

- workflow run: `30461120811`;
- reviewed head: `7433a58adb1c2cd7d8304d2af76bf30919345fb6`;
- artifact ID: `8727721661`;
- artifact digest: `sha256:c301bfc8ec367569da40923e214431a34bd7266999ba028d3a7cba9e0293e3f0`;
- artifact size: `284,393,626` bytes;
- official executable SHA-256: `599b491b021c7ec254ba3a1062386f287e56e54a0d3bb9b67cfa72275d6916da`;
- cases: 35;
- accepted: 16;
- rejected: 19;
- indeterminate: 0;
- expectations met: 35/35.

## Findings

### ALPHA/DFAULT

All seven dedicated ALPHA controls completed. The four gas-deposition records use source-verified `E196` DFAULT conflicts and `E198` no-ALPHA checks. `LOW_WIND`, `AWMADWNW`, and `ORD_DWNW` expose their target DFAULT-plus-ALPHA diagnostics as `E133`, `E122`, and `E123`. Aircraft-source processing produces `E198` without ALPHA and `E198/E204` under DFAULT plus ALPHA.

### ARCFTOPT

No-payload, repeated-same, repeated-different, and extra-field `ARCFTOPT` cards all completed. The dispatcher assigns the airport ID only when the card has exactly one payload field. Repeated one-payload cards are last-assignment-wins in source state; no-payload and extra-field forms remain accepted/preserved but do not assign the airport ID.

Actual aircraft processing also requires a matching `ARCFTSRC` and preceding `HOUREMIS`; retained diagnostics include `E821`, `E822`, and `E823`.

### MAXDCONT

Both secondary-rank and THRESH signatures completed with and without a trailing file unit, and all four cases generated their requested output file. THRESH warnings in the annual NO2 fixture do not reject the record form.

## Corrections during the batch

Exploratory iterations identified fixture issues rather than specification failures:

- aircraft cards were reordered so `HOUREMIS` precedes `ARCFTSRC`;
- aircraft controls retained the existing `SRCGROUP ALL` and used `POLLUTID OTHER` to avoid unrelated completeness checks;
- `MAXDCONT` filenames were shortened after exploratory `E500` file-open failures;
- a Windows-only CI failure was traced to CRLF conversion of byte-hashed `case-evidence.csv`.

The final fix adds a narrowly scoped `.gitattributes` policy for retained probe evidence files. It does not impose LF on future syntax fixtures that intentionally exercise CRLF preservation.

## Gate update

Completed catalog entries:

- `alpha_dependency_matrix`;
- `arcftopt_repeat_extra_fields`;
- `OU-MAXDCONT-FORMS`.

The behavior inventory is now 19 total, 10 executed, 1 source-resolved, and 8 pending. The syntax implementation gate remains closed.

## Validation and publication

Final PR #11 head `521bdb9c7c4857f3bc4507de4d742fa517e83d42` passed:

- full nine-job CI `30475925322`;
- batch-2 official regression `30475925186`;
- batch-3 official workflow `30475925233`.

Final-head artifact:

- artifact ID: `8733686581`;
- digest: `sha256:f7e7ffbb80f53de55db56e66a56d14c22731c061ce5fdd733a36fc1e258100c0`;
- size: `284,393,538` bytes.

PR #11 was merged to `main` as `cab11308b022fe648dcb3bd5ba00bc7e758bc19a`.

## Boundary

No production parser, immutable CST, format-preserving writer, semantic model, runner, output parser, or GIS layer was introduced.
