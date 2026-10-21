import { useState } from "react";
import type { CatalogueSection } from "../api/contracts";
import { Loading } from "../components/Loading";
import { ProblemPanel } from "../components/ProblemPanel";
import { useScreenRuntime } from "../screen-system/ScreenRuntimeContext";

export function CaseSelectionPage() {
  const { model, problem, canRetry, retry, dispatchAction, transitionLocked } = useScreenRuntime();
  const section = model as CatalogueSection | null;
  const [openingCase, setOpeningCase] = useState<string | null>(null);

  async function openCase(caseId: string) {
    setOpeningCase(caseId);
    const result = await dispatchAction("OPEN_CASE", { caseId });
    if (!result) setOpeningCase(null);
  }

  if (problem) return <ProblemPanel problem={problem} onRetry={canRetry ? retry : undefined} />;
  if (!section) return <Loading message="Opening the catalogue…" />;

  return (
    <main className="panel">
      <p className="eyebrow">Step 2 of 4 · {section.path.name}</p>
      <h1 tabIndex={-1}>Choose a training file</h1>
      <p>Academy content teaches the real mechanics without exposing the real mysteries.</p>
      {section.cases.length === 0 ? (
        <section className="empty-state">
          <h2>No published cases yet</h2>
          <p>{section.path.access_message}</p>
          <button className="button secondary" type="button" disabled={transitionLocked} onClick={() => void dispatchAction("BACK_TO_PATHS")}>Choose another path</button>
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
