# FGA06 renderer qualification workbench

This development-only package is independent of `apps/web` dependencies. It uses the same renderer-neutral fixture for candidate comparison and does not grant any candidate access to canonical truth or workspace state.

The current exhibit is a dependency-free semantic baseline. Candidate adapters must expose FGA node/edge IDs, typed styling, selection, fit/reset, resize, and cleanup without leaking native renderer objects.

`harness.ts` provides the shared lifecycle runner. It measures the same mount, fit, viewport, resize, and cleanup sequence for every adapter and emits only renderer-neutral values. It is intentionally an execution seam, not benchmark evidence: candidate package versions, browser runs, license records, and measured reports must still be supplied before a production decision is made.

`adapters/svg-baseline.ts` is the dependency-free reference adapter used to exercise that seam. It is a qualification fixture and fallback reference, not a production renderer decision and not a substitute for the named library comparison.

The commercial candidate is intentionally not fabricated: licensing and redistribution evidence must exist before a named product is evaluated.
