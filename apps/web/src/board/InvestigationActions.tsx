import { useEffect, useRef, useState } from "react";
import type { Graph, InvestigationCommand, Workspace } from "../api/contracts";
import { getInvestigationHistory, submitManualHypothesis } from "../api/client";
import { message } from "../messages";

const relationshipTypes = [
  ["POSSIBLE_IDENTITY", "Possible identity"],
  ["POSSIBLE_CONTROL", "Possible control"],
  ["POSSIBLE_FLOW", "Possible flow"],
] as const;

function retryIdentity(): string {
  return globalThis.crypto?.randomUUID?.() ?? `hypothesis-${Date.now()}-${Math.random().toString(36).slice(2)}`;
}

export function InvestigationActions({ workspace, graph }: { workspace: Workspace; graph: Graph }) {
  const [feedback, setFeedback] = useState("");
  const [sourceId, setSourceId] = useState("");
  const [targetId, setTargetId] = useState("");
  const [relationshipType, setRelationshipType] = useState<string>("POSSIBLE_CONTROL");
  const [history, setHistory] = useState<InvestigationCommand[]>([]);
  const [historyLoading, setHistoryLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const retryKey = useRef<string | null>(null);

  const hypothesisAvailable = workspace.actions.some(
    (action) => action.id === "CREATE_HYPOTHESIS" && action.state === "AVAILABLE",
  );

  useEffect(() => {
    const controller = new AbortController();
    setHistory([]);
    setHistoryLoading(true);
    setFeedback("");
    setSourceId("");
    setTargetId("");
    retryKey.current = null;
    void getInvestigationHistory(workspace.round.id, controller.signal)
      .then((result) => setHistory(result.commands))
      .catch(() => {
        if (controller.signal.aborted) return;
        setFeedback("History is temporarily unavailable; recorded commands remain on the server.");
      })
      .finally(() => {
        if (!controller.signal.aborted) setHistoryLoading(false);
      });
    return () => controller.abort();
  }, [workspace.round.id]);

  const updateSource = (value: string) => {
    setSourceId(value);
    retryKey.current = null;
    if (value === targetId) setTargetId("");
  };

  const updateTarget = (value: string) => {
    setTargetId(value);
    retryKey.current = null;
  };

  const updateRelationship = (value: string) => {
    setRelationshipType(value);
    retryKey.current = null;
  };

  const submit = async () => {
    if (!sourceId || !targetId || sourceId === targetId || busy) return;
    setBusy(true);
    setFeedback("");
    const idempotencyKey = retryKey.current ?? retryIdentity();
    retryKey.current = idempotencyKey;
    try {
      const result = await submitManualHypothesis(workspace.round.id, {
        idempotency_key: idempotencyKey,
        source_record_id: sourceId,
        target_record_id: targetId,
        relationship_type: relationshipType,
      });
      setHistory((current) => current.some((item) => item.command_id === result.command_id)
        ? current
        : [...current, result]);
      retryKey.current = null;
      setFeedback(result.replayed
        ? "The same hypothesis was already recorded. No credits were charged and no evidence was revealed."
        : "Hypothesis recorded. No credits were charged and no evidence was revealed.");
    } catch {
      setFeedback("The hypothesis could not be confirmed. No evidence was revealed; retry without changing the request.");
    } finally {
      setBusy(false);
    }
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

      {hypothesisAvailable && (
        <fieldset className="hypothesis-form">
          <legend>Record a manual hypothesis</legend>
          <label htmlFor="hypothesis-source">From</label>
          <select id="hypothesis-source" disabled={busy} value={sourceId} onChange={(event) => updateSource(event.target.value)}>
            <option value="">Choose an available record</option>
            {graph.nodes.map((node) => (
              <option key={node.record_id} value={node.record_id}>{node.label} · {node.record_id}</option>
            ))}
          </select>
          <label htmlFor="hypothesis-target">To</label>
          <select id="hypothesis-target" disabled={busy} value={targetId} onChange={(event) => updateTarget(event.target.value)}>
            <option value="">Choose a different available record</option>
            {graph.nodes.filter((node) => node.record_id !== sourceId).map((node) => (
              <option key={node.record_id} value={node.record_id}>{node.label} · {node.record_id}</option>
            ))}
          </select>
          <label htmlFor="hypothesis-type">Hypothesis</label>
          <select id="hypothesis-type" disabled={busy} value={relationshipType} onChange={(event) => updateRelationship(event.target.value)}>
            {relationshipTypes.map(([value, label]) => <option key={value} value={value}>{label}</option>)}
          </select>
          <button type="button" disabled={!sourceId || !targetId || sourceId === targetId || busy} onClick={() => void submit()}>
            {busy ? "Recording…" : "Record hypothesis"}
          </button>
          <p>This is your note, not source evidence. It costs no credits and reveals nothing.</p>
        </fieldset>
      )}

      <section className="investigation-history" aria-labelledby="history-title">
        <h3 id="history-title">Manual hypothesis history</h3>
        {historyLoading ? <p>Checking the case history…</p> : history.length ? (
          <ol>
            {history.map((item) => (
              <li key={item.command_id}>
                <span>{item.source_record_id} → {item.target_record_id}</span>
                <small>{item.relationship_type} · {item.status}</small>
              </li>
            ))}
          </ol>
        ) : <p>No recorded hypotheses yet.</p>}
      </section>
    </section>
  );
}
