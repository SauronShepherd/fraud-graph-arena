# Iteration 02 — Responsive investigation board

The qualified journey remains:

`Launch → Detective Academy → ACADEMY_001 → opening comic → ACTIVE round → responsive detective office → empty paper → empty graph → compact recomposition → refresh/recover`

The board uses three authorities: artwork supplies atmosphere, semantic React components supply interaction, and the server workspace projection supplies case/round/action truth. The logical board canvas is 1600×900. `apps/web/src/board/layout.ts` is the only coordinate transform implementation; CSS/container layout controls presentation and `ResizeObserver` responds to actual board size.

The current Academy action projection uses stable IDs (`COMPARE_IDENTITIES`, `FIND_SHARED_FIELDS`, `SEARCH_EVIDENCE`, `OPEN_CASE_FILE`) with explicit availability states. These actions are intentionally `NOT_IMPLEMENTED` in I02. No graph nodes, edges, evidence, retrieval, credits, submissions, scoring, evaluator, ranked case, or FGA03 screen-state machinery is included.

Board assets are versioned under `apps/web/public/assets/board/v1`, with manifest, regions, stacking levels, safe frames, and a neutral nonfatal fallback. The approved final office artwork is an external design dependency; the fallback is not claimed as that artwork.

Accessibility requirements are represented through semantic regions, real buttons, focus styles, screen-reader empty-state text, pointer-transparent decorative layers, and reduced-motion-safe CSS. Long labels must wrap rather than be baked into artwork.
