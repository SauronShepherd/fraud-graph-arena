# Fraud Graph Arena Modular Architecture Specification Pack

**Pack version:** 1.0  
**Pack ID:** `FGA-MODULAR-SPEC-PACK-1.0-20260726`  
**Parent normative pair:** `FGA-NORMATIVE-PAIR-9.0-20260726`  
**Date:** 26 July 2026

This pack contains **42 primary Markdown specifications**:

- 20 module functional specifications;
- 20 module technical architecture and test specifications;
- 1 high-level functional architecture/interactions specification;
- 1 high-level technical architecture/integration/whole-solution test strategy.

It does not replace the parent v9.0 normative pair. It decomposes that pair into independently testable modules and executable integration obligations.

## Architecture pair

- [High-Level Functional Architecture](architecture/HIGH_LEVEL_FUNCTIONAL_ARCHITECTURE.md)
- [High-Level Technical Architecture and Test Strategy](architecture/HIGH_LEVEL_TECHNICAL_ARCHITECTURE_AND_TEST_STRATEGY.md)

## Module pairs

### M01 — Application Shell and Navigation

- [Functional specification](modules/01-application-shell-navigation/FUNCTIONAL_SPECIFICATION.md)
- [Technical and test specification](modules/01-application-shell-navigation/TECHNICAL_AND_TEST_SPECIFICATION.md)

### M02 — Presentation System and Accessibility

- [Functional specification](modules/02-presentation-accessibility/FUNCTIONAL_SPECIFICATION.md)
- [Technical and test specification](modules/02-presentation-accessibility/TECHNICAL_AND_TEST_SPECIFICATION.md)

### M03 — Localization and Messaging

- [Functional specification](modules/03-localization-messaging/FUNCTIONAL_SPECIFICATION.md)
- [Technical and test specification](modules/03-localization-messaging/TECHNICAL_AND_TEST_SPECIFICATION.md)

### M04 — Asset and Resource Management

- [Functional specification](modules/04-asset-resource-management/FUNCTIONAL_SPECIFICATION.md)
- [Technical and test specification](modules/04-asset-resource-management/TECHNICAL_AND_TEST_SPECIFICATION.md)

### M05 — Audio and Radio

- [Functional specification](modules/05-audio-radio/FUNCTIONAL_SPECIFICATION.md)
- [Technical and test specification](modules/05-audio-radio/TECHNICAL_AND_TEST_SPECIFICATION.md)

### M06 — Client State and Synchronization

- [Functional specification](modules/06-client-state-synchronization/FUNCTIONAL_SPECIFICATION.md)
- [Technical and test specification](modules/06-client-state-synchronization/TECHNICAL_AND_TEST_SPECIFICATION.md)

### M07 — Identity, Account, Policy Receipt, and Privacy Requests

- [Functional specification](modules/07-identity-account-security/FUNCTIONAL_SPECIFICATION.md)
- [Technical and test specification](modules/07-identity-account-security/TECHNICAL_AND_TEST_SPECIFICATION.md)

### M08 — Career, Catalogue, and Progression

- [Functional specification](modules/08-career-catalogue-progression/FUNCTIONAL_SPECIFICATION.md)
- [Technical and test specification](modules/08-career-catalogue-progression/TECHNICAL_AND_TEST_SPECIFICATION.md)

### M09 — Round and Game-State Engine

- [Functional specification](modules/09-round-game-state/FUNCTIONAL_SPECIFICATION.md)
- [Technical and test specification](modules/09-round-game-state/TECHNICAL_AND_TEST_SPECIFICATION.md)

### M10 — Case Content and Rules

- [Functional specification](modules/10-case-content-rules/FUNCTIONAL_SPECIFICATION.md)
- [Technical and test specification](modules/10-case-content-rules/TECHNICAL_AND_TEST_SPECIFICATION.md)

### M11 — Investigation and Visibility Engine

- [Functional specification](modules/11-investigation-visibility/FUNCTIONAL_SPECIFICATION.md)
- [Technical and test specification](modules/11-investigation-visibility/TECHNICAL_AND_TEST_SPECIFICATION.md)

### M12 — Workspace Projection: List, Graph, Documents, and Semantic Navigation

- [Functional specification](modules/12-workspace-projection/FUNCTIONAL_SPECIFICATION.md)
- [Technical and test specification](modules/12-workspace-projection/TECHNICAL_AND_TEST_SPECIFICATION.md)

### M13 — Action, Quote, Command, and Settlement Orchestration

- [Functional specification](modules/13-action-command/FUNCTIONAL_SPECIFICATION.md)
- [Technical and test specification](modules/13-action-command/TECHNICAL_AND_TEST_SPECIFICATION.md)

### M14 — Investigation Economy and Credit Ledger

- [Functional specification](modules/14-economy-credit/FUNCTIONAL_SPECIFICATION.md)
- [Technical and test specification](modules/14-economy-credit/TECHNICAL_AND_TEST_SPECIFICATION.md)

### M15 — Save, Checkpoint, Draft History, and Recovery

- [Functional specification](modules/15-save-recovery/FUNCTIONAL_SPECIFICATION.md)
- [Technical and test specification](modules/15-save-recovery/TECHNICAL_AND_TEST_SPECIFICATION.md)

### M16 — Case File, Claims, Evidence Mapping, and Submission

- [Functional specification](modules/16-case-file-submission/FUNCTIONAL_SPECIFICATION.md)
- [Technical and test specification](modules/16-case-file-submission/TECHNICAL_AND_TEST_SPECIFICATION.md)

### M17 — Evaluation, Scoring, Endings, Verdicts, and Amendments

- [Functional specification](modules/17-evaluation-scoring-ending/FUNCTIONAL_SPECIFICATION.md)
- [Technical and test specification](modules/17-evaluation-scoring-ending/TECHNICAL_AND_TEST_SPECIFICATION.md)

### M18 — Leaderboard, Public Results, Moderation, and Disputes

- [Functional specification](modules/18-leaderboard-results/FUNCTIONAL_SPECIFICATION.md)
- [Technical and test specification](modules/18-leaderboard-results/TECHNICAL_AND_TEST_SPECIFICATION.md)

### M19 — Retrieval, Deterministic Resolver, and Provider Gateway

- [Functional specification](modules/19-retrieval-provider-gateway/FUNCTIONAL_SPECIFICATION.md)
- [Technical and test specification](modules/19-retrieval-provider-gateway/TECHNICAL_AND_TEST_SPECIFICATION.md)

### M20 — Publication Trust, Durable Workflow, and Runtime Control

- [Functional specification](modules/20-publication-workflow-runtime-control/FUNCTIONAL_SPECIFICATION.md)
- [Technical and test specification](modules/20-publication-workflow-runtime-control/TECHNICAL_AND_TEST_SPECIFICATION.md)

## Supporting files

- `manifest.json` — machine-readable document/module/dependency index.
- `SHA256SUMS.txt` — integrity digests for all files in the unpacked pack.

## Implementation rule

Twenty logical modules do not mean twenty microservices. The target is a modular monolith composed into `WEB`, `MAINTENANCE`, `EVALUATOR`, and `MIGRATE` runtime roles, with public contracts, strict data ownership, independent test kits, pairwise integration tests, capability-cluster tests, and complete-solution qualification.
