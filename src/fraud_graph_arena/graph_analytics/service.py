from __future__ import annotations

from dataclasses import replace
import hashlib
import json
from threading import RLock
from time import perf_counter
from uuid import uuid4
from typing import Any, Callable

from fraud_graph_arena.economy import EconomyService
from fraud_graph_arena.rounds.domain import RoundStatus
from fraud_graph_arena.rounds.service import RoundService
from fraud_graph_arena.shared.errors import ConflictError, InvalidRequestError, NotFoundError
from fraud_graph_arena.observability import instrumented

from .engine import (
    FRAMEWORK_SEMANTICS,
    GRAPH_ANALYTICS_VERSION,
    GRAPH_ENGINE,
    GraphAnalyticsEngine,
)
from .models import GRAPH_ANALYTICS_ALGORITHMS, GraphAnalysisResult


MAX_VISIBLE_RECORDS = 300
MAX_CACHE_ENTRIES = 256
FAILURE_GENERATION_MODE = "RUNTIME_FAILURE_BOUNDARY"
FAILURE_LIMITATIONS = (
    "The bounded graph question failed before an analytical result was produced; no evidence conclusion is available.",
    "Only the bounded player-visible projection was submitted; the source graph was not mutated.",
)


class GraphAnalyticsService:
    """Authorise bounded analysis against the current player-safe projection."""

    def __init__(
        self,
        rounds: RoundService,
        graph_provider: Callable[[str], dict[str, Any]],
        *,
        engine: GraphAnalyticsEngine | None = None,
        new_id: Callable[[], str] = lambda: str(uuid4()),
        economy: EconomyService | None = None,
        package_provider: Callable[[Any], Any] | None = None,
    ) -> None:
        self._rounds = rounds
        self._graph_provider = graph_provider
        self._engine = engine or GraphAnalyticsEngine()
        self._new_id = new_id
        self._economy = economy
        self._package_provider = package_provider
        self._cache: dict[str, GraphAnalysisResult] = {}
        self._cache_order: list[str] = []
        self._history: dict[str, list[GraphAnalysisResult]] = {}
        self._lock = RLock()

    @instrumented("domain.graph-analytics.analyze")
    def analyze(self, round_id: str, request: dict[str, Any]) -> GraphAnalysisResult:
        round_ = self._require_active_case(round_id)
        algorithm = str(request.get("algorithm", "")).upper()
        if algorithm not in GRAPH_ANALYTICS_ALGORITHMS:
            raise InvalidRequestError(
                code="UNSUPPORTED_GRAPH_ANALYSIS",
                title="Graph action is not available",
                detail=f"'{algorithm or 'empty'}' is not one of the bounded graph actions.",
                recovery="Choose neighbourhood, path, component, centrality, motif or circular-flow analysis.",
            )
        normalised_request = self._normalise_request(request)
        scope_for_identity = sorted({str(value) for value in request.get("visible_record_ids", ())})
        identity_material = {"parameters": normalised_request, "visible_record_ids": scope_for_identity}
        idempotency_key = str(request.get("idempotency_key") or "legacy-" + hashlib.sha256(json.dumps(identity_material, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()[:40])
        request_hash = EconomyService.request_hash({"action": "RUN_GRAPH_ANALYSIS", **identity_material})
        if self._economy is not None:
            result, _ = self._economy.execute(
                round_id,
                "RUN_GRAPH_ANALYSIS",
                idempotency_key,
                request_hash,
                lambda: self._analyze_uncached(round_id, request, round_, algorithm, normalised_request),
                serialize=self._serialize_result,
                deserialize=self._deserialize_result,
                refund_if=lambda value: value.status == "FAILED",
            )
            return replace(result, cached=not _ and result.status == "COMPLETED") if not _ else result
        return self._analyze_uncached(round_id, request, round_, algorithm, normalised_request)

    def _analyze_uncached(self, round_id: str, request: dict[str, Any], round_: Any, algorithm: str, normalised_request: dict[str, Any]) -> GraphAnalysisResult:
        graph = self._graph_provider(round_id)
        scoped_graph, visible_ids, visible_edge_ids = self._authorise_scope(graph, request.get("visible_record_ids", ()))
        self._validate_subjects(algorithm, request, visible_ids)
        snapshot_version = str(graph.get("snapshot_version", f"case:{round_.case_version}"))
        projection_version = str(graph.get("projection_version", "unknown"))
        cache_key = self._cache_key(
            round_id=round_id,
            case_version=round_.case_version,
            snapshot_version=snapshot_version,
            projection_version=projection_version,
            visible_ids=visible_ids,
            visible_edge_ids=visible_edge_ids,
            request=normalised_request,
        )
        with self._lock:
            cached = self._cache.get(cache_key)
            if cached is not None:
                return replace(cached, cached=True)
            started = perf_counter()
            try:
                payload = self._engine.analyze(scoped_graph, normalised_request)
                execution_millis = max(0, round((perf_counter() - started) * 1000))
            except ValueError as error:
                raise InvalidRequestError(
                    code="INVALID_GRAPH_ANALYSIS",
                    title="The graph action needs different parameters",
                    detail=str(error),
                    recovery="Keep the input bounded and choose visible records and supported parameters.",
                ) from error
            except Exception:
                # A provider/runtime failure must remain a visible boundary, not
                # be rewritten as an empty analytical answer. Do not cache it:
                # a transient provider failure should be retryable, while the
                # history still records that the question was attempted.
                failure = GraphAnalysisResult(
                    analysis_id=self._new_id(),
                    round_id=round_id,
                    algorithm=algorithm,
                    status="FAILED",
                    result_type="EXECUTION_FAILURE",
                    parameters=normalised_request,
                    snapshot_version=snapshot_version,
                    projection_version=projection_version,
                    graph_engine=GRAPH_ENGINE,
                    framework_semantics=FRAMEWORK_SEMANTICS,
                    generation_mode=FAILURE_GENERATION_MODE,
                    actual_engine_run=False,
                    input_node_count=len(scoped_graph["nodes"]),
                    input_edge_count=len(scoped_graph["edges"]),
                    nodes=(),
                    edges=(),
                    paths=(),
                    components=(),
                    ranked_leads=(),
                    motifs=(),
                    supporting_relationship_ids=(),
                    partial=False,
                    omitted_result_count=0,
                    interpretation=(
                        "The graph question could not produce an analytical result. "
                        "No identity, control or fraud conclusion follows from this failure."
                    ),
                    limitations=FAILURE_LIMITATIONS,
                    cache_key=cache_key,
                    execution_millis=max(0, round((perf_counter() - started) * 1000)),
                )
                self._history.setdefault(round_id, []).append(failure)
                return failure
            result = GraphAnalysisResult(
                analysis_id=self._new_id(),
                round_id=round_id,
                algorithm=algorithm,
                status="COMPLETED",
                result_type=str(payload["result_type"]),
                parameters=normalised_request,
                snapshot_version=snapshot_version,
                projection_version=projection_version,
                graph_engine=str(payload["graph_engine"]),
                framework_semantics=str(payload["framework_semantics"]),
                generation_mode=str(payload["generation_mode"]),
                actual_engine_run=bool(payload["actual_engine_run"]),
                input_node_count=len(scoped_graph["nodes"]),
                input_edge_count=len(scoped_graph["edges"]),
                nodes=tuple(payload["nodes"]),
                edges=tuple(payload["edges"]),
                paths=tuple(payload["paths"]),
                components=tuple(payload["components"]),
                ranked_leads=tuple(payload["ranked_leads"]),
                motifs=tuple(payload["motifs"]),
                supporting_relationship_ids=tuple(payload["supporting_relationship_ids"]),
                partial=bool(payload["partial"]),
                omitted_result_count=int(payload["omitted_result_count"]),
                interpretation=str(payload["interpretation"]),
                limitations=tuple(payload["limitations"]),
                cache_key=cache_key,
                execution_millis=execution_millis,
            )
            self._cache[cache_key] = result
            self._cache_order.append(cache_key)
            self._history.setdefault(round_id, []).append(result)
            while len(self._cache_order) > MAX_CACHE_ENTRIES:
                oldest = self._cache_order.pop(0)
                self._cache.pop(oldest, None)
            return result

    @staticmethod
    def _serialize_result(result: GraphAnalysisResult) -> str:
        return json.dumps({"analysis_id": result.analysis_id, **{key: value for key, value in result.__dict__.items()}} if hasattr(result, "__dict__") else {
            "analysis_id": result.analysis_id,
            "round_id": result.round_id,
            "algorithm": result.algorithm,
            "status": result.status,
            "result_type": result.result_type,
            "parameters": result.parameters,
            "snapshot_version": result.snapshot_version,
            "projection_version": result.projection_version,
            "graph_engine": result.graph_engine,
            "framework_semantics": result.framework_semantics,
            "generation_mode": result.generation_mode,
            "actual_engine_run": result.actual_engine_run,
            "input_node_count": result.input_node_count,
            "input_edge_count": result.input_edge_count,
            "nodes": result.nodes,
            "edges": result.edges,
            "paths": result.paths,
            "components": result.components,
            "ranked_leads": result.ranked_leads,
            "motifs": result.motifs,
            "supporting_relationship_ids": result.supporting_relationship_ids,
            "partial": result.partial,
            "omitted_result_count": result.omitted_result_count,
            "interpretation": result.interpretation,
            "limitations": result.limitations,
            "cache_key": result.cache_key,
            "cached": False,
            "execution_millis": result.execution_millis,
        }, sort_keys=True, separators=(",", ":"))

    @staticmethod
    def _deserialize_result(payload: str) -> GraphAnalysisResult:
        raw = json.loads(payload)
        for key in ("nodes", "edges", "paths", "components", "ranked_leads", "motifs", "supporting_relationship_ids", "limitations"):
            raw[key] = tuple(raw.get(key, ()))
        return replace(GraphAnalysisResult(**raw), cached=True)

    def history(self, round_id: str) -> tuple[GraphAnalysisResult, ...]:
        self._rounds.require(round_id)
        with self._lock:
            return tuple(self._history.get(round_id, ()))

    @staticmethod
    def _authorise_scope(graph: dict[str, Any], requested_ids: Any) -> tuple[dict[str, Any], tuple[str, ...], tuple[str, ...]]:
        def field(item: Any, key: str, default: Any = "") -> Any:
            if isinstance(item, dict):
                return item.get(key, default)
            return getattr(item, key, default)

        all_nodes = tuple(graph.get("nodes", ()))
        all_edges = tuple(graph.get("edges", ()))
        by_id = {str(field(node, "record_id")): node for node in all_nodes}
        if requested_ids:
            if not isinstance(requested_ids, (list, tuple)) or len(requested_ids) > MAX_VISIBLE_RECORDS:
                raise InvalidRequestError(
                    code="GRAPH_SCOPE_TOO_LARGE",
                    title="The analytical view is too large",
                    detail=f"Graph analysis accepts at most {MAX_VISIBLE_RECORDS} visible record IDs.",
                    recovery="Reduce the visible graph before running the analysis.",
                )
            visible_ids = tuple(sorted({str(value) for value in requested_ids}))
            unknown = sorted(set(visible_ids) - set(by_id))
            if unknown:
                raise NotFoundError(
                    code="GRAPH_SCOPE_NOT_AVAILABLE",
                    title="A visible record is unavailable",
                    detail=f"The analytical scope references records outside the published projection: {', '.join(unknown[:5])}.",
                )
        else:
            visible_ids = tuple(sorted(by_id))
        visible_set = set(visible_ids)
        visible_edges = tuple(
            edge
            for edge in all_edges
            if str(field(edge, "source_record_id")) in visible_set
            and str(field(edge, "target_record_id")) in visible_set
        )
        visible_edge_ids = tuple(sorted(str(field(edge, "relationship_id")) for edge in visible_edges))
        scoped = {
            "projection_version": graph.get("projection_version", "unknown"),
            "snapshot_version": graph.get("snapshot_version", "unknown"),
            "nodes": tuple(by_id[identifier] for identifier in visible_ids),
            "edges": visible_edges,
        }
        return scoped, visible_ids, visible_edge_ids

    @staticmethod
    def _validate_subjects(algorithm: str, request: dict[str, Any], visible_ids: tuple[str, ...]) -> None:
        available = set(visible_ids)
        required: tuple[str, ...]
        if algorithm == "NEIGHBOURHOOD":
            required = ("seed_record_id",)
        elif algorithm == "SHORTEST_PATH":
            required = ("source_record_id", "target_record_id")
        else:
            required = ()
        for field in required:
            value = str(request.get(field) or "")
            if value not in available:
                raise InvalidRequestError(
                    code="GRAPH_SUBJECT_NOT_VISIBLE",
                    title="The selected graph subject is unavailable",
                    detail=f"{field} must reference a record in the current player-visible projection.",
                    recovery="Select a visible record and try again.",
                )

    @staticmethod
    def _normalise_request(request: dict[str, Any]) -> dict[str, Any]:
        allowed = {
            "algorithm",
            "seed_record_id",
            "source_record_id",
            "target_record_id",
            "max_hops",
            "max_path_length",
            "result_limit",
            "directed",
            "centrality_metric",
            "relationship_families",
            "relationship_types",
            "time_from",
            "time_to",
        }
        normalised: dict[str, Any] = {}
        for key in sorted(allowed):
            if key not in request:
                continue
            value = request[key]
            if isinstance(value, list):
                normalised[key] = sorted({str(item) for item in value})
            elif key == "algorithm":
                normalised[key] = str(value).upper()
            else:
                normalised[key] = value
        normalised.setdefault("result_limit", 10)
        normalised.setdefault("directed", True)
        return normalised

    @staticmethod
    def _cache_key(
        *,
        round_id: str,
        case_version: str,
        snapshot_version: str,
        projection_version: str,
        visible_ids: tuple[str, ...],
        visible_edge_ids: tuple[str, ...],
        request: dict[str, Any],
    ) -> str:
        material = {
            "implementation_version": GRAPH_ANALYTICS_VERSION,
            "round_id": round_id,
            "case_version": case_version,
            "snapshot_version": snapshot_version,
            "projection_version": projection_version,
            "visible_record_ids": visible_ids,
            "visible_relationship_ids": visible_edge_ids,
            "request": request,
        }
        return "fga10:" + hashlib.sha256(json.dumps(material, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()

    def _require_active_round(self, round_id: str) -> Any:
        round_ = self._rounds.require(round_id)
        if round_.status != RoundStatus.ACTIVE:
            raise ConflictError(
                code="ROUND_NOT_ACTIVE",
                title="Investigation is not active",
                detail="Graph analytics can only run in an active round.",
                recovery="Open the case board and retry the bounded analysis.",
            )
        package = self._package_provider(round_) if self._package_provider is not None else None
        if package is not None and not package.supports("RUN_GRAPH_ANALYSIS"):
            raise ConflictError(
                code="ACTION_NOT_AVAILABLE",
                title="Graph analysis is unavailable",
                detail="This case package does not declare graph analysis.",
                recovery="Choose one of the actions declared by the active case package.",
            )
        return round_

    def _require_active_case(self, round_id: str) -> Any:
        return self._require_active_round(round_id)
