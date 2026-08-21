export function ConfigurationFailurePage({ code = "SCREEN_CONFIGURATION_FAILURE" }: { code?: string }) {
  return (
    <main className="panel" role="alert">
      <p className="eyebrow">The Dogtective Agency</p>
      <h1>Configuration unavailable</h1>
      <p>This training session cannot start safely right now.</p>
      <p className="problem-code">Reference: {code}</p>
    </main>
  );
}
