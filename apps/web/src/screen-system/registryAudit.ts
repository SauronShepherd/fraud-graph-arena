import type { ScreenDefinition, ScreenId, ScreenSetManifest } from "./contracts";
import { actions } from "./actions";
import { dataSources } from "./dataSources";
import { effects } from "./effects";
import { guards } from "./guards";
import { lifecycle } from "./lifecycle";
import { componentRegistry } from "./componentRegistry";
import type { ActionId, EventId } from "./contracts";

const actionOutcomes: Partial<Record<ActionId, EventId[]>> = {
  BEGIN: ["PATHS_REQUESTED"],
  RESUME_LAST_ROUND: ["ROUND_RESUME_REQUESTED"],
  SELECT_PATH: ["PATH_SELECTED"],
  BACK_TO_PATHS: ["RETURNED_TO_PATHS"],
  OPEN_CASE: ["CASE_OPENED"],
  CHANGE_INTRO_PAGE: ["INTRO_PAGE_CHANGED"],
  COMPLETE_INTRO: ["INTRODUCTION_COMPLETED"],
  SKIP_INTRO: ["INTRODUCTION_SKIPPED"],
  RETURN_TO_CATALOGUE: ["RETURNED_TO_CATALOGUE"]
};
const runtimeOutcomes: EventId[] = ["INTRODUCTION_ALREADY_COMPLETED", "INTRODUCTION_REQUIRED"];
const reviewedCycleTransitions = new Set([
  "LAUNCH|ROUND_RESUME_REQUESTED|INVESTIGATION_BOARD",
  "PATH_SELECTION|PATH_SELECTED|CASE_SELECTION",
  "CASE_SELECTION|CASE_OPENED|CASE_INTRODUCTION",
  "CASE_SELECTION|RETURNED_TO_PATHS|PATH_SELECTION",
  "CASE_INTRODUCTION|INTRO_PAGE_CHANGED|CASE_INTRODUCTION",
  "CASE_INTRODUCTION|INTRODUCTION_COMPLETED|INVESTIGATION_BOARD",
  "CASE_INTRODUCTION|INTRODUCTION_SKIPPED|INVESTIGATION_BOARD",
  "CASE_INTRODUCTION|INTRODUCTION_ALREADY_COMPLETED|INVESTIGATION_BOARD",
  "INVESTIGATION_BOARD|RETURNED_TO_CATALOGUE|CASE_SELECTION",
  "INVESTIGATION_BOARD|INTRODUCTION_REQUIRED|CASE_INTRODUCTION"
]);

function hasPath(from: ScreenId, to: ScreenId, byId: ReadonlyMap<ScreenId, ScreenDefinition>): boolean {
  const pending = [from];
  const visited = new Set<string>();
  while (pending.length) {
    const current = pending.pop()!;
    if (current === to) return true;
    if (visited.has(current)) continue;
    visited.add(current);
    for (const transition of byId.get(current)?.transitions ?? []) {
      if (byId.has(transition.target)) pending.push(transition.target);
    }
  }
  return false;
}

export function auditRegistries(definitions: ScreenSetManifest): string[] {
  const errors: string[] = [];
  const screenIds = new Set(definitions.screens.map((screen) => screen.id));
  const initial = definitions.screens.find((screen) => screen.id === definitions.initial_screen);
  if (!initial || initial.route.mode !== "PUBLIC") errors.push("INITIAL_SCREEN_NOT_PUBLIC");
  for (const screen of definitions.screens) {
    if (screen.route.mode === "PUBLIC" && screen.transitions.length === 0) errors.push(`PUBLIC_SCREEN_WITHOUT_TRANSITION:${screen.id}`);
    if (!(screen.data_source in dataSources)) errors.push(`DATA_SOURCE:${screen.data_source}`);
    if (!(screen.component in componentRegistry)) errors.push(`COMPONENT:${screen.component}`);
    for (const hook of screen.onLoad) if (hook !== "LOAD_SCREEN_MODEL" && !(hook in lifecycle)) errors.push(`LIFECYCLE:${hook}`);
    for (const hook of [...screen.onEnter, ...screen.onExit]) if (!(hook in lifecycle)) errors.push(`LIFECYCLE:${hook}`);
    for (const action of screen.actions) {
      if (!(action.handler in actions)) errors.push(`ACTION_HANDLER:${screen.id}:${action.handler}`);
      if (!(action.id in actions)) errors.push(`ACTION_ID:${screen.id}:${action.id}`);
      const outcomes = actionOutcomes[action.handler];
      if (outcomes && !screen.transitions.some((transition) => outcomes.includes(transition.event))) errors.push(`ACTION_WITHOUT_TRANSITION:${screen.id}:${action.id}`);
    }
    for (const transition of screen.transitions) {
      if (!screenIds.has(transition.target)) errors.push(`TARGET:${screen.id}:${transition.target}`);
      if (!(transition.effect in effects)) errors.push(`EFFECT:${screen.id}:${transition.effect}`);
      if (transition.guard && !(transition.guard in guards)) errors.push(`GUARD:${screen.id}:${transition.guard}`);
    }
    for (const transition of screen.transitions) if (!runtimeOutcomes.includes(transition.event) && !Object.values(actionOutcomes).some((outcomes) => outcomes?.includes(transition.event))) errors.push(`UNEMITTED_EVENT:${screen.id}:${transition.event}`);
    if (screen.route.mode === "PUBLIC" && !screen.onLoad.includes("LOAD_SCREEN_MODEL")) errors.push(`PUBLIC_SCREEN_WITHOUT_LOAD:${screen.id}`);
  }
  const byId = new Map<ScreenId, ScreenDefinition>(definitions.screens.map((screen) => [screen.id, screen]));
  for (const screen of definitions.screens) for (const transition of screen.transitions) {
    if (!hasPath(transition.target, screen.id, byId)) continue;
    const cycle = `${screen.id}|${transition.event}|${transition.target}`;
    if (!reviewedCycleTransitions.has(cycle)) errors.push(`UNREVIEWED_CYCLE:${cycle}`);
  }
  const reachable = new Set([definitions.initial_screen]);
  const pending = [definitions.initial_screen];
  while (pending.length) for (const transition of byId.get(pending.pop()!)?.transitions ?? []) if (!reachable.has(transition.target)) { reachable.add(transition.target); pending.push(transition.target); }
  for (const required of ["LAUNCH", "PATH_SELECTION", "CASE_SELECTION", "CASE_INTRODUCTION", "INVESTIGATION_BOARD"]) if (!reachable.has(required as typeof definitions.initial_screen)) errors.push(`UNREACHABLE_REQUIRED_SCREEN:${required}`);
  if (reachable.has("CASE_RESOLUTION")) errors.push("INTERNAL_SCREEN_REACHABLE:CASE_RESOLUTION");
  const resolution = byId.get("CASE_RESOLUTION");
  if (resolution && (resolution.route.mode !== "INTERNAL" || resolution.actions.length || resolution.transitions.length)) errors.push("INVALID_INTERNAL_TERMINAL:CASE_RESOLUTION");
  return errors;
}
