import { createContext, useCallback, useContext, useEffect, useRef, useState, type PropsWithChildren } from "react";
import { ApiProblem } from "../api/client";
import type { Opening, ProblemDetails } from "../api/contracts";
import { dataSources, type ScreenModel } from "./dataSources";
import { actions, type ActionResult } from "./actions";
import { resolveTransition } from "./machine";
import { screenDefinitions } from "./definitions";
import type { ActionId, ScreenContext, ScreenDefinition } from "./contracts";
import { useTransitionCoordinator } from "./TransitionCoordinator";

export interface ScreenRuntimeValue { context: ScreenContext; model: ScreenModel | null; problem: ProblemDetails | null; canRetry: boolean; retry: () => void; dispatchAction: (action: ActionId, payload?: Record<string, string | number>) => Promise<ActionResult | null>; transitionLocked: boolean; }
const RuntimeContext = createContext<ScreenRuntimeValue | null>(null);
function runtimeProblem(error: unknown, screenId: string): ProblemDetails {
  if (error instanceof ApiProblem) return error.problem;
  return { type: "https://fraud-graph-arena.invalid/problems/screen-runtime", title: "This screen could not continue", status: 500, detail: "The screen runtime could not complete the requested operation.", instance: screenId, code: "SCREEN_RUNTIME_FAILURE", correlation_id: "client-side", recovery: "Reload the screen and try again." };
}
export function ScreenRuntimeProvider({ definition, context, onAbortReady, children }: PropsWithChildren<{ definition: ScreenDefinition; context: ScreenContext; onAbortReady?: (abort: () => void) => void }>) {
  const coordinator = useTransitionCoordinator();
  const [model, setModel] = useState<ScreenModel | null>(null);
  const [loadedKey, setLoadedKey] = useState<string | null>(null);
  const [problem, setProblem] = useState<ProblemDetails | null>(null);
  const [problemKey, setProblemKey] = useState<string | null>(null);
  const [attempt, setAttempt] = useState(0);
  const [actionPending, setActionPending] = useState(false);
  const [retryKind, setRetryKind] = useState<"LOAD" | "ACTION" | null>(null);
  const actionPendingRef = useRef(false);
  const instanceId = useRef(`${definition.id}:${Math.random().toString(36).slice(2)}`);
  const retryAction = useRef<{ action: ActionId; payload?: Record<string, string | number> } | null>(null);
  const dataContext = Object.fromEntries(Object.entries(context).filter(([key]) => key !== "page"));
  const contextKey = JSON.stringify(dataContext);
  const screenKey = `${definition.id}:${contextKey}:${attempt}`;
  useEffect(() => {
    const controller = new AbortController();
    const sourceToken = coordinator.captureToken();
    retryAction.current = null;
    setModel(null); setLoadedKey(null); setProblem(null); setProblemKey(null); setRetryKind(null);
    onAbortReady?.(() => controller.abort());
    if (!definition.onLoad.includes("LOAD_SCREEN_MODEL")) return () => { controller.abort(); onAbortReady?.(() => undefined); };
    dataSources[definition.data_source](context, controller.signal)
      .then((value) => {
        if (controller.signal.aborted) return;
        if (definition.id === "CASE_INTRODUCTION" && (value as Opening).round.status === "ACTIVE") {
          const plan = resolveTransition(definition, context, { type: "INTRODUCTION_ALREADY_COMPLETED", context: { roundId: context.roundId, roundStatus: "ACTIVE" } }, screenDefinitions);
          if (plan && coordinator.request(plan, sourceToken)) return;
        }
        setModel(value); setLoadedKey(screenKey);
      })
      .catch((error: unknown) => {
        if (controller.signal.aborted) return;
        const details = runtimeProblem(error, definition.id);
        if (definition.id === "INVESTIGATION_BOARD" && details.code === "INTRO_REQUIRED") {
          const plan = resolveTransition(definition, context, { type: "INTRODUCTION_REQUIRED", context: { roundId: context.roundId, page: 1, roundStatus: "INTRO_PENDING" } }, screenDefinitions);
          if (plan && coordinator.request(plan, sourceToken)) return;
        }
        setProblem(details);
        setProblemKey(screenKey);
        setRetryKind("LOAD");
      });
    return () => { controller.abort(); onAbortReady?.(() => undefined); };
  }, [contextKey, definition.data_source, definition.id, attempt, screenKey, onAbortReady]);
  async function dispatchAction(action: ActionId, payload?: Record<string, string | number>): Promise<ActionResult | null> {
    if (coordinator.transitionLocked || actionPendingRef.current) return null;
    const sourceToken = coordinator.captureToken();
    const declaredAction = definition.actions.find((candidate) => candidate.id === action);
    if (!declaredAction) { setProblem(runtimeProblem(new Error(`ACTION_NOT_ALLOWED:${action}`), definition.id)); setProblemKey(screenKey); setRetryKind(null); return null; }
    const handler = actions[declaredAction.handler];
    if (!handler) { setProblem(runtimeProblem(new Error(`UNKNOWN_ACTION:${action}`), definition.id)); setProblemKey(screenKey); setRetryKind(null); return null; }
    actionPendingRef.current = true;
    setActionPending(true);
    setProblem(null);
    setProblemKey(null);
    setRetryKind(null);
    retryAction.current = null;
    try {
      const result = await handler({ context, payload, instanceId: instanceId.current });
      const plan = resolveTransition(definition, context, result.event, screenDefinitions);
      if (!plan) { setProblem(runtimeProblem(new Error(`UNRESOLVED_TRANSITION:${result.event.type}`), definition.id)); setProblemKey(screenKey); return null; }
      if (!coordinator.request(plan, sourceToken)) return null;
      retryAction.current = null;
      return result;
    } catch (error: unknown) {
      const details = runtimeProblem(error, definition.id);
      if (error instanceof ApiProblem) {
        retryAction.current = { action, payload };
        setRetryKind("ACTION");
      }
      setProblem(details);
      setProblemKey(screenKey);
      return null;
    } finally {
      actionPendingRef.current = false;
      setActionPending(false);
    }
  }
  function retry() {
    if (retryAction.current) { const request = retryAction.current; void dispatchAction(request.action, request.payload); return; }
    if (retryKind === "LOAD") setAttempt((value) => value + 1);
  }
  const currentModel = loadedKey === screenKey ? model : null;
  const currentProblem = problemKey === screenKey ? problem : null;
  return <RuntimeContext.Provider value={{ context, model: currentModel, problem: currentProblem, canRetry: currentProblem !== null && retryKind !== null, retry, dispatchAction, transitionLocked: coordinator.transitionLocked || actionPending }}>{children}</RuntimeContext.Provider>;
}
export function useScreenRuntime(): ScreenRuntimeValue { const value = useContext(RuntimeContext); if (!value) throw new Error("SCREEN_RUNTIME_OUTSIDE_PROVIDER"); return value; }
