"""Run the FGA-18 click-to-analytics trace smoke test locally."""

from __future__ import annotations

import json
import gc
from pathlib import Path
import sys
import tempfile

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from fraud_graph_arena.application import create_app
from fraud_graph_arena.config import Settings


def _expect(response, status: int) -> dict:
    assert response.status_code == status, response.text
    return response.json() if response.content else {}


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="fga18-observability-") as directory:
        root = Path(directory)
        settings = Settings(
            environment="test",
            round_repository="sqlite",
            sqlite_path=root / "rounds.sqlite3",
            frontend_dist=root / "missing",
            allowed_origins=[],
        )
        with TestClient(create_app(settings)) as client:
            trace_id = "fga18-local-smoke"
            headers = {"X-Trace-ID": trace_id, "X-Correlation-ID": "fga18-local-request"}
            created = _expect(
                client.post(
                    "/api/v1/rounds",
                    headers=headers,
                    json={"player_id": "smoke-player", "path_id": "DETECTIVE_ACADEMY", "case_id": "ACADEMY_T02"},
                ),
                201,
            )
            round_id = created["id"]
            _expect(client.post(f"/api/v1/rounds/{round_id}/start", headers=headers), 200)
            _expect(client.post(f"/api/v1/rounds/{round_id}/opening/complete", headers=headers), 200)
            _expect(
                client.post(
                    f"/api/v1/rounds/{round_id}/investigations/graph-analytics",
                    headers=headers,
                    json={"algorithm": "CENTRALITY", "centrality_metric": "degree", "result_limit": 5},
                ),
                200,
            )
            trace = client.app.state.observability.trace(trace_id)
            event_ids = sorted({event["event_id"] for event in trace["events"]})
            required = {
                "http.request",
                "domain.graph-analytics.analyze",
                "repository.economy.reserve",
                "repository.sqlite.round.charge",
                "repository.sqlite.ledger.add",
            }
            assert required <= set(event_ids)
            serialized = json.dumps(trace, sort_keys=True).lower()
            assert round_id not in serialized
            assert "smoke-player" not in serialized
            assert "expected_truth" not in serialized
            report = {
                "status": "pass",
                "trace_id": trace_id,
                "event_count": trace["event_count"],
                "event_ids": event_ids,
                "metrics": trace["metrics"],
                "redaction_checks": {"round_id": True, "player_id": True, "hidden_truth": True},
            }
            print(json.dumps(report, indent=2, sort_keys=True))
        del client
        gc.collect()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
