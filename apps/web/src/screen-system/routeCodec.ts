import type { ScreenContext, ScreenId } from "./contracts";
import type { ScreenDefinition } from "./contracts";
export function parseLocation(pathname: string, search: string, definitions: ReadonlyMap<ScreenId, ScreenDefinition>): { screen: ScreenId; context: ScreenContext; replace: boolean } {
  for (const definition of definitions.values()) {
    const pattern = definition.route.pattern;
    if (!pattern) continue;
    const names = [...pattern.matchAll(/:([A-Za-z0-9_]+)/g)].map((match) => match[1]);
    const regex = new RegExp(`^${pattern.replace(/:[A-Za-z0-9_]+/g, "([^/]+)")}$`);
    const match = pathname.match(regex);
    if (!match) continue;
    const context: Record<string, string | number> = {};
    names.forEach((name, index) => { context[name] = decodeURIComponent(match[index + 1]); });
    const page = new URLSearchParams(search).get("page");
    if (definition.id === "CASE_INTRODUCTION" && page) context.page = Number(page) || 1;
    return { screen: definition.id, context, replace: false };
  }
  return { screen: "LAUNCH", context: {}, replace: pathname !== "/" };
}
export function locationFor(definition: ScreenDefinition, context: ScreenContext): string {
  if (!definition.route.pattern) return "/";
  let path = definition.route.pattern.replace(/:([A-Za-z0-9_]+)/g, (_, key: string) => encodeURIComponent(String(context[key] ?? "")));
  if (definition.id === "CASE_INTRODUCTION" && context.page !== undefined) path += `?page=${encodeURIComponent(String(context.page))}`;
  return path;
}
