import json
from pathlib import Path

from fraud_graph_arena.application import create_app
from fraud_graph_arena.config import Settings

def test_committed_openapi_matches_application_contract():
    committed = json.loads((Path(__file__).parents[2] / "contracts/openapi-v1.json").read_text(encoding="utf-8"))
    generated = create_app(Settings(environment="test", round_repository="memory", frontend_dist="missing")).openapi()
    assert committed == generated
