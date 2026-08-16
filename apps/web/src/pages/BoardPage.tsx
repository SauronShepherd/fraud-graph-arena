import { useEffect, useRef, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { ApiProblem, getWorkspace } from "../api/client";
import type { ProblemDetails, Workspace } from "../api/contracts";
import { Loading } from "../components/Loading";
import { ProblemPanel } from "../components/ProblemPanel";
import { rememberRound } from "../state/session";
import { CasePaper } from "../board/CasePaper";
import { GraphViewport } from "../board/GraphViewport";
import { InvestigationActions } from "../board/InvestigationActions";
import { selectBoardMode } from "../board/layout";
import { DebugOverlay } from "../board/DebugOverlay";

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
    const observer = new ResizeObserver(([entry]) => setCompact(selectBoardMode(entry.contentRect.width, entry.contentRect.height) === "COMPACT"));
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

  return <main ref={boardRef} data-board-mode={compact ? "COMPACT" : "FULL"} className={`board-shell${compact ? " board-shell--compact" : ""}`} aria-labelledby="board-title">
    <div className="board-scene" aria-hidden="true"><img className="board-art" src="/assets/board/v1/fallback.svg" alt="" /><span className="lamp-glow" /><span className="desk-line" /></div>
    <section className="board-content">
      <header className="board-header"><div><p className="eyebrow">Active investigation · {workspace.path_name}</p><h1 id="board-title">{workspace.case.name}</h1></div><div className="round-badge" aria-label={`Round status ${workspace.round.status}`}>{workspace.round.status}</div></header>
      <div className="board-layout">
        <CasePaper workspace={workspace} /><GraphViewport />
      </div>
      <InvestigationActions workspace={workspace} />
      <footer className="board-footer"><p><strong>Training round:</strong> {workspace.round.id} · Future capabilities explain themselves when unavailable.</p><Link className="button secondary" to={`/paths/${workspace.round.path_id}/cases`}>Back to Academy catalogue</Link></footer>
    </section>
    <DebugOverlay mode={compact ? "COMPACT" : "FULL"} />
  </main>;
}
