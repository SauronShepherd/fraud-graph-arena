from __future__ import annotations

from fraud_graph_arena.application import create_app
from fraud_graph_arena.config import RuntimeRole, Settings

settings = Settings()
if settings.runtime_role == RuntimeRole.WEB:
    app = create_app(settings)
else:
    # Non-WEB roles intentionally do not expose an ASGI application. They are
    # selected by controlled job runners until their private capabilities exist.
    app = None

def main() -> int:
    if settings.runtime_role == RuntimeRole.WEB:
        raise SystemExit("WEB is an ASGI runtime; start fraud_graph_arena.runtime.main:app")
    raise SystemExit(f"Runtime role {settings.runtime_role.value} has no public web process")
