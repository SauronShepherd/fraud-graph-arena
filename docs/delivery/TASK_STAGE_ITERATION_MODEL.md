# Task, Stage, and Iteration Model

**Model ID:** `FGA-DELIVERY-MODEL-1.0-20260726`

## Task

A task is one bounded modification to exactly one repository file. It may create or update that file, but cannot change a second file. Every task has a stable ID, exact path, bounded change, file-local acceptance statement, and traceability target.

A cross-file capability is split into multiple tasks and grouped in one stage. Generated output is treated as a separate task unless its generation and verification are the sole bounded change to the declared output file.

## Stage

A stage is a functionally cohesive set of file-atomic tasks. It closes only when all tasks are reviewed, file-local checks and stage tests pass, affected contracts are current, and no defect created by the stage is deferred.

## Iteration

An iteration is a releasable set of stages that leaves the repository coherent, runnable where executable capability exists, demonstrable, and cumulatively verified. Code existence is insufficient: applicable gates must pass and evidence must be reproduced from a clean checkout.

## Examples

Valid task: update `schemas/governance/baseline.schema.json` to add one availability rule and run its schema fixtures.

Invalid task: “update the schema, registry, docs, and tests.” That is four files and must become four tasks in one stage.

## Enforcement

The traceability graph records one `path` for each task. Governance validation rejects duplicate task IDs and any task mapped to more than one implementation path.
