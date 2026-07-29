# Reference material policy

This directory stores indexes, checksums, capability matrices, and analysis notes. Large official downloads should not be committed blindly. Their provenance, component version, canonical URL, licence/distribution status, and checksum must be recorded.

Current structure:

- `epa/v26135/manifest.yaml` — current official asset and component-version manifest;
- `coverage/` — official capability inventories and evidence status;
- `gaps/` — official-versus-third-party comparison plans and findings.

Planned or later structures:

- `aermod-view/` — commercial workflow and interaction analysis;
- `github-projects/` — third-party capability audits;
- `fixtures/` — small legally distributable official or derived test fixtures;
- `checksums/` — checksums for externally materialized official assets.

## Rules

1. EPA official materials are authoritative for model behavior.
2. A component version must be tracked independently; AERMOD 26135 does not imply AERMAP 26135.
3. A local historical manual must never silently replace the current version.
4. Null checksums mean the original asset has not been materialized and verified.
5. Third-party source code is not copied merely because it implements a similar feature.
6. Derived interpretations must be visibly marked and promoted only after verification.
