# ADR-001: canonical contract authority

`contracts/canonical/v1/canonical-model.json` and the registry derived from it are the single shape authority. Converters and validators consume the registry; they do not define case-specific headers.
