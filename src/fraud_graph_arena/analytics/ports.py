from __future__ import annotations

from typing import Protocol, Sequence


class AnalyticsGateway(Protocol):
    """Reserved boundary for later graph/retrieval capabilities.

    Iteration 01 intentionally has no analytics implementation. Establishing the port
    now prevents future providers from owning game state or protected truth.
    """

    def capabilities(self) -> Sequence[str]: ...
