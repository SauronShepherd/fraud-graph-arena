from fastapi.routing import APIRoute

from fraud_graph_arena.application import create_app
from fraud_graph_arena.config import Settings


def test_application_boots_and_registers_walking_skeleton_routes(test_settings: Settings) -> None:
    app = create_app(test_settings)
    paths = {
        route.path
        for route in app.routes
        if isinstance(route, APIRoute)
    }

    assert "/api/v1/health/live" in paths
    assert "/api/v1/catalogue/sections" in paths
    assert "/api/v1/catalogue/{section}" in paths
    assert "/api/v1/rounds" in paths
    assert "/api/v1/rounds/{round_id}/start" in paths
    assert "/api/v1/rounds/{round_id}/opening" in paths
    assert "/api/v1/rounds/{round_id}/opening/complete" in paths
    assert "/api/v1/rounds/{round_id}/workspace" in paths


def test_openapi_uses_versioned_public_contract(test_settings: Settings) -> None:
    app = create_app(test_settings)
    schema = app.openapi()

    assert schema["info"]["version"] == "0.1.0"
    assert all(path.startswith("/api/v1/") for path in schema["paths"])
