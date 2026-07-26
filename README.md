# Fraud Graph Arena

This repository is being built from the approved modular architecture pack and the complete end-to-end build and qualification plan.

## Current delivery state

- **Implemented iteration:** `I00 — Normative baseline and delivery constitution`
- **Branch:** `Iteration-00`
- **Implementation state:** the sixteen planned I00 deliverables and corrective release-control tasks are present.
- **Qualification state:** **blocked, not failed**.
- **Immutable release tag:** not created. The repository deliberately removed the premature `fga-iteration-00` tag and now refuses to recreate it before formal closure passes.

The remaining external inputs are the exact approved v9.0 functional and technical source documents. Their attachment contents must be imported byte-for-byte; placeholders and summaries are rejected. Independent architecture, quality, and release approvals must then be recorded.

## Install the project and test tools

Project metadata, exactly pinned runtime dependencies, test dependencies, and pytest configuration are defined in `pyproject.toml`.

```text
python -m pip install -e ".[test]"
```

## Run all tests

```text
python -m pytest -v
```

Pytest executes the governance regression suite, including fixture-based successful closure, post-qualification tampering, placeholder-source rejection, and premature-tag prevention.

## Validate without changing files

Validation is side-effect-free by default:

```text
python scripts/validate_iteration_00.py
```

Formal closure is also side-effect-free and currently returns exit code `2` while source documents or approvals remain incomplete:

```text
python scripts/validate_iteration_00.py --require-closure
```

## Import the exact normative pair

```text
python scripts/import_normative_pair.py \
  /path/to/Fraud_Graph_Arena_Complete_Functional_Specification_v9.0.md \
  /path/to/Fraud_Graph_Arena_Complete_Technical_Architecture_and_Design_Specification_v9.0.md
```

The importer validates document identity and minimum completeness, copies the exact sources under `specifications/normative-pair-v9.0/`, calculates SHA-256 digests, and updates the baseline registry.

## Complete qualification

1. Commit the imported sources and updated baseline.
2. Record named, dated, evidence-backed independent approvals in `config/governance/approvals.yaml`.
3. Confirm the candidate checkout is clean.
4. Generate evidence:

```text
python scripts/validate_iteration_00.py --generate-evidence
```

5. Commit only `reports/iteration-00/` as the closure record.
6. Verify closure:

```text
python scripts/validate_iteration_00.py --require-closure
```

7. Create the immutable tag through the guarded command:

```text
python scripts/create_iteration_00_tag.py
```

The tag command refuses an existing tag and refuses to create a tag unless formal closure passes.

See [the Iteration-00 evidence summary](reports/iteration-00/README.md) for the current status.
