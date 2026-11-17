"""Produce the offline, non-player FGA-09 evaluation receipt."""

from __future__ import annotations

from datetime import UTC, datetime
import argparse
import json
from pathlib import Path

from fraud_graph_arena.entity_resolution.evaluation import evaluate_t02, metrics_to_dict


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, default=Path("reports/iteration-09/entity-resolution-evaluation.json"))
    args = parser.parse_args()
    report = metrics_to_dict(evaluate_t02())
    report["run_at_utc"] = datetime.now(UTC).isoformat()
    report["player_safe"] = False
    rendered = json.dumps(report, indent=2) + "\n"
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if report["regression_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
