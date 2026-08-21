# FGA03 compliance matrix

| Requirement | Implementation | Evidence |
| --- | --- | --- |
| Versioned finite screen definitions | `apps/web/src/screen-system/contracts.ts`, `definitions/` | `tests/iteration_03/test_screen_contract_schema.py` |
| No configuration-as-code | strict JSON Schema and semantic validator | schema negative tests |
| Central route resolution | `BrowserNavigationAdapter.tsx`, `routeCodec.ts` | route codec and navigation tests |
| Deterministic transitions | `machine.ts` | `machine.test.ts` |
| Registered reads/actions | `dataSources.ts`, `actions.ts` | runtime tests and walking skeleton |
| No page-local router/API calls | migrated pages | `test_frontend_navigation_architecture.py` |
| Resolution remains unreachable | internal definition with no production edge | `test_screen_definition_reachability.py` |
| No closing/protected-truth leakage | production JSON and screen-system static scans | `test_no_closing_leak.py` |
| Backend remains screen-agnostic | no screen interpreter or endpoint | `test_backend_screen_boundary.py` |
| I02 Academy journey preserved | existing board and backend contracts | `src/test/navigation.test.tsx` |

Evidence, graph analytics, credits, submission/evaluation, public resolution, and ranked content remain explicit non-goals for this iteration.
