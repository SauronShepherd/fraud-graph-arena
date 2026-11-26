# FGA-09 article / implementation traceability

This matrix is the bidirectional consistency receipt for the article source
09-zingg-me-a-river.md and branch FGA-09. A row is covered only when the
behavior exists in the implementation and has an executable test or a
machine-readable qualification receipt.

| Article claim / behavior | Implementation evidence | Executed evidence |
|---|---|---|
| NFKC, case folding, whitespace and field normalization are versioned | src/fraud_graph_arena/entity_resolution/normalization.py; fga09-norm-v1 | tests/iteration_09/test_normalization_and_engine.py covers compatibility variants, idempotency, original preservation and invalid states |
| Placeholders do not become identity evidence | Placeholder registry and normalize_value classification | Placeholder engine test; no exact match and no placeholder agreement fields |
| Exact identity needs the normalized contact pair, or a validated identifier exception | _strict_exact_fields; fga09-identifier-contract-v1 | Golden match, single-contact candidate, duplicate identifier and validated identifier tests |
| Exact output is player-safe and provenance-bearing | ExactIdentityMatch; API serialization | API provenance assertion; Databricks no-forbidden-column and association checks |
| Infrastructure associations do not become identity | PERSON-only engine path and exact-rule allowlist | Infrastructure exclusion test; live exact rows remain SAME_DEVICE, SAME_LOGIN_IP or SAME_REGISTERED_ADDRESS |
| Candidate generation is deterministic, bounded and explainable | EntityResolutionEngine, stable pair IDs, field explanations and version fields | Golden/hard-negative, focused-neighbour, cross-surname and candidate-field tests |
| Fallback is not presented as Zingg | RUNTIME_DETERMINISTIC_FALLBACK, actual_engine_run=False, compatibility receipt | API assertions and Databricks no_candidate_zingg_claim / actual_zingg_run=false checks |
| Training labels stay offline and leakage gates are independent | entity_resolution/evaluation.py is not imported by the web path | Balanced, pair-leak and record-ID-leak regressions; offline receipt |
| Identity analysis costs three credits and retries idempotently | entity_resolution/service.py and repository contracts | API concurrency, conflict, exhaustion, refund and SQLite restart tests |
| Reviews are accepted, rejected or unresolved without canonical merge | Review repository and PLAYER_REVIEWED_IDENTITY projection | Review API, player-safe edge and latest-review projection tests |
| Review history remains append-only while the graph shows the latest outcome | Repository lists all reviews; graph_with_reviews selects latest per candidate | Latest-review test asserts both history entries and no stale accepted edge |
| Missing fields are not rendered as disagreements | Engine emits separate arrays; panel renders missing: ... | Engine missing-phone assertions and frontend panel assertion |
| Browser retry keeps the same idempotency key across remount | Round-scoped sessionStorage retry map | Frontend remount/retry regression |
| Databricks qualification is read-only and publication-bound | scripts/qualify_entity_resolution.py uses SELECT-only statements | Qualification unit tests and historical profile-fga receipt |
| Current Databricks credential status is not misreported | Current qualification receipt records token-refresh failure | databricks-fga09-entity-resolution-current.json, invalid_grant before SQL |

## Explicit non-claims

The article and branch do not claim a live Zingg job, a qualified Spark/Scala
cluster, GraphFrames execution, transitive identity clusters, production model
quality, a universal locale policy, or a fraud verdict. Those limits are
implemented as visible fallback metadata and are part of the qualification
boundary.

## Final checks for this matrix

- Focused Python slice: 41 passed.
- Frontend: typecheck passed, 63 passed across 23 files, build passed.
- Offline evaluation: regression_pass=true, precision/recall 1.0, zero
  false merges/splits on the three-pair fixture.
- Live recheck: blocked at invalid_grant before SQL; no mutation attempted.
