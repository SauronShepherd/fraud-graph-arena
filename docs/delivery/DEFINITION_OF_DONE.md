# Definition of Done

## Task done

A task is done only when its one exact file contains the bounded change, its file-local acceptance statement passes, traceability is current, and review is complete.

## Stage done

A stage is done only when every task is complete, stage tests pass, public contracts are compatible or explicitly migrated, and no stage-created defect is deferred.

## Iteration done

An iteration is done only when:

- all stages are complete;
- all applicable cumulative gates pass;
- the qualified source candidate was tested from a clean checkout;
- all required source artefacts are present and digest-verified;
- required independent approvals are named, dated, and evidence-backed;
- no critical test is skipped, quarantined, muted, or expected-failure;
- no rerun-only green result remains unexplained;
- no blocking gap, release exception, or unresolved severity-one/two defect remains;
- an evidence-only closure commit records the qualified source commit;
- formal closure verification passes;
- the immutable iteration tag is created only after closure passes.

The evidence-only closure commit may change only the governed evidence directory. Any source, configuration, schema, test, or documentation change after qualification requires a new candidate run.

## No Pass, No Progress

A failure creates corrective work in the same iteration. The next iteration does not begin until the complete cumulative gate passes again and reproducible evidence is recorded.
