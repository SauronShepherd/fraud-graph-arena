# FGA-12 article ↔ implementation matrix

| Article promise | Implementation | Verification |
|---|---|---|
| A case is a versioned package, not a new application fork. | `case-packages/*/manifest.json`, `CasePackage`, `CasePackageRegistry`. | Package discovery test; catalogue lists ACADEMY_001, ACADEMY_T02 and ACADEMY_T03. |
| Package schema is closed and declarative. | `contracts/case-packages/fga12-case-package.schema.json`; no executable manifest field. | Schema mutation test adds `runtime_command` and is rejected. |
| Package, canonical, engine and rule versions remain separate. | Manifest fields `package_version`, `canonical.*`, `compatibility.*`, `economy.version`, `scoring.version`. | Registry/validator assertions; T03 receipt returns `fga12-scoring-v1` and `fga12-economy-v1`. |
| Validation happens before play. | `case_packages/validator.py`, `scripts/validate_case_packages.py`. | All three packages validate with zero errors; app validates narrative sequences at startup. |
| Public and protected evidence stay separate. | `CasePackage.rows()` is used for published data in projections; evaluator reads truth only server-side. | Workspace and analysis response assertions reject protected fields; Databricks checks safe columns only. |
| Existing T02 behavior remains stable. | Generic graph, identity, economy and evaluator paths select T02’s package. | Full repository suite: 263 passed; targeted regression includes FGA09–FGA11. |
| A new case reaches a playable resolution. | T03 manifest points to the existing canonical package; shared round/workspace/graph/submission services consume it. | T03 starts with 15 credits, exposes 23/27 graph projection, runs analysis, accepts six claims and returns CLEAN_COLLAR at 1000. |
| Supported actions are package data. | `supported_actions` controls workspace availability and service authorization, including manual hypotheses. | T02 keeps `CREATE_HYPOTHESIS` through its manifest; T03 omits it, identity resolution returns `ACTION_NOT_AVAILABLE`, and graph analysis remains available. |
| Economy is package data. | `EconomyService.cost_provider` and round initialization read manifest economy; the validator rejects costs for undeclared actions. | T03 graph analysis debits 3 from 15; an unsupported `COMPARE_IDENTITIES` cost is rejected; receipt reports `fga12-economy-v1`. |
| Databricks boundary is qualified with profile `fga`. | `scripts/qualify_case_packages.py`; report in `databricks-fga12-packages-current.json`. | Live profile `fga`: T02 20/21 and T03 23/27, one snapshot each, no forbidden columns, read-only. |
| Article assets follow the established FGA pair. | `angelic-assets` FGA-12 `images/articles/fga/12-case-me-if-you-can/1.png` and `2.png`. | Asset repository commit `103b4b6`; CDN HEAD checks after push. |

