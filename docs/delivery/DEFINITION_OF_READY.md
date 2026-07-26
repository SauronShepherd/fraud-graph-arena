# Definition of Ready

**Checklist ID:** `FGA-DOR-1.0-20260726`

## Task ready

- Stable task ID and one exact repository path are assigned.
- The bounded change and file-local acceptance statement are unambiguous.
- Requirement, module, interaction, risk, or quality attribute traceability exists.
- Inputs and public contracts are available, versioned, and compatible.
- Required test data contains no unapproved secrets or protected truth.

## Stage ready

- All file-atomic tasks are enumerated.
- Stage outcome, test target, owners, reviewers, and failure cases are defined.
- Cross-module work names public contracts and integration edges; no shared internals are assumed.
- Migration, security, privacy, accessibility, localization, performance, and operational consequences are assessed.

## Iteration ready

- Prerequisite iterations are closed.
- Governing artifacts are registered and digest-verified.
- Applicable universal gates and explicit not-applicable reasons are known.
- Clean-checkout execution and evidence paths are defined.
- No unresolved severity-1/2 defect or missing constitutional prerequisite is hidden.

The plan validator consumes this checklist through the iteration policy.
