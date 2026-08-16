"""Evaluator composition root, kept separate from the public web process."""

from fraud_graph_arena.config import Settings


def run(settings: Settings | None = None) -> int:
    _ = settings or Settings(runtime_role="EVALUATOR")
    return 0
