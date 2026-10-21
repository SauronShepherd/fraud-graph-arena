import { Component, StrictMode, type ErrorInfo, type ReactNode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { App } from "./App";
import "./styles.css";

const root = document.getElementById("root");
if (!root) throw new Error("Missing #root application mount");

class RuntimeRecoveryBoundary extends Component<{ children: ReactNode }, { failed: boolean }> {
  state = { failed: false };
  static getDerivedStateFromError(): { failed: boolean } { return { failed: true }; }
  componentDidCatch(_error: Error, _info: ErrorInfo): void { /* Keep diagnostics in the host console; never expose them as screen content. */ }
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
