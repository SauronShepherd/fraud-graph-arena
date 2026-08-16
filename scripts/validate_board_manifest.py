from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).parents[1]
MANIFEST = ROOT / "apps" / "web" / "public" / "assets" / "board" / "v1" / "manifest.json"

def validate(path: Path = MANIFEST) -> list[str]:
    errors: list[str] = []
    data = json.loads(path.read_text(encoding="utf-8"))
    if not data.get("template_id") or not data.get("template_version"): errors.append("template identity/version required")
    if data.get("canvas") != {"width": 1600, "height": 900}: errors.append("canvas must be exactly 1600x900")
    regions = path.parent / "regions.json"
    if not regions.is_file(): errors.append("regions.json is required")
    else:
        region_data = json.loads(regions.read_text(encoding="utf-8"))
        if region_data.get("template_version") != data.get("template_version"): errors.append("manifest and region template versions differ")
        if not region_data.get("stacking"): errors.append("stacking levels required")
        canvas = data["canvas"]
        for name, region in region_data.get("regions", {}).items():
            if any(region.get(key, -1) < 0 for key in ("x", "y", "width", "height")): errors.append(f"invalid region geometry: {name}")
            if region["x"] + region["width"] > canvas["width"] or region["y"] + region["height"] > canvas["height"]: errors.append(f"region outside canvas: {name}")
    assets = data.get("assets", [])
    if len({asset.get("id") for asset in assets}) != len(assets): errors.append("asset IDs must be unique")
    allowed_layers = {"scene", "typewriter", "paper", "graph", "decoration"}
    root = path.parent.resolve()
    for asset in assets:
        target = (path.parent / asset.get("path", "")).resolve()
        if root not in target.parents and target != root: errors.append(f"asset escapes root: {asset.get('path')}")
        if not target.is_file(): errors.append(f"missing asset: {asset.get('path')}")
        if asset.get("layer") not in allowed_layers: errors.append(f"unknown layer: {asset.get('layer')}")
        if not asset.get("version") or not asset.get("dimensions"): errors.append(f"incomplete asset metadata: {asset.get('id')}")
    return errors

if __name__ == "__main__":
    errors = validate()
    if errors:
        raise SystemExit("\n".join(errors))
    print("board manifest valid")
