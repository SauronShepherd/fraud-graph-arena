import type { MachineEvent, ScreenContext, ScreenDefinition, ScreenId, TransitionPlan } from "./contracts";
export function resolveTransition(current: ScreenDefinition, context: ScreenContext, event: MachineEvent, definitions: ReadonlyMap<ScreenId, ScreenDefinition>): TransitionPlan | null {
  const transition = current.transitions.find((candidate) => candidate.event === event.type);
  if (!transition) return null;
  if (transition.guard === "REQUIRED_CONTEXT" && Object.values(context).some((value) => value === undefined || value === "")) return null;
  const next = { ...context, ...(event.context ?? {}) };
  const target = definitions.get(transition.target);
  if (!target || target.validation.required_context.some((key) => next[key] === undefined || next[key] === "")) return null;
  return { source: current.id, target: target.id, context: next, effect: transition.effect, history: transition.history, event: event.type };
}
