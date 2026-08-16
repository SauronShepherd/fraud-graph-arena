# Iteration 02 — Responsive investigation board

The target candidate journey remains:

`Launch → Detective Academy → ACADEMY_001 → opening comic → ACTIVE round → responsive detective office → empty paper → empty graph → compact recomposition → refresh/recover`

The board uses three authorities: artwork supplies atmosphere, semantic React components supply interaction, and the server workspace projection supplies case/round/action truth. The logical board canvas is 1600×900. `apps/web/src/board/layout.ts` is the only coordinate transform implementation; CSS/container layout controls presentation and `ResizeObserver` responds to actual board size.

The current Academy action projection uses stable IDs (`COMPARE_IDENTITIES`, `FIND_SHARED_FIELDS`, `SEARCH_EVIDENCE`, `OPEN_CASE_FILE`) with explicit availability states. These actions are intentionally `NOT_IMPLEMENTED` in I02. No graph nodes, edges, evidence, retrieval, credits, submissions, scoring, evaluator, ranked case, or FGA03 screen-state machinery is included.

Board assets are versioned under `apps/web/public/assets/board/v1`, with manifest, regions, stacking levels, safe frames, and a neutral nonfatal fallback. The manifest currently records `EXTERNAL_APPROVAL_REQUIRED`; the approved final office artwork is an external design dependency and the fallback is not claimed as that artwork.

Accessibility requirements are represented through semantic regions, keyboard-reachable `aria-disabled` buttons, focus styles, screen-reader empty-state text, pointer-transparent decorative layers, and reduced-motion-safe CSS. Long labels must wrap rather than be baked into artwork.

## Qualification status

This document describes the current candidate, not a completed release. The neutral fallback asset is usable for development but does not satisfy the required approved layered detective-office artwork. The current logical mapper and semantic regions are wired into the board geometry model, while full artwork-calibrated placement and final release evidence remain pending. Do not label the current HEAD “qualified” until the clean cumulative gate and immutable lineage checks pass.
