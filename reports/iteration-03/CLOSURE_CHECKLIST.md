# I03 closure checklist

The source implementation and automated qualification are complete. Artwork approval is recorded for the canonical board asset. Release closure must still include the clean candidate and immutable evidence steps below:

1. Approved canonical board artwork and provenance reference: `fga-investigation-board-canonical-v1.png`; project-owner approval recorded in the task conversation on 2026-08-21.
2. Truthful manifest approval and asset digest update in `apps/web/public/assets/board/v1/manifest.json`.
3. A clean candidate commit containing the qualified source and evidence changes.
4. Two independent clean runs of `python scripts/run_iteration_03_gate.py` against that candidate.
5. A closure record linking the candidate commit, both gate reports, prior immutable lineage, and the approval reference.
6. An evidence-only closure commit and immutable I03 tag after the closure record validates.

The artwork gate may now pass; I03 still must not be tagged as qualified until the clean candidate, dual gate runs, closure record, and immutable tag steps are complete.
