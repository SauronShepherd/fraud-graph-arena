from __future__ import annotations
import csv, json
from pathlib import Path
from .registry import headers, load_typed_registry
def write_table(path: Path, table: str, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    cols = headers(table)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="raise", lineterminator="\n")
        w.writeheader()
        for row in rows:
            specs = {column["name"]: column for column in load_typed_registry()[table]["columns"]}
            missing = [column for column in cols if not specs[column]["nullable"] and row.get(column, "") == ""]
            if missing: raise ValueError(f"{table}: missing non-nullable fields: {','.join(missing)}")
            w.writerow({c: row.get(c, "") for c in cols})
def read_table(path: Path, table: str) -> list[dict[str,str]]:
    with path.open(newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        if r.fieldnames != list(headers(table)): raise ValueError(f"{table}: ordered header mismatch")
        return list(r)
