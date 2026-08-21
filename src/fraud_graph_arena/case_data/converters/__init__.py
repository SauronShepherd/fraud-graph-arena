from .base import Converter, ConverterRegistry
registry = ConverterRegistry()
from .families import AcademyConverter, AdultConverter, PuppyConverter, SeniorConverter
for _converter in (AcademyConverter, PuppyConverter, AdultConverter, SeniorConverter):
    registry.register(_converter)
