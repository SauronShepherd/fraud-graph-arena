import { useEffect, useState } from "react";
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

  return (
    <main className="panel board">
      <p className="eyebrow">Step 4 of 4 · Empty Academy board</p>
      <h1>{workspace.case.name}</h1>
      <dl className="case-facts">
        <div><dt>Path</dt><dd>{workspace.round.path_id}</dd></div>
        <div><dt>Case</dt><dd>{workspace.case.id}</dd></div>
        <div><dt>Status</dt><dd>{workspace.round.status}</dd></div>
        <div><dt>Evidence</dt><dd>{workspace.evidence_count}</dd></div>
        <div><dt>Suspects</dt><dd>{workspace.suspect_count}</dd></div>
      </dl>
      <section className="empty-board" aria-label="Empty Academy investigation workspace">
        <span className="question-mark" aria-hidden="true">?</span>
        <p>{workspace.board_message}</p>
        <p><strong>The right dog reached the right room carrying the right training file.</strong></p>
      </section>
      <Link className="button secondary" to={`/paths/${workspace.round.path_id}/cases`}>
        Back to Academy catalogue
      </Link>
    </main>
  );
}
