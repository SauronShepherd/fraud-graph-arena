"""Run the FGA-17 liveness, readiness and board-access smoke test."""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class SmokeFailure(RuntimeError):
    """Raised when a startup or board-access assertion fails."""


def _request(base_url: str, path: str, *, method: str = "GET", payload: dict[str, Any] | None = None) -> tuple[int, dict[str, Any]]:
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    request = Request(
        f"{base_url.rstrip('/')}{path}",
        data=body,
        method=method,
        headers={"Accept": "application/json", "Content-Type": "application/json"},
    )
    try:
        with urlopen(request, timeout=8) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError) as error:
        detail = getattr(error, "read", lambda: b"")()
        suffix = f": {detail.decode('utf-8', errors='replace')[:300]}" if detail else ""
        raise SmokeFailure(f"{method} {path} failed{suffix}") from error


def run_smoke(base_url: str, *, player_id: str = "fga17-smoke") -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    status, live = _request(base_url, "/api/v1/health/live")
    if status != 200 or live.get("status") != "alive":
        raise SmokeFailure(f"liveness contract failed: {live}")
    checks.append({"name": "liveness", "status": "pass"})

    status, ready = _request(base_url, "/api/v1/health/ready")
    if status != 200 or ready.get("status") != "ready":
        raise SmokeFailure(f"readiness contract failed: {ready}")
    if any(value != "ready" for value in ready.get("checks", {}).values()):
        raise SmokeFailure(f"readiness contains an unavailable check: {ready}")
    checks.append({"name": "readiness", "status": "pass", "checks": ready.get("checks", {})})

    status, catalogue = _request(base_url, "/api/v1/catalogue/DETECTIVE_ACADEMY")
    if status != 200 or catalogue.get("path", {}).get("id") != "DETECTIVE_ACADEMY":
        raise SmokeFailure(f"catalogue contract failed: {catalogue}")
    checks.append({"name": "academy-catalogue", "status": "pass"})

    status, created = _request(
        base_url,
        "/api/v1/rounds",
        method="POST",
        payload={"player_id": player_id, "path_id": "DETECTIVE_ACADEMY", "case_id": "ACADEMY_001"},
    )
    if status != 201 or not created.get("id"):
        raise SmokeFailure(f"round creation failed: {created}")
    round_id = created["id"]
    status, _ = _request(base_url, f"/api/v1/rounds/{round_id}/start", method="POST")
    if status != 200:
        raise SmokeFailure(f"round start failed with HTTP {status}")
    status, _ = _request(base_url, f"/api/v1/rounds/{round_id}/opening")
    if status != 200:
        raise SmokeFailure(f"opening retrieval failed with HTTP {status}")
    status, _ = _request(
        base_url,
        f"/api/v1/rounds/{round_id}/opening/complete",
        method="POST",
        payload={"completion": "FINISHED"},
    )
    if status != 200:
        raise SmokeFailure(f"opening completion failed with HTTP {status}")
    status, workspace = _request(base_url, f"/api/v1/rounds/{round_id}/workspace")
    if status != 200 or workspace.get("round", {}).get("id") != round_id:
        raise SmokeFailure(f"board access failed: {workspace}")
    checks.append({"name": "board-access", "status": "pass", "round_id": round_id})

    return {
        "status": "pass",
        "run_at_utc": datetime.now(UTC).isoformat(),
        "base_url": base_url.rstrip("/"),
        "checks": checks,
        "identity_boundary": "local player_id session; no external identity provider is claimed",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--player-id", default="fga17-smoke")
    args = parser.parse_args()
    report = run_smoke(args.base_url, player_id=args.player_id)
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
