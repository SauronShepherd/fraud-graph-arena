"""Run the FGA-14 publication and adversarial safety review locally."""

from __future__ import annotations

from datetime import UTC, datetime
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from fraud_graph_arena.case_packages import CasePackageRegistry  # noqa: E402
from fraud_graph_arena.ethics.review import review_all_packages, validate_adversarial_cases  # noqa: E402


def main() -> int:
    reports = review_all_packages()
    fixture_errors = validate_adversarial_cases()
    published = CasePackageRegistry().published()
    payload = {
        "status": "pass" if not fixture_errors and all(item.status == "PASS" for item in reports) else "fail",
        "iteration": "FGA14",
        "review_version": reports[0].version if reports else "fga14-publication-review-v1",
        "run_at_utc": datetime.now(UTC).isoformat(),
        "package_count": len(reports),
        "canonical_package_count": sum(item.kind == "canonical" for item in published),
        "noncanonical_published_packages": [item.package_id for item in published if item.kind != "canonical"],
        "adversarial_case_count": reports[0].adversarial_case_count if reports else 0,
        "fixture_errors": fixture_errors,
        "packages": [
            {
                "package_id": item.package_id,
                "status": item.status,
                "checks": [{"check_id": check.check_id, "status": check.status, "message": check.message} for check in item.checks],
            }
            for item in reports
        ],
    }
    rendered = json.dumps(payload, indent=2) + "\n"
    report_path = ROOT / "reports/iteration-14/fga14-ethics-review.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if payload["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
