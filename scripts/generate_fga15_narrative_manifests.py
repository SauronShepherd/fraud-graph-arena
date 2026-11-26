"""Add the FGA-15 narrative experience contract to every published package."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
VARIANTS = ("EXCELLENT", "PARTIAL", "FAILED")


def _panel(case_id: str, position: int, title: str, caption: str, asset_ref: str) -> dict[str, Any]:
    panel_id = f"{case_id}_P{position:02d}_{title.upper().replace(' ', '_')}"
    return {
        "id": panel_id[:128],
        "position": position,
        "title": title,
        "caption": caption,
        "transcript": caption,
        "asset_ref": asset_ref,
        "alt_text": f"A synthetic noir case illustration for {case_id}: {title.lower()}.",
        "audio_asset_id": None,
    }


def _audio(case_id: str) -> dict[str, Any]:
    def asset(asset_id: str, asset_type: str, purpose: str, priority: int, max_concurrency: int) -> dict[str, Any]:
        return {
            "id": f"{case_id.lower()}-{asset_id}",
            "type": asset_type,
            "purpose": purpose,
            "file": None,
            "source": "Optional audio slot documented in FGA-15; no binary shipped in this release.",
            "tool_or_performer": "None; intentionally disabled",
            "prompt_or_script": f"Reserved, non-authoritative {purpose.lower()} slot for {case_id}.",
            "license": "NOT_SHIPPED",
            "duration_ms": 0,
            "loudness_target_lufs": -18,
            "transcript": "",
            "subtitle_file": None,
            "loop_points": {"start_ms": 0, "end_ms": 0},
            "version": "fga15-audio-v1",
            "approval_status": "DEFERRED_OPTIONAL",
            "enabled": False,
            "priority": priority,
            "max_concurrency": max_concurrency,
            "fallback_behavior": "TEXT_ONLY" if asset_type in {"VOICE", "RADIO"} else "VISUAL_ONLY",
        }

    return {
        "enabled": False,
        "radio": {"enabled": False, "asset_id": None, "replayable": True, "required": False, "transcript": ""},
        "buses": {"master": 1.0, "music": 0.7, "voice": 1.0, "effects": 0.8},
        "assets": [
            asset("menu-loop", "MUSIC", "Main menu loop", 1, 1),
            asset("case-voice", "VOICE", "Case acceptance voice", 2, 1),
            asset("panel-transition", "EFFECT", "Panel transition", 3, 2),
            asset("verdict-cue", "EFFECT", "Verdict cue", 4, 1),
        ],
    }


def narrative(manifest: dict[str, Any]) -> dict[str, Any]:
    case_id = str(manifest["case_id"])
    title = str(manifest["title"])
    if case_id == "ACADEMY_001":
        opening_panels = [
            _panel(case_id, 1, "The Academy Door", "Hercule Perrot reports for training. The ranked case files remain sealed upstairs, where spoilers cannot develop bad habits.", "cover"),
            _panel(case_id, 2, "A Board with Nothing to Hide", "Inside waits an empty evidence board. The first lesson is not to solve a fraud, but to prove the whole journey reaches the correct room.", "cover"),
        ]
    else:
        opening_panels = [
            _panel(case_id, 1, "Assignment accepted", f"{title} entered the office. Hercule could inspect the evidence, or merely admire the folder.", "cover"),
        ]
    closure_text = {
        "EXCELLENT": "The evidence held together, the supported conclusion stayed bounded and the closing file could be stamped without inventing a culprit.",
        "PARTIAL": "The investigation found a useful direction, but the file still carries an unresolved edge. A lead is not a license to overstate it.",
        "FAILED": "The board recorded a failed conclusion. The transcript remains available, the evidence remains safe and the next attempt can begin without rewriting the case.",
    }
    variants = {
        variant: {"panels": [_panel(case_id, 1, f"{variant.title()} receipt", closure_text[variant], "infographic")]}
        for variant in VARIANTS
    }
    return {
        "schema_version": "fga15-narrative-v1",
        "fictionalization_statement": "All people, organisations, accounts and events in this playable package are synthetic; real mechanisms are discussed separately from gameplay.",
        "opening": {
            "sequence_id": str(manifest["briefing"]["opening_sequence_id"]),
            "skippable": True,
            "preload_next": True,
            "reduced_motion_behavior": "Keep the current panel visible and remove transition motion.",
            "panels": opening_panels,
        },
        "closing": {
            "sequence_id": str(manifest["briefing"]["closing_sequence_id"]),
            "skippable": True,
            "preload_next": True,
            "reduced_motion_behavior": "Keep the current receipt visible and remove transition motion.",
            "panels": variants["EXCELLENT"]["panels"],
            "variants": variants,
        },
        "audio": _audio(case_id),
    }


def build(*, write: bool) -> dict[str, Any]:
    changed: list[str] = []
    for path in sorted((ROOT / "case-packages").glob("*/manifest.json")):
        manifest = json.loads(path.read_text(encoding="utf-8"))
        manifest["narrative"] = narrative(manifest)
        if write:
            path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        changed.append(path.parent.name)
    return {"packages": len(changed), "package_ids": changed, "written": write}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    print(json.dumps(build(write=args.write), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
