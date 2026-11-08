import { describe, expect, it } from "vitest";
import {
  createGraphEngineExampleLibrary,
  getGraphEngineExample,
  graphEngineExampleIds,
  serializeGraphEngineExample,
  validateGraphEngineExample,
} from "./examples";

describe("graph engine example library", () => {
  it("provides deterministic, renderer-neutral examples", () => {
    const first = createGraphEngineExampleLibrary();
    const second = createGraphEngineExampleLibrary();
    expect(first.map((item) => item.id)).toEqual([
      "empty-academy-board",
      "shared-device-investigation",
      "temporal-path-tracing",
      "keyboard-and-semantic-journey",
      "dense-cluster-progressive-disclosure",
    ]);
    expect(serializeGraphEngineExample(first[1])).toBe(serializeGraphEngineExample(second[1]));
    expect(graphEngineExampleIds()).toEqual(first.map((item) => item.id));
  });

  it("validates empty, connected and dense scenarios", () => {
    const examples = createGraphEngineExampleLibrary();
    expect(examples[0].snapshot.nodes).toHaveLength(0);
    expect(examples[0].snapshot.edges).toHaveLength(0);
    expect(examples[1].snapshot.edges.every((item) => examples[1].snapshot.nodes.some((node) => node.id === item.sourceId))).toBe(true);
    expect(examples[4].snapshot.nodes).toHaveLength(34);
    expect(examples[4].snapshot.edges).toHaveLength(66);
    examples.forEach(validateGraphEngineExample);
  });

  it("keeps interaction actions explicit and targetable", () => {
    const example = getGraphEngineExample("shared-device-investigation");
    expect(example.actions.some((action) => action.kind === "open-context-menu" && action.target.kind === "edge")).toBe(true);
    expect(example.actions.some((action) => action.kind === "move-preview")).toBe(true);
    expect(example.actions.some((action) => action.kind === "move-commit")).toBe(true);
    expect(example.recommendedViews).toContain("matrix");
  });

  it("rejects dangling relationships and unknown action targets", () => {
    const example = getGraphEngineExample("empty-academy-board");
    expect(() => validateGraphEngineExample({
      ...example,
      snapshot: { ...example.snapshot, edges: [{ id: "bad", sourceId: "missing", targetId: "missing", relationshipFamily: "X", relationshipType: "Y", directed: true, confidence: "low" }] },
    })).toThrow("Dangling edge");
    expect(() => validateGraphEngineExample({
      ...example,
      actions: [{ kind: "select", target: { kind: "node", id: "missing" }, via: "keyboard" }],
    })).toThrow("Unknown node target");
  });
});

