# FGA06 implementation status audit

This audit is deliberately conservative: absence of an obvious gap is not treated as proof of completion.

| Plan obligation | Current evidence | Status |
|---|---|---|
| Preserve empty ACADEMY_001 | Local workspace smoke: 0 nodes/0 edges; catalogue remains present | COMPLETE_LOCALLY |
| Real player-safe T02 graph | `case_data/academy_graph.py`; exact seven-node/seven-edge gate | COMPLETE_LOCALLY |
| Renderer-neutral backend/API boundary | graph dataclasses, workspace envelope, OpenAPI contract | COMPLETE_LOCALLY |
| Stable IDs and direction/type/family/provenance | graph DTOs and FGA-owned frontend callbacks | COMPLETE_LOCALLY |
| Semantic non-canvas path | persistent HTML evidence list and inspector | COMPLETE_LOCALLY |
| Board selection owns IDs, not actions | `BoardPage` selection state and no investigation endpoint | COMPLETE_LOCALLY |
| Qualification fixture and frozen criteria | `qualification/fixture-v1.json`, requirements, envelope, schema, shared lifecycle harness, report validator | IMPLEMENTED_AND_EXECUTED |
| Renderer-neutral graph example library | `apps/web/src/graph-engine/examples.ts`, five deterministic scenarios, explicit action sequences and validation tests | IMPLEMENTED_AND_EXECUTED |
| Zero-install static example gallery | `docs/iteration-06/examples/gallery.html`, inline SVG/HTML/JS, five tabs, menus, filters, views and keyboard path | IMPLEMENTED_AND_BROWSER_CHECKED |
| Embeddable investigation mini-game | Static gallery HUD, objective/progress loop, hints/restart, node drag, background pan, modifier-wheel zoom and camera/layout separation | IMPLEMENTED_AND_BROWSER_CHECKED |
| Tactile graph motion and glyphs | Type-aware SVG glyphs, bounded spring/repulsion physics, drag release velocity, damping, settling and accessible Motion toggle | IMPLEMENTED_AND_BROWSER_CHECKED |
| Contextual hover panels | Interactive target-aware node/relationship preview on pointer hover and keyboard focus, delayed hide while entering the card, icon actions and persistent dossier on selection | IMPLEMENTED_AND_BROWSER_CHECKED |
| Investigator working relationships | Local relationship composer, dashed rendering, stable local IDs and deletion limited to investigator-added edges | IMPLEMENTED_AND_BROWSER_CHECKED |
| Marked targets and centering | Visible node/edge highlight rings, removable marked-target list and camera centering on the selected target | IMPLEMENTED_AND_BROWSER_CHECKED |
| Renderer-neutral interaction controller slice | Pure command reducer, ordered source-labelled events, movement preview/commit/cancel, working relationships, marks, camera centering and deterministic replay | IMPLEMENTED_AND_TESTED |
| Rich visual graph dossier | Focused node/edge neighborhood, connected relationships, route cards, confidence signal, presentation timeline and contextual actions | IMPLEMENTED_AND_BROWSER_CHECKED |
| Production GraphViewport context panel | `apps/web/src/board/GraphContextPanel.tsx` integrated into the real board viewport with node/edge focus, semantic list and direct source/target navigation | IMPLEMENTED_AND_TESTED |
| Reference-demo visual uplift | Full-screen dark investigation board, gold frame, concentric field, three-cluster dense scene, hub glyphs, legend/minimap overlays and accessibility-correct SVG semantics | IMPLEMENTED_AND_BROWSER_CHECKED |
| Candidate registry and decision gate | explicit registry, inventory audit, and normative Cytoscape decision evaluator | COMPLETE_LOCALLY |
| Cytoscape/Sigma/D3/React Flow comparison | exact versions, four adapters, shared A/B runner, selection probes, full-size tabbed exhibit and analyst review record | QUALIFIED_COMPARISON_EVIDENCE |
| Commercial renderer | explicitly excluded from this OSS/non-commercial project scope | OUT_OF_SCOPE |
| Performance measurements | twelve repetitions per candidate record first-useful-render, selection, fit, resize, cleanup and long-task telemetry against the frozen envelope | QUALIFIED_FOR_FROZEN_ENVELOPE |
| Production renderer decision | ADR and formal report qualify Cytoscape.js 3.34.4; semantic inspector/fallback remain project-owned | QUALIFIED_CYTOSCAPE_INCUMBENT |
| FGA05 live predecessor closure | FGA06 live sandbox qualification now passes with profile `fga`; historical formal predecessor closure still requires its own release evidence | LIVE_SANDBOX_PASS_HISTORICAL_CLOSURE_PENDING |
| Formal two-commit/tag release qualification | source/evidence commits, closure validator, Docker smoke and immutable tags `fga-iteration-06-r1`/`r2` | COMPLETE_AND_TAGGED |

## Scope deliberately not implemented

Bounded expansion, relationship filtering, focus mode, hairball prevention, graph-size rules, investigation commands, credits, analytics, identity candidates, exact-match reveals, guilt/suspicion, accusations, and advanced accessibility remain owned by later iterations as required by the plan.

## Verification performed

Python compilation, local gate, OpenAPI export, frontend typecheck/build, in-memory T02/ACADEMY_001 workspace smoke checks, JSON parsing, fixture hashing, the full FGA04–FGA06 Python regression (93 passed), Playwright renderer exhibit (5 passed), static gallery mini-game qualification (3 passed), twelve-run renderer performance qualification, Docker root/health smoke, and live Databricks qualification were performed. The latest frontend regression passed Vitest (22 files, 49 tests), `npm run build`, the gallery Playwright tests, and Axe with zero violations. `git diff --check` retains only the pre-existing CRLF normalization warning for `contracts/openapi-v1.json`; the release commits themselves are clean. The `fga` admin identity cannot qualify the non-admin denial test.

## Progress calculation — 2026-11-07

The strict delivery percentage is calculated from this table, not from line count:

- 25 tracked obligations total;
- 1 is explicitly out of scope, leaving 24 in-scope obligations;
- 23 are fully green (`COMPLETE_LOCALLY`, `IMPLEMENTED_AND_EXECUTED`, `IMPLEMENTED_AND_BROWSER_CHECKED`, `IMPLEMENTED_AND_TESTED`, `QUALIFIED_COMPARISON_EVIDENCE`, `QUALIFIED_FOR_FROZEN_ENVELOPE`, `QUALIFIED_CYTOSCAPE_INCUMBENT` or `COMPLETE_AND_TAGGED`);
- strict completion: **23 / 24 = 96%**;
- one deliberately visible predecessor gap remains: the historical FGA05 immutable closure record cannot be reconstructed or rewritten from the current administrator identity.

The first investigation-workflow slice, renderer decision, Docker deployment and formal release are complete and locally browser-checked. The 96% figure is for the FGA-06 delivery ledger; it must not be read as “the entire future graph-engine vision is finished”. The 30-feature catalogue still contains scheduled work such as lasso, multi-selection, full replay/undo, additional layouts and renderer-scale qualification.
