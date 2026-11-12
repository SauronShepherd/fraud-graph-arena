# FGA06 candidate matrix

This is the four-candidate OSS matrix after the automatic comparison, repeated performance run and analyst visual review recorded under `reports/iteration-06/`. Commercial graph components are deliberately excluded from this project scope: no commercial dependency, license obligation or vendor-specific production path is introduced.

| Candidate | Exact version | Automated evidence | Qualitative fit | License | Current decision |
| --- | --- | --- | --- | --- | --- |
| Cytoscape.js (normative incumbent) | 3.34.4 | A/B lifecycle + node/edge probes pass; 12-run p95 first useful render 123 ms; selection 0.2 ms; fit 6.1 ms; resize 26.4 ms | Graph-native semantics, styling and layouts; direct adapter boundary required for React | MIT | QUALIFIED incumbent for the frozen FGA06 envelope |
| Sigma.js | 4.0.3 | A/B lifecycle + node/edge probes pass; 12-run p95 first useful render 308.9 ms; cleanup p95 1461.9 ms; long tasks observed | Strong WebGL/network-scale candidate; cleanup cost and long-task profile need review | MIT | Comparison candidate; not selected |
| D3 | 7.9.0 | A/B lifecycle + node/edge probes pass; 12-run p95 first useful render 41.2 ms; selection 0.7 ms | Maximum bespoke control; FGA owns graph-product features and accessibility bridges | ISC | Comparison candidate; not selected |
| React Flow (`@xyflow/react`) | 12.12.0 | A/B lifecycle + node/edge probes pass; 12-run p95 first useful render 207.4 ms; fit 69.4 ms | Best React composition; editor/diagram orientation and external layout remain trade-offs | MIT | Comparison candidate; not selected |
| Commercial graph component | Excluded by project scope | Not run | Licensing/support reference only | Not applicable | OUT_OF_SCOPE |

Lifecycle values come from `renderer-comparison-fga-2026-11-03.json`; repeated p95 values and long-task telemetry come from `renderer-performance-fga-2026-11-08.json` (12 repetitions per candidate). All four candidates meet the frozen functional envelope. Sigma's teardown and long-task profile remain a material trade-off, so the decision is not a popularity or speed ranking. The dependency-free exhibit remains a semantic baseline and fallback demonstration.

The architecture decision is now explicit: qualify Cytoscape.js 3.34.4 as the normative incumbent for this FGA06 envelope. The project-owned inspector, semantic fallback, stable-ID contract and adapter boundary remain mandatory even with a qualified renderer. Sigma.js, D3 and React Flow remain documented comparison candidates rather than silently promoted alternatives.
