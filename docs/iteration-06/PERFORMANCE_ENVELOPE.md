# FGA06 performance envelope

This envelope was frozen before the 2026-11-04 exhibit rerun. The formal repeated-run qualification is now recorded in `reports/iteration-06/renderer-performance-fga-2026-11-08.json`.

| Phase | Target | Scope |
|---|---|---|
| First useful render | ≤ 1000 ms | T02 seven-node/seven-edge fixture in a local development browser |
| Selection visible | ≤ 100 ms | Known node or edge to persistent inspector update |
| Fit/reset | ≤ 500 ms | Fixed-position fixture |
| Resize recovery | ≤ 500 ms | Full-to-compact-to-full GraphViewport |
| Semantic fallback | Immediate after DOM commit | HTML list remains usable if visual renderer is unavailable |

Stress sizes are observations, not hidden product requirements. Formal candidate runs must record source SHA, exact versions, fixture hash, browser/OS, viewport, repetitions, and discarded runs.

The qualification run used twelve repetitions per candidate in headless Chromium on Windows, recorded the fixture hash, p95 distributions, cleanup and PerformanceObserver long-task telemetry, and passed every frozen functional target for all four candidates. Sigma produced the slowest cleanup (p95 1461.9 ms) and the largest long-task total; that is a comparison trade-off and does not block the qualified Cytoscape incumbent because the production decision evaluates the incumbent's p95 cleanup at 17.1 ms and all hard requirements pass.
