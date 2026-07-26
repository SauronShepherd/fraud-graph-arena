# Fraud Graph Arena v10.0 Normative Pair

This directory contains the exact primary product and engineering authorities for Iteration 00:

- `Fraud_Graph_Arena_Complete_Functional_Specification_v10.0.md`;
- `Fraud_Graph_Arena_Complete_Technical_Architecture_and_Design_Specification_v10.0.md`.

Both documents declare `FGA-NORMATIVE-PAIR-10.0-20260726` and explicitly supersede the paired v9.0 specifications.

## Re-import and verify

From the repository root:

```text
python scripts/import_normative_pair.py \
  /path/to/Fraud_Graph_Arena_Complete_Functional_Specification_v10.0.md \
  /path/to/Fraud_Graph_Arena_Complete_Technical_Architecture_and_Design_Specification_v10.0.md
```

The importer refuses placeholders, summaries, wrong versions, wrong pair IDs, or implausibly short documents. It copies the source files, calculates LF-canonical SHA-256 digests for their UTF-8 text, and updates `config/governance/baseline.json`.
