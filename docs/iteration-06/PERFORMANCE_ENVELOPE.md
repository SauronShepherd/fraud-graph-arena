# FGA06 performance envelope

This is the pre-measurement envelope. It is committed before benchmark results and is not a claim that a formal benchmark has run.

| Phase | Target | Scope |
|---|---|---|
| First useful render | ≤ 1000 ms | T02 seven-node/seven-edge fixture in a local development browser |
| Selection visible | ≤ 100 ms | Known node or edge to persistent inspector update |
| Fit/reset | ≤ 500 ms | Fixed-position fixture |
| Resize recovery | ≤ 500 ms | Full-to-compact-to-full GraphViewport |
| Semantic fallback | Immediate after DOM commit | HTML list remains usable if visual renderer is unavailable |

Stress sizes are observations, not hidden product requirements. Formal candidate runs must record source SHA, exact versions, fixture hash, browser/OS, viewport, repetitions, and discarded runs.
