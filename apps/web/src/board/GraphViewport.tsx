export function GraphViewport() {
  return <section className="graph-panel" aria-labelledby="graph-title"><div className="graph-grid" aria-hidden="true" /><div className="graph-empty"><span className="graph-mark" aria-hidden="true">∅</span><h2 id="graph-title">Evidence graph</h2><p>No evidence has been revealed.</p><p className="muted">The graph will display published relationships here.</p><p className="sr-only" role="status">Graph contains zero entities and zero relationships.</p></div></section>;
}
