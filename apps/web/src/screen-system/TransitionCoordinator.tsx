import { createContext, useContext, useEffect, useRef, useState, type PropsWithChildren } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { effectPlan } from "./effects";
import { locationFor, parseLocation } from "./routeCodec";
import { screenDefinitions } from "./definitions";
import type { TransitionPlan } from "./contracts";

interface PendingTransition { plan: TransitionPlan; sourceToken: number; }
interface TransitionRuntime { request: (plan: TransitionPlan, sourceToken?: number) => boolean; captureToken: () => number; transitionLocked: boolean; }
const TransitionContext = createContext<TransitionRuntime | null>(null);

export function useTransitionCoordinator(): TransitionRuntime {
  const value = useContext(TransitionContext);
  if (!value) throw new Error("TRANSITION_COORDINATOR_OUTSIDE_PROVIDER");
  return value;
}

export function TransitionCoordinator({ children }: PropsWithChildren) {
  const navigate = useNavigate();
  const location = useLocation();
  const [pending, setPending] = useState<PendingTransition | null>(null);
  const [active, setActive] = useState(false);
  const pendingRef = useRef<PendingTransition | null>(null);
  const resolvedLocation = parseLocation(location.pathname, location.search, screenDefinitions);
  const currentScreenRef = useRef(resolvedLocation.screen);
  const currentIdentityRef = useRef("");
  const routeTokenRef = useRef(0);
  const currentContext = Object.fromEntries(Object.entries(resolvedLocation.context).filter(([key]) => key !== "page"));
  const currentIdentity = `${resolvedLocation.screen}:${JSON.stringify(currentContext)}`;
  if (currentIdentityRef.current !== currentIdentity) {
    if (currentIdentityRef.current) routeTokenRef.current += 1;
    currentIdentityRef.current = currentIdentity;
  }
  currentScreenRef.current = resolvedLocation.screen;
  const captureToken = () => routeTokenRef.current;
  const request = (plan: TransitionPlan, sourceToken = routeTokenRef.current) => {
    const target = screenDefinitions.get(plan.target);
    if (sourceToken !== routeTokenRef.current || pendingRef.current || currentScreenRef.current !== plan.source || !target || target.route.mode !== "PUBLIC" || !target.route.pattern) return false;
    const queued = { plan, sourceToken };
    pendingRef.current = queued;
    setPending(queued);
    return true;
  };
  useEffect(() => {
    if (!pending) return;
    const { plan, sourceToken } = pending;
    const duration = effectPlan(plan.effect, window.matchMedia?.("(prefers-reduced-motion: reduce)").matches).durationMs;
    setActive(duration > 0);
    const timer = window.setTimeout(() => {
      const target = screenDefinitions.get(plan.target);
      if (sourceToken === routeTokenRef.current && currentScreenRef.current === plan.source && target?.route.mode === "PUBLIC" && target.route.pattern) {
        navigate(locationFor(target, plan.context), { replace: plan.history === "REPLACE" });
      }
      setActive(false);
      if (pendingRef.current === pending) pendingRef.current = null;
      setPending(null);
    }, duration);
    return () => window.clearTimeout(timer);
  }, [navigate, pending]);
  return <TransitionContext.Provider value={{ request, captureToken, transitionLocked: pending !== null }}>
    {children}
    {active ? <div className="screen-transition-overlay" data-transition-effect="FADE_TO_BLACK" aria-hidden="true" /> : null}
  </TransitionContext.Provider>;
}
