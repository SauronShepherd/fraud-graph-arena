# FGA-18 implementation log — Log Me Tender

## Scope and authority

- Implementation branch: `FGA-18`, based on the final FGA-17 branch.
- Article branch: `FGA-18` in the `angelic-articles` checkout.
- Assets branch: `FGA-18` in the `angelic-assets` checkout.
- Master outline is authoritative for numbering: it calls this article FGA-18. The older Development outline still labels the same observability block FGA-17/I17; that discrepancy is recorded rather than silently renumbering the series.
- The article claims only behaviour that is represented in this branch or in a stored test/qualification receipt.

## What was implemented

1. Added `fraud_graph_arena.observability` with a declarative catalogue loader, request context, safe structured events, bounded in-process snapshots, aggregate metrics, parent/child spans and a sync/async-preserving decorator.
2. Added `contracts/observability/fga18-instrumentation.json` and its JSON Schema. The catalogue contains selectors and safe options, not Python code or executable expressions.
3. Added middleware correlation and trace propagation through `X-Correlation-ID` and `X-Trace-ID`, response headers, normalized UUID routes and opaque replacement for suspicious external IDs.
4. Instrumented selected round, investigation, entity-resolution, graph-analytics, economy and case-resolution boundaries.
5. Instrumented the SQLite round and credit-ledger adapters so the trace reaches persistence without emitting SQL text, raw identifiers or payloads.
6. Added frontend session trace propagation, safe API/runtime/promise error observations, a bounded client buffer and a React recovery-boundary observation.
7. Added the browser propagation test, the local click-to-API/API-to-SQLite smoke, focused contract tests, frontend tests and the Databricks public-boundary qualification.

## Iteration and failure ledger

### Baseline and first implementation

- Confirmed the FGA-17 baseline before changing the new surface: the existing `tests/iteration_17` suite passed (`4 passed`).
- The first frontend validation attempt failed because the new worktree had no `node_modules`: `tsc` was not available and Vitest could not resolve its module. `npm ci --no-audit --no-fund` installed the locked dependencies. npm reported environment-level notices (a deprecated transitive package in the web worktree and install-script approval notices in the article worktree); the subsequent typecheck, tests and build emitted no application warning.
- The first local observability smoke reached the expected trace and then failed while Windows tried to remove a temporary SQLite directory. The client/app reference was still alive at cleanup. The smoke now releases the client and collects the runtime before temporary-directory cleanup. The failure and correction are retained here because a green assertion followed by a failed command is not a green command.

### Redaction passes

- The first focused observability run passed its initial four checks, then the raw round UUID was found in the serialized trace. The event fields were already pseudonymous; the leak was in the HTTP route field. The middleware now normalizes UUID path segments to `/:id`, and the regression test searches the complete serialized trace.
- The next full backend run exposed a second legitimate privacy gap: `bearer-token-value` matched the original safe-character pattern and became a request ID. Header validation now rejects token, secret, bearer, password, credential and email markers as well as invalid characters, replacing them with a fresh opaque ID.
- The corrected focused suite passed (`7 passed`). The smoke passed with 22 events, including HTTP, domain, economy, SQLite and analytics boundaries; raw round ID, player ID and hidden-truth checks passed.

### Behaviour and browser evidence

- The async probe confirmed two successful calls and one propagated exception; the decorator did not alter return values or swallow the error.
- The browser test performs the graph-analysis action through Playwright and verifies that the outgoing API request carries the session trace ID. The Python smoke covers the application half: HTTP → domain → economy → SQLite → analytics. No public trace-inspection endpoint was added merely to make the test look more integrated.
- Full frontend evidence before the final test-only additions: typecheck passed, screen definitions parsed, Vitest passed (`27 files`, `71 tests`), production build passed, and Playwright passed (`17 tests`). After the FGA-18 browser propagation test was added, Playwright passed (`18 tests`).

## Test receipts

Commands run from the implementation worktree:

```text
python -m pytest -q tests/iteration_18
python scripts/fga18_observability_smoke.py
python -m pytest -q
cd apps/web
npm run typecheck
npm run validate:screens
npm test -- --run
npm run build
npm run test:e2e
```

The first complete backend regression recorded `301 passed` and one failed FGA-18 privacy test. After the header fix, the regression recorded `302 passed` before the two additional catalogue tests were added. The final post-addition regression recorded `304 passed in 10:31`; no stale green receipt is promoted as final evidence.

## Databricks receipt

Command:

```text
python scripts/qualify_fga18_observability.py --profile fga --catalog sda_dev --schema sandbox --warehouse-id eded42c9d0a69b84 --report reports/iteration-18/databricks-fga18-observability-current.json
```

The live run completed with:

- status `pass`;
- profile `fga`, authenticated;
- warehouse `eded42c9d0a69b84`;
- catalog/schema `sda_dev.sandbox`;
- 13 canonical package boundaries passed;
- read-only `SELECT` checks only;
- `truth_source_queried: false`;
- `actual_engine_run: false`;
- `docker_execution_on_databricks: false`;
- local observability contract schema `1.0.0`, 19 entries, safe redaction policy.

The report stores public projection counts, snapshots and allowlisted columns. It deliberately does not store account metadata, email addresses, hidden answers or player-runtime trace events. The local recorder remains local; Databricks is a public-boundary qualification, not a claim that the local trace ran in the warehouse.

## Editorial reconciliation

- The article follows the FGA-16/FGA-17 structure: three short italic opening paragraphs; Parts I–VIII; `The Arrest`; `Case Closed?`; `Next in the Series`; one separator; `Source Code`; `Release Receipt`; one separator; final infographic and caption.
- The first draft was checked against both outlines. The article follows Master FGA-18 numbering and states the Development-outline numbering discrepancy in this log.
- The article now describes the browser and API evidence as a deliberate pair rather than claiming that the Python smoke itself is a browser test.
- The final article reading-time estimate is 16 minutes, below the 20-minute series target.

## Limits kept visible

- The recorder is an in-process bounded sink, not a distributed tracing backend, retention policy or production dashboard.
- The browser error buffer is a safe local diagnostic surface; it is not game-event history.
- The qualification checks Databricks’ active player-safe publication boundary. It does not run Docker, GraphFrames or a hidden-truth query in the SQL Warehouse.
- Cancellation, background-task propagation and a production overhead baseline are not claimed by this iteration; the implemented proof covers sync/async success and failure, correlation, redaction, duration, status, resource cost and bounded metrics.
