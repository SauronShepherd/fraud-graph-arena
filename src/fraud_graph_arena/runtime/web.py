"""WEB composition root for the public ASGI process."""

from fraud_graph_arena.application import create_app
from fraud_graph_arena.config import Settings

app = create_app(Settings())
