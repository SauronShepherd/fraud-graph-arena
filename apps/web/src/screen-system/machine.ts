import type { MachineEvent, ScreenContext, ScreenDefinition, ScreenId, TransitionPlan } from "./contracts";
import { guards } from "./guards";
export function resolveTransition(current: ScreenDefinition, context: ScreenContext, event: MachineEvent, definitions: ReadonlyMap<ScreenId, ScreenDefinition>): TransitionPlan | null {
  const transition = current.transitions.find((candidate) => candidate.event === event.type);
  if (!transition) return null;
  const next = { ...context, ...(event.context ?? {}) };
  if (transition.guard && !guards[transition.guard]?.(next)) return null;
  const target = definitions.get(transition.target);
  if (!target || target.validation.required_context.some((key) => next[key] === undefined || next[key] === "")) return null;
  return { source: current.id, target: target.id, context: next, effect: transition.effect, history: transition.history, event: event.type };
}
