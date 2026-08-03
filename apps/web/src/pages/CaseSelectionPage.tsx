import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { ApiProblem, createAndStartRound, getSection } from "../api/client";
import type { CatalogueSection, ProblemDetails } from "../api/contracts";
import { Loading } from "../components/Loading";
import { ProblemPanel } from "../components/ProblemPanel";
import { rememberRound } from "../state/session";

export function CaseSelectionPage() {
  const { pathId = "" } = useParams();
  const navigate = useNavigate();
  const [section, setSection] = useState<CatalogueSection | null>(null);
  const [problem, setProblem] = useState<ProblemDetails | null>(null);
  const [openingCase, setOpeningCase] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    getSection(pathId)
      .then((result) => active && setSection(result))
      .catch((error: unknown) => {
        if (active && error instanceof ApiProblem) setProblem(error.problem);
      });
    return () => { active = false; };
  }, [pathId]);

  async function openCase(caseId: string) {
    setOpeningCase(caseId);
    setProblem(null);
    try {
      const round = await createAndStartRound(pathId, caseId);
      rememberRound(round.id);
      navigate(`/rounds/${encodeURIComponent(round.id)}/intro?page=1`);
    } catch (error: unknown) {
      if (error instanceof ApiProblem) setProblem(error.problem);
      setOpeningCase(null);
    }
  }

  if (problem) return <ProblemPanel problem={problem} />;
  if (!section) return <Loading message="Opening the catalogue…" />;

  return (
    <main className="panel">
      <p className="eyebrow">Step 2 of 4 · {section.path.name}</p>
      <h1>Choose a training file</h1>
      <p>Academy content teaches the real mechanics without exposing the real mysteries.</p>
      {section.cases.length === 0 ? (
        <section className="empty-state">
          <h2>No published cases yet</h2>
          <p>{section.path.access_message}</p>
          <Link className="button secondary" to="/paths">Choose another path</Link>
        </section>
      ) : (
        <div className="card-grid" aria-label={`${section.path.name} cases`}>
          {section.cases.map((caseItem) => (
            <article className="case-card" key={caseItem.id}>
              <p className="eyebrow">{caseItem.id}</p>
              <h2>{caseItem.name}</h2>
              <p>{caseItem.description}</p>
              <p>Status: <strong>{caseItem.status}</strong></p>
              <button
                className="button"
                type="button"
                disabled={caseItem.status !== "OPEN" || openingCase !== null}
                onClick={() => void openCase(caseItem.id)}
              >
                {openingCase === caseItem.id ? "Carrying the training file…" : "Open training case"}
              </button>
            </article>
          ))}
        </div>
      )}
    </main>
  );
}
