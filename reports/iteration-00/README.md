# Iteration 00 Evidence

**Iteration:** `I00 — Normative baseline and delivery constitution`
**Evidence ID:** `EVID-I00-BASELINE`
**Status:** blocked, not failed

## Implemented outputs

All sixteen planned I00 file-atomic deliverables exist:

- baseline authority and digest registry;
- stable ID policy;
- task/stage/iteration model, ready and done definitions;
- machine-readable no-pass-no-progress policy;
- traceability model, schema, graph, owners, and change classification;
- evidence format, schema, generated bundle, and validation report.

Corrective delivery tasks also provide standard Python project metadata, exactly pinned runtime and test dependencies, pytest discovery configuration, actionable bootstrap diagnostics, and side-effect-free validator execution for automated tests.

## Passing checks

JSON Schema metaschemas and positive/negative fixtures, JSON/YAML/TOML syntax, all available source digests, Markdown structure and relative links, ID uniqueness, ownership coverage, traceability references and no-orphan rules, secret scan, protected-truth artifact scan, Python project metadata, pytest configuration, and the governance regression suite pass.

## Blocking prerequisite

`FGA-NORMATIVE-PAIR-9.0-20260726` is named as the parent authority by the supplied modular pack, but its functional and technical source documents are absent. The repository therefore refuses to mark `G01` or `G15` passing. No placeholder or guessed digest is used.

## Remediation

Add the two approved v9.0 normative documents under `specifications/normative-pair-v9.0/`, register their exact IDs, paths, and SHA-256 values in `config/governance/baseline.json`, set the baseline closure facts to complete, rerun the validation from a clean checkout, then record independent approvals.

## Install and run all tests

```text
python -m pip install -e ".[test]"
python -m pytest -v
```

Pytest reads its discovery and strictness configuration from `pyproject.toml`. The tests invoke the validator in a side-effect-free mode, so running the suite does not rewrite tracked evidence files.

## Run the validator directly

```text
python scripts/validate_iteration_00.py
python scripts/validate_iteration_00.py --require-closure
```

The first command validates the implementation and writes [`validation-results.json`](validation-results.json). The second intentionally blocks until the missing prerequisite is supplied.
