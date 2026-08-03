import { Navigate, Route, Routes } from "react-router-dom";
import { BoardPage } from "./pages/BoardPage";
import { CaseSelectionPage } from "./pages/CaseSelectionPage";
import { LaunchPage } from "./pages/LaunchPage";
import { OpeningComicPage } from "./pages/OpeningComicPage";
import { PathSelectionPage } from "./pages/PathSelectionPage";

export function App() {
  return (
    <div className="app-shell">
      <header className="masthead">
        <span className="paw" aria-hidden="true">🐾</span>
        <span>The Dogtective Agency</span>
      </header>
      <Routes>
        <Route path="/" element={<LaunchPage />} />
        <Route path="/paths" element={<PathSelectionPage />} />
        <Route path="/paths/:pathId/cases" element={<CaseSelectionPage />} />
        <Route path="/rounds/:roundId/intro" element={<OpeningComicPage />} />
        <Route path="/rounds/:roundId/board" element={<BoardPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </div>
  );
}
