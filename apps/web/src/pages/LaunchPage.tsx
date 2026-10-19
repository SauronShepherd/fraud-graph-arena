import { recalledRound } from "../state/session";
import { useScreenRuntime } from "../screen-system/ScreenRuntimeContext";

export function LaunchPage() {
  const { model, dispatchAction, transitionLocked } = useScreenRuntime();
  const lastRoundId = (model as { roundId?: string | null } | null)?.roundId ?? recalledRound();
  return (
    <main className="panel hero">
      <p className="eyebrow">Iteration 02 · Responsive investigation board</p>
      <h1 tabIndex={-1}>Fraud Graph Arena</h1>
      <p className="lede">
        The office is open. The board is empty. Please keep your accusations provisional.
      </p>
      <div className="actions">
        <button className="button" type="button" disabled={transitionLocked} onClick={() => void dispatchAction("BEGIN")}>Choose your trench coat</button>
        {lastRoundId ? (
          <button className="button secondary" type="button" disabled={transitionLocked} onClick={() => void dispatchAction("RESUME_LAST_ROUND", { roundId: lastRoundId })}>
            Return to the empty board
          </button>
        ) : null}
      </div>
    </main>
  );
}
