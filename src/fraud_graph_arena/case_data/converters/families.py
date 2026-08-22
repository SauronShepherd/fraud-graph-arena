from __future__ import annotations
from pathlib import Path
from typing import Any
from .base import Converter
from .common import convert_flat_csv

class FlatCsvFamilyConverter(Converter):
    family: str
    converter_id: str
    source_dialect: str
    def convert(self, source: Path, output: Path, mapping: dict[str, Any]) -> None:
        if mapping.get("source_dialect") not in (None, self.source_dialect):
            raise ValueError(f"unsupported source dialect for {self.family}: {mapping['source_dialect']}")
        convert_flat_csv(source, output, case_id=str(mapping["case_id"]), family=self.family, case_version=str(mapping.get("case_version", "1.0.0")), snapshot_version=str(mapping.get("snapshot_version", "1.0.0")), converter=self.converter_id)

class AcademyConverter(FlatCsvFamilyConverter):
    family = "ACADEMY"; converter_id = "academy.csv.v1"; source_dialect = "academy-flat-csv-v1"
class PuppyConverter(FlatCsvFamilyConverter):
    family = "PUPPY"; converter_id = "puppy.csv.v1"; source_dialect = "puppy-flat-csv-v1"
class AdultConverter(FlatCsvFamilyConverter):
    family = "ADULT"; converter_id = "adult.csv.v1"; source_dialect = "adult-flat-csv-v1"
class SeniorConverter(FlatCsvFamilyConverter):
    family = "SENIOR"; converter_id = "senior.csv.v1"; source_dialect = "senior-flat-csv-v1"
