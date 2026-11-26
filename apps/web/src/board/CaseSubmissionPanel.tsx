import { useRef, useState } from "react";
import { submitCase } from "../api/client";
import type { Graph, Workspace } from "../api/contracts";
import { useScreenRuntime } from "../screen-system/ScreenRuntimeContext";

const claims = [
  ["IDENTITY_MERGE", "The matching contact pair supports one identity."],
  ["FALSE_MERGE_REJECTION", "The similar candidate stays separate."],
  ["DIRECTED_PAYMENT_CYCLE", "The payment relationships keep their direction."],
  ["COORDINATED_ADMINISTRATION", "Exact device and IP relationships support coordination."],
  ["BENIGN_SHARED_INFRASTRUCTURE", "Shared address and kiosk are not guilt by association."],
] as const;

function newKey(): string {
  return globalThis.crypto?.randomUUID?.() ?? `submission-${Date.now()}-${Math.random().toString(36).slice(2)}`;
}

export function CaseSubmissionPanel({ workspace, graph }: { workspace: Workspace; graph: Graph }) {
  const { dispatchAction, transitionLocked } = useScreenRuntime();
  const [suspects, setSuspects] = useState<string[]>([]);
  const [selectedClaims, setSelectedClaims] = useState<string[]>([]);
  const [busy, setBusy] = useState(false);
  const [feedback, setFeedback] = useState("");
  const retryKey = useRef<string | null>(null);
  const submitted = workspace.round.status === "SUBMITTED";

  const toggle = (value: string, values: string[], setValues: (next: string[]) => void) => {
    setValues(values.includes(value) ? values.filter((item) => item !== value) : [...values, value]);
    retryKey.current = null;
  };

  const submit = async () => {
    if (busy || submitted) return;
    setBusy(true);
    setFeedback("");
    const idempotencyKey = retryKey.current ?? newKey();
    retryKey.current = idempotencyKey;
    try {
      await submitCase(workspace.round.id, { idempotency_key: idempotencyKey, suspect_record_ids: suspects, evidence_claim_ids: selectedClaims, expected_round_version: workspace.round.version });
      retryKey.current = null;
      await dispatchAction("OPEN_RESOLUTION");
    } catch {
      setFeedback("The receipt could not be filed. Retry without changing the selected evidence; the same key protects the ledger.");
    } finally {
      setBusy(false);
    }
  };

  return (
    <fieldset className="case-submission-form" aria-labelledby="submission-title">
      <legend id="submission-title">Submit the case</legend>
      <p className="economy-receipt"><strong>{workspace.round.credits_remaining} credits left.</strong> Navigation and hypotheses are free. Identity comparison and graph analysis cost 3 credits each.</p>
      <p>Choose the records you are prepared to name. Similarity is a lead; the receipt is a conclusion.</p>
      <div className="submission-checklist">
        <h3>Suspects and actors</h3>
        {graph.nodes.map((node) => <label key={node.record_id}><input type="checkbox" checked={suspects.includes(node.record_id)} disabled={busy || submitted} onChange={() => toggle(node.record_id, suspects, setSuspects)} /> {node.label} <small>{node.record_id}</small></label>)}
      </div>
      <div className="submission-checklist">
        <h3>Evidence claims</h3>
        {claims.map(([id, label]) => <label key={id}><input type="checkbox" checked={selectedClaims.includes(id)} disabled={busy || submitted} onChange={() => toggle(id, selectedClaims, setSelectedClaims)} /> {label}</label>)}
      </div>
      <p className="submission-warning">The submission is immutable. The board will score the evidence quality, relationship reading, protected-actor discipline and credit use.</p>
      <button type="button" disabled={busy || submitted || transitionLocked} onClick={() => void submit()}>{busy ? "Filing receipt…" : submitted ? "Case submitted" : "Submit investigation"}</button>
      {feedback && <p role="alert">{feedback}</p>}
    </fieldset>
  );
}
