import { useEffect, useRef, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { ApiProblem, getWorkspace } from "../api/client";
import type { ProblemDetails, Workspace } from "../api/contracts";
import { Loading } from "../components/Loading";
import { ProblemPanel } from "../components/ProblemPanel";
import { rememberRound } from "../state/session";

export function BoardPage() {
  const { roundId = "" } = useParams();
  const [workspace, setWorkspace] = useState<Workspace | null>(null);
  const [problem, setProblem] = useState<ProblemDetails | null>(null);
  const [attempt, setAttempt] = useState(0);
  const [compact, setCompact] = useState(false);
  const boardRef = useRef<HTMLElement>(null);

  useEffect(() => {
    const element = boardRef.current;
    if (!element || typeof ResizeObserver === "undefined") return;
    const observer = new ResizeObserver(([entry]) => setCompact(entry.contentRect.width < 900));
    observer.observe(element);
    return () => observer.disconnect();
  }, []);

  useEffect(() => {
    let active = true;
    setProblem(null);
    getWorkspace(roundId)
      .then((result) => {
        if (!active) return;
        rememberRound(result.round.id);
        setWorkspace(result);
      })
      .catch((error: unknown) => {
        if (active && error instanceof ApiProblem) setProblem(error.problem);
      });
    return () => { active = false; };
  }, [roundId, attempt]);

  if (problem) return <ProblemPanel problem={problem} onRetry={() => setAttempt((n) => n + 1)} />;
  if (!workspace) return <Loading message="Recovering the training file from authoritative state…" />;

  const actions = [["Entity Resolution", "Identity comparison is not available in Academy yet."], ["Shared Fields", "Exact shared-field analysis is not available in Academy yet."], ["Evidence Search", "Evidence search will unlock when the case publishes evidence."], ["Case File", "Case-file construction is not available in the empty Academy round."]];
  return <main ref={boardRef} className={`board-shell${compact ? " board-shell--compact" : ""}`} aria-labelledby="board-title">
    <div className="board-scene" aria-hidden="true"><span className="lamp-glow" /><span className="desk-line" /></div>
    <section className="board-content">
      <header className="board-header"><div><p className="eyebrow">Active investigation · Detective Academy</p><h1 id="board-title">{workspace.case.name}</h1></div><div className="round-badge" aria-label={`Round status ${workspace.round.status}`}>{workspace.round.status}</div></header>
      <div className="board-layout">
        <section className="case-paper" aria-labelledby="paper-title"><p className="paper-kicker">{workspace.round.path_id}</p><h2 id="paper-title">Case paper</h2><dl className="case-facts"><div><dt>Case</dt><dd>{workspace.case.id}</dd></div><div><dt>Evidence revealed</dt><dd>{workspace.evidence_count}</dd></div><div><dt>Suspects identified</dt><dd>{workspace.suspect_count}</dd></div></dl><p className="paper-empty">{workspace.board_message}</p><p className="paper-note">The paper is waiting for evidence. Empty means empty; it is not a clue.</p></section>
        <section className="graph-panel" aria-labelledby="graph-title"><div className="graph-grid" aria-hidden="true" /><div className="graph-empty"><span className="graph-mark" aria-hidden="true">∅</span><h2 id="graph-title">Evidence graph</h2><p>No evidence has been revealed.</p><p className="muted">The graph will display published relationships here.</p><p className="sr-only" role="status">Graph contains zero entities and zero relationships.</p></div></section>
      </div>
      <section className="typewriter" aria-labelledby="actions-title"><div className="typewriter-top"><h2 id="actions-title">Investigation tools</h2><span className="tool-status">Academy tools · unavailable</span></div><div className="key-row">{actions.map(([label, reason]) => <button className="typewriter-key" key={label} type="button" disabled title={reason}><span>{label}</span><small>{reason}</small></button>)}</div></section>
      <footer className="board-footer"><p><strong>Training round:</strong> {workspace.round.id} · Future capabilities explain themselves when unavailable.</p><Link className="button secondary" to={`/paths/${workspace.round.path_id}/cases`}>Back to Academy catalogue</Link></footer>
    </section>
  </main>;
}
