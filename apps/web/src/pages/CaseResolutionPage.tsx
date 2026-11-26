import { useEffect, useState } from "react";
import { Loading } from "../components/Loading";
import { ProblemPanel } from "../components/ProblemPanel";
import type { ComicPage, ComicSequence, ResolutionContext } from "../api/contracts";
import { useScreenData } from "../screen-system/useScreenData";
import { useScreenLocation } from "../screen-system/BrowserNavigationAdapter";
import { useScreenRuntime } from "../screen-system/ScreenRuntimeContext";
import { AudioControls, useAudioManager, useAudioPreferences } from "../narrative/AudioControls";
import type { AudioManager } from "../narrative/audio";
import { recordTranscriptOpen } from "../narrative/transcript";

interface ClosingNarrativeProps {
  pages: ComicPage[];
  sequence: ComicSequence;
  variant: string;
  audioManager: AudioManager;
}

function ClosingNarrative({ pages, sequence, variant, audioManager }: ClosingNarrativeProps) {
  const [failedImages, setFailedImages] = useState<Set<string>>(() => new Set());

  useEffect(() => {
    setFailedImages(new Set());
    if (!sequence.preload_next) return;
    pages.slice(1).forEach((page) => {
      const image = new Image();
      image.src = page.image_url;
    });
  }, [pages, sequence.preload_next]);

  function markImageFailed(page: ComicPage) {
    setFailedImages((current) => new Set(current).add(page.id));
    audioManager.record("MISSING_ASSET", page.id);
    audioManager.record("FALLBACK_ACTIVATED", page.id);
  }

  return <section className="resolution-dialogue" aria-labelledby="closing-title">
    <h2 id="closing-title">The closing note · {variant.toLowerCase()}</h2>
    {pages.map((page) => <article key={page.id}>
      <div className="comic-frame">
        {failedImages.has(page.id) ? <div className="comic-fallback" role="img" aria-label={page.alt_text}><span aria-hidden="true">🐾</span><p>Illustration unavailable. The transcript remains available to read.</p></div> : <img src={page.image_url} alt={page.alt_text} onError={() => markImageFailed(page)} />}
      </div>
      <div className="comic-caption">
        <p className="eyebrow">{page.id}</p>
        <h3 id={`closing-page-title-${page.id}`}>{page.title}</h3>
        <p>{page.caption || page.narration}</p>
        <details onToggle={(event) => recordTranscriptOpen(event.currentTarget, audioManager)}>
          <summary>Open transcript</summary>
          <p className="comic-transcript">{page.transcript || page.narration}</p>
        </details>
      </div>
    </article>)}
  </section>;
}

export function CaseResolutionPage() {
  const { context } = useScreenLocation();
  const { dispatchAction, transitionLocked } = useScreenRuntime();
  const audioManager = useAudioManager();
  const audioPreferences = useAudioPreferences(audioManager);
  const roundId = String(context.roundId ?? "");
  const { model, problem, retry } = useScreenData<ResolutionContext>("RESOLUTION_CONTEXT", { roundId }, roundId);
  if (problem) return <ProblemPanel problem={problem} onRetry={retry} />;
  if (!model) return <Loading message="Reading the final case receipt…" />;
  const sequence = model.closing?.sequence;
  const closureVariant = model.submission.ending_code === "CLEAN_COLLAR" ? "EXCELLENT" : model.submission.ending_code === "THE_SCENT_WENT_COLD" || model.submission.ending_code === "CASE_CLOSED_KENNEL_WRECKED" ? "PARTIAL" : "FAILED";
  const closing = sequence ? sequence.variants?.[closureVariant] ?? sequence.pages : [];
  return <main className="resolution-shell" data-resolution-screen="public" data-reduced-sensory={audioPreferences.reducedSensory ? "true" : "false"} data-reduced-motion={sequence?.reduced_motion_behavior ?? "static"} aria-labelledby="resolution-title">
    <header className="resolution-header"><p className="eyebrow">Case receipt · immutable submission</p><h1 id="resolution-title">{model.submission.ending_title}</h1><p className="resolution-score">{model.submission.score} / 1000 · {model.submission.ending_code}</p></header>
    <section className="resolution-verdict"><p>{model.submission.ending_narrative}</p><dl><div><dt>Evidence quality</dt><dd>{model.submission.dimensions.evidence_quality}</dd></div><div><dt>Relationship reading</dt><dd>{model.submission.dimensions.relationship_interpretation}</dd></div><div><dt>Protected actors</dt><dd>{model.submission.dimensions.protected_actor_discipline}</dd></div><div><dt>Efficiency</dt><dd>{model.submission.dimensions.efficiency}</dd></div><div><dt>Credits left</dt><dd>{model.submission.credits_remaining}</dd></div></dl></section>
    {sequence && closing.length > 0 && <ClosingNarrative pages={closing} sequence={sequence} variant={closureVariant} audioManager={audioManager} />}
    {sequence?.fictionalization_statement && <p className="comic-fictionalization">{sequence.fictionalization_statement}</p>}
    <AudioControls manager={audioManager} />
    <section className="resolution-ledger" aria-labelledby="ledger-title"><h2 id="ledger-title">Investigation ledger</h2><ol>{model.ledger.entries.map((entry) => <li key={entry.entry_id}>{entry.action.replaceAll("_", " ")} · {entry.entry_type.toLowerCase()} {entry.amount} · {entry.status.toLowerCase()} · {entry.balance_after} left</li>)}</ol></section>
    <button className="button secondary" type="button" disabled={transitionLocked} onClick={() => void dispatchAction("RETURN_TO_CATALOGUE")}>Back to Academy catalogue</button>
  </main>;
}
