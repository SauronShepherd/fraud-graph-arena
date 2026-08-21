import type { ComponentType } from "react";
import type { ComponentId } from "./contracts";
import { BoardPage } from "../pages/BoardPage";
import { CaseSelectionPage } from "../pages/CaseSelectionPage";
import { LaunchPage } from "../pages/LaunchPage";
import { OpeningComicPage } from "../pages/OpeningComicPage";
import { PathSelectionPage } from "../pages/PathSelectionPage";
import { CaseResolutionPage } from "../pages/CaseResolutionPage";

export const componentRegistry: Partial<Record<ComponentId, ComponentType>> = {
  LAUNCH: LaunchPage,
  PATH_SELECTION: PathSelectionPage,
  CASE_SELECTION: CaseSelectionPage,
  CASE_INTRODUCTION: OpeningComicPage,
  INVESTIGATION_BOARD: BoardPage,
  CASE_RESOLUTION: CaseResolutionPage
};
export function resolveComponent(id: ComponentId): ComponentType {
  const component = componentRegistry[id];
  if (!component) throw new Error(`UNKNOWN_SCREEN_COMPONENT:${id}`);
  return component;
}
