# FGA06 renderer decision rules

The decision is evidence-gated. The comparison exhibit may show raw measurements and qualitative trade-offs, but it may not promote a candidate to production by popularity or by a timing snapshot.

## Hard requirements

| ID | Requirement | Current evidence | Status |
|---|---|---|---|
| H01 | Semantic node styling by FGA type | Four adapters map fixture record types to candidate styles; analyst review passed | PASS |
| H02 | Semantic relationship styling by family/type/direction | Four adapters preserve directed edge IDs and relationship fields; analyst review passed | PASS |
| H03 | Stable FGA node ID on selection | Automated probes return `FIX-N-0000` for all four candidates | PASS |
| H04 | Stable FGA edge ID on selection | Automated probes return `FIX-E-0000` for all four candidates | PASS |
| H05 | Zoom and pan | Shared lifecycle and per-card controls execute | PASS_LOCAL |
| H06 | Programmatic fit/reset | Shared lifecycle and per-card controls execute | PASS_LOCAL |
| H07 | Preset positions | Frozen fixture supplies deterministic positions | PASS_LOCAL |
| H08 | Predictable resize | Shared lifecycle records resize for every candidate | PASS_LOCAL |
| H09 | Mount/update/unmount cleanup | Cytoscape 12-run cleanup p95 is 17.1 ms; Sigma's slower teardown remains a comparison caveat | PASS for incumbent |
| H10 | Persistent safe detail inspection | Full-size exhibit and production inspector keep stable node/edge details visible after selection | PASS |
| H11 | Project-owned semantic fallback | HTML inspector/list remains outside the renderer and uses only FGA-owned IDs and summaries | PASS |
| H12 | Acceptable measured performance | Twelve-run p95 first-render/selection/fit/resize evidence passes the frozen envelope | PASS |
| H13 | Production-suitable maturity | Exact versions, lockfile resolution, browser evidence and lifecycle report are recorded | PASS |
| H14 | Compatible core/extension licence | Direct candidates are MIT/ISC; Cytoscape is MIT and has no installed transitive dependencies | PASS |
| H15 | No native renderer objects in FGA contracts | `CandidateInstance` exposes only FGA operations and stable IDs | PASS_LOCAL |

## Decision algorithm

1. Any `FAIL` on a hard requirement blocks the normative choice and requires an architecture/specification change.
2. Any `PENDING` or `REVIEW` hard requirement keeps the production decision blocked.
3. If Cytoscape.js 3.34.4 satisfies every hard requirement and the frozen performance envelope, select it as the production renderer because it is the normative incumbent.
4. If Cytoscape.js fails, do not silently substitute another candidate; record `NORMATIVE_CHANGE_REQUIRED` and obtain an explicit architecture decision.
5. Commercial engines remain contextual only in this open-source, non-commercial project.

Current result: `QUALIFIED_CYTOSCAPE_INCUMBENT`. The qualification is bounded by the frozen FGA06 fixture and performance envelope; larger graph sizes, new renderer extensions or new product requirements reopen the decision.
