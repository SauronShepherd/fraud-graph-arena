# FGA 05 traceability

This matrix maps the plan families to implementation owners and evidence. Paths are repository-relative; machine-readable qualification evidence is under `reports/iteration-05/`.

| Plan family | Responsibility | Primary implementation | Verification evidence | Status |
|---|---|---|---|---|
| S00–S01 | environment boundary and topology contract | `config/lakehouse/*.json`, `docs/architecture/adr/*` | clean recreation and gate reports | PASS |
| S02 | executable 32-path registry and DDL | `canonical_persistence/registry.py`, `sql/lakehouse/*` | registry/DDL tests, package validation | PASS |
| S03 | manifest/hash/header/type preflight | `package.py`, `importer.py`, `types.py` | tamper/type/archive tests, package validation | PASS |
| S04 | run/file/dataset ledger receipts | `models.py`, `warehouse.py`, `importer.py`, `operational_registry.py` | lifecycle/ledger tests, live row receipt report | PASS |
| S05–S06 | closed planner and candidate loading | `planner.py`, `importer.py`, `load_case_datasets.py` | loader and candidate tests | PASS |
| S07–S08 | candidate validation and pointer publication | `canonical_persistence/validator.py`, `databricks_warehouse.py`, `import_databricks_candidate.py`, `validate_databricks_candidate.py`, `record_databricks_publication.py`, `identity.py` | publication/validation tests, idempotence evidence | PASS locally; live warehouse unavailable |
| S09 | cleanup and restart reconciliation | `recovery.py`, `reconcile_import_runs.py` | reconciliation and failure-isolation tests | PASS |
| S10 | fail-closed disposable recreation | `recreate_lakehouse_namespace.py`, `qualify_databricks.py` | reset safety and clean recreation reports | PASS |
| S11 | topology/resource budget | `topology.py`, `audit_lakehouse_topology.py`, resource script | final topology/resource reports | PASS |
| S12–S13 | loader/security/authority boundaries | `security.py`, permissions SQL, loader tests | security tests and SQL policy review | PASS locally |
| S14 | qualification harness and cumulative gate | `qualify_databricks*.py`, `databricks_bulk_lifecycle.py`, `run_iteration_05_gate.py` | gate, package, repeat, row-count, failure reports | PASS locally; live warehouse unavailable |
| S15 | operations, qualification, evidence, closure audit | `docs/iteration-05-*.md`, `scripts/collect_iteration_05_evidence.py`, requirement audit | `requirement-audit.json`, unified audit | OPEN until live qualification |

## Explicit qualification gaps

| Requirement | Evidence | Status |
|---|---|---|
| DBX-012 / SEC-001: non-admin identity denied truth access | `reports/iteration-05/security/truth-access-negative.json` | PASS: `angel.alvarez.pascua@gmail.com` safe read passed and truth read was denied |
| DBX-009 response-loss and cleanup-failure fault injection | `tests/iteration_05/test_canonical_persistence.py`, `scripts/qualify_databricks_failure.py` | PASS locally; live transport fault-injection adapter unavailable |
| Immutable closed tag | `reports/iteration-05/requirement-audit.json`, `reports/iteration-05/unified-audit-current.json` | Blocked: live warehouse is unavailable; closure remains disallowed |
