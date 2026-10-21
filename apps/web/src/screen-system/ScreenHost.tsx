import { useCallback, useEffect, useRef, useState, type PropsWithChildren } from "react";
import type { LifecycleHookId, ScreenDefinition, ScreenId } from "./contracts";
import { lifecycle } from "./lifecycle";
import { ScreenAnnouncer } from "./ScreenAnnouncer";
import { ScreenRuntimeProvider, useScreenRuntime } from "./ScreenRuntimeContext";
import type { ScreenContext } from "./contracts";

function isRuntimeLifecycleHook(hook: LifecycleHookId): hook is Exclude<LifecycleHookId, "LOAD_SCREEN_MODEL"> { return hook !== "LOAD_SCREEN_MODEL"; }
function screenInstanceKey(screen: ScreenId, context: ScreenContext): string {
  const routeContext = Object.fromEntries(Object.entries(context).filter(([key]) => key !== "page"));
  return `${screen}:${JSON.stringify(routeContext)}`;
}

function ScreenEntryLifecycle({ definition, screen, context, onAnnounce }: { definition: ScreenDefinition; screen: ScreenId; context: ScreenContext; onAnnounce: (message: string) => void }) {
  const { model, problem } = useScreenRuntime();
  const entryKey = screenInstanceKey(screen, context);
  const enteredKey = useRef<string | null>(null);
  const entryState = !definition.onLoad.includes("LOAD_SCREEN_MODEL") ? "READY" : model !== null ? "MODEL" : problem !== null ? "PROBLEM" : "LOADING";
  const activationKey = `${entryKey}:${entryState}`;
  useEffect(() => {
    if (entryState === "LOADING" || enteredKey.current === activationKey) return;
    const services = {
      focusPrimaryHeading: () => document.querySelector<HTMLElement>(`[data-screen-id="${screen}"] h1, [data-screen-id="${screen}"] h2`)?.focus(),
      announce: onAnnounce,
      announceScreenName: screen.replaceAll("_", " "),
      abortReads: () => undefined
    };
    definition.onEnter.filter(isRuntimeLifecycleHook).forEach((hook) => lifecycle[hook](services));
    enteredKey.current = activationKey;
  }, [activationKey, definition, entryState, onAnnounce, screen]);
  return null;
}

export function ScreenHost({ definition, screen, context, children }: PropsWithChildren<{ definition: ScreenDefinition; screen: ScreenId; context: ScreenContext }>) {
  const [announcement, setAnnouncement] = useState(screen.replaceAll("_", " "));
  const instanceKey = screenInstanceKey(screen, context);
  const abortReads = useRef<() => void>(() => undefined);
  const registerAbortReads = useCallback((abort: () => void) => { abortReads.current = abort; }, []);
  useEffect(() => {
    const services = { focusPrimaryHeading: () => undefined, announce: setAnnouncement, announceScreenName: screen.replaceAll("_", " "), abortReads: () => abortReads.current() };
    definition.onLoad.filter(isRuntimeLifecycleHook).forEach((hook) => lifecycle[hook](services));
    return () => definition.onExit.filter(isRuntimeLifecycleHook).forEach((hook) => lifecycle[hook](services));
  }, [definition, instanceKey, screen]);
  return <ScreenRuntimeProvider definition={definition} context={context} onAbortReady={registerAbortReads}><ScreenEntryLifecycle definition={definition} screen={screen} context={context} onAnnounce={setAnnouncement} /><ScreenAnnouncer message={announcement} /><section data-screen-id={screen}>{children}</section></ScreenRuntimeProvider>;
}
