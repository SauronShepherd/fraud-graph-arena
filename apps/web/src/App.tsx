import { useScreenLocation } from "./screen-system/BrowserNavigationAdapter";
import { TransitionCoordinator } from "./screen-system/TransitionCoordinator";
import { screenDefinitions, screenSet, screenValidationError } from "./screen-system/definitions";
import { ScreenHost } from "./screen-system/ScreenHost";
import { auditRegistries } from "./screen-system/registryAudit";
import { ScreenConfigurationError } from "./screen-system/contracts";
import { resolveComponent } from "./screen-system/componentRegistry";

export function App() {
  if (screenValidationError) throw screenValidationError;
  const startupDiagnostics = auditRegistries(screenSet);
  if (startupDiagnostics.length) throw new ScreenConfigurationError("INVALID_SCREEN_REGISTRIES", startupDiagnostics);
  const { screen, context } = useScreenLocation();
  const definition = screenDefinitions.get(screen);
  if (!definition) throw new ScreenConfigurationError("SCREEN_NOT_DEFINED", [screen]);
  const ScreenComponent = resolveComponent(definition.component);
  return (
    <div className="app-shell">
      <TransitionCoordinator>
        <header className="masthead">
          <span className="paw" aria-hidden="true">🐾</span>
          <span>The Dogtective Agency</span>
        </header>
        <ScreenHost definition={definition} screen={screen} context={context}>
          <ScreenComponent />
        </ScreenHost>
      </TransitionCoordinator>
    </div>
  );
}
