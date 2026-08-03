import type { ProblemDetails } from "../api/contracts";

interface Props {
  problem: ProblemDetails;
  onRetry?: () => void;
}

export function ProblemPanel({ problem, onRetry }: Props) {
  return (
    <section className="problem" role="alert" aria-live="assertive">
      <p className="eyebrow">Case interrupted</p>
      <h2>{problem.title}</h2>
      <p>{problem.detail}</p>
      {problem.recovery ? <p className="recovery">{problem.recovery}</p> : null}
      <small>Reference: {problem.correlation_id}</small>
      {onRetry ? (
        <button type="button" onClick={onRetry}>
          Try the door again
        </button>
      ) : null}
    </section>
  );
}
