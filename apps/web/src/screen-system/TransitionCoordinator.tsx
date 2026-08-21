import { useEffect, useRef, useState } from "react";
import { effectPlan } from "./effects";
import type { TransitionPlan } from "./contracts";

export function TransitionCoordinator({ plan, onComplete }: { plan: TransitionPlan | null; onComplete: () => void }) {
  const [active, setActive] = useState(false);
  useEffect(() => {
    if (!plan) return;
    const duration = effectPlan(plan.effect, window.matchMedia?.("(prefers-reduced-motion: reduce)").matches).durationMs;
    setActive(true);
    const timer = window.setTimeout(() => { setActive(false); onComplete(); }, duration);
    return () => window.clearTimeout(timer);
  }, [onComplete, plan]);
  return active ? <div className="screen-transition-overlay" data-transition-effect={plan?.effect} aria-hidden="true" /> : null;
}
