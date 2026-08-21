import raw from "./definitions/fga-screen-set.v1.json";
import type { ScreenDefinition, ScreenId, ScreenSetManifest } from "./contracts";
import { ScreenConfigurationError } from "./contracts";

const ids = new Set<string>(["LAUNCH", "PATH_SELECTION", "CASE_SELECTION", "CASE_INTRODUCTION", "INVESTIGATION_BOARD", "CASE_RESOLUTION"]);
export function validateScreenSet(input: ScreenSetManifest): ReadonlyMap<ScreenId, ScreenDefinition> {
  const errors: string[] = [];
  if (input.schema_version !== "1.0") errors.push("UNSUPPORTED_SCHEMA_VERSION");
  if (!ids.has(input.initial_screen)) errors.push("MISSING_INITIAL_SCREEN");
  const map = new Map<ScreenId, ScreenDefinition>();
  for (const screen of input.screens ?? []) {
    if (map.has(screen.id)) errors.push(`DUPLICATE_SCREEN:${screen.id}`);
    map.set(screen.id, screen);
    if (!ids.has(screen.id) || !ids.has(screen.component)) errors.push(`UNKNOWN_SCREEN:${screen.id}`);
    if (screen.route.mode === "INTERNAL" && screen.route.pattern !== null) errors.push(`INTERNAL_ROUTE:${screen.id}`);
    if (screen.route.mode === "PUBLIC" && !screen.route.pattern) errors.push(`PUBLIC_ROUTE_MISSING:${screen.id}`);
    for (const transition of screen.transitions) if (!ids.has(transition.target)) errors.push(`UNKNOWN_TARGET:${transition.target}`);
    for (const name of screen.validation.required_context) if (!/^[A-Za-z][A-Za-z0-9_]*$/.test(name)) errors.push(`INVALID_CONTEXT:${name}`);
  }
  if (!map.has(input.initial_screen)) errors.push("INITIAL_SCREEN_NOT_DEFINED");
  if (errors.length) throw new ScreenConfigurationError("INVALID_SCREEN_SET", errors);
  return map;
}
export const screenDefinitions = validateScreenSet(raw as ScreenSetManifest);
export const screenSet = raw as ScreenSetManifest;
