# Worklog — complete AERMOD v26135 CO pathway specification

## Scope

Completed all 15 remaining `COCARD` primary records in one combined stage, audited all 40 `MODELOPT` tokens, added exact-set verification, evidence tables, a focused official-behavior probe catalog, tests, and handover updates.

## Result

- 39/39 primary CO records bundled;
- ten JSON fragments;
- source-dispatch and bundled-specification sets match exactly;
- temporal cardinalities for `O3VALUES` and `NOX_VALS` recorded;
- gas-deposition, low-wind, downwash, direction-window, and aircraft dependencies documented;
- current-status classifications stored for all 40 source-recognized `MODELOPT` tokens;
- guide/source discrepancies preserved rather than normalized;
- focused official-executable probe catalog retained for ambiguous repeat and completeness behavior.

## Verified reconstruction

Direct transfer of large JSON blobs through the connector altered bytes during an early staging attempt. No corrupted object was added to the branch. The final payload was therefore transferred as SHA256-controlled compressed chunks and reconstructed inside GitHub Actions.

The workflow verified:

1. compressed payload SHA256;
2. safe archive paths;
3. SHA256 of all 19 target files;
4. editable package installation;
5. Ruff;
6. strict mypy;
7. pytest with coverage;
8. successful commit of the verified files.

GitHub Actions run `30421642505` completed successfully. All nine combinations of Ubuntu, Windows, and macOS with Python 3.11, 3.12, and 3.13 passed, and the final apply job successfully pushed commit `dc6676291173015e6b7a6b76bcaea2c059da1381`.

## Cleanup

The one-time reconstruction payload, reconstruction script, and temporary apply workflow are removed after verification. The ordinary CI matrix is restored in the final cleanup commit.
