import { createContext, useContext, type PropsWithChildren } from "react";
import type { DataSourceId, ScreenContext } from "./contracts";

export interface ScreenRuntimeValue {
  context: ScreenContext;
  dispatchAction: (action: string, payload?: Record<string, string | number>) => Promise<void>;
  loadScreenModel: (source: DataSourceId, context: ScreenContext) => Promise<unknown>;
  abortScreenLoad: () => void;
  transitionLocked: boolean;
}
const STANDALONE_RUNTIME: ScreenRuntimeValue = { context: {}, dispatchAction: async () => {}, loadScreenModel: async () => null, abortScreenLoad: () => {}, transitionLocked: false };
const RuntimeContext = createContext<ScreenRuntimeValue>(STANDALONE_RUNTIME);
export function ScreenRuntimeProvider({ value, children }: PropsWithChildren<{ value: ScreenRuntimeValue }>) { return <RuntimeContext.Provider value={value}>{children}</RuntimeContext.Provider>; }
export function useScreenRuntime(): ScreenRuntimeValue { return useContext(RuntimeContext); }
