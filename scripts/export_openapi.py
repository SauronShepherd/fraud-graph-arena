from __future__ import annotations

import json
from pathlib import Path

from fraud_graph_arena.application import create_app
from fraud_graph_arena.config import Settings


def main() -> None:
    destination = Path("contracts/openapi-v1.json")
    destination.parent.mkdir(parents=True, exist_ok=True)
    app = create_app(Settings(environment="test", round_repository="memory"))
    destination.write_text(
        json.dumps(app.openapi(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(destination)


if __name__ == "__main__":
    main()
