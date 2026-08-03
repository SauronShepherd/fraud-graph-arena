from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class FgaError(Exception):
    """A deliberate, player-safe application failure."""

    code: str
    title: str
    detail: str
    status: int
    recovery: str | None = None
    context: dict[str, Any] | None = None

    def __str__(self) -> str:
        return f"{self.code}: {self.detail}"


class NotFoundError(FgaError):
    def __init__(self, *, code: str, title: str, detail: str) -> None:
        super().__init__(code=code, title=title, detail=detail, status=404)


class ConflictError(FgaError):
    def __init__(
        self,
        *,
        code: str,
        title: str,
        detail: str,
        recovery: str | None = None,
    ) -> None:
        super().__init__(
            code=code,
            title=title,
            detail=detail,
            status=409,
            recovery=recovery,
        )


class InvalidRequestError(FgaError):
    def __init__(
        self,
        *,
        code: str,
        title: str,
        detail: str,
        recovery: str | None = None,
    ) -> None:
        super().__init__(
            code=code,
            title=title,
            detail=detail,
            status=400,
            recovery=recovery,
        )
