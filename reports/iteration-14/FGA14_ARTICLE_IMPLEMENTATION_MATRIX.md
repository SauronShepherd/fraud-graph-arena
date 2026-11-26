# FGA14 article ↔ implementation matrix

The article is closed only when every technical promise has a code path, a
test or a durable qualification receipt, and every material implementation
change is explained in the article.

| Article promise | Implementation | Verification | Status |
| --- | --- | --- | --- |
| A graph lead is not a verdict | `ethics/assessment.py`; `SUPPORTED`, `INCOMPLETE`, `UNSUPPORTED`; responsibility rule | Protected-actor, incomplete-anchor and public-response tests | PASS |
| Roles stay distinct | `contracts/ethics/fga14-ethical-contract.json`; role dimensions in `EthicalAssessment`; package review | Ethical-contract validation and response assertions | PASS |
| Benefit and harm stay distinct | Contract `impact_dimensions`; bounded `harm_penalty` | Contract validation; wrong-actor consequence test | PASS |
| Claims have a public vocabulary | `normalize_claim_type()` maps case-specific labels | Review of all canonical packages; statement assertions | PASS |
| Player-visible evidence can be cited | `SubmissionRequest.evidence_record_ids`; `EXPLICIT_ANCHORS` mode | Anchor-backed supported submission and insufficient-anchor tests | PASS |
| Legacy clients are explicit about their weaker audit trail | `CLAIM_DECLARATIONS` mode in the assessment | Existing FGA11 resolution suite plus response mode | PASS |
| Unsupported accusations have a consequence | `unsupported_accusation_count`, `harm_penalty`, protected-actor discipline | Wrong-tree test: one accusation, 150-point ethical consequence | PASS |
| Protected truth does not enter the response | Safe assessment fields; no evaluator rows in public data | Marker-field leak assertions; publication review truth-boundary check | PASS |
| Adversarial cases are part of the gate | `contracts/ethics/fga14-adversarial-cases.json` | Six-fixture validation and publication review | PASS |
| Submission receipts are immutable and replayable | Request hash includes evidence anchors; SQLite nested round-trip | Idempotency and SQLite restart tests; historical suite | PASS |
| Public package review runs before publication | `scripts/review_fga14_ethics.py`; 14-manifest review | Local receipt: 14 manifests, 6 fixtures, pass | PASS |
| Databricks uses the requested profile | `scripts/qualify_fga14_ethics.py` passes `--profile` through every CLI call | Live report: `profile=fga`, 13 canonical cases, read-only pass | PASS |
| Databricks scope remains honest | SQL Warehouse boundary reports no GraphFrames execution or truth query | Durable report fields `actual_engine_run=false`, `truth_source_queried=false` | PASS |
| Article visuals follow the series | Asset branch contains `1.png` newspaper and `2.png` infographic | Asset commit `9d504954cb483d780027de0ae327f3961e4f719e`; pinned URLs | PASS |
| Article structure follows FGA11–13 | Three-paragraph italic intro, nine parts, separators, receipt and caption | Content validation and editorial review | PASS |

## Deliberate limitations

- `CLAIM_DECLARATIONS` is retained for backwards compatibility. It is not
  described as equivalent to an anchor-backed audit trail; the response names
  the mode.
- The Databricks SQL Warehouse qualification validates the published safe
  boundary. It does not claim that GraphFrames, Zingg or protected truth ran in
  the warehouse.
- The adversarial fixtures are deterministic synthetic review cases. They are
  not a human fairness study or a substitute for a real player playtest.
