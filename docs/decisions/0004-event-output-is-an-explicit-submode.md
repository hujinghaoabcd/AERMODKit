# ADR 0004: Event output is an explicit output submode

## Decision

Represent ordinary `OUCARD` and event-mode `EV_OUCARD` separately. The ordinary OU exact set contains 18 records. Event processing recognizes `STARTING`, `EVENTOUT`, `FILEFORM`, and `FINISHED` through `EV_OUCARD` in `evset.f`.

## Rationale

Combining the sets would falsely imply `EVENTOUT` is accepted by ordinary OUCARD and would hide its mandatory status in event mode.
