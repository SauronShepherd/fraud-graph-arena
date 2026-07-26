# Fraud Graph Arena v9.0 Normative Pair Import

Iteration 00 requires the two approved source documents that form `FGA-NORMATIVE-PAIR-9.0-20260726`:

- `Fraud_Graph_Arena_Complete_Functional_Specification_v9.0.md`
- `Fraud_Graph_Arena_Complete_Technical_Architecture_and_Design_Specification_v9.0.md`

The source documents must not be recreated, summarized, or replaced with placeholders. Import the exact approved files with:

```text
python scripts/import_normative_pair.py \
  /path/to/Fraud_Graph_Arena_Complete_Functional_Specification_v9.0.md \
  /path/to/Fraud_Graph_Arena_Complete_Technical_Architecture_and_Design_Specification_v9.0.md
```

The importer verifies document identity and version, copies the files into this directory, calculates SHA-256 digests, and updates the machine-readable baseline. Formal closure remains blocked until the imported files are committed, independent approvals are recorded, evidence is regenerated from a clean candidate commit, and the closure verifier passes.
