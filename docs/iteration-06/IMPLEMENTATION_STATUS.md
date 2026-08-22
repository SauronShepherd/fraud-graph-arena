# FGA06 implementation status audit

This audit is deliberately conservative: absence of an obvious gap is not treated as proof of completion.

| Plan obligation | Current evidence | Status |
|---|---|---|
| Preserve empty ACADEMY_001 | Local workspace smoke: 0 nodes/0 edges; catalogue remains present | COMPLETE_LOCALLY |
| Real player-safe T02 graph | `case_data/academy_graph.py`; exact seven-node/seven-edge gate | COMPLETE_LOCALLY |
| Renderer-neutral backend/API boundary | graph dataclasses, workspace envelope, OpenAPI contract | COMPLETE_LOCALLY |
| Stable IDs and direction/type/family/provenance | graph DTOs and FGA-owned frontend callbacks | COMPLETE_LOCALLY |
| Semantic non-canvas path | persistent HTML evidence list and inspector | COMPLETE_LOCALLY |
| Board selection owns IDs, not actions | `BoardPage` selection state and no investigation endpoint | COMPLETE_LOCALLY |
| Qualification fixture and frozen criteria | `qualification/fixture-v1.json`, requirements, envelope, schemas | SCAFFOLDED_NOT_MEASURED |
| Cytoscape/Sigma/D3/React Flow comparison | candidate inventory exists; no exact packages/runs recorded | NOT_COMPLETE |
| Named commercial finalist/licence review | no finalist selected | NOT_COMPLETE |
| Performance measurements | envelope exists; benchmark report has no runs | NOT_COMPLETE |
| Production renderer decision | ADR is blocked pending qualification | NOT_COMPLETE_BY_DESIGN |
| FGA05 live predecessor closure | requires external Databricks qualification | BLOCKED_BY_USER_CONSTRAINT |
| Formal two-commit/tag release qualification | requires release workflow/evidence and tests | NOT_COMPLETE |

## Scope deliberately not implemented

Bounded expansion, relationship filtering, focus mode, hairball prevention, graph-size rules, investigation commands, credits, analytics, identity candidates, exact-match reveals, guilt/suspicion, accusations, and advanced accessibility remain owned by later iterations as required by the plan.

## Verification performed

Python compilation, local gate, OpenAPI export, frontend typecheck/build, in-memory T02/ACADEMY_001 workspace smoke checks, JSON parsing, fixture hashing, and diff hygiene were performed. Test runners were not executed and Databricks was not accessed.
