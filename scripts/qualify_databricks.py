from __future__ import annotations
import argparse, json, subprocess
from pathlib import Path
from fraud_graph_arena.canonical_persistence.registry import PHYSICAL_TARGETS, OPERATIONAL_TARGETS
from fraud_graph_arena.canonical_persistence.operational_registry import columns, ddl
from fraud_graph_arena.case_data.registry import headers
OPERATIONAL_COLUMNS = {table: list(columns(table)) for table in OPERATIONAL_TARGETS}
from fraud_graph_arena.canonical_persistence.registry import expected_topology

def api(profile: str, payload: dict) -> dict:
    result = subprocess.run(["databricks", "api", "post", "/api/2.0/sql/statements", "--profile", profile, "--json", json.dumps(payload)], capture_output=True, text=True, check=True)
    return json.loads(result.stdout)

def main() -> int:
    p = argparse.ArgumentParser(); p.add_argument("--profile", default="sda"); p.add_argument("--catalog", default="sda_dev"); p.add_argument("--schema", default="sandbox"); p.add_argument("--warehouse-id", default="e444f39962128242"); p.add_argument("--create", action="store_true"); p.add_argument("--recreate", action="store_true"); p.add_argument("--apply", action="store_true"); p.add_argument("--confirm"); p.add_argument("--report", type=Path); args = p.parse_args()
    if args.recreate and (not args.apply or args.confirm != f"fga_dev:{args.catalog}:{args.schema}"):
        raise SystemExit(f"refusing destructive qualification; require --apply --confirm fga_dev:{args.catalog}:{args.schema}")
    base = {"warehouse_id": args.warehouse_id, "wait_timeout": "30s", "catalog": args.catalog, "schema": args.schema}
    probe = api(args.profile, {**base, "statement": "SELECT 1 AS capability_probe"})
    if probe.get("status", {}).get("state") != "SUCCEEDED": raise SystemExit("Databricks capability probe failed")
    statements = []
    pre_inventory = api(args.profile, {**base, "statement": "SHOW TABLES IN `" + args.catalog + "`.`" + args.schema + "`"})
    pre_names = [row[1] for row in pre_inventory.get("result", {}).get("data_array", [])]
    if args.recreate:
        expected_names = set(expected_topology())
        # The approved disposable namespace is converged by removing only
        # objects discovered inside that namespace; no production fallback exists.
        for table in sorted(set(pre_names) - expected_names):
            api(args.profile, {**base, "statement": f"DROP TABLE IF EXISTS `{table}`"})
        for table in expected_names:
            if table in pre_names:
                api(args.profile, {**base, "statement": f"TRUNCATE TABLE `{table}`"})
    if args.create:
        for table in expected_topology():
            if table in PHYSICAL_TARGETS.values():
                path = next(path for path, target in PHYSICAL_TARGETS.items() if target == table)
                columns = list(headers(path)) + ["_publication_id", "_load_run_id"]
            else: statements.append(ddl(table)); continue
            statements.append(f"CREATE TABLE IF NOT EXISTS {table} (\n  " + ",\n  ".join(f"{column} STRING" for column in columns) + "\n) USING DELTA")
        for statement in statements:
            response = api(args.profile, {**base, "statement": statement})
            if response.get("status", {}).get("state") != "SUCCEEDED": raise SystemExit(json.dumps(response))
    inventory = api(args.profile, {**base, "statement": "SHOW TABLES IN `" + args.catalog + "`.`" + args.schema + "`"})
    names = [row[1] for row in inventory.get("result", {}).get("data_array", [])]
    expected = set(expected_topology()); actual = set(names)
    columns_response = api(args.profile, {**base, "statement": f"SELECT table_name, column_name FROM `{args.catalog}`.information_schema.columns WHERE table_schema = '{args.schema}' ORDER BY table_name, ordinal_position"})
    observed_columns = {}
    for row in columns_response.get("result", {}).get("data_array", []): observed_columns.setdefault(row[0], []).append(row[1])
    expected_columns = {table: list(headers(path)) + ["_publication_id", "_load_run_id"] for path, table in PHYSICAL_TARGETS.items()}
    expected_columns.update(OPERATIONAL_COLUMNS)
    column_mismatches = sorted(table for table in expected if observed_columns.get(table) != expected_columns.get(table))
    report = {"status": "pass" if expected == actual and not column_mismatches else "fail", "catalog": args.catalog, "schema": args.schema, "warehouse_id": args.warehouse_id, "capability_probe": "pass", "recreated": args.recreate, "pre_inventory": sorted(pre_names), "expected_count": len(expected), "actual_count": len(actual), "missing": sorted(expected - actual), "extra": sorted(actual - expected), "column_mismatches": column_mismatches}
    rendered = json.dumps(report, indent=2) + "\n"
    if args.report: args.report.parent.mkdir(parents=True, exist_ok=True); args.report.write_text(rendered, encoding="utf-8")
    print(rendered, end=""); return 0 if report["status"] == "pass" else 1
if __name__ == "__main__": raise SystemExit(main())
