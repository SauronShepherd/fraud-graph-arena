from __future__ import annotations

from typing import Any

from fraud_graph_arena.case_packages import CasePackage, CasePackageRegistry
from fraud_graph_arena.narrative.domain import ComicKind, ComicPage, ComicSequence


def _page(package: CasePackage, raw: dict[str, Any]) -> ComicPage:
    asset_ref = str(raw["asset_ref"])
    asset_path = package.assets.get(asset_ref)
    if not asset_path:
        raise ValueError(f"{package.case_id} narrative asset reference is not declared: {asset_ref}")
    caption = str(raw["caption"])
    return ComicPage(
        id=str(raw["id"]),
        position=int(raw["position"]),
        title=str(raw["title"]),
        narration=caption,
        image_url=f"/assets/{asset_path}",
        alt_text=str(raw["alt_text"]),
        caption=caption,
        transcript=str(raw["transcript"]),
        audio_asset_id=raw.get("audio_asset_id"),
    )


def _pages(package: CasePackage, scope: dict[str, Any]) -> tuple[ComicPage, ...]:
    return tuple(_page(package, item) for item in scope["panels"])


def _from_manifest(package: CasePackage) -> tuple[ComicSequence, ComicSequence]:
    manifest = package.narrative
    opening = manifest["opening"]
    closing = manifest["closing"]
    audio_ids = tuple(str(item["id"]) for item in manifest["audio"]["assets"] if item.get("enabled"))
    opening_sequence = ComicSequence(
        id=str(opening["sequence_id"]),
        case_id=package.case_id,
        case_version=package.case_version,
        kind=ComicKind.OPENING,
        skippable=bool(opening["skippable"]),
        pages=_pages(package, opening),
        fictionalization_statement=str(manifest["fictionalization_statement"]),
        reduced_motion_behavior=str(opening["reduced_motion_behavior"]),
        preload_next=bool(opening["preload_next"]),
        audio_asset_ids=audio_ids,
    )
    variants = {str(name).upper(): _pages(package, scope) for name, scope in closing["variants"].items()}
    closing_sequence = ComicSequence(
        id=str(closing["sequence_id"]),
        case_id=package.case_id,
        case_version=package.case_version,
        kind=ComicKind.CLOSING,
        skippable=bool(closing["skippable"]),
        pages=_pages(package, closing),
        variants=variants,
        fictionalization_statement=str(manifest["fictionalization_statement"]),
        reduced_motion_behavior=str(closing["reduced_motion_behavior"]),
        preload_next=bool(closing["preload_next"]),
        audio_asset_ids=audio_ids,
    )
    return opening_sequence, closing_sequence


def _fallback(package: CasePackage) -> tuple[ComicSequence, ComicSequence]:
    """Keep older local packages playable while they migrate to FGA-15 metadata."""

    opening = ComicSequence(
        id=package.briefing["opening_sequence_id"],
        case_id=package.case_id,
        case_version=package.case_version,
        kind=ComicKind.OPENING,
        skippable=True,
        pages=(ComicPage(
            id=f"{package.case_id}_OPENING_01",
            position=1,
            title=package.title,
            narration=package.description,
            image_url=f"/assets/{package.assets['cover']}",
            alt_text=f"Opening case-package illustration for {package.title}.",
        ),),
    )
    closing = ComicSequence(
        id=package.briefing["closing_sequence_id"],
        case_id=package.case_id,
        case_version=package.case_version,
        kind=ComicKind.CLOSING,
        skippable=True,
        pages=(ComicPage(
            id=f"{package.case_id}_CLOSING_01",
            position=1,
            title="Case Receipt",
            narration="The package records the published evidence, the player decision and the versioned result.",
            image_url=f"/assets/{package.assets['infographic']}",
            alt_text=f"Closing case-package illustration for {package.title}.",
        ),),
    )
    return opening, closing


class InMemoryNarrativeRepository:
    """Load spoiler-safe narrative sequences from declarative case packages."""

    def __init__(self, package_registry: CasePackageRegistry | None = None) -> None:
        registry = package_registry or CasePackageRegistry()
        sequences: list[ComicSequence] = []
        for package in registry.all():
            if package.narrative:
                sequences.extend(_from_manifest(package))
            else:
                sequences.extend(_fallback(package))
        self._sequences = tuple(sequences)

    def get_sequence(
        self,
        *,
        case_id: str,
        case_version: str,
        kind: ComicKind,
    ) -> ComicSequence | None:
        normalized_case_id = case_id.strip().upper()
        return next(
            (
                item
                for item in self._sequences
                if item.case_id == normalized_case_id
                and item.case_version == case_version
                and item.kind == kind
            ),
            None,
        )
