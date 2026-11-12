import { describe, expect, it } from "vitest";
import { stepGraphPhysics, type GraphPhysicsNode } from "./physics";

const node = (id: string, x: number, y: number, anchorX = x, anchorY = y): GraphPhysicsNode => ({ id, position: { x, y }, anchor: { x: anchorX, y: anchorY } });

describe("graph physics stepper", () => {
  it("moves a displaced node back toward its anchor deterministically", () => {
    const result = stepGraphPhysics([node("A", 0, 0, 40, 0)], [], new Map([["A", { x: 0, y: 0 }]]), { dt: 1 / 60, bounds: { minX: -100, maxX: 100, minY: -100, maxY: 100 } });
    expect(result.positions.get("A")?.x).toBeGreaterThan(0);
    expect(result.positions.get("A")?.x).toBeLessThan(40);
    expect(result.movingIds).toContain("A");
  });

  it("applies edge springs and ignores dangling relationships", () => {
    const result = stepGraphPhysics([node("A", 0, 0), node("B", 200, 0)], [{ sourceId: "A", targetId: "B", idealLength: 80 }, { sourceId: "B", targetId: "missing" }], new Map(), { dt: 1 / 60, bounds: { minX: -100, maxX: 300, minY: -100, maxY: 100 } });
    expect(result.positions.get("A")?.x).toBeGreaterThan(0);
    expect(result.positions.get("B")?.x).toBeLessThan(200);
  });

  it("clamps speed and positions to the declared bounds", () => {
    const result = stepGraphPhysics([node("A", 99, 99, 0, 0)], [], new Map([["A", { x: 999, y: 999 }]]), { dt: 1, maxSpeed: 10, bounds: { minX: 0, maxX: 100, minY: 0, maxY: 100 } });
    const position = result.positions.get("A");
    const velocity = result.velocities.get("A");
    expect(position?.x).toBeGreaterThanOrEqual(0);
    expect(position?.x).toBeLessThanOrEqual(100);
    expect(Math.hypot(velocity?.x ?? 0, velocity?.y ?? 0)).toBeLessThanOrEqual(10);
  });
});
