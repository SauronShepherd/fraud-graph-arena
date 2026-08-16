import type { Workspace } from "../api/contracts";
import { message } from "../messages";

export function InvestigationActions({ workspace }: { workspace: Workspace }) {
  return <section className="typewriter" aria-labelledby="actions-title"><div className="typewriter-top"><h2 id="actions-title">{message("board.tools")}</h2><span className="tool-status" role="status">{message("board.toolsUnavailable")}</span></div><div className="key-row">{workspace.actions.map((action) => <button className="typewriter-key" data-action-id={action.id} data-state={action.state} key={action.id} type="button" disabled={action.state !== "AVAILABLE"} aria-describedby={`reason-${action.id}`} title={action.reason}><span>{action.id.replaceAll("_", " ")}</span><small id={`reason-${action.id}`}>{action.reason}</small></button>)}</div></section>;
}
