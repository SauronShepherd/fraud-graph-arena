export type ScreenId = "LAUNCH" | "PATH_SELECTION" | "CASE_SELECTION" | "CASE_INTRODUCTION" | "INVESTIGATION_BOARD" | "CASE_RESOLUTION";
export type ComponentId = ScreenId;
export type DataSourceId = "LAST_ROUND_POINTER" | "CATALOGUE_SECTIONS" | "CATALOGUE_SECTION" | "ROUND_OPENING" | "ROUND_WORKSPACE" | "RESOLUTION_CONTEXT";
export type LifecycleHookId = "LOAD_SCREEN_MODEL" | "FOCUS_PRIMARY_HEADING" | "ANNOUNCE_SCREEN" | "ABORT_OBSOLETE_READS";
export type ActionId = "BEGIN" | "RESUME_LAST_ROUND" | "SELECT_PATH" | "BACK_TO_PATHS" | "OPEN_CASE" | "CHANGE_INTRO_PAGE" | "COMPLETE_INTRO" | "SKIP_INTRO" | "RETURN_TO_CATALOGUE";
export type EventId = "PATHS_REQUESTED" | "PATH_SELECTED" | "CASE_OPENED" | "ROUND_RESUMED" | "INTRO_PAGE_CHANGED" | "INTRODUCTION_COMPLETED" | "INTRODUCTION_SKIPPED" | "RETURNED_TO_PATHS" | "RETURNED_TO_CATALOGUE";
export type GuardId = "REQUIRED_CONTEXT" | "ROUTE_ALLOWED" | "ACTION_NOT_PENDING";
export type EffectId = "NONE" | "FADE_TO_BLACK";
export type HistoryPolicy = "PUSH" | "REPLACE";
export type RouteMode = "PUBLIC" | "INTERNAL";

export interface RouteDefinition { mode: RouteMode; pattern: string | null; }
export interface TransitionDefinition { event: EventId; target: ScreenId; effect: EffectId; history: HistoryPolicy; guard?: GuardId; }
export interface ActionDefinition { id: ActionId; handler: ActionId; }
export interface ScreenDefinition {
  schema_version: "1.0"; id: ScreenId; component: ComponentId; route: RouteDefinition;
  data_source: DataSourceId; onLoad: LifecycleHookId[]; onEnter: LifecycleHookId[]; onExit: LifecycleHookId[];
  actions: ActionDefinition[]; transitions: TransitionDefinition[]; effects: { default: EffectId };
  validation: { required_context: string[] };
}
export interface ScreenSetManifest { schema_version: "1.0"; screen_set_id: string; screen_set_version: string; initial_screen: ScreenId; screens: ScreenDefinition[]; }
export type ScreenContext = Readonly<Record<string, string | number | undefined>>;
export interface MachineEvent { type: EventId; context?: ScreenContext; }
export interface TransitionPlan { source: ScreenId; target: ScreenId; context: ScreenContext; effect: EffectId; history: HistoryPolicy; event: EventId; }

export class ScreenConfigurationError extends Error {
  constructor(readonly code: string, readonly diagnostics: string[]) { super(`Screen configuration error: ${code}`); this.name = "ScreenConfigurationError"; }
}
