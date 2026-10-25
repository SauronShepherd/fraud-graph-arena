import { useEffect, useRef, useState } from "react";
import type { Graph, InvestigationCommand, Workspace } from "../api/contracts";
import { getInvestigationHistory, submitManualHypothesis } from "../api/client";
import { message } from "../messages";

const relationshipTypes = [
  ["POSSIBLE_IDENTITY", "Possible identity"],
  ["POSSIBLE_CONTROL", "Possible control"],
  ["POSSIBLE_FLOW", "Possible flow"],
] as const;

export function InvestigationActions({ workspace, graph }: { workspace: Workspace; graph: Graph }) {
  const [feedback, setFeedback] = useState("");
  const [sourceId, setSourceId] = useState("");
  const [targetId, setTargetId] = useState("");
  const [relationshipType, setRelationshipType] = useState<string>("POSSIBLE_CONTROL");
  const [history, setHistory] = useState<InvestigationCommand[]>([]);
  const [busy, setBusy] = useState(false);
  const retryKey = useRef<string | null>(null);

  useEffect(() => {
    let alive = true;
    void getInvestigationHistory(workspace.round.id)
      .then((result) => {
        if (alive) setHistory(result.commands);
      })
      .catch(() => {
        if (alive) setFeedback("History is temporarily unavailable; recorded commands remain on the server.");
      });
    return () => {
      alive = false;
    };
  }, [workspace.round.id]);

  const submit = async () => {
    if (!sourceId || !targetId || sourceId === targetId || busy) return;
    setBusy(true);
    setFeedback("");
    try {
      retryKey.current ??= crypto.randomUUID();
      const result = await submitManualHypothesis(workspace.round.id, {
        idempotency_key: retryKey.current,
        source_record_id: sourceId,
        target_record_id: targetId,
        relationship_type: relationshipType,
      });
      setHistory((current) => current.some((item) => item.command_id === result.command_id)
        ? current
        : [...current, result]);
      retryKey.current = null;
      setFeedback("Hypothesis recorded. No credits were charged and no evidence was revealed.");
    } catch {
      setFeedback("The hypothesis could not be recorded. No evidence was revealed; retry when the service is available.");
    } finally {
      setBusy(false);
    }
  };

  const resetRetryKey = () => {
    retryKey.current = null;
  };
  const updateSource = (value: string) => {
    setSourceId(value);
    resetRetryKey();
  };
  const updateTarget = (value: string) => {
    setTargetId(value);
    resetRetryKey();
  };
  const updateRelationship = (value: string) => {
    setRelationshipType(value);
    resetRetryKey();
  };

  return (
    <section className="typewriter" aria-labelledby="actions-title">
      <div className="typewriter-top">
        <h2 id="actions-title">{message("board.tools")}</h2>
        <span className="tool-status" role="status">{feedback || message("board.toolsUnavailable")}</span>
      </div>

      <div className="key-row">
        {(workspace.actions ?? []).map((action) => (
          <button
            className="typewriter-key"
            data-action-id={action.id}
            data-state={action.state}
            key={action.id}
            type="button"
            aria-disabled={action.state !== "AVAILABLE"}
            aria-describedby={`reason-${action.id}`}
            title={action.reason}
            onClick={() => {
              if (action.state !== "AVAILABLE") setFeedback(action.reason);
            }}
          >
            <span>{action.id.replaceAll("_", " ")}</span>
            <small id={`reason-${action.id}`}>{action.reason}</small>
          </button>
        ))}
      </div>

      {workspace.case.id === "ACADEMY_T02" && (
        <fieldset className="hypothesis-form">
          <legend>Record a manual hypothesis</legend>
          <label>
            From
            <select disabled={busy} value={sourceId} onChange={(event) => updateSource(event.target.value)}>
              <option value="">Choose an available record</option>
              {graph.nodes.map((node) => (
                <option key={node.record_id} value={node.record_id}>{node.label} · {node.record_id}</option>
              ))}
            </select>
          </label>
          <label>
            To
            <select disabled={busy} value={targetId} onChange={(event) => updateTarget(event.target.value)}>
              <option value="">Choose a different available record</option>
              {graph.nodes.filter((node) => node.record_id !== sourceId).map((node) => (
                <option key={node.record_id} value={node.record_id}>{node.label} · {node.record_id}</option>
              ))}
            </select>
          </label>
          <label>
            Hypothesis
            <select disabled={busy} value={relationshipType} onChange={(event) => updateRelationship(event.target.value)}>
              {relationshipTypes.map(([value, label]) => <option key={value} value={value}>{label}</option>)}
            </select>
          </label>
          <button type="button" disabled={!sourceId || !targetId || sourceId === targetId || busy} onClick={() => void submit()}>
            {busy ? "Recording…" : "Record hypothesis"}
          </button>
          <p>This is your note, not source evidence. It costs no credits and reveals nothing.</p>
        </fieldset>
      )}

      <section aria-label="Investigation history">
        <h3>Manual hypothesis history</h3>
        {history.length ? (
          <ol>
            {history.map((item) => (
              <li key={item.command_id}>{item.source_record_id} → {item.target_record_id} · {item.relationship_type} · {item.status}</li>
            ))}
          </ol>
        ) : <p>No recorded hypotheses yet.</p>}
      </section>
    </section>
  );
}
