from __future__ import annotations
from pathlib import Path
from typing import Any
from .base import Converter
from .common import convert_flat_csv

class FlatCsvFamilyConverter(Converter):
    family: str
    converter_id: str
    def convert(self, source: Path, output: Path, mapping: dict[str, Any]) -> None:
        convert_flat_csv(source, output, case_id=str(mapping["case_id"]), family=self.family, converter=self.converter_id)

class AcademyConverter(FlatCsvFamilyConverter):
    family = "ACADEMY"; converter_id = "academy.csv.v1"
class PuppyConverter(FlatCsvFamilyConverter):
    family = "PUPPY"; converter_id = "puppy.csv.v1"
class AdultConverter(FlatCsvFamilyConverter):
    family = "ADULT"; converter_id = "adult.csv.v1"
class SeniorConverter(FlatCsvFamilyConverter):
    family = "SENIOR"; converter_id = "senior.csv.v1"
