from __future__ import annotations

from pathlib import PurePosixPath

from starlette.exceptions import HTTPException
from starlette.responses import Response
from starlette.staticfiles import StaticFiles


class SpaStaticFiles(StaticFiles):
    """Serve the built React app and fall back to index.html for client routes.

    Missing asset-like paths retain a real 404. Only extensionless browser routes are
    sent to the SPA shell, which is what makes a board URL refresh-safe.
    """

    @staticmethod
    def _is_client_route(path: str) -> bool:
        return PurePosixPath(path).suffix == ""

    async def get_response(self, path: str, scope: dict) -> Response:  # type: ignore[override]
        try:
            response = await super().get_response(path, scope)
        except HTTPException as exc:
            if exc.status_code != 404 or not self._is_client_route(path):
                raise
            return await super().get_response("index.html", scope)
        if response.status_code == 404 and self._is_client_route(path):
            return await super().get_response("index.html", scope)
        return response
