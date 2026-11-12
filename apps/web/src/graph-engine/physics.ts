/**
 * Renderer-neutral, deterministic graph motion.
 *
 * The stepper owns no DOM, timers or browser APIs. A renderer can call it from
 * requestAnimationFrame, a test can call it with a fixed dt, and a replay can
 * record the input positions/velocities without turning motion into evidence.
 */

export type GraphPhysicsPoint = { readonly x: number; readonly y: number };

export type GraphPhysicsNode = {
  readonly id: string;
  readonly position: GraphPhysicsPoint;
  readonly anchor: GraphPhysicsPoint;
};

export type GraphPhysicsEdge = {
  readonly sourceId: string;
  readonly targetId: string;
  readonly idealLength?: number;
};

export type GraphPhysicsVelocity = { readonly x: number; readonly y: number };

export type GraphPhysicsBounds = {
  readonly minX: number;
  readonly maxX: number;
  readonly minY: number;
  readonly maxY: number;
};

export type GraphPhysicsOptions = {
  readonly dt: number;
  readonly anchorStrength?: number;
  readonly repulsionRadius?: number;
  readonly repulsionStrength?: number;
  readonly springStrength?: number;
  readonly damping?: number;
  readonly maxSpeed?: number;
  readonly bounds?: GraphPhysicsBounds;
};

export type GraphPhysicsStep = {
  readonly positions: ReadonlyMap<string, GraphPhysicsPoint>;
  readonly velocities: ReadonlyMap<string, GraphPhysicsVelocity>;
  readonly movingIds: ReadonlySet<string>;
  readonly maxSpeed: number;
  readonly maxOffset: number;
};

const DEFAULT_BOUNDS: GraphPhysicsBounds = { minX: 0, maxX: 1120, minY: 0, maxY: 620 };

const clamp = (value: number, low: number, high: number): number => Math.max(low, Math.min(high, value));

export function stepGraphPhysics(
  nodes: readonly GraphPhysicsNode[],
  edges: readonly GraphPhysicsEdge[],
  velocities: ReadonlyMap<string, GraphPhysicsVelocity>,
  options: GraphPhysicsOptions,
): GraphPhysicsStep {
  const dt = clamp(options.dt, 0.001, 0.05);
  const anchorStrength = options.anchorStrength ?? 1.35;
  const repulsionRadius = options.repulsionRadius ?? 128;
  const repulsionStrength = options.repulsionStrength ?? .38;
  const springStrength = options.springStrength ?? .42;
  const damping = options.damping ?? .78;
  const maxSpeedLimit = options.maxSpeed ?? 240;
  const bounds = options.bounds ?? DEFAULT_BOUNDS;
  const forces = new Map(nodes.map((node) => [node.id, { x: 0, y: 0 }]));
  const addForce = (id: string, x: number, y: number): void => {
    const force = forces.get(id);
    if (force) {
      force.x += x;
      force.y += y;
    }
  };

  for (const node of nodes) {
    addForce(node.id, (node.anchor.x - node.position.x) * anchorStrength, (node.anchor.y - node.position.y) * anchorStrength);
  }

  for (let left = 0; left < nodes.length; left += 1) {
    const a = nodes[left];
    for (let right = left + 1; right < nodes.length; right += 1) {
      const b = nodes[right];
      const dx = a.position.x - b.position.x;
      const dy = a.position.y - b.position.y;
      const distance = Math.max(1, Math.hypot(dx, dy));
      if (distance < repulsionRadius) {
        const strength = (repulsionRadius - distance) * repulsionStrength / distance;
        addForce(a.id, dx * strength, dy * strength);
        addForce(b.id, -dx * strength, -dy * strength);
      }
    }
  }

  const byId = new Map(nodes.map((node) => [node.id, node]));
  for (const edge of edges) {
    const source = byId.get(edge.sourceId);
    const target = byId.get(edge.targetId);
    if (!source || !target) continue;
    const dx = target.position.x - source.position.x;
    const dy = target.position.y - source.position.y;
    const distance = Math.max(1, Math.hypot(dx, dy));
    const idealLength = edge.idealLength ?? 96;
    const strength = (distance - idealLength) * springStrength / distance;
    addForce(source.id, dx * strength, dy * strength);
    addForce(target.id, -dx * strength, -dy * strength);
  }

  const nextPositions = new Map<string, GraphPhysicsPoint>();
  const nextVelocities = new Map<string, GraphPhysicsVelocity>();
  const movingIds = new Set<string>();
  const frameDamping = Math.pow(damping, dt * 60);
  let maxSpeed = 0;
  let maxOffset = 0;
  for (const node of nodes) {
    const previousVelocity = velocities.get(node.id) ?? { x: 0, y: 0 };
    const force = forces.get(node.id) ?? { x: 0, y: 0 };
    const dampedVelocity = {
      x: clamp((previousVelocity.x + force.x * dt) * frameDamping, -maxSpeedLimit, maxSpeedLimit),
      y: clamp((previousVelocity.y + force.y * dt) * frameDamping, -maxSpeedLimit, maxSpeedLimit),
    };
    const dampedSpeed = Math.hypot(dampedVelocity.x, dampedVelocity.y);
    const speedScale = dampedSpeed > maxSpeedLimit ? maxSpeedLimit / dampedSpeed : 1;
    const velocity = { x: dampedVelocity.x * speedScale, y: dampedVelocity.y * speedScale };
    const position = {
      x: clamp(node.position.x + velocity.x * dt, bounds.minX, bounds.maxX),
      y: clamp(node.position.y + velocity.y * dt, bounds.minY, bounds.maxY),
    };
    const speed = Math.hypot(velocity.x, velocity.y);
    maxSpeed = Math.max(maxSpeed, speed);
    maxOffset = Math.max(maxOffset, Math.hypot(position.x - node.anchor.x, position.y - node.anchor.y));
    if (speed > .5 || Math.hypot(position.x - node.position.x, position.y - node.position.y) > .05) movingIds.add(node.id);
    nextPositions.set(node.id, position);
    nextVelocities.set(node.id, velocity);
  }

  return { positions: nextPositions, velocities: nextVelocities, movingIds, maxSpeed, maxOffset };
}
