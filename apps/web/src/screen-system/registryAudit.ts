import type { ScreenSetManifest } from "./contracts";
import { dataSources } from "./dataSources";
import { effects } from "./effects";
import { guards } from "./guards";
import { lifecycle } from "./lifecycle";
import { componentRegistry } from "./componentRegistry";
export function auditRegistries(definitions: ScreenSetManifest): string[] {
  const errors: string[] = [];
  for (const screen of definitions.screens) {
    if (!(screen.data_source in dataSources)) errors.push(`DATA_SOURCE:${screen.data_source}`);
    if (!(screen.component in componentRegistry)) errors.push(`COMPONENT:${screen.component}`);
    for (const hook of [...screen.onLoad, ...screen.onEnter, ...screen.onExit]) if (!(hook in lifecycle)) errors.push(`LIFECYCLE:${hook}`);
    for (const transition of screen.transitions) { if (!(transition.effect in effects)) errors.push(`EFFECT:${transition.effect}`); if (transition.guard && !(transition.guard in guards)) errors.push(`GUARD:${transition.guard}`); }
  }
  return errors;
}
