from __future__ import annotations
import argparse, csv, hashlib, json, subprocess, tempfile, re
from pathlib import Path
from fraud_graph_arena.canonical_persistence.registry import PHYSICAL_TARGETS, headers
from fraud_graph_arena.canonical_persistence.identity import content_digest, publication_id
from fraud_graph_arena.canonical_persistence.models import PackageIdentity
from fraud_graph_arena.canonical_persistence.databricks_warehouse import _literal

def sql_api(profile, warehouse, catalog, schema, statement):
    payload = json.dumps({"statement": statement, "warehouse_id": warehouse, "wait_timeout": "30s", "catalog": catalog, "schema": schema})
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as fh:
        fh.write(payload); payload_path = fh.name
    result = subprocess.run(["databricks", "api", "post", "/api/2.0/sql/statements", "--profile", profile, "--json", "@" + payload_path], capture_output=True, text=True)
    if result.returncode: raise RuntimeError(result.stderr or result.stdout)
    output = json.loads(result.stdout)
    if output.get("status", {}).get("state") != "SUCCEEDED": raise RuntimeError(json.dumps(output))
    return output

quote = _literal

def main():
    p = argparse.ArgumentParser(); p.add_argument("package", type=Path); p.add_argument("--profile", default="sda"); p.add_argument("--catalog", default="sda_dev"); p.add_argument("--schema", default="sandbox"); p.add_argument("--warehouse", default="e444f39962128242"); p.add_argument("--all-rows", action="store_true"); args = p.parse_args()
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", args.catalog) or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", args.schema):
        raise SystemExit("catalog and schema must be registered SQL identifiers")
    manifest = json.loads((args.package / "manifest.json").read_text(encoding="utf-8"))
    digest = content_digest(args.package)
    publication = publication_id(PackageIdentity(manifest["case_id"], manifest["case_version"], manifest["snapshot_version"], manifest["canonical_model_version"], digest))
    first_table = next(iter(PHYSICAL_TARGETS.values()))
    existing = sql_api(args.profile, args.warehouse, args.catalog, args.schema, f"SELECT COUNT(*) FROM {args.catalog}.{args.schema}.{first_table} WHERE _publication_id = {quote(publication)}")
    if existing.get("result", {}).get("data_array", [["0"]])[0][0] != "0":
        print(json.dumps({"status": "REUSED", "publication_id": publication, "package": str(args.package), "retry": "REUSED"}, indent=2)); return
    import uuid
    run_id = "dbx_run_" + uuid.uuid4().hex
    counts = {}
    for rel, table in PHYSICAL_TARGETS.items():
        path = args.package / rel
        with path.open(encoding="utf-8", newline="") as fh: rows = list(csv.DictReader(fh)) if args.all_rows else list(csv.DictReader(fh))[:1]
        if not rows: counts[rel] = 0; continue
        columns = list(headers(rel)) + ["_publication_id", "_load_run_id"]
        for offset in range(0, len(rows), 500):
            values_sql = []
            for row in rows[offset:offset + 500]: values_sql.append("(" + ", ".join([quote(row.get(column)) for column in headers(rel)] + [quote(publication), quote(run_id)]) + ")")
            sql_api(args.profile, args.warehouse, args.catalog, args.schema, f"INSERT INTO {args.catalog}.{args.schema}.{table} ({', '.join(columns)}) VALUES {', '.join(values_sql)}")
        counts[rel] = len(rows)
    report = {"status": "pass", "run_id": run_id, "publication_id": publication, "package": str(args.package), "datasets_with_rows": sum(1 for n in counts.values() if n), "row_counts": counts, "retry": "not_run"}
    print(json.dumps(report, indent=2))
if __name__ == "__main__": main()
