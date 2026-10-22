import raw from "./definitions/fga-screen-set.v1.json";
import type { ActionId, DataSourceId, EffectId, EventId, GuardId, LifecycleHookId, ScreenDefinition, ScreenId, ScreenSetManifest } from "./contracts";
import { ScreenConfigurationError } from "./contracts";

const screenIds: ScreenId[] = ["LAUNCH", "PATH_SELECTION", "CASE_SELECTION", "CASE_INTRODUCTION", "INVESTIGATION_BOARD", "CASE_RESOLUTION"];
const actionIds: ActionId[] = ["BEGIN", "RESUME_LAST_ROUND", "SELECT_PATH", "BACK_TO_PATHS", "OPEN_CASE", "CHANGE_INTRO_PAGE", "COMPLETE_INTRO", "SKIP_INTRO", "RETURN_TO_CATALOGUE"];
const eventIds: EventId[] = ["PATHS_REQUESTED", "ROUND_RESUME_REQUESTED", "PATH_SELECTED", "CASE_OPENED", "INTRO_PAGE_CHANGED", "INTRODUCTION_COMPLETED", "INTRODUCTION_SKIPPED", "INTRODUCTION_ALREADY_COMPLETED", "INTRODUCTION_REQUIRED", "RETURNED_TO_PATHS", "RETURNED_TO_CATALOGUE"];
const dataSourceIds: DataSourceId[] = ["LAST_ROUND_POINTER", "CATALOGUE_SECTIONS", "CATALOGUE_SECTION", "ROUND_OPENING", "ROUND_WORKSPACE", "RESOLUTION_CONTEXT"];
const effectIds: EffectId[] = ["NONE", "FADE_TO_BLACK"];
const guardIds: GuardId[] = ["REQUIRED_CONTEXT", "ACTION_NOT_PENDING", "ROUND_ACTIVE", "ROUND_INTRO_PENDING"];
const loadHooks: LifecycleHookId[] = ["LOAD_SCREEN_MODEL"];
const enterHooks: LifecycleHookId[] = ["FOCUS_PRIMARY_HEADING", "ANNOUNCE_SCREEN"];
const exitHooks: LifecycleHookId[] = ["ABORT_OBSOLETE_READS"];
const actionOutcomes: Record<ActionId, EventId[]> = {
  BEGIN: ["PATHS_REQUESTED"], RESUME_LAST_ROUND: ["ROUND_RESUME_REQUESTED"], SELECT_PATH: ["PATH_SELECTED"],
  BACK_TO_PATHS: ["RETURNED_TO_PATHS"], OPEN_CASE: ["CASE_OPENED"], CHANGE_INTRO_PAGE: ["INTRO_PAGE_CHANGED"],
  COMPLETE_INTRO: ["INTRODUCTION_COMPLETED"], SKIP_INTRO: ["INTRODUCTION_SKIPPED"], RETURN_TO_CATALOGUE: ["RETURNED_TO_CATALOGUE"]
};
const runtimeEvents: Partial<Record<ScreenId, EventId[]>> = {
  CASE_INTRODUCTION: ["INTRODUCTION_ALREADY_COMPLETED"],
  INVESTIGATION_BOARD: ["INTRODUCTION_REQUIRED"]
};
export const SCREEN_RUNTIME_VERSION = "1.0.0";

type JsonRecord = Record<string, unknown>;
function isRecord(value: unknown): value is JsonRecord { return typeof value === "object" && value !== null && !Array.isArray(value); }
function exactKeys(value: JsonRecord, required: string[], optional: string[] = [], path: string, errors: string[]): void {
  const allowed = new Set([...required, ...optional]);
  for (const key of required) if (!(key in value)) errors.push(`MISSING_FIELD:${path}.${key}`);
  for (const key of Object.keys(value)) if (!allowed.has(key)) errors.push(`UNKNOWN_FIELD:${path}.${key}`);
}
function enumValue<T extends string>(value: unknown, values: readonly T[]): value is T { return typeof value === "string" && values.includes(value as T); }
function versionParts(value: unknown): number[] | null {
  if (typeof value !== "string") return null;
  const match = /^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$/.exec(value);
  return match ? match.slice(1).map(Number) : null;
}
function isRuntimeCompatible(minimum: unknown): boolean {
  const required = versionParts(minimum);
  const runtime = versionParts(SCREEN_RUNTIME_VERSION);
  if (!required || !runtime) return false;
  for (let index = 0; index < 3; index += 1) if (required[index] !== runtime[index]) return required[index] < runtime[index];
  return true;
}

export function validateScreenSet(input: unknown): ReadonlyMap<ScreenId, ScreenDefinition> {
  const errors: string[] = [];
  const map = new Map<ScreenId, ScreenDefinition>();
  if (!isRecord(input)) throw new ScreenConfigurationError("INVALID_SCREEN_SET", ["ROOT_NOT_OBJECT"]);
  exactKeys(input, ["schema_version", "document_version", "minimum_runtime_version", "screen_set_id", "screen_set_version", "initial_screen", "screens"], [], "screenSet", errors);
  if (input.schema_version !== "1.0") errors.push("UNSUPPORTED_SCHEMA_VERSION");
  if (typeof input.document_version !== "string" || !input.document_version.trim()) errors.push("MISSING_DOCUMENT_VERSION");
  if (!isRuntimeCompatible(input.minimum_runtime_version)) errors.push(`INCOMPATIBLE_RUNTIME:${String(input.minimum_runtime_version)}`);
  if (input.screen_set_id !== "FGA03") errors.push("UNKNOWN_SCREEN_SET");
  if (typeof input.screen_set_version !== "string" || !input.screen_set_version.trim()) errors.push("MISSING_SCREEN_SET_VERSION");
  if (!enumValue(input.initial_screen, screenIds)) errors.push("MISSING_INITIAL_SCREEN");
  if (!Array.isArray(input.screens) || input.screens.length === 0) errors.push("SCREENS_NOT_ARRAY_OR_EMPTY");

  const rawScreens = Array.isArray(input.screens) ? input.screens : [];
  const publicRouteShapes = new Map<string, string>();
  rawScreens.forEach((rawScreen, index) => {
    const path = `screens[${index}]`;
    if (!isRecord(rawScreen)) { errors.push(`SCREEN_NOT_OBJECT:${index}`); return; }
    const screen = rawScreen;
    exactKeys(screen, ["schema_version", "document_version", "minimum_runtime_version", "id", "component", "route", "data_source", "onLoad", "onEnter", "onExit", "actions", "transitions", "effects", "validation"], [], path, errors);
    if (screen.schema_version !== input.schema_version) errors.push(`SCHEMA_VERSION_MISMATCH:${String(screen.id)}`);
    if (typeof screen.document_version !== "string" || !screen.document_version.trim()) errors.push(`MISSING_DOCUMENT_VERSION:${String(screen.id)}`);
    if (!isRuntimeCompatible(screen.minimum_runtime_version)) errors.push(`INCOMPATIBLE_RUNTIME:${String(screen.id)}:${String(screen.minimum_runtime_version)}`);
    if (!enumValue(screen.id, screenIds) || !enumValue(screen.component, screenIds)) errors.push(`UNKNOWN_SCREEN:${String(screen.id)}`);
    if (enumValue(screen.id, screenIds)) {
      if (map.has(screen.id)) errors.push(`DUPLICATE_SCREEN:${screen.id}`);
      else map.set(screen.id, screen as unknown as ScreenDefinition);
    }
    if (!enumValue(screen.data_source, dataSourceIds)) errors.push(`UNKNOWN_DATA_SOURCE:${String(screen.id)}`);

    if (!isRecord(screen.route)) errors.push(`ROUTE_NOT_OBJECT:${String(screen.id)}`);
    else {
      exactKeys(screen.route, ["mode", "pattern"], [], `${path}.route`, errors);
      const publicRoute = screen.route.mode === "PUBLIC" && typeof screen.route.pattern === "string" && screen.route.pattern.startsWith("/");
      const internalRoute = screen.route.mode === "INTERNAL" && screen.route.pattern === null;
      if (!publicRoute && !internalRoute) errors.push(`INVALID_ROUTE:${String(screen.id)}`);
      if (screen.route.mode === "PUBLIC" && typeof screen.route.pattern === "string") {
        const shape = screen.route.pattern.replace(/:[A-Za-z0-9_]+/g, ":PARAM");
        const previous = publicRouteShapes.get(shape);
        if (previous) errors.push(`AMBIGUOUS_PUBLIC_ROUTE:${previous}:${String(screen.id)}`);
        else publicRouteShapes.set(shape, String(screen.id));
        const params = [...screen.route.pattern.matchAll(/:([A-Za-z0-9_]+)/g)].map((match) => match[1]);
        const required = isRecord(screen.validation) && Array.isArray(screen.validation.required_context) ? screen.validation.required_context : [];
        for (const param of params) if (!required.includes(param)) errors.push(`ROUTE_CONTEXT_MISSING:${String(screen.id)}:${param}`);
      }
    }

    for (const [name, allowed] of [["onLoad", loadHooks], ["onEnter", enterHooks], ["onExit", exitHooks]] as const) {
      const hooks = screen[name];
      if (!Array.isArray(hooks) || hooks.some((hook) => !enumValue(hook, allowed)) || new Set(hooks).size !== hooks.length) errors.push(`INVALID_LIFECYCLE:${String(screen.id)}:${name}`);
    }

    if (!Array.isArray(screen.actions)) errors.push(`ACTIONS_NOT_ARRAY:${String(screen.id)}`);
    else {
      const seen = new Set<string>();
      screen.actions.forEach((rawAction, actionIndex) => {
        const actionPath = `${path}.actions[${actionIndex}]`;
        if (!isRecord(rawAction)) { errors.push(`ACTION_NOT_OBJECT:${actionPath}`); return; }
        exactKeys(rawAction, ["id", "handler"], [], actionPath, errors);
        if (!enumValue(rawAction.id, actionIds) || !enumValue(rawAction.handler, actionIds)) errors.push(`UNKNOWN_ACTION:${String(screen.id)}:${String(rawAction.id)}`);
        if (typeof rawAction.id === "string" && seen.has(rawAction.id)) errors.push(`DUPLICATE_ACTION:${String(screen.id)}:${rawAction.id}`);
        if (typeof rawAction.id === "string") seen.add(rawAction.id);
        if (enumValue(rawAction.handler, actionIds) && Array.isArray(screen.transitions)) {
          const expectedEvents = actionOutcomes[rawAction.handler];
          if (!screen.transitions.some((transition) => isRecord(transition) && expectedEvents.includes(transition.event as EventId))) errors.push(`ACTION_WITHOUT_TRANSITION:${String(screen.id)}:${String(rawAction.id)}`);
        }
      });
    }

    if (!Array.isArray(screen.transitions)) errors.push(`TRANSITIONS_NOT_ARRAY:${String(screen.id)}`);
    else {
      const seen = new Set<string>();
      screen.transitions.forEach((rawTransition, transitionIndex) => {
        const transitionPath = `${path}.transitions[${transitionIndex}]`;
        if (!isRecord(rawTransition)) { errors.push(`TRANSITION_NOT_OBJECT:${transitionPath}`); return; }
        exactKeys(rawTransition, ["event", "target", "effect", "history"], ["guard"], transitionPath, errors);
        if (!enumValue(rawTransition.event, eventIds) || !enumValue(rawTransition.target, screenIds) || !enumValue(rawTransition.effect, effectIds) || !["PUSH", "REPLACE"].includes(String(rawTransition.history))) errors.push(`INVALID_TRANSITION:${String(screen.id)}:${String(rawTransition.event)}`);
        if (rawTransition.guard !== undefined && !enumValue(rawTransition.guard, guardIds)) errors.push(`UNKNOWN_GUARD:${String(screen.id)}:${String(rawTransition.guard)}`);
        if (typeof rawTransition.event === "string" && seen.has(rawTransition.event)) errors.push(`DUPLICATE_TRANSITION_EVENT:${String(screen.id)}:${rawTransition.event}`);
        if (typeof rawTransition.event === "string") seen.add(rawTransition.event);
        const event = rawTransition.event as EventId;
        const actionEmitsEvent = Array.isArray(screen.actions) && screen.actions.some((action) => isRecord(action) && enumValue(action.handler, actionIds) && actionOutcomes[action.handler].includes(event));
        const runtimeEmitsEvent = (runtimeEvents[screen.id as ScreenId] ?? []).includes(event);
        if (typeof rawTransition.event === "string" && !runtimeEmitsEvent && !actionEmitsEvent) errors.push(`UNEMITTED_TRANSITION_EVENT:${String(screen.id)}:${rawTransition.event}`);
      });
    }

    if (!isRecord(screen.effects)) errors.push(`EFFECTS_NOT_OBJECT:${String(screen.id)}`);
    else { exactKeys(screen.effects, ["default"], [], `${path}.effects`, errors); if (!enumValue(screen.effects.default, effectIds)) errors.push(`UNKNOWN_DEFAULT_EFFECT:${String(screen.id)}`); }
    if (!isRecord(screen.validation)) errors.push(`VALIDATION_NOT_OBJECT:${String(screen.id)}`);
    else {
      exactKeys(screen.validation, ["required_context"], [], `${path}.validation`, errors);
      const keys = screen.validation.required_context;
      if (!Array.isArray(keys) || keys.some((key) => typeof key !== "string" || !/^[A-Za-z][A-Za-z0-9_]*$/.test(key)) || (Array.isArray(keys) && new Set(keys).size !== keys.length)) errors.push(`INVALID_REQUIRED_CONTEXT:${String(screen.id)}`);
    }
  });

  if (enumValue(input.initial_screen, screenIds) && !map.has(input.initial_screen)) errors.push("INITIAL_SCREEN_NOT_DEFINED");
  for (const screen of map.values()) if (Array.isArray(screen.transitions)) for (const transition of screen.transitions as unknown[]) {
    if (isRecord(transition) && typeof transition.target === "string" && !map.has(transition.target as ScreenId)) errors.push(`UNKNOWN_TARGET:${screen.id}:${transition.target}`);
  }
  if (enumValue(input.initial_screen, screenIds)) {
    const initial = map.get(input.initial_screen);
    if (initial?.route?.mode !== "PUBLIC") errors.push("INITIAL_SCREEN_NOT_PUBLIC");
    const reachable = new Set<ScreenId>([input.initial_screen]);
    const queue: ScreenId[] = [input.initial_screen];
    while (queue.length) {
      const screen = map.get(queue.shift()!);
      for (const transition of screen?.transitions ?? []) if (isRecord(transition) && typeof transition.target === "string" && map.has(transition.target as ScreenId) && !reachable.has(transition.target as ScreenId)) {
        reachable.add(transition.target as ScreenId);
        queue.push(transition.target as ScreenId);
      }
    }
    for (const id of ["LAUNCH", "PATH_SELECTION", "CASE_SELECTION", "CASE_INTRODUCTION", "INVESTIGATION_BOARD"] as const) if (!reachable.has(id)) errors.push(`UNREACHABLE_PUBLIC_SCREEN:${id}`);
    const resolution = map.get("CASE_RESOLUTION");
    if (reachable.has("CASE_RESOLUTION")) errors.push("INTERNAL_SCREEN_REACHABLE:CASE_RESOLUTION");
    if (resolution && (resolution.route?.mode !== "INTERNAL" || resolution.actions?.length !== 0 || resolution.transitions?.length !== 0)) errors.push("INVALID_INTERNAL_TERMINAL:CASE_RESOLUTION");
  }
  if (errors.length) throw new ScreenConfigurationError("INVALID_SCREEN_SET", errors);
  return map;
}

export const screenSet = raw as ScreenSetManifest;
let validatedDefinitions: ReadonlyMap<ScreenId, ScreenDefinition> = new Map();
let validationFailure: ScreenConfigurationError | null = null;
try { validatedDefinitions = validateScreenSet(raw); }
catch (error: unknown) {
  validationFailure = error instanceof ScreenConfigurationError ? error : new ScreenConfigurationError("INVALID_SCREEN_SET", ["UNEXPECTED_VALIDATION_FAILURE"]);
}
export const screenDefinitions = validatedDefinitions;
export const screenValidationError = validationFailure;
