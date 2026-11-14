# FGA-00 through FGA-07 article/implementation reconciliation

This is the bidirectional claim ledger for the canonical article
`C:\ANGEL\Personal\Articles\FGA\FGA_07_Every_Node_You_Take_Checked_Improved_Shortened.md`.
It records whether each externally testable feature family described by the
article is implemented, how it is tested, and which limits must remain visible
to a human reviewer.

Status meanings:

- `IMPLEMENTED + TESTED`: the repository contains the behaviour and a local regression covers it.
- `IMPLEMENTED + LIVE`: the behaviour is additionally exercised against Databricks with the `fga` profile or the qualified non-admin profile.
- `QUALIFIED WITH LIMIT`: the implementation is real, but the article must preserve a stated acceptance or scale boundary.
- `NOT A FGA-07 FEATURE`: the article must describe it as a future/design boundary, not as shipped behaviour.

| Iteration / article claim | Implementation | Test or evidence | Status |
|---|---|---|---|
| FGA-00 governance, stable identity keys, semantic relationship direction, truth/evidence separation | Governance docs, canonical contracts, source boundaries, graph projection allowlists | `tests/governance/`, `tests/iteration_01/`, `tests/iteration_04/test_truth_firewall.py`, `tests/iteration_04/test_projection_contract.py` | IMPLEMENTED + TESTED |
| FGA-01 walking skeleton and Academy board route | `apps/web/src/pages/BoardPage.tsx`, workspace service and route/screen system | `apps/web/src/test/navigation.test.tsx`, `tests/iteration_01/test_round_journey.py`, `npm run test:e2e` | IMPLEMENTED + TESTED |
| FGA-02 persistence and refresh boundary | canonical persistence/import modules and live publication helpers | `tests/iteration_05/test_canonical_persistence.py`, `tests/iteration_05/test_live_publication_lifecycle.py`, live Databricks receipts in `databricks-fga07-all-packages.json` | IMPLEMENTED + LIVE |
| FGA-03 declarative screens and navigation | `apps/web/src/screen-system/` and route codec/component registry | `apps/web/src/screen-system/*.test.ts*`, `tests/iteration_03/` | IMPLEMENTED + TESTED |
| FGA-04 canonical records, converters, validators, provenance and graph projection | `src/fraud_graph_arena/case_data/`, `src/fraud_graph_arena/canonical_persistence/`, graph projection modules | `tests/iteration_04/`, strict 13-package corpus gate | IMPLEMENTED + TESTED |
| FGA-05 Databricks lifecycle, safe published view and failure isolation | qualification scripts, publication lifecycle, bounded bulk transfer and permission SQL | `reports/iteration-07/databricks-fga07-all-packages.json`, `databricks-fga07-counts.json`, `databricks-fga07-repeat.json`, `databricks-fga07-failure.json`; `python -m pytest -q` | IMPLEMENTED + LIVE |
| FGA-06 renderer-neutral graph engine and renderer comparison | `apps/web/src/graph-engine/`, renderer qualification exhibit and ADR | `apps/web/src/graph-engine/*.test.ts`, `tests/iteration_06/test_renderer_qualification.py`, qualification Playwright suite | IMPLEMENTED + TESTED |
| Deterministic initial graph subset | `src/fraud_graph_arena/case_data/graph_investigation.py` | `tests/iteration_06/test_graph_investigation.py::test_initial_subset_is_deterministic_and_bounded` | IMPLEMENTED + TESTED |
| One-hop expansion only from the authorized revealed projection | graph investigation service, graph API and `BoardPage` expansion call | `tests/iteration_06/test_graph_investigation.py::test_expansion_is_one_hop_and_authorized_only`, `tests/iteration_06/test_graph_api.py` | IMPLEMENTED + TESTED |
| Hard node/edge and safe-text bounds | graph investigation limits and DTO validation | graph investigation/API tests, oversized safe-summary regression, focused graph suite | IMPLEMENTED + TESTED |
| Filters change presentation without changing truth | relationship-family filtering in service and viewport | `test_filter_changes_view_not_nodes_or_truth`, `GraphViewport.test.tsx` controlled-filter test | IMPLEMENTED + TESTED |
| Relationship-type filters | no current request field or UI control; only relationship-family filters exist | article wording explicitly marks type filters as future | NOT A FGA-07 FEATURE |
| View-only collapse and restore | local `collapsed` state in `GraphViewport.tsx` | collapse/restore and selected-node clearing tests; standard Playwright graph flow | IMPLEMENTED + TESTED |
| Full overlapping-branch collapse reason accounting | not implemented as a shared descendant policy; current collapse is local and reversible | article limitation retained | QUALIFIED WITH LIMIT |
| Zoom, keyboard/button pan, pointer pan, fit, reset, grid/circle layout and focus | `GraphViewport.tsx` controls and SVG transform | viewport component tests and qualification browser flow | IMPLEMENTED + TESTED |
| Semantic evidence list and non-hover inspector fallback | semantic list, inspector, accessible node buttons and minimap | viewport tests, accessibility E2E and qualification browser flow | IMPLEMENTED + TESTED |
| Minimap tracks visible layout and viewport marker | `.graph-minimap` SVG derived from positioned visible nodes and pan/zoom | viewport minimap assertions and qualification evidence | IMPLEMENTED + TESTED |
| Unknown node/relationship types remain visible | `GRAPH_NODE_TOKENS.DEFAULT` and `GRAPH_RELATIONSHIP_TOKENS.DEFAULT` | explicit unknown-token regression in `GraphViewport.test.tsx` | IMPLEMENTED + TESTED |
| Directed relationships retain semantic arrows | `markerEnd` for directed edges | directed-arrow regression in `GraphViewport.test.tsx` | IMPLEMENTED + TESTED |
| Evaluator/truth firewall before graph projection | graph service rejection of evaluator fields and forbidden sentinels | `tests/iteration_06/test_graph_api.py`, `tests/iteration_04/test_truth_firewall.py` | IMPLEMENTED + TESTED |
| Non-admin identity cannot read raw/truth data | `fga-non-admin-test` service principal, safe-view-only grant, live security probe | `reports/iteration-07/databricks-fga07-security.json`, security qualification script and focused tests | IMPLEMENTED + LIVE |
| Production player authentication and persisted reveal ledger | not implemented in this local prototype | article qualification boundary | NOT A FGA-07 FEATURE |
| Production manual relationship action | not exposed by the FGA-07 production board; present only in the FGA-06 static gallery/example | article wording scopes this to the gallery | NOT A FGA-07 FEATURE |
| Dedicated multi-role badge or role-accounting UI | no dedicated production UI or qualification fixture | article now states this limitation | NOT A FGA-07 FEATURE |
| Production request-byte and wall-clock envelope | no live scale qualification at the request boundary | release report and article limitation | QUALIFIED WITH LIMIT |
| Human accessibility/product-owner acceptance and visual judgement | automated browser/axe evidence exists; human sign-off is external | release report outstanding-closure section | QUALIFIED WITH LIMIT |

## Reconciliation conclusion

The article now describes the shipped FGA-07 surface, distinguishes the FGA-06
gallery from the production board, and names every known unimplemented or
externally gated feature instead of implying completion. The implementation
has an explicit regression for unknown renderer tokens, so the article's
fallback claim is backed by executable evidence.

The remaining `QUALIFIED WITH LIMIT` rows are not silently treated as green:
they require either a future feature or an explicit human/production-scale
acceptance step before the project can claim absolute end-to-end closure.
