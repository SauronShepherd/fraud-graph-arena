from __future__ import annotations
from pathlib import Path
from .csv_codec import write_table
from .manifest import write_manifest
from .registry import TABLE_PATHS
class PackageBuilder:
    def __init__(self, root: Path, case_id: str, family: str, snapshot_version='1.0.0', case_version='1.0.0'):
        self.root=Path(root); self.case_id=case_id; self.family=family; self.case_version=case_version; self.snapshot_version=snapshot_version; self.rows={p:[] for p in TABLE_PATHS}
    def add(self, table: str, row: dict):
        if table not in self.rows: raise KeyError(table)
        self.rows[table].append(row); return self
    def write(self, converter='unknown', source_inputs=None, source_dialect='manual-package-v1'):
        if not self.rows['config/case_profiles.csv']:
            self.rows['config/case_profiles.csv'].append({'case_id': self.case_id, 'profile_code': self.family, 'profile_name': self.family.title(), 'cumulative': 'false', 'starting_credits': 0, 'manual_cost': 0, 'zingg_cost': 0, 'graphframes_cost': 0, 'genie_cost': 0, 'genie_row_limit': 0, 'quote_required': 'false', 'no_result_charged': 'false', 'initial_item_count': 0, 'description': f'{self.family} package profile', 'snapshot_version': self.snapshot_version})
        if converter == 'unknown' and self.family in {'ACADEMY', 'PUPPY', 'ADULT', 'SENIOR'}:
            converter = {'ACADEMY': 'academy.csv.v1', 'PUPPY': 'puppy.csv.v1', 'ADULT': 'adult.csv.v1', 'SENIOR': 'senior.csv.v1'}[self.family]
            source_dialect = {'ACADEMY': 'academy-flat-csv-v1', 'PUPPY': 'puppy-flat-csv-v1', 'ADULT': 'adult-flat-csv-v1', 'SENIOR': 'senior-flat-csv-v1'}[self.family]
        self.root.mkdir(parents=True,exist_ok=True)
        for table, rows in self.rows.items(): write_table(self.root/table, table, rows)
        (self.root/'README.md').write_text(f'# Canonical package {self.case_id}\n\nFamily: {self.family}\nSnapshot: {self.snapshot_version}\n',encoding='utf-8')
        return write_manifest(self.root,case_id=self.case_id,family=self.family,case_version=self.case_version,snapshot_version=self.snapshot_version,converter=converter,source_inputs=source_inputs,source_dialect=source_dialect)
