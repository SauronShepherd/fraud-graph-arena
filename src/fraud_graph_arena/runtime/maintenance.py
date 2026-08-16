"""Maintenance-job composition root."""

from fraud_graph_arena.config import Settings


def run(settings: Settings | None = None) -> int:
    """Run maintenance work; currently a safe no-op until a job is scheduled."""
    _ = settings or Settings(runtime_role="MAINTENANCE")
    return 0
