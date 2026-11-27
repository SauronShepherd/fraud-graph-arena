from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, replace
from datetime import UTC, datetime
from functools import wraps
import hashlib
import hmac
import inspect
import json
import logging
from pathlib import Path
import secrets
from threading import RLock
from time import perf_counter
from typing import Any, Callable, Iterator, TypeVar
from uuid import uuid4


T = TypeVar("T")

_SENSITIVE_KEYS = {
    "access_token",
    "api_key",
    "authorization",
    "cookie",
    "credential",
    "email",
    "expected_truth",
    "password",
    "player_id",
    "secret",
    "token",
    "truth",
}
_IDENTIFIER_KEYS = {"candidate_id", "record_id", "round_id", "session_id", "submission_id"}
_SAFE_CALL_KEYS = {"action", "algorithm", "case_id", "completion", "outcome", "path_id", "relationship_type"}


@dataclass(frozen=True, slots=True)
class ObservationContext:
    request_id: str = "unknown"
    trace_id: str = "unknown"
    round_ref: str | None = None
    path_id: str | None = None
    case_id: str | None = None


_RECORDER: ContextVar[ObservabilityRecorder | None] = ContextVar("fga_observability_recorder", default=None)
_CONTEXT: ContextVar[ObservationContext] = ContextVar("fga_observability_context", default=ObservationContext())
_SPAN: ContextVar[str | None] = ContextVar("fga_observability_span", default=None)


@dataclass(frozen=True, slots=True)
class InstrumentationSpec:
    identifier: str
    target: str
    kind: str
    enabled: bool
    redaction_policy: str
    options: dict[str, Any]


class InstrumentationConfigError(ValueError):
    """Raised when the declarative instrumentation catalogue is unsafe or invalid."""


@dataclass(frozen=True, slots=True)
class InstrumentationConfig:
    schema_version: str
    default_enabled: bool
    default_redaction_policy: str
    entries: tuple[InstrumentationSpec, ...]

    @classmethod
    def from_mapping(cls, raw: dict[str, Any]) -> "InstrumentationConfig":
        if not isinstance(raw, dict):
            raise InstrumentationConfigError("instrumentation config must be an object")
        forbidden = {"code", "callable", "expression", "python", "script"}
        if any(key in raw for key in forbidden):
            raise InstrumentationConfigError("instrumentation config cannot contain executable content")
        defaults = raw.get("defaults", {})
        entries = raw.get("instrumentation", [])
        if not isinstance(defaults, dict) or not isinstance(entries, list):
            raise InstrumentationConfigError("instrumentation config has invalid defaults or entries")
        specs: list[InstrumentationSpec] = []
        seen: set[str] = set()
        for entry in entries:
            if not isinstance(entry, dict):
                raise InstrumentationConfigError("each instrumentation entry must be an object")
            if any(key in entry for key in forbidden):
                raise InstrumentationConfigError("instrumentation entry cannot contain executable content")
            identifier = str(entry.get("id", "")).strip()
            target = str(entry.get("target", "")).strip()
            kind = str(entry.get("kind", "")).strip()
            if not identifier or not target or not kind:
                raise InstrumentationConfigError("instrumentation entries require id, target and kind")
            if identifier in seen:
                raise InstrumentationConfigError(f"duplicate instrumentation id: {identifier}")
            seen.add(identifier)
            options = entry.get("options", {})
            if not isinstance(options, dict):
                raise InstrumentationConfigError(f"options must be an object: {identifier}")
            if any(key in options for key in forbidden):
                raise InstrumentationConfigError(f"instrumentation options cannot contain executable content: {identifier}")
            specs.append(
                InstrumentationSpec(
                    identifier=identifier,
                    target=target,
                    kind=kind,
                    enabled=bool(entry.get("enabled", defaults.get("enabled", True))),
                    redaction_policy=str(entry.get("redaction_policy", defaults.get("redaction_policy", "safe"))),
                    options=dict(options),
                )
            )
        return cls(
            schema_version=str(raw.get("schema_version", "")),
            default_enabled=bool(defaults.get("enabled", True)),
            default_redaction_policy=str(defaults.get("redaction_policy", "safe")),
            entries=tuple(specs),
        )

    def get(self, identifier: str) -> InstrumentationSpec | None:
        return next((entry for entry in self.entries if entry.identifier == identifier), None)

    def enabled(self, identifier: str) -> bool:
        spec = self.get(identifier)
        return False if spec is None else spec.enabled


def load_instrumentation_config(path: Path) -> InstrumentationConfig:
    raw = json.loads(path.read_text(encoding="utf-8"))
    config = InstrumentationConfig.from_mapping(raw)
    if config.schema_version != "1.0.0":
        raise InstrumentationConfigError(f"unsupported instrumentation schema: {config.schema_version}")
    return config


def current_recorder() -> "ObservabilityRecorder | None":
    return _RECORDER.get()


def _current_context() -> ObservationContext:
    return _CONTEXT.get()


def _normalise_status(value: Any) -> str | None:
    if value is None:
        return None
    candidate = getattr(value, "value", value)
    if isinstance(candidate, (str, int, float, bool)):
        return str(candidate)
    return None


def _result_fields(result: Any) -> dict[str, Any]:
    fields: dict[str, Any] = {}
    if result is None:
        return fields
    if isinstance(result, dict):
        for name in ("http_status", "error_code", "resource_cost"):
            value = result.get(name)
            if isinstance(value, (str, int, float, bool)):
                fields[name] = value
        return fields
    if isinstance(result, tuple):
        for item in result:
            fields.update(_result_fields(item))
        return fields
    for name in ("status", "result_type", "generation_mode", "actual_engine_run", "cached", "replayed"):
        if hasattr(result, name):
            value = getattr(result, name)
            normalised = _normalise_status(value)
            if normalised is not None:
                fields[name] = normalised if name != "actual_engine_run" and name != "cached" and name != "replayed" else bool(value)
    charged = getattr(result, "charged_credits", None)
    if isinstance(charged, int):
        fields["resource_cost"] = charged
    entry = getattr(result, "entry", None)
    amount = getattr(entry, "amount", None)
    if isinstance(amount, int):
        fields["resource_cost"] = amount
    return fields


def _exception_fields(error: BaseException) -> dict[str, str]:
    code = getattr(error, "code", None)
    return {
        "error_type": type(error).__name__,
        **({"error_code": str(code)} if code else {}),
    }


def _scrub_key(key: str) -> str:
    return key.strip().lower().replace("-", "_")


class ObservabilityRecorder:
    """In-process event, metric and trace sink with an intentionally small safe surface."""

    def __init__(self, config_path: Path, *, log_level: str = "INFO", enabled: bool = True) -> None:
        self.config = load_instrumentation_config(config_path)
        self.enabled = enabled
        self._events: list[dict[str, Any]] = []
        self._metrics: dict[str, dict[str, float | int]] = {}
        self._lock = RLock()
        self._reference_key = secrets.token_bytes(32)
        self._logger = logging.getLogger("fraud_graph_arena.observability")
        self._logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    @contextmanager
    def request_context(self, request_id: str, trace_id: str) -> Iterator[None]:
        recorder_token = _RECORDER.set(self)
        context_token = _CONTEXT.set(ObservationContext(request_id=request_id, trace_id=trace_id))
        try:
            yield
        finally:
            _CONTEXT.reset(context_token)
            _RECORDER.reset(recorder_token)

    @contextmanager
    def bind(self, *, round_id: str | None = None, path_id: str | None = None, case_id: str | None = None) -> Iterator[None]:
        current = _current_context()
        updated = replace(
            current,
            round_ref=self.reference(round_id) if round_id else current.round_ref,
            path_id=path_id or current.path_id,
            case_id=case_id or current.case_id,
        )
        token = _CONTEXT.set(updated)
        try:
            yield
        finally:
            _CONTEXT.reset(token)

    def reference(self, value: str) -> str:
        digest = hmac.new(self._reference_key, value.encode("utf-8"), hashlib.sha256).hexdigest()
        return f"ref_{digest[:16]}"

    def call_fields(self, function: Callable[..., Any], args: tuple[Any, ...], kwargs: dict[str, Any]) -> dict[str, Any]:
        try:
            bound = inspect.signature(function).bind_partial(*args, **kwargs)
        except (TypeError, ValueError):
            return {}
        fields: dict[str, Any] = {}
        for key, value in bound.arguments.items():
            normalized = _scrub_key(key)
            if normalized in _SAFE_CALL_KEYS and isinstance(value, (str, int, float, bool)):
                fields[normalized] = _normalise_status(value)
            elif normalized in _IDENTIFIER_KEYS and isinstance(value, str):
                fields[f"{normalized[:-3]}_ref" if normalized.endswith("_id") else f"{normalized}_ref"] = self.reference(value)
            elif normalized == "idempotency_key":
                fields["idempotency_key_present"] = bool(value)
            elif normalized in {"request", "input", "payload"} and isinstance(value, dict):
                for nested_key in _SAFE_CALL_KEYS:
                    nested_value = value.get(nested_key)
                    if isinstance(nested_value, (str, int, float, bool)):
                        fields[nested_key] = _normalise_status(nested_value)
        return fields

    @contextmanager
    def call_context(self, function: Callable[..., Any], args: tuple[Any, ...], kwargs: dict[str, Any]) -> Iterator[None]:
        try:
            bound = inspect.signature(function).bind_partial(*args, **kwargs)
        except (TypeError, ValueError):
            yield
            return
        round_id = bound.arguments.get("round_id")
        path_id = bound.arguments.get("path_id")
        case_id = bound.arguments.get("case_id")
        with self.bind(
            round_id=round_id if isinstance(round_id, str) else None,
            path_id=path_id if isinstance(path_id, str) else None,
            case_id=case_id if isinstance(case_id, str) else None,
        ):
            yield

    @contextmanager
    def span(self, identifier: str, fields: dict[str, Any] | None = None) -> Iterator[dict[str, Any]]:
        if not self.enabled or not self.config.enabled(identifier):
            yield {}
            return
        spec = self.config.get(identifier)
        span_id = uuid4().hex[:16]
        parent_span = _SPAN.get()
        span_token = _SPAN.set(span_id)
        state: dict[str, Any] = {"result": None}
        started = perf_counter()
        started_at = datetime.now(UTC).isoformat()
        try:
            yield state
        except Exception as error:
            self._finish(
                identifier,
                spec,
                span_id,
                parent_span,
                started_at,
                started,
                fields or {},
                status="error",
                result_fields=_exception_fields(error),
            )
            raise
        else:
            result = state.get("result")
            self._finish(
                identifier,
                spec,
                span_id,
                parent_span,
                started_at,
                started,
                fields or {},
                status=str(state.get("status", "ok")),
                result_fields=_result_fields(result),
            )
        finally:
            _SPAN.reset(span_token)

    def _finish(
        self,
        identifier: str,
        spec: InstrumentationSpec | None,
        span_id: str,
        parent_span: str | None,
        started_at: str,
        started: float,
        fields: dict[str, Any],
        *,
        status: str,
        result_fields: dict[str, Any],
    ) -> None:
        context = _current_context()
        event = {
            "timestamp_utc": datetime.now(UTC).isoformat(),
            "started_at_utc": started_at,
            "event_id": identifier,
            "kind": spec.kind if spec is not None else "operation",
            "request_id": context.request_id,
            "trace_id": context.trace_id,
            "span_id": span_id,
            "parent_span_id": parent_span,
            "status": status,
            "duration_ms": max(0, round((perf_counter() - started) * 1000, 3)),
            **({"round_ref": context.round_ref} if context.round_ref else {}),
            **({"path_id": context.path_id} if context.path_id else {}),
            **({"case_id": context.case_id} if context.case_id else {}),
            **fields,
            **result_fields,
        }
        safe = self._safe_event(event)
        with self._lock:
            self._events.append(safe)
            metric = self._metrics.setdefault(f"{identifier}|{status}", {"count": 0, "duration_ms_total": 0.0, "duration_ms_max": 0.0})
            metric["count"] = int(metric["count"]) + 1
            metric["duration_ms_total"] = float(metric["duration_ms_total"]) + float(safe["duration_ms"])
            metric["duration_ms_max"] = max(float(metric["duration_ms_max"]), float(safe["duration_ms"]))
        self._logger.info(json.dumps(safe, sort_keys=True, separators=(",", ":")))

    def _safe_event(self, event: dict[str, Any]) -> dict[str, Any]:
        safe: dict[str, Any] = {}
        for raw_key, value in event.items():
            key = _scrub_key(raw_key)
            if key in _SENSITIVE_KEYS or any(token in key for token in ("password", "token", "secret", "credential")):
                continue
            if key in {"record_id", "candidate_id", "submission_id", "session_id"}:
                continue
            if key == "round_id":
                if isinstance(value, str):
                    safe["round_ref"] = self.reference(value)
                continue
            if isinstance(value, (str, int, float, bool)) or value is None:
                safe[key] = value
            elif isinstance(value, (list, tuple)):
                safe[key] = [item for item in value if isinstance(item, (str, int, float, bool))][:20]
        return safe

    def snapshot(self) -> dict[str, Any]:
        with self._lock:
            return {
                "event_count": len(self._events),
                "events": [dict(event) for event in self._events],
                "metrics": {key: dict(value) for key, value in self._metrics.items()},
            }

    def trace(self, trace_id: str) -> dict[str, Any]:
        snapshot = self.snapshot()
        snapshot["events"] = [event for event in snapshot["events"] if event.get("trace_id") == trace_id]
        snapshot["event_count"] = len(snapshot["events"])
        return snapshot


def instrumented(identifier: str):
    """Decorate a narrow operation without changing return values or exceptions."""

    def decorate(function: Callable[..., T]) -> Callable[..., T]:
        if inspect.iscoroutinefunction(function):
            @wraps(function)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                recorder = current_recorder()
                if recorder is None:
                    return await function(*args, **kwargs)  # type: ignore[misc]
                with recorder.call_context(function, args, kwargs):
                    with recorder.span(identifier, recorder.call_fields(function, args, kwargs)) as span:
                        result = await function(*args, **kwargs)  # type: ignore[misc]
                        span["result"] = result
                        return result

            return async_wrapper  # type: ignore[return-value]

        @wraps(function)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            recorder = current_recorder()
            if recorder is None:
                return function(*args, **kwargs)
            with recorder.call_context(function, args, kwargs):
                with recorder.span(identifier, recorder.call_fields(function, args, kwargs)) as span:
                    result = function(*args, **kwargs)
                    span["result"] = result
                    return result

        return sync_wrapper  # type: ignore[return-value]

    return decorate
