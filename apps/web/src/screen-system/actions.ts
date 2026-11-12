import { completeOpening, createAndStartRound } from "../api/client";
import { recalledRound, rememberRound } from "../state/session";
import type { ActionId, MachineEvent, ScreenContext } from "./contracts";
export interface ActionInput { context: ScreenContext; payload?: Record<string, string | number>; }
export interface ActionResult { event: MachineEvent; context?: ScreenContext; }
const pending = new Set<string>();
export const actions: Record<ActionId, (input: ActionInput) => Promise<ActionResult>> = {
  BEGIN: async () => ({ event: { type: "PATHS_REQUESTED" } }),
  RESUME_LAST_ROUND: async () => {
    const roundId = recalledRound();
    if (!roundId) throw new Error("NO_LAST_ROUND");
    return { event: { type: "ROUND_RESUMED", context: { roundId } }, context: { roundId } };
  },
  SELECT_PATH: async ({ payload }) => ({ event: { type: "PATH_SELECTED", context: { pathId: payload?.pathId as string } } }),
  BACK_TO_PATHS: async () => ({ event: { type: "RETURNED_TO_PATHS" } }),
  OPEN_CASE: async ({ context, payload }) => {
    const key = `${context.pathId}:${payload?.caseId ?? ""}`;
    if (pending.has(key)) throw new Error("ACTION_PENDING");
    pending.add(key);
    try { const round = await createAndStartRound(String(context.pathId), String(payload?.caseId)); rememberRound(round.id); return { event: { type: "CASE_OPENED", context: { roundId: round.id, page: 1 } }, context: { roundId: round.id, page: 1 } }; }
    finally { pending.delete(key); }
  },
  CHANGE_INTRO_PAGE: async ({ payload }) => ({ event: { type: "INTRO_PAGE_CHANGED", context: { page: Number(payload?.page ?? 1) } } }),
  COMPLETE_INTRO: async ({ context }) => { const round = await completeOpening(String(context.roundId)); return { event: { type: "INTRODUCTION_COMPLETED", context: { roundId: round.id } } }; },
  SKIP_INTRO: async ({ context }) => { const round = await completeOpening(String(context.roundId), "SKIPPED"); return { event: { type: "INTRODUCTION_SKIPPED", context: { roundId: round.id } } }; },
  RETURN_TO_CATALOGUE: async ({ context }) => ({ event: { type: "RETURNED_TO_CATALOGUE", context }, context })
};
