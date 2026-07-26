# Definition of Done

**Checklist ID:** `FGA-DOD-1.0-20260726`

## Task done

The declared file contains the bounded change, its local check passes, traceability is current, review is complete, and no unrelated file is smuggled into the task.

## Stage done

Every task is done, stage-specific tests pass, public contracts and compatibility fixtures are current, and no stage-created defect is deferred.

## Iteration done

- Every stage is done.
- Every applicable cumulative gate `G01`–`G15` passes.
- Not-applicable gates have explicit capability-based reasons.
- A clean checkout with fresh generated state reproduces the result.
- No critical failure is skipped, muted, quarantined, or marked expected-failure.
- A rerun-only green result does not count; the original cause is identified and corrected.
- No severity-1/2 defect, stale contract, unreviewed migration, missing report, or blocking prerequisite remains.
- The evidence bundle validates, contains exact commands, environment, seeds, digests, results, exceptions, gaps, and approvals, and records `closure_eligible: true`.

## No pass, no progress

A failure creates a corrective task in the same iteration. The next iteration cannot begin until the complete cumulative gate passes again. Temporary exceptions apply only to noncritical checks, require signed ownership and expiry, and cannot survive release qualification.
