# FGA-10 article / implementation traceability

This matrix is the bidirectional closure record for the FGA-10 article. A row is
closed only when the implementation, executable evidence and article wording
agree.

| Article claim / behaviour | Implementation evidence | Executed evidence |
|---|---|---|
| Visual and analytical graphs are separate scopes | `GraphAnalyticsService._authorise_scope`; server rebuilds nodes/edges from IDs | API scope test and cache-key test |
| FGA owns a domain result instead of exposing DataFrames | `GraphAnalyticsGateway`, `GraphAnalysisResult`, typed API response | API contract/openapi regression |
| Neighbourhood analysis is bounded | `GraphAnalyticsEngine._neighbourhood`, max hops and result limit | engine/API tests |
| Shortest paths preserve direction and supporting edges | `_shortest_paths`, `paths`, `supporting_relationship_ids` | known T02 payment-path test |
| Components are structural grouping, not identity | `_components` and result limitation | disconnected-component test |
| Centrality is a structural lead, not guilt | degree/PageRank/betweenness, interpretation and edge support | deterministic centrality test |
| Motifs and circular flows preserve event times | `_motifs`, relationship/time filters and chronology flag | known cycle and time-window tests |
| Isolated or malformed records do not become misleading leads | endpoint validation and actionable centrality filtering | malformed graph and centrality tests |
| Parameters belong in the cache identity | `_cache_key` includes snapshot, visibility, request and implementation version | cache replay/scope test |
| Analysis does not charge or mutate the workspace graph | no economy settlement in FGA-10 service; graph provider remains source | API credits/graph regression |
| GraphFrames execution is not falsely claimed | `actual_engine_run=false`, fallback metadata, read-only qualification | mocked qualification and passed live boundary receipt |
| Execution failures remain explicit and are not cached as empty answers | `GraphAnalyticsService` returns `status=FAILED`, `result_type=EXECUTION_FAILURE`, keeps the result outside evidence and skips cache insertion | provider-failure API regression |
| Databricks qualification is read-only | `scripts/qualify_graph_analytics.py` SELECT-only statements | qualification tests; live profile `fga` receipt passed all 11 checks |
| Player can run a visible graph question | `InvestigationActions.tsx`, API client and action availability | focused UI test |
| Article is available without changing the public catalogue decision | `unlistedArticleSlugs` includes `fga--10-graphframes-of-mind` and the article source is routed at `/fga/10-graphframes-of-mind/` | content validation and production build emitted the direct route |
| Cover and final case-file summary are the article's pinned visuals | frontmatter cover and final Markdown image point to the FGA-10 asset commit `dd3e93f` | both CDN PNG URLs returned HTTP 200; production build retained both URLs |

## Explicit non-claims

FGA-10 does not claim a live GraphFrames job, production performance, an
identity cluster, a causal path, culpability, a universal centrality threshold,
or that a circular flow is fraud. It also does not introduce FGA-11's resource
economy.
