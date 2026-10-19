import { useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { locationFor, parseLocation } from "./routeCodec";
import { screenDefinitions } from "./definitions";
import type { ScreenId } from "./contracts";

export function useScreenLocation(): { screen: ScreenId; context: Readonly<Record<string, string | number | undefined>> } {
  const location = useLocation();
  const navigate = useNavigate();
  const resolved = parseLocation(location.pathname, location.search, screenDefinitions);
  const definition = screenDefinitions.get(resolved.screen);
  const canonicalLocation = definition ? locationFor(definition, resolved.context) : "/";
  useEffect(() => {
    if (resolved.replace && `${location.pathname}${location.search}` !== canonicalLocation) navigate(canonicalLocation, { replace: true });
  }, [canonicalLocation, location.pathname, location.search, navigate, resolved.replace]);
  return resolved;
}
