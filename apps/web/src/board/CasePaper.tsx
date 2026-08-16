import type { Workspace } from "../api/contracts";

export function CasePaper({ workspace }: { workspace: Workspace }) {
  return <section className="case-paper" aria-labelledby="paper-title">
    <p className="paper-kicker">{workspace.round.path_id}</p><h2 id="paper-title">Case paper</h2>
    <dl className="case-facts"><div><dt>Case</dt><dd>{workspace.case.id}</dd></div><div><dt>Evidence revealed</dt><dd>{workspace.evidence_count}</dd></div><div><dt>Suspects identified</dt><dd>{workspace.suspect_count}</dd></div></dl>
    <p className="paper-empty">No evidence has been revealed.</p><p className="paper-note">The paper is waiting for evidence. Empty means empty; it is not a clue.</p>
  </section>;
}
