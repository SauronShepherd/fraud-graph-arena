import type { GuardId, ScreenContext } from "./contracts";
export const guards: Record<GuardId, (context: ScreenContext) => boolean> = {
  REQUIRED_CONTEXT: (context) => Object.values(context).every((value) => value !== undefined && value !== ""),
  ACTION_NOT_PENDING: (context) => context.pendingAction === undefined,
  ROUND_ACTIVE: (context) => context.roundStatus === "ACTIVE",
  ROUND_INTRO_PENDING: (context) => context.roundStatus === "INTRO_PENDING"
};
