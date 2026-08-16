"""Database migration composition root."""

from fraud_graph_arena.config import Settings


def run(settings: Settings | None = None) -> int:
    _ = settings or Settings(runtime_role="MIGRATE")
    return 0
