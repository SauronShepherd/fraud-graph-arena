# FGA06 renderer qualification workbench

This development-only package is independent of `apps/web` dependencies. It uses the same renderer-neutral fixture for candidate comparison and does not grant any candidate access to canonical truth or workspace state.

The current exhibit is a dependency-free semantic baseline. Candidate adapters must expose FGA node/edge IDs, typed styling, selection, fit/reset, resize, and cleanup without leaking native renderer objects.

The commercial candidate is intentionally not fabricated: licensing and redistribution evidence must exist before a named product is evaluated.
