# FGA 05 operations

Use `python scripts/audit_lakehouse_topology.py` for the expected topology, `python scripts/recreate_lakehouse_namespace.py --environment fga_dev --dry-run` for a safe reset preview, and `python scripts/reconcile_import_runs.py` for serialized external state. Reset rejects every environment except the explicit disposable `fga_dev` target.
