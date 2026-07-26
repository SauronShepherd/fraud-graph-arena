# Iteration 00 Qualification Evidence

**Iteration:** `I00 — Normative baseline and delivery constitution`  
**Normative pair:** `FGA-NORMATIVE-PAIR-10.0-20260726`  
**Branch:** `Iteration-00`  
**Qualified source commit:** `eb219e5a6bc49be2aa71720499e73f92e97e9744`  
**Immutable release tag:** `fga-iteration-00-r1`  
**Evidence status:** `passing`  
**Closure eligible:** `true`  
**Evidence bundle digest:** `31e4b49a6dafaaeec7d8d6d9742816a662aef52b70f43f8288c9e319678d12e3`

## Result

Iteration 00 revision 1 is formally qualified. It establishes the normative authority, delivery constitution, traceability model, ownership and review records, evidence schema, no-pass-no-progress release controls, and cross-platform baseline digest semantics promised by Article 00.

Iteration 00 intentionally contains no player-facing executable capability. The absence of a title screen, graph, case catalogue, database, or gameplay runtime is a scoped non-goal rather than an incomplete implementation.

## Cross-platform correction

Revision 1 corrects the original release's Windows checkout defect. UTF-8 Markdown, JSON, and text source artifacts are fingerprinted after line endings are canonicalized to LF, while binary archives remain byte-for-byte hashed. `.gitattributes` also forces deterministic LF text checkout. Windows CRLF and Unix LF therefore represent the same governed textual content.

## Authoritative specifications

The registered current normative pair is:

- `Fraud_Graph_Arena_Complete_Functional_Specification_v10.0.md` — canonical SHA-256 `c5e1e4d36a402ba988d9bc76349c27e0eb45e8281851b8cdd755336f3ef753d2`;
- `Fraud_Graph_Arena_Complete_Technical_Architecture_and_Design_Specification_v10.0.md` — canonical SHA-256 `fc577c5bee06de7f1a9e143f8442cdb804ac387814458ad0c3e6f4520bae97b1`.

Both documents declare `FGA-NORMATIVE-PAIR-10.0-20260726` and explicitly supersede the paired v9.0 specifications.

## Qualification results

- Full pytest suite: **11 passed**.
- Windows/Unix line-ending equivalence regression: **passed**.
- Deterministic Git text checkout policy: **passed**.
- Governance and traceability checks: **passed**.
- Schema positive and negative fixtures: **passed**.
- Normative source identity and digest checks: **passed**.
- Ownership and approval checks: **passed**.
- Secret scan: **passed**.
- Protected-truth scan: **passed**.
- Applicable gates `G01`, `G02`, `G04`, `G11`, `G14`, and `G15`: **passed**.
- Remaining gates: **not applicable in governance-only Iteration 00**.
- Closure-blocking gaps: **none**.
- Temporary exceptions: **none**.

Detailed machine-readable results are available in:

- `evidence.json`;
- `validation-results.json`;
- `pytest-results.txt`.

## Approval provenance

The personal-project release records three explicit approval roles:

- architecture governance: independent AI-assisted repository audit;
- quality engineering: automated clean-checkout qualification evidence;
- release management: project-owner authorization in the project conversation.

These records are transparent provenance for this personal project, not claims of external certification.

## Reproduce the qualification

From a clean checkout of the immutable revision-1 tag:

```text
python -m pip install -e ".[test]"
python -m pytest -v
python scripts/validate_iteration_00.py --require-closure
```

The tests must report `11 passed`. The final command must return exit code `0` with an empty `closure_blockers` list.
