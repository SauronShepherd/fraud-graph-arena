import type { GuardId, ScreenContext } from "./contracts";
export const guards: Record<GuardId, (context: ScreenContext) => boolean> = {
  REQUIRED_CONTEXT: (context) => Object.values(context).every((value) => value !== undefined && value !== ""),
  ROUTE_ALLOWED: () => true,
  ACTION_NOT_PENDING: (context) => context.pendingAction === undefined
};
