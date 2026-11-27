import asyncio
import json
from pathlib import Path

from jsonschema import validate
from fastapi.testclient import TestClient

from fraud_graph_arena.observability import InstrumentationConfigError, ObservabilityRecorder, instrumented, load_instrumentation_config

from .conftest import active_t02


ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "contracts" / "observability" / "fga18-instrumentation.json"
SCHEMA_PATH = ROOT / "contracts" / "observability" / "fga18-instrumentation.schema.json"


def test_instrumentation_catalogue_is_declarative_and_schema_valid() -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    document = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    validate(instance=document, schema=schema)
    config = load_instrumentation_config(CONFIG_PATH)
    assert config.schema_version == "1.0.0"
    assert len(config.entries) >= 15
    assert len({entry.identifier for entry in config.entries}) == len(config.entries)
    assert not any(key in CONFIG_PATH.read_text(encoding="utf-8").lower() for key in ("\"code\"", "\"python\"", "\"script\""))


def test_loader_rejects_executable_and_duplicate_entries(tmp_path: Path) -> None:
    document = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    document["instrumentation"][0]["options"]["code"] = "print('no')"
    executable = tmp_path / "executable.json"
    executable.write_text(json.dumps(document), encoding="utf-8")
    try:
        load_instrumentation_config(executable)
    except InstrumentationConfigError:
        pass
    else:
        raise AssertionError("executable configuration was accepted")

    document = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    document["instrumentation"].append(document["instrumentation"][0])
    duplicate = tmp_path / "duplicate.json"
    duplicate.write_text(json.dumps(document), encoding="utf-8")
    try:
        load_instrumentation_config(duplicate)
    except InstrumentationConfigError:
        pass
    else:
        raise AssertionError("duplicate instrumentation was accepted")


def test_disabled_catalogue_entry_is_a_noop_without_changing_the_call(tmp_path: Path) -> None:
    document = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    next(entry for entry in document["instrumentation"] if entry["id"] == "test.async-probe")["enabled"] = False
    disabled = tmp_path / "disabled.json"
    disabled.write_text(json.dumps(document), encoding="utf-8")
    recorder = ObservabilityRecorder(disabled)

    @instrumented("test.async-probe")
    def probe() -> str:
        return "unchanged"

    with recorder.request_context("req", "trace"):
        assert probe() == "unchanged"
    assert recorder.trace("trace")["event_count"] == 0


def test_request_trace_reaches_database_and_analytics_without_sensitive_values(client: TestClient) -> None:
    trace_id = "fga18-test-trace"
    headers = {"X-Trace-ID": trace_id, "X-Correlation-ID": "fga18-test-request"}
    round_id = active_t02(client, headers=headers)
    response = client.post(
        f"/api/v1/rounds/{round_id}/investigations/graph-analytics",
        headers=headers,
        json={"algorithm": "CENTRALITY", "centrality_metric": "degree", "result_limit": 5},
    )
    assert response.status_code == 200, response.text
    assert response.headers["x-trace-id"] == trace_id

    trace = client.app.state.observability.trace(trace_id)
    event_ids = {event["event_id"] for event in trace["events"]}
    assert {"http.request", "domain.graph-analytics.analyze", "repository.economy.reserve", "repository.sqlite.round.charge", "repository.sqlite.ledger.add"} <= event_ids
    assert any(event["event_id"] == "domain.graph-analytics.analyze" and event["algorithm"] == "CENTRALITY" for event in trace["events"])
    assert any(event["event_id"] == "repository.economy.reserve" and event["resource_cost"] == 3 for event in trace["events"])
    assert all(event["trace_id"] == trace_id for event in trace["events"])
    assert all(event["duration_ms"] >= 0 for event in trace["events"])
    serialized = json.dumps(trace, sort_keys=True).lower()
    assert "observability-test-player" not in serialized
    assert "expected_truth" not in serialized
    assert round_id not in serialized


def test_http_failure_is_marked_without_recording_request_body(client: TestClient) -> None:
    trace_id = "fga18-error-trace"
    response = client.get("/api/v1/rounds/not-a-round/workspace", headers={"X-Trace-ID": trace_id})
    assert response.status_code == 404
    events = client.app.state.observability.trace(trace_id)["events"]
    http_events = [event for event in events if event["event_id"] == "http.request"]
    assert http_events
    assert http_events[-1]["status"] == "error"
    assert http_events[-1]["http_status"] == 404


def test_untrusted_trace_headers_are_replaced_with_opaque_ids(client: TestClient) -> None:
    response = client.get(
        "/api/v1/health/live",
        headers={"X-Trace-ID": "person@example.com", "X-Correlation-ID": "bearer-token-value"},
    )
    assert response.status_code == 200
    assert "@" not in response.headers["x-trace-id"]
    serialized = json.dumps(client.app.state.observability.snapshot()).lower()
    assert "person@example.com" not in serialized
    assert "bearer-token-value" not in serialized


def test_sync_and_async_instrumentation_preserve_results_and_exceptions(tmp_path: Path) -> None:
    recorder = ObservabilityRecorder(CONFIG_PATH)

    @instrumented("test.async-probe")
    def sync_probe(value: str) -> str:
        return value

    @instrumented("test.async-probe")
    async def async_probe(value: str) -> str:
        return value

    @instrumented("test.async-probe")
    async def failing_probe() -> None:
        raise RuntimeError("expected test failure")

    with recorder.request_context("req", "trace"):
        assert sync_probe("same") == "same"
        assert asyncio.run(async_probe("again")) == "again"
        try:
            asyncio.run(failing_probe())
        except RuntimeError as error:
            assert str(error) == "expected test failure"
        else:
            raise AssertionError("the instrumented exception was swallowed")

    events = recorder.trace("trace")["events"]
    assert [event["status"] for event in events] == ["ok", "ok", "error"]
    assert all(event["event_id"] == "test.async-probe" for event in events)
