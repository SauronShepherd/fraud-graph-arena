# FGA 00–02 compliance matrix

Article precedence: [ARTICLE_IMPLEMENTATION_PRECEDENCE.md](../governance/ARTICLE_IMPLEMENTATION_PRECEDENCE.md). Current release status: candidate; approved artwork and immutable I01/I02 closure evidence remain blocked.

| Requirement | Implementation | Evidence |
|---|---|---|
| 1600×900 logical canvas | `apps/web/src/board/layout.ts` | `layout.test.ts` | partial: production region integration pending |
| One contain mapper | `layout.ts` | point/rectangle round-trip tests | partial: production placement integration pending |
| Server-owned action IDs | `workspace/service.py`, `WorkspaceResponse` | round journey tests |
| Empty paper and graph | `CasePaper.tsx`, `GraphViewport.tsx` | board component/e2e target |
| Container recomposition | `BoardPage.tsx` `ResizeObserver`, `selectBoardMode` | layout tests | partial: full region-driven composition pending |
| Versioned assets and safe regions | `manifest.json`, `regions.json` | `validate_board_manifest.py` | blocked: approved artwork required |
| Runtime role boundaries | `runtime/main.py`, `application.py` | `test_runtime_roles.py` |
| I00 ancestry | `verify_release_lineage.py` | release-lineage command |
| Intro skip policy | `RoundService`, `IntroCompletionRequest` | round API tests |
| Comic image contract | `NarrativeService.validate_case` | narrative tests |
