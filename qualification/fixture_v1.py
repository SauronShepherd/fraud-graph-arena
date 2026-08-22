from __future__ import annotations

import hashlib
import json
from pathlib import Path

def build_fixture(node_count: int = 4, edge_count: int = 3) -> dict:
    nodes = [{"id": f"FIX-N-{i:04d}", "record_type": "PERSON_RECORD" if i % 3 == 0 else "ORGANIZATION_RECORD", "label": f"Fixture record {i:04d}", "x": 80 + (i % 8) * 120, "y": 80 + (i // 8) * 90} for i in range(node_count)]
    edges = [{"id": f"FIX-E-{i:04d}", "source_id": nodes[i % node_count]["id"], "target_id": nodes[(i * 7 + 3) % node_count]["id"], "relationship_family": "DIRECT_SOURCE", "relationship_type": "RELATED_TO", "directed": True} for i in range(edge_count)]
    return {"fixture_version": "1", "nodes": nodes, "edges": edges}

def write_fixture(path: Path) -> str:
    payload = json.dumps(build_fixture(), sort_keys=True, separators=(",", ":")) + "\n"
    path.write_text(payload, encoding="utf-8")
    return hashlib.sha256(payload.encode()).hexdigest()

if __name__ == "__main__":
    output = Path(__file__).with_name("fixture-v1.json")
    print(write_fixture(output))
