export const BOARD_CANVAS = Object.freeze({ width: 1600, height: 900 });
export type Point = { x: number; y: number };
export type Rect = { x: number; y: number; width: number; height: number };
export type ContainTransform = { scale: number; renderedWidth: number; renderedHeight: number; offsetX: number; offsetY: number };

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
