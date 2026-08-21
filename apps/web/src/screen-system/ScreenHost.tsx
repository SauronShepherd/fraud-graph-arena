import { useEffect, useRef, useState, type PropsWithChildren } from "react";
import type { ScreenDefinition, ScreenId } from "./contracts";
import { lifecycle } from "./lifecycle";
import { ScreenAnnouncer } from "./ScreenAnnouncer";

export function ScreenHost({ definition, screen, children }: PropsWithChildren<{ definition: ScreenDefinition; screen: ScreenId }>) {
  const [announcement, setAnnouncement] = useState(screen.replaceAll("_", " "));
  const abortController = useRef<AbortController | null>(null);
  useEffect(() => {
    abortController.current?.abort();
    abortController.current = new AbortController();
    const services = { focusPrimaryHeading: () => document.querySelector<HTMLElement>("h1, h2")?.focus(), announce: setAnnouncement, abortReads: () => abortController.current?.abort() };
    definition.onEnter.forEach((hook) => lifecycle[hook](services));
    return () => definition.onExit.forEach((hook) => lifecycle[hook](services));
  }, [definition, screen]);
  return <><ScreenAnnouncer message={announcement} /><section data-screen-id={screen}>{children}</section></>;
}
