import { describe, expect, it } from "vitest";
import { screenSet } from "./definitions";
import { auditRegistries } from "./registryAudit";
describe("screen registry audit", () => { it("accepts the production catalogue", () => expect(auditRegistries(screenSet)).toEqual([])); });
describe("screen registry failures", () => {
  it("reports missing action handlers and missing graph targets", () => {
    const candidate = structuredClone(screenSet) as unknown as { screens: Array<{ actions: Array<{ id: string; handler: string }>; transitions: Array<{ target: string }> }> };
    candidate.screens[0].actions[0].handler = "UNKNOWN_HANDLER";
    candidate.screens[0].transitions[0].target = "UNKNOWN_SCREEN";
    for (const screen of candidate.screens) screen.transitions = screen.transitions.filter(({ target }) => target !== "PATH_SELECTION");
    expect(auditRegistries(candidate as never)).toEqual(expect.arrayContaining(["ACTION_HANDLER:LAUNCH:UNKNOWN_HANDLER", "TARGET:LAUNCH:UNKNOWN_SCREEN", "UNREACHABLE_REQUIRED_SCREEN:PATH_SELECTION"]));
  });

  it("rejects public screens without a forward transition", () => {
    const candidate = structuredClone(screenSet);
    candidate.screens.find((screen) => screen.id === "CASE_SELECTION")!.transitions = [];
    expect(auditRegistries(candidate)).toContain("PUBLIC_SCREEN_WITHOUT_TRANSITION:CASE_SELECTION");
  });

  it("rejects graph cycles that are not in the reviewed journey", () => {
    const candidate = structuredClone(screenSet);
    candidate.screens.find((screen) => screen.id === "CASE_SELECTION")!.transitions[0].target = "INVESTIGATION_BOARD";
    expect(auditRegistries(candidate)).toContain("UNREVIEWED_CYCLE:CASE_SELECTION|CASE_OPENED|INVESTIGATION_BOARD");
  });
});
