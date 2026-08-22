import json
from pathlib import Path
from .base import Converter, ConverterRegistry
registry = ConverterRegistry()
from .families import AcademyConverter, AdultConverter, PuppyConverter, SeniorConverter
_mapping_path = Path(__file__).resolve().parents[4] / "config/converters/family-mappings.v1.json"
_mappings = json.loads(_mapping_path.read_text(encoding="utf-8"))["families"]
for _converter in (AcademyConverter, PuppyConverter, AdultConverter, SeniorConverter):
    mapping = _mappings.get(_converter.family)
    if not mapping or mapping.get("converter") != _converter.converter_id or mapping.get("source_dialect") != _converter.source_dialect:
        raise ValueError(f"converter mapping drift: {_converter.family}")
    registry.register(_converter)
