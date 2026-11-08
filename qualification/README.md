# FGA06 renderer qualification workbench

This development-only package is independent of `apps/web` dependencies. It uses the same renderer-neutral fixture for candidate comparison and does not grant any candidate access to canonical truth or workspace state.

The primary visual lab is `comparison-exhibit.html`. It presents Cytoscape.js, Sigma.js, D3 and React Flow as full-size tabs in one application shell so each graph can use the dominant canvas area without mixing native renderers. The shared lab fixture contains 18 nodes and 26 directed relationships with stable FGA IDs, realistic record types, relationship families and visual-only investigation states. Hovering or selecting a node/relationship opens a persistent contextual inspector; filters, fit, zoom, reset, a redundant legend and a custom minimap remain outside the renderer. Commercial engines are intentionally not executable candidates in this open-source/non-commercial branch; they remain a documented licensing and total-cost reference.

Run the lab from `apps/web` with `npm run qualification:dev` and open `http://127.0.0.1:5173/` (the root landing page) or `/comparison-exhibit.html`. Use `npm run qualification:build` to create the static deployable exhibit and `npm run qualification:e2e` to run its browser qualification suite. The engines are not isolated in iframes: the adapter boundary already prevents native objects from crossing into the shell, while same-window tabs preserve keyboard access, sizing, screenshots and comparable evidence.

The current Databricks evidence was produced with profile `fga` in `workspace.fga_sandbox` on warehouse `7c640666d4d3eb61`: the structure check covers 44 objects, the row verifier covers 32 active tables, and the 13-package rerun proves `REUSED_PRECHECK` with zero insert statements. The corresponding JSON reports live under `reports/iteration-06/`; the admin profile cannot qualify row-level denial because an admin session cannot prove its own lack of access.

The candidate adapters must expose FGA node/edge IDs, typed styling, selection, fit/reset, resize, cleanup and automated node/edge probes without leaking native renderer objects.

`harness.ts` provides the shared lifecycle runner. It measures the same mount, fit, viewport, resize, node probe, edge probe and cleanup sequence for every adapter and emits only renderer-neutral values. It is intentionally an execution seam, not benchmark evidence: candidate package versions, browser runs, licence records, manual review and measured reports must still be supplied before a production decision is made.

`adapters/svg-baseline.ts` is the dependency-free reference adapter used to exercise that seam. It is a qualification fixture and fallback reference, not a production renderer decision and not a substitute for the named library comparison.

`candidate-registry.ts` keeps that distinction machine-readable. The exhibit registers exact-version adapters for the four named libraries, while the registry remains conservative until hard requirements, licence evidence and manual review promote a candidate to `MEASURED`; the reference adapter is explicitly classified as a fallback.

Run `python qualification/audit_inventory.py` during evidence preparation to detect drift between the frozen candidate inventory and the required comparison set. A non-zero result is expected until every named candidate has measured evidence; it must never be bypassed by changing the production decision.

`decision.py` enforces the normative rule: missing or incomplete Cytoscape.js evidence blocks production, and a hard failure requires a normative specification change rather than a silent renderer substitution.

The commercial candidate is intentionally not fabricated: licensing and redistribution evidence must exist before a named product is evaluated. The executable decision remains blocked until the same hard requirements and manual review are complete for every open-source candidate.
