# FGA-10 implementation log

This is the working evidence trail for branch `FGA-10`. It keeps the commands,
failures, corrections and qualification boundaries behind the article's shorter
development-diary prose.

## Instruction boundary

- User request: continue the FGA series article by article, create the matching
  repository branch, implement the article, qualify the implementation with the
  Databricks profile `fga`, generate the two series images, and do not close an
  article until its claims and implementation are bidirectionally consistent.
- Attached outlines: treated as the execution specification for FGA-10. They are
  not allowed to expand the user's scope by themselves.
- Editorial reference: FGA-00 through FGA-09 are the style and continuity
  reference. They are not executable instructions.

## 2026-11-26 — baseline and branch

1. Read the two attached outlines and extracted the FGA-10 contract:
   GraphFrames versus the visual graph, bounded neighbourhoods, paths,
   components, centrality, motifs, circular flows, cost/limits, cache identity,
   evidence translation and deterministic fixtures.
2. Reviewed the actual FGA-08 and FGA-09 Markdown structure: short italicised
   noir opening, `Part I` through `Part IX` movement, `The Arrest`, `Case
   Closed?`, `Next in the Series`, `Source Code`, and a final infographic.
3. Finished the local FGA-09 closure receipt on branch `FGA-09` at commit
   `c9cc904`, including its article matrix and current Databricks credential
   receipt.
4. Created this clean worktree and branch from that exact FGA-09 commit:
   `FGA-10` at `C:\Users\angel.alvarez\PycharmProjects\_worktrees\fraud-graph-arena-fga10-20261126`.

The pre-existing dirty FGA-09 worktree contains unrelated historical render
directories and is not used as the FGA-10 implementation surface.

## Editorial and technical contract

FGA-10 must make the following claims, and only these claims:

- the visual graph and analytical input are different bounded projections;
- FGA owns a domain result contract and does not expose GraphFrames DataFrames;
- six analysis actions are available: neighbourhood, shortest path, connected
  components, centrality, motif candidates and circular flows;
- direction, relationship family/type, time window, depth/path length and result
  limits are parameters, not hidden magic;
- structural results carry supporting relationship IDs and an interpretation;
- centrality, components, short paths and cycles are leads or structures, not
  identity, control, culpability or a verdict;
- cache identity includes round, case version, snapshot, projection visibility,
  parameters and implementation version;
- malformed graphs, disconnected graphs, isolated nodes, time filters, duplicate
  relationships and out-of-scope subjects are handled deterministically;
- the local runtime is an explicit deterministic fallback. It does not claim that
  GraphFrames executed when the `fga` profile only reaches a SQL Warehouse;
- the action is currently bounded and does not charge FGA-11's future economy;
- the source graph is not mutated by an analysis response.

## Implementation passes

### Pass 1 — adapter and deterministic engine

Added:

- `src/fraud_graph_arena/graph_analytics/models.py` — result contract and
  supported action vocabulary;
- `src/fraud_graph_arena/graph_analytics/engine.py` — bounded deterministic
  fallback with breadth-first neighbourhood/path search, connected components,
  degree/PageRank/betweenness, cycle motifs and temporal circular-flow output;
- `src/fraud_graph_arena/graph_analytics/service.py` — active-round authority,
  visible-scope validation, cache identity, history and safe result assembly;
- `GraphAnalyticsGateway` — FGA-owned provider boundary for a future qualified
  GraphFrames provider;
- snapshot version propagation from the canonical T02 graph;
- `RUN_GRAPH_ANALYSIS` availability in the Academy T02 workspace;
- POST and history GET routes under
  `/api/v1/rounds/{round_id}/investigations/graph-analytics`;
- typed API response models and regenerated OpenAPI contract;
- a bounded graph-analysis panel in the React investigation desk.

The response exposes safe node/edge projections, paths, components, ranked leads,
motifs, support relationship IDs, result caps, cache metadata and limitations.
It does not expose truth tables, evaluator labels or a vendor DataFrame.

### Failure and correction: components were not one tidy graph

The first engine test assumed the T02 graph would be one 20-node component. The
published fixture is deliberately more interesting: its largest component has
17 nodes and the remaining records are disconnected. The test was corrected to
assert the known 17-node component and the presence of multiple components. The
implementation was not changed to make the fixture look more connected. A
component action must report the graph that exists.

### Failure and correction: PageRank promoted lonely witnesses

The first centrality implementation returned every node, including isolated
nodes whose PageRank came from the dangling-node distribution and which had no
supporting relationship. That was a poor player-facing lead. The correction
keeps isolated records in component analysis but excludes them from ranked
centrality leads. Every ranked lead now carries at least one supporting
relationship ID.

### Failure: clean worktree had no frontend dependencies

The first FGA-10 UI command failed before running code:

```text
"tsc" no se reconoce como un comando interno o externo
"vitest" no se reconoce como un comando interno o externo
```

The worktree had no ignored `apps/web/node_modules`. Running `npm ci` from the
declared frontend package restored the reproducible dependency surface. npm
reported the lockfile's existing deprecation/vulnerability notices during
installation; no `npm audit fix` was applied because that would change the
dependency contract without a scoped dependency decision.

### Pass 2 — API, cache and truth firewall

Added deterministic tests for:

- all six analysis families;
- directed paths and relationship-type filters;
- known payment cycle and event-time window;
- disconnected components;
- centrality determinism and supporting edges;
- malformed endpoints and duplicate edge IDs;
- cache replay and visibility-sensitive cache keys;
- authoritative scope rejection;
- history de-duplication;
- no credit charge and no workspace graph mutation;
- bounded request validation;
- response absence of evaluator sentinels.

### Pass 3 — explicit runtime failure boundary

The article said a provider failure must not be rewritten as a cheerful empty
graph. The first service implementation only translated `ValueError` into a
client validation error; an unexpected provider exception would still escape.
The service now returns a `FAILED` / `EXECUTION_FAILURE` result with no nodes,
edges, paths, components, leads or motifs, records the attempt in history and
does not cache it. The API regression replaces the provider with a failing test
engine, checks the explicit failure result and verifies that an identical retry
gets a new analysis ID instead of a cached failure.

### Pass 4 — test-environment warning boundary

The initial Vitest runs emitted Node's
`ExperimentalWarning: localStorage is not available because --localstorage-file
was not provided`. This was an environment warning, not an application failure,
but the requested closure gate requires a clean test receipt. The frontend test
script now uses `apps/web/scripts/run-vitest.mjs`, which gives Node workers a
temporary localStorage file without disabling warnings globally. The focused
and complete suites then ran without that warning.

## Test ledger

| Time | Area | Command or experiment | Result | Lesson |
|---|---|---|---|---|
| 2026-11-26 | Branch | `git worktree add -b FGA-10 ... FGA-09` | Created from `c9cc904` | FGA-10 starts from the closed FGA-09 implementation, not from a dirty mixed worktree. |
| 2026-11-26 | First engine pass | `pytest tests/iteration_10 -q` | 12 passed, 2 failed | The real fixture exposed disconnected components and unsupported isolated centrality leads. |
| 2026-11-26 | Correction | component and centrality assertions/engine | Corrected | A known-answer test must describe the fixture, not force a nicer story. |
| 2026-11-26 | FGA-10 local slice | `pytest tests/iteration_10 -q` | 17 passed | Algorithms, API, cache, explicit failure boundary, truth firewall and mocked Databricks qualification are green. |
| 2026-11-26 | Regression | `pytest tests/iteration_10 tests/iteration_09 tests/iteration_08 tests/iteration_01/test_openapi_contract.py -q` | 58 passed | FGA-10 coexists with identity resolution, manual hypotheses and the committed API contract. |
| 2026-11-26 | Complete Python regression | `python -m pytest -q` | 245 passed in 18:05 | The full repository suite is green after restoring direct-script import bootstraps for the historical CLI tests. |
| 2026-11-26 | Python hygiene | `python -m compileall -q src scripts tests/iteration_10` | Passed | New modules and direct qualification script compile. |
| 2026-11-26 | Diff hygiene | `git diff --check` | Passed | No whitespace errors in the implementation diff. |
| 2026-11-26 | Frontend dependencies | `npm ci` in `apps/web` | Installed; npm emitted existing deprecation and audit notices | Dependency installation is reproducible, but the lockfile still has upstream audit debt. |
| 2026-11-26 | Frontend typecheck | `npm run typecheck` in `apps/web` | Passed | The new graph-analysis panel and typed API contract compile. |
| 2026-11-26 | Focused frontend | `npm test -- --run src/board/InvestigationActions.test.tsx` | 8 passed, no warnings | The graph question is visible, sends the bounded visible scope and explains the non-verdict boundary. |
| 2026-11-26 | Complete frontend | `npm test` | 64 passed across 23 files, no warnings | The complete Vitest suite is green after the explicit localStorage-file runner fix. |
| 2026-11-26 | Frontend typecheck and build | `npm run typecheck; npm run validate:screens; npm run build` | Passed | The typed panel, screen set and production bundle compile and build. |
| 2026-11-26 | Article content validation | `npm run content:validate` | Validated 108 canonical articles | FGA-09 and FGA-10 satisfy the repository's canonical frontmatter and article rules. |
| 2026-11-26 | Internal links | `npm run check:links` | 116 same-origin URLs; no failures | The direct article links and existing site routes resolve without an internal-link failure. |
| 2026-11-26 | Article production build | `npm run build` in the article worktree | 98 pages built; Pagefind indexed 93 pages | FGA-09 and FGA-10 routes are emitted, and Pagefind reports no missing-body warning. |
| 2026-11-26 | Databricks live qualification | `qualify_graph_analytics.py --profile fga ...` | Passed: 11 checks, SELECT-only | Profile `fga` reauthenticated; publication, counts, endpoints, payment cycle, snapshot and column boundary all passed. GraphFrames remains explicitly unresolved on SQL Warehouse. |

## Databricks boundary

The new qualification is SELECT-only. It checks the active publication, twenty
records, twenty-one relationships, complete endpoints, the three-edge `PAYS`
cycle fixture, snapshot consistency and forbidden player columns. It does not
install GraphFrames, start a cluster, create a table, write a row or alter a
publication.

The current receipt is:

- `reports/iteration-10/databricks-fga10-graph-analytics-current.json`
- status: `pass`
- live checks: 11
- SQL statements: 7 SELECT-only statements
- mutation attempted: none

The earlier `invalid_grant` receipt was a real failed attempt and remains part
of the historical log. It is not the current qualification result. The current
receipt is the green run after the profile was reauthenticated.

The article must say this plainly. A mocked qualification proves the script's
logic; it is not a live Databricks pass.

## Final editorial and technical audit

### Pass 1 — reader promise and opening

The final article was read as a first-time FGA reader. The opening is three
short noir paragraphs and 107 words, matching the compact FGA-09 opening (105
words). It introduces the graph-analysis problem, separates structure from
culpability and states the bounded-question promise before Part I. No change
was justified.

### Pass 2 — series structure and visual rhythm

The FGA-09 and FGA-10 heading maps were compared. Both articles have nine
numbered parts, `The Arrest`, `Case Closed?`, `Next in the Series`, the same
source-code and release-receipt block, two body separators and the final
infographic caption. FGA-10 keeps the current series structure without copying
FGA-08's older long-form layout. No change was justified.

### Pass 3 — noir voice, contractions and terminology

The prose was checked for the established contractions, detective-dog humour,
occasional series references and the previously removed identity-example names.
FGA-10 contains no `NFKC` claim, no repeated artificial names and no identity
shortcut disguised as graph evidence. It uses “the same entity” where the
meaning is entity equivalence and keeps the GraphFrames/fallback language
distinct from FGA-09's Zingg language. No change was justified.

### Pass 4 — article-to-code technical traceability

The article's claims were checked against the graph-analysis models, service,
engine tests, API tests and traceability matrix. The six actions, result types,
bounded parameters, cache identity, deterministic fallback, explicit
`EXECUTION_FAILURE` boundary, supporting relationships and no-mutation/no-credit
behaviour are all implemented and tested as described. No unsupported claim was
found and no change was justified.

### Pass 5 — known-answer data and live receipt

The local fixture and the live Databricks receipt were re-read together. The
fixture has 20 nodes and 21 relationships; components are `[17, 1, 1, 1]`; the
known path uses `T2-REL-016` and `T2-REL-017`; the chronological cycle uses
`T2-REL-016`, `T2-REL-017` and `T2-REL-018`. The live `fga` receipt is `pass`,
read-only, has 11/11 checks, zero dangling endpoints and
`actual_engine_run=false`. No discrepancy was found and no change was
justified.

### Pass 6 — failure and boundary behaviour

The complete FGA-10 slice was re-run and closed with 17 passed tests. The edge
case review covers direction, time windows, relationship filters, disconnected
components, isolated nodes, malformed endpoints, duplicate IDs, invisible
subjects, bounded scopes, cache identity and an explicit provider failure that
is neither rewritten as an empty answer nor cached. No exception or misleading
success path was found and no change was justified.

### Pass 7 — UI, API contract and direct publication route

The focused `InvestigationActions` suite closed with 8/8 tests and no warning.
The panel exposes `RUN_GRAPH_ANALYSIS`, sends the visible scope and presents
the GraphFrames/fallback boundary. The direct routes for FGA-09 and FGA-10 are
included in the unlisted publication set, while the Pagefind body and redirect
fixes preserve the site's existing route behaviour. No inconsistency was found
and no change was justified.

### Pass 8 — copy, markup and whitespace hygiene

The final Markdown was checked for trailing whitespace, legacy `<code>` tags,
unbalanced inline backticks, unwanted entities and the series' colon
capitalisation pattern. The article has no trailing whitespace or legacy code
tags, uses backticks for inline code and matches FGA-09's punctuation rhythm.
`git diff --check` found no whitespace error. No change was justified.

### Pass 9 — reading time, density and image accessibility

FGA-10 has 3,738 body words, `readingTime: 19`, 77 prose blocks and a maximum
prose paragraph of 70 words. The table, list and section rhythm keep the deep
dive readable without expanding the introduction. Both images have descriptive
alt text/captions, and the pinned PNG URLs returned HTTP 200. No change was
justified.

### Pass 10 — integrated final regression

The final integrated pass closed with 245 Python tests, 64 frontend tests in 23
files, successful typecheck and screen validation, 108 validated articles, 116
healthy same-origin URLs, and a production build that emitted both FGA routes.
Pagefind indexed 93 pages without a missing-body warning. The article, code,
tests, direct route and visual assets now agree on the same bounded graph-
analytics contract. No change was justified.

## Closure gates currently satisfied

- complete frontend suite and production build ran from the clean FGA-10
  implementation worktree;
- the Node localStorage warning was resolved at the runner boundary without
  suppressing unrelated warnings;
- the FGA-10 slice and its FGA-08/FGA-09/OpenAPI regression are green;
- profile `fga` was reauthenticated and the live SELECT-only qualification
  passed;
- the article and implementation matrix now state the same current receipts;
- the newspaper cover and final infographic were generated, inspected and
  pushed as `1.png` and `2.png` in the FGA-10 asset branch.

The remaining closure work is committing and pushing the implementation and
article branches, then repeating the live `fga` qualification against the
definitive implementation commit and recording that final hash in the receipt.
