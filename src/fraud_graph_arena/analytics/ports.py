from __future__ import annotations

from typing import Any, Protocol, Sequence


class AnalyticsGateway(Protocol):
    """Reserved boundary for later graph/retrieval capabilities.

    Iteration 01 intentionally has no analytics implementation. Establishing the port
    now prevents future providers from owning game state or protected truth.
    """

    def capabilities(self) -> Sequence[str]: ...


class GraphAnalyticsGateway(Protocol):
    """FGA-owned graph-analysis boundary.

    Providers return domain results rather than Spark or GraphFrames DataFrames.
    That keeps an analytical engine replaceable and prevents it from owning game
    state, player visibility or protected truth.
    """

    def analyze(self, graph: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]: ...
