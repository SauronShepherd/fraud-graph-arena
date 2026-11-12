import type { LifecycleHookId } from "./contracts";
export interface LifecycleServices { focusPrimaryHeading: () => void; announce: (message: string) => void; abortReads: () => void; }
export const lifecycle: Record<LifecycleHookId, (services: LifecycleServices) => void> = {
  LOAD_SCREEN_MODEL: () => undefined,
  FOCUS_PRIMARY_HEADING: ({ focusPrimaryHeading }) => focusPrimaryHeading(),
  ANNOUNCE_SCREEN: ({ announce }) => announce("Screen ready"),
  ABORT_OBSOLETE_READS: ({ abortReads }) => abortReads()
};
