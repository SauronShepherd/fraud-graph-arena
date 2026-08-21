import { useMemo } from "react";
import type { CatalogueSections } from "../api/contracts";
import { Loading } from "../components/Loading";
import { ProblemPanel } from "../components/ProblemPanel";
import { useScreenData } from "../screen-system/useScreenData";
import { useScreenRuntime } from "../screen-system/ScreenRuntimeContext";

export function PathSelectionPage() {
  const { model, problem, retry } = useScreenData<CatalogueSections>("CATALOGUE_SECTIONS", {}, "paths");
  const paths = useMemo(() => model?.sections ?? [], [model]);
  const { dispatchAction, transitionLocked } = useScreenRuntime();

  if (problem) return <ProblemPanel problem={problem} onRetry={retry} />;
  if (paths.length === 0) return <Loading message="Inspecting available paths…" />;

  return (
    <main className="panel">
      <p className="eyebrow">Step 1 of 4</p>
      <h1>Choose your trench coat</h1>
      <p>The Academy is the public laboratory. Ranked case files remain sealed and spoiler-free.</p>
      <div className="card-grid" aria-label="Investigation paths">
        {paths.map((path) => {
          const isOpen = path.status === "OPEN";
          const content = <>
              <span className="choice-title">{path.name}</span>
              <span>{path.description}</span>
              <small>{path.ranked ? "Ranked path" : "Training path"} · {path.status}</small>
              <small id={`${path.id}-access`}>{path.access_message}</small>
            </>;
          return isOpen ? <button className="choice-card" data-status={path.status} key={path.id} type="button" disabled={transitionLocked} aria-describedby={`${path.id}-access`} onClick={() => void dispatchAction("SELECT_PATH", { pathId: path.id })}>{content}</button> : <button className="choice-card" data-status={path.status} key={path.id} type="button" disabled aria-describedby={`${path.id}-access`}>{content}</button>;
        })}
      </div>
    </main>
  );
}
