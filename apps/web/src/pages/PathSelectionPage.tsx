import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { ApiProblem, listSections } from "../api/client";
import type { PathSummary, ProblemDetails } from "../api/contracts";
import { Loading } from "../components/Loading";
import { ProblemPanel } from "../components/ProblemPanel";

export function PathSelectionPage() {
  const navigate = useNavigate();
  const [paths, setPaths] = useState<PathSummary[]>([]);
  const [problem, setProblem] = useState<ProblemDetails | null>(null);
  const [attempt, setAttempt] = useState(0);

  useEffect(() => {
    let active = true;
    setProblem(null);
    listSections()
      .then((result) => active && setPaths(result.sections))
      .catch((error: unknown) => {
        if (active && error instanceof ApiProblem) setProblem(error.problem);
      });
    return () => { active = false; };
  }, [attempt]);

  if (problem) return <ProblemPanel problem={problem} onRetry={() => setAttempt((n) => n + 1)} />;
  if (paths.length === 0) return <Loading message="Inspecting available paths…" />;

  return (
    <main className="panel">
      <p className="eyebrow">Step 1 of 4</p>
      <h1>Choose your trench coat</h1>
      <p>The Academy is the public laboratory. Ranked case files remain sealed and spoiler-free.</p>
      <div className="card-grid" aria-label="Investigation paths">
        {paths.map((path) => {
          const isOpen = path.status === "OPEN";
          return (
            <button
              className="choice-card"
              data-status={path.status}
              key={path.id}
              type="button"
              disabled={!isOpen}
              aria-describedby={`${path.id}-access`}
              onClick={() => navigate(`/paths/${encodeURIComponent(path.id)}/cases`)}
            >
              <span className="choice-title">{path.name}</span>
              <span>{path.description}</span>
              <small>{path.ranked ? "Ranked path" : "Training path"} · {path.status}</small>
              <small id={`${path.id}-access`}>{path.access_message}</small>
            </button>
          );
        })}
      </div>
    </main>
  );
}
