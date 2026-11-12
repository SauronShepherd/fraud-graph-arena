# Candidate run protocol

Before collecting a candidate result, freeze the exact package versions, fixture SHA, browser/OS/viewport, performance envelope, and run count. Each adapter must exercise the same node/edge IDs, selection sequence, fit/reset, zoom/pan, resize, detail update, and mount/unmount cleanup. Record hard requirements independently; a hard failure cannot be averaged away.

After a report is written, validate it locally with `python qualification/validate_report.py <report.json>`. The validator rejects stale fixture hashes, missing A/B runs, unmeasured hard requirements, incomplete environment metadata, and non-redistributable candidates.

The production rule remains: Cytoscape.js may proceed only if it passes every hard requirement, the envelope, license review, and lifecycle evidence. Otherwise the decision is blocked pending a normative specification change.
