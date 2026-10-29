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
| Qualification fixture and frozen criteria | `qualification/fixture-v1.json`, requirements, envelope, schema, shared lifecycle harness, report validator | IMPLEMENTED_NOT_MEASURED |
| Candidate registry and decision gate | explicit registry, inventory audit, and normative Cytoscape decision evaluator | COMPLETE_LOCALLY |
| Cytoscape/Sigma/D3/React Flow comparison | exact versions, four adapters, shared A/B runner and raw report are present | RAW_EVIDENCE_ONLY |
| Commercial renderer | explicitly excluded from this OSS/non-commercial project scope | OUT_OF_SCOPE |
| Performance measurements | raw lifecycle timings recorded; selection and hard-requirement review remain pending | RAW_EVIDENCE_ONLY |
| Production renderer decision | ADR and executable decision gate block silent substitution until Cytoscape evidence exists | BLOCKED_PENDING_QUALIFICATION |
| FGA05 live predecessor closure | requires live Databricks qualification; current `fga` workspace has no usable warehouse credits | BLOCKED_BY_EXTERNAL_WORKSPACE |
| Formal two-commit/tag release qualification | requires release workflow/evidence and tests | NOT_COMPLETE |

## Scope deliberately not implemented

Bounded expansion, relationship filtering, focus mode, hairball prevention, graph-size rules, investigation commands, credits, analytics, identity candidates, exact-match reveals, guilt/suspicion, accusations, and advanced accessibility remain owned by later iterations as required by the plan.

## Verification performed

Python compilation, local gate, OpenAPI export, frontend typecheck/build, in-memory T02/ACADEMY_001 workspace smoke checks, JSON parsing, fixture hashing, and diff hygiene were performed. Test runners were not executed and Databricks was not accessed.
