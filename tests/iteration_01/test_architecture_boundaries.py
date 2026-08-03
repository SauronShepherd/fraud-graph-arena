from __future__ import annotations

import ast
from pathlib import Path


SRC = Path(__file__).parents[2] / "src" / "fraud_graph_arena"
DOMAIN_FILES = [
    SRC / "catalogue" / "domain.py",
    SRC / "catalogue" / "ports.py",
    SRC / "narrative" / "domain.py",
    SRC / "narrative" / "ports.py",
    SRC / "rounds" / "domain.py",
    SRC / "rounds" / "ports.py",
    SRC / "analytics" / "ports.py",
]
FORBIDDEN_INFRASTRUCTURE_IMPORTS = {
    "fastapi",
    "pydantic",
    "pydantic_settings",
    "sqlite3",
    "uvicorn",
}


def imported_roots(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            roots.add(node.module.split(".")[0])
    return roots


def test_domain_and_ports_do_not_import_frameworks_or_database_drivers() -> None:
    failures: dict[str, set[str]] = {}
    for path in DOMAIN_FILES:
        forbidden = imported_roots(path) & FORBIDDEN_INFRASTRUCTURE_IMPORTS
        if forbidden:
            failures[str(path.relative_to(SRC))] = forbidden

    assert failures == {}


def test_frontend_does_not_define_canonical_path_ids_a_second_time() -> None:
    frontend = Path(__file__).parents[2] / "apps" / "web" / "src"
    canonical_literals = {
        "DETECTIVE_ACADEMY",
        "PUPPY",
        "ADULT_DOG",
        "SENIOR_DOG",
    }
    offenders: list[str] = []
    for path in frontend.rglob("*.tsx"):
        if "test" in path.relative_to(frontend).parts:
            continue
        text = path.read_text(encoding="utf-8")
        if sum(value in text for value in canonical_literals) >= 2:
            offenders.append(str(path.relative_to(frontend)))

    assert offenders == [], "Path IDs must come from the catalogue API, not UI constants"
