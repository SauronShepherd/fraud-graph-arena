import { recalledRound } from "../state/session";
import { useScreenRuntime } from "../screen-system/ScreenRuntimeContext";
import { ScreenLink } from "../screen-system/ScreenLink";

export function LaunchPage() {
  const lastRoundId = recalledRound();
  const { dispatchAction, transitionLocked } = useScreenRuntime();
  return (
    <main className="panel hero">
      <p className="eyebrow">Fraud Graph Arena · Investigation board</p>
      <h1>Fraud Graph Arena</h1>
      <p className="lede">
        The office is open. The board is empty. Please keep your accusations provisional.
      </p>
      <div className="actions">
        <ScreenLink className="button" to="/paths" aria-disabled={transitionLocked} onClick={(event) => { event.preventDefault(); if (!transitionLocked) void dispatchAction("BEGIN"); }}>Choose your trench coat</ScreenLink>
        {lastRoundId ? (
          <button className="button secondary" type="button" disabled={transitionLocked} onClick={() => void dispatchAction("RESUME_LAST_ROUND")}>
            Return to the empty board
          </button>
        ) : null}
      </div>
    </main>
  );
}
