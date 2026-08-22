import { useScreenLocation } from "./screen-system/BrowserNavigationAdapter";
import { TransitionCoordinator } from "./screen-system/TransitionCoordinator";
import { screenConfigurationError, screenDefinitions } from "./screen-system/definitions";
import { ScreenHost } from "./screen-system/ScreenHost";
import { resolveComponent } from "./screen-system/componentRegistry";
import { ScreenRuntimeProvider } from "./screen-system/ScreenRuntimeContext";
import { actions } from "./screen-system/actions";
import { resolveTransition } from "./screen-system/machine";
import { locationFor } from "./screen-system/routeCodec";
import type { ActionId, TransitionPlan } from "./screen-system/contracts";
import { useNavigate } from "react-router-dom";
import { ConfigurationFailurePage } from "./pages/ConfigurationFailurePage";
import { useCallback, useRef, useState } from "react";
import { ScreenLoadCoordinator } from "./screen-system/loadCoordinator";
import type { DataSourceId } from "./screen-system/contracts";

export function App() {
  if (screenConfigurationError) {
    return <div className="app-shell"><ConfigurationFailurePage code={screenConfigurationError.code} /></div>;
  }
  const { screen, context } = useScreenLocation();
  const navigate = useNavigate();
  const [transitionPlan, setTransitionPlan] = useState<TransitionPlan | null>(null);
  const [transitionLocked, setTransitionLocked] = useState(false);
  const loadCoordinator = useRef(new ScreenLoadCoordinator());
  const loadScreenModel = useCallback(async (source: DataSourceId, loadContext: typeof context) => {
    return loadCoordinator.current.load(source, loadContext);
  }, [screen]);
  const handleTransitionComplete = useCallback(() => {
    setTransitionPlan(null);
    setTransitionLocked(false);
  }, []);
  const dispatchAction = useCallback(async (actionId: string, payload?: Record<string, string | number>): Promise<void> => {
    if (transitionLocked) return;
    const action = actions[actionId as ActionId];
    if (!action) throw new Error(`UNKNOWN_SCREEN_ACTION:${actionId}`);
    setTransitionLocked(true);
    try {
      const result = await action({ context, payload });
      const plan = resolveTransition(screenDefinitions.get(screen)!, context, result.event, screenDefinitions);
      if (!plan) throw new Error(`UNDECLARED_SCREEN_TRANSITION:${screen}:${result.event.type}`);
      setTransitionPlan(plan);
      navigate(locationFor(screenDefinitions.get(plan.target)!, plan.context), { replace: plan.history === "REPLACE" });
    } catch (error) {
      setTransitionLocked(false);
      throw error;
    }
  }, [context, navigate, screen, transitionLocked]);
  let Component: ReturnType<typeof resolveComponent>;
  try {
    Component = resolveComponent(screenDefinitions.get(screen)?.component ?? screen);
  } catch {
    return <div className="app-shell"><ConfigurationFailurePage code="SCREEN_COMPONENT_UNREGISTERED" /></div>;
  }
  return (
    <div className="app-shell">
      <TransitionCoordinator plan={transitionPlan} onComplete={handleTransitionComplete} />
      <header className="masthead">
        <span className="paw" aria-hidden="true">🐾</span>
        <span>The Dogtective Agency</span>
      </header>
      <ScreenRuntimeProvider value={{ context, dispatchAction, loadScreenModel, transitionLocked }}>
        <ScreenHost definition={screenDefinitions.get(screen)!} screen={screen}>
          <Component />
        </ScreenHost>
      </ScreenRuntimeProvider>
    </div>
  );
}
