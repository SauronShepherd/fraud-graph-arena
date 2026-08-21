import { useEffect, useState } from "react";
export function ScreenAnnouncer({ message }: { message: string }) {
  const [announcement, setAnnouncement] = useState(message);
  useEffect(() => { setAnnouncement(message); }, [message]);
  return <p className="screen-announcer" role="status" aria-live="polite" aria-atomic="true">{announcement}</p>;
}
