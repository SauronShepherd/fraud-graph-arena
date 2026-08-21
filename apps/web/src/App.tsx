import { useScreenLocation } from "./screen-system/BrowserNavigationAdapter";
import { BoardPage } from "./pages/BoardPage";
import { CaseSelectionPage } from "./pages/CaseSelectionPage";
import { LaunchPage } from "./pages/LaunchPage";
import { OpeningComicPage } from "./pages/OpeningComicPage";
import { PathSelectionPage } from "./pages/PathSelectionPage";
import { TransitionCoordinator } from "./screen-system/TransitionCoordinator";
import { screenDefinitions } from "./screen-system/definitions";
import { ScreenHost } from "./screen-system/ScreenHost";

export function App() {
  const { screen } = useScreenLocation();
  return (
    <div className="app-shell">
      <TransitionCoordinator />
      <header className="masthead">
        <span className="paw" aria-hidden="true">🐾</span>
        <span>The Dogtective Agency</span>
      </header>
      <ScreenHost definition={screenDefinitions.get(screen)!} screen={screen}>
        {screen === "LAUNCH" ? <LaunchPage /> : null}
        {screen === "PATH_SELECTION" ? <PathSelectionPage /> : null}
        {screen === "CASE_SELECTION" ? <CaseSelectionPage /> : null}
        {screen === "CASE_INTRODUCTION" ? <OpeningComicPage /> : null}
        {screen === "INVESTIGATION_BOARD" ? <BoardPage /> : null}
      </ScreenHost>
    </div>
  );
}
