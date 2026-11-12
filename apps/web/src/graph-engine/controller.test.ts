import { describe, expect, it } from "vitest";
import {
  createGraphEngineController,
  replayGraphEngineActions,
} from "./controller";
import { getGraphEngineExample, type GraphEngineAction } from "./examples";

describe("graph engine interaction controller", () => {
  it("emits ordered source-labelled events and keeps selection renderer-neutral", () => {
    const snapshot = getGraphEngineExample("shared-device-investigation").snapshot;
    const controller = createGraphEngineController(snapshot);
    const first = controller.dispatch(
      { kind: "select", target: { kind: "node", id: "EX-N-0003" }, via: "pointer" },
      "pointer",
    );
    const second = controller.dispatch(
      { kind: "open-context-menu", target: { kind: "edge", id: "EX-E-0003" }, via: "keyboard" },
      "keyboard",
    );

    expect(first.event).toMatchObject({ sequence: 1, source: "pointer" });
    expect(second.event).toMatchObject({ sequence: 2, source: "keyboard" });
    expect(controller.getState().selection).toEqual({ kind: "edge", id: "EX-E-0003" });
    expect(controller.getState().contextTarget).toEqual({ kind: "edge", id: "EX-E-0003" });
    expect(controller.getEvents().map((event) => event.sequence)).toEqual([1, 2]);
  });

  it("separates preview movement from committed movement and cancels without drift", () => {
    const snapshot = getGraphEngineExample("shared-device-investigation").snapshot;
    const controller = createGraphEngineController(snapshot);
    const original = controller.getState().positions["EX-N-0003"];

    controller.dispatch({ kind: "move-preview", nodeId: "EX-N-0003", position: { x: 470, y: 350 } });
    expect(controller.getState().positions["EX-N-0003"]).toEqual(original);
    expect(controller.getState().draftPositions["EX-N-0003"]).toEqual({ x: 470, y: 350 });

    controller.dispatch({ kind: "move-cancel", nodeId: "EX-N-0003" });
    expect(controller.getState().draftPositions).toEqual({});
    expect(controller.getState().positions["EX-N-0003"]).toEqual(original);

    controller.dispatch({ kind: "move-preview", nodeId: "EX-N-0003", position: { x: 470, y: 350 } });
    controller.dispatch({ kind: "move-commit", nodeId: "EX-N-0003", position: { x: 470, y: 350 } });
    expect(controller.getState().positions["EX-N-0003"]).toEqual({ x: 470, y: 350 });
    expect(controller.getState().draftPositions).toEqual({});
  });

  it("keeps local relationships removable while detected relationships remain immutable", () => {
    const snapshot = getGraphEngineExample("shared-device-investigation").snapshot;
    const controller = createGraphEngineController(snapshot);
    const localRelationship = {
      id: "LOCAL-REL-0001",
      sourceId: "EX-N-0001",
      targetId: "EX-N-0006",
      relationshipFamily: "INVESTIGATOR_HYPOTHESIS",
      relationshipType: "REVIEWED_WITH",
      directed: false,
      confidence: "low" as const,
    };

    controller.dispatch({ kind: "add-relationship", relationship: localRelationship });
    controller.dispatch({ kind: "toggle-favorite", target: { kind: "edge", id: localRelationship.id } });
    expect(controller.getState().working.addedEdges).toHaveLength(1);
    expect(controller.getState().working.favorites).toEqual([{ kind: "edge", id: localRelationship.id }]);

    controller.dispatch({ kind: "delete-relationship", edgeId: "EX-E-0001" });
    expect(controller.getState().working.addedEdges).toHaveLength(1);

    controller.dispatch({ kind: "delete-relationship", edgeId: localRelationship.id });
    expect(controller.getState().working.addedEdges).toHaveLength(0);
    expect(controller.getState().working.favorites).toEqual([]);
  });

  it("replays a command sequence to the same serialisable state without timing", () => {
    const example = getGraphEngineExample("shared-device-investigation");
    const actions: readonly GraphEngineAction[] = [
      { kind: "select", target: { kind: "node", id: "EX-N-0003" }, via: "semantic-list" },
      { kind: "toggle-favorite", target: { kind: "node", id: "EX-N-0003" } },
      { kind: "center-target", target: { kind: "node", id: "EX-N-0003" } },
      { kind: "set-view", view: "matrix" },
      { kind: "filter-status", status: "DISCARDED", visible: false },
    ];
    const controller = createGraphEngineController(example.snapshot);
    actions.forEach((action) => controller.dispatch(action, "replay"));

    expect(JSON.stringify(controller.getState())).toBe(JSON.stringify(replayGraphEngineActions(example.snapshot, actions)));
    expect(controller.getState().working.favorites).toEqual([{ kind: "node", id: "EX-N-0003" }]);
    expect(controller.getState().view).toBe("matrix");
    expect(controller.getState().hiddenStatuses).toEqual(["DISCARDED"]);
  });
});
