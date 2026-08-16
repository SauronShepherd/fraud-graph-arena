import { useEffect, useMemo, useState } from "react";
import { useNavigate, useParams, useSearchParams } from "react-router-dom";
import { ApiProblem, completeOpening, getOpening } from "../api/client";
import type { Opening, ProblemDetails } from "../api/contracts";
import { Loading } from "../components/Loading";
import { ProblemPanel } from "../components/ProblemPanel";
import { rememberRound } from "../state/session";

export function OpeningComicPage() {
  const { roundId = "" } = useParams();
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();
  const [opening, setOpening] = useState<Opening | null>(null);
  const [problem, setProblem] = useState<ProblemDetails | null>(null);
  const [finishing, setFinishing] = useState(false);
  const [imageFailed, setImageFailed] = useState(false);
  const pageNumber = Number(searchParams.get("page") ?? "1");

  useEffect(() => {
    let active = true;
    setProblem(null);
    getOpening(roundId)
      .then((result) => {
        if (!active) return;
        rememberRound(result.round.id);
        setOpening(result);
      })
      .catch((error: unknown) => {
        if (active && error instanceof ApiProblem) setProblem(error.problem);
      });
    return () => { active = false; };
  }, [roundId]);

  const currentIndex = useMemo(() => {
    if (!opening) return 0;
    if (!Number.isInteger(pageNumber)) return 0;
    return Math.min(Math.max(pageNumber - 1, 0), opening.sequence.pages.length - 1);
  }, [opening, pageNumber]);

  useEffect(() => {
    setImageFailed(false);
  }, [currentIndex]);

  async function finish(completion: "FINISHED" | "SKIPPED" = "FINISHED") {
    setFinishing(true);
    setProblem(null);
    try {
      const round = await completeOpening(roundId, completion);
      navigate(`/rounds/${encodeURIComponent(round.id)}/board`, { replace: true });
    } catch (error: unknown) {
      if (error instanceof ApiProblem) setProblem(error.problem);
      setFinishing(false);
    }
  }

  if (problem) return <ProblemPanel problem={problem} />;
  if (!opening) return <Loading message="Projecting the Academy briefing…" />;

  const page = opening.sequence.pages[currentIndex];
  const isFirst = currentIndex === 0;
  const isLast = currentIndex === opening.sequence.pages.length - 1;

  return (
    <main className="panel comic-shell">
      <p className="eyebrow">Step 3 of 4 · Opening comic</p>
      <h1>{opening.case.name}</h1>
      <p className="comic-progress" aria-live="polite">
        Page {currentIndex + 1} of {opening.sequence.pages.length}
      </p>
      <article className="comic-page" aria-labelledby="comic-page-title">
        <div className="comic-frame">
          {imageFailed ? (
            <div className="comic-fallback" role="img" aria-label={page.alt_text}>
              <span aria-hidden="true">🐾</span>
              <p>Illustration unavailable. The transcript remains evidence.</p>
            </div>
          ) : (
            <img src={page.image_url} alt={page.alt_text} onError={() => setImageFailed(true)} />
          )}
        </div>
        <div className="comic-caption">
          <p className="eyebrow">{page.id}</p>
          <h2 id="comic-page-title">{page.title}</h2>
          <p>{page.narration}</p>
        </div>
      </article>
      <div className="actions comic-actions">
        <button
          className="button secondary"
          type="button"
          disabled={isFirst || finishing}
          onClick={() => setSearchParams({ page: String(currentIndex) })}
        >
          Previous page
        </button>
        {!isLast ? (
          <button
            className="button"
            type="button"
            disabled={finishing}
            onClick={() => setSearchParams({ page: String(currentIndex + 2) })}
          >
            Next page
          </button>
        ) : (
          <button className="button" type="button" disabled={finishing} onClick={() => void finish()}>
            {finishing ? "Opening the board…" : "Enter the Academy"}
          </button>
        )}
        {opening.sequence.skippable && !isLast ? (
            <button className="text-button" type="button" disabled={finishing} onClick={() => void finish("SKIPPED")}>
            Skip introduction
          </button>
        ) : null}
      </div>
    </main>
  );
}
