import type { LifecycleHookId } from "./contracts";
export interface LifecycleServices { focusPrimaryHeading: () => void; announce: (message: string) => void; announceScreenName: string; abortReads: () => void; }
export const lifecycle: Record<Exclude<LifecycleHookId, "LOAD_SCREEN_MODEL">, (services: LifecycleServices) => void> = {
  FOCUS_PRIMARY_HEADING: ({ focusPrimaryHeading }) => focusPrimaryHeading(),
  ANNOUNCE_SCREEN: ({ announce, announceScreenName }) => announce(`${announceScreenName} ready`),
  ABORT_OBSOLETE_READS: ({ abortReads }) => abortReads()
};
