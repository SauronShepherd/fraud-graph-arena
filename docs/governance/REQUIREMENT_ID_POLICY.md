# Requirement and Delivery ID Policy

**Policy ID:** `FGA-ID-POLICY-1.0-20260726`

IDs are stable, unique, case-sensitive, and never reused after retirement.

## Namespaces

| Kind | Pattern | Example |
|---|---|---|
| Module | `M01`–`M20` | `M13` |
| Interaction | `I01`–`I19` | `I09` |
| Requirement | `REQ-<AREA>-<TOPIC>-NNN` | `REQ-GOV-BASELINE-001` |
| Iteration | `IXX` | `I00` |
| Stage | `IXX-SYY` | `I00-S03` |
| Task | `IXX-SYY-TZZ` | `I00-S03-T02` |
| Test | `TEST-<UPPER-KEBAB>` | `TEST-I00-TRACEABILITY` |
| Evidence | `EVID-IXX-<UPPER-KEBAB>` | `EVID-I00-BASELINE` |
| Risk | `RISK-NNN` | `RISK-001` |
| Decision | `ADR-NNNN` | `ADR-0001` |
| Release | `REL-YYYY.MM.DD-NN` | `REL-2026.07.26-01` |

## Rules

- IDs identify concepts, not filenames. Renaming or moving a file does not change its stable ID.
- A changed meaning receives a new ID; the old ID is marked superseded.
- Task IDs are reserved by the approved plan. Corrective tasks use the next free task number in the same stage or a dedicated corrective stage in the same iteration.
- Tests and evidence must reference stable requirement, module, interaction, stage, or task IDs.
- Prefixes above are exclusive. Validation rejects unknown prefixes, malformed examples, duplicate node IDs, and duplicate artifact IDs.

## Retirement

Retired IDs remain in history with a retirement reason and successor where applicable. They cannot be reassigned to a different requirement or artifact.
