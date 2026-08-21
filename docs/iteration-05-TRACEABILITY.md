# FGA 05 traceability

| Requirement family | Evidence |
|---|---|
| fixed canonical topology | `canonical_persistence/registry.py`, `test_canonical_persistence.py` |
| immutable identity and exact retry | `identity.py`, `importer.py`, FGA 05 tests |
| candidate activation and rollback | `warehouse.py`, FGA 05 tests |
| manifest integrity | `importer.py`, tamper test |
| recovery and redaction | `recovery.py`, `security.py`, FGA 05 tests |
| local 13-package qualification | `scripts/run_iteration_05_gate.py`, `reports/iteration-05/gate.json` |
| live platform qualification | explicitly not qualified locally |
