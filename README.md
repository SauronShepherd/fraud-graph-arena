# Fraud Graph Arena

This repository contains the qualified `I00 — Normative baseline and delivery constitution` release.

## Release identity

- **Branch:** `Iteration-00`
- **Normative pair:** `FGA-NORMATIVE-PAIR-10.0-20260726`
- **Immutable tag:** `fga-iteration-00-r1`
- **Evidence:** `reports/iteration-00/`
- **Player-facing capability:** none by design

Version 10.0 of the complete functional and technical specifications is the primary authority and explicitly supersedes version 9.0. The earlier v1.0 modular pack and build plan remain registered supporting artefacts where compatible with v10.0.

## Install the project and test tools

```text
python -m pip install -e ".[test]"
```

## Run all tests

```text
python -m pytest -v
```

## Validate without changing files

```text
python scripts/validate_iteration_00.py
```

## Verify formal closure

```text
python scripts/validate_iteration_00.py --require-closure
```

A qualified release returns exit code `0`, reports no closure blockers, and has an annotated `fga-iteration-00-r1` tag pointing to the evidence-only closure commit.

## Re-import the normative pair

The exact v10.0 source documents are already included. To verify or replace them with byte-identical approved sources:

```text
python scripts/import_normative_pair.py \
  /path/to/Fraud_Graph_Arena_Complete_Functional_Specification_v10.0.md \
  /path/to/Fraud_Graph_Arena_Complete_Technical_Architecture_and_Design_Specification_v10.0.md
```

The importer validates document identity and completeness, copies the sources under `specifications/normative-pair-v10.0/`, calculates canonical SHA-256 digests for governed text and byte-exact SHA-256 digests for binary archives, and updates the baseline registry.

## Release protocol

1. Commit all candidate source and governance changes.
2. Run the full pytest suite from a clean checkout.
3. Generate evidence with `python scripts/validate_iteration_00.py --generate-evidence`.
4. Commit only `reports/iteration-00/` as the closure record.
5. Verify closure with `--require-closure`.
6. Create the immutable tag through `python scripts/create_iteration_00_tag.py`.

The tag command refuses to replace an existing tag and refuses release when closure does not pass.
