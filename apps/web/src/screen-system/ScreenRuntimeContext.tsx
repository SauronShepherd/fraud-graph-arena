import { createContext, useContext, type PropsWithChildren } from "react";
import type { ScreenContext } from "./contracts";

export interface ScreenRuntimeValue { context: ScreenContext; dispatchAction: (action: string, payload?: Record<string, string | number>) => void; transitionLocked: boolean; }
const RuntimeContext = createContext<ScreenRuntimeValue | null>(null);
export function ScreenRuntimeProvider({ value, children }: PropsWithChildren<{ value: ScreenRuntimeValue }>) { return <RuntimeContext.Provider value={value}>{children}</RuntimeContext.Provider>; }
export function useScreenRuntime(): ScreenRuntimeValue { const value = useContext(RuntimeContext); if (!value) throw new Error("SCREEN_RUNTIME_OUTSIDE_PROVIDER"); return value; }
