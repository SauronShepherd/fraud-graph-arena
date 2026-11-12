import { describe, expect, it } from "vitest";
import { getGraphEngineExample } from "./examples";
import {
  addGraphEngineRelationship,
  createGraphEngineWorkingState,
  getGraphEngineTargetPosition,
  isGraphEngineFavorite,
  removeGraphEngineRelationship,
  toggleGraphEngineFavorite,
} from "./workingState";

describe("graph engine working state", () => {
  it("adds and removes only investigator-added relationships", () => {
    const example = getGraphEngineExample("shared-device-investigation");
    const state = addGraphEngineRelationship(example.snapshot, createGraphEngineWorkingState(), {
      id: "LOCAL-E-0001",
      sourceId: "EX-N-0001",
      targetId: "EX-N-0005",
      relationshipFamily: "INVESTIGATOR_NOTE",
      relationshipType: "WORKING_HYPOTHESIS",
      directed: false,
      confidence: "low",
    });
    expect(state.addedEdges[0]).toMatchObject({ id: "LOCAL-E-0001", origin: "investigator-added" });
    expect(removeGraphEngineRelationship(state, "EX-E-0001").addedEdges).toHaveLength(1);
    expect(removeGraphEngineRelationship(state, "LOCAL-E-0001").addedEdges).toHaveLength(0);
  });

  it("toggles favorites and resolves node or edge focus positions", () => {
    const example = getGraphEngineExample("shared-device-investigation");
    let state = createGraphEngineWorkingState();
    state = toggleGraphEngineFavorite(state, { kind: "node", id: "EX-N-0003" });
    expect(isGraphEngineFavorite(state, { kind: "node", id: "EX-N-0003" })).toBe(true);
    expect(getGraphEngineTargetPosition(example.snapshot, state, { kind: "node", id: "EX-N-0003" })).toEqual({ x: 430, y: 330 });
    state = toggleGraphEngineFavorite(state, { kind: "node", id: "EX-N-0003" });
    expect(state.favorites).toHaveLength(0);
  });

  it("rejects endpoints outside the snapshot", () => {
    const example = getGraphEngineExample("empty-academy-board");
    expect(() => addGraphEngineRelationship(example.snapshot, createGraphEngineWorkingState(), {
      id: "LOCAL-E-INVALID",
      sourceId: "missing",
      targetId: "missing",
      relationshipFamily: "INVESTIGATOR_NOTE",
      relationshipType: "WORKING_HYPOTHESIS",
      directed: false,
      confidence: "low",
    })).toThrow("endpoints must exist");
  });
});
