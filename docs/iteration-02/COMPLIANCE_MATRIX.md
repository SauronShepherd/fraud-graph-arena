| Requirement | Implementation | Evidence |
|---|---|---|
| 1600×900 logical canvas | `apps/web/src/board/layout.ts` | `layout.test.ts` |
| One contain mapper | `layout.ts` | point/rectangle round-trip tests |
| Server-owned action IDs | `workspace/service.py`, `WorkspaceResponse` | round journey tests |
| Empty paper and graph | `CasePaper.tsx`, `GraphViewport.tsx` | board component/e2e target |
| Container recomposition | `BoardPage.tsx` `ResizeObserver` | build/runtime board check |
| Versioned assets and safe regions | `manifest.json`, `regions.json` | `validate_board_manifest.py` |
| Runtime role boundaries | `runtime/main.py`, `application.py` | `test_runtime_roles.py` |
| I00 ancestry | `verify_release_lineage.py` | release-lineage command |
| Intro skip policy | `RoundService`, `IntroCompletionRequest` | round API tests |
| Comic image contract | `NarrativeService.validate_case` | narrative tests |
