import { useEffect, useRef, useState } from "react";
import { useLocation } from "react-router-dom";
import { effectPlan } from "./effects";

export function TransitionCoordinator() {
  const location = useLocation();
  const previous = useRef(location.pathname);
  const [active, setActive] = useState(false);
  useEffect(() => {
    const isConfiguredFade = /\/rounds\/[^/]+\/intro$/.test(previous.current) && /\/rounds\/[^/]+\/board$/.test(location.pathname);
    previous.current = location.pathname;
    if (!isConfiguredFade) return;
    const duration = effectPlan("FADE_TO_BLACK", window.matchMedia?.("(prefers-reduced-motion: reduce)").matches).durationMs;
    setActive(true);
    const timer = window.setTimeout(() => setActive(false), duration);
    return () => window.clearTimeout(timer);
  }, [location.pathname]);
  return active ? <div className="screen-transition-overlay" data-transition-effect="FADE_TO_BLACK" aria-hidden="true" /> : null;
}
