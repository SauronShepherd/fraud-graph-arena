import { useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { parseLocation } from "./routeCodec";
import { screenDefinitions } from "./definitions";
import type { ScreenId } from "./contracts";

export function useScreenLocation(): { screen: ScreenId; context: Readonly<Record<string, string | number | undefined>> } {
  const location = useLocation();
  const navigate = useNavigate();
  const resolved = parseLocation(location.pathname, location.search, screenDefinitions);
  useEffect(() => {
    if (resolved.replace && location.pathname !== "/") navigate("/", { replace: true });
  }, [location.pathname, navigate, resolved.replace]);
  return resolved;
}
