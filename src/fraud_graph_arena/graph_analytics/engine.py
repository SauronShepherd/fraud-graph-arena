from __future__ import annotations

from collections import defaultdict, deque
from hashlib import sha256
import math
from typing import Any, Iterable

from .models import GRAPH_ANALYTICS_ALGORITHMS


GRAPH_ANALYTICS_VERSION = "fga10-graph-analytics-v1"
GRAPH_ENGINE = "FGA_GRAPH_ANALYTICS_ADAPTER"
GENERATION_MODE = "RUNTIME_DETERMINISTIC_FALLBACK"
FRAMEWORK_SEMANTICS = "GRAPHFRAMES_STYLE_ALGORITHM_CONTRACT"
MAX_RESULT_ITEMS = 20
MAX_PATH_LENGTH = 6
MAX_HOPS = 3

_STRUCTURAL_LIMITATION = (
    "Structural importance is a lead, not identity, control, culpability or a fraud verdict."
)
_COMMON_LIMITATIONS = (
    _STRUCTURAL_LIMITATION,
    "Only the bounded player-visible projection and its supporting relationships are analysed.",
    "A no-result answer means no qualifying structure met these parameters; it does not prove absence.",
)


def _value(item: Any, key: str, default: Any = "") -> Any:
    if isinstance(item, dict):
        return item.get(key, default)
    return getattr(item, key, default)


def _node_id(node: Any) -> str:
    return str(_value(node, "record_id"))


def _edge_id(edge: Any) -> str:
    return str(_value(edge, "relationship_id"))


def _node_payload(node: Any) -> dict[str, Any]:
    return {
        "record_id": _node_id(node),
        "record_type": str(_value(node, "record_type")),
        "label": str(_value(node, "label")),
        "safe_summary": str(_value(node, "safe_summary")),
        "record_subtype": str(_value(node, "record_subtype")),
        "source_system_id": str(_value(node, "source_system_id")),
        "provenance_ref": str(_value(node, "provenance_ref")),
    }


def _edge_payload(edge: Any) -> dict[str, Any]:
    return {
        "relationship_id": _edge_id(edge),
        "source_record_id": str(_value(edge, "source_record_id")),
        "target_record_id": str(_value(edge, "target_record_id")),
        "relationship_family": str(_value(edge, "relationship_family")),
        "relationship_type": str(_value(edge, "relationship_type")),
        "directed": bool(_value(edge, "directed")),
        "provenance": str(_value(edge, "provenance")),
        "player_safe_summary": str(_value(edge, "player_safe_summary")),
        "event_time": str(_value(edge, "event_time")),
    }


def _stable_component_id(record_ids: Iterable[str]) -> str:
    joined = "|".join(sorted(record_ids))
    return f"COMP-{sha256(joined.encode('utf-8')).hexdigest()[:12].upper()}"


class GraphAnalyticsEngine:
    """Run deterministic bounded algorithms behind the FGA-owned adapter.

    The implementation deliberately uses ordinary Python structures for the local
    and SQL-Warehouse-compatible fallback. A future GraphFrames provider can satisfy
    the same result contract without leaking DataFrames into the game boundary.
    """

    def analyze(self, graph: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
        algorithm = str(request.get("algorithm", "")).upper()
        if algorithm not in GRAPH_ANALYTICS_ALGORITHMS:
            raise ValueError(f"unsupported graph analysis algorithm: {algorithm}")
        nodes, edges = self._validate_graph(graph)
        families = self._normalise_strings(request.get("relationship_families", ()))
        relationship_types = self._normalise_strings(request.get("relationship_types", ()))
        filtered_edges = self._filter_edges(
            edges,
            families=families,
            relationship_types=relationship_types,
            time_from=request.get("time_from"),
            time_to=request.get("time_to"),
        )
        directed = bool(request.get("directed", True))
        result_limit = self._bounded_int(request.get("result_limit", 10), 1, MAX_RESULT_ITEMS, "result_limit")
        max_hops = self._bounded_int(request.get("max_hops", 1), 1, MAX_HOPS, "max_hops")
        max_path_length = self._bounded_int(request.get("max_path_length", 4), 1, MAX_PATH_LENGTH, "max_path_length")

        if algorithm == "NEIGHBOURHOOD":
            return self._neighbourhood(nodes, filtered_edges, request, directed, max_hops, result_limit)
        if algorithm == "SHORTEST_PATH":
            return self._shortest_paths(nodes, filtered_edges, request, directed, max_path_length, result_limit)
        if algorithm == "CONNECTED_COMPONENTS":
            return self._components(nodes, filtered_edges, directed, result_limit)
        if algorithm == "CENTRALITY":
            return self._centrality(nodes, filtered_edges, request, directed, result_limit)
        if algorithm == "MOTIF":
            return self._motifs(nodes, filtered_edges, request, directed, max_path_length, result_limit, "MOTIF_CANDIDATE")
        return self._motifs(nodes, filtered_edges, request, directed, max_path_length, result_limit, "CIRCULAR_FLOW")

    @staticmethod
    def _validate_graph(graph: dict[str, Any]) -> tuple[dict[str, Any], tuple[Any, ...]]:
        raw_nodes = tuple(graph.get("nodes", ()))
        raw_edges = tuple(graph.get("edges", ()))
        nodes: dict[str, Any] = {}
        for node in raw_nodes:
            identifier = _node_id(node)
            if not identifier:
                raise ValueError("graph node is missing record_id")
            if identifier in nodes:
                raise ValueError(f"graph contains duplicate node: {identifier}")
            nodes[identifier] = node
        edges: list[Any] = []
        edge_ids: set[str] = set()
        for edge in raw_edges:
            identifier = _edge_id(edge)
            source = str(_value(edge, "source_record_id"))
            target = str(_value(edge, "target_record_id"))
            if not identifier or not source or not target:
                raise ValueError("graph edge is missing an identifier or endpoint")
            if identifier in edge_ids:
                raise ValueError(f"graph contains duplicate relationship: {identifier}")
            if source not in nodes or target not in nodes:
                raise ValueError(f"graph edge endpoint is not visible: {identifier}")
            edge_ids.add(identifier)
            edges.append(edge)
        return nodes, tuple(sorted(edges, key=_edge_id))

    @staticmethod
    def _normalise_strings(values: Any) -> tuple[str, ...]:
        if values is None:
            return ()
        if isinstance(values, str):
            values = (values,)
        return tuple(sorted({str(value).strip() for value in values if str(value).strip()}))

    @staticmethod
    def _bounded_int(value: Any, minimum: int, maximum: int, label: str) -> int:
        try:
            integer = int(value)
        except (TypeError, ValueError) as error:
            raise ValueError(f"{label} must be an integer") from error
        if not minimum <= integer <= maximum:
            raise ValueError(f"{label} must be between {minimum} and {maximum}")
        return integer

    @classmethod
    def _filter_edges(
        cls,
        edges: Iterable[Any],
        *,
        families: tuple[str, ...],
        relationship_types: tuple[str, ...],
        time_from: Any,
        time_to: Any,
    ) -> tuple[Any, ...]:
        selected: list[Any] = []
        for edge in edges:
            family = str(_value(edge, "relationship_family"))
            relationship_type = str(_value(edge, "relationship_type"))
            event_time = str(_value(edge, "event_time"))
            if families and family not in families:
                continue
            if relationship_types and relationship_type not in relationship_types:
                continue
            if time_from is not None and (not event_time or event_time < str(time_from)):
                continue
            if time_to is not None and (not event_time or event_time > str(time_to)):
                continue
            selected.append(edge)
        return tuple(sorted(selected, key=_edge_id))

    @staticmethod
    def _adjacency(nodes: dict[str, Any], edges: Iterable[Any], directed: bool) -> dict[str, list[tuple[str, Any]]]:
        adjacency: dict[str, list[tuple[str, Any]]] = defaultdict(list)
        for edge in edges:
            source = str(_value(edge, "source_record_id"))
            target = str(_value(edge, "target_record_id"))
            adjacency[source].append((target, edge))
            if not directed:
                adjacency[target].append((source, edge))
        for identifier in nodes:
            adjacency[identifier].sort(key=lambda item: (item[0], _edge_id(item[1])))
        return adjacency

    @staticmethod
    def _edge_lookup(edges: Iterable[Any]) -> dict[str, Any]:
        return {_edge_id(edge): edge for edge in edges}

    def _neighbourhood(
        self,
        nodes: dict[str, Any],
        edges: tuple[Any, ...],
        request: dict[str, Any],
        directed: bool,
        max_hops: int,
        result_limit: int,
    ) -> dict[str, Any]:
        seed = str(request.get("seed_record_id") or "")
        if seed not in nodes:
            raise ValueError("seed_record_id must reference a visible node")
        adjacency = self._adjacency(nodes, edges, directed)
        distance = {seed: 0}
        queue: deque[str] = deque([seed])
        while queue:
            current = queue.popleft()
            if distance[current] >= max_hops:
                continue
            for neighbour, _ in adjacency[current]:
                if neighbour not in distance:
                    distance[neighbour] = distance[current] + 1
                    queue.append(neighbour)
        ordered_ids = sorted(distance, key=lambda identifier: (distance[identifier], identifier))
        visible_ids = ordered_ids[:result_limit]
        visible_set = set(visible_ids)
        selected_edges = tuple(edge for edge in edges if str(_value(edge, "source_record_id")) in visible_set and str(_value(edge, "target_record_id")) in visible_set)
        omitted = max(0, len(ordered_ids) - len(visible_ids))
        return self._payload(
            result_type="NEIGHBOURHOOD_FOUND" if len(visible_ids) > 1 else "NO_QUALIFYING_STRUCTURE",
            nodes=tuple(_node_payload(nodes[identifier]) for identifier in visible_ids),
            edges=tuple(_edge_payload(edge) for edge in selected_edges),
            supporting_relationship_ids=tuple(_edge_id(edge) for edge in selected_edges),
            partial=omitted > 0,
            omitted_result_count=omitted,
            interpretation=f"The bounded neighbourhood contains {len(visible_ids)} visible node(s) from {seed} within {max_hops} hop(s).",
        )

    def _shortest_paths(
        self,
        nodes: dict[str, Any],
        edges: tuple[Any, ...],
        request: dict[str, Any],
        directed: bool,
        max_path_length: int,
        result_limit: int,
    ) -> dict[str, Any]:
        source = str(request.get("source_record_id") or "")
        target = str(request.get("target_record_id") or "")
        if source not in nodes or target not in nodes:
            raise ValueError("source_record_id and target_record_id must reference visible nodes")
        if source == target:
            raise ValueError("source_record_id and target_record_id must be different")
        adjacency = self._adjacency(nodes, edges, directed)
        queue: deque[tuple[str, tuple[str, ...], tuple[str, ...]]] = deque([(source, (source,), ())])
        found_distance: int | None = None
        paths: list[tuple[tuple[str, ...], tuple[str, ...]]] = []
        path_count = 0
        while queue:
            current, path_nodes, path_edges = queue.popleft()
            depth = len(path_edges)
            if found_distance is not None and depth >= found_distance:
                continue
            if depth >= max_path_length:
                continue
            for neighbour, edge in adjacency[current]:
                if neighbour in path_nodes:
                    continue
                next_nodes = path_nodes + (neighbour,)
                next_edges = path_edges + (_edge_id(edge),)
                if neighbour == target:
                    found_distance = depth + 1 if found_distance is None else found_distance
                    if len(next_edges) == found_distance:
                        path_count += 1
                        if len(paths) < result_limit:
                            paths.append((next_nodes, next_edges))
                elif found_distance is None or depth + 1 < found_distance:
                    queue.append((neighbour, next_nodes, next_edges))
        paths.sort(key=lambda item: (len(item[1]), item[0], item[1]))
        selected_paths = paths[:result_limit]
        edge_lookup = self._edge_lookup(edges)
        node_ids = sorted({identifier for path, _ in selected_paths for identifier in path})
        edge_ids = sorted({edge_id for _, path_edges in selected_paths for edge_id in path_edges})
        return self._payload(
            result_type="PATH_FOUND" if selected_paths else "NO_QUALIFYING_STRUCTURE",
            nodes=tuple(_node_payload(nodes[identifier]) for identifier in node_ids),
            edges=tuple(_edge_payload(edge_lookup[identifier]) for identifier in edge_ids),
            paths=tuple({"record_ids": list(path), "relationship_ids": list(path_edges), "length": len(path_edges)} for path, path_edges in selected_paths),
            supporting_relationship_ids=tuple(edge_ids),
            partial=path_count > result_limit,
            omitted_result_count=max(0, path_count - result_limit),
            interpretation="A shortest path is a route under these direction, family, time and length constraints; it is not a causal explanation.",
        )

    def _components(
        self,
        nodes: dict[str, Any],
        edges: tuple[Any, ...],
        directed: bool,
        result_limit: int,
    ) -> dict[str, Any]:
        adjacency = self._adjacency(nodes, edges, directed=False)
        components: list[tuple[str, ...]] = []
        unseen = set(nodes)
        while unseen:
            start = min(unseen)
            queue = deque([start])
            unseen.remove(start)
            members: list[str] = []
            while queue:
                current = queue.popleft()
                members.append(current)
                for neighbour, _ in adjacency[current]:
                    if neighbour in unseen:
                        unseen.remove(neighbour)
                        queue.append(neighbour)
            components.append(tuple(sorted(members)))
        components.sort(key=lambda member: (-len(member), member))
        selected = components[:result_limit]
        selected_set = set(identifier for component in selected for identifier in component)
        selected_edges = tuple(edge for edge in edges if str(_value(edge, "source_record_id")) in selected_set and str(_value(edge, "target_record_id")) in selected_set)
        component_payload = tuple(
            {
                "component_id": _stable_component_id(component),
                "record_ids": list(component),
                "node_count": len(component),
                "edge_count": sum(1 for edge in selected_edges if str(_value(edge, "source_record_id")) in component and str(_value(edge, "target_record_id")) in component),
            }
            for component in selected
        )
        return self._payload(
            result_type="COMPONENT" if selected else "NO_QUALIFYING_STRUCTURE",
            nodes=tuple(_node_payload(nodes[identifier]) for identifier in sorted(selected_set)),
            edges=tuple(_edge_payload(edge) for edge in selected_edges),
            components=component_payload,
            supporting_relationship_ids=tuple(_edge_id(edge) for edge in selected_edges),
            partial=len(components) > len(selected),
            omitted_result_count=max(0, len(components) - len(selected)),
            interpretation="A connected component is structural grouping. It does not establish common control, identity or wrongdoing.",
        )

    def _centrality(
        self,
        nodes: dict[str, Any],
        edges: tuple[Any, ...],
        request: dict[str, Any],
        directed: bool,
        result_limit: int,
    ) -> dict[str, Any]:
        metric = str(request.get("centrality_metric", "degree")).lower()
        if metric not in {"degree", "pagerank", "betweenness"}:
            raise ValueError("centrality_metric must be degree, pagerank or betweenness")
        adjacency = self._adjacency(nodes, edges, directed)
        scores: dict[str, float]
        if metric == "degree":
            scores = {identifier: float(len(adjacency[identifier])) for identifier in nodes}
        elif metric == "pagerank":
            scores = self._pagerank(nodes, adjacency)
        else:
            scores = self._betweenness(nodes, adjacency)
        edge_ids_by_node: dict[str, set[str]] = defaultdict(set)
        for edge in edges:
            edge_ids_by_node[str(_value(edge, "source_record_id"))].add(_edge_id(edge))
            edge_ids_by_node[str(_value(edge, "target_record_id"))].add(_edge_id(edge))
        # A rank without a supporting relationship is not an actionable lead in
        # the player-safe workspace. Keep isolated nodes in component analysis,
        # but do not dress them up as centrality evidence.
        actionable = [identifier for identifier in nodes if edge_ids_by_node[identifier]]
        ordered = sorted(actionable, key=lambda identifier: (-scores[identifier], identifier))
        selected = ordered[:result_limit]
        leads = tuple(
            {
                "rank": index,
                "record_id": identifier,
                "metric": metric,
                "score": round(scores[identifier], 6),
                "supporting_relationship_ids": sorted(edge_ids_by_node[identifier]),
            }
            for index, identifier in enumerate(selected, start=1)
        )
        selected_edge_ids = sorted({edge_id for lead in leads for edge_id in lead["supporting_relationship_ids"]})
        edge_lookup = self._edge_lookup(edges)
        return self._payload(
            result_type="RANKED_LEAD" if leads else "NO_QUALIFYING_STRUCTURE",
            nodes=tuple(_node_payload(nodes[identifier]) for identifier in selected),
            edges=tuple(_edge_payload(edge_lookup[identifier]) for identifier in selected_edge_ids),
            ranked_leads=leads,
            supporting_relationship_ids=tuple(selected_edge_ids),
            partial=len(ordered) > len(selected),
            omitted_result_count=max(0, len(ordered) - len(selected)),
            interpretation=f"{metric} ranks structural position in this bounded graph. A high rank can identify a bank, platform or auditor; it is not a conviction.",
        )

    @staticmethod
    def _pagerank(nodes: dict[str, Any], adjacency: dict[str, list[tuple[str, Any]]]) -> dict[str, float]:
        identifiers = sorted(nodes)
        if not identifiers:
            return {}
        damping = 0.85
        scores = {identifier: 1.0 / len(identifiers) for identifier in identifiers}
        for _ in range(24):
            next_scores = {identifier: (1.0 - damping) / len(identifiers) for identifier in identifiers}
            dangling = sum(scores[identifier] for identifier in identifiers if not adjacency[identifier])
            for identifier in identifiers:
                next_scores[identifier] += damping * dangling / len(identifiers)
            for source in identifiers:
                neighbours = sorted({neighbour for neighbour, _ in adjacency[source]})
                if not neighbours:
                    continue
                share = damping * scores[source] / len(neighbours)
                for neighbour in neighbours:
                    next_scores[neighbour] += share
            scores = next_scores
        return scores

    @staticmethod
    def _betweenness(nodes: dict[str, Any], adjacency: dict[str, list[tuple[str, Any]]]) -> dict[str, float]:
        scores = {identifier: 0.0 for identifier in nodes}
        for source in sorted(nodes):
            stack: list[str] = []
            predecessors: dict[str, list[str]] = {identifier: [] for identifier in nodes}
            sigma = {identifier: 0.0 for identifier in nodes}
            distance = {identifier: -1 for identifier in nodes}
            sigma[source] = 1.0
            distance[source] = 0
            queue: deque[str] = deque([source])
            while queue:
                current = queue.popleft()
                stack.append(current)
                for neighbour, _ in adjacency[current]:
                    if distance[neighbour] < 0:
                        queue.append(neighbour)
                        distance[neighbour] = distance[current] + 1
                    if distance[neighbour] == distance[current] + 1:
                        sigma[neighbour] += sigma[current]
                        predecessors[neighbour].append(current)
            dependency = {identifier: 0.0 for identifier in nodes}
            while stack:
                current = stack.pop()
                for predecessor in predecessors[current]:
                    if sigma[current]:
                        dependency[predecessor] += (sigma[predecessor] / sigma[current]) * (1.0 + dependency[current])
                if current != source:
                    scores[current] += dependency[current]
        return scores

    def _motifs(
        self,
        nodes: dict[str, Any],
        edges: tuple[Any, ...],
        request: dict[str, Any],
        directed: bool,
        max_path_length: int,
        result_limit: int,
        result_type: str,
    ) -> dict[str, Any]:
        adjacency = self._adjacency(nodes, edges, directed)
        cycles: dict[tuple[str, ...], tuple[tuple[str, ...], tuple[str, ...]]] = {}
        edge_lookup = self._edge_lookup(edges)

        def canonical(record_ids: tuple[str, ...], relationship_ids: tuple[str, ...]) -> tuple[tuple[str, ...], tuple[str, ...]]:
            rotations = [
                (record_ids[index:] + record_ids[:index], relationship_ids[index:] + relationship_ids[:index])
                for index in range(len(record_ids))
            ]
            if not directed:
                reverse_nodes = tuple(reversed(record_ids))
                reverse_edges = tuple(reversed(relationship_ids))
                rotations.extend(
                    (reverse_nodes[index:] + reverse_nodes[:index], reverse_edges[index:] + reverse_edges[:index])
                    for index in range(len(reverse_nodes))
                )
            return min(rotations, key=lambda item: (item[0], item[1]))

        def visit(start: str, current: str, path_nodes: tuple[str, ...], path_edges: tuple[str, ...]) -> None:
            if len(path_edges) >= max_path_length:
                return
            for neighbour, edge in adjacency[current]:
                if neighbour == start and len(path_nodes) >= 3:
                    key = canonical(path_nodes, path_edges + (_edge_id(edge),))
                    cycles[key[0]] = key
                elif neighbour not in path_nodes and neighbour >= start:
                    visit(start, neighbour, path_nodes + (neighbour,), path_edges + (_edge_id(edge),))

        for start in sorted(nodes):
            visit(start, start, (start,), ())

        ordered_cycles = sorted(cycles.values(), key=lambda item: (len(item[0]), item[0], item[1]))
        selected_cycles = ordered_cycles[:result_limit]
        selected_node_ids = sorted({identifier for record_ids, _ in selected_cycles for identifier in record_ids})
        selected_edge_ids = sorted({identifier for _, relationship_ids in selected_cycles for identifier in relationship_ids})
        motifs = []
        for record_ids, relationship_ids in selected_cycles:
            times = [str(_value(edge_lookup[identifier], "event_time")) for identifier in relationship_ids]
            present_times = [time for time in times if time]
            time_span = None
            if len(present_times) >= 2:
                time_span = present_times[-1] + " to " + present_times[0] if present_times[-1] != present_times[0] else present_times[0]
            motifs.append(
                {
                    "motif_type": "DIRECTED_CYCLE" if directed else "CYCLE",
                    "record_ids": list(record_ids),
                    "relationship_ids": list(relationship_ids),
                    "length": len(relationship_ids),
                    "event_times": times,
                    "time_span": time_span,
                    "chronology_observed": bool(present_times) and present_times == sorted(present_times),
                }
            )
        return self._payload(
            result_type=result_type if motifs else "NO_QUALIFYING_STRUCTURE",
            nodes=tuple(_node_payload(nodes[identifier]) for identifier in selected_node_ids),
            edges=tuple(_edge_payload(edge_lookup[identifier]) for identifier in selected_edge_ids),
            motifs=tuple(motifs),
            supporting_relationship_ids=tuple(selected_edge_ids),
            partial=len(ordered_cycles) > len(selected_cycles),
            omitted_result_count=max(0, len(ordered_cycles) - len(selected_cycles)),
            interpretation="A cycle or motif is a structure worth inspecting. It is not, by itself, proof that every participant shares control or intent.",
        )

    @staticmethod
    def _payload(
        *,
        result_type: str,
        nodes: tuple[dict[str, Any], ...] = (),
        edges: tuple[dict[str, Any], ...] = (),
        paths: tuple[dict[str, Any], ...] = (),
        components: tuple[dict[str, Any], ...] = (),
        ranked_leads: tuple[dict[str, Any], ...] = (),
        motifs: tuple[dict[str, Any], ...] = (),
        supporting_relationship_ids: tuple[str, ...] = (),
        partial: bool = False,
        omitted_result_count: int = 0,
        interpretation: str = "",
    ) -> dict[str, Any]:
        return {
            "result_type": "CAPPED_RESULT" if partial else result_type,
            "nodes": nodes,
            "edges": edges,
            "paths": paths,
            "components": components,
            "ranked_leads": ranked_leads,
            "motifs": motifs,
            "supporting_relationship_ids": tuple(sorted(set(supporting_relationship_ids))),
            "partial": partial,
            "omitted_result_count": omitted_result_count,
            "interpretation": interpretation,
            "limitations": _COMMON_LIMITATIONS,
            "generation_mode": GENERATION_MODE,
            "graph_engine": GRAPH_ENGINE,
            "framework_semantics": FRAMEWORK_SEMANTICS,
            "actual_engine_run": False,
        }
