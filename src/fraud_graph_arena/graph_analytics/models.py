from __future__ import annotations

from dataclasses import dataclass
from typing import Any


GRAPH_ANALYTICS_ALGORITHMS: tuple[str, ...] = (
    "NEIGHBOURHOOD",
    "SHORTEST_PATH",
    "CONNECTED_COMPONENTS",
    "CENTRALITY",
    "MOTIF",
    "CIRCULAR_FLOW",
)


@dataclass(frozen=True, slots=True)
class GraphAnalysisResult:
    analysis_id: str
    round_id: str
    algorithm: str
    status: str
    result_type: str
    parameters: dict[str, Any]
    snapshot_version: str
    projection_version: str
    graph_engine: str
    framework_semantics: str
    generation_mode: str
    actual_engine_run: bool
    input_node_count: int
    input_edge_count: int
    nodes: tuple[dict[str, Any], ...]
    edges: tuple[dict[str, Any], ...]
    paths: tuple[dict[str, Any], ...]
    components: tuple[dict[str, Any], ...]
    ranked_leads: tuple[dict[str, Any], ...]
    motifs: tuple[dict[str, Any], ...]
    supporting_relationship_ids: tuple[str, ...]
    partial: bool
    omitted_result_count: int
    interpretation: str
    limitations: tuple[str, ...]
    cache_key: str
    cached: bool = False
    execution_millis: int = 0
