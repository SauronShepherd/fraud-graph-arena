import { completeOpening, createAndStartRound } from "../api/client";
import { rememberRound } from "../state/session";
import type { ActionId, MachineEvent, ScreenContext } from "./contracts";
export interface ActionInput { context: ScreenContext; payload?: Record<string, string | number>; instanceId?: string; }
export interface ActionResult { event: MachineEvent; context?: ScreenContext; }
const pending = new Set<string>();
const openCaseCommandKeys = new Map<string, string>();
function commandScope(pathId: unknown, caseId: unknown): string { return `${String(pathId ?? "")}:${String(caseId ?? "")}`; }
function getOrCreateCommandKey(scope: string): string {
  const cached = openCaseCommandKeys.get(scope);
  if (cached) return cached;
  const storageKey = `fga:open-case:${scope}`;
  try {
    const stored = globalThis.sessionStorage?.getItem(storageKey);
    if (stored) { openCaseCommandKeys.set(scope, stored); return stored; }
  } catch { /* Storage may be unavailable; retain the key for this page lifetime. */ }
  const key = crypto.randomUUID();
  openCaseCommandKeys.set(scope, key);
  try { globalThis.sessionStorage?.setItem(storageKey, key); } catch { /* In-memory replay still works until navigation/reload. */ }
  return key;
}
function clearCommandKey(scope: string): void {
  openCaseCommandKeys.delete(scope);
  try { globalThis.sessionStorage?.removeItem(`fga:open-case:${scope}`); } catch { /* The operation succeeded; storage cleanup is best effort. */ }
}
export const actions: Record<ActionId, (input: ActionInput) => Promise<ActionResult>> = {
  BEGIN: async () => ({ event: { type: "PATHS_REQUESTED" } }),
  RESUME_LAST_ROUND: async ({ payload }) => ({ event: { type: "ROUND_RESUME_REQUESTED", context: { roundId: String(payload?.roundId ?? "") } } }),
  SELECT_PATH: async ({ payload }) => ({ event: { type: "PATH_SELECTED", context: { pathId: payload?.pathId as string } } }),
  BACK_TO_PATHS: async () => ({ event: { type: "RETURNED_TO_PATHS" } }),
  OPEN_CASE: async ({ context, payload, instanceId }) => {
    const key = `${instanceId ?? "legacy"}:${context.pathId}:${payload?.caseId ?? ""}`;
    const scope = commandScope(context.pathId, payload?.caseId);
    if (pending.has(key)) throw new Error("ACTION_PENDING");
    pending.add(key);
    try { const round = await createAndStartRound(String(context.pathId), String(payload?.caseId), String(payload?.commandKey ?? getOrCreateCommandKey(scope))); clearCommandKey(scope); rememberRound(round.id); return { event: { type: "CASE_OPENED", context: { roundId: round.id, page: 1 } }, context: { roundId: round.id, page: 1 } }; }
    finally { pending.delete(key); }
  },
  CHANGE_INTRO_PAGE: async ({ payload }) => ({ event: { type: "INTRO_PAGE_CHANGED", context: { page: Number(payload?.page ?? 1) } } }),
  COMPLETE_INTRO: async ({ context }) => { const round = await completeOpening(String(context.roundId)); return { event: { type: "INTRODUCTION_COMPLETED", context: { roundId: round.id, roundStatus: round.status } } }; },
  SKIP_INTRO: async ({ context }) => { const round = await completeOpening(String(context.roundId), "SKIPPED"); return { event: { type: "INTRODUCTION_SKIPPED", context: { roundId: round.id, roundStatus: round.status } } }; },
  RETURN_TO_CATALOGUE: async ({ payload }) => ({ event: { type: "RETURNED_TO_CATALOGUE", context: { pathId: String(payload?.pathId ?? "") } } })
};
