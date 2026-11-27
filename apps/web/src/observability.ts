export interface FrontendObservation {
  event: "frontend.error";
  kind: "api" | "runtime" | "promise";
  trace_id: string;
  path?: string;
  status?: number;
  code?: string;
  correlation_id?: string;
  error_type?: string;
}

const TRACE_KEY = "fga.trace_id";
const observations: FrontendObservation[] = [];
let listenersInstalled = false;

function sessionValue(key: string): string | null {
  try {
    return globalThis.sessionStorage?.getItem(key) ?? null;
  } catch {
    return null;
  }
}

function saveSessionValue(key: string, value: string): void {
  try {
    globalThis.sessionStorage?.setItem(key, value);
  } catch {
    // Private browsing and server-side rendering can deny storage. The trace
    // remains valid for the current request even when it cannot be persisted.
  }
}

export function browserTraceId(): string {
  const existing = sessionValue(TRACE_KEY);
  if (existing) return existing;
  const generated = globalThis.crypto?.randomUUID?.() ?? `trace-${Date.now()}-${Math.random().toString(16).slice(2)}`;
  saveSessionValue(TRACE_KEY, generated);
  return generated;
}

export function recordFrontendError(input: Omit<FrontendObservation, "event" | "trace_id">): void {
  const observation: FrontendObservation = { event: "frontend.error", trace_id: browserTraceId(), ...input };
  observations.push(observation);
  while (observations.length > 50) observations.shift();
  if (import.meta.env.VITE_FGA_OBSERVABILITY_DEBUG === "true") {
    console.info("[fga.observability]", JSON.stringify(observation));
  }
}

export function frontendObservations(): readonly FrontendObservation[] {
  return observations.slice();
}

export function installFrontendObservability(): void {
  if (listenersInstalled || typeof window === "undefined") return;
  listenersInstalled = true;
  window.addEventListener("error", (event) => {
    recordFrontendError({ kind: "runtime", error_type: event.error?.name ?? "Error" });
  });
  window.addEventListener("unhandledrejection", (event) => {
    recordFrontendError({ kind: "promise", error_type: event.reason?.name ?? "UnhandledRejection" });
  });
}
