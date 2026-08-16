export function DebugOverlay({ mode }: { mode: "FULL" | "COMPACT" }) {
  if (!import.meta.env.DEV || new URLSearchParams(window.location.search).get("debug") !== "1") return null;
  return <aside className="debug-overlay" aria-label="Board layout diagnostics">layout={mode} · graph=empty · evidence=empty</aside>;
}
