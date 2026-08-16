export const BOARD_CANVAS = Object.freeze({ width: 1600, height: 900 });
export type Point = { x: number; y: number };
export type Rect = { x: number; y: number; width: number; height: number };
export type ContainTransform = { scale: number; renderedWidth: number; renderedHeight: number; offsetX: number; offsetY: number };
export type BoardMode = "FULL" | "COMPACT";
export const BOARD_REGIONS = Object.freeze({
  CASE_PAPER: { x: 120, y: 110, width: 600, height: 580 },
  GRAPH_VIEWPORT: { x: 760, y: 110, width: 720, height: 560 },
  TYPEWRITER_CONTROLS: { x: 240, y: 710, width: 800, height: 120 },
  BOARD_STATUS: { x: 40, y: 30, width: 1520, height: 60 },
});

export type BoardGeometry = { transform: ContainTransform; regions: Record<string, Rect> };

export function calculateBoardGeometry(containerWidth: number, containerHeight: number): BoardGeometry {
  const transform = calculateContainTransform(containerWidth, containerHeight);
  const regions = Object.fromEntries(Object.entries(BOARD_REGIONS).map(([name, rect]) => [name, transformRect(rect, transform)]));
  return { transform, regions };
}

/** Selects composition from the available rectangle, not viewport width alone. */
export function selectBoardMode(containerWidth: number, containerHeight: number): BoardMode {
  return containerWidth < 900 || containerHeight < 620 ? "COMPACT" : "FULL";
}

export function calculateContainTransform(containerWidth: number, containerHeight: number): ContainTransform {
  const scale = Math.min(containerWidth / BOARD_CANVAS.width, containerHeight / BOARD_CANVAS.height);
  const renderedWidth = BOARD_CANVAS.width * scale;
  const renderedHeight = BOARD_CANVAS.height * scale;
  return { scale, renderedWidth, renderedHeight, offsetX: (containerWidth - renderedWidth) / 2, offsetY: (containerHeight - renderedHeight) / 2 };
}

export function logicalToRenderedPoint(point: Point, transform: ContainTransform): Point {
  return { x: transform.offsetX + point.x * transform.scale, y: transform.offsetY + point.y * transform.scale };
}

export function renderedToLogicalPoint(point: Point, transform: ContainTransform): Point {
  return { x: (point.x - transform.offsetX) / transform.scale, y: (point.y - transform.offsetY) / transform.scale };
}

export function transformRect(rect: Rect, transform: ContainTransform): Rect {
  return { x: transform.offsetX + rect.x * transform.scale, y: transform.offsetY + rect.y * transform.scale, width: rect.width * transform.scale, height: rect.height * transform.scale };
}
