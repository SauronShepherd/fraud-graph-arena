import type { EffectId } from "./contracts";
export interface EffectPlan { id: EffectId; durationMs: number; }
export function effectPlan(id: EffectId, reducedMotion = false): EffectPlan { return { id, durationMs: reducedMotion || id === "NONE" ? 0 : 500 }; }
export const effects: Record<EffectId, true> = { NONE: true, FADE_TO_BLACK: true };
