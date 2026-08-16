import { describe, expect, it } from "vitest";
import { BOARD_CANVAS, calculateContainTransform, logicalToRenderedPoint, renderedToLogicalPoint, selectBoardMode, transformRect } from "./layout";

describe("board logical canvas", () => {
  it("uses one 1600 by 900 contain transform", () => {
    expect(calculateContainTransform(3200, 1800)).toEqual({ scale: 2, renderedWidth: 3200, renderedHeight: 1800, offsetX: 0, offsetY: 0 });
    expect(calculateContainTransform(1000, 1000)).toEqual({ scale: .625, renderedWidth: 1000, renderedHeight: 562.5, offsetX: 0, offsetY: 218.75 });
  });
  it("round trips points and rectangles", () => {
    const transform = calculateContainTransform(1280, 720);
    for (const point of [{ x: 0, y: 0 }, { x: 801.5, y: 210.25 }, { x: BOARD_CANVAS.width, y: BOARD_CANVAS.height }]) {
      const actual = renderedToLogicalPoint(logicalToRenderedPoint(point, transform), transform);
      expect(actual.x).toBeCloseTo(point.x, 8); expect(actual.y).toBeCloseTo(point.y, 8);
    }
    expect(transformRect({ x: 100, y: 50, width: 300, height: 200 }, transform)).toEqual({ x: 80, y: 40, width: 240, height: 160 });
  });
  it("selects compact composition from width and height constraints", () => {
    expect(selectBoardMode(1200, 800)).toBe("FULL");
    expect(selectBoardMode(899, 800)).toBe("COMPACT");
    expect(selectBoardMode(1200, 619)).toBe("COMPACT");
  });
});
