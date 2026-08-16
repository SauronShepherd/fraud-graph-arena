from __future__ import annotations

import ast
from pathlib import Path


SRC = Path(__file__).parents[2] / "src" / "fraud_graph_arena"
DOMAIN_FILES = sorted((*SRC.rglob("domain.py"), *SRC.rglob("ports.py")))
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


def test_capability_modules_do_not_import_another_modules_private_adapters() -> None:
    offenders: list[str] = []
    for path in SRC.rglob("*.py"):
        relative = path.relative_to(SRC)
        owner = relative.parts[0]
        if owner in {"runtime", "application.py"}:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            module = node.module if isinstance(node, ast.ImportFrom) else None
            names = [alias.name for alias in node.names] if isinstance(node, ast.Import) else []
            candidates = ([module] if module else []) + names
            for imported in candidates:
                if imported.startswith("fraud_graph_arena.") and ".adapters" in imported:
                    imported_owner = imported.split(".")[1]
                    if imported_owner != owner:
                        offenders.append(f"{relative}: {imported}")
    assert offenders == []
