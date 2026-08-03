export function Loading({ message = "Following the trail…" }: { message?: string }) {
  return <p className="loading" role="status">{message}</p>;
}
