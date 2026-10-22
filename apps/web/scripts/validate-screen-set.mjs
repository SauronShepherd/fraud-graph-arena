import { readFileSync } from "node:fs";
import { parseJsonRejectDuplicateKeys } from "./json-duplicate-check.mjs";

const sourcePath = process.argv[2] ?? "src/screen-system/definitions/fga-screen-set.v1.json";
const value = parseJsonRejectDuplicateKeys(readFileSync(sourcePath, "utf8"));
const errors = [];
const screensAllowed = ["LAUNCH", "PATH_SELECTION", "CASE_SELECTION", "CASE_INTRODUCTION", "INVESTIGATION_BOARD", "CASE_RESOLUTION"];
const actionsAllowed = ["BEGIN", "RESUME_LAST_ROUND", "SELECT_PATH", "BACK_TO_PATHS", "OPEN_CASE", "CHANGE_INTRO_PAGE", "COMPLETE_INTRO", "SKIP_INTRO", "RETURN_TO_CATALOGUE"];
const eventsAllowed = ["PATHS_REQUESTED", "ROUND_RESUME_REQUESTED", "PATH_SELECTED", "CASE_OPENED", "INTRO_PAGE_CHANGED", "INTRODUCTION_COMPLETED", "INTRODUCTION_SKIPPED", "INTRODUCTION_ALREADY_COMPLETED", "INTRODUCTION_REQUIRED", "RETURNED_TO_PATHS", "RETURNED_TO_CATALOGUE"];
const dataSourcesAllowed = ["LAST_ROUND_POINTER", "CATALOGUE_SECTIONS", "CATALOGUE_SECTION", "ROUND_OPENING", "ROUND_WORKSPACE", "RESOLUTION_CONTEXT"];
const effectsAllowed = ["NONE", "FADE_TO_BLACK"];
const guardsAllowed = ["REQUIRED_CONTEXT", "ACTION_NOT_PENDING", "ROUND_ACTIVE", "ROUND_INTRO_PENDING"];
const lifecycleAllowed = ["LOAD_SCREEN_MODEL", "FOCUS_PRIMARY_HEADING", "ANNOUNCE_SCREEN", "ABORT_OBSOLETE_READS"];
const outcomes = {
  BEGIN: ["PATHS_REQUESTED"], RESUME_LAST_ROUND: ["ROUND_RESUME_REQUESTED"], SELECT_PATH: ["PATH_SELECTED"],
  BACK_TO_PATHS: ["RETURNED_TO_PATHS"], OPEN_CASE: ["CASE_OPENED"], CHANGE_INTRO_PAGE: ["INTRO_PAGE_CHANGED"],
  COMPLETE_INTRO: ["INTRODUCTION_COMPLETED"], SKIP_INTRO: ["INTRODUCTION_SKIPPED"], RETURN_TO_CATALOGUE: ["RETURNED_TO_CATALOGUE"]
};
const runtimeEventsByScreen = {
  CASE_INTRODUCTION: ["INTRODUCTION_ALREADY_COMPLETED"],
  INVESTIGATION_BOARD: ["INTRODUCTION_REQUIRED"]
};
const exactKeys = (object, allowed, path) => {
  for (const key of Object.keys(object ?? {})) if (!allowed.includes(key)) errors.push(`unknown_field:${path}.${key}`);
  for (const key of allowed) if (!(key in (object ?? {}))) errors.push(`missing_field:${path}.${key}`);
};
const version = (text) => typeof text === "string" && /^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$/.test(text) ? text.split(".").map(Number) : null;
const compatible = (minimum, runtime = "1.0.0") => {
  const a = version(minimum); const b = version(runtime);
  if (!a || !b) return false;
  for (let i = 0; i < 3; i += 1) if (a[i] !== b[i]) return a[i] < b[i];
  return true;
};

if (!value || typeof value !== "object" || Array.isArray(value)) throw new Error("Screen set root must be an object");
exactKeys(value, ["schema_version", "document_version", "minimum_runtime_version", "screen_set_id", "screen_set_version", "initial_screen", "screens"], "root");
if (value.schema_version !== "1.0") errors.push("schema_version");
if (typeof value.document_version !== "string" || !value.document_version.trim()) errors.push("document_version");
if (value.screen_set_id !== "FGA03") errors.push("screen_set_id");
if (typeof value.screen_set_version !== "string" || !value.screen_set_version.trim()) errors.push("screen_set_version");
if (!compatible(value.minimum_runtime_version)) errors.push("minimum_runtime_version");
if (!Array.isArray(value.screens) || value.screens.length === 0) errors.push("screens");

const byId = new Map();
const routeShapes = new Map();
const screenList = Array.isArray(value.screens) ? value.screens : [];
for (const [index, screen] of screenList.entries()) {
  const path = `screens[${index}]`;
  if (!screen || typeof screen !== "object" || Array.isArray(screen)) { errors.push(`screen_object:${path}`); continue; }
  exactKeys(screen, ["schema_version", "document_version", "minimum_runtime_version", "id", "component", "route", "data_source", "onLoad", "onEnter", "onExit", "actions", "transitions", "effects", "validation"], path);
  if (!screensAllowed.includes(screen.id) || screen.component !== screen.id) errors.push(`screen_component:${path}`);
  if (byId.has(screen.id)) errors.push(`duplicate_screen:${screen.id}`); else byId.set(screen.id, screen);
  if (screen.schema_version !== value.schema_version || !compatible(screen.minimum_runtime_version)) errors.push(`screen_version:${screen.id}`);
  if (typeof screen.document_version !== "string" || !screen.document_version.trim()) errors.push(`document_version:${screen.id}`);
  if (!dataSourcesAllowed.includes(screen.data_source)) errors.push(`data_source:${screen.id}`);
  for (const field of ["onLoad", "onEnter", "onExit"]) {
    const hooks = screen[field];
    if (!Array.isArray(hooks) || hooks.some((hook) => !lifecycleAllowed.includes(hook)) || new Set(hooks).size !== hooks.length) errors.push(`lifecycle:${screen.id}:${field}`);
  }
  const route = screen.route;
  if (!route || typeof route !== "object" || !["PUBLIC", "INTERNAL"].includes(route.mode)) errors.push(`route:${screen.id}`);
  else if (route.mode === "PUBLIC") {
    if (typeof route.pattern !== "string" || !route.pattern.startsWith("/")) errors.push(`route_pattern:${screen.id}`);
    else {
      const params = [...route.pattern.matchAll(/:([A-Za-z0-9_]+)/g)].map((match) => match[1]);
      const shape = route.pattern.replace(/:[A-Za-z0-9_]+/g, ":PARAM");
      if (routeShapes.has(shape)) errors.push(`ambiguous_route:${routeShapes.get(shape)}:${screen.id}`); else routeShapes.set(shape, screen.id);
      if (!Array.isArray(screen.validation?.required_context) || params.some((param) => !screen.validation.required_context.includes(param))) errors.push(`route_context:${screen.id}`);
      try { const compiled = route.pattern.replace(/[.*+?^${}()|[\]\\]/g, "\\$&").replace(/:[A-Za-z0-9_]+/g, "([^/]+)"); new RegExp(`^${compiled}$`); }
      catch { errors.push(`route_regex:${screen.id}`); }
    }
  } else if (route.pattern !== null) errors.push(`internal_route_pattern:${screen.id}`);

  if (!Array.isArray(screen.actions)) errors.push(`actions:${screen.id}`);
  else {
    const seen = new Set();
    for (const action of screen.actions) {
      if (!action || typeof action !== "object") { errors.push(`action_shape:${screen.id}`); continue; }
      exactKeys(action, ["id", "handler"], `${path}.actions`);
      if (!actionsAllowed.includes(action.id) || !actionsAllowed.includes(action.handler)) errors.push(`action_enum:${screen.id}`);
      if (seen.has(action.id)) errors.push(`duplicate_action:${screen.id}:${action.id}`); seen.add(action.id);
      if (!(outcomes[action.handler] ?? []).some((event) => (screen.transitions ?? []).some((transition) => transition.event === event))) errors.push(`action_transition:${screen.id}:${action.id}`);
    }
  }
  if (!Array.isArray(screen.transitions)) errors.push(`transitions:${screen.id}`);
  else {
    const seen = new Set();
    for (const transition of screen.transitions) {
      if (!transition || typeof transition !== "object") { errors.push(`transition_shape:${screen.id}`); continue; }
      exactKeys(transition, ["event", "target", "effect", "history", ...(Object.hasOwn(transition, "guard") ? ["guard"] : [])], `${path}.transitions`);
      if (!eventsAllowed.includes(transition.event) || !screensAllowed.includes(transition.target) || !effectsAllowed.includes(transition.effect) || !["PUSH", "REPLACE"].includes(transition.history)) errors.push(`transition_enum:${screen.id}`);
      if (transition.guard !== undefined && !guardsAllowed.includes(transition.guard)) errors.push(`guard:${screen.id}`);
      if (seen.has(transition.event)) errors.push(`duplicate_transition:${screen.id}:${transition.event}`); seen.add(transition.event);
      const actionEmitsEvent = (screen.actions ?? []).some((action) => outcomes[action.handler]?.includes(transition.event));
      const runtimeEmitsEvent = (runtimeEventsByScreen[screen.id] ?? []).includes(transition.event);
      if (!runtimeEmitsEvent && !actionEmitsEvent) errors.push(`unemitted_event:${screen.id}:${transition.event}`);
    }
  }
  if (!screen.effects || typeof screen.effects !== "object" || !effectsAllowed.includes(screen.effects.default)) errors.push(`effects:${screen.id}`);
  if (!screen.validation || !Array.isArray(screen.validation.required_context) || screen.validation.required_context.some((key) => typeof key !== "string" || !/^[A-Za-z][A-Za-z0-9_]*$/.test(key)) || new Set(screen.validation.required_context).size !== screen.validation.required_context.length) errors.push(`validation:${screen.id}`);
}
if (!byId.has(value.initial_screen) || byId.get(value.initial_screen)?.route.mode !== "PUBLIC") errors.push("initial_screen");
for (const screen of byId.values()) for (const transition of screen.transitions ?? []) if (!byId.has(transition.target)) errors.push(`unknown_target:${screen.id}:${transition.target}`);
const reachable = new Set([value.initial_screen]); const queue = [value.initial_screen];
while (queue.length) for (const transition of byId.get(queue.shift())?.transitions ?? []) if (!reachable.has(transition.target)) { reachable.add(transition.target); queue.push(transition.target); }
for (const id of ["LAUNCH", "PATH_SELECTION", "CASE_SELECTION", "CASE_INTRODUCTION", "INVESTIGATION_BOARD"]) if (!reachable.has(id)) errors.push(`unreachable:${id}`);
if (reachable.has("CASE_RESOLUTION")) errors.push("internal_screen_reachable:CASE_RESOLUTION");
const resolution = byId.get("CASE_RESOLUTION");
if (resolution && (resolution.route.mode !== "INTERNAL" || resolution.actions.length !== 0 || resolution.transitions.length !== 0)) errors.push("invalid_internal_terminal");

if (errors.length) { console.error(`Invalid screen set: ${errors.join(", ")}`); process.exit(1); }
console.log(`Validated screen set: ${value.screens.length} screens`);
