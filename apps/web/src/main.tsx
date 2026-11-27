import { Component, StrictMode, type ErrorInfo, type ReactNode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { App } from "./App";
import "./styles.css";
import { installFrontendObservability, recordFrontendError } from "./observability";

installFrontendObservability();

const root = document.getElementById("root");
if (!root) throw new Error("Missing #root application mount");

class RuntimeRecoveryBoundary extends Component<{ children: ReactNode }, { failed: boolean }> {
  state = { failed: false };
  static getDerivedStateFromError(): { failed: boolean } { return { failed: true }; }
  componentDidCatch(error: Error, _info: ErrorInfo): void {
    recordFrontendError({ kind: "runtime", error_type: error.name || "ReactError" });
  }
  render() {
    if (this.state.failed) return <main className="panel problem" role="alert"><h1>Investigation workspace unavailable</h1><p>The screen catalogue could not be loaded safely.</p><button className="button" type="button" onClick={() => window.location.reload()}>Reload the application</button></main>;
    return this.props.children;
  }
}

createRoot(root).render(
  <StrictMode>
    <BrowserRouter>
      <RuntimeRecoveryBoundary><App /></RuntimeRecoveryBoundary>
    </BrowserRouter>
  </StrictMode>
);
