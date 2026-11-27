# FGA-18 article ↔ implementation ↔ evidence matrix

| Article promise | Implementation | Test or receipt | Article location |
| --- | --- | --- | --- |
| Request correlation and game-session continuity | Frontend `browserTraceId`, `X-Trace-ID`, API middleware, request context and pseudonymous round reference | `tests/iteration_18/test_observability_contract.py`; browser propagation Playwright test; local smoke | Parts I–II |
| Player action, path and case context | Allowlisted action/algorithm fields plus path/case context on selected domain spans | End-to-end trace assertions and smoke event receipt | Parts I–II, V |
| Analytics execution evidence | `domain.graph-analytics.analyze` result summaries: status, result type, generation mode, engine flag and duration | Focused trace test and local smoke | Parts V, VII |
| Database-query boundary | Instrumented SQLite round and credit-ledger adapter methods with no SQL text or payload logging | Focused trace requires round charge and ledger insert; smoke lists both | Parts I, V, VIII |
| Frontend error evidence | Bounded `frontend.error` observations, API/network classification, React recovery-boundary hook | `apps/web/src/observability.test.ts`; API client implementation | Parts II, VII |
| Logs, metrics, traces and game history remain distinct | Structured event list, aggregate metric snapshot, trace filter and no observability table/history mutation | Focused snapshot assertions; no diagnostic persistence file | Part III |
| Compare instrumentation approaches | Narrative comparison of manual, decorators, middleware and broad automatic wrapping | Chosen hybrid exists in code: middleware + selected decorators + explicit safe context | Part IV |
| JSON catalogue lists targets and methods | Versioned JSON catalogue and JSON Schema with IDs, targets, kinds, options and redaction policy | Schema validation and loader test | Part IV |
| Configuration selects, never executes | Loader rejects executable-looking keys and duplicate IDs; decorators activate only configured IDs | `test_loader_rejects_executable_and_duplicate_entries`; disabled-entry test | Part IV |
| Sync and async semantics survive instrumentation | Separate sync/async wrappers preserve return values and re-raise exceptions | `test_sync_and_async_instrumentation_preserve_results_and_exceptions` | Part V |
| Secrets, player data, identifiers and hidden truth stay out | Allowlist, HMAC references, route normalization, header sanitization and sensitive-key filter | Full serialized-trace redaction assertions; untrusted-header test; smoke checks | Part VI |
| Duration, status and resource cost are measurable | Span elapsed time, success/error status, result summaries and economy `resource_cost` | Focused trace checks; smoke metrics receipt | Part VII |
| Useful production/article logs without pretending to be a platform | Structured JSON logger, bounded snapshot, aggregate counters and explicit limitations | Smoke output and stored implementation log | Parts III, VI, VIII |
| Browser click reaches API trace | Frontend sends stable trace header from the browser request | `apps/web/e2e/fga18-observability.spec.ts` (`18 passed` full E2E run) | Parts VII–VIII |
| API trace reaches database and analytics | Python TestClient smoke exercises create/start/opening/graph flow with SQLite | `fga18_observability_smoke.py`; full backend regression | Parts V, VII–VIII |
| Databricks boundary stays honest | Profile-specific read-only qualification script; no Docker or hidden truth | `databricks-fga18-observability-current.json`, status `pass`, 13 packages | Parts VII, Case Closed? |
| FGA-18 remains under the time budget and series pattern | 17-minute estimate; direct route, newspaper cover, final infographic and matching separators | Content validation, link check and Astro build generated `/fga/18-log-me-tender/` | Source Code, Release Receipt |

## Deliberate non-claims

- The article does not claim a distributed tracing backend, retention/alerting platform, cancellation/background propagation coverage or a production overhead baseline.
- The article does not claim GraphFrames, Zingg, Docker or protected truth execution in Databricks.
