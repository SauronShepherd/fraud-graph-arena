import pytest

from fraud_graph_arena.application import create_app
from fraud_graph_arena.config import RuntimeRole, Settings

@pytest.mark.parametrize("role", [RuntimeRole.MAINTENANCE, RuntimeRole.EVALUATOR, RuntimeRole.MIGRATE])
def test_non_web_roles_cannot_create_public_app(role: RuntimeRole) -> None:
    with pytest.raises(RuntimeError, match="only available for WEB"):
        create_app(Settings(environment="test", runtime_role=role, frontend_dist="missing"))
