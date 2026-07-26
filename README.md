# Fraud Graph Arena

This repository is being built from the approved modular architecture pack and the complete end-to-end build and qualification plan.

## Current delivery state

- **Implemented iteration:** `I00 — Normative baseline and delivery constitution`
- **Implementation state:** all sixteen planned I00 file-atomic deliverables and subsequent corrective tasks are present and validated.
- **Closure state:** **blocked by a missing prerequisite**. The modular pack identifies `FGA-NORMATIVE-PAIR-9.0-20260726` as its parent authority, but the two v9.0 normative source documents were not supplied with the build inputs. The repository records this explicitly and never invents their digests.

## Install the project and test tools

Project metadata, runtime dependencies, test dependencies, and pytest configuration are defined in `pyproject.toml`.

```text
python -m pip install -e ".[test]"
```

An isolated virtual environment is recommended. Create and activate it using the standard mechanism for your environment before running the installation command.

## Run all tests

```text
python -m pytest -v
```

The pytest suite executes the governance regression tests and invokes the complete Iteration-00 validator without modifying tracked evidence files.

## Run the validator directly

```text
python scripts/validate_iteration_00.py
```

Require formal iteration closure, which is currently expected to return a blocking exit code until the parent pair is supplied:

```text
python scripts/validate_iteration_00.py --require-closure
```

See [the iteration evidence](reports/iteration-00/README.md) for exact status and remediation.
