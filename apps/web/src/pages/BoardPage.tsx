import { useEffect, useRef, useState } from "react";
import type { Workspace } from "../api/contracts";
import { Loading } from "../components/Loading";
import { ProblemPanel } from "../components/ProblemPanel";
import { rememberRound } from "../state/session";
import { CasePaper } from "../board/CasePaper";
import { GraphViewport } from "../board/GraphViewport";
import { InvestigationActions } from "../board/InvestigationActions";
import { calculateBoardGeometry, selectBoardMode, type BoardGeometry } from "../board/layout";
import { DebugOverlay } from "../board/DebugOverlay";
import { useScreenRuntime } from "../screen-system/ScreenRuntimeContext";
import { useScreenLocation } from "../screen-system/BrowserNavigationAdapter";

const BOARD_ARTWORK = "/assets/board/v1/fga-investigation-board-canonical-v1.png";

export function BoardPage() {
  const { context: routeContext } = useScreenLocation();
  const roundId = String(routeContext.roundId ?? "");
  const { model, problem: loadProblem, canRetry, retry, dispatchAction, transitionLocked } = useScreenRuntime();
  const workspace = model as Workspace | null;
  const [compact, setCompact] = useState(false);
  const [geometry, setGeometry] = useState<BoardGeometry | null>(null);
  const boardRef = useRef<HTMLElement>(null);

  useEffect(() => {
    const element = boardRef.current;
    if (!element || typeof ResizeObserver === "undefined") return;
    const observer = new ResizeObserver(([entry]) => {
      setCompact(selectBoardMode(entry.contentRect.width, entry.contentRect.height) === "COMPACT");
      setGeometry(calculateBoardGeometry(entry.contentRect.width, entry.contentRect.height));
    });
    observer.observe(element);
    return () => observer.disconnect();
  }, []);

  useEffect(() => { if (workspace) rememberRound(workspace.round.id); else if (roundId) rememberRound(roundId); }, [workspace, roundId]);

  if (loadProblem) return <ProblemPanel problem={loadProblem} onRetry={canRetry ? retry : undefined} />;
  if (!workspace) return <Loading message="Recovering the training file from authoritative state…" />;

  return <main ref={boardRef} data-board-mode={compact ? "COMPACT" : "FULL"} className={`board-shell${compact ? " board-shell--compact" : ""}`} aria-labelledby="board-title">
    <div className="board-scene" aria-hidden="true"><img className="board-art" src={BOARD_ARTWORK} alt="" /><span className="lamp-glow" /><span className="desk-line" /></div>
    <section className="board-content">
      <header className="board-header" data-region="BOARD_STATUS"><div><p className="eyebrow">Active investigation · {workspace.path_name}</p><h1 id="board-title" tabIndex={-1}>{workspace.case.name}</h1></div><div className="round-badge" aria-label={`Round status ${workspace.round.status}`}>{workspace.round.status}</div></header>
      <div className="board-layout">
        <div data-region="CASE_PAPER" style={geometry ? { minHeight: geometry.regions.CASE_PAPER.height } : undefined}><CasePaper workspace={workspace} /></div><div data-region="GRAPH_VIEWPORT" style={geometry ? { minHeight: geometry.regions.GRAPH_VIEWPORT.height } : undefined}><GraphViewport /></div>
      </div>
      <div data-region="TYPEWRITER_CONTROLS"><InvestigationActions workspace={workspace} /></div>
      <footer className="board-footer"><p><strong>Training round:</strong> {workspace.round.id} · Future capabilities explain themselves when unavailable.</p><button className="button secondary" type="button" disabled={transitionLocked} onClick={() => void dispatchAction("RETURN_TO_CATALOGUE", { pathId: workspace.round.path_id })}>Back to Academy catalogue</button></footer>
    </section>
    <DebugOverlay mode={compact ? "COMPACT" : "FULL"} />
  </main>;
}
