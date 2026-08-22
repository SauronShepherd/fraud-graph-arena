"""Rebuild the governed canonical corpus from approved source packages.

The command is intentionally fail-closed: the source root and output directory
are explicit, the output must be empty, and every family is resolved through
the closed converter registry.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from fraud_graph_arena.case_data.converters import registry


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def package_digest(package: Path, table_paths: list[str]) -> str:
    hasher = hashlib.sha256()
    for relative in sorted(table_paths):
        hasher.update(relative.encode("utf-8"))
        hasher.update((package / relative).read_bytes())
    return hasher.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=Path("config/canonical-corpus.v1.json"))
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--compare-root", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    if args.output_root.exists() and any(args.output_root.iterdir()):
        raise SystemExit("refusing rebuild: output root must be empty")
    args.output_root.mkdir(parents=True, exist_ok=True)
    corpus = json.loads(args.manifest.read_text(encoding="utf-8"))
    if len(corpus.get("order", [])) != 13 or len(set(corpus.get("order", []))) != 13:
        raise SystemExit("refusing rebuild: governed corpus must contain exactly 13 unique packages")
    results = []
    table_paths = [path for path in json.loads((Path(__file__).resolve().parents[1] / "contracts/canonical/v1/canonical-model.json").read_text(encoding="utf-8"))["tables"]]
    for package_name in corpus["order"]:
        source = args.source_root / package_name
        output = args.output_root / package_name
        family = {"T": "ACADEMY", "P": "PUPPY", "A": "ADULT", "S": "SENIOR"}[package_name[0]]
        converter_id = json.loads((Path(__file__).resolve().parents[1] / "config/converters/family-mappings.v1.json").read_text(encoding="utf-8"))["families"][family]["converter"]
        converter = registry.resolve(converter_id)
        if converter.family != family:
            raise SystemExit(f"converter family mismatch: {converter_id}")
        source_manifest = json.loads((source / "manifest.json").read_text(encoding="utf-8"))
        if source_manifest.get("package_name") not in (None, package_name):
            raise SystemExit(f"source package identity mismatch: {package_name}")
        converter.convert(source, output, {"source_dialect": converter.source_dialect, "case_id": source_manifest["case_id"], "case_version": source_manifest["case_version"], "snapshot_version": source_manifest["snapshot_version"]})
        missing = [relative for relative in table_paths if not (output / relative).is_file()]
        if missing:
            raise SystemExit(f"incomplete canonical output for {package_name}: {missing[:3]}")
        canonical_digest = package_digest(output, table_paths)
        item = {"package": package_name, "family": family, "converter": converter_id, "source_digest": digest(source / "manifest.json"), "output_digest": digest(output / "manifest.json"), "canonical_content_digest": canonical_digest}
        if args.compare_root:
            expected = package_digest(args.compare_root / package_name, table_paths)
            item["comparison_digest"] = expected
            item["deterministic_match"] = canonical_digest == expected
            if not item["deterministic_match"]:
                raise SystemExit(f"deterministic rebuild mismatch: {package_name}")
        results.append(item)
    report = {"schema_version": "1.0.0", "manifest": str(args.manifest), "package_count": len(results), "results": results, "status": "pass", "evidence_scope": "source-to-canonical-rebuild"}
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
