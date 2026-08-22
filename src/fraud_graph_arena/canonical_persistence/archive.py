from __future__ import annotations
from pathlib import Path, PurePosixPath
from zipfile import ZipFile, ZipInfo
import stat

class ArchiveSafetyError(ValueError): pass

def _safe_name(info: ZipInfo) -> str:
    raw = info.filename.replace("\\", "/")
    path = PurePosixPath(raw)
    if path.is_absolute() or (bool(path.parts) and ":" in path.parts[0]):
        raise ArchiveSafetyError("absolute archive path")
    normalized = str(path)
    if normalized in ("", ".") or any(part == ".." for part in path.parts):
        raise ArchiveSafetyError("archive path traversal")
    return normalized

def safe_extract(archive: Path, destination: Path, *, max_members: int = 128, max_bytes: int = 100_000_000, max_ratio: int = 200) -> list[Path]:
    with ZipFile(archive) as zipped:
        if len(zipped.infolist()) > max_members: raise ArchiveSafetyError("archive member limit exceeded")
        names: set[str] = set(); total = 0; result = []
        for info in zipped.infolist():
            name = _safe_name(info)
            mode = (info.external_attr >> 16) & 0xFFFF
            if mode and (stat.S_ISLNK(mode) or stat.S_ISSOCK(mode) or stat.S_ISFIFO(mode)):
                raise ArchiveSafetyError("archive contains unsupported special file")
            if name in names: raise ArchiveSafetyError("duplicate normalized archive path")
            names.add(name); total += info.file_size
            if total > max_bytes: raise ArchiveSafetyError("archive byte limit exceeded")
            if info.compress_size and info.file_size / info.compress_size > max_ratio: raise ArchiveSafetyError("suspicious compression ratio")
            target = (destination / name).resolve()
            target.relative_to(destination.resolve())
            if info.is_dir(): target.mkdir(parents=True, exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                with zipped.open(info) as src, target.open("wb") as dst: dst.write(src.read())
                result.append(target)
        return result
