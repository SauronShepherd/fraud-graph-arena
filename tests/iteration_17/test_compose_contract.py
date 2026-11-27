from pathlib import Path

import yaml

from scripts.fga17_compose_contract import validate


ROOT = Path(__file__).resolve().parents[2]


def test_compose_contract_is_complete() -> None:
    assert validate(ROOT) == []


def test_local_workflow_is_a_build_and_published_workflow_is_an_image() -> None:
    local = yaml.safe_load((ROOT / "compose.yaml").read_text(encoding="utf-8"))
    published = yaml.safe_load((ROOT / "compose.published.yaml").read_text(encoding="utf-8"))
    assert local["services"]["web"]["profiles"] == ["local-build"]
    assert local["services"]["web"]["build"]["context"] == "."
    assert "build" not in published["services"]["web-published"]
    assert published["services"]["web-published"]["profiles"] == ["published-image"]
    assert "${FGA_IMAGE:?" in (ROOT / "compose.published.yaml").read_text(encoding="utf-8")


def test_health_checks_name_the_boundary_they_can_prove() -> None:
    compose = yaml.safe_load((ROOT / "compose.yaml").read_text(encoding="utf-8"))
    web_health = str(compose["services"]["web"]["healthcheck"]["test"])
    postgres_health = str(compose["services"]["postgres"]["healthcheck"]["test"])
    assert "/api/v1/health/ready" in web_health
    assert "pg_isready" in postgres_health
    assert "depends_on" not in compose["services"]["web"]
