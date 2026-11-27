import { useState } from "react";
import type { CatalogueSection, ProblemDetails } from "../api/contracts";
import { Loading } from "../components/Loading";
import { ProblemPanel } from "../components/ProblemPanel";
import { ScreenLink } from "../screen-system/ScreenLink";
import { apiProblem, useScreenData } from "../screen-system/useScreenData";
import { useScreenLocation } from "../screen-system/BrowserNavigationAdapter";
import { useScreenRuntime } from "../screen-system/ScreenRuntimeContext";

export function CaseSelectionPage() {
  const { context: routeContext } = useScreenLocation();
  const pathId = String(routeContext.pathId ?? "");
  const { model: section, problem: loadProblem, retry } = useScreenData<CatalogueSection>("CATALOGUE_SECTION", { pathId }, pathId);
  const [problem, setProblem] = useState<ProblemDetails | null>(null);
  const [openingCase, setOpeningCase] = useState<string | null>(null);
  const { dispatchAction, transitionLocked } = useScreenRuntime();

  async function openCase(caseId: string) {
    setOpeningCase(caseId);
    setProblem(null);
    try {
      await dispatchAction("OPEN_CASE", { caseId });
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
      {section.academy_curriculum && <section className="academy-curriculum" aria-labelledby="academy-curriculum-title">
        <div className="academy-curriculum__header">
          <div><p className="eyebrow">FGA-16 · machine-checked field manual</p><h2 id="academy-curriculum-title">Academy qualification track</h2></div>
          <span className="academy-curriculum__count">{section.academy_curriculum.scenario_count} mechanics · one complete loop</span>
        </div>
        <p>Practice the same boundaries the automated suite checks: selection, evidence, resources, review and the final receipt.</p>
        <ol className="academy-curriculum__list">
          {section.academy_curriculum.scenarios.map((scenario) => <li key={scenario.scenario_id}>
            <div><strong>{scenario.title}</strong><small>{scenario.mechanic.replaceAll("_", " ")}</small></div>
            <p>{scenario.learning_objective}</p>
            <span>{scenario.tutorial_guidance[0]}</span>
          </li>)}
        </ol>
      </section>}
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
                disabled={caseItem.status !== "OPEN" || openingCase !== null || transitionLocked}
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
