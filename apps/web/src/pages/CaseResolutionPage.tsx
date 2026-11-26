import { Loading } from "../components/Loading";
import { ProblemPanel } from "../components/ProblemPanel";
import type { ResolutionContext } from "../api/contracts";
import { useScreenData } from "../screen-system/useScreenData";
import { useScreenLocation } from "../screen-system/BrowserNavigationAdapter";
import { useScreenRuntime } from "../screen-system/ScreenRuntimeContext";

export function CaseResolutionPage() {
  const { context } = useScreenLocation();
  const { dispatchAction, transitionLocked } = useScreenRuntime();
  const roundId = String(context.roundId ?? "");
  const { model, problem, retry } = useScreenData<ResolutionContext>("RESOLUTION_CONTEXT", { roundId }, roundId);
  if (problem) return <ProblemPanel problem={problem} onRetry={retry} />;
  if (!model) return <Loading message="Reading the final case receipt…" />;
  const closing = model.closing?.sequence.pages ?? [];
  return <main className="resolution-shell" data-resolution-screen="public" aria-labelledby="resolution-title">
    <header className="resolution-header"><p className="eyebrow">Case receipt · immutable submission</p><h1 id="resolution-title">{model.submission.ending_title}</h1><p className="resolution-score">{model.submission.score} / 1000 · {model.submission.ending_code}</p></header>
    <section className="resolution-verdict"><p>{model.submission.ending_narrative}</p><dl><div><dt>Evidence quality</dt><dd>{model.submission.dimensions.evidence_quality}</dd></div><div><dt>Relationship reading</dt><dd>{model.submission.dimensions.relationship_interpretation}</dd></div><div><dt>Protected actors</dt><dd>{model.submission.dimensions.protected_actor_discipline}</dd></div><div><dt>Efficiency</dt><dd>{model.submission.dimensions.efficiency}</dd></div><div><dt>Credits left</dt><dd>{model.submission.credits_remaining}</dd></div></dl></section>
    {closing.length > 0 && <section className="resolution-dialogue" aria-labelledby="closing-title"><h2 id="closing-title">The closing note</h2>{closing.map((page) => <article key={page.id}><h3>{page.title}</h3><p>{page.narration}</p></article>)}</section>}
    <section className="resolution-ledger" aria-labelledby="ledger-title"><h2 id="ledger-title">Investigation ledger</h2><ol>{model.ledger.entries.map((entry) => <li key={entry.entry_id}>{entry.action.replaceAll("_", " ")} · {entry.entry_type.toLowerCase()} {entry.amount} · {entry.status.toLowerCase()} · {entry.balance_after} left</li>)}</ol></section>
    <button className="button secondary" type="button" disabled={transitionLocked} onClick={() => void dispatchAction("RETURN_TO_CATALOGUE")}>Back to Academy catalogue</button>
  </main>;
}
