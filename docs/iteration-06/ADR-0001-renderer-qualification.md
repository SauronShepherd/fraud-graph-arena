# ADR-0001: graph renderer qualification

Status: `QUALIFIED_CYTOSCAPE_INCUMBENT`

## Decision

Qualify Cytoscape.js `3.34.4` as the normative incumbent for the frozen FGA06 fixture and performance envelope. Do not switch production to Sigma.js, D3 or React Flow from the comparison evidence.

This is a bounded decision: the exhibit supplies common lifecycle and visual evidence for all four open-source candidates, the repeated performance runner records twelve runs per candidate, and the formal Cytoscape report passes every hard requirement. The production shell remains responsible for the persistent inspector, semantic fallback and stable FGA-owned contract.

## Evidence

- `reports/iteration-06/renderer-comparison-fga-2026-11-03.json` — generated renderer-neutral report from the full-size tabbed exhibit; all four candidates pass the common lifecycle and stable node/edge probes on the 18-node/26-relationship fixture.
- `docs/iteration-06/CANDIDATE_MATRIX.md` — qualitative pros/cons, exact versions and observed timing caveats.
- `qualification/comparison-exhibit.html` — manual controls and five review checks per candidate.
- `reports/iteration-06/renderer-performance-fga-2026-11-08.json` — twelve-run p95 performance and long-task evidence.
- `reports/iteration-06/renderer-manual-review-fga-2026-11-08.json` — analyst review of all five manual checks for all candidates.
- `reports/iteration-06/renderer-cytoscape-qualification-fga-2026-11-08.json` — formal hard-requirement report validated by `qualification/validate_report.py`.
- `reports/iteration-06/databricks-all-packages-fga-2026-11-03.json` — 13/13 live package lifecycle pass using profile `fga`.

The raw comparison report is not a winner-ranking benchmark. It is complemented by the repeated-run report: Sigma's teardown is notably slower (p95 1461.9 ms) and its long-task profile is materially larger, while its functional envelope still passes. Those are recorded as comparison trade-offs rather than converted into unsupported hard failures.

The production boundary is renderer-neutral: FGA graph IDs, typed records, directed relationship semantics, safe summaries, and explicit counts cross the workspace API; renderer-native objects do not.

Commercial components remain outside the executable matrix because this is an open-source, non-commercial project. They may be discussed as licensing/support context, but no proprietary dependency or evaluation result is introduced.

Reopen triggers: a hard requirement failure, performance-envelope failure, incompatible license, unsupported version maturity, manual semantic/accessibility failure, a future FGA change requiring capabilities not available behind the adapter, or visible graph sizes materially exceeding the qualified envelope.
