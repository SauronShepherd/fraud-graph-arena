# Iteration Evidence Bundle Format

## Purpose

Every Fraud Graph Arena iteration closes with a machine-readable evidence bundle and a human-readable summary. Evidence is created from a clean candidate commit and cannot be reconstructed after release from memory or terminal screenshots.

## Two-commit qualification model

Iteration qualification uses two preserved commits:

```text
C — qualified source candidate
│
└── E — evidence-only closure record
        └── immutable iteration tag
```

The evidence bundle stored in `E` identifies `C` through `source_commit`. The closure validator requires:

- `C` exists and is an ancestor of `E`;
- the candidate was clean when evidence was generated;
- changes from `C` to `E` are limited to `reports/iteration-00/`;
- all required source artefacts are present and digest-verified;
- all required independent approvals are approved;
- no closure-blocking gap or release exception remains;
- required I00 gates and tests pass;
- the evidence bundle digest is valid.

This model avoids a self-referential commit hash inside a file committed by the same commit.

## Required contents

The bundle records:

- evidence and iteration IDs;
- generation time;
- qualified source commit;
- status and closure eligibility;
- operating system, Python version, and clean-checkout observation;
- exact commands;
- required source artefacts and SHA-256 digests, using LF-canonical UTF-8 text fingerprints and byte-exact binary fingerprints;
- all fifteen universal gates with applicability rationale;
- normalized test results and reports;
- exceptions and known gaps;
- independent approvals;
- canonical bundle digest.

## Status meanings

- `passing`: every applicable requirement for closure is satisfied;
- `failing`: one or more implemented validation checks failed;
- `blocked`: implemented checks may pass, but an external prerequisite, approval, or clean-run condition is incomplete.

`not_applicable` is allowed only before a capability exists and must include a concrete reason. It does not mean “not run.”

## Commands

Side-effect-free validation:

```text
python scripts/validate_iteration_00.py
```

Generate evidence from a clean candidate commit:

```text
python scripts/validate_iteration_00.py --generate-evidence
```

After committing only the evidence directory, verify formal closure:

```text
python scripts/validate_iteration_00.py --require-closure
```

The immutable tag is created only through `scripts/create_iteration_00_tag.py` after closure passes.
