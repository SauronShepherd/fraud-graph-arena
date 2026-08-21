import { recalledRound } from "../state/session";
import { ScreenLink } from "../screen-system/ScreenLink";

export function LaunchPage() {
  const lastRoundId = recalledRound();
  return (
    <main className="panel hero">
      <p className="eyebrow">Iteration 02 · Responsive investigation board</p>
      <h1>Fraud Graph Arena</h1>
      <p className="lede">
        The office is open. The board is empty. Please keep your accusations provisional.
      </p>
      <div className="actions">
        <ScreenLink className="button" to="/paths">Choose your trench coat</ScreenLink>
        {lastRoundId ? (
          <ScreenLink className="button secondary" to={`/rounds/${lastRoundId}/board`}>
            Return to the empty board
          </ScreenLink>
        ) : null}
      </div>
    </main>
  );
}
