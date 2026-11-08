# FGA06 qualification evidence map

This map is intentionally conservative. A local implementation artifact is not treated as benchmark or release evidence.

| Requirement | Local evidence | Current state |
|---|---|---|
| Shared renderer-neutral contract | `candidate-contract.ts` | Implemented |
| Stable fixture and hashes | `fixture-v1.json`, `fixture_v1.py` | Implemented |
| Real player-safe Academy graph | `src/fraud_graph_arena/case_data/academy_graph.py`, `exhibit.html` | Implemented locally |
| Common adapter lifecycle | `harness.ts`, `comparison-exhibit.html` | Implemented; browser smoke and all four lifecycle runs pass |
| Dependency-free reference adapter | `adapters/svg-baseline.ts` | Implemented locally |
| Candidate inventory/roles | `candidate-inventory.json`, `candidate-registry.ts` | Implemented |
| Report schema and validator | `benchmark-report.schema.json`, `validate_report.py` | Implemented and executed; formal Cytoscape report validates |
| Normative renderer decision rule | `decision.py`, `docs/iteration-06/DECISION_RULES.md`, ADR-0001 | Implemented and evaluated; Cytoscape qualifies for the frozen envelope |
| Cytoscape.js qualification | `reports/iteration-06/renderer-cytoscape-qualification-fga-2026-11-08.json` | Qualified on all FGA06 hard requirements for the fixed envelope |
| Sigma.js/D3/React Flow comparison | `reports/iteration-06/renderer-comparison-fga-2026-11-03.json`, `renderer-performance-fga-2026-11-08.json` | Automatic, repeated performance and analyst review evidence pass; documented trade-offs remain |
| Commercial renderer review | Deliberately excluded from this OSS/non-commercial project scope | Out of scope |
| Formal FGA06 release gate | Clean-candidate qualification, closure evidence, immutable tag | Pending source/evidence release workflow |

The outstanding rows require execution and/or external evidence. They must not be represented as complete by changing status files alone.
