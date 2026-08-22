from __future__ import annotations
from pathlib import Path
from .csv_codec import write_table
from .manifest import write_manifest
from .registry import TABLE_PATHS
class PackageBuilder:
    def __init__(self, root: Path, case_id: str, family: str, snapshot_version='1.0.0'):
        self.root=Path(root); self.case_id=case_id; self.family=family; self.snapshot_version=snapshot_version; self.rows={p:[] for p in TABLE_PATHS}
    def add(self, table: str, row: dict):
        if table not in self.rows: raise KeyError(table)
        self.rows[table].append(row); return self
    def write(self, converter='unknown', source_inputs=None):
        self.root.mkdir(parents=True,exist_ok=True)
        for table, rows in self.rows.items(): write_table(self.root/table, table, rows)
        (self.root/'README.md').write_text(f'# Canonical package {self.case_id}\n\nFamily: {self.family}\nSnapshot: {self.snapshot_version}\n',encoding='utf-8')
        return write_manifest(self.root,case_id=self.case_id,family=self.family,snapshot_version=self.snapshot_version,converter=converter,source_inputs=source_inputs)
