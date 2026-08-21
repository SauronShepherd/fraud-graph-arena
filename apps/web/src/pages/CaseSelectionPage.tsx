import { useState } from "react";
import type { CatalogueSection, ProblemDetails } from "../api/contracts";
import { Loading } from "../components/Loading";
import { ProblemPanel } from "../components/ProblemPanel";
import { rememberRound } from "../state/session";
import { ScreenLink } from "../screen-system/ScreenLink";
import { apiProblem, useScreenData } from "../screen-system/useScreenData";
import { useScreenLocation } from "../screen-system/BrowserNavigationAdapter";
import { actions } from "../screen-system/actions";

export function CaseSelectionPage() {
  const { context: routeContext } = useScreenLocation();
  const pathId = String(routeContext.pathId ?? "");
  const { model: section, problem: loadProblem, retry } = useScreenData<CatalogueSection>("CATALOGUE_SECTION", { pathId }, pathId);
  const [problem, setProblem] = useState<ProblemDetails | null>(null);
  const [openingCase, setOpeningCase] = useState<string | null>(null);
  const [openedRoundId, setOpenedRoundId] = useState<string | null>(null);

  async function openCase(caseId: string) {
    setOpeningCase(caseId);
    setProblem(null);
    try {
      const result = await actions.OPEN_CASE({ context: { pathId }, payload: { caseId } });
      const roundId = String(result.context?.roundId ?? "");
      rememberRound(roundId);
      setOpenedRoundId(roundId);
    } catch (error: unknown) {
      const details = apiProblem(error);
      if (details) setProblem(details);
      setOpeningCase(null);
    }
  }

  if (problem || loadProblem) return <ProblemPanel problem={problem ?? loadProblem!} onRetry={loadProblem ? retry : undefined} />;
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
          <ScreenLink className="button secondary" to="/paths">Choose another path</ScreenLink>
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
              {openedRoundId ? <ScreenLink auto className="button" to={`/rounds/${encodeURIComponent(openedRoundId)}/intro?page=1`}>Continue to introduction</ScreenLink> : null}
            </article>
          ))}
        </div>
      )}
    </main>
  );
}
