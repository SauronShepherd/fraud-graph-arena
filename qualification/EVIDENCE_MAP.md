# FGA06 qualification evidence map

This map is intentionally conservative. A local implementation artifact is not treated as benchmark or release evidence.

| Requirement | Local evidence | Current state |
|---|---|---|
| Shared renderer-neutral contract | `candidate-contract.ts` | Implemented |
| Stable fixture and hashes | `fixture-v1.json`, `fixture_v1.py` | Implemented |
| Real player-safe Academy graph | `src/fraud_graph_arena/case_data/academy_graph.py`, `exhibit.html` | Implemented locally |
| Common adapter lifecycle | `harness.ts` | Implemented, not executed |
| Dependency-free reference adapter | `adapters/svg-baseline.ts` | Implemented locally |
| Candidate inventory/roles | `candidate-inventory.json`, `candidate-registry.ts` | Implemented |
| Report schema and validator | `benchmark-report.schema.json`, `validate_report.py` | Implemented, not executed |
| Normative renderer decision rule | `decision.py`, ADR-0001 | Implemented, evidence pending |
| Cytoscape.js qualification | Exact package, lifecycle run, benchmark, license report | Outstanding |
| Sigma.js/D3/React Flow comparison | Exact adapters, lifecycle runs, benchmark reports | Outstanding |
| Commercial renderer review | Deliberately excluded from this OSS/non-commercial project scope | Out of scope |
| Formal FGA06 release gate | Clean-candidate qualification, closure evidence, immutable tag | Outstanding |

The outstanding rows require execution and/or external evidence. They must not be represented as complete by changing status files alone.
