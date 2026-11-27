"""Validate the FGA-17 local container contract without starting services."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
SECRET_BUILD_PATTERN = re.compile(r"(?i)(secret|password|token|private[_-]?key)")


def _load(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.name} must contain a mapping")
    return value


def validate(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    compose_path = root / "compose.yaml"
    published_path = root / "compose.published.yaml"
    contract_path = root / "contracts/deployment/fga17-compose-contract.json"
    runtime_env = root / "docker/runtime.env"
    dockerignore = root / ".dockerignore"
    dockerfile = root / "Dockerfile"

    if not compose_path.is_file():
        return ["compose.yaml is missing"]
    if not published_path.is_file():
        errors.append("compose.published.yaml is missing")
    if not contract_path.is_file():
        errors.append("fga17-compose-contract.json is missing")
    if not runtime_env.is_file():
        errors.append("docker/runtime.env is missing")

    compose = _load(compose_path)
    services = compose.get("services", {})
    web = services.get("web", {})
    postgres = services.get("postgres", {})
    if "local-build" not in web.get("profiles", []):
        errors.append("web must be explicit about the local-build profile")
    if web.get("build", {}).get("context") != ".":
        errors.append("web must build from the repository root")
    if "FGA_LOCAL_IMAGE" not in str(web.get("image", "")):
        errors.append("web must expose a deterministic local image name")
    web_health = str(web.get("healthcheck", {}).get("test", ""))
    if "/api/v1/health/ready" not in web_health:
        errors.append("web healthcheck must call application readiness")
    if "./docker/runtime.env" not in web.get("env_file", []):
        errors.append("web must declare runtime env injection separately")
    postgres_health = str(postgres.get("healthcheck", {}).get("test", ""))
    if "pg_isready" not in postgres_health:
        errors.append("postgres healthcheck must use pg_isready")
    if "postgres" not in postgres.get("profiles", []):
        errors.append("postgres must be opt-in through its own profile")

    if published_path.is_file():
        published_text = published_path.read_text(encoding="utf-8")
        if "${FGA_IMAGE:?" not in published_text:
            errors.append("published workflow must fail fast when FGA_IMAGE is absent")
        published = _load(published_path)
        published_service = published.get("services", {}).get("web-published", {})
        if "build" in published_service:
            errors.append("published workflow must not build a different source tree")
        if "published-image" not in published_service.get("profiles", []):
            errors.append("published service must be explicit about its profile")

    dockerfile_text = dockerfile.read_text(encoding="utf-8") if dockerfile.is_file() else ""
    if "COPY contracts/ ./contracts/" not in dockerfile_text:
        errors.append("Dockerfile must copy contracts required by the runtime")
    if "COPY config/ ./config/" not in dockerfile_text:
        errors.append("Dockerfile must copy config required by the runtime")
    if "COPY case-data/ ./case-data/" not in dockerfile_text:
        errors.append("Dockerfile must copy case data required by the runtime")
    if "COPY case-packages/ ./case-packages/" not in dockerfile_text:
        errors.append("Dockerfile must copy case packages required by the runtime")
    for line in dockerfile_text.splitlines():
        if line.strip().upper().startswith("ARG ") and SECRET_BUILD_PATTERN.search(line):
            errors.append("Dockerfile must not accept a secret-like build argument")
    if re.search(r"(?im)^COPY\s+.*\.env", dockerfile_text):
        errors.append("Dockerfile must not copy environment files into image layers")

    ignored = dockerignore.read_text(encoding="utf-8") if dockerignore.is_file() else ""
    for required in ("!contracts/", "!config/", "!case-data/", "!case-packages/"):
        if required not in ignored:
            errors.append(f".dockerignore must re-include {required}")

    runtime_text = runtime_env.read_text(encoding="utf-8") if runtime_env.is_file() else ""
    for line in runtime_text.splitlines():
        if line and not line.lstrip().startswith("#") and SECRET_BUILD_PATTERN.search(line):
            errors.append("runtime.env must not contain secret-like variables in the repository")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    errors = validate(args.root.resolve())
    report = {"status": "pass" if not errors else "fail", "errors": errors}
    print(json.dumps(report, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
