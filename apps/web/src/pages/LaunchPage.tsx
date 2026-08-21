import { recalledRound } from "../state/session";
import { ScreenLink } from "../screen-system/ScreenLink";
import { useScreenRuntime } from "../screen-system/ScreenRuntimeContext";

export function LaunchPage() {
  const lastRoundId = recalledRound();
  const { dispatchAction, transitionLocked } = useScreenRuntime();
  return (
    <main className="panel hero">
      <p className="eyebrow">Iteration 02 · Responsive investigation board</p>
      <h1>Fraud Graph Arena</h1>
      <p className="lede">
        The office is open. The board is empty. Please keep your accusations provisional.
      </p>
      <div className="actions">
        <ScreenLink className="button" to="/paths" aria-disabled={transitionLocked} onClick={(event) => { event.preventDefault(); if (!transitionLocked) void dispatchAction("BEGIN"); }}>Choose your trench coat</ScreenLink>
        {lastRoundId ? (
          <ScreenLink className="button secondary" to={`/rounds/${lastRoundId}/board`}>
            Return to the empty board
          </ScreenLink>
        ) : null}
      </div>
    </main>
  );
}
