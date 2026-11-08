# FGA06 interaction notes — 2026-11-03

Observation source: `reports/iteration-06/renderer-manual-review-fga-2026-11-08.json` and the four per-candidate screenshots captured from the full-size tabbed exhibit. The common fixture is the 18-node/26-relationship investigation scene whose SHA is recorded in the generated JSON reports.

## Cross-candidate observations

- Each tab exposes the same controls: Fit, Zoom / pan, Probe node, Probe edge and Remount.
- Each graph shows the same directed 26-relationship topology and distinguishes investigation states with redundant shape/icon/colour treatment; no visual treatment is presented as guilt or certainty.
- Pros, cons and the fit signal are adjacent to the graph rather than hidden in a separate report.
- The five manual review checks were reviewed for every candidate: selection, viewport, semantic cues, resize and cleanup. The review is analyst evidence, not product-owner acceptance, and is kept separate from the browser automation.

## Candidate observations

| Candidate | Initial visual observation | Follow-up evidence |
|---|---|---|
| Cytoscape.js 3.34.4 | Initial fit shows the investigation scene, readable labels, directed arrows and relationship labels in the dark graph surface. | Graph-native styling and selection probes pass; conditional normative incumbent. |
| Sigma.js 4.0.3 | WebGL surface shows the investigation scene with readable light labels and directed edge geometry. | Node/edge probes pass; edge events are explicitly enabled; teardown is approximately 0.97–1.08 s in this two-run report and remains a cleanup/performance review item. |
| D3 7.9.0 | SVG surface shows the complete topology, readable labels and clear directed edges. | Bespoke visualisation remains the largest FGA-owned maintenance surface; probes and keyboard node/edge activation are wired. |
| React Flow 12.12.0 | React node cards, edge labels, background, compact dark minimap and visible attribution are present. | Native React composition is strong; editor/diagram orientation and external layout remain trade-offs. |

## Limits of this observation

This is a visual smoke observation, not proof of 200% zoom accessibility, keyboard-only operation, long-task/frame health, large-graph readability, or production integration. The browser's five checkboxes are intentionally left for the operator who deploys and reviews the exhibit.
