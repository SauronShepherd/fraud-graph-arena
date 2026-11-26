import { useEffect, useRef, useState } from "react";
import type { EntityResolutionAnalysis, EntityResolutionReview, Graph, IdentityCandidate, InvestigationCommand, Workspace } from "../api/contracts";
import { getEntityResolutionHistory, getInvestigationHistory, reviewEntityResolutionCandidate, runEntityResolution, submitManualHypothesis } from "../api/client";
import { message } from "../messages";

const relationshipTypes = [
  ["POSSIBLE_IDENTITY", "Possible identity"],
  ["POSSIBLE_CONTROL", "Possible control"],
  ["POSSIBLE_FLOW", "Possible flow"],
] as const;

function retryIdentity(): string {
  return globalThis.crypto?.randomUUID?.() ?? `hypothesis-${Date.now()}-${Math.random().toString(36).slice(2)}`;
}

function newResolutionKey(prefix: string): string {
  return globalThis.crypto?.randomUUID?.() ?? `${prefix}-${Date.now()}-${Math.random().toString(36).slice(2)}`;
}

function resolutionRetryStorageKey(roundId: string): string {
  return `fga09:identity-resolution-retry:${roundId}`;
}

function readResolutionRetryKeys(roundId: string): Map<string, string> {
  try {
    const raw = globalThis.sessionStorage?.getItem(resolutionRetryStorageKey(roundId));
    if (!raw) return new Map();
    const parsed: unknown = JSON.parse(raw);
    if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) return new Map();
    return new Map(
      Object.entries(parsed).filter(
        ([operationKey, idempotencyKey]) => typeof operationKey === "string" && typeof idempotencyKey === "string",
      ) as Array<[string, string]>,
    );
  } catch {
    return new Map();
  }
}

function persistResolutionRetryKeys(roundId: string, keys: Map<string, string>): void {
  try {
    const storageKey = resolutionRetryStorageKey(roundId);
    if (keys.size === 0) {
      globalThis.sessionStorage?.removeItem(storageKey);
      return;
    }
    globalThis.sessionStorage?.setItem(storageKey, JSON.stringify(Object.fromEntries(keys)));
  } catch {
    // Storage can be unavailable in privacy mode; the in-memory retry still works.
  }
}

export function InvestigationActions({ workspace, graph, selectedNodeId = null }: { workspace: Workspace; graph: Graph; selectedNodeId?: string | null }) {
  const [feedback, setFeedback] = useState("");
  const [sourceId, setSourceId] = useState("");
  const [targetId, setTargetId] = useState("");
  const [relationshipType, setRelationshipType] = useState<string>("POSSIBLE_CONTROL");
  const [history, setHistory] = useState<InvestigationCommand[]>([]);
  const [historyLoading, setHistoryLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [resolutionBusy, setResolutionBusy] = useState(false);
  const [analyses, setAnalyses] = useState<EntityResolutionAnalysis[]>([]);
  const [resolutionReviews, setResolutionReviews] = useState<EntityResolutionReview[]>([]);
  const retryKey = useRef<string | null>(null);
  const resolutionRetryKeys = useRef<Map<string, string>>(new Map());

  const hypothesisAvailable = workspace.actions.some(
    (action) => action.id === "CREATE_HYPOTHESIS" && action.state === "AVAILABLE",
  );
  const identityResolutionAvailable = workspace.actions.some(
    (action) => action.id === "COMPARE_IDENTITIES" && action.state === "AVAILABLE",
  );
  const selectedNode = selectedNodeId ? graph.nodes.find((node) => node.record_id === selectedNodeId) : undefined;

  useEffect(() => {
    const controller = new AbortController();
    setHistory([]);
    setHistoryLoading(true);
    setFeedback("");
    setSourceId("");
    setTargetId("");
    retryKey.current = null;
    resolutionRetryKeys.current = readResolutionRetryKeys(workspace.round.id);
    void getInvestigationHistory(workspace.round.id, controller.signal)
      .then((result) => setHistory(result.commands))
      .catch(() => {
        if (controller.signal.aborted) return;
        setFeedback("History is temporarily unavailable; recorded commands remain on the server.");
      })
      .finally(() => {
        if (!controller.signal.aborted) setHistoryLoading(false);
      });
    if (identityResolutionAvailable) {
      void getEntityResolutionHistory(workspace.round.id, controller.signal)
        .then((result) => {
          setAnalyses(result.analyses);
          setResolutionReviews(result.reviews);
        })
        .catch(() => {
          if (!controller.signal.aborted) setFeedback("The identity desk is temporarily unavailable; the graph itself has not changed.");
        });
    } else {
      setAnalyses([]);
      setResolutionReviews([]);
    }
    return () => controller.abort();
  }, [workspace.round.id, identityResolutionAvailable]);

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

  const useSelectedAs = (field: "source" | "target") => {
    if (!selectedNode) return;
    retryKey.current = null;
    if (field === "source") {
      setSourceId(selectedNode.record_id);
      if (targetId === selectedNode.record_id) setTargetId("");
    } else {
      setTargetId(selectedNode.record_id);
      if (sourceId === selectedNode.record_id) setSourceId("");
    }
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

  const compareIdentities = async () => {
    if (resolutionBusy) return;
    setResolutionBusy(true);
    setFeedback("");
    const operationKey = `${workspace.round.id}:${selectedNodeId ?? ""}`;
    const idempotencyKey = resolutionRetryKeys.current.get(operationKey) ?? newResolutionKey("identity-resolution");
    resolutionRetryKeys.current.set(operationKey, idempotencyKey);
    persistResolutionRetryKeys(workspace.round.id, resolutionRetryKeys.current);
    try {
      const result = await runEntityResolution(workspace.round.id, {
        idempotency_key: idempotencyKey,
        focus_record_id: selectedNodeId,
      });
      setAnalyses((current) => [...current.filter((item) => item.analysis_id !== result.analysis_id), result]);
      resolutionRetryKeys.current.delete(operationKey);
      persistResolutionRetryKeys(workspace.round.id, resolutionRetryKeys.current);
      setFeedback(result.replayed
        ? "The same identity analysis was replayed. No second charge was made."
        : `Identity analysis complete. ${result.charged_credits} credits charged; no ground truth or fraud verdict was revealed.`);
    } catch {
      setFeedback("The identity analysis could not be completed. Nothing was merged and no evidence was revealed.");
    } finally {
      setResolutionBusy(false);
    }
  };

  const reviewCandidate = async (candidate: IdentityCandidate, outcome: "ACCEPTED" | "REJECTED" | "UNRESOLVED") => {
    if (resolutionBusy) return;
    setResolutionBusy(true);
    const operationKey = `${workspace.round.id}:${candidate.candidate_id}:${outcome}`;
    const idempotencyKey = resolutionRetryKeys.current.get(operationKey) ?? newResolutionKey(`identity-review-${candidate.candidate_id}`);
    resolutionRetryKeys.current.set(operationKey, idempotencyKey);
    persistResolutionRetryKeys(workspace.round.id, resolutionRetryKeys.current);
    try {
      const result = await reviewEntityResolutionCandidate(workspace.round.id, candidate.candidate_id, {
        idempotency_key: idempotencyKey,
        outcome,
      });
      setResolutionReviews((current) => [...current.filter((item) => item.candidate_id !== result.candidate_id), result]);
      resolutionRetryKeys.current.delete(operationKey);
      persistResolutionRetryKeys(workspace.round.id, resolutionRetryKeys.current);
      setFeedback(`${outcome.toLowerCase()} review recorded. It is a player note, not a canonical merge or fraud verdict.`);
    } catch {
      setFeedback("The candidate review could not be recorded. The published graph remains unchanged.");
    } finally {
      setResolutionBusy(false);
    }
  };

  const latestAnalysis = analyses[analyses.length - 1];
  const recordLabel = (recordId: string) => graph.nodes.find((node) => node.record_id === recordId)?.label ?? recordId;
  const reviewFor = (candidateId: string) => {
    const matching = resolutionReviews.filter((review) => review.candidate_id === candidateId);
    const latest = matching.reduce<EntityResolutionReview | undefined>((current, review) => {
      if (!current) return review;
      const currentKey = `${current.created_at}:${current.review_id}`;
      const reviewKey = `${review.created_at}:${review.review_id}`;
      return reviewKey > currentKey ? review : current;
    }, undefined);
    return latest?.outcome;
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
          <p className="hypothesis-selection-context" role="status">
            {selectedNode ? `Selected record: ${selectedNode.label} · ${selectedNode.record_id}` : "Select a graph node or choose records below."}
          </p>
          <div className="hypothesis-shortcuts" aria-label="Use graph selection">
            <button type="button" disabled={!selectedNode || busy} onClick={() => useSelectedAs("source")}>Use selected as From</button>
            <button type="button" disabled={!selectedNode || busy} onClick={() => useSelectedAs("target")}>Use selected as To</button>
          </div>
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

      {identityResolutionAvailable && (
        <fieldset className="identity-resolution-form">
          <legend>Compare identities</legend>
          <p className="hypothesis-selection-context" role="status">
            {selectedNode ? `Focused record: ${selectedNode.label} · ${selectedNode.record_id}` : "Compare the published identity records, then review each candidate."}
          </p>
          <button type="button" disabled={resolutionBusy} onClick={() => void compareIdentities()}>
            {resolutionBusy ? "Comparing…" : "Run identity analysis"}
          </button>
          <p>This costs 3 credits. It produces explainable candidates only: similarity is not guilt, and review never creates a canonical merge.</p>
          {latestAnalysis && (
            <div className="identity-resolution-results" aria-live="polite">
              <p><strong>Analysis:</strong> {latestAnalysis.generation_mode} · snapshot {latestAnalysis.snapshot_version} · Zingg run: {latestAnalysis.actual_engine_run ? "yes" : "no; deterministic fallback"}</p>
              {latestAnalysis.exact_matches.length > 0 && <section aria-labelledby="exact-identity-title"><h3 id="exact-identity-title">Strict identity observations</h3><ul>{latestAnalysis.exact_matches.map((match) => <li key={match.match_id}>{recordLabel(match.left_record_id)} ↔ {recordLabel(match.right_record_id)} · {match.evidence_fields.join(", ")}</li>)}</ul></section>}
              <h3>Candidate review</h3>
              {latestAnalysis.candidates.length ? <ol>{latestAnalysis.candidates.map((candidate) => {
                const reviewed = reviewFor(candidate.candidate_id);
                return <li key={candidate.candidate_id} className="identity-candidate"><strong>{recordLabel(candidate.left_record_id)} ↔ {recordLabel(candidate.right_record_id)}</strong><span>{candidate.confidence_band} · {candidate.estimated_score.toFixed(2)} · {candidate.agreement_fields.length ? `agrees: ${candidate.agreement_fields.join(", ")}` : "no agreeing fields"}</span><span>{candidate.disagreement_fields.length ? `disagrees: ${candidate.disagreement_fields.join(", ")}` : "no conflicting fields"}</span>{candidate.missing_fields.length > 0 && <span>missing: {candidate.missing_fields.join(", ")}</span>}<small>{candidate.evidence_reasons.join(" ")}</small>{candidate.review_required && <div><button type="button" disabled={resolutionBusy} onClick={() => void reviewCandidate(candidate, "ACCEPTED")}>Accept candidate</button><button type="button" disabled={resolutionBusy} onClick={() => void reviewCandidate(candidate, "REJECTED")}>Reject candidate</button><button type="button" disabled={resolutionBusy} onClick={() => void reviewCandidate(candidate, "UNRESOLVED")}>Leave unresolved</button></div>}{reviewed && <em>Review: {reviewed.toLowerCase()}.</em>}</li>;
              })}</ol> : <p>No identity candidates were produced for this focus.</p>}
            </div>
          )}
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
