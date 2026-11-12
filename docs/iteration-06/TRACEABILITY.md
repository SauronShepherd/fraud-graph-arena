# FGA06 renderer traceability

| Requirement | Implementation/evidence | Result |
|---|---|---|
| Four open-source engines use one fixture | `qualification/comparison-exhibit.ts`, `qualification/fixture-v1.json` | Four candidates use the same 18-node/26-relationship fixture in full-size same-window tabs |
| Same lifecycle sequence | `qualification/harness.ts` | Mount, fit, viewport, resize, node probe, edge probe, destroy |
| Stable node and edge IDs | `qualification/candidate-contract.ts`, adapter `probe*` methods | Automated probes pass for all four |
| Manual visual review | `qualification/comparison-exhibit.html`, `interaction-notes.md` | Initial visual smoke observed in full-size tabs; five persistent checks per candidate remain operator evidence |
| Pros/cons and fit | `comparison-exhibit.ts` trade-off matrix | Visible in the active engine inspector beside every graph |
| Downloadable evidence | `#download-report` and generated report | `reports/iteration-06/renderer-comparison-fga-2026-11-03.json`, with build-derived fixture SHA |
| Local browser qualification | `apps/web/e2e/qualification-exhibit.spec.ts` | 5 Playwright tests pass, including contextual node/relationship menus in every tab |
| Local regression | `npm test`, `pytest tests/iteration_05` | 33 Vitest and 67 Python tests pass |
| Databricks profile | `reports/iteration-06/databricks-*-fga-2026-11-03.json` | 13 packages, 44 objects, 32 tables pass |
| Databricks idempotency | `databricks-all-packages-fga-rerun-2026-11-03.json` | 13 `REUSED_PRECHECK`, zero insert statements |
| Security denial | `databricks-security-fga-2026-11-03.json` | Not qualified: `fga` identity is admin |
| Final engine decision | `ADR-0001-renderer-qualification.md`, `DECISION_RULES.md` | Cytoscape conditional incumbent; production gate remains blocked |

The traceability table intentionally distinguishes automatic evidence from manual and hard-requirement review. A green browser test is not evidence that a human has inspected semantic clarity, accessibility or visual legibility.
